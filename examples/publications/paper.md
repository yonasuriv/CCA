# Convergent Context Architecture

> **An Agent-Agnostic Interoperability Architecture for Filesystem-Native AI Context**

| Field | Value |
| --- | --- |
| **Document type** | Whitepaper (non-normative) |
| **Version** | Draft 0.2 |
| **Status** | Working draft; non-normative |
| **Date** | 2026-08-20 |
| **Authors** | Jonathan Di Rico |
| **Normative counterpart** | `skills/cca/references/core/` |
| **License** | MIT |

## Abstract

AI agents increasingly operate directly on ordinary filesystems: code repositories, research corpora, personal knowledge bases, client workspaces, project trees, workflow folders, and durable operational state. Existing methods already solve important parts of that environment. ICM/MWP defines a concrete staged context architecture; LLM Wiki describes persistent LLM-maintained knowledge synthesis; AGENTS.md provides scoped portable instructions; Agent Skills packages reusable capabilities; PARA, BASB/CODE, and Zettelkasten organize human knowledge work in different ways. The unresolved problem is not the absence of another method. It is the absence of a small shared semantic layer for composing independently governed filesystem-native systems without forcing them into one structural convention.

Convergent Context Architecture (CCA) addresses that interoperability problem through three core ideas: **scoped boundaries**, **stable semantic roles**, and **configurable bindings**. A role describes what something means; a binding describes where or how that role is implemented inside a particular boundary. This lets a CCA-aware consumer resolve `boundary + semantic role -> binding` before relying on path names, while upstream-native systems keep their own authority and native structures.

CCA therefore distinguishes five composable claims rather than one maturity ladder: **Upstream-native**, **CCA-compatible**, **CCA-conformant**, **Profile-conformant**, and **CCA-hardened**. Selected upstream patterns may also be described as **ICM-derived** or otherwise source-derived without claiming native conformance. The architecture is intentionally path-agnostic at its core, profile-aware where stronger contracts are useful, and designed so large collections can route through boundary-local catalogs/indexes rather than a single global manifest or broad filesystem grep.

The central claim is deliberately narrow: CCA is useful only if the semantic interoperability layer remains smaller and more durable than the systems it connects. If it becomes a fixed folder tree, a replacement for ICM, a mandatory wiki, a runtime, or another ecosystem island, it has failed its own purpose.

## 1. Introduction

### 1.1 Context has become a filesystem concern

Modern coding agents and general-purpose AI runtimes increasingly receive substantial operating context from files. Repositories may contain instructions, policies, workflow contracts, source material, maintained knowledge, task state, tools, templates, outputs, logs, and nested projects. This shift is useful because plain files are human-readable, diffable, versionable, portable, and compatible with many execution environments.

The filesystem, however, does not carry universal semantics. A directory called `resources/` may mean a PARA Resource shelf, static application assets, external research, or something entirely different. `CONTEXT.md` is a native contract in ICM but may be an arbitrary filename elsewhere. `_state/` may be a useful implementation choice in one profile without being meaningful in another. A nested project may have its own authority that intentionally conflicts with assumptions made by an outer workspace.

The problem therefore becomes semantic resolution rather than merely storage.

### 1.2 The interoperability gap

Existing systems solve different questions:

- ICM/MWP: how a staged filesystem-native workflow routes context and handoffs.
- LLM Wiki: how maintained synthesis can compound over durable sources.
- AGENTS.md: how agent guidance can be scoped through a repository tree.
- Agent Skills: how reusable capabilities can be packaged with progressive disclosure.
- PARA: where actionable material belongs according to horizon of commitment.
- BASB/CODE: how human knowledge moves through capture, organization, distillation, and expression.
- Zettelkasten: how addressable linked ideas develop over time.
- Scrum, Kanban, DevOps, and other delivery approaches: how work is coordinated at their own process scopes.

