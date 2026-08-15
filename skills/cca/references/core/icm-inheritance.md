# ICM inheritance map

This file maps the current upstream Interpretable Context Methodology (ICM/MWP) capability surface into CCA. It is a compatibility map, not a fork or redefinition of ICM.

For a workspace that claims **native ICM**, the current upstream ICM repository remains authoritative. CCA must preserve every applicable upstream rule and acceptance check. If this map drifts from upstream, upstream wins and this map must be updated.

CCA may extend an ICM workspace only when the extension is additive and does not weaken, replace, rename, or silently reinterpret native ICM semantics.

## Provenance classes

Use these classifications when auditing CCA against ICM:

- **Inherited / preserved**: an ICM capability remains available with the same native semantics.
- **Inherited / extended**: the ICM capability is preserved and CCA adds optional interoperability around it.
- **Delegated to upstream**: CCA intentionally relies on the current upstream rule/validator instead of freezing a competing copy.
- **ICM-derived only**: CCA borrows a pattern without claiming native ICM compatibility.
- **Regression**: CCA claims native ICM compatibility but removes, weakens, contradicts, or replaces an applicable upstream capability.

An inherited capability is not an "ICM-only" capability merely because it originated in ICM.

## Native Layer 0 and five-layer routing

Upstream native ICM defines:

1. Layer 0: `CLAUDE.md`
2. Layer 1: root `CONTEXT.md`
3. Layer 2: stage `CONTEXT.md`
4. Layer 3: stable reference/factory material
5. Layer 4: per-run working/product artifacts

CCA classification: **Inherited / extended**.

For native ICM, preserve the native `CLAUDE.md` Layer-0 entry semantics. `AGENTS.md` may be added as portable cross-agent guidance only when it does not replace or invalidate the native entry path. Generic CCA-created workspaces may prefer `AGENTS.md`; that preference is not retroactively an ICM rule.

## ICM pattern inheritance

| Upstream capability | CCA native-ICM requirement | Classification |
|---|---|---|
| Stage contracts | Preserve exact `Inputs`, `Process`, `Outputs` semantics and canonical Inputs columns `Source | File/Location | Section/Scope | Why` | Inherited / preserved |
| Stage handoffs through `output/` | Preserve predictable downstream handoffs and human-editable artifacts | Inherited / preserved |
| One-way cross-references | Preserve cycle-free dependency direction; do not add reverse links for symmetry | Inherited / preserved |
| Selective section routing | Preserve section-scoped loading when full files are unnecessary | Inherited / preserved |
| Canonical sources | Preserve one canonical home per substantive fact/rule; prefer links over competing copies | Inherited / preserved |
| `CONTEXT.md` routing purity | Keep routers/contracts compact; substantive reference material remains outside routers | Inherited / preserved |
| Tool prerequisites | Preserve setup/verification guidance for required system tools | Inherited / preserved |
| `setup` / `status` triggers | Preserve current upstream behavior for native ICM | Delegated to upstream acceptance |
| Questionnaire design | Preserve flat, all-at-once, system-level, derive-don't-ask, sensible-default, ask-once behavior | Inherited / preserved |
| Bundled skills | Preserve workspace-local skill bundling when the native workspace uses it; CCA may additionally route Agent Skills portably | Inherited / extended |
| Specs as contracts | Preserve WHAT/WHEN separation from implementation HOW where applicable | Inherited / preserved |
| Human checkpoints | Preserve checkpoints for applicable creative stages | Inherited / preserved |
| Stage audits | Preserve audits for applicable creative/build stages | Inherited / preserved |
| Value validation | Preserve applicable value checks before/within content-producing work | Inherited / preserved |
| Docs over outputs | Preserve stable reference docs as authority over prior generated artifacts | Inherited / preserved |
| Shared constants | Preserve canonical configurable values for applicable code-producing workspaces | Inherited / preserved |
| Quality guardrails | Preserve current upstream native limits/style rules when claiming native ICM | Delegated to upstream acceptance |
| Placeholder syntax/coverage | Preserve current upstream syntax, conditional semantics, complete substitution, and no orphan placeholders | Delegated to upstream acceptance plus `native-icm-setup.md` coverage mapping |

## Factory / product semantics

Upstream ICM distinguishes stable Layer-3 configuration/reference material from changing Layer-4 per-run artifacts.

CCA classification: **Inherited / extended**.

CCA's generic role vocabulary (`factory`, `product`, `source`, `synthesis`, and related roles) may describe functions across broader workspaces, but it must not erase the native Layer-3/Layer-4 distinction inside an ICM workspace.

## Workspace forms

CCA preserves the ICM architectural forms it inherits and may apply equivalent forms outside native ICM only as design heuristics. In CCA they are not evidence that the form became CCA-owned.

Current CCA architect coverage includes:

- Pipeline
- Umbrella
- Record Library
- Knowledge Bundle
- Context Map
- System Map

When a form is used for native ICM, upstream constraints win. When used generically, CCA may relax ICM-specific requirements that are not claimed.

## Build and restructure behavior

CCA architect retains both construction and restructuring workflows:

- **Build**: derive the smallest justified workspace from the actual process/problem, preserving native profiles and external authorities.
- **Restructure**: audit first, classify existing material, propose an explicit migration map, require approval before destructive/moving changes, then validate the applicable native profile.

CCA classification: **Inherited / extended** where these behaviors originate from ICM and are generalized without weakening native ICM.

## Walk validation

CCA retains the cold/fresh-agent walk test:

1. Orient from durable workspace files without chat memory.
2. Act using routed context and available tools.
3. Report changes, outputs, remaining work, and ambiguity.

CCA classification: **Inherited / extended**.

For native ICM, the CCA walk test supplements current upstream validation. Passing CCA's walk test never converts an upstream failure into a pass.

## CCA extensions beyond the ICM floor

The following are additive CCA concerns and must not be used to rewrite native ICM:

- interoperability with existing LLM Wiki implementations;
- human-method overlays such as PARA, Zettelkasten, and BASB/CODE;
- portable AGENTS.md guidance across compatible harnesses;
- profile-aware linting that distinguishes upstream validity from optional hardening;
- cross-method and cross-profile routing;
- advisor guidance for engineering, process/frameworks, security, agents, context engineering, and AI/ML;
- one installable Agent Skill with lazy internal modes;
- operation modes for scaffold, sync, ingest, query, and lint.

These extensions are evaluated separately from ICM conformance. CCA succeeds as an ICM evolution layer only if the inherited ICM floor remains intact first.

## Acceptance rule

For any native-ICM claim:

```text
current upstream ICM acceptance
        AND
no CCA regression of applicable ICM semantics
        AND
optional CCA extensions do not weaken upstream behavior
```

If any applicable upstream requirement fails, report the workspace as not native-ICM-compatible even if CCA-specific validation passes.
