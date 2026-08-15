# Workspace Builder Parity and Granular Evaluation Design

## Goal

Make `cca` Architect capable of performing the complete applicable native ICM workspace-builder behavior from an installed CCA skill, while preserving upstream ICM as the semantic authority, then make the evaluation granular enough to distinguish model competence, inherited ICM value, and CCA-specific improvement.

## Architecture

`cca` remains one installable skill. `architect` gains a lazy `workspace-builder.md` reference used only for create/setup/status/full-workspace-generation requests. The builder is profile-driven: native ICM follows the current upstream ICM behavioral contract exactly where applicable; generic/hybrid CCA generation may reuse the orchestration pattern without relabeling non-ICM workspaces as native ICM.

The evaluator gains a no-skill control arm and two additional suites: an atomic ICM-parity suite and a CCA-extension suite. The atomic suite decomposes ICM behavior into individually testable contracts so a broad pass cannot hide a regression. The extension suite requires CCA-specific composition/knowledge/routing behavior rather than merely asking agents to preserve a foreign methodology.

## Native ICM builder contract inside CCA Architect

For native ICM generation or material rebuild, Architect must be able to perform:

1. discovery of the workflow, stages, inputs, outputs, references, shared context, variables, optional stages, tools, and skills;
2. mapping into exact stage contracts, canonical sources, output consumption, and a one-way dependency graph;
3. scaffolding of the native workspace with Layer 0-4 routing, stage folders, output handoffs, references, `.gitkeep`, applicable value/shared-constant patterns, tool guides, and bundled skills;
4. questionnaire design with flat all-at-once questions, system/per-run separation, defaults, derive-don't-ask behavior, conditional sections, and complete placeholder coverage;
5. validation and repair of cross-references, cycles, placeholders, conditionals, handoffs, routing purity, checkpoints, audits, spec purity, size/naming rules, tool prerequisites, and native quality rules;
6. `setup` execution: collect answers conversationally, hydrate the workspace, resolve/remove conditionals, verify zero orphan placeholders, and avoid repeated onboarding after successful setup;
7. `status` execution: scan stage output folders and render COMPLETE/PENDING state using native semantics;
8. fresh-agent walk verification after upstream/native acceptance passes.

CCA may add portable `AGENTS.md` guidance, broader profiles, method overlays, or other interoperability only when those additions do not weaken native ICM semantics.

## Evaluation model

Every applicable behavioral case can run three arms with identical model/runtime/budget/fixture:

- `A`: reference material / baseline repository skill;
- `B`: candidate CCA skill;
- `C`: no-skill control.

The control arm receives the task and fixture but no tested repository skill material. It measures how much of the result comes from the model itself.

Interpretation:

- A=B=C: benchmark likely measures generic model competence.
- A=B>C: both architectures contribute useful behavior; no candidate advantage proven.
- B>A>=C: candidate improvement on that capability.
- A>B>=C: candidate regression on inherited capability.

## Granularity

The ICM parity suite must cover atomic behavior rather than one broad native-pipeline case. Coverage includes Layer 0-4 routing, exact stage contracts, handoffs, one-way references, selective section routing, canonical sources, routing purity, prerequisites, setup/status, questionnaire rules, placeholder handling, conditional stages, skill bundling, specs, checkpoints, audits, value validation, docs-over-outputs, shared constants, naming/size/format guardrails, cold-agent walk, build/restructure behavior, factory/product separation, and complete workspace-builder flow.

The CCA extension suite must force semantics that generic preservation cannot satisfy: cross-authority routing, human-vs-agent knowledge authority, LLM Wiki ingest/query, profile-aware linting, nested native profiles, methodology scope/conflict/composition, progressive-disclosure non-trigger behavior, and hybrid lifecycle decisions.

## Success criterion

CCA may be called an ICM evolution/superset only when:

1. every applicable inherited ICM primitive is behaviorally parity or improvement, never regression;
2. compound ICM workflows are parity or better in outcome, with equal or lower overhead preferred;
3. CCA extensions demonstrate value above the no-skill and ICM arms in scenarios that actually require those extensions;
4. broader scope does not impose a context, structure, or intervention tax on ordinary/native ICM tasks.
