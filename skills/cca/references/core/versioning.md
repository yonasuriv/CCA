# CCA Contract Versioning

Normative. This file defines the installed CCA contract identity and its evolution rules. It is a companion to [`spec.md`](spec.md).

## Contract identity

CCA compatibility, conformance, and CCA-owned profile claims **MUST identify the applicable CCA contract by version**.

A repository commit, tree SHA, blob SHA, branch revision, tag target SHA, file/content hash, package installation revision, or other source-control identity **MUST NOT serve as CCA conformance identity** and MUST NOT determine whether an otherwise valid consumer remains CCA-compatible or CCA-conformant.

Source-control identities MAY be recorded as **non-normative provenance** for audit, debugging, evidence, reproduction, or source-nearest verification. They describe which source was inspected or executed; they do not define the CCA contract a consumer adopts.

Therefore:

```text
CCA contract identity = CCA version
source revision        = optional provenance
```

A moving branch or additional repository commits under the same declared CCA contract version do not invalidate a conformant consumer merely because their commit identity changed.

This rule concerns **a consumer's identity of CCA itself**. It does not forbid CCA from retaining an upstream source revision inside an upstream compatibility mapping when that revision is useful provenance for verifying what CCA mapped. Upstream mapping provenance and consumer CCA identity are separate concerns.

## Canonical version

The canonical installed CCA contract version is `metadata.version` in the frontmatter of `skills/cca/SKILL.md`.

The installed skill version and the normative CCA specification version are one semantic version. They MUST agree. Release/citation surfaces that publish the current CCA release MUST agree with that version.

Consumers SHOULD record only the version required by their local contract, for example:

```yaml
cca:
  specification: 1.1.0
```

They SHOULD NOT add a CCA source revision to the active conformance identity. Historical evidence MAY separately note which CCA checkout was inspected.

## SemVer policy

CCA uses Semantic Versioning for the installed skill and normative interoperability contract.

- **MAJOR** — incompatible change to CCA-owned normative semantics or an advertised contract.
- **MINOR** — backwards-compatible addition or expansion of CCA-owned semantics, modes, lint/audit behavior, compatibility handling, profile behavior, or other advertised installed behavior.
- **PATCH** — backwards-compatible correction to behavior already promised by the current contract.
- **No bump** — only changes with no effect on the installed CCA contract or advertised runtime behavior, such as typo-only explanatory documentation or internal CI maintenance.

A change to contract-sensitive installed surfaces MUST carry an explicit version decision. CCA repository CI enforces that contract-sensitive changes do not silently retain the same version.

## Validation behavior

When CCA creates, audits, remediates, or lints a consumer:

1. Resolve the CCA contract version the consumer intentionally adopts.
2. Validate the consumer against that versioned contract and any separately declared profile/upstream claims.
3. Treat a normative CCA commit/revision pin as a conformance error because it substitutes implementation revision for contract identity.
4. Permit source revisions in clearly non-authoritative evidence/provenance.
5. Never invalidate a consumer solely because the CCA repository moved to a different commit while the applicable contract version remained the same.

## Current version

CCA contract version: **1.1.1**.

CCA 1.1.0 includes the backwards-compatible post-1.0 expansion of workspace-architecture audit semantics, detached-boundary portability guidance, and this explicit versioned-contract identity rule. CCA 1.1.1 is a patch: the Hybrid Workspace Profile's generated `paths.sh` now resolves correctly when sourced from zsh as well as bash (it previously relied on bash-only associative-array key iteration and `BASH_SOURCE`, which failed silently under zsh); the promised `WS`/`WS_BINDING` lookup behavior is unchanged.
