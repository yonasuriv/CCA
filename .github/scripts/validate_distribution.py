#!/usr/bin/env python3
"""Validate CCA's portable distribution boundary and current architecture vocabulary."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "cca"
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


FROZEN_README = """Convergent Context Architecture (CCA) is an evolving, agent-agnostic interoperability architecture for filesystem-native AI context. It helps humans and AI agents understand, navigate, and operate across workspaces, projects, and bodies of knowledge by defining stable semantic roles, scoped boundaries, and configurable bindings that preserve meaning even when their concrete paths or implementations change.

CCA aims to bridge human knowledge work and agentic work without forcing existing systems into a new competing convention, by building on open standards, ecosystem conventions, established methodologies, protocols and frameworks, and based on software-engineering principles and fundamentals.

Its goal is to make automation easier in service of augmenting human capabilities while improving efficiency, reducing technical debt and unnecessary complexity, and lowering compute, context, usage, and operational costs."""

if FROZEN_README not in read(ROOT / "README.md"):
    fail("README frozen positioning statement changed or disappeared")

skill_md = read(SKILL / "SKILL.md")
for phrase in (
    "boundary + semantic role",
    "CCA-compatible",
    "Upstream-native",
    "one installable skill with seven",
    "skills/cca/",
    "Automation is the means; augmenting human capabilities is the goal.",
):
    if phrase not in skill_md:
        fail(f"SKILL.md missing governing phrase: {phrase!r}")
for mode in ("architect", "scaffold", "sync", "ingest", "query", "lint", "advise"):
    if f"`{mode}`" not in skill_md:
        fail(f"SKILL.md missing mode {mode}")

skill_dirs = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
if skill_dirs != ["cca"]:
    fail(f"expected exactly one first-party skill directory ['cca'], got {skill_dirs}")

required = [
    "references/core/spec.md",
    "references/core/compatibility.md",
    "references/core/method-composition.md",
    "references/architect/hybrid-workspace.md",
    "references/operations/scaffold.md",
    "references/operations/sync.md",
    "references/operations/lint.md",
    "assets/hybrid-workspace/WORKSPACE.yaml",
    "assets/hybrid-workspace/AGENTS.md",
    "assets/hybrid-workspace/schema.py",
    "assets/hybrid-workspace/generate.py",
    "assets/hybrid-workspace/audit.py",
    "assets/hybrid-workspace/requirements.txt",
    "assets/hybrid-workspace/tests/test_freeze.py",
    "assets/hybrid-workspace/tests/test_targeting.py",
]
for rel in required:
    if not (SKILL / rel).is_file():
        fail(f"portable CCA package missing required resource: skills/cca/{rel}")

profile_ref = read(SKILL / "references" / "architect" / "hybrid-workspace.md")
for phrase in ("not a new CCA mode", "explicit target", "assets/hybrid-workspace/", "context.router", "Repository-global files are never runtime dependencies"):
    if phrase not in profile_ref:
        fail(f"hybrid profile reference missing invariant: {phrase!r}")

generator = read(SKILL / "assets" / "hybrid-workspace" / "generate.py")
for phrase in ('parser.add_argument("--target", required=True', "target must be outside the installed hybrid-workspace tool package", 'slots_by_key(data)["context.router"]["binding"]'):
    if phrase not in generator:
        fail(f"hybrid generator missing target/binding safeguard: {phrase!r}")
if 'SCHEMA_PATH = ROOT / "WORKSPACE.yaml"' in generator:
    fail("hybrid generator regressed to script-directory workspace anchoring")
if '"_state/"' in generator or '"_runtime/"' in generator:
    fail("hybrid generator contains hardcoded default namespace identity")

audit = read(SKILL / "assets" / "hybrid-workspace" / "audit.py")
for phrase in ('parser.add_argument("--target"', "target must be outside the installed hybrid-workspace tool package"):
    if phrase not in audit:
        fail(f"hybrid audit missing explicit-target safeguard: {phrase!r}")

# Current curated human-facing docs must describe the installed architecture.
# Underscore-prefixed WIP files and non-normative publication snapshots are not
# curated authority and are intentionally excluded from this vocabulary gate.
doc_files = [ROOT / "CONTRIBUTING.md"] + [p for p in sorted((ROOT / "docs").glob("*.md")) if not p.name.startswith("_")]
stale = (
    "cca-architect", "cca-scaffold", "cca-sync", "cca-ingest", "cca-query", "cca-lint", "cca-advisor",
    "six first-party skills", "suite of focused Agent Skills",
    "focused Agent Skill packages intended to be distributed as the CCA skill suite",
    "Native-compatible",
)
for path in doc_files:
    text = read(path)
    for pattern in stale:
        if pattern in text:
            fail(f"{path.relative_to(ROOT)} contains stale architecture vocabulary {pattern!r}")

# Relative Markdown links inside the installed skill must remain package-local.
link_re = re.compile(r"\[[^\]]*\]\(([^)#]+)(?:#[^)]+)?\)")
for path in SKILL.rglob("*.md"):
    for raw in link_re.findall(path.read_text(encoding="utf-8")):
        if "://" in raw or raw.startswith("mailto:"):
            continue
        target = (path.parent / raw).resolve(strict=False)
        try:
            target.relative_to(SKILL.resolve())
        except ValueError:
            fail(f"skill-local markdown link escapes portable package: {path.relative_to(ROOT)} -> {raw}")

if ERRORS:
    print("CCA distribution validation failed:")
    for error in ERRORS:
        print(f"  - {error}")
    raise SystemExit(1)
print("CCA distribution validation passed")
