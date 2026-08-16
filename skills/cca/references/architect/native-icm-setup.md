# Native ICM setup mapping

Read this only when creating, setting up, or materially rebuilding a **full native ICM workspace**. Generic CCA scaffolding and ICM-derived stage use do not require this procedure. For the executable onboarding/build workflow, read `workspace-builder.md`.

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

## Runtime behavior

`setup` is an inherited native behavior implemented by Architect through `workspace-builder.md`. It must collect the generated questionnaire, hydrate direct/derived/default values, resolve conditional sections/stages, verify no unresolved placeholders remain, and avoid repeating setup after successful configuration.

`status` is also inherited runtime behavior: scan real stage outputs, ignore `.gitkeep`, and render COMPLETE/PENDING state. Do not infer status from plans or conversation history.

## Acceptance

Do not call the native workspace setup-complete until the current upstream questionnaire/placeholder/conditional syntax rules pass together with workspace-builder-equivalent end-to-end validation. CCA's builder performs the workflow; current upstream ICM remains the authority that decides whether the native result is valid.
