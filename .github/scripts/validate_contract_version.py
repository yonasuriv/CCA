#!/usr/bin/env python3
"""Fail when installed CCA contract behavior changes without a version bump."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys


SKILL_PATH = "skills/cca/SKILL.md"
SPEC_PATH = "skills/cca/references/core/spec.md"
CONTRACT_SENSITIVE_PREFIXES = (
    "skills/cca/references/",
    "skills/cca/assets/",
)
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
VERSION_RE = re.compile(
    r"(?ms)^metadata:\s*$.*?^\s+version:\s*[\"']([^\"']+)[\"']\s*$"
)
SPEC_VERSION_RE = re.compile(r"\*\*Version\s+((?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*))\*\*")


class VersionGateError(RuntimeError):
    pass


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        raise VersionGateError(
            f"git {' '.join(args)} failed: {result.stderr.strip() or result.stdout.strip()}"
        )
    return result


def parse_version(skill_text: str, source: str) -> str:
    if not skill_text.startswith("---\n"):
        raise VersionGateError(f"{source}: SKILL.md is missing YAML frontmatter")
    try:
        frontmatter = skill_text.split("---", 2)[1]
    except IndexError as error:
        raise VersionGateError(f"{source}: malformed SKILL.md frontmatter") from error
    match = VERSION_RE.search(frontmatter)
    if not match:
        raise VersionGateError(f"{source}: metadata.version is required")
    version = match.group(1)
    if not SEMVER_RE.fullmatch(version):
        raise VersionGateError(f"{source}: metadata.version must be stable SemVer x.y.z, got {version!r}")
    return version


def parse_historical_spec_version(spec_text: str, source: str) -> str:
    match = SPEC_VERSION_RE.search(spec_text)
    if not match:
        raise VersionGateError(
            f"{source}: cannot recover historical CCA version; expected '**Version x.y.z**'"
        )
    return match.group(1)


def semver_tuple(version: str) -> tuple[int, int, int]:
    return tuple(int(part) for part in version.split("."))  # type: ignore[return-value]


def ref_exists(repo: Path, ref: str) -> bool:
    return run_git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}", check=False).returncode == 0


def resolve_base(repo: Path, explicit: str | None) -> str | None:
    candidates: list[str] = []
    if explicit:
        candidates.append(explicit)
    env_base = os.getenv("CCA_VERSION_BASE")
    if env_base:
        candidates.append(env_base)
    github_base = os.getenv("GITHUB_BASE_REF")
    if github_base:
        candidates.extend((f"origin/{github_base}", github_base))

    ref_name = os.getenv("GITHUB_REF_NAME")
    if ref_name and ref_name != "main":
        candidates.append("origin/main")

    candidates.append("HEAD^")

    for candidate in candidates:
        if ref_exists(repo, candidate):
            return candidate
    return None


def changed_paths(repo: Path, base: str) -> list[str]:
    triple = run_git(repo, "diff", "--name-only", f"{base}...HEAD", check=False)
    result = triple if triple.returncode == 0 else run_git(repo, "diff", "--name-only", f"{base}..HEAD")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def is_contract_sensitive(path: str) -> bool:
    return path == SKILL_PATH or any(path.startswith(prefix) for prefix in CONTRACT_SENSITIVE_PREFIXES)


def version_at(repo: Path, ref: str) -> str:
    skill_result = run_git(repo, "show", f"{ref}:{SKILL_PATH}", check=False)
    if skill_result.returncode != 0:
        raise VersionGateError(
            f"{ref}: historical baseline is missing {SKILL_PATH}; cannot determine CCA version"
        )

    try:
        return parse_version(skill_result.stdout, f"{ref}:{SKILL_PATH}")
    except VersionGateError as skill_error:
        if "metadata.version is required" not in str(skill_error):
            raise

    spec_result = run_git(repo, "show", f"{ref}:{SPEC_PATH}", check=False)
    if spec_result.returncode != 0:
        raise VersionGateError(
            f"{ref}: historical SKILL.md has no metadata.version and {SPEC_PATH} is unavailable"
        )
    return parse_historical_spec_version(spec_result.stdout, f"{ref}:{SPEC_PATH}")


def validate(repo: Path, base: str | None) -> int:
    skill = repo / SKILL_PATH
    if not skill.is_file():
        raise VersionGateError(f"missing {SKILL_PATH}")
    current = parse_version(skill.read_text(encoding="utf-8"), SKILL_PATH)

    if base is None:
        print(f"PASS: CCA contract version {current}; no comparable Git baseline found")
        return 0

    baseline = version_at(repo, base)
    paths = changed_paths(repo, base)
    sensitive = sorted(path for path in paths if is_contract_sensitive(path))

    if not sensitive:
        print(f"PASS: no contract-sensitive installed CCA changes since {base}; version {current}")
        return 0

    if current == baseline:
        joined = "\n  - ".join(sensitive)
        raise VersionGateError(
            "contract-sensitive installed CCA files changed without a version bump "
            f"({baseline} -> {current}) since {base}:\n  - {joined}"
        )

    if semver_tuple(current) <= semver_tuple(baseline):
        raise VersionGateError(
            f"contract-sensitive changes require a forward version bump; {baseline} -> {current}"
        )

    print(
        f"PASS: contract-sensitive CCA changes carry version bump {baseline} -> {current} "
        f"since {base} ({len(sensitive)} sensitive path(s))"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--base", help="Git ref to compare against")
    args = parser.parse_args()
    repo = args.repo.resolve()

    try:
        base = resolve_base(repo, args.base)
        return validate(repo, base)
    except VersionGateError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
