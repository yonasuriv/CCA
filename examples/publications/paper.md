# Convergent Context Architecture

> **An Agent-Agnostic Interoperability Architecture for Filesystem-Native AI Context**

| Field | Value |
| --- | --- |
| **Document type** | Whitepaper (non-normative) |
| **Version** | 1.0 |
| **Status** | Release companion; non-normative |
| **Date** | 2026-08-21 |
| **Authors** | Jonathan Di Rico |
| **Normative counterpart** | `skills/cca/references/core/` |
| **License** | MIT |

## Abstract

AI agents increasingly operate directly on ordinary filesystems: code repositories, research corpora, personal knowledge bases, client workspaces, project trees, workflow folders, and durable operational state. Existing methods already solve important parts of that environment. ICM/MWP defines a concrete staged context architecture; LLM Wiki describes persistent LLM-maintained knowledge synthesis; AGENTS.md provides scoped portable instructions; Agent Skills packages reusable capabilities; PARA, BASB/CODE, and Zettelkasten organize human knowledge work in different ways. The unresolved problem is not the absence of another method. It is the absence of a small shared semantic contract for composing independently governed filesystem-native systems without forcing them into one structural convention.

Convergent Context Architecture (CCA) addresses that interoperability problem through three primary ideas: **scoped boundaries**, **stable semantic roles**, and **configurable bindings**. A role describes what something means; a binding describes where or how that role is implemented inside a particular boundary. A CCA-aware consumer resolves `boundary + semantic role -> binding` before relying on path names, while upstream-native systems keep their own authority and native structures.

CCA distinguishes five composable claims rather than a maturity ladder: **Upstream-native**, **CCA-compatible**, **CCA-conformant**, **Profile-conformant**, and **CCA-hardened**. Selected upstream patterns may additionally be described as **ICM-derived** or otherwise source-derived without claiming native conformance. The architecture is path-agnostic at its core, profile-aware where stronger contracts are useful, and designed so large collections can route through boundary-local catalogs and indexes rather than a single global manifest or broad filesystem grep.

The central claim is deliberately narrow: CCA is useful only if the interoperability architecture remains smaller and more durable than the systems it connects. If it becomes a fixed folder tree, a replacement for ICM, a mandatory wiki, a runtime, or another ecosystem island, it has failed its own purpose.

## 1. Introduction

### 1.1 Context has become a filesystem concern

Modern coding agents and general-purpose AI runtimes receive substantial operating context from files. Repositories may contain instructions, policies, workflow contracts, source material, maintained knowledge, task state, tools, templates, outputs, logs, and nested projects. Plain files are valuable because they are human-readable, diffable, versionable, portable, and compatible with many execution environments.

The filesystem, however, does not carry universal semantics. A directory called `resources/` may mean a PARA Resource shelf, static application assets, external research, or something entirely different. `CONTEXT.md` is a native contract in ICM but may be an arbitrary filename elsewhere. `_state/` may be a useful implementation choice in one profile without being meaningful in another. A nested project may have its own authority that intentionally conflicts with assumptions made by an outer workspace.

The problem therefore becomes semantic resolution rather than merely storage.

### 1.2 The interoperability gap

Existing systems answer different questions:

- **ICM/MWP**: how a staged filesystem-native workflow routes context, contracts, and handoffs.
- **LLM Wiki**: how persistent maintained synthesis can compound over durable source material.
- **AGENTS.md**: how portable agent guidance is scoped through a repository tree.
- **Agent Skills**: how reusable capabilities are packaged with progressive disclosure.
- **PARA**: where actionable material belongs according to horizon of commitment.
- **BASB/CODE**: how human knowledge moves through capture, organization, distillation, and expression.
- **Zettelkasten**: how addressable linked ideas develop over time.
- **Scrum, Kanban, DevOps, and other delivery approaches**: how work is coordinated at their own process scopes.

These systems are valuable precisely because they remain distinct. The gap appears when several coexist and an agent must decide which boundary it is in, which authority governs it, what role it needs, where that role is implemented, and what it may change without breaking another system.

### 1.3 Product position

