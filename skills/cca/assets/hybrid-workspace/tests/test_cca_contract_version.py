#!/usr/bin/env python3
# Regression tests for version-based CCA compatibility checking. This
# deliberately never pins a CCA repository commit/tree/blob identity — see
# references/core/versioning.md.
from __future__ import annotations

import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
# The generic version-compatibility mechanism is exercised on the frozen v2 fixture;
# schema v3 additionally requires cca.specification >= 1.3.0 (see test_v3_profile).
V2 = PACKAGE / "profiles" / "v2"
SKILL_MD = PACKAGE.parent.parent / "SKILL.md"


def run(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PACKAGE / "audit.py"), "--target", str(cwd), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def make_target(cca_block: str | None) -> Path:
    target = Path(tempfile.mkdtemp(prefix="cca-version-target-"))
    text = (V2 / "WORKSPACE.yaml").read_text(encoding="utf-8")
    text = re.sub(r"(?m)^cca:\n(?:^ {2}.*\n)*", "", text)
    if cca_block is not None:
        text = cca_block + "\n" + text
    (target / "WORKSPACE.yaml").write_text(text, encoding="utf-8")
    shutil.copy2(V2 / "AGENTS.md", target / "AGENTS.md")
    return target


def installed_version() -> tuple[int, int, int]:
    frontmatter = SKILL_MD.read_text(encoding="utf-8").split("---", 2)[1]
    match = re.search(r'(?m)^\s+version:\s*["\']([^"\']+)["\']\s*$', frontmatter)
    assert match is not None
    return tuple(int(p) for p in match.group(1).split("."))  # type: ignore[return-value]


class CcaContractVersionTests(unittest.TestCase):
    def test_default_template_declares_a_version_compatible_with_itself(self) -> None:
        # audit.py forbids the installed package dir as a target; use a copy instead.
        target = make_target(None)
        shutil.copy2(V2 / "WORKSPACE.yaml", target / "WORKSPACE.yaml")
        result = run(cwd=target)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("cca-version", result.stdout)

    def test_missing_cca_block_warns_but_does_not_fail(self) -> None:
        target = make_target(None)
        result = run(cwd=target)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN", result.stdout)
        self.assertIn("cca-version", result.stdout)
        self.assertIn("does not declare cca.specification", result.stdout)

    def test_matching_declared_version_passes(self) -> None:
        major, minor, patch = installed_version()
        target = make_target(f'cca:\n  specification: "{major}.{minor}.{patch}"\n')
        result = run(cwd=target)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("cca-version", result.stdout)

    def test_declared_older_than_installed_passes(self) -> None:
        major, minor, patch = installed_version()
        older_minor = max(minor - 1, 0)
        target = make_target(f'cca:\n  specification: "{major}.{older_minor}.0"\n')
        result = run(cwd=target)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_declared_newer_than_installed_fails(self) -> None:
        major, minor, patch = installed_version()
        target = make_target(f'cca:\n  specification: "{major}.{minor + 1}.0"\n')
        result = run(cwd=target)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("cca-version", result.stdout)
        self.assertIn("older", result.stdout)

    def test_major_mismatch_fails(self) -> None:
        major, minor, patch = installed_version()
        target = make_target(f'cca:\n  specification: "{major + 1}.0.0"\n')
        result = run(cwd=target)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("cca-version", result.stdout)
        self.assertIn("major", result.stdout.lower())

    def test_malformed_version_string_fails(self) -> None:
        target = make_target('cca:\n  specification: "not-a-semver"\n')
        result = run(cwd=target)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("cca-version", result.stdout)
        self.assertIn("SemVer", result.stdout)

    def test_cca_block_without_specification_fails(self) -> None:
        target = make_target("cca:\n  unrelated: true\n")
        result = run(cwd=target)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("cca.specification is required", result.stdout)

    def test_check_never_reads_a_repository_revision(self) -> None:
        # The version check must be satisfiable from SKILL.md alone; it must
        # never require or accept a commit/tree/blob field to pass.
        major, minor, patch = installed_version()
        target = make_target(f'cca:\n  specification: "{major}.{minor}.{patch}"\n')
        result = run(cwd=target)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        combined = (result.stdout + result.stderr).lower()
        for forbidden in ("commit", "blob sha", "tree sha"):
            self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()
