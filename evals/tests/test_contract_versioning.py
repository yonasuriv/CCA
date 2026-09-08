from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = ROOT / "skills" / "cca"


class ContractVersioningTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_versioning_reference_defines_consumer_contract_identity(self) -> None:
        versioning = self.read("skills/cca/references/core/versioning.md")
        self.assertIn("MUST identify the applicable CCA contract by version", versioning)
        self.assertIn("MUST NOT serve as CCA conformance identity", versioning)
        self.assertIn("non-normative provenance", versioning)
        self.assertIn("MAJOR", versioning)
        self.assertIn("MINOR", versioning)
        self.assertIn("PATCH", versioning)

    def test_spec_is_versioned_and_routes_to_versioning_authority(self) -> None:
        spec = self.read("skills/cca/references/core/spec.md")
        self.assertIn("**Version 1.2.1**", spec)
        self.assertIn("versioning.md", spec)

    def test_skill_exposes_and_routes_contract_version(self) -> None:
        skill = self.read("skills/cca/SKILL.md")
        self.assertIn('version: "1.2.1"', skill)
        self.assertIn("versioning.md", skill)
        self.assertIn("contract version", skill.lower())
        self.assertIn("semver", skill.lower())
        self.assertIn(
            "Any operation that creates, validates, migrates, or reports a CCA compatibility/conformance/profile identity MUST load `references/core/versioning.md`.",
            skill,
        )

    def test_versioning_authority_defines_lint_and_creation_behavior(self) -> None:
        versioning = self.read("skills/cca/references/core/versioning.md")
        self.assertIn("When CCA creates, audits, remediates, or lints a consumer", versioning)
        self.assertIn("normative CCA commit/revision pin as a conformance error", versioning)
        self.assertIn("Permit source revisions in clearly non-authoritative evidence/provenance", versioning)

    def test_installed_skill_never_advertises_reference_commit_identity(self) -> None:
        offenders = []
        for path in SKILL_ROOT.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".json", ".py"}:
                if "reference_commit" in path.read_text(encoding="utf-8", errors="ignore"):
                    offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
