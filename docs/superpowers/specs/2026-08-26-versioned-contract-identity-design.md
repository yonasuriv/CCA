# Versioned CCA Contract Identity Design

## Problem

CCA-conformant consumers have started pinning their conformance identity to a CCA repository commit SHA. That couples durable compatibility to an implementation/repository revision and causes otherwise valid workspaces to become tied to one historical source tree.

This contradicts CCA's own portability model: stable semantic contracts should survive repository implementation evolution. A source commit can be useful provenance, but it must not define whether a consumer remains compatible or conformant.

CCA also currently exposes `Version 1.0.0` in the normative spec and citation metadata while user-visible skill behavior has changed under `Unreleased`. The installed `SKILL.md` does not expose a package/contract version, so consumers have no skill-local machine-readable version identity to bind against.

## Decision

CCA compatibility/conformance identity is version-based, never commit-based.

The canonical CCA contract version is exposed from `skills/cca/SKILL.md` frontmatter as:

```yaml
metadata:
  version: "1.1.0"
```

The skill version and normative CCA specification version are one semantic version. They MUST NOT drift as separate identities.

A CCA consumer records the CCA contract version it adopts, for example:

```yaml
cca:
  specification: 1.1.0
```

A consumer MUST NOT use a repository commit, tree SHA, blob SHA, branch revision, tag target SHA, file hash, or installation revision as its compatibility/conformance identity.

VCS/source identities MAY be retained as non-normative audit/debugging provenance. They do not participate in determining current CCA compatibility or conformance.

## Versioning policy

CCA uses SemVer for the installed skill + normative interoperability contract:

- **MAJOR**: incompatible change to CCA-owned normative semantics or an advertised contract.
- **MINOR**: backwards-compatible addition or expansion of CCA-owned semantics, modes, lint/audit behavior, compatibility handling, or other advertised behavior.
- **PATCH**: backwards-compatible correction to behavior already promised by the current contract.
- **No version bump**: changes with no effect on installed CCA contract or advertised runtime behavior, such as typo-only explanatory documentation or internal CI maintenance.

The existing post-1.0 changes under `Unreleased` materially expand CCA behavior (workspace architecture audit semantics and detached-boundary portability), so this change establishes **CCA 1.1.0**.

## Version coherence

The following release surfaces must agree on the same version:

- `skills/cca/SKILL.md` → `metadata.version` (canonical installed identity)
- `skills/cca/references/core/spec.md`
- `skills/cca/CITATION.cff`
- root `CITATION.cff`
- current released entry in `CHANGELOG.md`

CI must validate this coherence.

## Version-bump enforcement

CCA CI must also detect behavior/contract drift without a version bump.

A dedicated version gate compares the current tree with the applicable Git baseline. If installed/normative behavior surfaces changed while `skills/cca/SKILL.md` `metadata.version` is unchanged from the baseline, validation fails.

Contract-sensitive surfaces include:

- `skills/cca/SKILL.md`
- `skills/cca/references/core/`
- `skills/cca/references/architect/`
- `skills/cca/references/operations/`
- `skills/cca/references/advisor/` when advertised decision behavior changes
- `skills/cca/assets/` when installed behavior/profile contracts change

The gate is not a substitute for review: it enforces that a behavior-changing diff carries an explicit version decision.

## CCA runtime behavior

### Core specification

CCA adds a normative contract-identity rule:

> CCA compatibility, conformance, and CCA-owned profile claims MUST identify the applicable CCA contract by version. Repository/source revision identities MUST NOT serve as conformance identity. VCS identities MAY be retained only as non-normative provenance.

### Architect / builder / scaffold

When creating or remediating a CCA-conformant consumer, CCA writes or recommends a versioned contract identity and never introduces a commit pin.

### Lint

Lint checks intentionally adopted CCA contracts against their declared CCA version. A normative commit/revision pin is a conformance error. A historical source SHA in clearly non-authoritative evidence/provenance is allowed.

### Compatibility

Compatibility documentation distinguishes:

- **contract identity** → CCA version
- **source provenance** → optional commit/tree/blob/hash metadata

Changing `main` or publishing additional commits under the same contract version cannot by itself invalidate an existing conformant consumer.

## Consumer migration: Symbiont

Symbiont is migrated from:

```yaml
cca:
  specification: 1.0.0
  reference_commit: <sha>
```

to:

```yaml
cca:
  specification: 1.1.0
```

Active validation must no longer require a CCA repository commit. Historical evidence may preserve the old SHA as provenance describing what source was inspected at the time.

Symbiont's validator, schemas, conformance matrix, tests, and active evidence/claim logic must be updated so version determines contract identity and source revision does not.

## Durable Symbiont learning

The broader collaboration rule is retained in Symbiont's agent-side durable model:

> Compatibility with an external architecture, standard, skill, protocol, or framework should bind to its declared versioned contract, not its repository commit. Source commits are provenance/debugging evidence unless the external contract explicitly defines commit identity as normative.

This is a general operating heuristic, not a CCA-only registry object.

## Verification

CCA must pass its complete repository validation suite, including new tests proving:

1. `SKILL.md` exposes version `1.1.0`;
2. all canonical release/version surfaces agree;
3. normative CCA docs reject commit identity for consumer conformance;
4. lint/architect/builder guidance uses contract versions;
5. the version gate fails when a contract-sensitive surface changes without a version bump and passes when the version changes.

Symbiont must pass its complete validation suite after removing the active CCA commit pin, and its conformance claim must report CCA `1.1.0` without requiring a CCA source SHA.

## Non-goals

- Do not remove commit SHAs from historical evidence or ordinary Git provenance.
- Do not prevent upstream compatibility mappings from pinning an upstream source revision internally when source-nearest verification genuinely needs one; that is CCA's mapping provenance, not a consumer's CCA identity.
- Do not make Git tags or GitHub releases the runtime compatibility authority. The versioned contract inside the installed skill remains canonical.
- Do not create a second package version independent from the normative specification version.
