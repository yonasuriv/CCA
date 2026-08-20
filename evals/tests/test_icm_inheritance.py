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
        self.assertIn("Layer 0 `CLAUDE.md`", combined)
        self.assertIn("Preserve native `CLAUDE.md` Layer-0 entry semantics", combined)
        self.assertIn("not universal CCA requirements", combined)

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
            "routing purity",
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

    def test_icm_inheritance_preserves_upstream_authority_without_universalizing_it(self):
        text = (CORE / "icm-inheritance.md").read_text(encoding="utf-8")
        self.assertIn("current upstream ICM repository remains authoritative", text)
        self.assertIn("upstream wins", text)
        self.assertIn("Regression", text)
        self.assertIn("never converts an upstream ICM failure into a pass", text)
        self.assertIn("not universal CCA requirements", text)
        self.assertIn("ICM-derived", text)


if __name__ == "__main__":
    unittest.main()
