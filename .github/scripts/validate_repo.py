#!/usr/bin/env python3
"""CCA repository regression validator.

Checks mechanical invariants that protect selected ICM-derived patterns,
Agent Skills package locality, documentation integrity, the unified skill layout,
and the worked example. This is a repository regression gate, not certification
of the complete native ICM acceptance surface.

Uses only the Python standard library so contributors and CI can run it without
setup.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent
ROOT = SCRIPT.parents[1]
SKILLS = ROOT / "skills"
CCA = SKILLS / "cca"
EXAMPLE = ROOT / "examples" / "workspaces" / "topic-research"

ERRORS: list[str] = []


def error(message: str) -> None:
    ERRORS.append(message)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        error(f"Missing required file: {path.relative_to(ROOT)}")
        return ""


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = read(path)
    if not text.startswith("---\n"):
        error(f"Missing YAML frontmatter: {path.relative_to(ROOT)}")
        return {}

    try:
        block = text.split("---\n", 2)[1]
    except IndexError:
        error(f"Unterminated YAML frontmatter: {path.relative_to(ROOT)}")
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


def validate_single_skill_package() -> None:
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir()) if SKILLS.is_dir() else []
    names = [path.name for path in skill_dirs]
    if names != ["cca"]:
        error(f"Expected exactly one first-party skill package ['cca']; found {names}")


def validate_unified_skill_surface() -> None:
    required = [
        CCA / "SKILL.md",
        CCA / "references/core/spec.md",
        CCA / "references/core/compatibility.md",
        CCA / "references/core/method-composition.md",
        CCA / "references/core/adapters.md",
        CCA / "references/architect/mode.md",
        CCA / "references/architect/core.md",
        CCA / "references/architect/forms.md",
        CCA / "references/architect/methods.md",
        CCA / "references/architect/system-map.md",
        CCA / "references/architect/native-icm-setup.md",
        CCA / "references/advisor/mode.md",
        CCA / "references/advisor/engineering-principles.md",
        CCA / "references/advisor/frameworks-and-methodologies.md",
        CCA / "references/advisor/security-and-adversarial-thinking.md",
        CCA / "references/advisor/agent-system-design.md",
        CCA / "references/advisor/context-engineering.md",
        CCA / "references/advisor/ai-ml-practice.md",
        CCA / "references/advisor/escalation-triggers.md",
        CCA / "references/operations/scaffold.md",
        CCA / "references/operations/sync.md",
        CCA / "references/operations/ingest.md",
        CCA / "references/operations/query.md",
        CCA / "references/operations/lint.md",
        CCA / "assets/templates",
    ]
    for path in required:
        if not path.exists():
            error(f"Missing unified CCA skill surface: {path.relative_to(ROOT)}")

    # Core owns adapter semantics; architect may consume but must not duplicate it.
    if (CCA / "references/architect/adapters.md").exists():
        error("Duplicate adapter authority: architect/adapters.md must not coexist with core/adapters.md")


def validate_skills() -> None:
    if not SKILLS.is_dir():
        error("skills/ directory is missing")
        return

    for skill_dir in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            error(f"Skill missing SKILL.md: {skill_dir.relative_to(ROOT)}")
            continue

        meta = parse_frontmatter(skill_file)
        name = meta.get("name", "")
        description = meta.get("description", "")

        if name != skill_dir.name:
            error(f"Skill name mismatch: {skill_dir.name!r} != {name!r}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            error(f"Invalid Agent Skills name: {name!r}")
        if not 1 <= len(name) <= 64:
            error(f"Skill name length out of range: {name!r}")
        if not 1 <= len(description) <= 1024:
            error(f"Skill description length out of range: {skill_dir.name} ({len(description)})")

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

        if re.search(r"(?:\.\./)+cca-[a-z0-9-]+/", text):
            error(f"Skill uses sibling filesystem dependency: {skill_dir.name}")



def validate_skill_self_containment() -> None:
    """The installed skill must not depend on removed sibling packages or repo-only runtime paths."""
    banned = {
        "cca-advisor": "removed standalone skill id",
        "cca-architect": "removed standalone skill id",
        "cca-scaffold": "removed standalone skill id",
        "cca-sync": "removed standalone skill id",
        "cca-ingest": "removed standalone skill id",
        "cca-query": "removed standalone skill id",
        "cca-lint": "removed standalone skill id",
        "spec/SPEC.md": "removed repository-level spec path",
        "spec/compatibility.md": "removed repository-level spec path",
        "spec/method-composition.md": "removed repository-level spec path",
        "../docs/": "repository-only path from installed package",
        "../../docs/": "repository-only path from installed package",
        "../../../docs/": "repository-only path from installed package",
        "../../../../docs/": "repository-only path from installed package",
    }
    for path in sorted(CCA.rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".json", ".py", ".sh"}:
            continue
        text = read(path)
        for pattern, reason in banned.items():
            if pattern in text:
                error(f"Installed skill is not self-contained: {path.relative_to(ROOT)} contains {pattern!r} ({reason})")


def validate_session_semantics() -> None:
    """Prevent regressions into the rejected audit conclusions and old package model."""
    checks = {
        CCA / "references/architect/forms.md": [
            ("`AGENTS.md` as the authoritative Layer-0 catalog", "old native-ICM Layer-0 claim"),
            ("single-line `@AGENTS.md` include only when a harness needs it", "universal native-entry rewrite"),
        ],
        CCA / "references/architect/mode.md": [
            ("`AGENTS.md` as the authoritative Layer-0 catalog", "old native-ICM Layer-0 claim"),
            ("references/core.md", "stale architect-local path"),
            ("references/methods.md", "stale architect-local path"),
            ("references/adapters.md", "stale architect-local path"),
        ],
        CCA / "references/core/method-composition.md": [
            ("suite of focused capabilities", "old multi-package skill model"),
            ("multiple skills", "old multi-package skill model"),
        ],
    }
    for path, forbidden in checks.items():
        text = read(path)
        for pattern, reason in forbidden:
            if pattern in text:
                error(f"Session semantic regression in {path.relative_to(ROOT)}: {pattern!r} ({reason})")

    required_fragments = {
        CCA / "references/architect/system-map.md": ["live", "leftover", "ghost", "Hits", "Does not hit", "Cold-agent walk", "Re-verify"],
        CCA / "references/architect/forms.md": ["Record Library defaults", "half-created", "frequency", "System Map", "full display name", "beta-corp"],
        CCA / "references/architect/native-icm-setup.md": ["Bidirectional coverage gate", "Question/answer → use", "Placeholder/field → source", "Conditional stage → condition"],
        CCA / "references/advisor/mode.md": ["These are seven references, not six."],
    }
    for path, fragments in required_fragments.items():
        text = read(path)
        for fragment in fragments:
            if fragment not in text:
                error(f"Missing session-required semantic in {path.relative_to(ROOT)}: {fragment!r}")


def _validate_case_suite(directory: str, expected_count: int) -> None:
    cases = ROOT / "evals" / directory
    dirs = sorted(path for path in cases.iterdir() if path.is_dir() and re.match(r"^\d{2}-", path.name)) if cases.is_dir() else []
    expected = [f"{i:02d}" for i in range(1, expected_count + 1)]
    found = [path.name[:2] for path in dirs]
    if found != expected:
        error(f"Expected {directory} evaluation cases 01..{expected_count:02d}; found {found}")
        return
    for path in dirs:
        for required in ("case.json", "prompt.md", "assertions.json"):
            if not (path / required).is_file():
                error(f"Evaluation case missing {required}: {path.relative_to(ROOT)}")
        fixture = path / "fixture"
        if not fixture.is_dir() or not any(p.is_file() for p in fixture.rglob("*")):
            error(f"Evaluation case missing non-empty fixture: {path.relative_to(ROOT)}")
        assertions = path / "assertions.json"
        if assertions.is_file() and '"assertions": []' in read(assertions).replace(" ", ""):
            error(f"Evaluation case has empty assertions: {path.relative_to(ROOT)}")


def validate_evaluation_cases() -> None:
    _validate_case_suite("cases", 14)
    _validate_case_suite("methodologies", 20)


def validate_methodology_corpus() -> None:
    path = CCA / "references/advisor/frameworks-and-methodologies.md"
    text = read(path)
    anchors = [
        "Cynefin", "SAFe", "LeSS", "Disciplined Agile", "waterfall", "stage-gate", "V-model",
        "Scrum", "Kanban", "DSDM", "FDD", "ASD", "XP", "RAD", "IID", "Lean",
        "RUP / UP", "DevOps", "TDD", "MDE", "PSP", "TSP", "SEMAT", "Essence",
    ]
    for anchor in anchors:
        if anchor not in text:
            error(f"Methodology corpus lost coverage anchor: {anchor!r}")

def validate_icm_derived_example() -> None:
    """Validate only the ICM-derived patterns the hybrid example adopts."""
    stages = EXAMPLE / "stages"
    if not stages.is_dir():
        error("Worked example is missing stages/")
        return

    stage_dirs = sorted(path for path in stages.iterdir() if path.is_dir())
    for stage in stage_dirs:
        if not re.fullmatch(r"\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*", stage.name):
            error(f"Non-ICM-derived stage directory name: {stage.relative_to(ROOT)}")

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
            error(f"Stage missing output/ handoff: {stage.relative_to(ROOT)}")

    expected_handoff = EXAMPLE / "stages/01-collect/output/2026-08-11-collect-notes.md"
    if not expected_handoff.is_file():
        error("Worked example current-state handoff is missing")


def validate_architect_templates() -> None:
    """Catch regressions in templates instantiated into ICM-derived workspaces."""
    template_dir = CCA / "assets/templates"
    if not template_dir.is_dir():
        error("cca templates directory is missing")
        return

    underscore_stage = re.compile(r"0\d_|01_|0\[N\+?1\]_|0\[N\]_|\d{2}_[a-z]")
    for path in sorted(template_dir.glob("*.md")):
        text = read(path)
        for line_no, line in enumerate(text.splitlines(), start=1):
            if underscore_stage.search(line):
                error(f"underscore stage variant in template {path.name}:{line_no}")
            if "\u2014" in line:
                error(f"em dash in template {path.name}:{line_no} (native ICM guardrail)")


def validate_example_style() -> None:
    """The ICM-derived worked example inherits the native no-em-dash guardrail."""
    for path in sorted(EXAMPLE.rglob("*.md")):
        text = read(path)
        for line_no, line in enumerate(text.splitlines(), start=1):
            if "\u2014" in line:
                error(f"em dash in example {path.relative_to(ROOT)}:{line_no}")


def validate_current_documentation_paths() -> None:
    """Catch stale textual directory maps that Markdown-link checks cannot see."""
    current_docs = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "docs/README.md",
        ROOT / "docs/getting-started.md",
        ROOT / "docs/faq.md",
        ROOT / "docs/method-composition.md",
        ROOT / "docs/scenarios.md",
        ROOT / "examples/README.md",
        ROOT / "examples/publications/blog.md",
        ROOT / "examples/publications/article.md",
        ROOT / "examples/publications/paper.md",
    ]
    stale_patterns = {
        "skills/cca-advisor": "removed seven-package skill layout",
        "skills/cca-architect": "removed seven-package skill layout",
        "skills/cca-scaffold": "removed seven-package skill layout",
        "skills/cca-sync": "removed seven-package skill layout",
        "skills/cca-ingest": "removed seven-package skill layout",
        "skills/cca-query": "removed seven-package skill layout",
        "skills/cca-lint": "removed seven-package skill layout",
        "spec/SPEC.md": "removed repository-level spec path",
        "spec/compatibility.md": "removed repository-level spec path",
        "spec/method-composition.md": "removed repository-level spec path",
        "examples/articles/": "removed examples path",
        "docs/principles.md": "removed docs path",
    }
    for path in current_docs:
        if not path.exists():
            continue
        text = read(path)
        for pattern, reason in stale_patterns.items():
            if pattern in text:
                error(f"Stale documented path in {path.relative_to(ROOT)}: {pattern!r} ({reason})")


def validate_markdown_links() -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        if "assets" in path.parts and "templates" in path.parts:
            continue
        # Paper may use repository-root citations/identifiers that are not local links.
        if path.name in {"paper.md", "paper-brief.md"}:
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
                error(f"Broken Markdown link: {path.relative_to(ROOT)} -> {target}")


def validate_required_docs() -> None:
    required = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "CITATION.cff",
        ROOT / "CONTRIBUTING.md",
        ROOT / "docs/README.md",
        ROOT / "docs/getting-started.md",
        ROOT / "docs/faq.md",
        ROOT / "docs/scenarios.md",
        ROOT / "docs/method-composition.md",
        ROOT / "docs/standards.md",
        ROOT / "examples/publications/blog.md",
        ROOT / "examples/publications/article.md",
        ROOT / "examples/publications/paper.md",
        ROOT / "evals/README.md",
        ROOT / "evals/cases/README.md",
        ROOT / "evals/methodologies/README.md",
    ]
    for path in required:
        if not path.is_file():
            error(f"Missing required repository surface: {path.relative_to(ROOT)}")


def validate_publications() -> None:
    minimum_bytes = {"blog.md": 1000, "article.md": 4000, "paper.md": 12000}
    for name, minimum in minimum_bytes.items():
        path = ROOT / "examples/publications" / name
        if path.is_file() and path.stat().st_size < minimum:
            error(f"Publication appears incomplete: {path.relative_to(ROOT)} ({path.stat().st_size} < {minimum} bytes)")


def main() -> int:
    validate_required_docs()
    validate_single_skill_package()
    validate_unified_skill_surface()
    validate_skills()
    validate_skill_self_containment()
    validate_session_semantics()
    validate_evaluation_cases()
    validate_methodology_corpus()
    validate_icm_derived_example()
    validate_architect_templates()
    validate_example_style()
    validate_current_documentation_paths()
    validate_publications()
    validate_markdown_links()

    if ERRORS:
        print(f"\nCCA validation failed with {len(ERRORS)} issue(s):", file=sys.stderr)
        for item in ERRORS:
            print(f"- {item}", file=sys.stderr)
        return 1

    print("\nCCA repository validation passed (mechanical regression checks only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())