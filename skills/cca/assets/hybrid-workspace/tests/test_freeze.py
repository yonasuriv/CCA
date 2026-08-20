#!/usr/bin/env python3
# Regression/freeze tests for the workspace schema toolchain.
# These are black-box where possible: they verify observable contract behavior.
from __future__ import annotations

import copy
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_FILES = [
    "WORKSPACE.yaml",
    "AGENTS.md",
]


def run(*args: str, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    command = list(args)
    if len(command) >= 2 and command[0] == sys.executable and command[1] in {"generate.py", "audit.py"}:
        tool = ROOT / command[1]
        command = [sys.executable, str(tool), "--target", str(cwd), *command[2:]]
    return subprocess.run(
        command, cwd=cwd, env=env, text=True, capture_output=True, check=False
    )


def make_copy(*, with_agents: bool = True) -> Path:
    root = Path(tempfile.mkdtemp(prefix="workspace-freeze-"))
    for name in PACKAGE_FILES:
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, root / name)
    if not with_agents:
        (root / "AGENTS.md").unlink(missing_ok=True)
    elif not (root / "AGENTS.md").exists():
        raise RuntimeError("release fixture is missing AGENTS.md")
    return root


class FreezeToolchainTests(unittest.TestCase):
    def tearDown(self) -> None:
        # temp dirs are intentionally independent; Python cleans OS temp eventually.
        pass

    def test_audit_is_cwd_independent(self) -> None:
        target = make_copy()
        outside = Path(tempfile.mkdtemp(prefix="workspace-outside-"))
        result = run(sys.executable, str(ROOT / "audit.py"), "--target", str(target), cwd=outside)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_generate_check_detects_context_drift(self) -> None:
        root = make_copy()
        generated = run(sys.executable, "generate.py", cwd=root)
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        with (root / "CONTEXT.md").open("a", encoding="utf-8") as fh:
            fh.write("\nDRIFT\n")
        checked = run(sys.executable, "generate.py", "--check", cwd=root)
        self.assertNotEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("drift", (checked.stdout + checked.stderr).lower())
        self.assertIn("CONTEXT.md", checked.stdout + checked.stderr)

    def test_generate_check_detects_spec_drift(self) -> None:
        root = make_copy()
        generated = run(sys.executable, "generate.py", cwd=root)
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        with (root / "SPEC.md").open("a", encoding="utf-8") as fh:
            fh.write("\nDRIFT\n")
        checked = run(sys.executable, "generate.py", "--check", cwd=root)
        self.assertNotEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("SPEC.md", checked.stdout + checked.stderr)

    def test_mkdirs_is_root_anchored_and_never_fabricates_authority_files(self) -> None:
        root = make_copy(with_agents=False)
        result = run(sys.executable, "generate.py", cwd=root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        workspace_before = (root / "WORKSPACE.yaml").read_bytes()
        # Remove generated/human files to prove mkdirs will not fabricate them.
        for name in ("AGENTS.md", "CONTEXT.md", "SPEC.md"):
            (root / name).unlink(missing_ok=True)
        outside = Path(tempfile.mkdtemp(prefix="workspace-outside-"))
        ran = run("bash", str(root / "mkdirs.sh"), "--all", cwd=outside)
        self.assertEqual(ran.returncode, 0, ran.stdout + ran.stderr)
        self.assertTrue((root / "00-wiki").is_dir())
        self.assertTrue((root / "_state" / "tasks").is_dir())
        self.assertFalse((outside / "00-wiki").exists())
        self.assertFalse((outside / "WORKSPACE.yaml").exists())
        self.assertEqual((root / "WORKSPACE.yaml").read_bytes(), workspace_before)
        self.assertFalse((root / "AGENTS.md").exists())
        self.assertFalse((root / "CONTEXT.md").exists())
        self.assertFalse((root / "SPEC.md").exists())
        self.assertTrue((root / "_state" / "NOW.md").exists())

    def test_duplicate_yaml_keys_are_rejected(self) -> None:
        root = make_copy()
        text = (root / "WORKSPACE.yaml").read_text()
        text = text.replace("schema_version: 1", "schema_version: 1\nschema_version: 999", 1)
        (root / "WORKSPACE.yaml").write_text(text)
        result = run(sys.executable, "audit.py", cwd=root)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("duplicate", (result.stdout + result.stderr).lower())

    def test_context_renders_effective_operations_not_raw_write(self) -> None:
        root = make_copy()
        result = run(sys.executable, "generate.py", cwd=root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        context = (root / "CONTEXT.md").read_text()
        router_row = next(line for line in context.splitlines() if "`context.router`" in line)
        upstream_row = next(line for line in context.splitlines() if "`project.upstream`" in line)
        memory_row = next(line for line in context.splitlines() if "`state.memory`" in line)
        self.assertIn("regenerate", router_row)
        self.assertNotRegex(router_row, r"\| write \|")
        self.assertIn("reconstruct", upstream_row)
        self.assertNotRegex(upstream_row, r"\| write \|")
        self.assertIn("append", memory_row)

    def test_known_contract_corruptions_fail_audit(self) -> None:
        mutations = {
            "required durable knowledge made optional": (
                "requirement: required\n    description: >\n      Distilled, synthesized",
                "requirement: optional\n    description: >\n      Distilled, synthesized",
            ),
            "human asset made agent writable": (
                "key: system.assets\n    binding: _runtime/assets/",
                "key: system.assets\n    binding: _runtime/assets/",
            ),
            "durable graph removed": (
                "key: knowledge.durable",
                "key: knowledge.durable",
            ),
            "router authority no longer derived": (
                "key: context.router",
                "key: context.router",
            ),
            "crosswalk removed": ("crosswalk:\n", "crosswalk_removed:\n"),
            "mutable delete semantics changed": ("delete: allowed\n  regenerate:", "delete: prohibited\n  regenerate:"),
        }

        for label, (old, new) in mutations.items():
            with self.subTest(label=label):
                root = make_copy()
                text = (root / "WORKSPACE.yaml").read_text()
                if label == "human asset made agent writable":
                    marker = "key: system.assets"
                    pos = text.index(marker)
                    end = text.index("\n\n", pos)
                    block = text[pos:end]
                    block = block.replace("agent_access: read-only", "agent_access: write")
                    text = text[:pos] + block + text[end:]
                elif label == "durable graph removed":
                    marker = "key: knowledge.durable"
                    pos = text.index(marker)
                    end = text.index("\n\n", pos)
                    block = text[pos:end]
                    block = block.replace("link_target: graph", "link_target: none")
                    text = text[:pos] + block + text[end:]
                elif label == "router authority no longer derived":
                    marker = "key: context.router"
                    pos = text.index(marker)
                    end = text.index("\n\n", pos)
                    block = text[pos:end]
                    block = block.replace("authority: derived", "authority: shared")
                    text = text[:pos] + block + text[end:]
                else:
                    self.assertIn(old, text, f"fixture setup failed for {label}")
                    text = text.replace(old, new, 1)
                (root / "WORKSPACE.yaml").write_text(text)
                result = run(sys.executable, "audit.py", cwd=root)
                self.assertNotEqual(
                    result.returncode,
                    0,
                    f"corruption passed audit: {label}\n{result.stdout}{result.stderr}",
                )

    def test_schema_contains_archive_identity_and_external_trust_contracts(self) -> None:
        data = yaml.safe_load((ROOT / "WORKSPACE.yaml").read_text())
        invariants = data.get("invariants", {})
        self.assertIn("archive_identity", invariants)
        self.assertIn("external_boundary_trust", invariants)
        archive = data.get("archive_contract", {})
        self.assertEqual(archive.get("manifest"), ".archive.yaml")
        for field in ("semantic_role", "boundary", "boundary_class", "original_binding", "archived_at", "archived_by"):
            self.assertIn(field, archive.get("required_fields", []))
        trust = data.get("boundary_trust", {})
        self.assertEqual(trust.get("project.upstream"), "external-untrusted")

    def test_tasks_are_non_deletable_and_append_has_no_generic_compaction_escape(self) -> None:
        data = yaml.safe_load((ROOT / "WORKSPACE.yaml").read_text())
        tasks = next(s for s in data["slots"] if s["key"] == "state.tasks")
        task_policy = data["policy_definitions"][tasks["mutability"]]
        self.assertEqual(task_policy.get("delete"), "prohibited")
        self.assertNotIn("compaction", data["policy_definitions"]["append"])
        memory_ops = data.get("privileged_operations", {}).get("state.memory", {})
        self.assertEqual(memory_ops.get("compaction"), "human-authorized")

    def test_mkdirs_default_materializes_only_required_slots(self) -> None:
        root = make_copy()
        generated = run(sys.executable, "generate.py", cwd=root)
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        ran = run("bash", "mkdirs.sh", cwd=root)
        self.assertEqual(ran.returncode, 0, ran.stdout + ran.stderr)
        self.assertTrue((root / "00-wiki").is_dir())
        self.assertTrue((root / "10-inbox").is_dir())
        self.assertTrue((root / "20-sources").is_dir())
        self.assertFalse((root / "30-areas").exists())
        self.assertFalse((root / "40-projects").exists())
        self.assertFalse((root / "50-outputs").exists())
        self.assertFalse((root / "90-archive").exists())
        self.assertFalse((root / "_state").exists())
        self.assertFalse((root / "_runtime").exists())

    def test_nested_binding_precedence_is_frozen(self) -> None:
        data = yaml.safe_load((ROOT / "WORKSPACE.yaml").read_text())
        invariants = data.get("invariants", {})
        self.assertIn("binding_precedence", invariants)
        text = invariants["binding_precedence"]
        self.assertIn("most-specific", text)
        self.assertIn("Ancestor", text)

    def test_audit_self_test_exercises_exhaustive_frozen_field_mutations(self) -> None:
        result = run(sys.executable, str(ROOT / "audit.py"), "--self-test", cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("exhaustive frozen-field mutations rejected", result.stdout)

    def test_binding_change_is_nonbreaking_and_regenerates_everywhere(self) -> None:
        root = make_copy()
        text = (root / "WORKSPACE.yaml").read_text()
        marker = "key: knowledge.durable"
        pos = text.index(marker)
        end = text.index("\n\n", pos)
        block = text[pos:end].replace("binding: 00-wiki/", "binding: 05-knowledge/")
        text = text[:pos] + block + text[end:]
        (root / "WORKSPACE.yaml").write_text(text)
        audited = run(sys.executable, "audit.py", cwd=root)
        self.assertEqual(audited.returncode, 0, audited.stdout + audited.stderr)
        generated = run(sys.executable, "generate.py", cwd=root)
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        for name in ("paths.sh", "CONTEXT.md", "SPEC.md"):
            rendered = (root / name).read_text()
            self.assertIn("05-knowledge/", rendered, name)
        checked = run(sys.executable, "generate.py", "--check", cwd=root)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_symlink_binding_escape_is_rejected(self) -> None:
        root = make_copy()
        outside = Path(tempfile.mkdtemp(prefix="workspace-escape-"))
        (root / "escape").symlink_to(outside, target_is_directory=True)
        text = (root / "WORKSPACE.yaml").read_text()
        marker = "key: output.artifact"
        pos = text.index(marker)
        end = text.index("\n\n", pos)
        block = text[pos:end].replace("binding: 50-outputs/", "binding: escape/outputs/")
        text = text[:pos] + block + text[end:]
        (root / "WORKSPACE.yaml").write_text(text)
        result = run(sys.executable, "audit.py", cwd=root)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("escapes workspace", (result.stdout + result.stderr).lower())

    def test_missing_or_empty_agents_fails_freeze_check(self) -> None:
        for value in (None, ""):
            with self.subTest(value=value):
                root = make_copy()
                if value is None:
                    (root / "AGENTS.md").unlink()
                else:
                    (root / "AGENTS.md").write_text(value)
                generated = run(sys.executable, "generate.py", cwd=root)
                self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
                checked = run(sys.executable, "generate.py", "--check", cwd=root)
                self.assertNotEqual(checked.returncode, 0, checked.stdout + checked.stderr)
                self.assertIn("AGENTS.md", checked.stdout + checked.stderr)

    def test_spec_documents_all_closed_vocabularies_and_trust_semantics(self) -> None:
        root = make_copy()
        generated = run(sys.executable, "generate.py", cwd=root)
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        spec = (root / "SPEC.md").read_text()
        for heading in (
            "## Category semantics",
            "## Arity semantics",
            "## Indexed semantics",
            "## Authority semantics",
            "## Agent access semantics",
            "## Link target semantics",
            "## Requirement semantics",
            "### Trust meanings",
        ):
            self.assertIn(heading, spec)
        self.assertIn("`external-untrusted`", spec)
        self.assertIn("`boundary_class` may be null", spec)

    def test_generated_spec_is_outside_human_knowledge_index(self) -> None:
        root = make_copy()
        generated = run(sys.executable, "generate.py", cwd=root)
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        excludes = (root / "obsidian-excludes.txt").read_text()
        self.assertIn("SPEC.md", excludes.splitlines())
        data = yaml.safe_load((root / "WORKSPACE.yaml").read_text())
        contract = data.get("generation_contract", {})
        self.assertIn("SPEC.md", contract.get("derived", []))
        self.assertEqual(contract.get("index_policy", {}).get("SPEC.md"), "disabled")

    def test_release_check_passes_from_outside_cwd(self) -> None:
        target = make_copy()
        generated = run(sys.executable, "generate.py", cwd=target)
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        outside = Path(tempfile.mkdtemp(prefix="workspace-outside-"))
        result = run(sys.executable, str(ROOT / "generate.py"), "--target", str(target), "--check", cwd=outside)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
