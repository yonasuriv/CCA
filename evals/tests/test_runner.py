from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path

import sys

EVALS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVALS))

import runner  # type: ignore  # noqa: E402


class EvaluationRunnerTests(unittest.TestCase):
    def test_discovers_exactly_fourteen_numbered_cases(self) -> None:
        cases = runner.discover_cases(EVALS / "cases")
        self.assertEqual(len(cases), 14)
        self.assertEqual([case.name[:2] for case in cases], [f"{i:02d}" for i in range(1, 15)])

    def test_every_case_has_required_contract(self) -> None:
        for case_dir in runner.discover_cases(EVALS / "cases"):
            case = runner.load_case(case_dir)
            self.assertEqual(case["id"], case_dir.name[:2])
            self.assertTrue(case["name"])
            self.assertIn(case["baseline"], {"icm", "icm-architect", "none"})
            self.assertIsInstance(case["profiles"], list)
            self.assertTrue(case["expected_behavior"])
            self.assertTrue((case_dir / "prompt.md").is_file())
            self.assertTrue((case_dir / "fixture").is_dir())
            self.assertTrue((case_dir / "assertions.json").is_file())

    def test_prepare_run_isolates_fixture_and_arm_material(self) -> None:
        case_dir = EVALS / "cases" / "01-native-icm"
        case = runner.load_case(case_dir)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cca = root / "cca"
            baseline = root / "baseline"
            (cca / "references").mkdir(parents=True)
            (cca / "SKILL.md").write_text("cca", encoding="utf-8")
            baseline.mkdir()
            (baseline / "BASELINE.md").write_text("upstream", encoding="utf-8")

            arm_a = runner.prepare_run(case, "A", root / "runs", cca, baseline)
            arm_b = runner.prepare_run(case, "B", root / "runs", cca, baseline)

            self.assertTrue((arm_a / "workspace" / "CLAUDE.md").is_file())
            self.assertTrue((arm_b / "workspace" / "CLAUDE.md").is_file())
            self.assertTrue((arm_a / "baseline" / "BASELINE.md").is_file())
            self.assertFalse((arm_a / "cca").exists())
            self.assertTrue((arm_b / "cca" / "SKILL.md").is_file())
            self.assertFalse((arm_b / "baseline").exists())

    def test_run_agent_executes_in_workspace_and_records_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            result = runner.run_agent(
                [sys.executable, "-c", "from pathlib import Path; Path('made.txt').write_text('ok')"],
                workspace,
                {"CCA_TEST": "1"},
            )
            self.assertEqual(result["returncode"], 0)
            self.assertTrue((workspace / "made.txt").is_file())
            self.assertGreaterEqual(result["duration_ms"], 0)

    def test_evaluate_case_supports_required_assertion_types(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "required.txt").write_text("hello world", encoding="utf-8")
            (workspace / "unchanged.txt").write_text("stable", encoding="utf-8")
            digest = hashlib.sha256(b"stable").hexdigest()
            assertions = {
                "assertions": [
                    {"type": "path_exists", "path": "required.txt"},
                    {"type": "path_absent", "path": "forbidden.txt"},
                    {"type": "file_contains", "path": "required.txt", "text": "hello"},
                    {"type": "file_not_contains", "path": "required.txt", "text": "goodbye"},
                    {"type": "sha256_equals", "path": "unchanged.txt", "sha256": digest},
                    {"type": "glob_count", "pattern": "*.txt", "count": 2},
                ]
            }
            assertion_path = workspace / "assertions.json"
            assertion_path.write_text(json.dumps(assertions), encoding="utf-8")
            report = runner.evaluate_assertions(workspace, assertion_path)
            self.assertTrue(report["passed"])
            self.assertEqual(len(report["results"]), 6)

    def test_write_result_round_trips_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "result.json"
            payload = {"case": "03", "arm": "B", "passed": True}
            runner.write_result(payload, path)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), payload)


if __name__ == "__main__":
    unittest.main()
