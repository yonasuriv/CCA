# Convergent Context Architecture

> **Convergent Context Architecture (CCA)** is an evolving, agent-agnostic interoperability architecture for filesystem-native AI context. It helps humans and AI agents understand, navigate, and operate across workspaces, projects, and bodies of knowledge by defining stable semantic roles, scoped boundaries, and configurable bindings that preserve meaning even when their concrete paths or implementations change.

CCA aims to bridge human knowledge work and agentic work without forcing existing systems into a new competing convention, by building on open standards, ecosystem conventions, established methodologies, protocols and frameworks, and based on software-engineering principles and fundamentals.

Its goal is to make automation easier in service of augmenting human capabilities while improving efficiency, reducing technical debt and unnecessary complexity, and lowering compute, context, usage, and operational costs.

<!-- ADD THE "IN PLAIN ENGLISH EXPLAINATION" --
_In plain English_

<TEXT HERE>
-->

> **Automation is the means; augmenting human capabilities is the goal.**

## Documentation

- [Documentation index](docs/README.md)
- [Getting started](docs/getting-started.md)
- [Scenarios](docs/scenarios.md)
- [References](docs/references.md)
- [Standards](docs/standards.md)
- [Design principles](docs/design-principles.md)
- [Method composition](docs/method-composition.md)
- [Common environments](docs/common-environments.md)
- [Compatibility details](docs/compatibility-details.md)
- [Migration](docs/migration.md)
- [FAQ](docs/faq.md)

> _Braindump file that may or may not be aligned with the current goal of the repo is under [docs/_wip.md](docs/_wip.md) (must be processed first)_ \
> _Non-normative publication forms are under [examples/publications/](examples/publications/)._

## Why CCA exists

AI-assisted work increasingly depends on filesystem-native context: project instructions, routers, source material, maintained knowledge, reusable skills, configuration, working artifacts, human edits, outputs, tasks, decisions, memory, and execution state.

At the same time, humans already use established knowledge-management, planning, engineering, and delivery methods, while agent ecosystems are converging on their own standards and conventions.

These systems often solve different parts of the same problem, operate at different scopes, and define different authorities. They are not automatically interoperable.

CCA defines shared ground between them.

The objective is not one universal directory tree, workflow, knowledge model, or methodology. The objective is:

- **interoperability** across heterogeneous systems;
- **navigability** without broad filesystem search;
- **portability** across tools, models, and runtimes;
- **explicit boundaries and authority** over context and state;
- **durable human control** over canonical information;
- **minimum sufficient context** for the task at hand;
- **recoverable and deterministic operations** where possible.

CCA builds on and interoperates with existing work rather than redefining it and adds only the compatibility, routing, and context semantics needed so humans and agents can determine:

1. **Where am I?**
2. **What already governs this boundary?**
3. **What context is relevant now?**
4. **What can I change safely?**
5. **How does this boundary connect to the others?**

Its filesystem-native context foundations are strongly influenced by Van Clief and McDermott's *Interpretable Context Methodology: Folder Structure as Agentic Architecture* and its Model Workspace Protocol (MWP), which treat filesystem structure, routing, stage contracts, handoffs, and progressive context loading as part of the agent architecture.

CCA extends these ideas to broader and more heterogeneous environments: workspaces containing multiple projects, long-lived responsibilities, source repositories, raw notes, clippings, transcripts, documents, research, maintained knowledge, operational state, restricted material, reusable capabilities, and nested systems with their own native semantics.

At this scale, paths alone are not enough. Agents need to understand not only **where something is**, but also:

- What semantic role it serves;
- What may modify it;
- How concurrent mutation is handled;
- How it can be recovered or rebuilt;
- Which boundary it belongs to;
- Which authority governs it;
- Whether it is durable, derived, or disposable;
- Whether freshness matters;
- Whether it is required by the active contract.

CCA addresses this through a small semantic model:

```mermaid
---
config:
  flowchart:
    wrappingWidth: 500
---
flowchart LR
    A["Boundary + Semantic Role"]
    B["Binding"]
    C["Authority · Capabilities · Concurrency"]
    D["Durability · Recovery · Freshness · Requiredness"]

    A --> B --> C --> D
```

Semantic roles remain stable while bindings may change.

For example, `state.tasks` may resolve to `TASKS.md`, a directory, a structured file, or another locally declared implementation without changing what the role means.

Stable object identifiers may additionally be used where rename-independent identity materially matters, such as durable notes, decisions, tasks, or records. They are not required for every file or directory.

## What CCA is

CCA is:

- an interoperability and composition architecture for filesystem-native context;
- a semantic layer for boundaries, roles, bindings, routing, authority, mutation, durability, recovery, and freshness;
- a way to preserve native systems while making their relationships explicit;
- a model for deterministic context discovery before broad search;
- a framework for deciding when to preserve, compose, validate, harden, scaffold, index, or deliberately restructure;
- a portable Agent Skill with focused, progressively disclosed capabilities;
- an evolving compatibility layer that should adapt as its upstream standards, conventions, and ecosystems evolve.

CCA is **not**:

- a universal directory tree;
- a replacement knowledge-management methodology;
- an agent runtime or orchestration framework;
- a real-time multi-agent message bus;
- a scheduler or queue;
- a vector database or retrieval engine;
- a replacement for MCP;
- a replacement for ICM, LLM Wiki, `AGENTS.md`, Agent Skills, PARA, BASB/CODE, Zettelkasten, Scrum, Kanban, XP, DevOps, SAFe, LeSS, Disciplined Agile, or other established systems;
- a requirement that every repository use `CONTEXT.md`, `stages/`, a wiki, a manifest, frontmatter, stable object IDs, or any fixed directory structure.

## Convergence model

CCA sits between existing authorities and the filesystem-native boundaries in which humans and agents operate.

It does not own those authorities or flatten them into a common schema. It provides the semantic contract required to identify boundaries, resolve roles, preserve authority, and route to the minimum relevant context while allowing each nested system to retain its native behavior.

<!-- Composition + interoperability semantics -->
```mermaid
---
config:
  flowchart:
    wrappingWidth: 500
    defaultRenderer: elk
---
flowchart TB
    subgraph UPSTREAM["Upstream"]
        direction TB
        STANDARDS["Standards"]
        PRINCIPLES["Principles"]
        FRAMEWORKS["Frameworks"]
        CONVENTIONS["Conventions"]
        METHODOLOGIES["Methodologies"]
    end

    subgraph CONSUMERS["Consumers"]
        direction LR
        AGENTS["Agents"]
        HUMANS["Humans"]
    end

    subgraph CCA_CONTAINER["CCA"]
        direction LR
        SPEC["<b>STRUCTURE</b><br/>Specification <br>↓<br> Boundary + Semantic Role <br>↓<br> Binding<br/>↓<br>Authority · Capabilities · Concurrency<br/>↓<br>Durability · Recovery · Freshness · Requiredness"]
        RESOLVER["<b>RESOLVE</b><br/>Route before search"]
        LINT["<b>LINT</b><br/>Static + Runtime enforcement"]
        SPEC --> LINT
        SPEC --> RESOLVER
    end

    subgraph CONTAINER["Workspace Container"]
        direction LR
        subgraph WORKSPACE_LAYER[" "]
            direction TB
            GENERAL["<b>Portable Workspaces</b><br>PKM / Second brains<br/>Coding projects<br/>Research systems<br/>Hybrid workspaces"]
            CONFIDENTIAL["<b>Restricted Workspaces</b><br>Client workspaces<br/>Confidential workspaces<br/><i>Gated · Not globally indexed</i>"]
        end
        subgraph SYSTEM_LAYER["System Layer"]
            direction TB
            SYS_ND["Index<br/>Cache<br/>Reports<br/><i>Generated · Rebuildable</i>"]
            SYS_ST["Scripts<br/>Templates<br/>Internal conventions<br><i>Automation · Support</i>"]
        end
    end

    UPSTREAM --> SPEC
    PRINCIPLES --> SPEC
    FRAMEWORKS --> SPEC
    CONVENTIONS --> SPEC
    METHODOLOGIES --> SPEC

    CONSUMERS -- "Intent" --> RESOLVER
    RESOLVER -- "Resolved context" --> CONSUMERS

    LINT -. "Governs" .-> GENERAL
    LINT -.-> CONFIDENTIAL
    SPEC -. "Defines" .-> SYS_ST

    RESOLVER -- "Default scope" --> GENERAL
    RESOLVER -. "Explicit scope" .-> CONFIDENTIAL
    RESOLVER -- "Reads index" --> SYS_ND

    classDef restricted stroke-dasharray:4 3
    class CONFIDENTIAL restricted
```

