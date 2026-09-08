# ICM inheritance map

This file maps the current upstream Interpretable Context Methodology (ICM/MWP) capability surface into CCA. It is a compatibility map, not a fork or redefinition of ICM.

For a workspace that claims **upstream-native ICM**, the current upstream ICM repository remains authoritative. CCA MUST preserve every applicable upstream rule and acceptance check. If this map drifts from upstream, upstream wins and this map must be updated.

CCA may extend an ICM workspace only when the extension is additive and does not weaken, replace, rename, or silently reinterpret native ICM semantics.

Mapping provenance: the restructure/reference-integrity additions below were revalidated against upstream `RinDig/icm-architect` commit `e16cafe6a664dcf6d787a726b452adba77d913f4`. That revision is evidence for this mapping, not ICM identity and not CCA conformance identity; current upstream authority still wins.

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
| `setup` / `status` triggers | Preserve current native behavior, including artifact-vs-placeholder status semantics | Do not export native trigger semantics into non-native targets unless explicitly adopted. |
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
| Pre-move reference integrity | Before proposing path-changing/destructive restructure work, enumerate in-workspace, sibling-relative, symlink, and bounded known external referrers; apparent disuse is not proof of safety | Reusable safety mechanic for CCA-owned/custom restructures when path changes are in scope. |
| Case-fold destination collision | Check intended destinations case-folded before copy/rename so case-insensitive aliases cannot overwrite an existing path | Reusable filesystem-safety mechanic; does not make a concrete path semantic identity. |
| Copy-verify-remove migration | For substantive moves/renames, copy, verify parity, then remove the source; update/preserve live referrers in the same approved change | Reusable recoverability mechanic when migration mutates existing content. |
| Post-move reference preservation | Re-run references that resolved before the move and were expected to survive | Reusable restructure verification mechanic. |
| System Map inbound consumers | Walk change-impact maps backward to identify bounded known external consumers that point into the mapped tree | Reusable System Map hardening; does not require every CCA target to have a System Map. |

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

CCA Architect retains construction and restructuring workflows: inspect first, preserve authorities, map semantics before paths, require reference integrity before destructive/path-changing proposals, require explicit migration decisions, and validate the claims actually made.

For upstream-native ICM restructures, the inherited current floor includes pre-move referrer discovery, case-fold collision checks, copy-verify-remove migration for substantive existing content, and post-move verification that surviving references still resolve. `../architect/reference-integrity.md` packages these mechanics for Architect without redefining upstream authority.

Where a behavior is borrowed from ICM, CCA may acknowledge that provenance without converting it into a universal CCA conformance requirement.

## System Map reverse walk

For current upstream-native ICM System Map behavior, outward `effects/` reasoning is not sufficient to establish complete change impact. Known consumers outside the mapped tree can point inward without leaving evidence inside the subject.

CCA therefore preserves the inbound/reverse-walk behavior in `../architect/system-map.md`: inspect bounded known external consumers such as configs, sibling/parent repositories, scheduled jobs, agents, harnesses, CI/deploy definitions, and issue/project automation, and record verified inbound dependencies on the card they land on.

## Walk validation

CCA retains a fresh-agent walk test as a portability check for intentionally structured CCA-conformant/profile targets. It is inspired by ICM's durable routing properties but is not equivalent to native ICM validation.

For restructures, a passing walk also requires every pre-move reference expected to survive to resolve after the migration.

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
