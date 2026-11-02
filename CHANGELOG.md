# Changelog

This changelog records released CCA milestones and pending user-visible changes. Normative semantics remain governed by the versioned specification and compatibility references inside `skills/cca/`.

## Unreleased

### Fixed

- `provenance.py` discovers the workspace manifest through the shared bootstrap lookup, so `stamp` and `identity` work on v3 workspaces that use `workspace.yaml`, and a missing or duplicate manifest is reported instead of raising a traceback.

## 1.3.0 - 2026-11-01

Minor: adds Hybrid Workspace Profile **schema v3** as an opt-in contract for existing targets (`--init` now seeds v3). Schema v2 targets keep validating under the unchanged v2 rules and generate byte-identical artifacts; the frozen v2 template is bundled at `assets/hybrid-workspace/profiles/v2/` with its full regression suite.

### Added

- `generation_contract.outputs` (v3): every generated artifact resolves its destination through a declared slot binding (defaults `_runtime/operations/` for helpers and `_runtime/docs/` for the specification), so `WORKSPACE.yaml` is the only fixed bootstrap path. Outputs may only target agent-writable derived/shared system or control bindings that govern the destination and are not nested in content bindings; collisions are checked case-insensitively; the generator replaces an existing file only when it carries that artifact's exact generated header.
- Relocatable, cross-platform helpers: generated `paths`/`mkdirs` helpers default to Python (`paths.py`, `mkdirs.py`, usable on any OS); a `.sh` output name still renders the bash/zsh variant, and names, extensions, and locations are configured in `generation_contract.outputs`. Helpers verify the workspace by a semantic fingerprint (comments and formatting never invalidate them), canonicalise their own path, walk back from their declared destination, and accept the root only when `WORKSPACE.yaml` is there and the declared destination is the helper itself. Helpers embed the SHA-256 of the `WORKSPACE.yaml` they were generated from, so copied or stale helpers fail closed until regenerated; symlinked helpers resolve their own workspace; a failed `source` leaves `WS_ROOT` unset.
- Optional machine-readable workspace `identity` (`endpoint`, `owner`) rendered into the generated router and specification.
- Slots `state.hotset` (indexed for human search), `system.operations`, `system.documentation`, `asset.library`, `asset.templates`, and the `asset` category.
- Representation-aware provenance: Markdown frontmatter (nested `provenance:` mapping or top-level fields) with a body-scoped SHA-256, file sidecars, directory manifests with a coreutils-reproducible `sha256-tree` identity or a per-file `files` map; honest `acquired_at_basis` and `original_acquisition_time` (timestamp, date, or unknown); organizational containers walked at any depth instead of being treated as acquisition batches; optional `field_aliases`.
- Curation records (`curated_by`, `curated_at`, optional `curated_at_basis: promotion | direct-admission | migration`).
- `assets/hybrid-workspace/provenance.py`: streaming identity primitives and a deposit-time `stamp <paths…>` helper limited to `reference.collected` that never overwrites an existing hash, never invents fields, and verifies or rolls back its edit.
- Scoped archive manifests: required for formal semantic retirement, never for ordinary cold storage; every manifest present is validated.
- `tests/test_v3_profile.py` (relocation, root resolution, symlink/copy/containment, identity, curation/provenance, stamping safety, hotset/asset resolution, archive scope, v2 compatibility) and v3 audit self-test mutations.

### Changed

- v3 redefines `reference.collected` / `reference.curated` as actor-independent curation state: collected is preserved raw/reference material not explicitly promoted (any acquirer, legitimate permanent home); curated is deliberately human-admitted maintained reference entered by explicit human-authorized promotion or direct admission. Review never promotes.
- The generator validates the `agent.instructions` binding instead of a hardcoded `AGENTS.md` for v3 targets.
- Normative profile, operation, and method references describe v3, document a v2 → v3 migration procedure, and keep the v2 contract documented as supported.
- ICM compatibility documentation carried into this release:
  - `compatibility.md §4.1`: updated the ICM semantic-authority description to acknowledge that icm-architect's skill references (`references/core.md`, `references/forms.md`, `references/system-map.md`, `references/reference-integrity.md`) are the effective operational spec for Build, Restructure, and System Map behavior; `_core/CONVENTIONS.md` remains the canonical pattern-level authority. Where the two sources diverge on operational detail, icm-architect's field-tested references take precedence.
  - `compatibility.md §4.1 item 11`: extended restructure move-safety to include workspace-root durability confirmation (confirm root is tracked or backed up before reorganizing) as the first gate, ahead of referrer discovery. This reflects the requirement added in icm-architect `references/reference-integrity.md` (2026-08-25).
  - `docs/standards.md`: added restructure move-safety (including workspace-root durability confirmation) and System Map inbound/reverse-walk to the ICM authority prose, keeping the explanatory document consistent with the normative compatibility reference.

