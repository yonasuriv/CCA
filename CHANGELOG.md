# Changelog

This changelog records released CCA milestones and pending user-visible changes. Normative semantics remain governed by the versioned specification and compatibility references inside `skills/cca/`.

## Unreleased

No changes yet. New user-visible, compatibility, semantic, profile, packaging, or release-relevant changes should be recorded here before the next release.

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
