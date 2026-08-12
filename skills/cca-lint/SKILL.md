---
name: cca-lint
description: Audit a filesystem-native agent workspace against the correct profile: native ICM compatibility, native LLM Wiki compatibility, or intentional CCA conformance. Use when the user asks to lint, validate, health-check, audit, or verify a workspace before sharing or after structural changes. Separates upstream compatibility failures from optional CCA hardening opportunities and repairs only explicitly authorized, unambiguous issues.
compatibility: Filesystem read access is required. Write access is optional and used only when repairs are authorized.
---

# CCA Lint

Validate the workspace it actually is. Do not fail upstream projects for omitting CCA-specific conventions they never adopted.

## 1. Detect the profile

Determine one or more applicable profiles from the workspace files and instructions:

- **ICM native compatibility**
- **LLM Wiki native compatibility**
- **CCA conformance**
- **ordinary project with portable agent guidance**

If detection is ambiguous, report the ambiguity. Do not silently choose the strictest profile.

## 2. Universal structural checks

These checks apply where relevant regardless of profile:

- referenced paths resolve;
- canonical rules are not duplicated as divergent authoritative copies;
- routing files contain routing rather than large bodies of unrelated content;
- nested instruction scopes are preserved rather than flattened;
- adapters do not contradict the canonical guidance they route to;
- files required by an explicitly adopted contract actually exist.

## 3. ICM native compatibility checks

When the workspace claims or exhibits ICM/MWP structure, verify the upstream invariants:

1. Five-layer routing semantics are preserved.
2. Native Layer 0 `CLAUDE.md` behavior is not broken.
3. Root and stage `CONTEXT.md` files route context rather than duplicate reference content.
4. Stage folders use zero-padded lowercase hyphenated names such as `01-collect`.
5. Every stage contract contains `Inputs`, `Process`, and `Outputs`.
6. The Inputs table uses the canonical columns `Source | File/Location | Section/Scope | Why`.
7. Inputs use selective section routing where only part of a reference is needed.
8. Cross-stage/reference dependencies are one-way.
9. Each stage writes to its own `output/` handoff surface.
10. Canonical-source discipline is preserved.

CCA-only wiki metadata is irrelevant to this profile unless the workspace also adopted it.

## 4. LLM Wiki native compatibility checks

Do not require one directory schema. Verify the implementation's own instructions first, then check the core behavior:

1. durable source material/evidence exists or has a defined home;
2. maintained synthesis persists across sessions;
3. there is an explicit maintenance procedure for integrating/querying knowledge;
4. the knowledge base is directly inspectable/editable as files;
5. the implementation's own links/index/schema resolve and are internally coherent.

Missing CCA frontmatter, `raw/`, `wiki/`, `wiki/index.md`, `log.md`, entity/concept subdirectories, or CCA log syntax are **not** native LLM Wiki failures.

## 5. CCA conformance checks

Only apply requirements the workspace intentionally adopted. Examples include:

- portable `AGENTS.md` routing;
- CCA file-role classifications;
- a CCA-hardened knowledge bundle;
- provenance/lifecycle metadata;
- CCA maintenance history conventions;
- the fresh-agent walk test.

Report optional hardening recommendations separately from errors.

## 6. Agent Skills checks

When a `skills/` directory exists, validate each bundled skill independently:

- `SKILL.md` exists;
- frontmatter contains valid `name` and `description`;
- directory name and skill name agree;
- name uses lowercase letters, digits, and hyphens and remains within the current Agent Skills limits;
- description states purpose and trigger conditions and remains within the current limits;
- referenced resources are relative and exist inside the skill package;
- core behavior does not require a sibling skill or repository-global file;
- detailed resources are progressively disclosed rather than copied wholesale into `SKILL.md`.

## 7. History and append-only claims

A filesystem snapshot alone cannot prove that a file has never been rewritten.

- Validate current log syntax only if the active profile defines one.
- Claim append-only history only when version-control/history evidence is actually available and inspected.
- Otherwise report history immutability as **not verified**, not passed.

## 8. Repairs

Default lint behavior is report-only unless the user asked for remediation.

When remediation is authorized, automatically repair only changes whose intent is unambiguous, such as a catalog path that clearly points to a uniquely renamed file. Do not automatically:

- delete files;
- resolve semantic contradictions;
- rename an upstream-native structure into a CCA preference;
- merge competing instruction files without reviewing unique content;
- fabricate missing provenance or metadata.

## Report format

```text
# Lint report — [workspace]

Profiles detected:
- ICM native compatibility: PASS | FAIL | N/A
- LLM Wiki native compatibility: PASS | FAIL | N/A
- CCA conformance: PASS | PARTIAL | N/A

## Compatibility errors
[Issues that break a claimed upstream/native profile]

## CCA conformance errors
[Only requirements intentionally adopted by this workspace]

## Hardening opportunities
[Optional improvements, never presented as upstream failures]

## Verification limits
[Checks that could not be proven from available evidence]

## Repairs applied
[Only if explicitly authorized]
```

## Production rule

A clean lint report means the workspace satisfies the profile it claims. It does not mean CCA has imposed every optional convention it knows about.
