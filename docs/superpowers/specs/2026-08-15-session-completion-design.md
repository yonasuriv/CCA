# Session Completion Design

## Goal

Complete the CCA refactor so every architectural conclusion reached during the audit/re-evaluation session is represented by one of: normative runtime semantics, focused operation/form guidance, deterministic repository regression coverage, or an executable real-agent evaluation contract.

## Non-negotiable architecture

1. CCA remains **one installable `cca` Agent Skill** with seven lazy modes: `architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`, and `advise`.
2. The installed package is self-contained. Runtime behavior cannot depend on repository-only `docs/`, removed `spec/`, or removed sibling skill packages.
3. Architect and advisor remain separate reference domains. Architect may consult advisor lazily; it must not absorb, duplicate, or redefine advisor guidance.
4. CCA preserves external authorities instead of replacing them. ICM/MWP, LLM Wiki, AGENTS.md, Agent Skills, PARA, Zettelkasten, BASB/CODE, Scrum/Kanban/XP/DevOps and similar methods remain distinct authorities at their own boundaries.
5. A healthy existing repository may legitimately require no structural change. Structure must earn its maintenance/context cost.

## Corrections from the previous audit

The repository must encode the following conclusions explicitly enough that later agents cannot reintroduce the rejected remediation:

- **Layer 0:** native ICM keeps its native entry semantics. Portable `AGENTS.md` guidance may coexist/interoperate but does not universally override or replace native `CLAUDE.md` behavior. CCA-created/hardened non-native workspaces may prefer `AGENTS.md` as portable canonical guidance.
- **Stage contracts:** native/ICM-derived stage Inputs use the canonical four-column `Source | File/Location | Section/Scope | Why` shape. Do not loosen it because a separate selective-routing example uses three columns.
- **Em dashes:** the no-em-dash rule is scoped to native ICM artifacts where upstream requires it and CCA templates/examples that intentionally instantiate that profile. It is not a repository-wide CCA prose rule.
- **Size limits:** native ICM routing/reference limits are profile-scoped, not universal limits on CCA advisor/reference documents.
- **Questionnaires:** native ICM onboarding is flat, all-at-once and system-level. Hybrid/non-native examples are not to be linted as full native ICM merely because they borrow stages.
- **Human gates:** human-editable handoffs are universal to the relevant workflow; explicit checkpoints are required where the active profile/form calls for them, not after every stage universally.
- **Root `CONTEXT.md`:** required inside a native ICM profile; optional/recommended in generic CCA workspaces. No cross-profile contradiction.
- **Filesystem state:** physical file/folder existence does not imply semantic state unless the active profile explicitly defines that inference. Native ICM status semantics are preserved when active.
- **Indexes:** maintained semantic catalogs and generated indexes/file maps are different classes. Generated indexes are rebuilt; semantic catalogs may be intentionally maintained. Do not force one global `FILE-MAP` convention.
- **Validation:** CCA may validate more broadly than an upstream builder, but broader linting supplements rather than weakens the active upstream acceptance surface.
- **Mermaid:** preferred for CCA-owned conceptual diagrams; upstream-required representations win inside native profiles.

## Real capability gaps to close

### System Map

System Map remains a distinct form from Context Map. It covers mutable repositories/vaults/mixed trees and must support source-backed change-impact reasoning, including:

- live / leftover / ghost universes;
- source-of-truth citations;
- object/process/effect separation when scale justifies it;
- Hits / Does not hit boundaries;
- a change-impact index;
- staged inventory → catalog → nouns → verbs → impact → re-verification work;
- explicit human/cold-walk gates between expensive slices;
- a cold-agent walk that lands on source, not another essay;
- no empty decorative shelves and no duplication of the subject tree.

### Record Library

For a fresh same-shaped record library, the record template is the schema/default creation source. New records start from the template, identifier/status authority has one declared home when those fields exist, lifecycle is deliberately small, and half-created/schema-drifted records are detectable. Existing libraries keep their native schema.

