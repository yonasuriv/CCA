from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ReleaseReadinessTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_normative_spec_is_1_2_0_stable(self) -> None:
        spec = self.read("skills/cca/references/core/spec.md")
        self.assertIn("**Version 1.2.0**", spec)
        self.assertRegex(spec, r"\bStatus:\s*Stable\b")
        self.assertNotIn("Status: Draft", spec)

    def test_installed_skill_exposes_1_2_0_contract_version(self) -> None:
        skill = self.read("skills/cca/SKILL.md")
        frontmatter = skill.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^metadata:\s*$")
        self.assertRegex(frontmatter, r'(?m)^\s+version:\s*["\']1\.2\.0["\']\s*$')

    def test_public_readme_has_no_release_placeholder(self) -> None:
        readme = self.read("README.md")
        self.assertNotIn('ADD THE "IN PLAIN ENGLISH EXPLAINATION"', readme)
        self.assertNotIn("<TEXT HERE>", readme)
        self.assertNotIn("must be processed first", readme)

    def test_current_package_maps_include_hybrid_workspace(self) -> None:
        readme = self.read("README.md")
        docs_index = self.read("docs/README.md")
        for text in (readme, docs_index):
            self.assertIn("hybrid-workspace.md", text)
            self.assertRegex(text, r"assets/[\s\S]{0,300}hybrid-workspace/")

    def test_root_and_docs_indexes_cover_all_public_docs(self) -> None:
        readme = self.read("README.md")
        docs_index = self.read("docs/README.md")
        public_docs = sorted(
            path.name
            for path in (ROOT / "docs").glob("*.md")
            if path.name not in {"README.md", "_wip.md"}
        )
        self.assertTrue(public_docs)
        for name in public_docs:
            self.assertIn(f"docs/{name}", readme, f"root README missing docs/{name}")
            self.assertIn(f"({name})", docs_index, f"docs index missing {name}")

    def test_documentation_index_includes_release_development_surfaces(self) -> None:
        docs_index = self.read("docs/README.md")
        for required in (
            "CONTRIBUTING.md",
            "CHANGELOG.md",
            "evals/",
            "PULL_REQUEST_TEMPLATE.md",
            "validate.yml",
            "validate_contract_version.py",
            "validate_repo.py",
            "validate_distribution.py",
        ):
            self.assertIn(required, docs_index, required)

    def test_contributing_documents_complete_ci_suite(self) -> None:
        contributing = self.read("CONTRIBUTING.md")
        required_commands = (
            "python .github/scripts/validate_contract_version.py",
            "python -m unittest discover -s evals/tests -v",
            "python evals/personal-hybrid-intent/tests/test_score_intent.py",
            "python -m unittest discover -s skills/cca/assets/hybrid-workspace/tests -v",
            "python skills/cca/assets/hybrid-workspace/audit.py --self-test",
            "python .github/scripts/validate_repo.py",
            "python .github/scripts/validate_distribution.py",
        )
        for command in required_commands:
            self.assertIn(command, contributing, command)

    def test_contributing_defines_end_to_end_change_workflow(self) -> None:
        contributing = self.read("CONTRIBUTING.md")
        for required in (
            "every repository change",
            "PULL_REQUEST_TEMPLATE.md",
            "CHANGELOG.md",
            "Unreleased",
            "exact PR head",
            "Semantic Versioning",
            "MAJOR",
            "MINOR",
            "PATCH",
            "metadata.version",
        ):
            self.assertIn(required, contributing, required)

    def test_pull_request_template_covers_cca_release_contract(self) -> None:
        path = ROOT / ".github/PULL_REQUEST_TEMPLATE.md"
        self.assertTrue(path.is_file(), "CCA requires a pull request template")
        text = path.read_text(encoding="utf-8")
        for required in (
            "Upstream authority",
            "Compatibility / conformance claims",
            "Documentation and distribution",
            "Validation",
            "boundary + semantic role -> binding",
        ):
            self.assertIn(required, text, required)

    def test_agents_requires_contributing_before_repository_changes(self) -> None:
        agents = self.read("AGENTS.md")
        self.assertIn("Before modifying repository content", agents)
        self.assertIn("CONTRIBUTING.md", agents)
        self.assertIn("PULL_REQUEST_TEMPLATE.md", agents)
        self.assertIn("complete validation suite", agents)

    def test_whitepaper_describes_current_hybrid_v2(self) -> None:
        paper = self.read("examples/publications/paper.md")
        self.assertIn("current bundled profile schema is v2", paper.lower())
        self.assertIn("reference.curated", paper)
        self.assertIn("reference.collected", paper)
        self.assertNotIn("profile uses a frozen-v1 `WORKSPACE.yaml` semantic/policy matrix", paper)
        self.assertNotIn("`CONTEXT.md` is only its frozen-v1 default binding", paper)

    def test_reference_markdown_targets_do_not_contain_stray_quotes(self) -> None:
        text = self.read("docs/references.md")
        targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        malformed = []
        for target in targets:
            first_token = target.strip().split(maxsplit=1)[0]
            if first_token.endswith(('"', "'")):
                malformed.append(target)
        self.assertEqual([], malformed, f"Malformed Markdown targets: {malformed}")
        self.assertNotRegex(text, r"\]\([^)]*\)\[[^\]]+\]\(")

    def test_primary_public_product_identity_is_architecture(self) -> None:
        surfaces = {
            "AGENTS.md": "CCA is an agent-agnostic interoperability architecture",
            "examples/publications/article.md": "CCA (Convergent Context Architecture) is an evolving, agent-agnostic interoperability architecture",
            "examples/publications/blog.md": "CCA (Convergent Context Architecture) is an agent-agnostic interoperability architecture",
        }
        for path, expected in surfaces.items():
            self.assertIn(expected, self.read(path), path)

    def test_pre_1_0_wip_is_explicitly_historical(self) -> None:
        wip = self.read("docs/_wip.md")
        self.assertIn("Historical pre-1.0 design notebook", wip)
        self.assertIn("not current release authority", wip)

    def test_release_citation_metadata_is_consistent(self) -> None:
        root_cff = self.read("CITATION.cff")
        skill_cff = self.read("skills/cca/CITATION.cff")
        for text in (root_cff, skill_cff):
            self.assertIn("version: '1.2.0'", text)
            self.assertIn("date-released: '2026-08-27'", text)
            self.assertIn("CCA is an agent-agnostic interoperability architecture", text)
            self.assertIn("title: 'CCA: Convergent Context Architecture'", text)
            self.assertIn("repository-code: 'https://github.com/yonasuriv/CCA'", text)

    def test_release_history_exists(self) -> None:
        changelog = ROOT / "CHANGELOG.md"
        self.assertTrue(changelog.is_file(), "CHANGELOG.md is required for released CCA versions")
        text = changelog.read_text(encoding="utf-8")
        self.assertIn("## Unreleased", text)
        self.assertIn("## 1.2.0 - 2026-08-27", text)
        self.assertIn("## 1.1.1 - 2026-08-27", text)
        self.assertIn("## 1.1.0 - 2026-08-26", text)
        self.assertIn("## 1.0.0 - 2026-08-21", text)


if __name__ == "__main__":
    unittest.main()
