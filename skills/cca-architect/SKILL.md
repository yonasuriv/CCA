---
name: cca-architect
description: Design a filesystem-native CCA workspace or restructure an existing folder, repo, ICM workspace, or LLM Wiki without breaking native compatibility. Use when the user wants to build an agent workspace, structure a process for agents, create a persistent knowledge workspace, combine an ICM pipeline with maintained knowledge, or migrate/restructure existing context. Preserves upstream ICM and LLM Wiki semantics, uses AGENTS.md where portable guidance helps, and requires an approved migration map before destructive restructuring.
compatibility: Filesystem read/write access. No vendor-specific runtime required.
---

# CCA Architect

Design the smallest filesystem structure that makes the work navigable, durable, and agent-agnostic.

Read [references/core.md](references/core.md) before designing. Read [references/forms.md](references/forms.md) only when choosing a workspace form. Read [references/adapters.md](references/adapters.md) only when a harness-specific adapter is needed. Templates live under `assets/templates/`.

## Compatibility gate

Before changing structure, identify the current profile:

- **Native ICM**: preserve the complete applicable current ICM profile, not only its stage folder shape. This includes native `CLAUDE.md`, five-layer routing, root/stage `CONTEXT.md`, exact stage contracts, setup/status behavior, questionnaire rules, naming, handoffs, selective loading, one-way references, canonical sources, applicable checkpoints/audits/spec/value/shared-constant rules, quality guardrails, and workspace-builder-equivalent validation. See `references/core.md`.
- **ICM-derived**: another project may borrow numbered stage contracts or output handoffs without claiming to be a full native ICM workspace. Keep that distinction explicit.
- **Native LLM Wiki**: discover the implementation's own schema and maintenance conventions first. Do not force CCA frontmatter, page taxonomy, log syntax, or directory names onto it.
- **Ordinary project**: preserve the existing project layout unless the user explicitly wants restructuring.
- **CCA-conformant**: preserve the CCA specification the workspace intentionally adopted.

Compatibility is acceptance, not ownership. Do not label an upstream workspace CCA-conformant merely because CCA can read it, and do not label a partial ICM-derived scaffold as native ICM-compatible.

## Build mode

1. Extract the workflow and knowledge boundaries already implied by the request.
2. Choose the smallest useful form. Pipelines fit sequential handoffs; knowledge bundles fit persistent synthesis; hybrids are valid when a pipeline consumes or maintains knowledge.
3. Decide whether a pipeline needs the **full native ICM profile** or only **ICM-derived stage-contract patterns**. Do not silently upgrade one claim into the other.
4. If the intended result will be contributed to an upstream project, check that upstream repository's current contribution policy before scaffolding. Compatibility does not waive repository-specific contribution requirements. In particular, if the current ICM repository requires contributed workspaces to be created with its `workspace-builder`, follow that process rather than substituting CCA's generator.
5. Scaffold only the files the selected form/profile actually needs.
6. For a full native ICM workspace outside any stricter upstream contribution workflow, implement the complete applicable ICM profile from `references/core.md`, preserve native Layer 0 `CLAUDE.md`, and validate against the current upstream convention/validation surface before claiming compatibility.
7. For ICM-derived pipelines, use `stages/01-name/`, exact ICM contract columns, selective routing, one-way dependencies, and output handoffs, but describe the result as ICM-derived unless the rest of the native profile also passes.
8. Use `AGENTS.md` for portable guidance when it improves cross-agent routing. Preserve native instruction files required by the target harness/profile.
9. Add adapters only when needed and only after reading `references/adapters.md`.
10. Validate the selected native profile first, then run the CCA fresh-agent walk test.

## Restructure mode

1. **Audit** the actual folder and read enough content to classify confidently.
2. **Preserve native semantics** before proposing CCA hardening.
3. **Propose a migration map**: current path → function/profile → destination → action → compatibility impact.
4. **Stop for explicit approval** before moves, merges, renames, or deletions.
5. Apply only the approved map. Preserve content unless deletion was explicitly approved.
6. Validate native compatibility first, then any intentional CCA conformance.

## Invariants

- One fact, one canonical home.
- Routing files point; they do not become knowledge dumps.
- Load only context needed for the current operation.
- A stage has one job and one-way dependencies.
- Human-editable files are valid handoff surfaces.
- Never invent a competing convention where an upstream standard already solves the problem.
- Never require a sibling skill or repository-global file for core execution.
- Never claim a harness precedence rule you have not verified.
- Never substitute the CCA walk test for an upstream profile's stricter acceptance criteria.
- Never use compatibility as a reason to bypass an upstream repository's contribution process.
- Prefer CCA's own presentation conventions only where they do not override an upstream-required representation.

## Walk test

The walk test is a CCA portability check **after** applicable native-profile validation, not a replacement for it.

Simulate a fresh agent with no chat memory:

1. **Orient**: identify the workspace, active profile/form, and where relevant context lives.
2. **Act**: perform one representative operation using only routed files and available tools.
3. **Report**: state what changed, what was produced, what remains, and what is ambiguous or broken.

If required knowledge exists only in chat history or someone's head, fix the durable files rather than explaining around the gap.
