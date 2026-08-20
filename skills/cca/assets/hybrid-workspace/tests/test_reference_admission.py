#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))

import schema as schema_module  # noqa: E402


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd or PACKAGE,
        text=True,
        capture_output=True,
        check=False,
    )


def make_target() -> Path:
    target = Path(tempfile.mkdtemp(prefix="cca-reference-admission-"))
    for name in ("WORKSPACE.yaml", "AGENTS.md"):
        shutil.copy2(PACKAGE / name, target / name)
    return target


def load_target_schema(target: Path) -> dict:
    return yaml.safe_load((target / "WORKSPACE.yaml").read_text(encoding="utf-8"))


def slot_map(data: dict) -> dict[str, dict]:
    return {slot["key"]: slot for slot in data["slots"]}


def write_collected_file(target: Path, name: str = "paper.pdf", content: bytes = b"evidence") -> Path:
    collected = target / "20-sources" / "collected"
    collected.mkdir(parents=True, exist_ok=True)
    source = collected / name
    source.write_bytes(content)
    digest = hashlib.sha256(content).hexdigest()
    sidecar = source.with_name(source.name + ".source.yaml")
    sidecar.write_text(
        yaml.safe_dump(
            {
                "provenance": {
                    "acquired_by": "agent:test",
                    "acquisition_method": "web-fetch",
                    "origin": "https://example.test/paper.pdf",
                    "acquired_at": "2026-08-20T23:42:00+02:00",
                    "content_hash": f"sha256:{digest}",
                },
                "review": {"status": "unreviewed"},
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return source


class ReferenceAdmissionContractTests(unittest.TestCase):
    def test_v2_extends_without_mutating_frozen_v1_reference_role(self) -> None:
        data = yaml.safe_load((PACKAGE / "WORKSPACE.yaml").read_text(encoding="utf-8"))
        by = slot_map(data)
        self.assertEqual(data.get("schema_version"), 2)
        self.assertIn("reference.curated", by)
        self.assertIn("reference.collected", by)

        parent = by["knowledge.reference"]
        self.assertEqual(parent["binding"], "20-sources/")
        self.assertEqual(parent["mutability"], "immutable")
        self.assertEqual(parent["authority"], "human")
        self.assertEqual(parent["agent_access"], "read-only")
        self.assertEqual(parent["link_target"], "referenceable")

    def test_both_admission_classes_compose_to_knowledge_reference(self) -> None:
        data = yaml.safe_load((PACKAGE / "WORKSPACE.yaml").read_text(encoding="utf-8"))
        composition = data.get("classification_roles", {})
        self.assertEqual(composition.get("reference.curated"), "knowledge.reference")
        self.assertEqual(composition.get("reference.collected"), "knowledge.reference")
        self.assertEqual(composition.get("project.remote"), "work.project")
        self.assertFalse(any(slot["key"].startswith("research.") for slot in data["slots"]))

    def test_curated_is_agent_read_only_and_collected_is_add_child_only(self) -> None:
        data = schema_module.load_schema(PACKAGE / "WORKSPACE.yaml")
        by = slot_map(data)
        self.assertIn("reference.curated", by)
        self.assertIn("reference.collected", by)

        curated_ops = schema_module.effective_agent_operations(by["reference.curated"], data)
        collected_ops = schema_module.effective_agent_operations(by["reference.collected"], data)

        self.assertEqual(curated_ops, ["read"])
        self.assertIn("add-child", collected_ops)
        for forbidden in ("edit", "rename", "relocate", "delete", "reconstruct", "regenerate"):
            self.assertNotIn(forbidden, collected_ops)

    def test_most_specific_reference_class_policy_wins_over_parent(self) -> None:
        self.assertTrue(
            hasattr(schema_module, "resolve_slot_for_path"),
            "schema must expose most-specific binding resolution for policy checks",
        )
        data = schema_module.load_schema(PACKAGE / "WORKSPACE.yaml")
        resolver = getattr(schema_module, "resolve_slot_for_path")
        curated = resolver("20-sources/curated/paper.pdf", data)
        collected = resolver("20-sources/collected/paper.pdf", data)
        self.assertEqual(curated["key"], "reference.curated")
        self.assertEqual(collected["key"], "reference.collected")
        self.assertEqual(schema_module.effective_agent_operations(curated, data), ["read"])
        self.assertIn("add-child", schema_module.effective_agent_operations(collected, data))

    def test_direct_source_files_under_reference_parent_are_rejected(self) -> None:
        target = make_target()
        parent = target / "20-sources"
        parent.mkdir(parents=True, exist_ok=True)
        (parent / "loose.pdf").write_bytes(b"unclassified evidence")
        result = run(sys.executable, str(PACKAGE / "audit.py"), "--target", str(target))
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("loose", (result.stdout + result.stderr).lower())
        self.assertIn("reference.curated", result.stdout + result.stderr)
        self.assertIn("reference.collected", result.stdout + result.stderr)

    def test_collected_file_requires_provenance_and_hash_identity(self) -> None:
        target = make_target()
        collected = target / "20-sources" / "collected"
        collected.mkdir(parents=True, exist_ok=True)
        (collected / "paper.pdf").write_bytes(b"evidence")
        missing = run(sys.executable, str(PACKAGE / "audit.py"), "--target", str(target))
        self.assertNotEqual(missing.returncode, 0, missing.stdout + missing.stderr)
        self.assertIn("provenance", (missing.stdout + missing.stderr).lower())

        source = write_collected_file(target)
        valid = run(sys.executable, str(PACKAGE / "audit.py"), "--target", str(target))
        self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)

        source.write_bytes(b"mutated evidence")
        mutated = run(sys.executable, str(PACKAGE / "audit.py"), "--target", str(target))
        self.assertNotEqual(mutated.returncode, 0, mutated.stdout + mutated.stderr)
        self.assertIn("hash", (mutated.stdout + mutated.stderr).lower())

    def test_required_materialization_creates_both_reference_classes(self) -> None:
        target = make_target()
        generated = run(sys.executable, str(PACKAGE / "generate.py"), "--target", str(target))
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        made = run("bash", str(target / "mkdirs.sh"), cwd=target)
        self.assertEqual(made.returncode, 0, made.stdout + made.stderr)
        self.assertTrue((target / "20-sources" / "curated").is_dir())
        self.assertTrue((target / "20-sources" / "collected").is_dir())

    def test_generated_router_and_spec_preserve_role_classification_distinction(self) -> None:
        target = make_target()
        generated = run(sys.executable, str(PACKAGE / "generate.py"), "--target", str(target))
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        context = (target / "CONTEXT.md").read_text(encoding="utf-8")
        spec = (target / "SPEC.md").read_text(encoding="utf-8")
        combined = context + "\n" + spec
        self.assertIn("reference.curated", combined)
        self.assertIn("reference.collected", combined)
        self.assertIn("semantic.role = knowledge.reference", combined)
        self.assertIn("knowledge.durable", combined)
        self.assertIn("output.artifact", combined)
        self.assertNotIn("research.role", combined)
        checked = run(
            sys.executable,
            str(PACKAGE / "generate.py"),
            "--target",
            str(target),
            "--check",
        )
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_source_class_bindings_relocate_as_a_nested_unit(self) -> None:
        target = make_target()
        data = load_target_schema(target)
        replacements = {
            "knowledge.reference": "evidence/",
            "reference.curated": "evidence/admitted/",
            "reference.collected": "evidence/automatic/",
        }
        for slot in data["slots"]:
            if slot["key"] in replacements:
                slot["binding"] = replacements[slot["key"]]
        (target / "WORKSPACE.yaml").write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

        audited = run(sys.executable, str(PACKAGE / "audit.py"), "--target", str(target))
        self.assertEqual(audited.returncode, 0, audited.stdout + audited.stderr)
        generated = run(sys.executable, str(PACKAGE / "generate.py"), "--target", str(target))
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        combined = (target / "CONTEXT.md").read_text() + (target / "SPEC.md").read_text() + (target / "paths.sh").read_text()
        for binding in replacements.values():
            self.assertIn(binding, combined)
        self.assertNotIn("20-sources/curated/", combined)
        self.assertNotIn("20-sources/collected/", combined)

    def test_routing_meanings_remain_distinct(self) -> None:
        data = yaml.safe_load((PACKAGE / "WORKSPACE.yaml").read_text(encoding="utf-8"))
        contract = data.get("reference_contract", {})
        routing = contract.get("routing", {})
        self.assertEqual(routing.get("unclassified_incoming"), "context.capture")
        self.assertEqual(routing.get("preserved_evidence"), "knowledge.reference")
        self.assertEqual(routing.get("derived_synthesis"), "knowledge.durable")
        self.assertEqual(routing.get("external_deliverable"), "output.artifact")
        self.assertEqual(routing.get("finite_research_effort"), "work.project")


if __name__ == "__main__":
    unittest.main(verbosity=2)
