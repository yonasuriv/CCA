from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".github" / "scripts" / "validate_contract_version.py"


class ContractVersionGateTests(unittest.TestCase):
    def git(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            text=True,
            capture_output=True,
        )

    def write_skill(self, repo: Path, version: str, body: str = "# CCA\n") -> None:
        path = repo / "skills" / "cca" / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            textwrap.dedent(
                f'''\
                ---
                name: cca
                description: Test CCA skill.
                metadata:
                  version: "{version}"
                ---

                {body}
                '''
            ),
            encoding="utf-8",
        )

    def write_unversioned_skill(self, repo: Path, body: str = "# CCA\n") -> None:
        path = repo / "skills" / "cca" / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            textwrap.dedent(
                f'''\
                ---
                name: cca
                description: Historical pre-metadata CCA skill.
                ---

                {body}
                '''
            ),
            encoding="utf-8",
        )

    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        repo = Path(temp.name)
        self.git(repo, "init", "-b", "main")
        self.git(repo, "config", "user.email", "cca-tests@example.invalid")
        self.git(repo, "config", "user.name", "CCA Tests")
        self.write_skill(repo, "1.0.0")
        core = repo / "skills" / "cca" / "references" / "core"
        core.mkdir(parents=True, exist_ok=True)
        (core / "spec.md").write_text("# Spec\n", encoding="utf-8")
        (repo / "README.md").write_text("# Repo\n", encoding="utf-8")
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "baseline")
        return temp, repo

    def make_pre_metadata_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        repo = Path(temp.name)
        self.git(repo, "init", "-b", "main")
        self.git(repo, "config", "user.email", "cca-tests@example.invalid")
        self.git(repo, "config", "user.name", "CCA Tests")
        self.write_unversioned_skill(repo)
        core = repo / "skills" / "cca" / "references" / "core"
        core.mkdir(parents=True, exist_ok=True)
        (core / "spec.md").write_text(
            "# CCA Specification\n\n**Version 1.0.0** — Status: Stable\n",
            encoding="utf-8",
        )
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "historical baseline")
        return temp, repo

    def run_gate(self, repo: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(repo), "--base", "HEAD^"],
            cwd=repo,
            text=True,
            capture_output=True,
        )

    def commit(self, repo: Path, message: str) -> None:
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", message)

    def test_docs_only_change_with_same_version_passes(self) -> None:
        temp, repo = self.make_repo()
        self.addCleanup(temp.cleanup)
        (repo / "README.md").write_text("# Repo\n\nDocs only.\n", encoding="utf-8")
        self.commit(repo, "docs")
        result = self.run_gate(repo)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_contract_change_with_same_version_fails(self) -> None:
        temp, repo = self.make_repo()
        self.addCleanup(temp.cleanup)
        (repo / "skills/cca/references/core/spec.md").write_text("# Spec\n\nChanged.\n", encoding="utf-8")
        self.commit(repo, "contract change")
        result = self.run_gate(repo)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("contract-sensitive", (result.stdout + result.stderr).lower())
        self.assertIn("1.0.0", result.stdout + result.stderr)

    def test_contract_change_with_version_bump_passes(self) -> None:
        temp, repo = self.make_repo()
        self.addCleanup(temp.cleanup)
        (repo / "skills/cca/references/core/spec.md").write_text("# Spec\n\nChanged.\n", encoding="utf-8")
        self.write_skill(repo, "1.1.0")
        self.commit(repo, "versioned contract change")
        result = self.run_gate(repo)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_pre_metadata_baseline_uses_normative_spec_version(self) -> None:
        temp, repo = self.make_pre_metadata_repo()
        self.addCleanup(temp.cleanup)
        self.write_skill(repo, "1.1.0")
        (repo / "skills/cca/references/core/spec.md").write_text(
            "# CCA Specification\n\n**Version 1.1.0** — Status: Stable\n",
            encoding="utf-8",
        )
        self.commit(repo, "introduce version metadata")
        result = self.run_gate(repo)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("1.0.0 -> 1.1.0", result.stdout + result.stderr)

    def test_skill_body_change_with_same_version_fails(self) -> None:
        temp, repo = self.make_repo()
        self.addCleanup(temp.cleanup)
        self.write_skill(repo, "1.0.0", "# CCA\n\nBehavior changed.\n")
        self.commit(repo, "skill behavior")
        result = self.run_gate(repo)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("SKILL.md", result.stdout + result.stderr)

    def test_version_only_change_passes(self) -> None:
        temp, repo = self.make_repo()
        self.addCleanup(temp.cleanup)
        self.write_skill(repo, "1.0.1")
        self.commit(repo, "version only")
        result = self.run_gate(repo)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
