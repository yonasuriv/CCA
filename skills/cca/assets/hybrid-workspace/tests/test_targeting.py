#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

PACKAGE = Path(__file__).resolve().parents[1]
GENERATED_STATIC = ("paths.sh", "mkdirs.sh", "obsidian-excludes.txt", "SPEC.md")


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd or PACKAGE,
        text=True,
        capture_output=True,
        check=False,
    )


def make_target(*, with_agents: bool = True) -> Path:
    target = Path(tempfile.mkdtemp(prefix="cca-hybrid-target-"))
    shutil.copy2(PACKAGE / "WORKSPACE.yaml", target / "WORKSPACE.yaml")
    if with_agents:
        shutil.copy2(PACKAGE / "AGENTS.md", target / "AGENTS.md")
    return target


def replace_binding(target: Path, key: str, new_binding: str) -> None:
    path = target / "WORKSPACE.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    slot = next(s for s in data["slots"] if s["key"] == key)
    old_binding = slot["binding"]
    text = path.read_text(encoding="utf-8")
    marker = f"key: {key}"
    start = text.index(marker)
    end = text.index("\n\n", start)
    block = text[start:end].replace(f"binding: {old_binding}", f"binding: {new_binding}")
    path.write_text(text[:start] + block + text[end:], encoding="utf-8")


class TargetIsolationTests(unittest.TestCase):
    def test_generate_requires_explicit_target(self) -> None:
        result = run(sys.executable, str(PACKAGE / "generate.py"))
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("--target", result.stdout + result.stderr)

    def test_generate_writes_only_to_target(self) -> None:
        target = make_target()
        before = {p.name for p in PACKAGE.iterdir()}
        result = run(
            sys.executable,
            str(PACKAGE / "generate.py"),
            "--target",
            str(target),
            cwd=Path(tempfile.mkdtemp(prefix="cca-outside-")),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name in GENERATED_STATIC + ("CONTEXT.md",):
            self.assertTrue((target / name).is_file(), name)
        after = {p.name for p in PACKAGE.iterdir()}
        self.assertEqual(before, after)

    def test_init_scaffolds_human_authored_templates_on_target_without_overwrite(self) -> None:
        target = Path(tempfile.mkdtemp(prefix="cca-hybrid-init-"))
        result = run(
            sys.executable,
            str(PACKAGE / "generate.py"),
            "--target",
            str(target),
            "--init",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((target / "WORKSPACE.yaml").is_file())
        self.assertTrue((target / "AGENTS.md").is_file())
        original = (target / "AGENTS.md").read_text(encoding="utf-8")
        (target / "AGENTS.md").write_text(original + "\nLOCAL EDIT\n", encoding="utf-8")
        rerun = run(
            sys.executable,
            str(PACKAGE / "generate.py"),
            "--target",
            str(target),
            "--init",
        )
        self.assertEqual(rerun.returncode, 0, rerun.stdout + rerun.stderr)
        self.assertTrue((target / "AGENTS.md").read_text(encoding="utf-8").endswith("LOCAL EDIT\n"))

    def test_router_binding_controls_generated_router_filename(self) -> None:
        target = make_target()
        replace_binding(target, "context.router", "ROUTER.md")
        result = run(sys.executable, str(PACKAGE / "generate.py"), "--target", str(target))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((target / "ROUTER.md").is_file())
        self.assertFalse((target / "CONTEXT.md").exists())
        self.assertIn("context.router", (target / "ROUTER.md").read_text(encoding="utf-8"))
        checked = run(
            sys.executable,
            str(PACKAGE / "generate.py"),
            "--target",
            str(target),
            "--check",
        )
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_state_and_system_binding_moves_do_not_leak_default_namespaces(self) -> None:
        target = make_target()
        replacements = {
            "state.current": "control/current.md",
            "state.tasks": "tasks/",
            "state.memory": "memory/",
            "agent.skills": "capabilities/",
            "system.scripts": "tooling/scripts/",
            "system.templates": "tooling/templates/",
            "system.workflows": "tooling/workflows/",
            "system.assets": "tooling/assets/",
        }
        for key, binding in replacements.items():
            replace_binding(target, key, binding)
        result = run(sys.executable, str(PACKAGE / "generate.py"), "--target", str(target))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        combined = "\n".join(
            (target / name).read_text(encoding="utf-8")
            for name in ("paths.sh", "mkdirs.sh", "SPEC.md", "CONTEXT.md")
        )
        self.assertNotIn("_state/", combined)
        self.assertNotIn("_runtime/", combined)
        for binding in replacements.values():
            self.assertIn(binding, combined)

    def test_audit_validates_target_from_outside_package_and_cwd(self) -> None:
        target = make_target()
        outside = Path(tempfile.mkdtemp(prefix="cca-audit-outside-"))
        result = run(
            sys.executable,
            str(PACKAGE / "audit.py"),
            "--target",
            str(target),
            "--self-test",
            cwd=outside,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("frozen-v1", result.stdout)

        text = (target / "WORKSPACE.yaml").read_text(encoding="utf-8")
        text = text.replace("status: frozen", "status: draft", 1)
        (target / "WORKSPACE.yaml").write_text(text, encoding="utf-8")
        broken = run(
            sys.executable,
            str(PACKAGE / "audit.py"),
            "--target",
            str(target),
            cwd=outside,
        )
        self.assertNotEqual(broken.returncode, 0, broken.stdout + broken.stderr)
        self.assertIn("status", (broken.stdout + broken.stderr).lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
