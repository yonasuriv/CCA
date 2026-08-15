#!/usr/bin/env python3
"""Prepare and grade isolated CCA behavioral evaluation runs.

This runner never simulates an agent. It prepares isolated workspaces, executes a
caller-supplied command when requested, and grades deterministic filesystem
assertions. Model/runtime selection and equal-budget enforcement remain the
responsibility of the external harness invoking this script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any


REQUIRED_CASE_FILES = ("case.json", "prompt.md", "assertions.json")


def discover_cases(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and len(path.name) >= 3 and path.name[:2].isdigit() and path.name[2] == "-"
    )


def suite_root(evals_root: Path, suite: str) -> Path:
    mapping = {
        "core": "cases",
        "methodologies": "methodologies",
        "icm-parity": "icm-parity",
        "cca-extensions": "cca-extensions",
    }
    try:
        return evals_root / mapping[suite]
    except KeyError as exc:
        raise ValueError(f"unknown evaluation suite: {suite}") from exc


def load_case(case_dir: Path) -> dict[str, Any]:
    for name in REQUIRED_CASE_FILES:
        path = case_dir / name
        if not path.is_file():
            raise ValueError(f"case {case_dir.name} missing {name}")
    if not (case_dir / "fixture").is_dir():
        raise ValueError(f"case {case_dir.name} missing fixture/")
    data = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
    required = ("id", "name", "baseline", "profiles", "expected_behavior")
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"case {case_dir.name} missing manifest keys: {', '.join(missing)}")
    data["_case_dir"] = str(case_dir.resolve())
    return data


def load_capability_catalog(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    capabilities = payload.get("capabilities")
    if not isinstance(capabilities, list):
        raise ValueError(f"capability catalog {path} must contain a capabilities list")
    return capabilities


def _copy_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def material_path_for_arm(arm: str, run_dir: Path) -> Path | None:
    if arm == "A":
        return run_dir / "baseline"
    if arm == "B":
        return run_dir / "cca"
    if arm == "C":
        return None
    raise ValueError("arm must be A, B, or C")


def prepare_run(
    case: dict[str, Any],
    arm: str,
    run_root: Path,
    cca_skill: Path,
    baseline_root: Path | None,
) -> Path:
    if arm not in {"A", "B", "C"}:
        raise ValueError("arm must be A, B, or C")
    case_dir = Path(case["_case_dir"])
    destination = run_root / f"{case['id']}-{arm}"
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    _copy_tree(case_dir / "fixture", destination / "workspace")
    shutil.copy2(case_dir / "prompt.md", destination / "prompt.md")
    shutil.copy2(case_dir / "assertions.json", destination / "assertions.json")
    (destination / "case.json").write_text(
        json.dumps({key: value for key, value in case.items() if not key.startswith("_")}, indent=2) + "\n",
        encoding="utf-8",
    )

    if arm == "A":
        if case["baseline"] != "none":
            if baseline_root is None or not baseline_root.is_dir():
                raise ValueError(f"case {case['id']} requires baseline material")
            _copy_tree(baseline_root, destination / "baseline")
    elif arm == "B":
        if not (cca_skill / "SKILL.md").is_file():
            raise ValueError("CCA arm requires an installable skill root containing SKILL.md")
        _copy_tree(cca_skill, destination / "cca")
    # Arm C intentionally receives no tested repository material.
    return destination


def run_agent(command: list[str], workspace: Path, env: dict[str, str] | None = None) -> dict[str, Any]:
    if not command:
        raise ValueError("agent command cannot be empty")
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    started = time.monotonic()
    process = subprocess.run(command, cwd=workspace, env=merged_env, text=True, capture_output=True, check=False)
    duration_ms = int((time.monotonic() - started) * 1000)
    return {
        "command": command,
        "returncode": process.returncode,
        "duration_ms": duration_ms,
        "stdout": process.stdout,
        "stderr": process.stderr,
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate_assertions(workspace: Path, assertion_path: Path) -> dict[str, Any]:
    payload = json.loads(assertion_path.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    for assertion in payload.get("assertions", []):
        kind = assertion["type"]
        passed = False
        detail = ""
        if kind == "path_exists":
            target = workspace / assertion["path"]
            passed = target.exists()
            detail = str(target)
        elif kind == "path_absent":
            target = workspace / assertion["path"]
            passed = not target.exists()
            detail = str(target)
        elif kind == "file_contains":
            target = workspace / assertion["path"]
            passed = target.is_file() and assertion["text"] in target.read_text(encoding="utf-8")
            detail = f"{target} contains {assertion['text']!r}"
        elif kind == "file_not_contains":
            target = workspace / assertion["path"]
            passed = target.is_file() and assertion["text"] not in target.read_text(encoding="utf-8")
            detail = f"{target} excludes {assertion['text']!r}"
        elif kind == "sha256_equals":
            target = workspace / assertion["path"]
            passed = target.is_file() and _sha256(target) == assertion["sha256"]
            detail = f"{target} sha256"
        elif kind == "glob_count":
            matches = list(workspace.glob(assertion["pattern"]))
            passed = len(matches) == assertion["count"]
            detail = f"{assertion['pattern']} -> {len(matches)}"
        else:
            raise ValueError(f"unsupported assertion type: {kind}")
        results.append({"assertion": assertion, "passed": passed, "detail": detail})
    return {"passed": all(item["passed"] for item in results), "results": results}


def evaluate_case(case: dict[str, Any], workspace: Path) -> dict[str, Any]:
    return evaluate_assertions(workspace, Path(case["_case_dir"]) / "assertions.json")


def write_result(result: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", choices=("core", "methodologies", "icm-parity", "cca-extensions"), default="core")
    parser.add_argument("--case", required=True, help="Case directory or two-digit case id")
    parser.add_argument("--arm", choices=("A", "B", "C"), required=True)
    parser.add_argument("--runs", type=Path, default=Path("evals/runs"))
    parser.add_argument("--cca-skill", type=Path, default=Path("skills/cca"))
    parser.add_argument("--baseline-root", type=Path)
    parser.add_argument("--command", nargs=argparse.REMAINDER, help="Real agent command to run inside workspace/")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    evals_root = Path(__file__).resolve().parent
    cases_root = suite_root(evals_root, args.suite)
    case_dirs = discover_cases(cases_root)
    matches = [path for path in case_dirs if path.name == args.case or path.name.startswith(f"{args.case}-")]
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one case matching {args.case!r}; found {len(matches)}")
    case = load_case(matches[0])
    prepared = prepare_run(case, args.arm, args.runs, args.cca_skill, args.baseline_root)
    command_result = None
    if args.command:
        material = material_path_for_arm(args.arm, prepared)
        command_result = run_agent(
            args.command,
            prepared / "workspace",
            {
                "CCA_EVAL_CASE": case["id"],
                "CCA_EVAL_ARM": args.arm,
                "CCA_EVAL_PROMPT": str((prepared / "prompt.md").resolve()),
                "CCA_EVAL_MATERIAL": "" if material is None else str(material.resolve()),
            },
        )
    assertion_result = evaluate_assertions(prepared / "workspace", prepared / "assertions.json")
    result = {
        "case": case["id"],
        "name": case["name"],
        "arm": args.arm,
        "agent": command_result,
        "assertions": assertion_result,
        "behavioral_run_executed": command_result is not None,
    }
    write_result(result, prepared / "result.json")
    print(json.dumps(result, indent=2))
    return 0 if assertion_result["passed"] and (command_result is None or command_result["returncode"] == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
