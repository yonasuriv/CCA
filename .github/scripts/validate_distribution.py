#!/usr/bin/env python3
"""Validate the portable CCA distribution boundary.

This gate intentionally validates packaging/locality, not CCA semantics. Normative
architecture lives in skills/cca/references/core and behavioral/documentation
regressions live in eval/profile tests. Keeping those concerns separate avoids
turning this script into a second hidden specification.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
SKILL = SKILLS / "cca"
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


# Distribution shape: CCA ships as one self-contained Agent Skill.
skill_dirs = sorted(p.name for p in SKILLS.iterdir() if p.is_dir()) if SKILLS.is_dir() else []
if skill_dirs != ["cca"]:
    fail(f"expected exactly one first-party skill directory ['cca'], got {skill_dirs}")

required = [
    "SKILL.md",
    "references/core/spec.md",
    "references/core/compatibility.md",
    "references/core/method-composition.md",
    "references/core/icm-inheritance.md",
    "references/architect/mode.md",
    "references/architect/core.md",
    "references/architect/methods.md",
    "references/architect/hybrid-workspace.md",
    "references/operations/scaffold.md",
    "references/operations/sync.md",
    "references/operations/ingest.md",
    "references/operations/query.md",
    "references/operations/lint.md",
    "assets/hybrid-workspace/WORKSPACE.yaml",
    "assets/hybrid-workspace/AGENTS.md",
    "assets/hybrid-workspace/schema.py",
    "assets/hybrid-workspace/generate.py",
    "assets/hybrid-workspace/audit.py",
    "assets/hybrid-workspace/requirements.txt",
    "assets/hybrid-workspace/tests/test_freeze.py",
    "assets/hybrid-workspace/tests/test_targeting.py",
    "assets/hybrid-workspace/tests/test_adversarial_targeting.py",
]
for rel in required:
    if not (SKILL / rel).is_file():
        fail(f"portable CCA package missing required resource: skills/cca/{rel}")

# Markdown references in the installed package must not depend on repository
# files that disappear when only skills/cca is installed.
link_re = re.compile(r"\[[^\]]*\]\(([^)#]+)(?:#[^)]+)?\)")
for path in SKILL.rglob("*.md"):
    for raw in link_re.findall(path.read_text(encoding="utf-8")):
        raw = raw.strip().strip("<>")
        if not raw or "://" in raw or raw.startswith("mailto:"):
            continue
        target = (path.parent / raw).resolve(strict=False)
        try:
            target.relative_to(SKILL.resolve())
        except ValueError:
            fail(f"skill-local markdown link escapes portable package: {path.relative_to(ROOT)} -> {raw}")

# Runtime/source files must not reach into repository-only docs/examples/evals
# or removed sibling CCA packages. This is a dependency-boundary check rather
# than a terminology check.
for path in SKILL.rglob("*"):
    if not path.is_file() or path.suffix not in {".md", ".py", ".sh", ".yaml", ".yml", ".json"}:
        continue
    text = path.read_text(encoding="utf-8")
    for escaped in ("../docs/", "../../docs/", "../../../docs/", "../../../../docs/", "../examples/", "../evals/"):
        if escaped in text:
            fail(f"installed skill depends on repository-global path: {path.relative_to(ROOT)} -> {escaped}")
    if re.search(r"(?:\.\./)+cca-(?:architect|advisor|scaffold|sync|ingest|query|lint)/", text):
        fail(f"installed skill depends on removed sibling CCA package: {path.relative_to(ROOT)}")

# The package entry itself must remain an Agent Skill with its own frontmatter;
# detailed frontmatter semantics are validated by the repository validator.
skill_md = read(SKILL / "SKILL.md")
if not skill_md.startswith("---\n"):
    fail("skills/cca/SKILL.md is missing YAML frontmatter")

if ERRORS:
    print("CCA distribution validation failed:")
    for error in ERRORS:
        print(f"  - {error}")
    raise SystemExit(1)

print("CCA distribution validation passed")
