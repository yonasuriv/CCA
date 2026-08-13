---
name: cca-architect
description: Design or restructure a filesystem-native CCA workspace while preserving native boundaries. Use for new agent workspaces, second brains, PKM systems, PARA, Zettelkasten, Building a Second Brain/BASB, LLM Wiki, ICM, coding/client/research workspaces, or hybrids that need several methods to coexist. Chooses the smallest form, preserves upstream semantics, and semantically delegates focused CCA operations when needed.
compatibility: Filesystem read/write access. No vendor-specific runtime required.
---

# CCA Architect

Design the smallest filesystem structure that makes the work navigable, durable, and agent-agnostic.

Read [references/core.md](references/core.md) before designing. Read [references/forms.md](references/forms.md) only when choosing a workspace form. Read [references/methods.md](references/methods.md) when the request involves PARA, Zettelkasten, BASB/CODE, second brains, PKM, LLM Wiki/ICM composition, or another hybrid knowledge-work architecture. Read [references/adapters.md](references/adapters.md) only when a harness-specific adapter is needed. Templates live under `assets/templates/` and include the Layer-0 `AGENTS.md` catalog, pipeline contracts, wiki/log helpers, and the context-map operating model (`node.md`, `schema.md`). Harness-specific entry files such as `CLAUDE.md` are not shipped as templates; create them by directive as a single-line `@AGENTS.md` include only when a harness needs its own entry path.

## Role in the CCA skill suite

`cca-architect` is the primary entry point for compound **architecture** requests: decide what the workspace should become, which methods/profiles apply, where boundaries sit, and which focused operation should execute next.

It is not a mandatory gateway for already-clear operations. A direct lint request should use `cca-lint`; a direct ingest request should use `cca-ingest`; likewise for scaffold, sync, and query.

When architecture work requires another CCA capability, delegate semantically by skill name, for example `Use cca-scaffold to implement the approved structure` or `Use cca-lint to validate the claimed profile`. Never reach into a sibling skill directory or depend on its implementation paths.

## Compatibility gate

Before changing structure, identify the current profile and any method overlays:

- **Native ICM**: preserve the complete applicable current ICM profile, not only its stage folder shape. This includes `AGENTS.md` as the authoritative Layer-0 catalog (with a single-line `@AGENTS.md` `CLAUDE.md` include when a harness path is needed; an existing upstream workspace keeps its native `CLAUDE.md`), five-layer routing, root/stage `CONTEXT.md`, exact stage contracts, setup/status behavior, questionnaire rules, naming, handoffs, selective loading, one-way references, canonical sources, applicable checkpoints/audits/spec/value/shared-constant rules, quality guardrails, and workspace-builder-equivalent validation. See `references/core.md`.
- **ICM-derived**: another project may borrow numbered stage contracts or output handoffs without claiming to be a full native ICM workspace. Keep that distinction explicit.
- **Native LLM Wiki**: discover the implementation's own schema and maintenance conventions first. Do not force CCA frontmatter, page taxonomy, log syntax, or directory names onto it.
- **Ordinary project**: preserve the existing project layout unless the user explicitly wants restructuring.
- **CCA-conformant**: preserve the CCA specification the workspace intentionally adopted.
- **Method overlays**: PARA, Zettelkasten, and BASB/CODE may organize or guide the workspace without becoming structural compatibility profiles. Preserve their semantics and nested boundaries; do not invent a universal CCA acceptance schema for them.

Compatibility is acceptance, not ownership. Do not label an upstream workspace CCA-conformant merely because CCA can read it, and do not label a partial ICM-derived scaffold as native ICM-compatible.

## Build mode

