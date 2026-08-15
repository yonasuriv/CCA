from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
ARCHITECT = ROOT / "skills" / "cca" / "references" / "architect"
CORE = ROOT / "skills" / "cca" / "references" / "core"


class ICMInheritanceContractTests(unittest.TestCase):
    def test_native_icm_layer_zero_preserves_claude_md(self):
        paths = (
            ARCHITECT / "core.md",
            ARCHITECT / "mode.md",
            ARCHITECT / "forms.md",
            ARCHITECT / "native-icm-setup.md",
            CORE / "icm-inheritance.md",
        )
        texts = {path.name: path.read_text(encoding="utf-8") for path in paths}
        for name, text in texts.items():
            self.assertNotIn(
                "`AGENTS.md` as the authoritative Layer-0 catalog",
                text,
                f"{name} redefines native ICM Layer 0",
            )
        combined = "\n".join(texts.values())
        self.assertIn("native Layer-0 `CLAUDE.md`", combined)

    def test_claimed_native_icm_surface_is_preserved(self):
        inheritance = CORE / "icm-inheritance.md"
        self.assertTrue(inheritance.is_file(), "ICM inheritance map must ship with CCA")
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                inheritance,
                ARCHITECT / "core.md",
                ARCHITECT / "mode.md",
                ARCHITECT / "forms.md",
                ARCHITECT / "native-icm-setup.md",
            )
        )
        anchors = [
            "five-layer",
            "Source | File/Location | Section/Scope | Why",
            "output/",
            "one-way",
            "selective section routing",
            "canonical sources",
            "CONTEXT.md routing purity",
            "tool prerequisites",
            "setup",
            "status",
            "questionnaire",
            "bundled skills",
            "Specs as contracts",
            "checkpoints",
            "Stage audits",
            "Value validation",
            "Docs over outputs",
            "Shared constants",
            "Quality guardrails",
            "Placeholder syntax/coverage",
            "factory",
            "product",
            "Pipeline",
            "Umbrella",
            "Record Library",
            "Knowledge Bundle",
            "Context Map",
            "System Map",
            "Build",
            "Restructure",
            "walk test",
        ]
        missing = [anchor for anchor in anchors if anchor.lower() not in combined.lower()]
        self.assertEqual([], missing, f"Missing inherited ICM capability anchors: {missing}")

    def test_icm_inheritance_is_a_floor_not_a_competing_fork(self):
        text = (CORE / "icm-inheritance.md").read_text(encoding="utf-8")
        for fragment in (
            "current upstream ICM repository remains authoritative",
            "upstream wins",
            "Regression",
            "Passing CCA's walk test never converts an upstream failure into a pass",
        ):
            self.assertIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
