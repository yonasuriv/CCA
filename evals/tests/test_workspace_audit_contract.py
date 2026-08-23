from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class WorkspaceAuditContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_skill_routes_workspace_architecture_audits_to_architect(self) -> None:
        skill = self.read("skills/cca/SKILL.md")
        self.assertIn("workspace architecture audit", skill.lower())
        self.assertIn("use `architect`", skill.lower())
        self.assertIn("lint is claim validation", skill.lower())

    def test_spec_says_compatibility_is_not_architecture_quality(self) -> None:
        spec = self.read("skills/cca/references/core/spec.md")
        self.assertIn("Compatibility is not an architecture-quality certification.", spec)
        self.assertIn("A child-boundary pass MUST NOT imply a parent-boundary pass", spec)

    def test_architect_audit_preserves_requested_scope_and_scores_quality(self) -> None:
        architect = self.read("skills/cca/references/architect/mode.md")
        self.assertIn("## Audit mode", architect)
        self.assertIn("requested audit boundary", architect.lower())
        self.assertIn("A child-boundary PASS MUST NOT close a parent/workspace audit.", architect)
        for dimension in (
            "boundary discovery",
            "root orientation",
            "intent routing",
            "context selectivity",
            "authority clarity",
            "canonicality",
            "human navigation",
            "agent navigation",
            "search dependency",
            "drift resistance",
            "scalability",
        ):
            self.assertIn(dimension, architect.lower(), dimension)

    def test_lint_keeps_compatibility_and_conformance_independent(self) -> None:
        lint = self.read("skills/cca/references/operations/lint.md")
        self.assertIn(
            "A missing explicit CCA contract makes `CCA-conformant` N/A; it does not make `CCA-compatible` N/A.",
            lint,
        )
        self.assertIn("Lint success does not certify architecture quality.", lint)
        self.assertIn("requested boundary", lint.lower())
        self.assertIn("inspected boundaries", lint.lower())

    def test_user_facing_docs_explain_audit_vs_lint(self) -> None:
        faq = self.read("docs/faq.md")
        self.assertIn("Does a clean CCA lint mean the workspace has good context architecture?", faq)
        changelog = self.read("CHANGELOG.md")
        self.assertIn("workspace architecture audit", changelog.lower())


if __name__ == "__main__":
    unittest.main()
