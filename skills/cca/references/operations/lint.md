# Lint mode

Validate the target it actually is. Do not fail upstream systems for omitting CCA conventions they never adopted, and do not invent native profiles for human methods that do not define one.

Lint is claim validation, not a substitute for a workspace architecture audit. If the user asks whether a repository/workspace's context, routing, navigation, authority, or context efficiency is well designed, route the compound request through Architect Audit mode and use lint only for the claim-validation portion.

## 1. Detect claims, target, and boundaries

Record the requested boundary before inspecting descendants. Determine applicable claims from durable files/instructions:

- **upstream-native ICM**;
- **ICM-derived patterns**;
- **LLM Wiki-style maintained-knowledge compatibility**;
- **CCA-compatible**;
- **CCA-conformant**;
- **CCA Hybrid Workspace Profile-conformant**;
- **CCA-hardened**;
- ordinary project/workspace with portable agent guidance.

Also detect method overlays where declared or structurally clear, such as PARA, Zettelkasten, or BASB/CODE. Treat them as preservation/context boundaries rather than inventing structural certification.

Report the **requested boundary**, **inspected boundaries**, and any excluded/unresolved boundaries. A pass for one inspected child establishes only that child's result; it must not be promoted into a parent/workspace pass.

If detection is ambiguous, report the ambiguity. Do not silently choose the strictest claim.

A missing explicit CCA contract makes `CCA-conformant` N/A; it does not make `CCA-compatible` N/A. Evaluate CCA compatibility independently where there is enough evidence to determine whether CCA can resolve and operate on the boundary without structural migration or semantic replacement.

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

Do not add an ICM-shaped structural requirement to this universal set. Navigation requirements come from the active upstream, named profile, or local contract.

**Detached-boundary portability** is normally an architecture/hardening concern, not a new compatibility or conformance claim. If lint encounters an independently addressable boundary whose required routing depends on incidental parent placement, report it as a **hardening opportunity** unless the active contract explicitly requires detached portability. If a referenced path is already broken in the inspected target, or an adopted contract requires standalone/detached behavior, validate that as an applicable failure instead of downgrading it to advice.

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

## 4. ICM-derived checks

A non-native boundary may borrow ICM stages, local contracts, selective routing, one-way dependencies, progressive disclosure, or handoffs. Validate only the constructs actually adopted.

Do not require every CCA-compatible workspace to look like an ICM pipeline. If a named CCA-owned profile explicitly adopts ICM-style cold-agent navigation, validate that profile's own declared mapping/acceptance rather than promoting it to native ICM.

## 5. LLM Wiki-style maintained knowledge

Do not require one directory schema. When a boundary intentionally uses this pattern, read the implementation's own instructions first, then verify the behavior it actually claims, such as:

1. durable source/evidence exists or has a defined home;
2. maintained synthesis persists across sessions;
3. maintenance behavior for integrating/querying knowledge exists;
4. humans can inspect/edit the knowledge base directly as files;
5. the implementation's own navigation/schema resolves coherently.

Missing CCA-preferred paths/metadata are not failures unless the implementation explicitly adopted them.

## 6. Method-overlay preservation

PARA, Zettelkasten, BASB/CODE, and similar methods are not automatically CCA lint profiles.

When declared, lint MAY report whether CCA changes preserve their locally observable semantics and boundaries. Examples:

- an organizational PARA boundary still preserves the categories the workspace actually relies on;
- nested upstream-native systems have not been flattened by outer organization;
- Zettelkasten/human notes have not been silently reclassified as agent-writable synthesis;
- BASB/CODE terminology is not misrepresented as a mandatory filesystem taxonomy;
- PARA `Resources` has not been treated as synonymous with preserved raw/reference evidence.

Report these as method-preservation findings, not invented native certification.

## 7. CCA conformance

Apply only intentionally adopted CCA requirements. Validate:

- explicit boundary/authority semantics where the adopted contract needs them;
- stable semantic role/key resolution;
- configurable bindings where the governing contract permits them;
- no semantic identity hidden in a default path;
- one-fact-one-home / adapter locality;
- installed-skill portability where CCA-owned runtime behavior is used;
- applicable provenance/lifecycle/maintenance contracts;
- supplemental fresh-agent walkability where claimed.