These systems are not missing because they need to be merged. They are valuable because they remain distinct. The gap appears when several of them coexist and an agent must decide which boundary it is in, which authority governs, what role it needs, where that role is implemented, and what it may change without breaking another system.

### 1.3 Frozen product position

CCA's normative repository defines the product as an evolving, agent-agnostic interoperability architecture for filesystem-native AI context. It aims to bridge human knowledge work and agentic work without forcing existing systems into a new competing convention, while improving efficiency and reducing unnecessary context, compute, usage, operational cost, and technical debt.

This whitepaper does not redefine that statement. It explains the architecture that follows from it.

## 2. Design constraints

CCA is constrained by several rules.

### 2.1 Preservation over replacement

When a supported upstream or established method already owns a semantic domain, that authority is preserved. CCA may map it, route to it, or optionally harden the surrounding workspace, but it must not silently rewrite the upstream while continuing to call the result native.

A native ICM workspace remains ICM. An LLM Wiki implementation remains governed by its own schema. A PARA tree remains PARA organization rather than a disguised CCA taxonomy. Agent Skills remain Agent Skills rather than becoming CCA modules.

### 2.2 Stable meaning over stable paths

CCA's primary resolution primitive is:

```text
boundary + semantic role -> binding
```

For example:

```text
workspace::state.current -> _state/NOW.md
```

may later become:

```text
workspace::state.current -> today.md
```

without changing the semantic role, provided the governing profile/contract allows relocation.

Likewise:

```text
project/cca::context.router -> CONTEXT.md
project/example::context.router -> ROUTER.md
```

can coexist because the path is not the identity. Native upstream requirements are the exception: if an upstream makes a concrete filename part of conformance, CCA preserves it inside that upstream-native boundary.

### 2.3 Boundaries before taxonomy

A boundary identifies the scope whose authority and local semantics apply. Boundaries can nest. A personal workspace may contain a normal code repository, an upstream-native ICM client workflow, a maintained knowledge base, and human notes. CCA should not flatten these merely to obtain one uniform tree.

Boundary composition is therefore more important than choosing one repository-wide taxonomy.

### 2.4 Automation in service of augmentation

CCA treats automation as implementation machinery rather than the product objective. The durable environment should increase a human's ability to understand, direct, inspect, recover, and reuse work. Derived indexes, generators, agents, or automation should not make the human-owned context less legible or less portable.

## 3. Relationship to upstream systems

### 3.1 ICM / Model Workspace Protocol

Current upstream ICM/MWP defines a concrete five-layer routing architecture. Layer 0 is native `CLAUDE.md`; Layer 1 is root `CONTEXT.md`; Layer 2 is stage `CONTEXT.md`; Layer 3 contains stable reference/factory material; Layer 4 contains per-run working/product artifacts. It also defines exact stage contract structure, output-folder handoffs, one-way references, selective section loading, canonical sources, setup/status behavior, and current quality rules.

CCA preserves those rules when a boundary claims **Upstream-native ICM**. It does not rename native files to fit a CCA preference and does not replace `CLAUDE.md` with `AGENTS.md` merely to appear more portable.

A non-native boundary may borrow selected ICM ideas such as local contracts, stages, one-way dependencies, handoffs, or progressive disclosure. That usage is **ICM-derived**. It does not make every CCA workspace an ICM skeleton, and it does not make an optional CCA profile native ICM.

This distinction prevents an important failure mode: taking the strongest upstream influence on CCA and accidentally turning it into a universal CCA requirement.

### 3.2 LLM Wiki

Karpathy's LLM Wiki is an intentionally abstract idea pattern. Its published architecture separates immutable raw sources, an LLM-owned maintained wiki, and a schema/instruction document that defines how the maintainer operates. The concrete directory structure and tooling are intentionally left to the implementation.

