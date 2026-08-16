# Architect mode

Design the smallest filesystem structure that makes the work navigable, durable, and agent-agnostic.

Read `../core/spec.md` and `core.md` before designing. Read `forms.md` only when choosing a workspace form. Read `workspace-builder.md` when the request is to create, initialize, set up, report status for, or materially rebuild a workspace. Read `methods.md` when the request involves PARA, Zettelkasten, BASB/CODE, second brains, PKM, LLM Wiki/ICM composition, or another hybrid knowledge-work architecture. Read `../core/adapters.md` only when a harness-specific adapter is needed. Templates live under `assets/templates/`. Preserve the active native/profile entry semantics first; add a harness bridge to shared portable guidance only when the harness currently supports that mechanism and the target profile permits it.

## Role in the CCA skill suite

`cca` in `architect` mode is the primary entry point for compound **architecture** requests: decide what the workspace should become, which methods/profiles apply, where boundaries sit, which builder path applies, and which focused operation should execute next.

It is not a mandatory gateway for already-clear operations. A direct lint request should use `cca` in `lint` mode; a direct ingest request should use `cca` in `ingest` mode; likewise for scaffold, sync, and query.

## Trigger routing

- **create / build / initialize workspace** → load `workspace-builder.md` and execute the applicable profile-driven builder.
- **setup** for native ICM → load `workspace-builder.md` plus `native-icm-setup.md` and perform inherited onboarding/hydration behavior.
- **status** for native ICM → load `workspace-builder.md` and derive COMPLETE/PENDING from real stage outputs.
- **restructure / migrate** → use Restructure mode; if rebuilding a complete workspace, also load `workspace-builder.md` after authority/migration decisions are approved.

When architecture work requires another CCA capability, delegate semantically by mode name, for example `Use scaffold mode to implement the approved structure` or `Use lint mode to validate the claimed profile`. Never depend on removed sibling skill directories.

## Compatibility gate

Before changing structure, identify the current profile and any method overlays:

- **Native ICM**: preserve the complete applicable current ICM profile, not only its stage folder shape. Preserve native Layer-0 `CLAUDE.md`, five-layer routing, root/stage `CONTEXT.md` (exact upstream filenames), exact stage contracts, setup/status behavior, questionnaire rules, naming, handoffs, selective loading, one-way references, canonical sources, applicable checkpoints/audits/spec/value/shared-constant rules, quality guardrails, and workspace-builder validation. Portable `AGENTS.md` may interoperate but does not override native entry semantics. Read `../core/icm-inheritance.md`; for creation/setup also read `workspace-builder.md` and `native-icm-setup.md`.
- **ICM skeleton**: same layer roles and contracts; declare filenames in the L0 skeleton map (`../core/spec.md` §5.1); default to `CONTEXT.md`; never assume names. Not a native pipeline claim.
- **ICM-derived**: another project may borrow numbered stage contracts or output handoffs without claiming full native ICM. Keep that distinction explicit.
- **Native LLM Wiki**: discover the implementation's own schema and maintenance conventions first. Do not force CCA frontmatter, page taxonomy, log syntax, or directory names onto it.
- **Ordinary project**: preserve the existing project layout unless the user explicitly wants restructuring.
- **CCA-conformant**: preserve the CCA specification the workspace intentionally adopted.
- **Method overlays**: PARA, Zettelkasten, and BASB/CODE may organize or guide the workspace without becoming structural compatibility profiles. Preserve their semantics and nested boundaries.

Compatibility is acceptance, not ownership. Do not label an upstream workspace CCA-conformant merely because CCA can read it, and do not label a partial ICM-derived scaffold as native ICM-compatible.

## Build mode

1. Extract the workflow, knowledge boundaries, organizational method, and authority boundaries already implied by the request.
2. If building a complete workspace rather than a small focused scaffold, load `workspace-builder.md` and use its discovery → mapping → scaffolding → questionnaire → validation/repair flow.
3. Choose the smallest useful form. Pipelines fit sequential handoffs; knowledge bundles fit persistent synthesis; ordinary repositories keep their existing structure; hybrids are valid when those concerns naturally compose.
4. If PARA, Zettelkasten, BASB, second-brain/PKM, or mixed knowledge-work methods are involved, load `methods.md` and preserve them as method overlays rather than compatibility profiles.
5. Decide whether a pipeline needs the **full native ICM profile** or only **ICM-derived stage-contract patterns**. Do not silently upgrade one claim into the other.
6. Identify nested native boundaries. An outer PARA/CCA organization may place a native ICM workspace or LLM Wiki but must not rewrite its internals merely for consistency.
7. If the intended result will be contributed to an upstream project, check that upstream repository's current contribution policy before scaffolding. Compatibility does not waive repository-specific contribution requirements.
8. For a full native ICM workspace, Architect itself can perform workspace-builder-equivalent behavior through `workspace-builder.md`; current upstream conventions/validation still decide whether the result is native-valid. If an upstream contribution policy specifically mandates its own builder artifact/process, follow that contribution rule.
9. Implement only the files the selected form/profile actually needs. Prefer scaffold mode for a focused in-place scaffold rather than duplicating that operation.
10. Use `AGENTS.md` for portable guidance only when it improves cross-agent routing without replacing native instruction files.
11. Add adapters only when needed and only after reading `../core/adapters.md`.
12. Validate the selected native profile first, then run the CCA fresh-agent walk test.

## Restructure mode

1. **Audit** the actual folder and read enough content to classify confidently.
2. **Preserve native semantics** before proposing CCA hardening.
3. **Preserve method boundaries** before proposing taxonomy changes.
4. **Propose a migration map**: current path → function/profile → destination → action → compatibility impact.
5. **Stop for explicit approval** before moves, merges, renames, or deletions.
6. Apply only the approved map. Preserve content unless deletion was explicitly approved.
7. Use sync mode after approved structural changes when navigation/routing needs reconciliation.
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
- Cross-mode coordination uses semantic mode names, never sibling filesystem paths.
- Never invent a competing convention where an upstream standard already solves the problem.
- Never claim a harness precedence rule you have not verified.
- Never substitute the CCA walk test for an upstream profile's stricter acceptance criteria.
- Never use compatibility as a reason to bypass an upstream repository's contribution process.

## Walk test

The walk test is a CCA portability check **after** applicable native-profile validation, not a replacement for it.

Simulate a fresh agent with no chat memory:

1. **Orient**: identify the workspace, active profile/form/method overlays, nested authority boundaries, and where relevant context lives.
2. **Act**: perform one representative operation using only routed files and available tools.
3. **Report**: state what changed, what was produced, what remains, and what is ambiguous or broken.

If required knowledge exists only in chat history or someone's head, fix the durable files rather than explaining around the gap.

## Advisor consultation boundary

Architecture owns workspace structure; advisor owns engineering judgment. When a structural choice depends on engineering/process trade-offs, lazily read only the relevant file under `../advisor/`. Do not copy advisor guidance into architect references and do not turn a methodology into a CCA structural profile.