Report optional hardening separately from conformance errors.

## 8. CCA Hybrid Workspace Profile

Load `../architect/hybrid-workspace.md` when the target matches the current bundled **v2** profile. V2 preserves all frozen-v1 semantics and adds only two admission classifications beneath `knowledge.reference`.

Use the skill-local reference implementation on an **explicit target**:

```bash
python <cca-skill>/assets/hybrid-workspace/audit.py --target <workspace>
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --check
```

For release-grade/self-test verification:

```bash
python <cca-skill>/assets/hybrid-workspace/audit.py --target <workspace> --self-test
```

Profile checks include:

1. frozen-v1 semantic-key/policy/authority baseline plus the v2 extension contract passes;
2. unsafe/escaping bindings and generated destinations are rejected after symlink resolution;
3. effective permissions remain intersections rather than a single-axis grant;
4. archive identity/trust/promotion invariants pass;
5. required generated **semantic outputs** agree with current bindings and profile semantics;
6. `AGENTS.md` satisfies the human-authored `workspace-contract:v2` control contract;
7. non-breaking binding moves propagate to generated consumers;
8. `context.router` generation follows its current binding rather than treating literal `CONTEXT.md` as identity;
9. moving `_state/`, `_runtime/`, `20-sources/`, or another default does not leak obsolete default paths into generated artifacts;
10. the tooling leaves the installed package untouched and writes/checks only the explicit target;
11. local routing/indexing remains boundary-scoped as large collections grow rather than requiring one root manifest;
12. `reference.curated` and `reference.collected` both compose with semantic role `knowledge.reference`;
13. filesystem mutation policy resolves from the most-specific source-class binding so parent permissions cannot widen/narrow the wrong child;
14. no loose source object exists directly under the parent `knowledge.reference` binding;
15. collected source objects preserve required acquisition provenance and content identity/hash;
16. collected sources remain collected after review; review metadata never rewrites admission provenance;
17. existing curated and collected sources are immutable to normal agent operation;
18. agent-generated synthesis routes to `knowledge.durable`, external deliverables remain `output.artifact`, and finite research work remains `work.project`.

When the bundled Python reference implementation owns an artifact, `generate.py --check` additionally performs its canonical byte-for-byte drift check. Do not treat Python rendering details as the only possible implementation of the profile; an independent implementation must satisfy the normative semantic/artifact contract in `../architect/hybrid-workspace.md`.

Do not "repair" a failed frozen semantic/policy field by treating it as a binding customization. Semantic/key changes follow the profile's evolution/version contract.

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
- For collected source files, a matching content hash verifies current content identity against recorded acquisition metadata; it does not by itself prove the entire historical custody chain.

## 11. Repairs

Default lint behavior is report-only unless remediation is requested.

When remediation is authorized, automatically repair only unambiguous issues. Do not automatically:

- delete files;
- resolve semantic contradictions by guessing;
- rename an upstream-native structure into a CCA preference;
- flatten a method overlay or nested native boundary;
- merge competing instruction authorities without reviewing unique content;
- fabricate provenance/metadata;
- move collected evidence to curated because a human reviewed it;
- reset a Hybrid Workspace Profile target from bundled templates over human-authored control files.

## Report format

```text
# Lint report — [target]

Scope:
- Requested boundary: [target]
- Inspected boundaries: [list]
- Excluded/unresolved boundaries: [list | none]

Claims/boundaries detected:
- Upstream-native ICM: PASS | FAIL | N/A
- ICM-derived patterns: PASS | FAIL | N/A
- LLM Wiki-style maintained knowledge: PASS | FAIL | N/A
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
[Optional improvements, including detached-boundary portability/outward-coupling findings when they are not contract failures]

## Verification limits
[What available evidence cannot prove]

## Repairs applied
[Only if authorized]
```

## Production rule

A clean lint report means the inspected boundaries satisfy the claims checked within the evidence inspected. It does not promote uninspected parent boundaries to PASS. CCA compatibility/conformance and the fresh-agent walk test never waive a failed upstream-native acceptance check.

Lint success does not certify architecture quality. For workspace/context architecture quality, use Architect Audit mode and preserve the requested parent/workspace boundary through completion.