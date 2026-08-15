#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CCA = ROOT / "skills/cca"


def replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"expected text not found in {path}: {old[:80]!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def replace_optional(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old in text:
        path.write_text(text.replace(old, new), encoding="utf-8")


forms = CCA / "references/architect/forms.md"
replace(
    forms,
    "When native ICM compatibility is requested, implement the complete applicable current ICM profile: `AGENTS.md` as the authoritative Layer-0 catalog, five-layer routing, root and stage contracts, `setup`/`status` behavior, flat all-at-once questionnaire, naming and placeholder rules, tool prerequisites where needed, applicable checkpoints/audits/spec/value/shared-constant patterns, quality guardrails, and workspace-builder-equivalent validation. Create a harness entry (`CLAUDE.md`) as a single-line `@AGENTS.md` include only when a harness needs it. When operating on an existing upstream workspace, preserve its native `CLAUDE.md` entry path.",
    "When native ICM compatibility is requested, implement the complete applicable current ICM profile: preserve the current native Layer-0 entry semantics, five-layer routing, root and stage contracts, `setup`/`status` behavior, flat all-at-once questionnaire, naming and placeholder rules, tool prerequisites where needed, applicable checkpoints/audits/spec/value/shared-constant patterns, quality guardrails, and workspace-builder-equivalent validation. Portable `AGENTS.md` guidance may be added as an interoperable counterpart when useful, but it must not be described as universally overriding or replacing the native ICM `CLAUDE.md` entry. For new full-native generation, also read `native-icm-setup.md` and map onboarding answers to concrete files/placeholders/conditional stages before claiming setup completeness.",
)
forms.write_text(forms.read_text(encoding="utf-8").replace(
    "## Record Library defaults\n\nFor a fresh Record Library, treat the record template as the schema: create new\nrecords by copying it rather than starting blank. Keep identifier/status\nauthority in one declared catalog when the library uses those fields, define a\nsmall lifecycle only when needed, and detect half-created records or schema drift.\nExisting libraries keep their own schema and lifecycle.",
    "## Record Library defaults\n\nFor a fresh Record Library, treat the record template as the schema and creation source: every new record starts by copying the template, then replacing declared fields; never create a blank record and reconstruct the shape from memory. If identifiers or lifecycle status exist, declare one catalog as their authority and make record-local copies derived/readable rather than competing authorities. Keep lifecycle deliberately small (for example `draft → active → archived`) unless the domain already defines one. A record is half-created when its catalog entry exists without the required template-derived body, or the body exists without the required catalog identity; lint/sync should report that state rather than silently guessing. Detect schema drift by comparing required template fields/sections against records, while preserving an existing library's own schema and lifecycle instead of imposing these defaults."
).replace(
    "## Context Map operational fields\n\nWhen useful for the actual mapping question, nodes may include `frequency` in\naddition to ownership, value, pain, governance, inputs, outputs, and interfaces.\nWorkshop observations are evidence, not automatically canonical truth. Promote a\npattern only when the workspace's evidence rule is satisfied; three independent\noccurrences is a useful default, not a universal law.",
    "## Context Map operational fields\n\nContext Map models organizational/process/information relationships, not source-code change impact. When useful for the actual mapping question, nodes may include `frequency` in addition to ownership, value, pain, governance, inputs, outputs, and interfaces. Keep evidence links/observation references close to claims that came from workshops or discovery. Workshop observations are evidence events, not automatically canonical truth. Promote a repeated pattern only when the workspace's evidence rule is satisfied; three independent occurrences is a useful default when no stronger local rule exists, never a universal law. If the question becomes 'what source file changes and what does that hit?', switch to System Map instead of stretching Context Map into a code graph."
), encoding="utf-8")

methods = CCA / "references/architect/methods.md"
replace(
    methods,
    "│       │   ├── CLAUDE.md            # created by directive: '@AGENTS.md' (or native entry preserved)\n│       │   ├── AGENTS.md            # authoritative Layer-0 catalog",
    "│       │   ├── CLAUDE.md            # native ICM entry semantics preserved\n│       │   ├── AGENTS.md            # optional portable counterpart when useful",
)
replace(methods, "The semantic skill name is the coordination boundary.", "The semantic mode name is the coordination boundary.")
replace(methods, "Direct requests still route directly to the focused skill.", "Direct requests still route directly to the focused mode.")

