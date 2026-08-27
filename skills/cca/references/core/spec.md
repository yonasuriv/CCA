# CCA Specification

**Version 1.1.1** — Status: Stable, tracking ICM, LLM Wiki, AGENTS.md, Agent Skills, and other directly supported upstreams.

Normative. CCA runtime behavior and CCA-conformant examples must conform to this document. Contract identity and SemVer evolution are governed by [`versioning.md`](versioning.md); compatibility details by [`compatibility.md`](compatibility.md); method composition by [`method-composition.md`](method-composition.md).

The key words **MUST**, **SHOULD**, and **MAY** are interpreted as in RFC 2119.

## 1. What CCA is

Convergent Context Architecture (CCA) is an evolving, agent-agnostic interoperability architecture for filesystem-native AI context. It helps humans and AI agents understand, navigate, and operate across workspaces, projects, and bodies of knowledge by defining stable semantic roles, scoped boundaries, and configurable bindings that preserve meaning even when their concrete paths or implementations change.

CCA bridges human knowledge work and agentic work without forcing existing systems into a new competing convention. It builds on open standards, ecosystem conventions, established methodologies, protocols and frameworks, and software-engineering principles and fundamentals.

Its objective is augmentation:

> **Automation is the means; augmenting human capabilities is the goal.**

CCA SHOULD prefer designs that increase human agency, comprehension, portability, and effective capability while reducing unnecessary human effort and machine work.

CCA currently builds strongly on:

- **ICM / Model Workspace Protocol** for filesystem-native routing, layered context, progressive disclosure, local work contracts, canonical sources, one-way dependencies, handoffs, and human review;
- **LLM Wiki** for persistent maintained synthesis that compounds across sessions;
- **AGENTS.md** for portable agent guidance;
- **Agent Skills (`SKILL.md`)** for portable progressively disclosed capabilities.

CCA may compose with human knowledge-work and delivery methods such as PARA, Zettelkasten, BASB/CODE, Scrum, Kanban, and others without absorbing or redefining them.

## 2. Core principle: convergence over invention

CCA MUST preserve an upstream's native semantics and authority when claiming compatibility with it.

CCA MAY add semantics where upstreams leave implementation open, but MUST NOT:

1. redefine an upstream convention while claiming the result is the same upstream contract;
2. make a CCA-specific choice appear mandatory for upstream compatibility;
3. require a proprietary runtime, database, vendor, model, or harness to understand CCA's durable semantics;
4. duplicate canonical rules across adapters, catalogs, or documentation authorities;
5. force a pipeline, wiki, database, agent framework, organizational taxonomy, or universal directory tree where the work does not need one;
6. preserve an inferior CCA-specific convention merely because CCA introduced it first.

### 2.1 Upstream-change rule

CCA is deliberately evolvable.

- CCA **MUST** update or explicitly version/pin a compatibility mapping when a supported upstream changes in a way that affects a compatibility claim.
- CCA **SHOULD** converge toward an upstream approach that demonstrates a materially better solution to the same problem, provided the change does not violate CCA's core principles.
- Upstream changes MUST be verified against the applicable primary authority before compatibility semantics are changed.

CCA therefore treats current upstream methods as authorities to interoperate with, not dependencies to fork and freeze.

## 3. Semantic resolution model

The primary CCA resolution primitive is:

```text
boundary + semantic role -> binding
```

The parts are distinct:

- **boundary** — the scope whose authority, context, and policies apply;
- **semantic role/key** — the stable meaning being requested;
- **binding** — the concrete workspace-local file, directory, adapter, or implementation that currently fulfills that role.

A path is an implementation detail unless the governing upstream/profile explicitly makes the path part of conformance.

For example:

```text
workspace::state.current -> _state/NOW.md
```

and:

```text
workspace::state.current -> today.md
```

may carry the same CCA semantic identity under contracts that allow binding relocation.

A nested boundary may independently resolve the same role:

```text
project/cca::context.router -> CONTEXT.md
project/foo::context.router -> ROUTER.md
```

Consumers MUST resolve the applicable boundary and semantic role before assuming a binding. Native upstream requirements override CCA defaults when a native claim makes the concrete representation normative.

