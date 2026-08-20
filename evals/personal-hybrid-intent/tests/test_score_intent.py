#!/usr/bin/env python3
"""Deterministic intent-score tests for personal-hybrid builder eval."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "tests" / "score_intent.py"
SKILL = Path(__file__).resolve().parents[3] / "skills" / "cca"


def _load():
    spec = importlib.util.spec_from_file_location("score_intent", SCORE)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


class IntentScoreTests(unittest.TestCase):
    def test_prompt_not_in_skill(self):
        mod = _load()
        result = mod.assert_prompt_not_in_skill(SKILL)
        self.assertTrue(result["ok"], result)

    def test_score_module_imports(self):
        mod = _load()
        self.assertTrue(hasattr(mod, "score_workspace"))
        self.assertGreaterEqual(mod.PASS_SCORE, 80)

    def test_generic_personal_hybrid_score_does_not_require_icm_skeleton_artifacts(self):
        mod = _load()
        root = Path(tempfile.mkdtemp(prefix="cca-intent-score-"))
        for directory in ("projects", "notes", "sources", "knowledge", "inbox"):
            (root / directory).mkdir()
        (root / "AGENTS.md").write_text(
            "Route by relevant collection and local index. Use targeted search within the collection; broad search is fallback only.\n",
            encoding="utf-8",
        )
        (root / "README.md").write_text(
            "Daily use: capture into inbox. Sources are preserved evidence; corrections supersede old sources. "
            "Human notes stay human-owned. Maintained knowledge records contradictions and cites sources.\n",
            encoding="utf-8",
        )
        (root / "sources" / "example.md").write_text("# Source\n" + "evidence " * 12, encoding="utf-8")
        (root / "knowledge" / "concept.md").write_text(
            "# Concept\nSources: example.md\n" + "maintained synthesis " * 8,
            encoding="utf-8",
        )

        result = mod.score_workspace(root)
        ids = {check["id"] for check in result["checks"]}
        self.assertNotIn("skeleton_map_in_entry", ids)
        self.assertNotIn("folder_contracts_icm_shape", ids)
        self.assertNotIn("live_factory_stamps", ids)
        self.assertNotIn("status_without_memory", ids)
        self.assertIn("bounded_route_before_search", ids)
        self.assertFalse((root / "CONTEXT.md").exists())


if __name__ == "__main__":
    unittest.main()