CCA therefore treats LLM Wiki as a source of a maintained-knowledge pattern rather than a fixed filesystem certification. A boundary that uses the idea should preserve the distinction between durable evidence and persistent synthesis, but CCA must not attribute its own capture folders, provenance fields, lifecycle metadata, or shared human/agent write policies to LLM Wiki.

If a CCA profile uses shared human/agent synthesis instead of an LLM-owned wiki, that is an explicit adaptation rather than a silent claim about upstream semantics.

### 3.3 AGENTS.md

AGENTS.md provides repository-scoped instructions for compatible agents. CCA uses it as an existing convention rather than defining a competing agent-instruction filename. Nested instruction scope must remain intact. CCA does not prescribe a universal heading schema for AGENTS.md and does not claim that AGENTS.md replaces harness-specific native files when another system requires them.

### 3.4 Agent Skills

CCA ships as one Agent Skill named `cca`. Detailed behavior is progressively disclosed through skill-local references and assets. The package exposes seven lazy modes: `architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`, and `advise`.

The distribution boundary is `skills/cca/`. Runtime behavior must not depend on repository-global docs or removed sibling packages. Architect, operations, core specification, and advisor material remain distinct domains inside the package even though they share one installable skill.

### 3.5 Human knowledge-work methods

PARA, BASB/CODE, and Zettelkasten are not machine-facing CCA profiles.

PARA organizes according to actionability. BASB/CODE provides a human lifecycle lens. Zettelkasten develops addressable linked ideas. CCA may route across these structures, but it does not reinterpret them as semantic-role schemas.

This matters particularly for PARA `Resources`. A Resource is an organizational category and may contain a book, raw source, dataset, personal note, maintained synthesis, or nested workspace. It is therefore not equivalent to a CCA `knowledge.reference` role. Organizational shelves and epistemic roles are separate axes.

## 4. Compatibility model

CCA uses five independent, composable claims.

| Claim | Meaning |
| --- | --- |
| **Upstream-native** | The boundary satisfies an upstream according to that upstream's current authority. |
| **CCA-compatible** | CCA can resolve and operate the boundary without structural migration or semantic replacement. |
| **CCA-conformant** | The boundary intentionally adopts CCA's normative interoperability semantics. |
| **Profile-conformant** | The boundary satisfies a named optional CCA-owned profile. |
| **CCA-hardened** | Optional CCA capabilities were added without invalidating native semantics. |

These claims are not sequential states. A native ICM workspace can be Upstream-native and CCA-compatible while not being CCA-conformant. A custom workspace can be CCA-conformant without adopting the Hybrid Workspace Profile. A profile-conformant target can contain nested upstream-native boundaries.

Derived-pattern labels such as **ICM-derived** provide provenance and prevent partial adoption from masquerading as upstream conformance.

## 5. The semantic interoperability model

### 5.1 Boundary

A boundary is the scope at which authority and semantics are resolved. Examples include a repository root, a nested project, a client workspace, a native ICM root, a knowledge base, or a restricted subtree.

### 5.2 Semantic role

A semantic role is the stable meaning a consumer needs. Examples include a context router, preserved source/reference material, maintained synthesis, current state, tasks, project work, or a capability collection.

Roles are deliberately fewer and more stable than concrete paths. They should exist only where they pay for interoperability.

### 5.3 Binding

A binding is the concrete local implementation of a semantic role: a file, directory, adapter, tool, or other implementation recognized by the governing contract.

The binding may be configurable. CCA consumers must not infer semantic identity from a default path when the contract says the binding can move.

### 5.4 Authority and mutation

Meaning alone is insufficient for safe operation. A consumer may also need to know whether a role is human-authoritative, shared, external, or derived; whether it is mutable, append-oriented, immutable, reconstructable, or governed; and what operations an agent may perform.

These dimensions belong to the profile/local contract when needed. CCA core does not require every workspace to serialize a large policy matrix. It requires interoperability semantics to remain explicit enough where ambiguity would otherwise be unsafe.

## 6. Route before search

