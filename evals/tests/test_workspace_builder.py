from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
CCA = ROOT / "skills" / "cca"
ARCHITECT = CCA / "references" / "architect"
CORE = CCA / "references" / "core"


class WorkspaceBuilderParityTests(unittest.TestCase):
    def test_architect_ships_first_class_workspace_builder(self):
        builder = ARCHITECT / "workspace-builder.md"
        self.assertTrue(builder.is_file(), "Architect must ship workspace-builder behavior")

        text = builder.read_text(encoding="utf-8")
        for anchor in (
            "Discovery",
            "Mapping",
            "Scaffolding",
            "Questionnaire design",
            "Validation and repair",
            "setup",
            "status",
            "tool prerequisites",
            "skill discovery",
            "conditional stages",
            "orphan placeholders",
            "fresh-agent",
        ):
            self.assertIn(anchor.lower(), text.lower(), f"workspace builder missing {anchor!r}")

    def test_architect_routes_creation_setup_and_status_to_builder(self):
        mode = (ARCHITECT / "mode.md").read_text(encoding="utf-8")
        skill = (CCA / "SKILL.md").read_text(encoding="utf-8")
        combined = f"{mode}\n{skill}"
        self.assertIn("workspace-builder.md", combined)
        self.assertIn("setup", combined.lower())
        self.assertIn("status", combined.lower())

    def test_native_setup_status_are_inherited_runtime_behaviors(self):
        inheritance = (CORE / "icm-inheritance.md").read_text(encoding="utf-8")
        self.assertNotIn(
            "`setup` / `status` triggers | Preserve current upstream behavior for native ICM | Delegated to upstream acceptance",
            inheritance,
        )
        self.assertIn("Inherited / preserved", inheritance)
        self.assertIn("workspace-builder.md", inheritance)

    def test_builder_preserves_native_acceptance_floor(self):
        text = (ARCHITECT / "workspace-builder.md").read_text(encoding="utf-8")
        for fragment in (
            "upstream ICM",
            "CLAUDE.md",
            "Source | File/Location | Section/Scope | Why",
            "output/",
            "one-way",
            "CONTEXT.md",
        ):
            self.assertIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
