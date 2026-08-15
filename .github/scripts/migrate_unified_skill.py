#!/usr/bin/env python3
"""One-shot migration for refactor/unified-cca-skill.

Preserves existing reference text by copying it inside the checkout, then changes
only package boundaries, mode routing, known stale paths, and the explicitly
approved CCA architecture corrections.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
CCA = SKILLS / "cca"
REFS = CCA / "references"


def ensure(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dst: Path) -> None:
    ensure(dst.parent)
    shutil.copy2(src, dst)


def strip_skill(path: Path, title: str) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        _, _, text = text.partition("\n---\n")
    text = re.sub(r"^\n*# [^\n]+\n+", f"# {title}\n\n", text, count=1)
    return text


def replace(path: Path, pairs: list[tuple[str, str]]) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


# 1. Preserve all existing runtime material inside the single installable skill.
for name in [
    "engineering-principles.md",
    "frameworks-and-methodologies.md",
    "security-and-adversarial-thinking.md",
    "agent-system-design.md",
    "context-engineering.md",
    "ai-ml-practice.md",
    "escalation-triggers.md",
]:
    copy_file(SKILLS / "cca-advisor" / "references" / name, REFS / "advisor" / name)

for name in ["core.md", "forms.md", "methods.md", "adapters.md"]:
    copy_file(SKILLS / "cca-architect" / "references" / name, REFS / "architect" / name)

for src in (SKILLS / "cca-architect" / "assets" / "templates").glob("*"):
    if src.is_file():
        copy_file(src, CCA / "assets" / "templates" / src.name)

# Repository-level normative material becomes skill-local runtime authority.
core = REFS / "core"
ensure(core)
copy_file(ROOT / "spec" / "SPEC.md", core / "spec.md")
copy_file(ROOT / "spec" / "compatibility.md", core / "compatibility.md")
copy_file(ROOT / "spec" / "method-composition.md", core / "method-composition.md")
copy_file(ROOT / "spec" / "adapters.md", core / "adapters.md")

# Mode procedures are lazy-loaded internal procedures, not sibling skills.
ensure(REFS / "operations")
(REFS / "architect" / "mode.md").write_text(
    strip_skill(SKILLS / "cca-architect" / "SKILL.md", "Architect mode"), encoding="utf-8"
)
for old, new in [
    ("cca-scaffold", "scaffold"),
    ("cca-sync", "sync"),
    ("cca-ingest", "ingest"),
    ("cca-query", "query"),
    ("cca-lint", "lint"),
]:
    src = SKILLS / old / "SKILL.md"
    (REFS / "operations" / f"{new}.md").write_text(
        strip_skill(src, f"{new.capitalize()} mode"), encoding="utf-8"
    )

# 2. Convert cross-skill delegation language to internal mode routing.
mode_pairs = [
    ("`cca-architect`", "`cca` in `architect` mode"),
    ("`cca-scaffold`", "`cca` in `scaffold` mode"),
    ("`cca-sync`", "`cca` in `sync` mode"),
    ("`cca-ingest`", "`cca` in `ingest` mode"),
    ("`cca-query`", "`cca` in `query` mode"),
    ("`cca-lint`", "`cca` in `lint` mode"),
    ("`cca-advisor`", "`cca` in `advise` mode"),
    ("Use cca-scaffold", "Use `scaffold` mode"),
    ("Use cca-sync", "Use `sync` mode"),
    ("Use cca-ingest", "Use `ingest` mode"),
    ("Use cca-query", "Use `query` mode"),
    ("Use cca-lint", "Use `lint` mode"),
]
for path in list((REFS / "architect").glob("*.md")) + list((REFS / "operations").glob("*.md")):
    replace(path, mode_pairs)

# Architect and advisor remain separate domains.
architect_mode = REFS / "architect" / "mode.md"
text = architect_mode.read_text(encoding="utf-8")
text = text.replace(
    "Read [references/core.md](references/core.md) before designing.",
    "Read `../core/spec.md` and `core.md` before designing."
)
text = text.replace(
    "Read [references/forms.md](references/forms.md) only when choosing a workspace form.",
    "Read `forms.md` only when choosing a workspace form."
)
text = text.replace(
    "Read [references/methods.md](references/methods.md)",
    "Read `methods.md`"
)
text = text.replace(
    "Read [references/adapters.md](references/adapters.md) only when a harness-specific adapter is needed.",
    "Read `../core/adapters.md` only when a harness-specific adapter is needed."
)
text += """