mode = CCA / "references/architect/mode.md"
replace(
    mode,
    "Harness-specific entry files such as `CLAUDE.md` are not shipped as templates; create them by directive as a single-line `@AGENTS.md` include only when a harness needs its own entry path.",
    "Harness-specific entry files such as `CLAUDE.md` are not shipped as generic templates. Preserve the active native/profile entry semantics first; add a harness bridge to shared portable guidance only when the harness currently supports that mechanism and the target profile permits it.",
)
replace(
    mode,
    "- **Native ICM**: preserve the complete applicable current ICM profile, not only its stage folder shape. This includes `AGENTS.md` as the authoritative Layer-0 catalog (with a single-line `@AGENTS.md` `CLAUDE.md` include when a harness path is needed; an existing upstream workspace keeps its native `CLAUDE.md`), five-layer routing, root/stage `CONTEXT.md`, exact stage contracts, setup/status behavior, questionnaire rules, naming, handoffs, selective loading, one-way references, canonical sources, applicable checkpoints/audits/spec/value/shared-constant rules, quality guardrails, and workspace-builder-equivalent validation. See `references/core.md`.",
    "- **Native ICM**: preserve the complete applicable current ICM profile, not only its stage folder shape. Preserve the current native Layer-0 `CLAUDE.md` semantics, five-layer routing, root/stage `CONTEXT.md`, exact stage contracts, setup/status behavior, questionnaire rules, naming, handoffs, selective loading, one-way references, canonical sources, applicable checkpoints/audits/spec/value/shared-constant rules, quality guardrails, and workspace-builder-equivalent validation. Portable `AGENTS.md` guidance may interoperate where useful but is not declared to override native entry semantics. Read `core.md`; for new full-native generation also read `native-icm-setup.md`.",
)
replace(mode, "load `references/methods.md`", "load `methods.md`")
replace(mode, "implement the complete applicable ICM profile from `references/core.md`, create `AGENTS.md` as the authoritative Layer-0 catalog, and validate against the current upstream convention/validation surface before claiming compatibility. Create a harness entry (`CLAUDE.md`, `GEMINI.md`, ...) as a single-line `@AGENTS.md` include only when a harness requires it. If the workspace already has a native `CLAUDE.md`, do not overwrite it; derive the portable `AGENTS.md` counterpart from it instead, keeping one substantive source of truth.", "implement the complete applicable ICM profile from `core.md` plus `native-icm-setup.md`, preserve the native Layer-0 entry semantics, and validate against the current upstream convention/validation surface before claiming compatibility. Add portable `AGENTS.md` guidance only as an interoperable counterpart when it improves cross-agent use and does not invalidate the native profile. If the workspace already has a native `CLAUDE.md`, do not overwrite it merely to satisfy a CCA preference.")
replace(mode, "reading `references/adapters.md`", "reading `../core/adapters.md`")

compat = CCA / "references/core/compatibility.md"
replace(
    compat,
    "CCA's first-party skills are intentionally distributed as a **suite of focused capabilities**. Package portability does not mean every skill must be a sensible unrelated product when installed alone. It means installation paths and sibling filesystem layouts are not part of the capability contract.\n\nCross-skill coordination is therefore allowed by **semantic skill name**, for example `Use lint mode to validate the selected profile`. A skill must not reach into `../lint mode/`, `../../spec/`, or another sibling/repository-global implementation path to perform that delegation.",
    "CCA is distributed as **one installable `cca` skill with seven lazily loaded modes**. Package portability means every runtime reference, template, and script required by those modes remains inside that one package and installation location is not part of the capability contract.\n\nCross-mode coordination uses semantic mode names, for example `Use lint mode to validate the selected profile`; it never relies on removed sibling skill packages or repository-global implementation paths.",
)
replace_optional(compat, "See `docs/standards.md` for the tracked upstream surface.", "Repository maintainers should verify the current primary upstream surfaces before changing compatibility semantics and update the skill-local compatibility/specification references together.")