### Fixed

- Binding text validation now inspects raw path segments, rejecting `./`, `a/./b`, and empty segments (`a//b`) that `PurePosixPath` previously normalised away. This intentionally also applies to v2 targets, whose behaviour is otherwise unchanged: such bindings could alias the workspace root or another binding.

## 1.2.1 - 2026-09-08

Patch: restores CCA's already-promised current-upstream ICM compatibility floor after upstream `icm-architect` hardened restructure safety in `e16cafe6a664dcf6d787a726b452adba77d913f4` without changing its core invariants.

### Fixed

- Architect restructuring now performs a pre-proposal reference-integrity gate over in-boundary references, sibling `../` paths, symlinks, and bounded known external consumers; apparent disuse is no longer treated as move-safety evidence.
- Path-changing migrations check destinations case-folded before copy/rename, then use copy → parity verification → remove for substantive existing content and re-run surviving pre-move references afterward.
- System Maps now include an inbound/reverse dependency walk for known consumers outside the mapped tree, including configs, sibling/parent repositories, scheduled jobs, agents/harnesses, CI/deploy definitions, and issue/project automation where material.
- Native ICM status semantics now distinguish real output artifacts from placeholder-only files generally; `.gitkeep` remains an example rather than the semantic definition.
- The ICM parity capability suite gained explicit coverage for pre-move reference integrity, case-fold collisions, copy-verify-remove migration, and inbound external consumers.
- Added `references/architect/reference-integrity.md` as a lazy move-safety reference; upstream ICM remains the authority for upstream-native boundaries.

No new CCA semantic identity or Hybrid Workspace Profile behavior is introduced.

## 1.2.0 - 2026-08-27

Minor: makes CCA's versioned-conformance-identity rule (1.1.0) enforceable for the Hybrid Workspace Profile instead of only documented.

### Added

- `WORKSPACE.yaml` gained an optional `cca.specification` field declaring the CCA contract version a workspace targets.
- `audit.py` now checks that field against the installed `skills/cca/SKILL.md` version on every `--target` audit: same major and installed-at-least-declared is compatible; a missing field warns without failing existing workspaces; a major mismatch or an installed version older than declared fails.
- The bundled `WORKSPACE.yaml` template now declares `cca.specification: "1.2.0"`, so `--init` scaffolds a compatibility declaration by default.

This directly replaces the anti-pattern versioning.md already forbade: pinning a CCA source commit/tree/blob hash as a consumer's compatibility gate. `audit.py` never reads or requires a CCA repository revision to determine compatibility — only the declared and installed SemVer.

## 1.1.1 - 2026-08-27

Patch: Hybrid Workspace Profile generated-tooling fix, no semantic/policy change.

### Fixed

- Generated `paths.sh` now resolves the workspace root and sources cleanly under zsh as well as bash. It previously used bash-only `BASH_SOURCE` and `${!array[@]}` key iteration, which failed (`bad substitution`) when sourced from zsh. `WS_BINDING`/`WS` are now emitted as fully literal associative-array declarations (no runtime key loop), and the workspace-root probe branches on `BASH_SOURCE`/`ZSH_VERSION`/`$0`. The promised `WS`/`WS_BINDING` lookup behavior is unchanged.

## 1.1.0 - 2026-08-26

Backwards-compatible expansion of the CCA interoperability contract and installed skill behavior.

### Versioned contract identity

- Exposed the installed CCA contract version as `metadata.version: "1.1.0"` in `skills/cca/SKILL.md`.
- Defined CCA compatibility, conformance, and CCA-owned profile identity by semantic version rather than repository commit, tree, blob, branch, tag-target, file-hash, or installation revision.
- Kept source revisions available only as non-normative provenance for audit, debugging, reproduction, and source-nearest verification.
- Added a canonical skill-local versioning contract and CI enforcement so contract-sensitive installed behavior cannot change without an explicit version decision.
- Clarified that upstream compatibility-mapping source pins are separate provenance and do not become a consumer's CCA identity.

