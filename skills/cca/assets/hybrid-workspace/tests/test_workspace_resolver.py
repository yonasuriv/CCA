#!/usr/bin/env python3
# Regression coverage for SSOT resolution, bootstrap case variants, and harmless edits.
from __future__ import annotations

from pathlib import Path
import json
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
        mkdirs = run(sys.executable, str(target / outputs["mkdirs"]), "--required")
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
        self.assertNotIn("WORKSPACE.yaml", {entry.name for entry in target.iterdir()})


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
        paths = (target / "_runtime/operations/paths.py").read_text(encoding="utf-8")
        self.assertIn("WORKSPACE.yaml-archive", spec)
        self.assertIn("'output.artifact': 'WORKSPACE.yaml.d/'", paths)

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
        result = subprocess.run([sys.executable, str(target / "_runtime/operations/paths.py"), "--list"], capture_output=True, text=True)
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
            src = subprocess.run([sys.executable, str(target / "_runtime/operations/paths.py"), "--list"], capture_output=True, text=True, env=env)
            self.assertEqual(src.returncode, 0, src.stderr)

    def test_unparseable_manifest_is_reported_as_such(self) -> None:
        target = self._v3()
        with (target / "workspace.yaml").open("a", encoding="utf-8") as handle:
            handle.write("\nbroken: [unclosed\n")
        result = subprocess.run([sys.executable, str(target / "_runtime/operations/paths.py"), "--list"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot read or parse", result.stderr)


class PythonHelperTests(unittest.TestCase):
    """The default v3 helpers are Python: same guarantees as the shell variant, on any OS."""

    def setUp(self) -> None:
        self.target = Path(tempfile.mkdtemp(prefix="cca-pyhelper-"))
        made = subprocess.run([sys.executable, str(ROOT / "generate.py"), "--target", str(self.target), "--init"], capture_output=True, text=True)
        self.assertEqual(made.returncode, 0, made.stdout + made.stderr)
        self.paths = self.target / "_runtime/operations/paths.py"
        self.mkdirs = self.target / "_runtime/operations/mkdirs.py"

    def run_py(self, script: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, cwd=cwd or tempfile.gettempdir())

    def test_defaults_are_python_and_resolve_from_any_cwd(self) -> None:
        self.assertTrue(self.paths.is_file() and self.mkdirs.is_file())
        self.assertFalse((self.target / "_runtime/operations/paths.sh").exists())
        durable = self.run_py(self.paths, "knowledge.durable")
        self.assertEqual(durable.returncode, 0, durable.stderr)
        self.assertEqual(Path(durable.stdout.strip()), self.target.resolve() / "00-wiki")
        mapping = json.loads(self.run_py(self.paths, "--json").stdout)
        self.assertEqual(mapping["context.capture"], str(self.target.resolve() / "10-inbox"))
        self.assertEqual(self.run_py(self.paths, "no.such.key").returncode, 2)
        self.assertEqual(self.run_py(self.mkdirs, "--all").returncode, 0)
        self.assertTrue((self.target / "40-projects" / "upstream").is_dir())
        self.assertFalse((self.target / "_runtime" / "operations" / "00-wiki").exists())

    def test_importable_module(self) -> None:
        code = f"import importlib.util,sys; s=importlib.util.spec_from_file_location('p', {str(self.paths)!r}); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.ws()['knowledge.durable'])"
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        self.assertEqual(Path(result.stdout.strip()), self.target.resolve() / "00-wiki")

    def test_whitespace_safe_semantic_change_fails_closed_until_regenerated(self) -> None:
        manifest = self.target / "workspace.yaml"
        manifest.write_text(manifest.read_text(encoding="utf-8") + "\n# owner comment\n\n", encoding="utf-8")
        self.assertEqual(self.run_py(self.paths, "--list").returncode, 0)
        manifest.write_text(manifest.read_text(encoding="utf-8").replace("binding: 50-outputs/", "binding: outputs/"), encoding="utf-8")
        stale = self.run_py(self.paths, "--list")
        self.assertEqual(stale.returncode, 1)
        self.assertIn("regenerate", stale.stderr)
        self.assertEqual(self.run_py(self.mkdirs, "--all").returncode, 1)
        subprocess.run([sys.executable, str(ROOT / "generate.py"), "--target", str(self.target)], check=True, capture_output=True)
        self.assertEqual(self.run_py(self.paths, "output.artifact").stdout.strip(), str(self.target.resolve() / "outputs"))

    def test_copied_and_symlinked_helpers(self) -> None:
        stray = Path(tempfile.mkdtemp(prefix="cca-stray-")) / "a" / "b"
        stray.mkdir(parents=True)
        shutil.copy2(self.paths, stray / "paths.py")
        copied = self.run_py(stray / "paths.py", "--list")
        self.assertEqual(copied.returncode, 1)
        outer = Path(tempfile.mkdtemp(prefix="cca-outer-"))
        try:
            os.symlink(self.paths, outer / "paths.py")
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest("Windows symlink privilege unavailable")
            raise
        linked = self.run_py(outer / "paths.py", "workspace.schema")
        self.assertEqual(Path(linked.stdout.strip()), self.target.resolve() / "workspace.yaml")

    def test_helper_extension_must_be_supported(self) -> None:
        manifest = self.target / "workspace.yaml"
        manifest.write_text(manifest.read_text(encoding="utf-8").replace("file: paths.py}", "file: paths.rb}"), encoding="utf-8")
        audit = subprocess.run([sys.executable, str(ROOT / "audit.py"), "--target", str(self.target)], capture_output=True, text=True)
        self.assertNotEqual(audit.returncode, 0)
        self.assertIn(".py (cross-platform) or .sh", audit.stdout)

    def test_helper_names_and_locations_are_configurable(self) -> None:
        manifest = self.target / "workspace.yaml"
        text = manifest.read_text(encoding="utf-8").replace("file: paths.py}", "file: ws_paths.py}").replace("binding: _runtime/operations/", "binding: tools/generated/")
        manifest.write_text(text, encoding="utf-8")
        regenerated = subprocess.run([sys.executable, str(ROOT / "generate.py"), "--target", str(self.target)], capture_output=True, text=True)
        self.assertEqual(regenerated.returncode, 0, regenerated.stdout + regenerated.stderr)
        helper = self.target / "tools/generated/ws_paths.py"
        self.assertEqual(Path(self.run_py(helper, "context.capture").stdout.strip()), self.target.resolve() / "10-inbox")


if __name__ == "__main__":
    unittest.main(verbosity=2)