composition = CCA / "references/core/method-composition.md"
start = composition.read_text(encoding="utf-8")
old = """## 5. CCA skill suite

CCA's first-party Agent Skills are a **suite of focused capabilities**, not unrelated standalone products.

Package portability means:

1. each skill's implementation resources referenced by file path are contained within that skill package;
2. no skill reaches into a sibling skill directory or repository-global implementation file by relative path;
3. installation location must not become part of CCA semantics;
4. a skill may coordinate with another installed CCA capability by semantic skill name, for example `Use lint mode to validate the selected profile`;
5. semantic delegation must not be rewritten as a brittle filesystem dependency.

The intended first-party suite is:

- `architect` mode
- `scaffold` mode
- `sync` mode
- `ingest` mode
- `query` mode
- `lint` mode

`architect` mode is the primary entry point for compound architecture/design requests and may lazy-load method/form references before delegating focused operations. It is not a mandatory gateway for an operation whose intent already matches another skill directly.

## 6. Progressive disclosure

CCA should use Agent Skills progressive disclosure rather than creating a single monolithic skill.

- skill metadata routes to the appropriate focused capability;
- `SKILL.md` contains the compact operational procedure;
- detailed method/profile knowledge remains in skill-local references and is loaded only when relevant;
- compound architecture work may coordinate multiple skills semantically.

Creating a dedicated `cca-para`, `cca-zettelkasten`, or `cca-second-brain` skill is not justified merely to store methodology knowledge. Such knowledge belongs behind the architecture capability unless a future distinct executable operation warrants its own skill.
"""
new = """## 5. CCA skill package and modes

CCA is **one installable Agent Skill** named `cca`. It exposes seven lazy modes: six workspace operations (`architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`) plus the separate `advise` judgment capability.

Package portability means:

1. every runtime resource referenced by path remains inside `skills/cca/` after installation;
2. no mode depends on removed sibling skill packages or repository-global implementation files;
3. installation location is not part of CCA semantics;
4. modes coordinate by semantic mode name, not filesystem package boundaries;
5. architect and advisor remain separate reference domains even though they share one package.

`architect` mode is the primary entry point for compound architecture/design requests and may lazy-load form/method references or consult the advisor domain for judgment. It is not a mandatory gateway for an operation whose intent already matches another mode directly.

## 6. Progressive disclosure

CCA uses Agent Skills progressive disclosure *inside the single package* rather than splitting tightly coupled operations into separately installable skills or loading all references at activation time.

- `SKILL.md` routes intent to one mode;
- a mode loads only the core/form/method/advisor references required by the task;
- detailed methodology knowledge stays behind architect references;
- advisor references stay behind `advise` or explicit architect consultation;
- focused operations do not need to load unrelated architecture or advisor material.

Creating dedicated PARA, Zettelkasten, BASB, Scrum, or similar CCA skills is not justified merely to store methodology knowledge. Those external methods remain authorities and are loaded only when the active problem crosses their boundary.
"""
if old not in start:
    raise SystemExit("method composition package section drifted")
composition.write_text(start.replace(old, new), encoding="utf-8")

system_map = CCA / "references/architect/system-map.md"
system_map.write_text("""# System Map form

Use a System Map when the subject is a mutable repository, vault, or mixed tree and the user needs reliable **change-impact reasoning** rather than only an organizational/process graph.

A System Map is distinct from a Context Map:

- **Context Map**: people, teams, workflows, systems, ownership, information movement.
- **System Map**: concrete mutable objects, processes, effects, source-backed change impact.

Do not create either form when ordinary code navigation, search, or existing architecture documentation already answers the question cheaply.

## Smallest justified shape

Start with inventory and a proposed map. Create shelves only when verified material needs them:

```text
map/
├── CONTEXT.md
├── schema.md
├── templates/
├── objects/
├── processes/          # only when verified recurring movements exist
└── effects/
    └── CONTEXT.md      # only when a useful impact index exists
```

The subject tree remains source of truth. Cards cite it; they do not copy it into a second specification.

## Universes

Classify evidence-backed material when the distinction is useful:

- **live**: currently wired/in force;
- **leftover**: still present but no longer the primary path;
- **ghost**: named, documented, or stubbed but not actually wired/implemented.

Do not promote aspiration or a stale document to live merely because it has a confident name.

## Human/cold-walk slices

System-map construction can be expensive. Work in slices and stop for human review **or a cold-agent verification gate** before the next expensive slice:

0. **Inventory**: inspect the real tree, infer candidate nouns/verbs, classify universes, propose the smallest useful map; do not write speculative cards.
1. **Catalog**: establish `CONTEXT.md`, schema/templates and a route from the subject's existing orientation surface when needed.
2. **Objects**: create source-cited noun cards. Mark verified only when citations/revision evidence support the claim.
3. **Processes**: add only recurring movements that can be evidenced. State input → movement → output and link affected objects.
4. **Effects**: create the change-impact index. `Hits` and `Does not hit` should capture first-order boundaries, not invented waterfalls.
5. **Re-verify**: re-open source for load-bearing claims, especially impact boundaries, after the initial fill or material subject changes.

A person does not have to approve every trivial file; the gate exists before costly/speculative expansion. Linear verification may continue when evidence is deterministic.

## Card requirements

A useful object/process card identifies:

- what the thing is, including product/file/type names when they differ;
- why its shape matters;
- source-of-truth path(s) and revision/verification context when available;
- connected objects/processes;
- **Hits** and **Does not hit** for useful first-order change boundaries;
- who/what reads or writes it;
- inference versus observed fact.

Do not mark a card verified without source evidence. Do not cite another explanatory card as the final source when the real code/file is available.

## Cold-agent walk

A fresh agent with no chat memory should be able to:

1. reach the map from the subject's normal entry/orientation surface;
2. distinguish live, leftover, and ghost names that matter;
3. open one card and land on the real source it cites;
4. answer one stated change-impact question from `effects/CONTEXT.md` plus the minimum relevant cards;
5. state both what the change hits and an obvious nearby thing it does **not** hit;
6. identify which claims are inferred or stale and need re-verification.

If the agent must load the whole map or the map merely duplicates source files, split/shrink it rather than adding a longer reading guide.

## Failure modes

- collapsing Context Map and System Map into one vague graph;
- generating empty `processes/`/`effects/` shelves for symmetry;
- copying source behavior into cards instead of citing source;
- treating ghost/leftover material as live;
- verified labels without evidence;
- unlimited transitive impact claims;
- a map that becomes more expensive to maintain than direct navigation.
""", encoding="utf-8")

