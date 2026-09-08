# Compatibility: upstreams ↔ CCA

Normative companion to [`spec.md`](spec.md). This document defines compatibility boundaries. CCA preserves upstream authority before applying CCA-specific semantics or hardening. Method-overlay composition is additionally governed by [`method-composition.md`](method-composition.md).

## 1. Compatibility principle

CCA uses five distinct terms:

- **Upstream-native** — the boundary satisfies the applicable upstream system according to that upstream's own current authority and acceptance rules.
- **CCA-compatible** — CCA can resolve and operate on the boundary's semantics without structural migration or semantic replacement.
- **CCA-conformant** — the boundary intentionally adopts CCA's normative interoperability contract.
- **Profile-conformant** — the boundary satisfies a named optional CCA-owned profile.
- **CCA-hardened** — optional CCA routing, portability, provenance, validation, or maintenance capabilities were added without invalidating existing native semantics.

These dimensions are composable, not a maturity ladder. An upstream-native workspace need not adopt CCA in order to be CCA-compatible.

A valid native ICM workspace is CCA-compatible because CCA resolves its native semantics without structural migration through:

```text
boundary + semantic role -> binding
```

That statement does **not** make ICM a CCA-owned profile and does not transfer authority over ICM semantics to CCA. ICM remains ICM; CCA owns only its mapping and interoperability behavior.

Likewise, a legitimate LLM Wiki implementation may be CCA-compatible without becoming CCA-conformant.

CCA distinguishes an upstream-native boundary from derived use of upstream patterns. Borrowing part of a convention does not justify claiming upstream-native conformance.

PARA, Zettelkasten, BASB/CODE, and similar human methods are method overlays unless a concrete upstream or CCA profile explicitly defines a machine-facing conformance surface for them.

## 2. Mapping rule

CCA maps semantics; it does not normalize upstreams into one filesystem tree.

```text
upstream/native semantic
        ↓ mapping
CCA boundary + semantic role
        ↓ resolution
local binding
```

Rules:

1. the upstream remains authoritative for the meaning of an upstream-native construct;
2. the CCA semantic role is a stable interoperability address;
3. the binding is the concrete local implementation and may vary where the governing contract allows it;
4. a CCA mapping must not silently redefine or weaken upstream semantics;
5. agents resolve the applicable boundary and role before assuming a concrete path;
6. native-path requirements remain exact when the upstream makes the concrete representation part of conformance.

## 3. Concept mapping

Roles overlap; concrete filenames and paths may differ where the applicable contract permits variation.

| CCA concept | ICM equivalent/default | LLM Wiki analogue |
|---|---|---|
| portable agent guidance | portable `AGENTS.md`; native ICM Layer 0 remains `CLAUDE.md` | implementation-defined schema/instructions |
| `context.router` / workspace routing | Layer 1 `CONTEXT.md` | index/schema-defined navigation |
| local work contract | stage/folder `CONTEXT.md` | ingest/query/maintenance procedure |
| stable factory/reference context | Layer 3 references/configuration | stable schema/conventions |
| working input/product | Layer 4 working artifacts | query/ingest working material |
| preserved evidence | user/source material | durable raw/source material |
| maintained synthesis | no direct ICM equivalent | core LLM Wiki behavior |
| chronicle/history | Git/history or workspace artifact | optional implementation detail |

Semantic overlap is not permission to force identical directory trees or ownership rules.

## 4. ICM compatibility

### 4.1 Upstream-native ICM

CCA recognizes a boundary as **upstream-native: ICM** only when it satisfies the complete applicable current ICM/MWP contract. Upstream ICM `_core/CONVENTIONS.md` is the semantic authority; the upstream workspace-builder validation behavior is the practical acceptance surface for generated workspaces.

A native ICM boundary is also **CCA-compatible** by design. CCA does not require renaming stages, rewriting contracts, replacing `CLAUDE.md`, adding CCA metadata, or structurally migrating the workspace before resolving it.

Native ICM validation includes, where applicable:

1. five-layer routing and the current native Layer-0 entry semantics;
2. root and per-stage `CONTEXT.md` routing using exact upstream filenames;
3. exact `Inputs` / `Process` / `Outputs` stage contracts and current Inputs columns;
4. current naming rules, including zero-padded lowercase-hyphenated stages;
5. per-stage `output/` handoffs and an unbroken handoff chain;
6. cross-reference integrity and an acyclic one-way dependency graph;
7. selective section routing and canonical-source discipline;
8. contract-file purity;
9. current `setup` and `status` trigger behavior, including real-artifact versus placeholder-only completion semantics;
10. current questionnaire, placeholder, conditional-placeholder, tooling, bundled-skill, checkpoint, audit, validation, documentation, shared-constant, size, formatting, and readability requirements where applicable;
11. current restructure move-safety behavior where path-changing work applies: pre-proposal referrer discovery (including sibling-relative paths, symlinks, and bounded known external consumers), case-fold destination collision checks, copy-verify-remove migration discipline, and post-move verification of references expected to survive;
12. current System Map inbound/reverse-walk behavior where that form applies, so known consumers outside the mapped tree are not hidden by an outward-only effects index;
13. workspace-builder-equivalent end-to-end validation before a generated workspace is described as ready.

CCA extensions must be ignorable by an ICM-only consumer. A native ICM root may be nested inside an outer PARA, BASB-guided, coding, client, hybrid, or CCA-conformant workspace; the outer boundary may organize where it lives but must not rewrite native ICM internals merely for uniformity.

### 4.2 ICM-derived patterns

A non-ICM boundary may intentionally borrow ICM constructs such as numbered stages, local contracts, selective Inputs routing, one-way dependencies, output handoffs, or progressive context loading.

That is **ICM-derived**, not upstream-native ICM, unless the complete applicable upstream profile passes.

### 4.3 ICM-derived navigation in optional profiles

A CCA-owned profile may intentionally adopt ICM's cold-agent navigation behaviors without claiming to be native ICM. When such a profile declares this behavior, validate the profile's declared mapping and local contracts rather than pretending the profile is an upstream ICM pipeline.

The CCA Hybrid Workspace Profile does this selectively: stable roles and bindings expose deterministic routing while nested native ICM boundaries remain governed by ICM itself.

### 4.4 Portable `AGENTS.md` with ICM

Adding `AGENTS.md` is optional interoperability hardening. Do not delete, replace, or invalidate native ICM's `CLAUDE.md` merely to make CCA or AGENTS.md appear canonical.

Where both exist:

- preserve substantive guidance in its actual authority;
- use supported include/import behavior where appropriate;
- otherwise keep interoperable counterparts minimal enough to avoid divergent duplicated rules;
- never claim CCA overrides a harness's own instruction-discovery precedence.

## 5. LLM Wiki compatibility

Karpathy's LLM Wiki is explicitly an **idea pattern**, not a fixed conformance standard. Its published core distinguishes immutable raw sources, an LLM-owned maintained wiki, and a schema/instruction document that humans and the LLM co-evolve. It also says implementation details are intentionally domain- and preference-dependent.

CCA compatibility therefore preserves that pattern instead of inventing a universal filesystem certification:

- durable raw/source material remains the evidence layer and is not silently rewritten by the maintainer;
- maintained synthesis persists and compounds across sessions rather than being reconstructed from scratch for every question;
- a local schema/instruction contract tells the maintainer how to ingest, query, and maintain the wiki;
- the filesystem-native result remains directly inspectable by the human;
- write ownership follows the local LLM Wiki implementation/schema rather than a CCA default. The published idea gives the LLM ownership of the wiki layer; a human-editable shared variant is therefore an adaptation unless its local schema explicitly defines that behavior.

CCA may recommend hardening such as stronger indexes, provenance metadata, lifecycle state, trust controls, logs, or integrity checks, but must not attribute those choices to LLM Wiki as mandatory requirements.

## 6. AGENTS.md compatibility

CCA uses `AGENTS.md` because it is an existing open convention.

- Root `AGENTS.md` may provide portable repository/workspace guidance.
- Nested `AGENTS.md` files preserve subtree scope; the closest applicable file wins according to the convention.
- CCA must not flatten nested instructions when doing so destroys scope.
- `AGENTS.md` has no CCA-required heading schema.
- CCA must not claim authority over harness-specific precedence beyond the upstream convention/runtime behavior.