CCA is an evolving, agent-agnostic interoperability architecture for filesystem-native AI context. It aims to bridge human knowledge work and agentic work without forcing existing systems into a new competing convention, while improving efficiency and reducing unnecessary context, compute, usage, operational cost, and technical debt.

This whitepaper is explanatory. The normative specification inside the installable `skills/cca/` package remains authoritative for CCA semantics.

## 2. Design constraints

### 2.1 Preservation over replacement

When an upstream, framework, methodology, protocol, or standard already owns a semantic domain, CCA preserves that authority. CCA may map it, route to it, compose with it, or optionally harden the surrounding workspace, but it must not silently rewrite the upstream while continuing to call the result native.

A native ICM workspace remains ICM. An LLM Wiki implementation remains governed by its own schema and maintenance contract. A PARA tree remains PARA organization rather than a disguised CCA taxonomy. Agent Skills remain Agent Skills rather than becoming CCA modules.

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

without changing semantic meaning if the governing contract permits relocation.

Likewise:

```text
project/cca::context.router -> CONTEXT.md
project/example::context.router -> ROUTER.md
```

can coexist because the path is not the identity. Native upstream requirements are the exception: if an upstream makes a concrete filename part of conformance, CCA preserves that requirement inside the upstream-native boundary.

### 2.3 Boundaries before taxonomy

A boundary identifies the scope whose authority and local semantics apply. Boundaries can nest. A personal workspace may contain a normal code repository, an upstream-native ICM workflow, a maintained knowledge base, and human notes. CCA should not flatten these merely to obtain one uniform tree.

The composition rule is simple:

> **Nest boundaries; do not merge schemas merely because they coexist.**

### 2.4 Automation in service of augmentation

CCA treats automation as implementation machinery rather than the product objective.

> **Automation is the means; augmenting human capabilities is the goal.**

The durable environment should increase a human's ability to understand, direct, inspect, recover, and reuse work. Derived indexes, generators, agents, or automation should not make human-owned context less legible or less portable.

## 3. Relationship to upstream systems

### 3.1 ICM / Model Workspace Protocol

ICM/MWP provides CCA's strongest filesystem-native context influence. Native ICM defines concrete routing layers, exact context contracts, handoffs, one-way dependencies, selective loading, canonical sources, and other acceptance behavior.

CCA preserves those requirements when a boundary claims **Upstream-native ICM**. It does not rename native files to fit a CCA preference and does not replace harness-native authority merely to appear more portable.

A non-native boundary may borrow selected ICM ideas such as local contracts, stages, one-way dependencies, handoffs, or progressive disclosure. That usage is **ICM-derived**. It does not make every CCA workspace an ICM skeleton, and it does not make a CCA-owned profile native ICM.

### 3.2 LLM Wiki

Karpathy's LLM Wiki is an intentionally abstract idea pattern centered on durable source material and persistent maintained synthesis. Its concrete filesystem structure and tooling are implementation choices.

CCA therefore treats LLM Wiki as a maintained-knowledge pattern rather than a fixed filesystem certification. A boundary using the idea should preserve the distinction between durable evidence and maintained synthesis, but CCA must not attribute its own capture folders, provenance fields, lifecycle metadata, or shared human/agent policies to LLM Wiki.

### 3.3 AGENTS.md

AGENTS.md provides portable repository-scoped agent guidance. CCA uses it as an existing convention rather than defining a competing portable instruction filename. Nested instruction scope remains intact. CCA does not claim AGENTS.md universally replaces harness-specific native files when another system requires them.

### 3.4 Agent Skills

CCA ships as one Agent Skill named `cca`. Detailed behavior is progressively disclosed through skill-local references and assets. The package exposes seven lazy modes: `architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`, and `advise`.

The distribution boundary is `skills/cca/`. Runtime-required CCA meaning must not depend on repository-global documentation or removed sibling packages.

### 3.5 Human knowledge-work methods

PARA, BASB/CODE, and Zettelkasten are not machine-facing CCA profiles.

PARA organizes according to actionability. BASB/CODE provides a human lifecycle lens. Zettelkasten develops addressable linked ideas. CCA may route across these structures, but it does not reinterpret them as semantic-role schemas.