native_setup = CCA / "references/architect/native-icm-setup.md"
native_setup.write_text("""# Native ICM setup mapping

Read this only when creating or materially rebuilding a **full native ICM workspace**. Generic CCA scaffolding and ICM-derived stage use do not require this procedure.

Native onboarding is flat, all-at-once, system-level and one-time. The questionnaire is not complete merely because questions were asked: answers must be mapped into the factory/configuration/stage structure they configure.

## Mapping table

Before writing the workspace, derive a setup map with one row per effective answer:

| Answer / derived value | Source question or derivation | Canonical destination | Placeholder / field | Conditional effect |
|---|---|---|---|---|
| workspace name | Q1 | declared workspace config/reference | explicit placeholder/field | none |
| output/reviewer needs | Q1/Q2 | relevant stable reference | explicit placeholder/field | may affect stage/checkpoint configuration |
| style examples/rules | Q3/Q5 | canonical style/quality reference | declared fields | only when style is relevant |
| hard constraints | Q4 | canonical policy/reference | declared fields | may disable actions/stages |
| knowledge entities/sources | Q6 | knowledge/reference schema | declared fields | only for maintained-knowledge use |
| representative run/artifacts | Q7 | root/stage routing/contracts | stage/output declarations | determines applicable stages |
| deterministic tooling | Q8/Q9 | tool/setup reference | tool fields | only required tools become prerequisites |
| harnesses | Q10 | adapter decision | no frozen filename placeholder | only verified needed adapters |
| defaults | Q11 + derived values | relevant canonical references | declared defaults | no duplicate question |

The concrete file names come from the selected current native ICM form/workspace; do not invent a second CCA configuration schema merely to host the map.

## Bidirectional coverage gate

Before setup is complete verify both directions:

1. **Question/answer → use:** every non-discarded answer changes or confirms at least one declared canonical destination, placeholder, field, stage decision, or default. If an answer has no consumer, remove the question or document why it is intentionally informational.
2. **Placeholder/field → source:** every setup placeholder/configurable field has exactly one answer, derived value, or explicit default source. No orphaned placeholder remains.
3. **Conditional stage → condition:** every optional stage/tool/block has an explicit condition derived from answers or observable environment; do not create optional stages unconditionally and hide them later.
4. **Derivation → no re-ask:** values inferable from earlier answers or the filesystem are derived, not asked again.
5. **One-time behavior:** after successful setup, later runs use the configured files and do not repeat onboarding unless the user explicitly resets/reconfigures it.

## Acceptance

Do not call the native workspace setup-complete until the current upstream questionnaire/placeholder/conditional syntax rules pass together with workspace-builder-equivalent end-to-end validation. This mapping procedure supplements current upstream acceptance; it does not replace it.
""", encoding="utf-8")