1. Extract the workflow, knowledge boundaries, organizational method, and authority boundaries already implied by the request.
2. Choose the smallest useful form. Pipelines fit sequential handoffs; knowledge bundles fit persistent synthesis; ordinary repositories keep their existing structure; hybrids are valid when those concerns naturally compose.
3. If PARA, Zettelkasten, BASB, second-brain/PKM, or mixed knowledge-work methods are involved, load `references/methods.md` and preserve them as method overlays rather than compatibility profiles.
4. Decide whether a pipeline needs the **full native ICM profile** or only **ICM-derived stage-contract patterns**. Do not silently upgrade one claim into the other.
5. Identify nested native boundaries. An outer PARA/CCA organization may place a native ICM workspace or LLM Wiki but must not rewrite its internals merely for consistency.
6. If the intended result will be contributed to an upstream project, check that upstream repository's current contribution policy before scaffolding. Compatibility does not waive repository-specific contribution requirements. In particular, if the current ICM repository requires contributed workspaces to be created with its `workspace-builder`, follow that process rather than substituting CCA's generator.
7. Implement only the files the selected form/profile actually needs. Prefer `Use cca-scaffold` for focused in-place scaffolding rather than duplicating that skill's procedure here.
8. For a full native ICM workspace outside any stricter upstream contribution workflow, implement the complete applicable ICM profile from `references/core.md`, create `AGENTS.md` as the authoritative Layer-0 catalog, and validate against the current upstream convention/validation surface before claiming compatibility. Create a harness entry (`CLAUDE.md`, `GEMINI.md`, ...) as a single-line `@AGENTS.md` include only when a harness requires it. If the workspace already has a native `CLAUDE.md`, do not overwrite it; derive the portable `AGENTS.md` counterpart from it instead, keeping one substantive source of truth.
9. For ICM-derived pipelines, use `stages/01-name/`, exact ICM contract columns, selective routing, one-way dependencies, and output handoffs, but describe the result as ICM-derived unless the rest of the native profile also passes.
10. Use `AGENTS.md` for portable guidance when it improves cross-agent routing. Preserve native instruction files required by the target harness/profile. When a native `CLAUDE.md` already exists and portability is wanted, generate the `AGENTS.md` counterpart so both interoperate through the open AGENTS.md convention rather than duplicating rules.
11. Add adapters only when needed and only after reading `references/adapters.md`.
12. Validate the selected native profile first. When the CCA suite is available, use `cca-lint` for profile-aware validation, then run the CCA fresh-agent walk test.

## Restructure mode

1. **Audit** the actual folder and read enough content to classify confidently.
2. **Preserve native semantics** before proposing CCA hardening.
3. **Preserve method boundaries** before proposing taxonomy changes. Outer organization may wrap nested workspaces; it does not erase them.
4. **Propose a migration map**: current path → function/profile → destination → action → compatibility impact.
5. **Stop for explicit approval** before moves, merges, renames, or deletions.
6. Apply only the approved map. Preserve content unless deletion was explicitly approved.
7. Use `cca-sync` after approved structural changes when navigation/routing needs reconciliation.
8. Validate native compatibility first, then any intentional CCA conformance.

## Invariants

- One fact, one canonical home.
- Routing files point; they do not become knowledge dumps.
- Load only context needed for the current operation.
- Infer ordinary filesystem semantics when safe; do not create a giant manifest merely to restate obvious paths.
- A stage has one job and one-way dependencies.
- Human-editable files are valid handoff surfaces.
- Nest boundaries; do not merge schemas merely because several methods coexist.
- PARA, Zettelkasten, and BASB are method overlays, not native compatibility profiles.
- Cross-skill coordination uses semantic skill names, never sibling filesystem paths.
- Never invent a competing convention where an upstream standard already solves the problem.
- Never claim a harness precedence rule you have not verified.
- Never substitute the CCA walk test for an upstream profile's stricter acceptance criteria.
- Never use compatibility as a reason to bypass an upstream repository's contribution process.
- Prefer CCA's own presentation conventions only where they do not override an upstream-required representation.

## Walk test

The walk test is a CCA portability check **after** applicable native-profile validation, not a replacement for it.

Simulate a fresh agent with no chat memory:

1. **Orient**: identify the workspace, active profile/form/method overlays, nested authority boundaries, and where relevant context lives.
2. **Act**: perform one representative operation using only routed files and available tools.
3. **Report**: state what changed, what was produced, what remains, and what is ambiguous or broken.

If required knowledge exists only in chat history or someone's head, fix the durable files rather than explaining around the gap.
