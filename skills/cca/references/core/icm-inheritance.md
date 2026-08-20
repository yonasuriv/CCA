# ICM inheritance map

This file maps the current upstream Interpretable Context Methodology (ICM/MWP) capability surface into CCA. It is a compatibility map, not a fork or redefinition of ICM.

For a workspace that claims **upstream-native ICM**, the current upstream ICM repository remains authoritative. CCA MUST preserve every applicable upstream rule and acceptance check. If this map drifts from upstream, upstream wins and this map must be updated.

CCA may extend an ICM workspace only when the extension is additive and does not weaken, replace, rename, or silently reinterpret native ICM semantics.

## Provenance classes

- **Inherited / preserved**: an ICM capability remains available with the same native semantics.
- **Inherited / extended**: native ICM is preserved and CCA adds optional interoperability around it.
- **Delegated to upstream acceptance**: CCA can operate on the behavior but current upstream validation/rules remain acceptance authority.
- **ICM-derived only**: a non-native target explicitly borrows a pattern without claiming upstream-native ICM.
- **Regression**: CCA claims native ICM interoperability but removes, weakens, contradicts, or replaces an applicable upstream capability.

## Native Layer 0 and five-layer routing

Current upstream ICM defines Layer 0 `CLAUDE.md`, Layer 1 root `CONTEXT.md`, Layer 2 stage `CONTEXT.md`, Layer 3 stable reference/factory material, and Layer 4 per-run working/product artifacts.

CCA classification for an upstream-native ICM boundary: **Inherited / extended**. Preserve native `CLAUDE.md` Layer-0 entry semantics and exact `CONTEXT.md` filenames. Portable `AGENTS.md` MAY be added only when it does not replace or invalidate native authority.

Outside upstream-native ICM, these layer roles are **not universal CCA requirements**. A CCA-owned profile or custom target may explicitly adopt selected ICM-derived navigation behavior; when it does, that target/profile defines its own bindings and acceptance criteria.

## ICM pattern inheritance

| Upstream capability | Upstream-native ICM treatment | Non-native/derived treatment |
|---|---|---|
| Stage contracts | Preserve exact `Inputs`, `Process`, `Outputs` semantics and canonical Inputs columns `Source | File/Location | Section/Scope | Why` | Use only when explicitly adopted; do not call the host native ICM. |
| Folder contract filename | Preserve exact native `CONTEXT.md` where upstream requires it | Binding/name belongs to the adopting local/profile contract; no CCA-global default identity. |
| One folder, one job | Preserve applicable native semantics | Optional ICM-derived design principle. |
| Stage handoffs through `output/` | Preserve predictable downstream handoffs and human-editable artifacts | Optional ICM-derived handoff pattern. |
| One-way cross-references | Preserve cycle-free dependency direction | Apply only where the adopted workflow requires one-way dependency flow. |
| Selective section routing | Preserve section-scoped loading | Reusable ICM-derived context-efficiency pattern. |
| Canonical sources | Preserve one canonical home per substantive fact/rule | Also aligns with CCA's independent one-fact-one-home principle. |
| Contract-file routing purity | Keep native routers/contracts compact | Apply only to routers/contracts the target actually has. |
| Tool prerequisites | Preserve applicable setup/verification guidance | Local implementation decision. |
| `setup` / `status` triggers | Preserve current native behavior | Do not export native trigger semantics into non-native targets unless explicitly adopted. |
| Questionnaire design | Preserve current applicable upstream behavior | Local/profile onboarding contract decides. |
| Bundled skills | Preserve applicable native behavior | Agent Skills/package strategy belongs to the adopting target. |
| Specs as contracts | Preserve upstream WHAT/WHEN discipline where applicable | Optional ICM-derived workflow pattern. |
| Human checkpoints | Preserve where upstream requires/applicably defines them | Add only when the workflow benefits. |
| Stage audits | Preserve where upstream requires/applicably defines them | Add only when the workflow benefits. |
| Value validation | Preserve where applicable | Local workflow policy. |
| Docs over outputs | Preserve native authority discipline | Reusable where it matches the target's authority model. |
| Shared constants | Preserve where applicable | Local implementation decision. |
| Quality guardrails | Check current upstream rules | Do not impose ICM formatting/size rules on generic CCA-compatible workspaces. |
| Placeholder syntax/coverage | Preserve current upstream syntax and coverage | Local/profile configuration contract decides. |

## Workspace-builder behavior

CCA Architect ships `../architect/workspace-builder.md` as a runtime capability so the installed skill can design and operate supported forms without depending on repository-global development files.

For upstream-native ICM generation or maintenance, current upstream ICM remains semantic and acceptance authority. CCA's builder behavior MUST track the current upstream requirements it claims to preserve.

For non-native targets, Architect reuses only mechanics justified by the selected form. It MUST NOT reproduce the native ICM builder surface merely because ICM is an important CCA influence.

## Factory / product semantics

Upstream ICM distinguishes stable Layer-3 configuration/reference material from changing Layer-4 per-run artifacts. For upstream-native ICM this distinction is preserved exactly.

Outside native ICM, a target MAY adopt an analogous stable-input/working-output distinction, but CCA does not require every workspace to expose factory/product layers.

## Workspace forms

CCA may use design heuristics such as Pipeline, Umbrella, Record Library, Knowledge Bundle, Context Map, and System Map. These are CCA design forms, not proof of native ICM status.

When a form is upstream-native ICM, upstream constraints win. When it merely borrows ICM behavior, label the adopted behavior **ICM-derived**.

## Build and restructure behavior

CCA Architect retains construction and restructuring workflows: inspect first, preserve authorities, map semantics before paths, require explicit migration decisions for destructive changes, and validate the claims actually made.

Where a behavior is borrowed from ICM, CCA may acknowledge that provenance without converting it into a universal CCA conformance requirement.

## Walk validation

CCA retains a fresh-agent walk test as a portability check for intentionally structured CCA-conformant/profile targets. It is inspired by ICM's durable routing properties but is not equivalent to native ICM validation.

Passing the CCA walk test never converts an upstream ICM failure into a pass, and generic CCA compatibility alone does not require an ICM-shaped Layer 0/1/2 skeleton.

## CCA extensions beyond native ICM preservation

CCA concerns beyond the native ICM mapping include interoperability with existing LLM Wiki-style knowledge systems; PARA, Zettelkasten, BASB/CODE and other human methods; portable AGENTS.md guidance; cross-boundary semantic roles/bindings; profile-aware linting; advisor guidance; one installable Agent Skill with lazy modes; and optional CCA-owned profiles/reference implementations.

These are evaluated separately from ICM conformance.

## Acceptance rule for upstream-native ICM

```text
current upstream ICM acceptance
        AND
CCA runtime can perform the applicable claimed behavior
        AND
no CCA regression of applicable ICM semantics
        AND
optional CCA additions do not weaken upstream behavior
```

If any applicable upstream requirement fails, report the boundary as not upstream-native ICM even if CCA-specific validation passes.
