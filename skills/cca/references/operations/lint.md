# Lint mode

Validate the workspace it actually is. Do not fail upstream projects for omitting CCA-specific conventions they never adopted, and do not invent native PARA/Zettelkasten/BASB profiles.

## 1. Detect the profile

Determine one or more applicable profiles from the workspace files and instructions:

- **ICM native compatibility**
- **ICM-derived patterns only**
- **LLM Wiki native compatibility**
- **CCA conformance**
- **ordinary project with portable agent guidance**

Also detect **method overlays** when locally declared or structurally clear, such as PARA, Zettelkasten, or BASB/CODE. Treat them as preservation/context boundaries, not native compatibility profiles.

If detection is ambiguous, report the ambiguity. Do not silently choose the strictest profile. A project that only borrows ICM stage contracts is not automatically a native ICM workspace.

## 2. Universal structural checks

These checks apply where relevant regardless of profile:

- referenced paths resolve;
- canonical rules are not duplicated as divergent authoritative copies;
- routing files contain routing rather than large bodies of unrelated content;
- nested instruction scopes are preserved rather than flattened;
- nested native/method boundaries remain identifiable;
- adapters do not contradict the canonical guidance they route to;
- files required by an explicitly adopted contract actually exist.

## 3. ICM native compatibility checks

For a workspace that claims native ICM/MWP compatibility, validate the **complete applicable current upstream profile**, not only stage-folder syntax. Treat current upstream ICM `_core/CONVENTIONS.md` as canonical and its workspace-builder validation stage as the practical acceptance checklist for generated workspaces.

At minimum verify:

1. **Five layers.** Native Layer 0 `CLAUDE.md`, root `CONTEXT.md`, stage `CONTEXT.md`, selectively loaded reference material, and working artifacts preserve ICM semantics.
2. **Root routing.** One root `CONTEXT.md` routes task types to the appropriate stages rather than storing reference content.
3. **Stage contracts.** Every stage has `Inputs`, `Process`, and `Outputs`; the Inputs table uses exactly `Source | File/Location | Section/Scope | Why`.
4. **CONTEXT purity.** `CONTEXT.md` files contain routing/process/checkpoint/audit/output contract material, not extended reference content.
5. **Naming.** Files/folders follow current ICM naming rules; stages use zero-padded `01-name` prefixes; output artifacts follow the workspace convention; no spaces; intentionally empty persistent folders contain `.gitkeep`.
6. **Handoff chain.** Each stage writes to its own `output/`; Stage N+1 references Stage N's actual output location; the chain is unbroken.
7. **Reference integrity.** Every path named by an Inputs table exists.
8. **One-way graph.** Cross-stage/reference dependencies are acyclic and do not point backward in a way that creates circular dependencies.
9. **Selective routing.** Inputs identify exact sections where only part of a reference is needed; use `Full file` only when justified.
10. **Canonical sources.** Substantive rules have one authoritative home; downstream routers point rather than duplicate.
11. **Setup trigger.** `setup` starts the one-time onboarding flow defined by the workspace and resolves configured placeholders.
12. **Status trigger.** `status` reports pipeline completion according to the current ICM convention. Do not substitute a different presentation format when native ICM specifies one.
13. **Questionnaire.** Onboarding is flat, all-at-once, system-level, derives instead of re-asking inferable fields, supplies sensible defaults/examples, and is not repeated after setup.
14. **Placeholder coverage.** Every placeholder has a corresponding setup answer/question, every questionnaire field maps somewhere useful, no unresolved/orphaned placeholders remain, and conditional placeholder blocks are structurally valid when used.
15. **Tool prerequisites.** Required system tools have setup/verification guidance in the correct reference scope; optional tools remain conditional.
16. **Bundled skills.** If present, skill references and discovery/bundling behavior do not break current ICM expectations; CCA package-locality checks may be reported separately.
17. **Specs as contracts.** Specification stages define WHAT/WHEN and leave implementation HOW to the build stage where applicable.
18. **Checkpoints.** Creative stages include at least one valid checkpoint; checkpoint step references resolve.
19. **Audits.** Creative/build stages include specific pass/fail audit checks after process execution and before writing output where applicable.
20. **Value validation.** Content-producing stages define and lock relevant value criteria where the current ICM pattern applies.
21. **Docs over outputs.** Reference docs remain authoritative for quality/build rules; old outputs are not treated as pattern libraries.
22. **Shared constants.** Code-producing workspaces centralize configurable shared values when applicable.
23. **Quality guardrails.** Enforce current ICM size/readability/formatting guardrails, including CONTEXT/reference size limits and ICM-specific text style rules.
24. **End-to-end validation.** A generated workspace should pass the equivalent of the current workspace-builder validation stage and complete at least one representative run before being called ready when that claim is being made.