### 3.1 Agnosticism

CCA semantic identity MUST NOT depend on a particular:

- vendor;
- model;
- agent runtime or harness;
- application;
- database/retrieval engine;
- operating-system-specific absolute path;
- CCA installation path;
- default folder name.

Adapters MAY translate CCA semantics for specific hosts without becoming the semantic authority.

## 4. Compatibility vocabulary

CCA distinguishes five composable claims:

- **Upstream-native** — conforms to an upstream according to that upstream's own current authority.
- **CCA-compatible** — CCA can resolve and operate on the boundary without structural migration or semantic replacement.
- **CCA-conformant** — explicitly adopts this normative CCA interoperability contract.
- **Profile-conformant** — satisfies a named optional CCA-owned profile.
- **CCA-hardened** — optional CCA capabilities were added without invalidating native semantics.

A valid native ICM workspace is CCA-compatible because CCA resolves its native semantics without structural migration through the CCA boundary/role/binding model. That does not make ICM CCA-owned or require the workspace to become CCA-conformant.

See [`compatibility.md`](compatibility.md) for acceptance and swap guarantees and [`versioning.md`](versioning.md) for the versioned identity of CCA compatibility/conformance claims.

### 4.1 Compatibility vs architecture quality

Compatibility is not an architecture-quality certification.

Compatibility/conformance lint asks whether a boundary satisfies the claims and contracts that actually apply to it. A workspace architecture audit asks a different question: whether the requested workspace boundary is efficiently understandable, navigable, and operable by humans and agents with clear authority and bounded context loading.

When CCA is asked to audit or review a workspace's context/routing architecture:

- the **requested audit boundary** MUST remain the unit of completion unless the user explicitly narrows scope;
- nested boundaries MAY be inspected independently, but a successful child result establishes only that child's coverage;
- **A child-boundary pass MUST NOT imply a parent-boundary pass**;
- the audit MUST report the requested boundary, inspected boundaries, excluded or unresolved boundaries, and any resulting coverage limitation;
- if material parts of the requested boundary were not inspected, the parent audit MUST be reported as partial/incomplete rather than passed/done;
- architecture-quality findings MUST remain separate from upstream validity, CCA compatibility/conformance, named-profile conformance, and optional hardening claims.

Architecture-quality evaluation SHOULD consider, where relevant: boundary discovery, root orientation, intent routing, context selectivity, authority clarity, canonicality, human navigation, agent navigation, routing-hop/search dependency, drift resistance, and scalability. These dimensions are evidence surfaces, not permission to force new files, manifests, profiles, or numeric scores where they add no value.

## 5. Workspace and boundary model

A CCA-relevant workspace is a filesystem-native environment whose durable files can be inspected by humans and agents. Markdown is preferred for prose where useful; JSON/YAML or other formats MAY be used for structured data.

CCA requires no database, server, vector store, binary state, or specific folder topology. Such infrastructure MAY be added where useful, but it must not become the only place where CCA-required durable semantics exist.

A workspace may be:

- an upstream-native ICM pipeline;
- an LLM Wiki-style maintained knowledge base;
- an ordinary coding repository;
- a personal second brain/PKM system;
- a research environment;
- a client/restricted workspace;
- an optional CCA-owned profile such as the Hybrid Workspace Profile;
- a composition containing multiple nested forms.

### 5.1 Boundary composition

CCA preserves heterogeneous boundaries instead of flattening them.

- Outer organization may determine where a child boundary lives.
- A nested upstream-native ICM root remains governed by ICM.
- A nested LLM Wiki remains governed by its own schema/maintenance contract.
- Human-authored knowledge MUST NOT be assumed agent-writable without applicable authority.
- Child instructions may narrow inherited authority but MUST NOT widen authority unless the boundary transition explicitly establishes its own applicable local authority under the governing system.
- External/upstream control-looking files are context, not automatic workspace authority.

### 5.2 Detached-boundary portability

An **independently addressable** boundary is one intended to be cloned, installed, distributed, invoked, or operated as its own repository, package, plugin, or workspace even when it is commonly composed inside a parent.