This matters particularly for PARA `Resources`. A Resource is an organizational category and may contain a book, raw source, dataset, personal note, maintained synthesis, or nested workspace. It is therefore not equivalent to `knowledge.reference`. Organizational shelves and epistemic roles are separate axes.

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

Labels such as **ICM-derived** provide provenance for borrowed patterns and prevent partial adoption from masquerading as upstream conformance.

## 5. The semantic interoperability model

### 5.1 Boundary

A boundary is the scope at which authority and semantics are resolved. Examples include a repository root, a nested project, a client workspace, a native ICM root, a knowledge base, or a restricted subtree.

### 5.2 Semantic role

A semantic role is the stable meaning a consumer needs. Examples include a context router, preserved source/reference material, maintained synthesis, current state, tasks, project work, or a capability collection.

Roles are deliberately fewer and more stable than concrete paths. They should exist only where they pay for interoperability.

### 5.3 Binding

A binding is the concrete local implementation of a semantic role: a file, directory, adapter, tool, or other implementation recognized by the governing contract.

The binding may be configurable. CCA consumers must not infer semantic identity from a default path when the governing contract says the binding can move.

### 5.4 Orthogonal policy

Meaning alone is insufficient for safe operation. A profile or local contract may separately define authority, mutability, lifecycle, provenance, indexing, recovery, or other operational properties.

These properties are not semantic roles. CCA's core concern is keeping identity and policy separable enough that a path, actor, or implementation detail does not accidentally redefine what an object means.

## 6. Route before search

A large workspace cannot be made scalable merely by moving files into prettier directories. A cold consumer needs a bounded navigation algorithm.

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

Large systems should route recursively. A root bootstrap identifies the relevant boundary or role. A project may expose its own local router. A large knowledge domain may expose a local catalog or index. A nested native ICM workspace uses its own native routing. No root file needs to enumerate the universe.

At hundreds of files, ordinary structure and a compact router may be sufficient. At tens of thousands, boundary-local catalogs and search indexes become more useful. At hundreds of thousands, stronger retrieval infrastructure may be justified. The retrieval implementation can change without changing the semantic contract, and derived indexes remain rebuildable unless a separate authority explicitly owns them.

## 7. Bootstrap without circularity

A semantic resolver cannot require a manifest whose location can only be found by already running that resolver.

CCA therefore separates the interoperability requirement from profile-specific bootstrap anchors. An upstream-native system uses its upstream bootstrap. AGENTS.md may provide portable scoped guidance where applicable. A named CCA profile defines its own bootstrap. An ordinary repository may remain discoverable from its existing conventional files without adopting a new manifest.

CCA core does not require one universal root filename.

## 8. Optional Hybrid Workspace Profile

The CCA Hybrid Workspace Profile is a CCA-owned optional profile for a recurring hybrid problem: one filesystem-native environment containing maintained knowledge, captured material, preserved sources, projects, operational state, reusable capabilities, and human/agent workflows.

It is not CCA itself.

The **current bundled profile schema is v2**. V2 preserves the complete frozen-v1 semantic-role, policy, authority, vocabulary, generation, and invariant baseline. The version bump exists because frozen v1 itself declared semantic-key additions to require a schema-version bump.

The v2 extension adds two filesystem-visible source-admission classifications beneath the existing semantic role `knowledge.reference`:

```text
20-sources/
├── curated/      # reference.curated   -> knowledge.reference
└── collected/    # reference.collected -> knowledge.reference
```

The core rule is:

```text
source provenance/admission
!= content authorship
!= semantic role
```

Both classes remain preserved source/evidence. They do not become separate knowledge roles.

### 8.1 Curated evidence

`reference.curated` means the source was explicitly admitted by a human. It composes with `knowledge.reference` and remains human-authoritative. Agents may read curated evidence but may not add, edit, replace, rename, relocate, or delete it under normal profile operation.

“Curated” records how the source entered the corpus. It does not mean the source is correct, high quality, or endorsed.

### 8.2 Collected evidence

`reference.collected` means an agent, crawler, integration, workflow, API, or equivalent tool automatically acquired the source. Agents may deposit **new** source objects using the profile's existing append/add-child semantics. Existing collected objects remain unchanged by normal agent operation.

