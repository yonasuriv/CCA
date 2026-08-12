#!/usr/bin/env python3
"""CCA repository regression validator.

Checks mechanical invariants that protect selected ICM-derived patterns,
Agent Skills portability, documentation integrity, and the worked example.
This is a repository regression gate, not a certification of the complete
native ICM acceptance surface. Uses only the Python standard library so
contributors and CI can run it without setup.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXAMPLE = ROOT / "examples" / "topic-research"

ERRORS: list[str] = []


def error(message: str) -> None:
    ERRORS.append(message)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        error(f"missing required file: {path.relative_to(ROOT)}")
        return ""


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = read(path)
    if not text.startswith("---\n"):
        error(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
        return {}

    try:
        block = text.split("---\n", 2)[1]
    except IndexError:
        error(f"unterminated YAML frontmatter: {path.relative_to(ROOT)}")
        return {}

    values: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values


def validate_skills() -> None:
    if not SKILLS.is_dir():
        error("skills/ directory is missing")
        return

    for skill_dir in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            error(f"skill missing SKILL.md: {skill_dir.relative_to(ROOT)}")
            continue

        meta = parse_frontmatter(skill_file)
        name = meta.get("name", "")
        description = meta.get("description", "")

        if name != skill_dir.name:
            error(f"skill name mismatch: {skill_dir.name!r} != {name!r}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            error(f"invalid Agent Skills name: {name!r}")
        if not 1 <= len(name) <= 64:
            error(f"skill name length out of range: {name!r}")
        if not 1 <= len(description) <= 1024:
            error(f"skill description length out of range: {skill_dir.name} ({len(description)})")

        text = read(skill_file)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "#")):
                continue
            target_path = (skill_dir / target.split("#", 1)[0]).resolve()
            try:
                target_path.relative_to(skill_dir.resolve())
            except ValueError:
                error(f"skill reference escapes package: {skill_dir.name}: {target}")
                continue
            if not target_path.exists():
                error(f"broken skill-local reference: {skill_dir.name}: {target}")


def validate_icm_derived_example() -> None:
    """Validate only the ICM-derived patterns the hybrid example adopts."""
    stages = EXAMPLE / "stages"
    if not stages.is_dir():
        error("worked example is missing stages/")
        return

    stage_dirs = sorted(path for path in stages.iterdir() if path.is_dir())
    for stage in stage_dirs:
        if not re.fullmatch(r"\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*", stage.name):
            error(f"non-ICM-derived stage directory name: {stage.relative_to(ROOT)}")

        contract = stage / "CONTEXT.md"
        text = read(contract)
        for heading in ("## Inputs", "## Process", "## Outputs"):
            if heading not in text:
                error(f"missing {heading!r}: {contract.relative_to(ROOT)}")

        canonical_header = "| Source | File/Location | Section/Scope | Why |"
        if canonical_header not in text:
            error(f"ICM-derived Inputs table drift: {contract.relative_to(ROOT)}")
        if "| Role |" in text or "| Section/Scope | Role | Why |" in text:
            error(f"CCA-only Role column added to ICM-derived contract: {contract.relative_to(ROOT)}")
        if not (stage / "output").is_dir():
            error(f"stage missing output/ handoff: {stage.relative_to(ROOT)}")

    expected_handoff = EXAMPLE / "stages" / "01-collect" / "output" / "2026-08-11-collect-notes.md"
    if not expected_handoff.is_file():
        error("worked example current-state handoff is missing")


def validate_markdown_links() -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        # Template links intentionally contain placeholders for files that will
        # exist only after the template is instantiated in a target workspace.
        if "assets" in path.parts and "templates" in path.parts:
            continue

        text = read(path)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = target.strip().strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            candidate = (path.parent / clean).resolve()
            if not candidate.exists():
                error(f"broken Markdown link: {path.relative_to(ROOT)} -> {target}")


def validate_required_docs() -> None:
    required = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "CITATION.cff",
        ROOT / "CONTRIBUTING.md",
        ROOT / "docs" / "getting-started.md",
        ROOT / "docs" / "faq.md",
        ROOT / "docs" / "standards.md",
        ROOT / "spec" / "SPEC.md",
        ROOT / "spec" / "compatibility.md",
    ]
    for path in required:
        if not path.is_file():
            error(f"missing required repository surface: {path.relative_to(ROOT)}")


def main() -> int:
    validate_required_docs()
    validate_skills()
    validate_icm_derived_example()
    validate_markdown_links()

    if ERRORS:
        print(f"CCA validation failed with {len(ERRORS)} issue(s):", file=sys.stderr)
        for item in ERRORS:
            print(f"- {item}", file=sys.stderr)
        return 1

    print("CCA repository validation passed (mechanical regression checks only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
