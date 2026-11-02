#!/usr/bin/env python3
# Regression coverage for SSOT resolution, bootstrap case variants, and harmless edits.
from __future__ import annotations

from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "profiles" / "v2"
sys.path.insert(0, str(ROOT))

from resolve import resolve  # noqa: E402
from schema import workspace_schema_path, generated_outputs, load_schema  # noqa: E402


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), text=True, capture_output=True, check=False)


def make_target(*, v3: bool = True, lowercase: bool = True) -> Path:
    root = Path(tempfile.mkdtemp(prefix="cca-binding-"))
    profile = ROOT if v3 else V2
    name = "workspace.yaml" if lowercase else "WORKSPACE.yaml"
    source = (profile / "WORKSPACE.yaml").read_text(encoding="utf-8")
    agents = (profile / "AGENTS.md").read_text(encoding="utf-8")
    if lowercase:
        source = source.replace("WORKSPACE.yaml", name)
        agents = agents.replace("WORKSPACE.yaml", name)
    (root / name).write_text(source, encoding="utf-8")
    (root / "AGENTS.md").write_text(agents, encoding="utf-8")
    return root


class WorkspaceResolverTests(unittest.TestCase):
    def test_lowercase_v3_is_discovered_and_generated(self) -> None:
        target = make_target()
        self.assertEqual(workspace_schema_path(target).name, "workspace.yaml")
        data = load_schema(workspace_schema_path(target))
        generated = run(sys.executable, str(ROOT / "generate.py"), "--target", str(target))
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        paths = generated_outputs(data)
        for relative in paths.values():
            self.assertTrue((target / relative).is_file(), relative)
        checked = run(sys.executable, str(ROOT / "generate.py"), "--target", str(target), "--check")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        relative, absolute = resolve(target, key="knowledge.durable")
        self.assertEqual(relative, next(s["binding"] for s in data["slots"] if s["key"] == "knowledge.durable"))
        self.assertEqual(absolute, target / relative.rstrip("/"))
        generated_relative, _ = resolve(target, output="paths")
        self.assertEqual(generated_relative, paths["paths"])

    def test_whitespace_change_does_not_invalidate_generated_shell_helpers(self) -> None:
        target = make_target()
        generated = run(sys.executable, str(ROOT / "generate.py"), "--target", str(target))
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
        manifest = target / "workspace.yaml"
        manifest.write_text(manifest.read_text(encoding="utf-8") + "\n# harmless comment\n", encoding="utf-8")
        checked = run(sys.executable, str(ROOT / "generate.py"), "--target", str(target), "--check")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        outputs = generated_outputs(load_schema(manifest))
        mkdirs = run("bash", str(target / outputs["mkdirs"]), "--required")
        self.assertEqual(mkdirs.returncode, 0, mkdirs.stdout + mkdirs.stderr)

    def test_relocation_updates_resolution_and_generated_artifacts(self) -> None:
        target = make_target()
        before = run(sys.executable, str(ROOT / "generate.py"), "--target", str(target))
        self.assertEqual(before.returncode, 0, before.stdout + before.stderr)
        manifest = target / "workspace.yaml"
        raw = manifest.read_text(encoding="utf-8")
        data = yaml.safe_load(raw)
        slot = next(s for s in data["slots"] if s["key"] == "state.current")
        old_binding = slot["binding"]
        new_binding = "00-state/session-now.md"
        self.assertNotEqual(old_binding, new_binding)
        text = raw.replace(f"binding: {old_binding}", f"binding: {new_binding}", 1)
        self.assertNotEqual(text, raw)
        manifest.write_text(text, encoding="utf-8")
        self.assertEqual(resolve(target, key="state.current")[0], new_binding)
        stale = run(sys.executable, str(ROOT / "generate.py"), "--target", str(target), "--check")
        self.assertNotEqual(stale.returncode, 0, stale.stdout + stale.stderr)
        updated = run(sys.executable, str(ROOT / "generate.py"), "--target", str(target))
        self.assertEqual(updated.returncode, 0, updated.stdout + updated.stderr)
        checked = run(sys.executable, str(ROOT / "generate.py"), "--target", str(target), "--check")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_uppercase_legacy_v2_and_v3_supported(self) -> None:
        for version in (2, 3):
            with self.subTest(version=version):
                target = make_target(v3=version == 3, lowercase=False)
                self.assertEqual(workspace_schema_path(target).name, "WORKSPACE.yaml")
                self.assertTrue(resolve(target, key="knowledge.durable")[0])
                audit = run(sys.executable, str(ROOT / "audit.py"), "--target", str(target))
                self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_ambiguous_manifest_fails_closed(self) -> None:
        target = make_target()
        (target / "WORKSPACE.yaml").write_text("schema_version: 3\n", encoding="utf-8")
        variants = [p for p in target.iterdir() if p.name.casefold() == "workspace.yaml"]
        if len(variants) == 1:
            self.skipTest("case-insensitive filesystem cannot represent both spellings")
        with self.assertRaises(ValueError):
            workspace_schema_path(target)

    def test_invalid_manifest_or_binding_cannot_escape_root(self) -> None:
        target = make_target()
        with self.assertRaises(KeyError):
            resolve(target, key="not.a.real.key")
        manifest = target / "workspace.yaml"
        raw = manifest.read_text(encoding="utf-8")
        data = yaml.safe_load(raw)
        binding = next(s["binding"] for s in data["slots"] if s["key"] == "knowledge.durable")
        manifest.write_text(raw.replace(f"binding: {binding}", "binding: ../escape/", 1), encoding="utf-8")
        with self.assertRaises(ValueError):
            resolve(target, key="knowledge.durable")

    def test_fast_structure_check_does_not_scan_sources(self) -> None:
        target = make_target()
        collected = resolve(target, key="reference.collected")[1]
        collected.mkdir(parents=True)
        (collected / "unadmitted.md").write_text("Unverified evidence\\n", encoding="utf-8")
        fast = run(sys.executable, str(ROOT / "audit.py"), "--target", str(target), "--structure-only")
        self.assertEqual(fast.returncode, 0, fast.stdout + fast.stderr)
        full = run(sys.executable, str(ROOT / "audit.py"), "--target", str(target))
        self.assertNotEqual(full.returncode, 0, full.stdout + full.stderr)
        regenerated = run(sys.executable, str(ROOT / "generate.py"), "--target", str(target))
        self.assertEqual(regenerated.returncode, 0, regenerated.stdout + regenerated.stderr)

    def test_init_new_v3_target_uses_lowercase_name(self) -> None:
        target = Path(tempfile.mkdtemp(prefix="cca-init-case-"))
        result = run(sys.executable, str(ROOT / "generate.py"), "--target", str(target), "--init")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((target / "workspace.yaml").is_file())
        self.assertFalse((target / "WORKSPACE.yaml").exists())