### Detached-boundary portability

- Defined independently addressable child boundaries as repositories/packages/plugins/workspaces that may be cloned, installed, distributed, or operated outside their parent composition.
- Added the rule that such boundaries should remain locally orientable when detached and must not rely on incidental parent filesystem placement for required routing unless parent dependence is intentional and declared.
- Added Architect Audit checks for outward coupling, escaping relative instruction references, parent-only routing/config needed merely for orientation, and exact embedding-path assumptions.
- Kept intentional parent-dependent boundaries valid and clarified that detached portability concerns context/routing/authority rather than requiring every application to execute fully standalone.
- Kept detached-portability findings separate from compatibility/conformance failures unless an adopted contract explicitly requires detached behavior.

### Workspace architecture audit

- Distinguished workspace architecture audit quality from compatibility/conformance linting: a clean claim lint no longer implies efficient context architecture.
- Routed broad repository/workspace audit requests through Architect, preserving the user-requested parent boundary instead of silently narrowing completion to a convenient child boundary.
- Added explicit audit coverage reporting, human/agent navigation quality dimensions, and the hard rule that a child-boundary pass cannot close a parent/workspace audit.
- Clarified that absence of an explicit CCA conformance contract makes `CCA-conformant` inapplicable without automatically making `CCA-compatible` inapplicable.
- Added deterministic regression coverage for the workspace architecture audit contract.

### Repository governance

- Added structured GitHub Issue Forms for concrete bug reports and CCA change proposals while keeping blank issues available for exceptional cases.
- Expanded the pull-request template into an evidence-backed change-summary contract covering rationale, scope/non-goals, authority, compatibility/version impact, verification, and known follow-up debt.
- Documented when to open an issue versus proceeding with a direct pull request, and routed fresh agents/contributors through the same governance surfaces.
- Added regression coverage for the GitHub contribution-governance contract.

## 1.0.0 - 2026-08-21

First stable CCA specification release.

### Core architecture

- Stabilizes CCA as an agent-agnostic interoperability architecture for filesystem-native AI context.
- Defines `boundary + semantic role -> binding` as the primary semantic resolution primitive.
- Establishes convergence over invention, route before search, stable semantics over stable paths, nested-boundary preservation, and human augmentation as core principles.
- Establishes the composable compatibility vocabulary: Upstream-native, CCA-compatible, CCA-conformant, Profile-conformant, and CCA-hardened.
- Preserves ICM, LLM Wiki, AGENTS.md, Agent Skills, human knowledge-work methods, and other external systems as independent authorities rather than absorbing them into CCA.

### Portable skill

- Ships CCA as one self-contained `cca` Agent Skill with seven progressively disclosed modes: `architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`, and `advise`.
- Keeps normative/runtime resources under `skills/cca/` so the installed package does not depend on repository-global implementation files.
- Separates core semantics, architecture, focused operations, and advisor judgment inside the single portable package.

### Hybrid Workspace Profile

- Ships the optional CCA Hybrid Workspace Profile with explicit-target generation/audit tooling and adversarial regression tests.
- Preserves the complete frozen-v1 semantic, policy, authority, vocabulary, generation, and invariant baseline.
- Defines current Hybrid schema v2 by adding only the `reference.curated` and `reference.collected` admission classifications beneath `knowledge.reference` plus the provenance/routing contract required to enforce that distinction.
- Keeps source admission provenance separate from content authorship, semantic role, and review/epistemic state.
- Requires most-specific nested source policy, provenance/content identity for automatically collected evidence, and preservation of raw/reference material through distillation.

### Validation and release hardening

- Validates upstream/native claims separately from CCA/profile claims and optional hardening.
- Includes repository evaluation tests, Hybrid Workspace regression/adversarial tests, exhaustive frozen-contract mutation checks, repository validation, and portable-distribution validation in CI.
- Aligns the public README, exhaustive documentation index, references, publications, citation metadata, contribution workflow, pull-request template, evaluation documentation, and release terminology with the stable 1.0.0 specification.
- Preserves pre-1.0 exploratory material through Git history while removing obsolete design vocabulary from current release guidance.