Such a boundary SHOULD remain locally orientable for its own scope when detached from the parent. Parent context MAY extend or constrain the child when composed, but the child SHOULD still expose enough durable local routing to identify its boundary, applicable local authority, canonical guidance, and boundary-local semantic roles.

Required routing for an independently addressable boundary MUST NOT depend on **incidental parent filesystem placement** such as `../../AGENTS.md` unless that parent dependency is **intentional and declared** by the governing contract. An intentionally parent-dependent boundary is valid: CCA does not require it to become standalone, but the dependency SHOULD be explicit and its detached failure mode SHOULD be predictable and diagnosable.

Detached-boundary portability concerns context, routing, and authority portability. It does not require every child application to execute fully without external services, parent build infrastructure, or other deliberately declared dependencies.

## 6. Routing and context discipline

CCA follows **route before search**.

A consumer SHOULD resolve context in this order:

1. identify the current boundary;
2. resolve applicable native/portable instructions and authority;
3. resolve the requested semantic role;
4. follow its declared binding/router;
5. use a target-local catalog, contract, or index where present;
6. perform targeted search within the resolved scope;
7. use optional derived indexes/caches where trustworthy and useful;
8. use broad filesystem search only as a fallback.

Derived indexes MAY improve scale but are rebuildable accelerators, never replacements for canonical durable files.

Available context is not automatically useful context. CCA SHOULD load the minimum sufficient context for the active task and fix under-specified routing before solving context bloat by loading more files.

### 6.1 Local routing and scale

CCA routing is federated by boundary. A root bootstrap/router MUST NOT require one root manifest to enumerate arbitrary descendants merely so the workspace can grow.

As a collection grows, a boundary MAY expose local routers, catalogs, indexes, or search adapters that describe only their own scope. Nested boundaries MAY repeat the same pattern recursively. A consumer should descend through the smallest applicable routing surface before searching the bounded collection.
Derived catalogs, search indexes, embeddings, caches, and graph projections MUST remain rebuildable views over canonical durable state unless a separately declared authority explicitly owns that data. Their loss MUST NOT erase the semantic identity or canonical content they index.

CCA does not prescribe one scale threshold or retrieval engine. At hundreds, tens of thousands, or hundreds of thousands of artifacts, implementations MAY introduce progressively stronger local indexing/search infrastructure while preserving the same boundary/role/binding semantics and avoiding a mandatory universe-wide manifest.

## 7. ICM relationship and profile

ICM currently supplies CCA's strongest filesystem-native navigation foundation. CCA SHOULD use ICM directly where ICM already supplies the better abstraction rather than mint a competing CCA convention.

CCA recognizes:

- **upstream-native ICM** — complete applicable upstream contract passes;
- **ICM-derived patterns** — selected constructs are borrowed without claiming full ICM;
- **CCA-owned profiles adopting ICM navigation behavior** — a CCA profile may use ICM-proven routing principles without becoming native ICM.

### 7.1 Native ICM preservation

When the current boundary is upstream-native ICM:

- preserve native Layer-0 semantics and `CLAUDE.md` where required;
- preserve root and stage `CONTEXT.md` filenames where upstream requires them;
- preserve current stage-contract shape and Inputs columns;
- preserve current naming, output handoffs, one-way dependencies, selective routing, canonical-source rules, setup/status triggers, builder validation, and other applicable upstream requirements;
- do not rename or reinterpret native structure merely to make it resemble a CCA-owned profile;
- portable `AGENTS.md` MAY coexist as interoperability hardening but MUST NOT falsely replace native authority.

The complete current acceptance surface is maintained in [`compatibility.md`](compatibility.md) and must track upstream changes.

### 7.2 ICM-derived usage

A non-ICM boundary MAY borrow numbered stages, local contracts, one-way references, output handoffs, progressive disclosure, or selective input routing. These constructs remain ICM-derived unless the complete applicable upstream profile passes.

### 7.3 Cold-agent walkability

CCA values ICM's cold-agent property: a fresh agent should be able to orient from durable workspace files rather than prior chat memory.

This is a CCA portability objective, not a universal requirement that every CCA-compatible workspace mimic an ICM pipeline.