## 7. Agent Skills compatibility and portability

CCA is distributed as **one installable `cca` skill with seven lazily loaded modes**. Every runtime resource required by those modes must remain inside `skills/cca/`.

A valid package keeps:

- `SKILL.md` activation metadata and routing at the skill root;
- detailed normative/operational material under skill-local `references/`;
- templates, executable tooling, fixtures, and other implementation resources under skill-local `assets/` and/or `scripts/` according to the existing package topology;
- no runtime dependency on repository-global `docs/`, examples, publications, sibling skills, or a fixed installation path.

Repository documentation may elaborate, illustrate, research, or publish CCA, but must not be the sole authority for semantics or behavior required by the installed skill.

## 8. CCA Hybrid Workspace Profile

The optional Hybrid Workspace Profile is CCA-owned, CCA-compatible by construction, and intended to be CCA-conformant/profile-conformant when its declared contracts pass.

It is **not** a new CCA mode and **not** native ICM. Its portable reference implementation is bundled inside the `cca` skill and is governed by [`../architect/hybrid-workspace.md`](../architect/hybrid-workspace.md).

Profile tooling operates on an explicit target workspace. The installed skill/package directory is implementation machinery, never the workspace target.

## 9. Method-overlay compatibility

PARA, Zettelkasten, BASB/CODE, and similar human methods are composed by preserving their boundaries and useful semantics rather than forcing structural equivalence.

Rules:

1. preserve the method's useful local semantics where the workspace declares or clearly uses them;
2. do not invent CCA-only metadata merely to restate obvious filesystem organization;
3. do not imply semantic equivalence where a profile crosswalk maps only a useful subset of an upstream concept;
4. preserve nested upstream-native boundaries even when an outer method organizes them;
5. determine write authority before treating human-authored knowledge as agent-maintained synthesis.

See [`method-composition.md`](method-composition.md).

## 10. Swap guarantees

### Upstream-native ICM → CCA tooling

CCA tooling must resolve and operate on native ICM without structural migration. Optional hardening may add interoperable capabilities, but native ICM remains valid and authoritative.

### LLM Wiki → CCA tooling

CCA tooling must discover the wiki's own schema/instructions before imposing implementation preferences. Optional hardening remains optional. CCA must not silently convert the published LLM-owned wiki layer into shared or human-owned synthesis.

### CCA-conformant → ICM consumer

If a CCA-conformant boundary claims **upstream-native ICM**, it must preserve the complete applicable current ICM acceptance surface so an ICM consumer does not depend on CCA-only semantics.

If it only borrows ICM patterns, it must describe them as ICM-derived or as behavior adopted by a named CCA profile rather than promise native ICM interchangeability.

### CCA maintained-knowledge profile → LLM Wiki pattern

A CCA-owned knowledge profile may be inspired by LLM Wiki without claiming exact LLM Wiki ownership semantics. If it claims LLM Wiki compatibility, document any ownership/authority adaptations explicitly rather than hiding them behind a one-to-one mapping.

## 11. Validation precedence

Validation order is:

1. resolve the current boundary and any upstream-native claim;
2. validate upstream-native claims against their current upstream authority;
3. resolve CCA semantic roles and bindings without requiring structural migration;
4. preserve declared method overlays without promoting them to native profiles;
5. validate intentionally adopted CCA conformance;
6. validate any named CCA profile contract;
7. run supplemental fresh-agent/portability checks;
8. report optional hardening separately.

A successful CCA walk test never waives a failed upstream-native acceptance check.

## 12. Upstream evolution

CCA is deliberately evolvable.

- CCA **MUST** update or explicitly version/pin a compatibility mapping when a supported upstream changes in a way that affects a compatibility claim.
- CCA **SHOULD** converge toward an upstream approach that demonstrates a materially better solution to the same problem, provided the change does not violate CCA's core principles.
- CCA **MUST NOT** preserve an inferior CCA-specific convention merely because CCA introduced it first.
- Upstream changes are verified from primary authority before compatibility semantics are changed.

This rule applies to ICM, LLM Wiki, AGENTS.md, Agent Skills, and future supported upstreams. CCA remains agent-, vendor-, runtime-, and concrete-path-agnostic while it evolves.