## Advisor consultation boundary

Architecture owns workspace structure; advisor owns engineering judgment. When a
structural choice depends on engineering/process trade-offs, lazily read only the
relevant file under `../advisor/` (for example `frameworks-and-methodologies.md`
for Scrum/Kanban/process questions). Do not copy advisor guidance into architect
references and do not turn a methodology into a CCA structural profile.
"""
architect_mode.write_text(text, encoding="utf-8")

# 3. Restore System Map as a distinct form and strengthen specialized forms.
system_map = REFS / "architect" / "system-map.md"
system_map.write_text("""# System Map form

Use a System Map when the subject is a mutable repository, vault, or mixed tree
and the user needs reliable change-impact reasoning rather than only an
organizational/process graph.

A System Map is distinct from a Context Map:

- **Context Map**: people, teams, workflows, systems, information movement.
- **System Map**: concrete mutable objects, processes, effects, and change impact.

## Minimal shape

```text
map/
├── CONTEXT.md
├── schema.md
├── templates/
├── objects/
├── processes/
└── effects/
```

Use the existing workspace paths as evidence; do not copy the whole repository
into the map. Object/process/effect cards must cite their source of truth.

## Required semantics

- classify discovered material as **live**, **leftover**, or **ghost** when that distinction can be evidenced;
- record `Hits` and `Does not hit` for impact boundaries where useful;
- maintain a change-impact index from mapped object/process relationships;
- distinguish observed fact from inference;
- re-verify affected cards after material changes;
- support a cold-agent walk: a fresh agent can identify what changes, what is affected, and which source files prove it.

Do not use System Map when ordinary code navigation, existing architecture docs,
or search already answer the question cheaply. The form must earn its maintenance cost.
""", encoding="utf-8")

forms = REFS / "architect" / "forms.md"
text = forms.read_text(encoding="utf-8")
if "## System Map" not in text:
    text += """

## System Map

Use for mutable code/file/vault systems where change-impact reasoning is the
primary problem. Read `system-map.md`. Do not collapse this into Context Map:
Context Map models organizational/process/data relationships; System Map models
concrete mutable objects, processes, effects, and impact.

## Record Library defaults

For a fresh Record Library, treat the record template as the schema: create new
records by copying it rather than starting blank. Keep identifier/status
authority in one declared catalog when the library uses those fields, define a
small lifecycle only when needed, and detect half-created records or schema drift.
Existing libraries keep their own schema and lifecycle.

## Context Map operational fields

