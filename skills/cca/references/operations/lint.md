# Lint mode

Validate the target it actually is. Do not fail upstream systems for omitting CCA conventions they never adopted, and do not invent native profiles for human methods that do not define one.

## 1. Detect claims and boundaries

Determine applicable claims from durable files/instructions:

- **upstream-native ICM**;
- **ICM-derived patterns**;
- **LLM Wiki compatibility**;
- **CCA-compatible**;
- **CCA-conformant**;
- **CCA Hybrid Workspace Profile-conformant**;
- **CCA-hardened**;
- ordinary project/workspace with portable agent guidance.

Also detect method overlays where declared or structurally clear, such as PARA, Zettelkasten, or BASB/CODE. Treat them as preservation/context boundaries rather than inventing structural certification.

If detection is ambiguous, report the ambiguity. Do not silently choose the strictest claim.

## 2. Universal structural checks

Where relevant:

- resolve the current boundary before applying rules;
- referenced bindings/paths resolve;
- CCA operations resolve `boundary + semantic role -> binding` rather than treating defaults as identity;
- canonical rules are not duplicated into divergent authoritative copies;
- routing files route rather than accumulate unrelated payload;
- nested instruction scopes remain scoped;
- native/method boundaries remain identifiable;
- adapters do not contradict canonical guidance;
- files required by an explicitly adopted contract exist;
- installed CCA skill resources do not depend on repository-global runtime files.

## 3. Upstream-native ICM checks

When a boundary claims native ICM/MWP, validate the complete applicable **current upstream profile**, not only stage-folder syntax. Treat upstream ICM `_core/CONVENTIONS.md` and the applicable workspace-builder validation behavior as the authority.

At minimum verify, where applicable:

1. five-layer routing and current native Layer-0 semantics;
2. root and per-stage `CONTEXT.md` routing using exact upstream-native filenames;
3. exact `Inputs` / `Process` / `Outputs` contracts and current Inputs columns;
4. contract purity;
5. current file/folder/stage naming and intentionally empty persistent-folder rules;
6. per-stage `output/` handoffs and an unbroken handoff chain;
7. referenced-input integrity;
8. an acyclic one-way dependency graph;
9. selective section routing;
10. canonical-source discipline;
11. current `setup` trigger behavior;
12. current `status` trigger behavior/presentation;
13. current onboarding/questionnaire behavior;
14. complete placeholder/conditional-placeholder coverage where used;
15. required-tool setup/verification guidance;
16. bundled-skill behavior where applicable;
17. specification-stage WHAT/WHEN discipline where applicable;
18. checkpoints in applicable creative stages;
19. audits in applicable creative/build stages;
20. value validation where applicable;
21. docs-over-outputs discipline;
22. shared constants where applicable;
23. current size/readability/formatting quality guardrails;
24. workspace-builder-equivalent end-to-end validation before a generated workspace is described as ready.

A valid upstream-native ICM boundary is **CCA-compatible** without requiring structural migration or CCA metadata. If only ICM-derived patterns are present, report those patterns separately and mark upstream-native ICM `N/A` unless the full native claim is actually present.

## 4. ICM-derived / ICM-navigation checks

A non-native boundary may borrow ICM stages, local contracts, selective routing, one-way dependencies, progressive disclosure, or handoffs. Validate only the constructs actually adopted.

Do not require every CCA-compatible workspace to look like an ICM pipeline. If a named CCA-owned profile explicitly adopts ICM-style cold-agent navigation, validate that profile's own declared mapping/acceptance rather than promoting it to native ICM.

## 5. LLM Wiki compatibility

Do not require one directory schema. Read the implementation's own instructions first, then verify core behavior:

1. durable source/evidence exists or has a defined home;
2. maintained synthesis persists across sessions;
3. maintenance behavior for integrating/querying knowledge exists;
4. humans can inspect/edit the knowledge base directly as files;
5. the implementation's own navigation/schema resolves coherently.

Missing CCA-preferred paths/metadata are not LLM Wiki compatibility failures unless the implementation explicitly adopted them.

## 6. Method-overlay preservation

PARA, Zettelkasten, BASB/CODE, and similar methods are not automatically CCA lint profiles.

When declared, lint MAY report whether CCA changes preserve their locally observable semantics and boundaries. Examples:

- an organizational PARA boundary still preserves the categories the workspace actually relies on;
- nested upstream-native systems have not been flattened by outer organization;
- Zettelkasten/human notes have not been silently reclassified as agent-writable synthesis;
- BASB/CODE terminology is not misrepresented as a mandatory filesystem taxonomy.

Report these as method-preservation findings, not invented native certification.

## 7. CCA conformance

Apply only intentionally adopted CCA requirements. Validate:

- explicit boundary/authority semantics;
- stable semantic role/key resolution;
- configurable bindings where the governing contract permits them;
- no semantic identity hidden in a default path;
- one-fact-one-home / adapter locality;
- installed-skill portability where CCA-owned runtime behavior is used;
- applicable provenance/lifecycle/maintenance contracts;
- supplemental fresh-agent walkability where claimed.

Report optional hardening separately from conformance errors.

## 8. CCA Hybrid Workspace Profile

Load `../architect/hybrid-workspace.md` when the target matches the bundled frozen-v1 profile.

Use the skill-local implementation on an **explicit target**:

```bash
python <cca-skill>/assets/hybrid-workspace/audit.py --target <workspace>
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --check
```

For release-grade/self-test verification:

```bash
python <cca-skill>/assets/hybrid-workspace/audit.py --target <workspace> --self-test
```

Profile checks include:

1. frozen semantic-key/policy/authority contract passes;
2. unsafe/escaping bindings are rejected;
3. effective permissions remain intersections rather than a single-axis grant;
4. archive identity/trust/promotion invariants pass;
5. generated artifacts match canonical render;
6. `AGENTS.md` satisfies the human-authored profile control contract;
7. non-breaking binding moves propagate to generated consumers;
8. `context.router` generation follows its current binding rather than literal `CONTEXT.md`;
9. moving `_state/`, `_runtime/`, or another default does not leak obsolete default paths into generated artifacts;
10. the tooling leaves the installed package untouched and writes/checks only the explicit target.

Do not "repair" a failed frozen semantic/policy field by treating it as a binding customization. Semantic changes follow the profile's evolution/version contract.

## 9. Agent Skills checks

When validating Agent Skills packages:

- `SKILL.md` exists with valid current-standard frontmatter;
- directory and skill name agree;
- detailed resources are progressively disclosed;
- implementation resources remain inside the package;
- no runtime dependency escapes into sibling skills or repository-global implementation files;
- semantic delegation to another capability/mode is distinct from a filesystem dependency.

For CCA itself, verify that everything required to understand/operate advertised installed behavior exists under `skills/cca/`.

## 10. History and append-only claims

A filesystem snapshot alone cannot prove historical immutability.

- Validate current syntax only where the active contract defines it.
- Claim append-only history only when relevant history/version evidence is available and inspected.
- Otherwise report immutability history as **not verified**.

## 11. Repairs

Default lint behavior is report-only unless remediation is requested.

When remediation is authorized, automatically repair only unambiguous issues. Do not automatically:

- delete files;
- resolve semantic contradictions by guessing;
- rename an upstream-native structure into a CCA preference;
- flatten a method overlay or nested native boundary;
- merge competing instruction authorities without reviewing unique content;
- fabricate provenance/metadata;
- reset a Hybrid Workspace Profile target from bundled templates over human-authored control files.

## Report format

```text
# Lint report — [target]

Claims/boundaries detected:
- Upstream-native ICM: PASS | FAIL | N/A
- ICM-derived patterns: PASS | FAIL | N/A
- LLM Wiki compatibility: PASS | FAIL | N/A
- CCA-compatible: PASS | FAIL | N/A
- CCA-conformant: PASS | PARTIAL | FAIL | N/A
- Profile-conformant (name): PASS | FAIL | N/A
- CCA-hardened: [present capabilities | none]
- Method overlays: [list | none]

## Upstream compatibility errors
[Only failures against a claimed upstream authority]

## CCA conformance errors
[Only intentionally adopted CCA requirements]

## Profile conformance errors
[Only named CCA profile requirements]

## Method-preservation findings
[Declared/observable overlay findings; not native certification]

## Hardening opportunities
[Optional improvements]

## Verification limits
[What available evidence cannot prove]

## Repairs applied
[Only if authorized]
```

## Production rule

A clean lint report means the target satisfies the claims checked within the evidence inspected. CCA compatibility/conformance and the fresh-agent walk test never waive a failed upstream-native acceptance check.