The original scalability problem cannot be solved by moving files into prettier directories. A cold consumer needs a bounded navigation algorithm.

CCA's preferred order is:

```text
intent
  -> boundary
  -> applicable authority/instructions
  -> semantic role
  -> binding/router
  -> boundary-local catalog/index/contract
  -> targeted search
  -> optional derived search/index infrastructure
  -> broad filesystem search as fallback
```

This is intentionally different from a universal root manifest.

### 6.1 Federated routing

Large systems should route recursively. A root bootstrap identifies the relevant boundary or role. A project may then expose its own local router. A large knowledge domain may expose a local catalog or index. A nested native ICM workspace uses its own native routing. No root file needs to enumerate the universe.

This matters at different scales:

- **~100 files**: ordinary filesystem structure and a compact router/index may be enough.
- **~10,000 files**: local domain/project routers, targeted keyword search, or derived indexes usually become useful.
- **~100,000 files**: stronger search/index infrastructure may be justified, but it should remain scoped and replaceable rather than turning into the only semantic authority.
- **many nested projects**: each project remains a boundary with its own routing/authority instead of becoming entries in one giant mutable manifest.

CCA does not prescribe a vector database, graph database, BM25 engine, or other retrieval technology. Those are replaceable implementations. The durable contract is that a consumer can narrow the scope before broad search and that derived indexes remain rebuildable views unless separately declared authoritative.

## 7. Bootstrap without circularity

A semantic resolver cannot require a manifest whose location can only be found by already running that resolver.

CCA therefore separates the interoperability requirement from profile-specific bootstrap anchors.

An upstream-native system uses its upstream bootstrap. AGENTS.md may provide another portable scoped entry where applicable. A named CCA profile defines its own durable bootstrap. An ordinary repository may be discoverable from its existing conventional files without adopting a new manifest.

CCA core does not require one global filename. It requires a claimed CCA-conformant/profile target to make its bootstrap discoverable through its declared contract.

## 8. Optional Hybrid Workspace Profile

The CCA Hybrid Workspace Profile is a CCA-owned optional profile for a recurring hybrid problem: one filesystem-native environment containing maintained knowledge, captured/raw material, projects, operational state, reusable capabilities, and human/agent workflows.

It is not CCA itself.

The profile uses a frozen-v1 `WORKSPACE.yaml` semantic/policy matrix and a human-authored `AGENTS.md` control surface. Its reference implementation includes Python generation/audit tooling, but the tooling is not the normative architecture.

### 8.1 Target isolation

Reference tooling requires an explicit external target. It must not use the installed skill directory as the workspace merely because the scripts live there. Binding and generated destinations must remain beneath the target after path/symlink resolution.

### 8.2 Configurable bindings

The profile's stable keys identify roles while bindings identify current paths. Moving `_state/`, `_runtime/`, or the `context.router` binding must propagate through generated consumers without changing semantic identity.

### 8.3 Generated artifacts

The profile distinguishes semantic outputs from reference-implementation filenames. `context.router` is a semantic output role; `CONTEXT.md` is only its frozen-v1 default binding. `SPEC.md`, `paths.sh`, `mkdirs.sh`, and editor exclusions are derived helpers/views rather than canonical content authorities.

The bundled Python renderer may use byte-for-byte drift checks for artifacts it owns. An independent implementation in Rust, Go, or another language does not need to reproduce Python control flow. It must reproduce the normative semantic and safety contract.

### 8.4 Crosswalks

The profile's crosswalk records influences/mappings, not equivalence. In particular, the simple frozen-v1 PARA mapping must not be read as proof that PARA `Resources` means `knowledge.reference`. A future version may use a richer exact/partial/composed machine representation; changing the frozen machine shape itself should be versioned rather than smuggled in as a path customization.

## 9. Independent implementation test

CCA should be understandable without its reference scripts.