When useful for the actual mapping question, nodes may include `frequency` in
addition to ownership, value, pain, governance, inputs, outputs, and interfaces.
Workshop observations are evidence, not automatically canonical truth. Promote a
pattern only when the workspace's evidence rule is satisfied; three independent
occurrences is a useful default, not a universal law.
"""
forms.write_text(text, encoding="utf-8")

# 4. Correct normative packaging and Layer-0 terminology.
spec = core / "spec.md"
text = spec.read_text(encoding="utf-8")
text = text.replace(
    "| 0 | `AGENTS.md` (authoritative Layer-0 catalog), created by directive when needed: `CLAUDE.md` = single-line `@ AGENTS.md` | Where am I? |",
    "| 0 | native harness entry plus portable guidance (`AGENTS.md` in CCA-hardened workspaces; native `CLAUDE.md` remains authoritative where ICM/harness semantics require it) | Where am I? |"
)
text = text.replace(
    "CCA's first-party skills are distributed as a **suite of focused capabilities**. Package portability means a skill does not depend on where sibling packages happen to be installed; it does not require each capability to be a useful unrelated standalone product.\n\nA skill may coordinate with another installed CCA capability by semantic skill name, for example `Use cca-lint to validate the selected profile`. This is semantic delegation, not a filesystem dependency.\n\n`cca-architect` is the primary coordinator for compound workspace-design requests and may lazy-load detailed method/form references before delegating focused operations. It is not a mandatory gateway for direct requests that already match another focused skill.",
    "CCA is distributed as **one installable `cca` skill with seven lazily loaded modes**. Six modes are portable workspace operations (`architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`); `advise` is a separate judgment capability inside the same package. Runtime references, templates, and scripts required by those modes must remain skill-local so installation is self-contained. Architect and advisor reference domains remain separate even though they share one package."
)
text = text.replace("CCA currently defines six portable operations:", "CCA defines six portable workspace operations plus one advisory mode:")
text = text.replace("| `lint` | validate the workspace using the correct compatibility/conformance profile |", "| `lint` | validate the workspace using the correct compatibility/conformance profile |\n| `advise` | apply engineering/process/security/autonomy/context/model judgment without turning priors into enforcement |")
text = text.replace("At minimum, `cca-lint` supports:", "At minimum, `lint` mode supports:")
spec.write_text(text, encoding="utf-8")

# 5. Known repository documentation drift and package-language migration.
doc_files = [
    ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CONTRIBUTING.md",
    ROOT / "docs" / "README.md", ROOT / "docs" / "faq.md",
    ROOT / "docs" / "getting-started.md", ROOT / "docs" / "method-composition.md",
    ROOT / "docs" / "migration.md", ROOT / "docs" / "references.md",
    ROOT / "docs" / "standards.md", ROOT / "docs" / "compatibility-details.md",
    ROOT / "examples" / "README.md",
]
for path in doc_files:
    replace(path, mode_pairs + [
        ("spec/SPEC.md", "skills/cca/references/core/spec.md"),
        ("spec/compatibility.md", "skills/cca/references/core/compatibility.md"),
        ("spec/method-composition.md", "skills/cca/references/core/method-composition.md"),
        ("spec/adapters.md", "skills/cca/references/core/adapters.md"),
        ("docs/principles.md", "docs/design-principles.md"),
        ("examples/articles/", "examples/publications/"),
        ("the six CCA capabilities", "the seven CCA modes"),
        ("the six CCA skills", "the single CCA skill and its seven modes"),
        ("seven CCA skills", "seven CCA modes"),
        ("seven skills", "seven modes"),
    ])

# Explicit package note in getting started/FAQ to prevent ambiguity.
getting = ROOT / "docs" / "getting-started.md"
with getting.open("a", encoding="utf-8") as fh:
    fh.write("""

## One skill, seven modes

Install `skills/cca/`. The package is self-contained: its normative CCA semantics,
compatibility rules, architect references, advisor corpus, operation procedures,
templates, and validation material live inside the skill. Modes are selected
lazily so a lint request does not load architecture or advisor material, and an
advice request does not load workspace templates.
""")

faq = ROOT / "docs" / "faq.md"
with faq.open("a", encoding="utf-8") as fh:
    fh.write("""

## Why one skill instead of seven packages?

The modes share one semantic authority and are commonly composed, while Agent
Skills already supports progressive disclosure through skill-local references,
assets, and scripts. One package prevents installation drift and keeps the
runtime specification available after installation. Internal domain boundaries
remain strict: architect references do not absorb the advisor corpus.

## What happens in an existing code repository?

CCA preserves the repository first. It may add or improve portable routing such
as `AGENTS.md`, but it does not introduce ICM stages, PARA folders, a wiki, or a
CCA manifest unless they solve an actual problem. Existing architecture docs,
tests, package metadata, issue trackers, and delivery tooling remain authoritative.

## What happens in a second brain?

CCA can preserve PARA as outer action-oriented organization, Zettelkasten as
linked idea development, BASB/CODE as a lifecycle lens, and an LLM Wiki as
maintained synthesis. Nested coding projects or native ICM workspaces keep their
own semantics. CCA maps boundaries and write authority; it does not merge the
methods into a new taxonomy.

## How does CCA combine with Scrum, Kanban, XP, DevOps, SAFe, LeSS, or DA?

