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


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd or PACKAGE,
        text=True,
        capture_output=True,
        check=False,
    )


def make_target() -> Path:
    target = Path(tempfile.mkdtemp(prefix="cca-hybrid-adversarial-"))
    shutil.copy2(PACKAGE / "WORKSPACE.yaml", target / "WORKSPACE.yaml")
    shutil.copy2(PACKAGE / "AGENTS.md", target / "AGENTS.md")
    return target


class AdversarialTargetingTests(unittest.TestCase):
    def test_generation_contract_names_router_semantically(self) -> None:
        data = yaml.safe_load((PACKAGE / "WORKSPACE.yaml").read_text(encoding="utf-8"))
        derived = data["generation_contract"]["derived"]
        self.assertIn("context.router", derived)
        self.assertNotIn("CONTEXT.md", derived)

    def test_parent_traversal_binding_is_rejected(self) -> None:
        target = make_target()
        text = (target / "WORKSPACE.yaml").read_text(encoding="utf-8")
        text = text.replace("binding: 50-outputs/", "binding: ../outside/", 1)
        (target / "WORKSPACE.yaml").write_text(text, encoding="utf-8")
        result = run(sys.executable, str(PACKAGE / "audit.py"), "--target", str(target))
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("binding", (result.stdout + result.stderr).lower())

    def test_static_generated_symlink_escape_is_rejected_before_write(self) -> None:
        target = make_target()
        outside = Path(tempfile.mkdtemp(prefix="cca-hybrid-outside-"))
        escaped = outside / "SPEC.md"
        escaped.write_text("DO NOT TOUCH\n", encoding="utf-8")
        (target / "SPEC.md").symlink_to(escaped)

        result = run(sys.executable, str(PACKAGE / "generate.py"), "--target", str(target))
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(escaped.read_text(encoding="utf-8"), "DO NOT TOUCH\n")
        self.assertIn("escapes workspace", (result.stdout + result.stderr).lower())

    def test_relocated_router_still_satisfies_semantic_generation_contract(self) -> None:
        target = make_target()
        text = (target / "WORKSPACE.yaml").read_text(encoding="utf-8")
        text = text.replace("binding: CONTEXT.md", "binding: ROUTER.md", 1)
        (target / "WORKSPACE.yaml").write_text(text, encoding="utf-8")

        result = run(sys.executable, str(PACKAGE / "generate.py"), "--target", str(target))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((target / "ROUTER.md").is_file())
        self.assertFalse((target / "CONTEXT.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