Automatically collected evidence preserves acquisition provenance and content identity. The current profile requires sufficient metadata to identify the acquisition actor/method, origin, timestamp, and content hash or durable identity as applicable.

A collected source does not move to curated merely because a human later reviews it. Review is metadata; the classification preserves original admission provenance.

### 8.3 Evidence is not truth

Presence under either source class means **preserved evidence**, not truth, correctness, quality, or endorsement. `collected` material may be explicitly unreviewed.

Raw/reference material survives distillation. An agent does not “clean up” a raw source by rewriting it as prose in place.

The distinctions remain:

```text
knowledge.reference
  = what the material IS: preserved evidence

reference.curated | reference.collected
  = HOW the evidence entered the workspace

knowledge.durable
  = what the workspace LEARNED from evidence

output.artifact
  = what the workspace deliberately PRODUCED for external consumption
```

Research itself is an activity, not another knowledge role. A finite research effort is represented as project work and may traverse capture -> references -> durable synthesis -> output while tasks/state represent execution.

### 8.4 Nested binding precedence

The parent `knowledge.reference` binding cannot widen or erase the policies of the child source classes. Semantic classification composes across matching bindings, while mutation policy resolves from the most-specific matching binding. This allows both classes to remain `knowledge.reference` while preserving different admission behavior.

### 8.5 Target isolation and generated artifacts

The reference implementation requires an explicit target workspace. It must not use the installed skill directory as the workspace merely because the scripts live there. Bindings and generated destinations remain beneath the target after path and symlink resolution.

The profile distinguishes semantic outputs from implementation filenames. `context.router` is the semantic identity; `CONTEXT.md` is its current default binding in this profile and may relocate where the profile permits. `SPEC.md`, `paths.sh`, `mkdirs.sh`, and editor-exclusion files are derived artifacts rather than canonical knowledge.

## 9. Independent implementation test

CCA should be understandable without its Python reference scripts.

An independent implementer should be able to read the normative CCA references and a named profile contract and build an equivalent resolver in Rust, Go, another language, or another runtime. The implementation needs to know:

1. how boundaries are identified;
2. how semantic roles are addressed;
3. how bindings are resolved;
4. how upstream authority is preserved;
5. which profile fields are normative;
6. which outputs are derived and rebuildable;
7. which mutation and authority rules apply where declared;
8. what conformance claim is being made;
9. how bootstrap discovery works;
10. how local routing can grow without a global manifest.

If crucial behavior is available only by reverse-engineering one implementation, that behavior belongs in the normative contract. Conversely, Python formatting details do not become normative merely because the reference implementation uses them.

## 10. Validation model

CCA validation is claim-aware. The order is:

1. identify the boundary and claimed upstream/profile;
2. validate upstream-native claims against the current upstream authority;
3. validate CCA semantic resolution only where CCA conformance is claimed;
4. validate a named CCA profile against its own contract;
5. validate implementation drift where the reference implementation owns generated artifacts;
6. run portability and fresh-agent checks where claimed;
7. report optional hardening separately.

A CCA validation pass never waives an upstream failure.

Behavioral claims require behavioral tests. Target isolation is exercised with external targets and different current working directories. Binding relocation is exercised rather than inferred from strings. Symlink escapes are rejected. Generated artifacts are drift-checked. The exact committed package is what release CI tests.

## 11. Skill architecture

CCA intentionally ships as one `cca` Agent Skill rather than seven independently installable packages.

The seven modes are operation or decision surfaces:

- `architect`: workspace structure, boundaries, profiles, and method composition;
- `scaffold`: minimal approved materialization;
- `sync`: reconcile declared routing, bindings, and derived state;
- `ingest`: integrate evidence under applicable authority;
- `query`: resolve maintained knowledge and evidence with minimum sufficient context;
- `lint`: validate the claims actually made;
- `advise`: apply engineering, process, security, autonomy, model, and context judgment without turning preferences into enforcement.

Progressive disclosure is preserved by loading only the selected mode's required references. Architect and advisor remain logically separate reference domains even though they share one package.

## 12. Open-standard readiness

CCA is not mature merely because it is stored in Markdown. An interoperability architecture needs stronger properties.

### 12.1 Obvious normative surface

Normative semantics must be clearly identified and installable with the skill. Repository articles and examples may explain the system but cannot be the only source of runtime meaning.

