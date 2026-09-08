# Changelog

This changelog records released CCA milestones and pending user-visible changes. Normative semantics remain governed by the versioned specification and compatibility references inside `skills/cca/`.

## Unreleased

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
