#!/usr/bin/env python3
"""Deterministic intent-score tests for personal-hybrid builder eval."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "tests" / "score_intent.py"
# tests/ -> personal-hybrid-intent/ -> evals/ -> cca-main/
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


if __name__ == "__main__":
    unittest.main()