### 12.2 Defaults are not identities

Default bindings and reference layouts are profile choices. Independent implementations do not need to reproduce a folder name unless a governing upstream or profile makes that representation normative.

### 12.3 Testable claims

Validation should state which claim was checked: Upstream-native, CCA-compatible, CCA-conformant, named profile-conformant, or optional hardening. Those are not interchangeable pass/fail labels.

### 12.4 Extension without absorption

New profiles may define stronger contracts without changing CCA core. New upstream mappings may be added without transferring authority from the upstream. Retrieval engines and runtimes can evolve below the semantic layer.

### 12.5 Backward compatibility

Semantic keys and profile-policy vocabularies declared stable follow explicit evolution rules. A binding change can be non-breaking where a profile says so. Changes to frozen semantic meaning or policy require explicit version treatment.

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
- a global metadata manifest enumerating every file;
- a proprietary database required to understand workspace meaning;
- a collection of duplicated compatibility vocabularies;
- a reference implementation whose code is the only practical specification.

Structure must continue to earn its cost.

## 14. Limitations

CCA does not solve every context problem. Real-time multi-agent coordination requires runtime/message-passing infrastructure. Large-scale retrieval may require specialized search/index services. Fine-grained authorization requires actual enforcement beyond descriptive files. Distributed consistency and transactional state require conventional systems. Some upstream conventions remain vendor- or harness-specific by design.

CCA also cannot infer authority safely when a workspace provides no reliable evidence. In ambiguous cases the system should report ambiguity rather than invent a confident mapping.

The Hybrid Workspace Profile is deliberately opinionated and cannot be the right profile for every environment.

## 15. Evolution principle

CCA is expected to change as upstream systems and ecosystem standards evolve.

If ICM improves its routing or validation model, CCA should update its mapping rather than preserve a stale imitation. If AGENTS.md or Agent Skills evolve, CCA should follow current primary authority. If a better broadly adopted interoperability convention supersedes a CCA-specific mechanism, convergence means deleting the redundant CCA mechanism.

The stable principle is not a filename or field. It is preservation of independently governed meaning across boundaries and implementations.

## 16. Final architectural test

Remove the name CCA and ask what remains.

The irreducible problem is this:

> Independently governed filesystem-native systems can coexist in one larger environment, but no individual upstream tells a generic consumer how to preserve each boundary's authority while addressing the same kind of context through stable semantic roles whose concrete bindings differ by boundary and may relocate over time.

ICM solves a concrete staged workspace architecture. LLM Wiki solves persistent maintained synthesis. AGENTS.md solves scoped instructions. Agent Skills solves capability packaging. PARA, BASB/CODE, and Zettelkasten solve human knowledge-work concerns. Ordinary filesystem conventions provide durable representation. Software-engineering principles provide design discipline.

None of those individually defines the cross-system resolution contract:

```text
resolve boundary
  -> preserve governing authority
  -> request stable semantic role
  -> resolve local binding
  -> descend through local routing/indexing
  -> operate under local policy
```

That small interoperability contract is CCA's defensible contribution. If CCA grows beyond what is necessary to provide it and optional well-scoped profiles around it, it should be reduced.

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
route before search
```

Profiles may add stronger policies. Reference implementations may add generators and validators. Upstream mappings may add interoperability knowledge. None of those should be confused with CCA core.

The measure of success is not how much CCA vocabulary a workspace contains. It is whether humans and agents can move between independently governed filesystem-native systems without losing meaning, authority, portability, or the ability to understand what is happening.

## References

- [Jake Van Clief and David McDermott, *Interpretable Context Methodology: Folder Structure as Agent Architecture*](https://arxiv.org/abs/2603.16021), 2026.
- [RinDig, *Interpretable Context Methodology* repository](https://github.com/RinDig/Interpretable-Context-Methodology).
- [Andrej Karpathy, *LLM Wiki* idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
- [AGENTS.md open convention](https://agents.md).
- [Agent Skills specification](https://agentskills.io).
- [Tiago Forte, PARA](https://fortelabs.com/blog/para/) and [Building a Second Brain](https://fortelabs.com/blog/basboverview/).
