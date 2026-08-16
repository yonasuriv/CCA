from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
SKILL = ROOT / "skills" / "cca" / "SKILL.md"


class PositioningAndRoutingTests(unittest.TestCase):
    def test_readme_states_cca_on_its_own_terms(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("bridge human knowledge work and agentic work", text.lower())
        self.assertIn("without forcing it into a new competing convention", text.lower())
        self.assertIn("reducing technical debt", text.lower())
        self.assertIn("operational costs", text.lower())
        self.assertNotIn("## Is CCA better than ICM?", text)
        self.assertNotIn("behavioral superiority over ICM", text)

    def test_skill_description_does_not_trigger_for_ordinary_implementation(self):
        text = SKILL.read_text(encoding="utf-8")
        frontmatter = text.split("---\n", 2)[1]
        description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE).group(1)
        self.assertIn("Do not use for ordinary implementation", description)

    def test_root_router_stops_after_smallest_matching_mode(self):
        text = SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("do not enter `architect`", text)
        self.assertIn("stop loading cca references", text)


if __name__ == "__main__":
    unittest.main()