When a named CCA profile explicitly adopts ICM-style cold-agent behavior, that profile MUST define its own required router/contracts and acceptance surface. The Hybrid Workspace Profile does this through semantic-key bindings and its bundled validation tooling.

## 8. Maintained-knowledge interoperability

CCA can interoperate with the LLM Wiki idea pattern of persistent maintained synthesis over durable source material without making a wiki mandatory for CCA compatibility.

When a boundary uses or claims compatibility with an LLM Wiki-style maintained-knowledge pattern, it SHOULD provide:

1. durable source material/evidence or an explicit durable source home;
2. maintained synthesis that persists across sessions;
3. explicit maintenance behavior for integrating new material and querying existing knowledge;
4. a human-inspectable filesystem representation whose write ownership follows the boundary's own schema/maintenance contract.

CCA hardening MAY add a capture inbox, raw/reference layer, human notes, wiki, index, maintenance log, provenance fields, contradiction tracking, lifecycle state, integrity manifests, or other useful structure. Those are CCA implementation/profile choices unless an upstream explicitly requires them.

### 8.1 Knowledge invariants

When adopted by a workspace:

- synthesis operations SHOULD NOT silently rewrite preserved evidence;
- corrections SHOULD supersede preserved evidence rather than mutate it where provenance matters;
- contradictions SHOULD be represented rather than silently overwritten;
- stale/superseded knowledge SHOULD remain inspectable where history matters;
- indexes SHOULD route rather than duplicate entire page contents;
- human notes MUST NOT be silently reclassified as agent-maintained synthesis.

## 9. File/semantic roles

CCA uses semantic roles as an internal interoperability model, not mandatory directories.

Common roles include:

| Role | Function |
|---|---|
| **catalog/router** | routes to other context with little substantive payload |
| **contract** | defines one unit/folder of work |
| **factory** | stable constraints, references, templates, reusable capability material |
| **source/reference** | preserved evidence/input |
| **synthesis** | maintained derived knowledge |
| **product/output** | working or shipped artifact |
| **chronicle** | historical/maintenance record |
| **state** | current or durable operational state |

A role classification MUST NOT force an upstream workspace to move files solely to match CCA labels.

## 10. Canonical sources and adapters

**One fact, one home.** If the same substantive rule is independently authoritative in multiple files, CCA treats that as drift risk.

Adapters SHOULD point to canonical guidance rather than copy it. A host-specific file MAY contain minimal bootstrap material required by that host, but MUST NOT become a divergent second specification of the workspace.

## 11. Agent Skills distribution contract

CCA is distributed as **one installable `cca` skill with seven lazily loaded modes**:

- `architect`
- `scaffold`
- `sync`
- `ingest`
- `query`
- `lint`
- `advise`

`skills/cca/` is the portable CCA distribution boundary.

Every CCA-owned resource required to understand, resolve, generate, operate, validate, or maintain behavior advertised by the installed skill MUST be available inside that boundary.

Repository-level documentation MAY elaborate, illustrate, cite, research, or publish CCA, but MUST NOT be the sole authority for runtime-required or normative semantics.

The skill package MUST:

- contain a valid `SKILL.md`;
- progressively disclose detailed material through skill-local references/assets/scripts according to the existing package topology;
- keep implementation references inside the skill package;
- avoid runtime dependencies on removed sibling skill packages, repository-global docs/examples, or a fixed installation path;
- preserve architect and advisor reference-domain separation even though they share one package.

## 12. Operations

| Mode | Purpose |
|---|---|
| `architect` | design/map/audit a workspace, preserve existing authority, and coordinate compound composition |
| `scaffold` | add the smallest approved routing/profile layer without unintended restructuring |
| `sync` | reconcile declared routing/bindings/derived artifacts with disk without inventing content |
| `ingest` | integrate new evidence into maintained knowledge under applicable authority |
| `query` | resolve and navigate relevant knowledge/evidence with minimum sufficient context |
| `lint` | validate the actual upstream/CCA/profile claims separately; it does not certify architecture quality |
| `advise` | apply engineering, process, security, autonomy, context, and model judgment without turning priors into enforcement |

