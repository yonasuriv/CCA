# ICM inheritance map

This file maps the current upstream Interpretable Context Methodology (ICM/MWP) capability surface into CCA. It is a compatibility map, not a fork or redefinition of ICM.

For a workspace that claims **native ICM**, the current upstream ICM repository remains authoritative. CCA must preserve every applicable upstream rule and acceptance check. If this map drifts from upstream, upstream wins and this map must be updated.

CCA may extend an ICM workspace only when the extension is additive and does not weaken, replace, rename, or silently reinterpret native ICM semantics.

## Provenance classes

- **Inherited / preserved**: an ICM capability remains available with the same native semantics.
- **Inherited / extended**: the ICM capability is preserved and CCA adds optional interoperability around it.
- **Delegated to upstream acceptance**: CCA performs the behavior but relies on current upstream validation/rules rather than freezing a competing validator.
- **ICM-derived only**: CCA borrows a pattern without claiming native ICM compatibility.
- **Regression**: CCA claims native ICM compatibility but removes, weakens, contradicts, or replaces an applicable upstream capability.

An inherited capability is not an "ICM-only" capability merely because it originated in ICM.

## Native Layer 0 and five-layer routing

Upstream native ICM defines Layer 0 `CLAUDE.md`, Layer 1 root `CONTEXT.md`, Layer 2 stage `CONTEXT.md`, Layer 3 stable reference/factory material, and Layer 4 per-run working/product artifacts.

CCA classification: **Inherited / extended**. For native ICM, preserve native `CLAUDE.md` Layer-0 entry semantics and exact `CONTEXT.md` filenames. Outside native ICM, the same layer **roles** apply with default filenames `CONTEXT.md`; alternate names are allowed only when declared in the Layer-0 skeleton map (`../core/spec.md` §5.1). `AGENTS.md` may be added as portable cross-agent guidance only when it does not replace or invalidate the native entry path.

## ICM pattern inheritance

| Upstream capability | CCA native-ICM requirement | Classification |
|---|---|---|
| Stage contracts | Preserve exact `Inputs`, `Process`, `Outputs` semantics and canonical Inputs columns `Source | File/Location | Section/Scope | Why` | Inherited / preserved |
| Folder contract filename | Default `CONTEXT.md`; under native ICM must remain `CONTEXT.md`; outside native ICM renamable only via L0 map | Inherited / extended |
| One folder, one job | Each working folder states its job in its folder-contract file | Inherited / preserved |
| Stage handoffs through `output/` | Preserve predictable downstream handoffs and human-editable artifacts | Inherited / preserved |
| One-way cross-references | Preserve cycle-free dependency direction | Inherited / preserved |
| Selective section routing | Preserve section-scoped loading when full files are unnecessary | Inherited / preserved |
| Canonical sources | Preserve one canonical home per substantive fact/rule | Inherited / preserved |
| Contract-file routing purity | Keep routers/contracts compact; substantive reference material remains outside routers | Inherited / preserved |
| Tool prerequisites | Preserve setup/verification guidance for required system tools | Inherited / preserved |
| `setup` / `status` triggers | Perform current native behavior through `../architect/workspace-builder.md`; upstream remains acceptance authority | Inherited / preserved |
| Questionnaire design | Preserve flat, all-at-once, system-level, derive-don't-ask, sensible-default, ask-once behavior | Inherited / preserved |
| Bundled skills | Discover/bundle workspace-local domain skills when applicable; CCA may additionally route Agent Skills portably | Inherited / extended |
| Specs as contracts | Preserve WHAT/WHEN separation from implementation HOW where applicable | Inherited / preserved |
| Human checkpoints | Preserve checkpoints for applicable creative stages | Inherited / preserved |
| Stage audits | Preserve audits for applicable creative/build stages | Inherited / preserved |
| Value validation | Preserve applicable value checks before/within content-producing work | Inherited / preserved |
| Docs over outputs | Preserve stable reference docs as authority over prior generated artifacts | Inherited / preserved |
| Shared constants | Preserve canonical configurable values for applicable code-producing workspaces | Inherited / preserved |
| Quality guardrails | Perform/check current native rules; upstream decides acceptance | Delegated to upstream acceptance |
| Placeholder syntax/coverage | Perform substitution/conditional handling and coverage checks through Architect builder; upstream syntax wins | Inherited / preserved + upstream acceptance |

## Workspace-builder behavior

CCA Architect ships `../architect/workspace-builder.md` as a first-class runtime capability. It preserves the applicable upstream builder behavior without requiring the upstream builder checkout at execution time:

1. Discovery
2. Mapping
3. Scaffolding
4. Questionnaire design
5. Validation and repair
6. setup execution
7. status execution
8. fresh-agent verification

The current upstream ICM repository remains the semantic and acceptance authority. The CCA implementation exists so the installed CCA skill is not weaker at runtime than the ICM capability it claims to inherit.

## Factory / product semantics

Upstream ICM distinguishes stable Layer-3 configuration/reference material from changing Layer-4 per-run artifacts. CCA classification: **Inherited / extended**. Generic role vocabulary may describe broader workspaces but must not erase the native distinction.

## Workspace forms

CCA preserves inherited architectural forms and may apply equivalent forms outside native ICM only as design heuristics:

- Pipeline
- Umbrella
- Record Library
- Knowledge Bundle
- Context Map
- System Map

When a form is used for native ICM, upstream constraints win.

## Build and restructure behavior

CCA Architect retains construction and restructuring workflows. Build derives the smallest justified workspace from the actual problem. Restructure audits first, classifies material, proposes an explicit migration map, requires approval before destructive/moving changes, and validates the applicable native profile.

CCA classification: **Inherited / extended** where these behaviors originate from ICM and are generalized without weakening native ICM.

## Walk validation

CCA retains the cold/fresh-agent walk test: Orient, Act, Report. Classification: **Inherited / extended**. Passing CCA's walk test never converts an upstream failure into a pass.

## CCA extensions beyond the ICM floor

Additive CCA concerns include interoperability with existing LLM Wiki implementations; PARA, Zettelkasten, BASB/CODE; portable AGENTS.md guidance; profile-aware linting; cross-method/profile routing; advisor guidance; one installable Agent Skill with lazy modes; and scaffold/sync/ingest/query/lint operations.

These extensions are evaluated separately from ICM conformance. CCA succeeds as an ICM evolution layer only if the inherited ICM floor remains intact first.

## Acceptance rule

```text
current upstream ICM acceptance
        AND
CCA runtime can perform applicable inherited behavior
        AND
no CCA regression of applicable ICM semantics
        AND
optional CCA extensions do not weaken upstream behavior
```

If any applicable upstream requirement fails, report the workspace as not native-ICM-compatible even if CCA-specific validation passes.
