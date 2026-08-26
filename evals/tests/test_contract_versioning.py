from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ContractVersioningTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_spec_defines_version_as_consumer_contract_identity(self) -> None:
        spec = self.read("skills/cca/references/core/spec.md")
        self.assertIn("contract identity", spec.lower())
        self.assertIn("MUST identify the applicable CCA contract by version", spec)
        self.assertIn("MUST NOT serve as CCA conformance identity", spec)
        self.assertIn("non-normative provenance", spec)

    def test_compatibility_separates_contract_identity_from_source_provenance(self) -> None:
        compatibility = self.read("skills/cca/references/core/compatibility.md").lower()
        self.assertIn("contract identity", compatibility)
        self.assertIn("source provenance", compatibility)
        self.assertIn("version", compatibility)
        self.assertIn("commit", compatibility)

    def test_lint_rejects_normative_source_revision_pin(self) -> None:
        lint = self.read("skills/cca/references/operations/lint.md").lower()
        self.assertIn("commit", lint)
        self.assertIn("conformance error", lint)
        self.assertIn("provenance", lint)
        self.assertIn("contract version", lint)

    def test_architect_and_builder_never_introduce_commit_identity(self) -> None:
        for relative in (
            "skills/cca/references/architect/mode.md",
            "skills/cca/references/architect/workspace-builder.md",
        ):
            text = self.read(relative)
            lowered = text.lower()
            self.assertIn("cca contract version", lowered, relative)
            self.assertIn("source provenance", lowered, relative)
            self.assertNotIn("reference_commit", text, relative)

    def test_skill_declares_semver_policy_as_installed_contract(self) -> None:
        skill = self.read("skills/cca/SKILL.md")
        self.assertIn('version: "1.1.0"', skill)
        self.assertIn("contract version", skill.lower())
        self.assertIn("semver", skill.lower())


if __name__ == "__main__":
    unittest.main()
