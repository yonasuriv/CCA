from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "cca"


class ArchitectureConvergenceTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_icm_navigation_is_not_universalized_outside_explicit_claims(self) -> None:
        surfaces = (
            "skills/cca/references/core/method-composition.md",
            "skills/cca/references/core/icm-inheritance.md",
            "skills/cca/references/architect/methods.md",
            "docs/compatibility-details.md",
        )
        forbidden = (
            "always apply the **ICM skeleton**",
            "always apply ICM skeleton roles",
            "same roles every time",
            "ICM skeleton compatibility",
            "The ICM skeleton does not change when the overlay changes",
        )
        for relative in surfaces:
            text = self.read(relative)
            for phrase in forbidden:
                with self.subTest(path=relative, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_compatibility_surfaces_use_composable_current_vocabulary(self) -> None:
        surfaces = (
            "skills/cca/references/core/spec.md",
            "skills/cca/references/core/compatibility.md",
            "docs/compatibility-details.md",
        )
        required = (
            "Upstream-native",
            "CCA-compatible",
            "CCA-conformant",
            "Profile-conformant",
            "CCA-hardened",
        )
        for relative in surfaces:
            text = self.read(relative)
            for term in required:
                with self.subTest(path=relative, term=term):
                    self.assertIn(term, text)
            self.assertNotIn("Native-compatible", text)
            self.assertNotIn("native-compatible", text)
            self.assertNotIn("three-state compatibility", text.lower())

    def test_llm_wiki_behavior_is_scoped_to_boundaries_that_use_it(self) -> None:
        spec = self.read("skills/cca/references/core/spec.md")
        self.assertNotIn("A compatible implementation SHOULD provide", spec)
        self.assertIn("When a boundary uses or claims compatibility with an LLM Wiki-style maintained-knowledge pattern", spec)

    def test_core_defines_federated_scale_without_global_manifest(self) -> None:
        spec = self.read("skills/cca/references/core/spec.md")
        self.assertIn("Local routing and scale", spec)
        self.assertIn("MUST NOT require one root manifest to enumerate arbitrary descendants", spec)
        self.assertIn("rebuildable", spec.lower())


if __name__ == "__main__":
    unittest.main()
