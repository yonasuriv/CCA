#!/usr/bin/env python3
# Schema v4: v3 plus system.schemas, agent.rules, and declared boundary context
# files. These tests pin the frozen v4 additions, the boundary-context exemptions,
# and that v4 targets audit, generate, and resolve end to end via a minimal manifest.
from __future__ import annotations

import copy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import audit  # noqa: E402
from schema import compose_manifest, contract_fingerprint, contract_path, load_manifest, normalize_prose  # noqa: E402

PIN = contract_fingerprint("hybrid-workspace", 4)
TEMPLATE = load_manifest(ROOT / "WORKSPACE.yaml")
BINDINGS = {s["key"]: s["binding"] for s in TEMPLATE["slots"] if s["key"] != "workspace.schema"}
BINDINGS.update({"system.schemas": "_runtime/schemas/", "agent.rules": "_runtime/rules/"})


def manifest(**extra) -> dict:
    data = {
        "extends": {"profile": "hybrid-workspace", "schema_version": 4, "fingerprint": PIN},
        "cca": {"specification": "1.5.0"},
        "bindings": dict(BINDINGS),
    }
    data.update(extra)
    return data


def workspace(data: dict | None = None) -> Path:
    root = Path(tempfile.mkdtemp(prefix="cca-v4-"))
    (root / "workspace.yaml").write_text(yaml.safe_dump(data or manifest(), sort_keys=False), encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").replace("WORKSPACE.yaml", "workspace.yaml").replace("workspace-contract:v3", "workspace-contract:v4")
    (root / "AGENTS.md").write_text(agents, encoding="utf-8")
    return root


def run(tool: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(ROOT / tool), *args], text=True, capture_output=True, check=False)


def reference(root: Path) -> tuple[Path, Path]:
    composed = compose_manifest(load_manifest(root / "workspace.yaml"), "workspace.yaml")
    slots = {s["key"]: s["binding"] for s in composed["slots"]}
    return root / slots["knowledge.reference"], root / slots["reference.collected"]


class ContractTests(unittest.TestCase):
    def test_v4_is_v3_plus_two_keys_and_boundary_context(self) -> None:
        v3 = load_manifest(contract_path("hybrid-workspace", 3))
        v4 = load_manifest(contract_path("hybrid-workspace", 4))
        self.assertEqual(v4["boundary_context"], audit.EXPECTED_BOUNDARY_CONTEXT)
        added = [s for s in v4["slots"] if s["key"] in audit.FROZEN_V4_EXTENSION]
        self.assertEqual({s["key"] for s in added}, set(audit.FROZEN_V4_EXTENSION))
        for slot in added:
            frozen = audit.FROZEN_V4_EXTENSION[slot["key"]]
            self.assertEqual({k: slot[k] for k in frozen}, frozen)
        rest = copy.deepcopy(v4)
        rest["slots"] = [s for s in rest["slots"] if s["key"] not in audit.FROZEN_V4_EXTENSION]
        rest.pop("boundary_context")
        rest["schema_version"] = 3
        self.assertEqual(normalize_prose(rest), normalize_prose(v3))

    def test_v4_needs_cca_1_5(self) -> None:
        with self.assertRaisesRegex(ValueError, "hybrid-workspace@4 manifest must declare cca.specification >= 1.5.0"):
            compose_manifest(manifest(cca={"specification": "1.4.0"}), "workspace.yaml")

    def test_new_bindings_are_required(self) -> None:
        data = manifest()
        del data["bindings"]["agent.rules"]
        with self.assertRaisesRegex(ValueError, "agent.rules"):
            compose_manifest(data, "workspace.yaml")


class WorkspaceTests(unittest.TestCase):
    def audit(self, root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return run("audit.py", "--target", str(root), *extra)

    def test_minimal_v4_workspace_audits_generates_and_resolves(self) -> None:
        root = workspace()
        generated = run("generate.py", "--target", str(root))
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        self.assertEqual(run("generate.py", "--target", str(root), "--check").returncode, 0)
        result = self.audit(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("schema v4", result.stdout)
        resolved = run("resolve.py", "--target", str(root), "--key", "agent.rules", "--format", "relative")
        self.assertEqual(resolved.stdout.strip(), "_runtime/rules/")
        router = (root / "CONTEXT.md").read_text(encoding="utf-8")
        self.assertIn("`system.schemas`", router)
        self.assertIn("read its `CONTEXT.md` when present", router)

    def test_boundary_context_is_not_a_loose_or_unprovenanced_source(self) -> None:
        root = workspace()
        parent, collected = reference(root)
        collected.mkdir(parents=True)
        (parent / "CONTEXT.md").write_text("# Sources\n", encoding="utf-8")
        (collected / "CONTEXT.md").write_text("# Collected\n", encoding="utf-8")
        result = self.audit(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_other_loose_files_and_nested_context_still_fail(self) -> None:
        root = workspace()
        parent, collected = reference(root)
        (collected / "clippings").mkdir(parents=True)
        (parent / "notes.md").write_text("loose\n", encoding="utf-8")
        (collected / "clippings" / "CONTEXT.md").write_text("not a binding root\n", encoding="utf-8")
        output = self.audit(root).stdout
        self.assertIn("loose/unknown source entry", output)
        self.assertIn("clippings/CONTEXT.md", output)

    def test_boundary_context_is_rejected_outside_v4(self) -> None:
        full = copy.deepcopy(TEMPLATE)
        full["boundary_context"] = dict(audit.EXPECTED_BOUNDARY_CONTEXT)
        fails, _ = audit.validate_schema(full, check_filesystem=False)
        self.assertTrue(any("boundary_context is a schema v4 extension" in f for f in fails), fails)

    def test_v4_self_test_rejects_contract_mutations(self) -> None:
        composed = compose_manifest(manifest(), "workspace.yaml")
        root = workspace()
        failures, _ = audit.run_self_test(composed, root)
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