### Context Map

Context Map remains an organization/process/information relationship map, not a source-code impact map. It may carry frequency plus ownership/value/pain/governance/interfaces where useful. Workshop observations are evidence events, not automatically canonical truth; repeated-pattern promotion needs an explicit evidence rule (three independent occurrences is a useful default, not a universal law).

### Native ICM setup

Full native generation must map questionnaire answers to concrete placeholders/files/conditional stages, derive inferable values, and verify both directions: every placeholder has an answer/source and every answer is used or intentionally discarded.

## Existing projects and human/process methods

CCA must distinguish method authority from filesystem structure:

- **Coding repository:** preserve application structure, build/test tooling and scoped instructions. Add only routing that earns its cost.
- **Scrum/Kanban/XP/DevOps/etc.:** process/delivery authority remains external to CCA. CCA may route backlog, ADR, release, source and operational artifacts without pretending the method is a folder schema.
- **PARA:** may organize the outer workspace by actionability while nested code/ICM/wiki boundaries retain native semantics.
- **Zettelkasten:** preserve addressable linked ideas and local write authority; do not silently convert human notes into agent-maintained synthesis.
- **BASB/CODE:** lifecycle lens, not structural compatibility profile.
- **LLM Wiki:** persistent maintained synthesis over durable source material; preserve implementation flexibility before CCA hardening.

## Evaluation architecture

Behavioral superiority is not a documentation claim. The repository will provide an executable harness contract with 14 scenario fixtures.

Each case contains:

- a case manifest;
- a task prompt;
- an initial filesystem fixture;
- deterministic case assertions;
- baseline material requirements.

The runner prepares isolated copies for Arm A and Arm B and delegates actual model execution to caller-supplied commands. Arm A receives only the case's baseline/upstream material; Arm B receives only the installable `skills/cca/` package. Same model/config/tool/network/context/tool-call budgets are required externally.

The harness records actual filesystem changes/no-change decisions, command metadata, deterministic assertion results and basic cost proxies available to the runner. It must never create a simulated agent plan and call that behavioral evidence.

Cases:

1. native ICM pipeline;
2. ICM-derived pipeline;
3. existing healthy code repository;
4. code repository + Scrum process authority;
5. PARA second brain;
6. PARA + Zettelkasten;
7. LLM Wiki;
8. LLM Wiki + ICM workflow;
9. Record Library;
10. Context Map;
11. System Map;
12. hybrid nested authorities;
13. explicit existing-workspace restructure;
14. no-op/already healthy workspace.

Native compatibility failures are graded before qualitative preference. For mixed/existing-workspace cases, useful CCA gains include fewer unnecessary mutations, preserved authorities, lower exploration/context cost, and better cold-agent success.

## Testing strategy

Repository CI remains standard-library-only. New behavior is developed test-first:

- unit tests validate case discovery, manifest integrity, isolated preparation, assertion loading and result writing;
- fixture tests ensure all 14 cases exist and carry required artifacts;
- semantic regression tests scan the installed skill for rejected Layer-0/package/path wording and enforce the current one-skill model;
- existing repository validation continues to enforce links, native ICM template/example invariants and self-containment.

The CI test suite proves harness/repository mechanics only. It does **not** claim the real model A/B runs have happened.

## Success criteria

The branch is ready when:

- one installable skill is the only first-party skill package;
- runtime references contain no removed standalone skill/package assumptions;
- the session corrections above are reflected consistently across core, architect, modes and templates;
- System Map, Record Library, Context Map and native ICM setup carry the missing operational semantics;
- 14 evaluation fixtures are present and mechanically valid;
- the evaluation runner can execute caller-supplied real-agent commands in isolated workspaces and grade deterministic outputs;
- normal CI passes on the final commit;
- documentation states clearly that real A/B results remain unproven until actual agent executions are supplied.