## Supporting skill

CCA ships with one self-contained Agent Skill under [`skills/cca/`](skills/cca/) that provides a portable operational interface to the architecture.

```text
skills/cca/
├── SKILL.md
├── references/
│   ├── core/          # normative CCA semantics and compatibility
│   ├── architect/     # workspace forms, boundaries, builders
│   ├── advisor/       # engineering and process judgment
│   └── operations/    # scaffold, sync, ingest, query, lint
└── assets/
    └── templates/
```

The root [`SKILL.md`](skills/cca/SKILL.md) acts as a compact router. It selects the smallest applicable mode and loads only the references that operation requires. It should select the smallest applicable mode and progressively load only the references required for the current operation.

Implementation work that needs no context architecture, knowledge operation, validation, or advice should never reach deeper CCA material.
> Progressive disclosure is architectural, not packaging: **This applies to both context and capability.**

| Mode        | Responsibility                                                                             |
| ----------- | ------------------------------------------------------------------------------------------ |
| `architect` | Design or restructure boundaries, semantic roles, bindings, authorities, and compositions. |
| `scaffold`  | Add the smallest useful CCA surface without unnecessarily restructuring native content.    |
| `sync`      | Reconcile declared bindings, routing, indexes, and the real filesystem.                    |
| `ingest`    | Integrate source material into the authority that owns maintained knowledge.               |
| `query`     | Resolve and synthesize relevant knowledge through declared boundaries and native systems.  |
| `lint`      | Validate adopted CCA semantics and the compatibility profiles actually claimed.            |
| `advise`    | Apply engineering, process, security, agent-system, context, and AI/ML judgment.           |

The skill is an implementation of CCA, not the definition of CCA itself:
- A CCA workspace must remain understandable from its durable files and declared semantics without requiring a particular model, harness, or installed skill.
- CCA documentation should never override the active upstream authority for a native profile.

### Normative Authority

Normative CCA semantics are maintained inside the portable skill package, not in this README:

| Reference                                                                        | Governs                                      |
| -------------------------------------------------------------------------------- | -------------------------------------------- |
| [`core/spec.md`](skills/cca/references/core/spec.md)                             | CCA semantics and operation model            |
| [`core/compatibility.md`](skills/cca/references/core/compatibility.md)           | Upstream and native compatibility boundaries |
| [`core/method-composition.md`](skills/cca/references/core/method-composition.md) | Composition semantics                        |
| [`core/adapters.md`](skills/cca/references/core/adapters.md)                     | Harness interoperability                     |
| [`core/icm-inheritance.md`](skills/cca/references/core/icm-inheritance.md)       | Provenance map for inherited ICM behavior    |

CCA-owned specifications govern only CCA semantics.

When a boundary declares or inherits an external authority, that authority remains authoritative within its scope. CCA may describe, route to, validate, or compose with it, but must not silently override it.

## References

See [Citation](CITATION.cff) and [References](docs/references.md) for acknowledgements, inspirations, and citation metadata.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md).

Changes affecting compatibility, composition, boundary semantics, or external authorities should cite the relevant primary authority and update the complete affected normative surface in the same change.

## License

MIT. See [LICENSE](LICENSE).