class QAFindingRegressionTests(unittest.TestCase):
    def _v3(self) -> Path:
        target = Path(tempfile.mkdtemp(prefix="cca-qa-"))
        run_ok = subprocess.run([sys.executable, str(ROOT / "generate.py"), "--target", str(target), "--init"], capture_output=True, text=True)
        self.assertEqual(run_ok.returncode, 0, run_ok.stdout + run_ok.stderr)
        return target

    def _gen(self, target: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(ROOT / "generate.py"), "--target", str(target), *extra], capture_output=True, text=True)

    def test_manifest_name_is_never_rewritten_inside_user_content(self) -> None:
        target = self._v3()
        path = target / "workspace.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        slot = next(s for s in data["slots"] if s["key"] == "output.artifact")
        slot["description"] = "Deliverables, including a file named WORKSPACE.yaml-archive."
        slot["binding"] = "WORKSPACE.yaml.d/"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        self.assertEqual(self._gen(target).returncode, 0)
        spec = (target / "_runtime/docs/SPEC.md").read_text(encoding="utf-8")
        paths = (target / "_runtime/operations/paths.sh").read_text(encoding="utf-8")
        self.assertIn("WORKSPACE.yaml-archive", spec)
        self.assertIn("[output.artifact]=WORKSPACE.yaml.d/", paths)

    def test_lowercase_manifest_requires_schema_v3_in_every_tool(self) -> None:
        target = Path(tempfile.mkdtemp(prefix="cca-qa-v2lower-"))
        shutil.copy2(ROOT / "profiles" / "v2" / "WORKSPACE.yaml", target / "workspace.yaml")
        shutil.copy2(ROOT / "profiles" / "v2" / "AGENTS.md", target / "AGENTS.md")
        audit = subprocess.run([sys.executable, str(ROOT / "audit.py"), "--target", str(target)], capture_output=True, text=True)
        self.assertNotEqual(audit.returncode, 0)
        self.assertNotEqual(self._gen(target).returncode, 0)

    def test_helper_rejects_two_manifest_spellings(self) -> None:
        target = self._v3()
        (target / "WORKSPACE.yaml").write_bytes((target / "workspace.yaml").read_bytes())
        if len([p for p in target.iterdir() if p.name.casefold() == "workspace.yaml"]) < 2:
            self.skipTest("case-insensitive filesystem")
        result = subprocess.run(["bash", "-c", f'source "{target}/_runtime/operations/paths.sh"'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exactly one", result.stderr)

    def test_fingerprint_is_deterministic_for_sets_and_mixed_keys(self) -> None:
        target = self._v3()
        with (target / "workspace.yaml").open("a", encoding="utf-8") as handle:
            handle.write("\nx_extension:\n  tags: !!set {b, a, c}\n  1: one\n  two: 2\n")
        first = self._gen(target)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        for seed in ("1", "2", "3"):
            env = dict(os.environ, PYTHONHASHSEED=seed)
            check = subprocess.run([sys.executable, str(ROOT / "generate.py"), "--target", str(target), "--check"], capture_output=True, text=True, env=env)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
            src = subprocess.run(["bash", "-c", f'source "{target}/_runtime/operations/paths.sh"'], capture_output=True, text=True, env=env)
            self.assertEqual(src.returncode, 0, src.stderr)

    def test_unparseable_manifest_is_reported_as_such(self) -> None:
        target = self._v3()
        with (target / "workspace.yaml").open("a", encoding="utf-8") as handle:
            handle.write("\nbroken: [unclosed\n")
        result = subprocess.run(["bash", "-c", f'source "{target}/_runtime/operations/paths.sh"'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot read or parse", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