Those methods govern process at their own scope. CCA does not create fake
`sprints/` or `standups/` folders to "implement Scrum". It records or routes to
the actual authority (for example Jira for backlog state, Git for code/history,
CI for delivery state) and may use ICM/CCA forms inside a particular workflow
only when useful. Process-method judgment comes from the advisor domain;
workspace structure remains an architect concern.
""")

# 6. Add scenario documentation that makes composition behavior testable.
scenarios = ROOT / "docs" / "scenarios.md"
scenarios.write_text("""# CCA scenarios

These scenarios are behavioral expectations, not mandatory directory templates.

## Existing code repository

**Default:** preserve `src/`, tests, docs, build configuration, issue/backlog tools,
and native harness instructions. Add only the smallest missing routing layer.
Do not ICM-ify a healthy application repository.

## Existing code repository using Scrum

Scrum remains process authority; the backlog remains in its real system of
record; Git remains code/history authority; CI/CD remains delivery authority.
CCA may route agents to those authorities and may use an ICM-derived workflow for
a bounded activity (for example a security review) without turning Scrum into a
filesystem schema.

## PARA second brain + Zettelkasten + LLM Wiki

PARA may organize Projects/Areas/Resources/Archives. Zettelkasten remains linked,
human-governed idea development. LLM Wiki remains maintained synthesis. A nested
project can contain an ordinary code repository or native ICM workspace. CCA
preserves each boundary and declares write/authority relationships instead of
flattening schemas.

## Native ICM

Preserve and validate the complete applicable upstream ICM profile. CCA's
portable AGENTS.md guidance may coexist with the harness-native entry, but must
not overwrite an existing native entry or weaken exact stage contracts.

## System Map

Use only when the user needs change-impact reasoning across a mutable repository,
vault, or mixed tree and existing navigation is insufficient. Map evidence and
impact; do not duplicate the system.

## Doing nothing is valid

If a fresh agent can already orient, act, and report with bounded context and the
workspace has clear authorities, CCA should recommend no structural change.
""", encoding="utf-8")

# 7. Fill the missing blog publication with extractable non-normative prose.
blog = ROOT / "examples" / "publications" / "blog.md"
blog.write_text("""# Convergent Context Architecture: making human and agent work interoperable

AI agents are getting better at acting on files, code, tools, and knowledge, but
the hard part is increasingly not the model. It is context: where instructions
live, what is authoritative, what an agent is allowed to change, and how several
methods or tools coexist without duplicating the same truth.

CCA (Convergent Context Architecture) is an agent-agnostic interoperability layer
for that problem. It does not replace ICM, LLM Wiki, AGENTS.md, Agent Skills,
PARA, Zettelkasten, BASB, Scrum, Kanban, or other established methods. It keeps
them distinct and makes their boundaries explicit enough for humans and agents
to navigate them together.

The rule is simple: **convergence over invention**. Preserve an existing authority
when it already solves the problem. Add the smallest missing routing layer. Do
not turn every repository into a pipeline, every second brain into a wiki, or
every team process into a folder taxonomy.

In an existing code repository, the best CCA result may be one compact
`AGENTS.md` and no restructuring at all. In a second brain, PARA can remain the
outer organization, Zettelkasten the idea network, BASB/CODE the lifecycle lens,
and an LLM Wiki the maintained synthesis layer. In a native ICM workspace, CCA
preserves the complete ICM profile instead of approximating it.

CCA is packaged as one Agent Skill with seven lazy modes: architect, scaffold,
sync, ingest, query, lint, and advise. The advisor corpus remains separate from
workspace architecture internally, so engineering and methodology judgment can
inform a structural decision without becoming the structure itself.

Automation is useful, but it is not the objective. The objective is to augment
human capability while keeping knowledge, authority, and decisions inspectable.
""", encoding="utf-8")

# 8. Remove obsolete installable package/spec boundaries only after copies exist.
for old in [
    "cca-advisor", "cca-architect", "cca-scaffold", "cca-sync",
    "cca-ingest", "cca-query", "cca-lint",
]:
    shutil.rmtree(SKILLS / old)
shutil.rmtree(ROOT / "spec")

print("Unified CCA skill migration applied")
