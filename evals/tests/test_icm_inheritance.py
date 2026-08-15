from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
ARCHITECT = ROOT / "skills" / "cca" / "references" / "architect"


class ICMInheritanceContractTests(unittest.TestCase):
    def test_native_icm_layer_zero_preserves_claude_md(self):
        texts = {
            path.name: path.read_text(encoding="utf-8")
            for path in (
                ARCHITECT / "core.md",
                ARCHITECT / "mode.md",
                ARCHITECT / "forms.md",
                ARCHITECT / "native-icm-setup.md",
            )
        }
        for name, text in texts.items():
            self.assertNotIn(
                "`AGENTS.md` as the authoritative Layer-0 catalog",
                text,
                f"{name} redefines native ICM Layer 0",
            )
        combined = "\n".join(texts.values())
        self.assertIn("native Layer-0 `CLAUDE.md`", combined)

    def test_claimed_native_icm_surface_is_preserved(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
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
            "selective",
            "canonical",
            "setup",
            "status",
            "questionnaire",
            "tool prerequisite",
            "checkpoints",
            "audits",
            "spec",
            "value",
            "docs-over-outputs",
            "shared constants",
            "quality guardrails",
            "walk test",
            "Build mode",
            "Restructure mode",
            "factory",
            "product",
        ]
        missing = [anchor for anchor in anchors if anchor.lower() not in combined.lower()]
        self.assertEqual([], missing, f"Missing inherited ICM capability anchors: {missing}")


if __name__ == "__main__":
    unittest.main()
