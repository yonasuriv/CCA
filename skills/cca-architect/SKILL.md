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

- **Native ICM**: preserve its five layers, `CLAUDE.md`, root/stage `CONTEXT.md`, hyphenated numbered stages, exact Inputs/Process/Outputs contract shape, selective section routing, one-way references, and output handoffs.
- **Native LLM Wiki**: discover the implementation's own schema and maintenance conventions first. Do not force CCA frontmatter, page taxonomy, log syntax, or directory names onto it.
- **Ordinary project**: preserve the existing project layout unless the user explicitly wants restructuring.
- **CCA-conformant**: preserve the CCA specification the workspace intentionally adopted.

Compatibility is acceptance, not ownership. Do not label an upstream workspace CCA-conformant merely because CCA can read it.

## Build mode

1. Extract the workflow and knowledge boundaries already implied by the request.
2. Choose the smallest useful form. Pipelines fit sequential handoffs; knowledge bundles fit persistent synthesis; hybrids are valid when a pipeline consumes or maintains knowledge.
3. Scaffold only the files the form needs.
4. For ICM-compatible pipelines, use `stages/01-name/` and the exact ICM contract table shape from the bundled stage template.
5. Use `AGENTS.md` for portable guidance when it improves cross-agent routing. Preserve native instruction files required by the target harness/profile.
6. Add adapters only when needed and only after reading `references/adapters.md`.
7. Validate with a fresh-agent walk test.

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

## Walk test

Simulate a fresh agent with no chat memory:

1. **Orient**: identify the workspace, active profile/form, and where relevant context lives.
2. **Act**: perform one representative operation using only routed files and available tools.
3. **Report**: state what changed, what was produced, what remains, and what is ambiguous or broken.

If required knowledge exists only in chat history or someone's head, fix the durable files rather than explaining around the gap.
