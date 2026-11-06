#!/usr/bin/env python3
# Minimal (extends) manifests: a workspace pins a bundled profile contract by
# semantic fingerprint and declares only bindings, identity, cca version,
# provenance aliases and access narrowing. These tests pin the composition rules,
# the fail-closed boundaries, and end-to-end audit/generate/resolve behavior.
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

from schema import (  # noqa: E402
    compose_manifest, contract_fingerprint, load_manifest, load_schema, minimize_manifest,
)

PIN = contract_fingerprint("hybrid-workspace", 3)


def minimal(**extra) -> dict:
    data = {"extends": {"profile": "hybrid-workspace", "schema_version": 3, "fingerprint": PIN}}
    data.update(extra)
    return data


def write_workspace(manifest: dict) -> Path:
    """Create a target with the manifest and the package's human control template."""
    root = Path(tempfile.mkdtemp(prefix="cca-minimal-"))
    (root / "workspace.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").replace("WORKSPACE.yaml", "workspace.yaml")
    (root / "AGENTS.md").write_text(agents, encoding="utf-8")
    return root


def run(tool: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(ROOT / tool), *args], text=True, capture_output=True, check=False)


class CompositionTests(unittest.TestCase):
    def slot(self, data: dict, key: str) -> dict:
        return next(s for s in data["slots"] if s["key"] == key)

    def test_empty_overlay_composes_the_contract_defaults(self) -> None:
        contract = load_manifest(ROOT / "WORKSPACE.yaml")
        composed = compose_manifest(minimal(), "workspace.yaml")
        self.assertEqual([s["key"] for s in composed["slots"]], [s["key"] for s in contract["slots"]])
        self.assertEqual(self.slot(composed, "knowledge.durable")["binding"], self.slot(contract, "knowledge.durable")["binding"])
        self.assertEqual(self.slot(composed, "workspace.schema")["binding"], "workspace.yaml")
        self.assertNotIn("identity", composed)

    def test_bindings_identity_and_cca_overlay(self) -> None:
        composed = compose_manifest(minimal(
            bindings={"knowledge.durable": "wiki/"},
            identity={"endpoint": "brain://example", "owner": "human"},
            cca={"specification": "1.4.0"},
        ), "workspace.yaml")
        self.assertEqual(self.slot(composed, "knowledge.durable")["binding"], "wiki/")
        self.assertEqual(composed["identity"]["endpoint"], "brain://example")
        self.assertEqual(composed["cca"], {"specification": "1.4.0"})

    def test_contract_is_not_mutated_by_composition(self) -> None:
        before = load_manifest(ROOT / "WORKSPACE.yaml")
        compose_manifest(minimal(bindings={"knowledge.durable": "wiki/"}), "workspace.yaml")
        self.assertEqual(load_manifest(ROOT / "WORKSPACE.yaml"), before)

    def test_pinned_fingerprint_must_match_installed_contract(self) -> None:
        stale = minimal()
        stale["extends"]["fingerprint"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "does not match the installed contract"):
            compose_manifest(stale, "workspace.yaml")

    def test_unknown_profile_or_version_fails(self) -> None:
        for profile, version in (("other", 3), ("hybrid-workspace", 9)):
            data = minimal()
            data["extends"].update(profile=profile, schema_version=version)
            with self.assertRaisesRegex(ValueError, "unknown profile contract"):
                compose_manifest(data, "workspace.yaml")

    def test_policy_slots_and_vocab_cannot_be_overridden(self) -> None:
        for key in ("slots", "vocab", "policy_definitions", "invariants", "status"):
            with self.assertRaisesRegex(ValueError, "not allowed"):
                compose_manifest(minimal(**{key: {}}), "workspace.yaml")

    def test_unknown_binding_key_and_unsafe_binding_fail(self) -> None:
        with self.assertRaisesRegex(ValueError, "not a key"):
            compose_manifest(minimal(bindings={"knowledge.secret": "secret/"}), "workspace.yaml")
        for bad in ("../escape/", "/abs/", "a/./b/", ""):
            with self.assertRaises(ValueError):
                compose_manifest(minimal(bindings={"knowledge.durable": bad}), "workspace.yaml")

    def test_bootstrap_binding_must_name_the_loaded_manifest(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be the manifest itself"):
            compose_manifest(minimal(bindings={"workspace.schema": "other.yaml"}), "workspace.yaml")

    def test_access_can_narrow_but_never_widen(self) -> None:
        composed = compose_manifest(minimal(narrow={"agent_access": {"context.capture": "read-only"}}), "workspace.yaml")
        self.assertEqual(self.slot(composed, "context.capture")["agent_access"], "read-only")
        with self.assertRaisesRegex(ValueError, "would widen"):
            compose_manifest(minimal(narrow={"agent_access": {"workspace.schema": "write"}}), "workspace.yaml")
        with self.assertRaisesRegex(ValueError, "may only contain agent_access"):
            compose_manifest(minimal(narrow={"authority": {"knowledge.durable": "agent"}}), "workspace.yaml")

    def test_provenance_aliases_only_for_canonical_fields(self) -> None:
        composed = compose_manifest(minimal(provenance_aliases={"origin": "source"}), "workspace.yaml")
        aliases = composed["reference_contract"]["provenance"]["representations"]["markdown_frontmatter"]["field_aliases"]
        self.assertEqual(aliases["origin"], "source")
        with self.assertRaisesRegex(ValueError, "not a canonical provenance field"):
            compose_manifest(minimal(provenance_aliases={"approved_by": "x"}), "workspace.yaml")


class MinimizeTests(unittest.TestCase):
    def full_manifest(self) -> dict:
        full = load_manifest(ROOT / "WORKSPACE.yaml")
        for slot in full["slots"]:
            if slot["key"] == "workspace.schema":
                slot["binding"] = "workspace.yaml"
            if slot["key"] == "knowledge.durable":
                slot["binding"] = "wiki/"
        return full

    def test_minimize_round_trips_exactly(self) -> None:
        full = self.full_manifest()
        small = minimize_manifest(full, "workspace.yaml")
        self.assertEqual(small["bindings"], {"knowledge.durable": "wiki/"})
        self.assertEqual(compose_manifest(small, "workspace.yaml"), full)

    def test_minimize_refuses_semantic_divergence(self) -> None:
        full = self.full_manifest()
        full["policy_defaults"] = {"unspecified": "allowed"}
        with self.assertRaisesRegex(ValueError, "diverges"):
            minimize_manifest(full, "workspace.yaml")
        full = self.full_manifest()
        next(s for s in full["slots"] if s["key"] == "knowledge.durable")["description"] = "changed"
        with self.assertRaisesRegex(ValueError, "diverges"):
            minimize_manifest(full, "workspace.yaml")


class EndToEndTests(unittest.TestCase):
    def test_audit_generate_and_resolve_on_a_minimal_workspace(self) -> None:
        root = write_workspace(minimal(bindings={"knowledge.durable": "wiki/"}, cca={"specification": "1.4.0"}))
        generated = run("generate.py", "--target", str(root))
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        check = run("generate.py", "--target", str(root), "--check")
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        audit = run("audit.py", "--target", str(root), "--structure-only")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        resolved = run("resolve.py", "--target", str(root), "--key", "knowledge.durable", "--format", "relative")
        self.assertEqual(resolved.stdout.strip(), "wiki/")
        paths = load_schema(root / "workspace.yaml")
        helper = root / next(s for s in paths["slots"] if s["key"] == "system.operations")["binding"] / "paths.py"
        helper_run = subprocess.run([sys.executable, str(helper), "knowledge.durable"], text=True, capture_output=True, check=False)
        self.assertEqual(helper_run.returncode, 0, helper_run.stderr)
        self.assertEqual(Path(helper_run.stdout.strip()), root / "wiki")

    def test_binding_change_makes_generated_helpers_stale(self) -> None:
        root = write_workspace(minimal())
        self.assertEqual(run("generate.py", "--target", str(root)).returncode, 0)
        manifest = yaml.safe_load((root / "workspace.yaml").read_text(encoding="utf-8"))
        manifest["bindings"] = {"knowledge.durable": "knowledge/"}
        (root / "workspace.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        self.assertNotEqual(run("generate.py", "--target", str(root), "--check").returncode, 0)

    def test_minimize_cli_matches_library(self) -> None:
        full = copy.deepcopy(MinimizeTests().full_manifest())
        root = write_workspace(full)
        printed = run("resolve.py", "--target", str(root), "--minimize")
        self.assertEqual(printed.returncode, 0, printed.stderr)
        self.assertEqual(yaml.safe_load(printed.stdout), minimize_manifest(full, "workspace.yaml"))
        fingerprint = run("resolve.py", "--contract-fingerprint", "hybrid-workspace@3")
        self.assertEqual(fingerprint.stdout.strip(), PIN)


if __name__ == "__main__":
    unittest.main()
