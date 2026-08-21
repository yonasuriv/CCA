from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class GitHubGovernanceTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_issue_forms_exist_and_split_bug_from_proposal(self) -> None:
        bug = ROOT / ".github/ISSUE_TEMPLATE/bug.yml"
        proposal = ROOT / ".github/ISSUE_TEMPLATE/proposal.yml"
        config = ROOT / ".github/ISSUE_TEMPLATE/config.yml"

        self.assertTrue(bug.is_file(), "missing bug issue form")
        self.assertTrue(proposal.is_file(), "missing proposal issue form")
        self.assertTrue(config.is_file(), "missing issue form config")

        bug_text = bug.read_text(encoding="utf-8")
        proposal_text = proposal.read_text(encoding="utf-8")

        for required in (
            "What happened?",
            "Expected behavior",
            "Affected surface",
            "Reproduction",
            "Evidence",
            "Version / commit",
        ):
            self.assertIn(required, bug_text, required)

        for required in (
            "Problem",
            "Affected authority / scope",
            "Existing standards or conventions considered",
            "Semantic impact",
            "Why CCA should change",
            "Compatibility / migration impact",
            "Evidence / references",
        ):
            self.assertIn(required, proposal_text, required)

    def test_pull_request_template_supports_evidence_backed_change_summaries(self) -> None:
        text = self.read(".github/PULL_REQUEST_TEMPLATE.md")
        for required in (
            "## Summary",
            "## Why",
            "## Scope",
            "## Non-goals",
            "## What changed",
            "## Verification",
            "## Compatibility / version impact",
            "## Follow-up / known debt",
            "Authority and scope",
            "boundary + semantic role -> binding",
        ):
            self.assertIn(required, text, required)

    def test_contribution_docs_explain_issue_vs_direct_pr_flow(self) -> None:
        contributing = self.read("CONTRIBUTING.md")
        agents = self.read("AGENTS.md")
        docs_index = self.read("docs/README.md")

        for required in (
            "When to open an issue",
            "bug.yml",
            "proposal.yml",
            "direct pull request",
        ):
            self.assertIn(required, contributing, required)

        self.assertIn("ISSUE_TEMPLATE", agents)
        self.assertIn("CONTRIBUTING.md", agents)
        self.assertIn("ISSUE_TEMPLATE", docs_index)
        self.assertIn("PULL_REQUEST_TEMPLATE.md", docs_index)


if __name__ == "__main__":
    unittest.main()