evals = ROOT / "evals/README.md"
eval_text = evals.read_text(encoding="utf-8")
if "## Runner usage" not in eval_text:
    eval_text += """

## Runner usage

The repository ships `evals/runner.py`; it prepares and grades runs but does not choose or impersonate an agent.

```bash
# Arm B: CCA-only material. Everything after --command is the real agent command.
python evals/runner.py \\
  --case 03 \\
  --arm B \\
  --runs /tmp/cca-evals \\
  --cca-skill skills/cca \\
  --command <agent-command> <agent-args>

# Arm A: upstream baseline material must be supplied for cases that require it.
python evals/runner.py \\
  --case 01 \\
  --arm A \\
  --runs /tmp/cca-evals \\
  --baseline-root /path/to/pinned/icm-material \\
  --command <same-agent-command> <same-agent-args>
```

The invoked command runs with its working directory set to the isolated `workspace/`. It receives `CCA_EVAL_CASE`, `CCA_EVAL_ARM`, `CCA_EVAL_PROMPT`, and `CCA_EVAL_MATERIAL` environment variables. The caller is responsible for giving both arms the same model/configuration, tool permissions, network policy, context/token budget, tool-call budget, and time/step budget.

Each prepared run writes `result.json` containing command/exit/duration metadata (when a command was actually run) and deterministic filesystem assertion results. `behavioral_run_executed: false` means the runner only prepared/graded a workspace; such output is **not** behavioral evidence.

The 14 fixtures and harness are implemented. Real model A/B results are still unproven until actual external agent commands execute both arms under matched conditions and their artifacts are retained. Report results per scenario; never turn fixture existence or CI success into a universal “CCA is better than ICM” claim.
"""
    evals.write_text(eval_text, encoding="utf-8")

cases_readme = ROOT / "evals/cases/README.md"
case_text = cases_readme.read_text(encoding="utf-8")
if "## Implemented cases" not in case_text:
    case_text += """

## Implemented cases

Directories `01-` through `14-` are executable fixture contracts, not recorded model outcomes. Each contains `case.json`, `prompt.md`, `fixture/`, and `assertions.json`. Assertions intentionally target semantic invariants and preservation boundaries rather than byte-for-byte reproduction of a pre-existing upstream golden workspace.
"""
    cases_readme.write_text(case_text, encoding="utf-8")

validator = ROOT / ".github/scripts/validate_repo.py"
v = validator.read_text(encoding="utf-8")
v = v.replace(
    '        CCA / "references/architect/system-map.md",',
    '        CCA / "references/architect/system-map.md",\n        CCA / "references/architect/native-icm-setup.md",',
)
if "def validate_session_semantics()" not in v:
    insertion = r'''
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
        CCA / "references/architect/forms.md": ["Record Library defaults", "half-created", "frequency", "System Map"],
        CCA / "references/architect/native-icm-setup.md": ["Bidirectional coverage gate", "Question/answer → use", "Placeholder/field → source", "Conditional stage → condition"],
        CCA / "references/advisor/mode.md": ["These are seven references, not six."],
    }
    for path, fragments in required_fragments.items():
        text = read(path)
        for fragment in fragments:
            if fragment not in text:
                error(f"Missing session-required semantic in {path.relative_to(ROOT)}: {fragment!r}")


def validate_evaluation_cases() -> None:
    cases = ROOT / "evals/cases"
    dirs = sorted(path for path in cases.iterdir() if path.is_dir() and re.match(r"^\d{2}-", path.name)) if cases.is_dir() else []
    expected = [f"{i:02d}" for i in range(1, 15)]
    found = [path.name[:2] for path in dirs]
    if found != expected:
        error(f"Expected evaluation cases 01..14; found {found}")
        return
    for path in dirs:
        for required in ("case.json", "prompt.md", "assertions.json"):
            if not (path / required).is_file():
                error(f"Evaluation case missing {required}: {path.relative_to(ROOT)}")
        fixture = path / "fixture"
        if not fixture.is_dir() or not any(p.is_file() for p in fixture.rglob("*")):
            error(f"Evaluation case missing non-empty fixture: {path.relative_to(ROOT)}")

'''
    v = v.replace("\ndef validate_icm_derived_example() -> None:\n", "\n" + insertion + "def validate_icm_derived_example() -> None:\n")
    v = v.replace(
        "    validate_skill_self_containment()\n    validate_icm_derived_example()",
        "    validate_skill_self_containment()\n    validate_session_semantics()\n    validate_evaluation_cases()\n    validate_icm_derived_example()",
    )
validator.write_text(v, encoding="utf-8")

print("session semantics finalized")