An independent implementer should be able to read the normative CCA references and a named profile contract and build a compatible resolver in another language. The implementation needs to know:

1. how boundaries are identified;
2. how semantic roles are addressed;
3. how bindings are resolved;
4. how upstream authority takes precedence;
5. which profile fields are normative;
6. which outputs are derived and rebuildable;
7. which mutation/authority rules apply where declared;
8. what conformance claim is being made;
9. how the bootstrap is discovered;
10. how local routing can grow without a global manifest.

If crucial behavior is available only by reverse-engineering Python, that behavior belongs in the normative profile contract. Conversely, Python formatting details do not become normative merely because the reference implementation uses them.

## 10. Validation model

CCA validation is claim-aware.

The order is:

1. identify the boundary and claimed upstream/profile;
2. validate upstream-native claims against the current upstream authority;
3. validate CCA semantic resolution only where CCA conformance is claimed;
4. validate a named CCA profile against its own contract;
5. validate reference-implementation drift where the reference implementation owns generated artifacts;
6. run portability/fresh-agent checks where claimed;
7. report optional hardening separately.

A CCA validation pass never waives an upstream failure.

### 10.1 Validation should test behavior

String-presence checks are appropriate for limited documentation consistency cases, but they are insufficient for behavioral claims. Target isolation must be tested with external targets and different current working directories. Binding relocation must be exercised. Symlink escapes must be rejected. Generated outputs must be inspected at materialized targets. The exact committed package must be what the final suite tests.

Validators should also avoid encoding a second hidden specification. Package/distribution validators should verify packaging boundaries and resource locality; semantic behavior should remain grounded in the normative references and behavioral tests.

## 11. Skill architecture

CCA intentionally ships as one `cca` Agent Skill rather than seven separately installable packages.

The seven modes are operation/decision surfaces, not seven products:

- `architect`: workspace structure, boundaries, profiles, method composition.
- `scaffold`: minimal approved materialization.
- `sync`: reconcile declared routing/bindings/derived state.
- `ingest`: integrate evidence under applicable authority.
- `query`: resolve maintained knowledge/evidence with minimum sufficient context.
- `lint`: validate the claims actually made.
- `advise`: apply engineering/process/security/context judgment without turning preferences into enforcement.

Progressive disclosure is preserved by loading only the selected mode's references. Architect and advisor remain logically distinct reference domains.

## 12. Open-standard readiness

CCA is not mature merely because it is stored in Markdown. An interoperability architecture should satisfy stronger properties.

### 12.1 Obvious normative surface

Normative semantics must be clearly identified and installable with the skill. Repository articles and examples may explain the system but cannot be the only source of runtime meaning.

### 12.2 Defaults are not requirements

Default bindings and reference layouts must be labeled as defaults/profile choices. Independent implementations must not have to mimic folder names that are not semantically normative.

### 12.3 Testable conformance claims

A tool should be able to state which claim it validated: upstream-native, CCA-compatible, CCA-conformant, named profile-conformant, or optional hardening. These are not interchangeable pass/fail labels.

### 12.4 Extension points

New profiles may define stronger contracts without changing CCA core. New upstream mappings may be added without transferring authority from the upstream. Retrieval engines and runtimes can evolve below the semantic layer.

### 12.5 Backward compatibility

Semantic keys and profile-policy vocabularies that are declared stable must follow explicit evolution rules. Binding changes can be non-breaking where the profile says so. Changes to semantic meaning or frozen policy matrices should be versioned.

### 12.6 Usable without the skill

A materialized workspace should remain inspectable and useful if the CCA skill disappears. The skill can make operations easier, but it should not be the only place where durable target semantics live.

## 13. What CCA must not become

CCA fails if it becomes any of the following:

- a fixed universal directory tree;
- ICM with configurable folder names;
- a replacement or fork of ICM;
- a mandatory LLM Wiki implementation;
- a PARA/BASB/Zettelkasten merger;
- a runtime or orchestration framework;
- a global metadata manifest that enumerates every file;
- a proprietary database required to understand workspace meaning;
- a collection of duplicated compatibility vocabularies;
- a Python implementation whose behavior is the only practical specification.

The architecture should continuously delete accidental machinery that does not pay for interoperability.

## 14. Limitations

CCA does not solve every context problem.

Real-time multi-agent coordination requires runtime/message-passing infrastructure. Large-scale retrieval may require specialized search/index services. Fine-grained authorization requires actual enforcement outside descriptive files. Distributed consistency and transactional state require conventional systems. Some upstream conventions remain vendor/harness-specific by design.

CCA also cannot infer authority safely when a workspace provides no reliable evidence. In ambiguous cases the system should report ambiguity rather than invent a confident mapping.

The Hybrid Workspace Profile is deliberately opinionated and therefore cannot be the right profile for every environment.

## 15. Evolution principle

CCA is explicitly expected to change as upstream systems and better ecosystem standards evolve.

If ICM improves its routing/validation model, CCA should update its mapping rather than preserve a stale imitation. If AGENTS.md or Agent Skills evolve, CCA should follow current primary authority. If a better broadly adopted interoperability convention supersedes a CCA-specific mechanism, convergence means deleting the redundant CCA mechanism.

The stable principle is not a filename or field. It is preservation of independently governed meaning across boundaries and implementations.

## 16. Final architectural test

Remove the name CCA and ask what remains.

The irreducible problem is this:

> Independently governed filesystem-native systems can coexist in one larger environment, but no individual upstream tells a generic consumer how to preserve each boundary's authority while addressing the same kind of context through stable semantic roles whose concrete bindings differ by boundary and may relocate over time.

ICM solves a concrete staged workspace architecture. LLM Wiki solves persistent maintained synthesis. AGENTS.md solves scoped instructions. Agent Skills solves capability packaging. PARA/BASB/Zettelkasten solve human knowledge-work concerns. Ordinary filesystem conventions provide durable representation. Software-engineering principles provide design discipline.

None of those individually defines the cross-system resolution contract:

```text
resolve boundary
  -> preserve governing authority
  -> request stable semantic role
  -> resolve local binding
  -> descend through local routing/indexing
  -> operate under local mutation policy
```

That small semantic interoperability layer is the defensible contribution.

If CCA grows beyond what is necessary to provide that layer and optional well-scoped profiles around it, it should be reduced. If its implementation starts deriving semantics from `_state`, `_runtime`, `CONTEXT.md`, `wiki/`, or another default path instead of the governing boundary/role/binding contract, it has regressed into the exact coupling it was created to avoid.

## Conclusion

CCA should not ask the ecosystem to converge on one tree. It should make heterogeneous trees and systems mutually legible while preserving the authority that made each system valid in the first place.

Its durable core is intentionally small:

```text
scoped boundaries
+
stable semantic roles
+
configurable bindings
+
explicit authority/compatibility semantics where needed
+
route-before-search
```

Profiles may add stronger policies. Reference implementations may add generators and validators. Upstream mappings may add interoperability knowledge. None of those should be confused with CCA core.

The measure of success is not how much CCA vocabulary a workspace contains. It is whether humans and agents can move between independently governed filesystem-native systems without losing meaning, authority, portability, or the ability to understand what is happening.

## References

- Jake Van Clief and David McDermott, *Interpretable Context Methodology: Folder Structure as Agent Architecture*, arXiv:2603.16021.
- RinDig, *Interpretable Context Methodology* repository and `_core/CONVENTIONS.md`.
- Andrej Karpathy, *LLM Wiki* idea file.
- `agents.md`, AGENTS.md open convention.
- Agent Skills specification, `agentskills.io`.
- Tiago Forte, PARA and Building a Second Brain/CODE.
- Niklas Luhmann and subsequent Zettelkasten practice literature.
