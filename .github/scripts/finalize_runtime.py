#!/usr/bin/env python3
"""One-shot runtime self-containment cleanup for the unified CCA skill."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CCA = ROOT / "skills/cca"
SPEC = CCA / "references/core/spec.md"

text = SPEC.read_text(encoding="utf-8")
text = text.replace(
    "7. `AGENTS.md` is the authoritative Layer-0 catalog in CCA-created and CCA-hardened workspaces. Where a harness needs its own entry path (`CLAUDE.md`, `GEMINI.md`, ...), that file is created by directive as a single-line `@ AGENTS.md` include, never a second copy of the routing, and never shipped as a template asset.",
    "7. In CCA-created or CCA-hardened workspaces that do not already have a stricter native profile, `AGENTS.md` is the preferred canonical portable guidance surface. A harness-native entry may bridge to that guidance using the harness's current supported mechanism. In a native upstream profile such as ICM, preserve the upstream's own entry semantics first; portable guidance is an interoperable counterpart, not a declaration that it overrides the native entry.",
)
text = text.replace(
    "1. five-layer routing, with `AGENTS.md` as the authoritative Layer-0 catalog; harness entry files such as `CLAUDE.md` are created by directive as single-line `@ AGENTS.md` includes when needed, and an existing upstream workspace keeps its native `CLAUDE.md` entry path;",
    "1. five-layer routing with the current native ICM Layer-0 entry semantics preserved; when portable `AGENTS.md` guidance is added, it interoperates with rather than replaces or overrides the native `CLAUDE.md` entry path;",
)
text = text.replace(
    "See `docs/standards.md` for the tracked compatibility surface and update procedure.",
    "Repository maintainers should track the current primary upstream compatibility surfaces and update this skill-local specification, compatibility reference, affected modes, templates, examples, and regression checks together. The installed skill must not depend on repository-only documentation to execute correctly.",
)
text = text.replace(
    "Normative. Skills and examples in this repository must conform to this document.",
    "Normative. CCA runtime behavior and CCA-conformant examples must conform to this document.",
)
SPEC.write_text(text, encoding="utf-8")

# Removed package IDs must not survive inside the installed runtime corpus.
replacements = {
    "`cca-advisor`": "`advise` mode",
    "`cca-architect`": "`architect` mode",
    "`cca-scaffold`": "`scaffold` mode",
    "`cca-sync`": "`sync` mode",
    "`cca-ingest`": "`ingest` mode",
    "`cca-query`": "`query` mode",
    "`cca-lint`": "`lint` mode",
    "cca-advisor": "advise mode",
    "cca-architect": "architect mode",
    "cca-scaffold": "scaffold mode",
    "cca-sync": "sync mode",
    "cca-ingest": "ingest mode",
    "cca-query": "query mode",
    "cca-lint": "lint mode",
}
for path in CCA.rglob("*.md"):
    data = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        data = data.replace(old, new)
    path.write_text(data, encoding="utf-8")

# Add a permanent validator for semantic/path drift inside all installed files.
validator = ROOT / ".github/scripts/validate_repo.py"
v = validator.read_text(encoding="utf-8")
if "def validate_skill_self_containment()" not in v:
    marker = "\ndef validate_icm_derived_example() -> None:\n"
    fn = r'''
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

'''
    v = v.replace(marker, "\n" + fn + "def validate_icm_derived_example() -> None:\n")
    v = v.replace(
        "    validate_skills()\n    validate_icm_derived_example()",
        "    validate_skills()\n    validate_skill_self_containment()\n    validate_icm_derived_example()",
    )
validator.write_text(v, encoding="utf-8")

print("Runtime self-containment aligned")