Modes describe **what the agent is doing**. Profiles describe **which optional workspace contract it is operating against**. Do not create a new mode merely because a profile has its own schemas/scripts.

## 13. CCA Hybrid Workspace Profile

The optional Hybrid Workspace Profile is defined by [`../architect/hybrid-workspace.md`](../architect/hybrid-workspace.md) and implemented completely inside `skills/cca/assets/hybrid-workspace/`.

The profile:

- is CCA-owned and optional;
- is not a universal CCA directory tree;
- uses stable semantic keys with configurable bindings;
- uses ICM-proven navigation principles where useful without claiming native ICM;
- may contain nested upstream-native boundaries;
- preserves the complete frozen-v1 semantic/policy/authority baseline and its adversarial tests, while the current v2 schema adds only the `reference.curated` and `reference.collected` admission classifications beneath `knowledge.reference` plus the provenance/routing contract required to enforce that distinction;
- requires generation/audit operations to use an explicit **target workspace**;
- MUST NOT materialize a workspace inside the installed skill/tool directory;
- resolves the generated `context.router` artifact through its current binding rather than a hardcoded filename.

The two reference classifications describe **how preserved evidence entered the corpus**, not new semantic knowledge roles. Their detailed current contract is normative for the profile and lives in [`../architect/hybrid-workspace.md`](../architect/hybrid-workspace.md).

## 14. Profile-aware linting

Linting MUST distinguish upstream validity from CCA compatibility/conformance, named profile conformance, and optional hardening.

At minimum `lint` supports:

- upstream-native ICM validation against current ICM;
- ICM-derived pattern checks without falsely promoting the host to native ICM;
- LLM Wiki compatibility behavior without imposing one CCA filesystem schema;
- CCA conformance for explicitly adopted CCA semantics;
- Hybrid Workspace Profile conformance using its bundled audit/generation checks.

A missing optional CCA convention MAY be reported as a hardening opportunity but MUST NOT be reported as an upstream compatibility failure.

## 15. CCA walk test

For intentionally structured CCA-conformant workspaces, the portability walk test is:

> A fresh agent with no prior chat memory can orient, perform a representative operation, and report status using durable workspace files alone.

- **Orient** — identify the boundary, applicable authority/profile, and routed context.
- **Act** — perform one representative operation through resolved semantics/bindings.
- **Report** — state what changed, what was produced, what remains, and what is ambiguous.

If a required decision exists only in chat history or someone's memory, the durable workspace is incomplete.

This test is supplemental; it never substitutes for upstream-native or named-profile acceptance.

## 16. Human + agent operating principle

CCA exists for humans and agents operating on shared knowledge and work.

A human should be able to understand and retain agency over the durable environment. An agent should be able to answer, without broad blind search:

1. Where am I?
2. What governs this boundary?
3. Which semantic role do I need?
4. Where is that role bound here?
5. What is authoritative?
6. What may I read or mutate?
7. What context is sufficient for this operation?
8. Where should durable output/state go?

Human-centric does not mean requiring unnecessary manual toil. Safe automation that preserves provenance, inspectability, override, and authority may increase human agency more than manual repetition.

## 17. Out of scope

CCA is not:

- an agent runtime;
- a real-time multi-agent message bus;
- a replacement for MCP;
- a vector database or retrieval engine;
- a workflow scheduler;
- a replacement for ICM, LLM Wiki, AGENTS.md, Agent Skills, PARA, Zettelkasten, BASB, Scrum, or other upstream systems/methods;
- a requirement to use Markdown for every artifact;
- a universal directory tree;
- a claim that every filesystem-native workspace should look identical.

Real-time tight-loop multi-agent coordination requires appropriate orchestration/message-passing infrastructure. CCA may provide durable shared context beneath such systems but does not replace them.

## 18. Maintenance and evolution

Repository maintainers MUST keep this skill-local specification, [`versioning.md`](versioning.md), [`compatibility.md`](compatibility.md), affected mode references, portable implementation assets, examples, and regression checks consistent when CCA semantics change.

The repository outside `skills/cca/` is a development, research, documentation, publication, and validation environment. It may explain CCA more broadly, but installed-skill meaning must not disappear when the repository is absent.