If only ICM-derived stage patterns are present, report whether those borrowed patterns are internally valid, but mark **ICM native compatibility: N/A** unless the full profile is actually claimed and present.

CCA-only wiki metadata and outer method organization are irrelevant to the native ICM profile unless they break the nested ICM boundary.

## 4. LLM Wiki native compatibility checks

Do not require one directory schema. Verify the implementation's own instructions first, then check the core behavior:

1. durable source material/evidence exists or has a defined home;
2. maintained synthesis persists across sessions;
3. there is an explicit maintenance procedure for integrating/querying knowledge;
4. the knowledge base is directly inspectable/editable as files;
5. the implementation's own links/index/schema resolve and are internally coherent.

Missing CCA frontmatter, `raw/`, `wiki/`, `wiki/index.md`, `log.md`, entity/concept subdirectories, or CCA log syntax are **not** native LLM Wiki failures.

## 5. Method-overlay preservation

PARA, Zettelkasten, BASB/CODE, and similar methods are not native CCA lint profiles.

When a workspace explicitly declares such a method, lint may report whether CCA changes preserve its locally observable/declared boundaries. Examples:

- an outer PARA tree still distinguishes Projects, Areas, Resources, and Archives where the workspace relies on those categories;
- a nested native ICM root has not been flattened or rewritten by outer organization;
- Zettelkasten notes have not been silently reclassified as agent-writable maintained synthesis without authority;
- BASB/CODE terminology is not misrepresented as a structural filesystem requirement.

Report these as **method-preservation findings**, not upstream/native compatibility certification.

## 6. CCA conformance checks

Only apply requirements the workspace intentionally adopted. Examples include:

- portable `AGENTS.md` routing;
- CCA file-role classifications;
- a CCA-hardened knowledge bundle;
- provenance/lifecycle metadata;
- CCA maintenance history conventions;
- the fresh-agent walk test.

Report optional hardening recommendations separately from errors.

## 7. Agent Skills checks

When a `skills/` directory exists, validate each bundled skill package:

- `SKILL.md` exists;
- frontmatter contains valid `name` and `description`;
- directory name and skill name agree;
- name uses lowercase letters, digits, and hyphens and remains within the current Agent Skills limits;
- description states purpose and trigger conditions and remains within the current limits;
- implementation resources referenced by file path are relative and remain inside the skill package;
- no skill reaches into a sibling skill directory or repository-global implementation file by relative path;
- semantic delegation to another installed capability by skill name is allowed;
- detailed resources are progressively disclosed rather than copied wholesale into `SKILL.md`.

Do not fail a CCA skill merely because another suite capability is named as the correct next operation. Package locality and semantic capability composition are separate concerns.

## 8. History and append-only claims

A filesystem snapshot alone cannot prove that a file has never been rewritten.

- Validate current log syntax only if the active profile defines one.
- Claim append-only history only when version-control/history evidence is actually available and inspected.
- Otherwise report history immutability as **not verified**, not passed.

## 9. Repairs

Default lint behavior is report-only unless the user asked for remediation.

When remediation is authorized, automatically repair only changes whose intent is unambiguous, such as a catalog path that clearly points to a uniquely renamed file. Do not automatically:

- delete files;
- resolve semantic contradictions;
- rename an upstream-native structure into a CCA preference;
- flatten a method overlay or nested native boundary;
- merge competing instruction files without reviewing unique content;
- fabricate missing provenance or metadata.

## Report format

```text
# Lint report — [workspace]

Profiles detected:
- ICM native compatibility: PASS | FAIL | N/A
- ICM-derived patterns: PASS | FAIL | N/A
- LLM Wiki native compatibility: PASS | FAIL | N/A
- CCA conformance: PASS | PARTIAL | N/A
Method overlays detected: [list or none]

## Compatibility errors
[Issues that break a claimed upstream/native profile]

## CCA conformance errors
[Only requirements intentionally adopted by this workspace]

## Method-preservation findings
[Only locally declared/observable overlay constraints; not native certification]

## Hardening opportunities
[Optional improvements, never presented as upstream failures]

## Verification limits
[Checks that could not be proven from available evidence]

## Repairs applied
[Only if explicitly authorized]
```

## Production rule

A clean lint report means the workspace satisfies the profile it claims within the evidence inspected. The CCA walk test supplements profile-specific validation; it does not replace ICM acceptance or another upstream's stricter rules.
