# Convergent Context Architecture

**Synopsis**

> **CCA (Convergent Context Architecture)** is an evolving, agent-agnostic interoperability layer for filesystem-native AI context. It aims to bridge human knowledge work and agentic work by building on open standards, ecosystem conventions, and proven methodologies, protocols and frameworks, based on software engineering principles and fundamentals, to make any workspace, project, or body of human knowledge easier for both humans and AI agents to understand, navigate, and use, without forcing it into a new competing convention. It's goal is to make automation easier in service of augmenting human capabilities, while improving efficiency, reducing technical debt, unnecessary complexity, and lowering compute, usage, and operational costs.

**In plain English**

CCA is a way to help people and AI work together more easily using the files, folders, tools, and methods they already have, and propose the best ones when they don't.

Instead of creating another system that people need to adopt, CCA connects existing standards, frameworks, protocols, and proven ways of working so both humans and AI agents can better understand, navigate, and use the same projects and knowledge.

The goal is to make automation easier where it helps people, while improving effectiveness, efficiency, and productivity and reducing unnecessary complexity, operational and usage costs

## Table of Contents

- [Why CCA exists](#why-cca-exists)
  - [What CCA is](#what-cca-is)
  - [What CCA is not](#what-cca-is-not)
  - [Where CCA works well](#where-cca-works-well)
  - [Where CCA is not enough](#where-cca-is-not-enough)
- [The Convergence Model](#the-convergence-model)
- [The Compatibility Model](#the-compatibility-model)
  - [How context routing works](#how-context-routing-works)
  - [A native ICM stage contract](#a-native-icm-stage-contract)
- [The Validation Model](#the-validation-model)
- [The CCA skill suite](#the-cca-skill-suite)
- [Getting started](#getting-started)
  - [I already have an ICM workspace](#i-already-have-an-icm-workspace)
  - [I already have an LLM Wiki](#i-already-have-an-llm-wiki)
  - [I already use PARA, Zettelkasten, BASB, or another second-brain method](#i-already-use-para-zettelkasten-basb-or-another-second-brain-method)
  - [I already have a coding project](#i-already-have-a-coding-project)
  - [I want to build a new workspace](#i-want-to-build-a-new-workspace)
- [Design principles](#design-principles)
  - [Staying compatible as upstreams evolve](#staying-compatible-as-upstreams-evolve)
  - [Why plain files matter](#why-plain-files-matter)
- [Contributing](#contributing)
- [References](#references)
- [Citation](#citation)
- [License](#license)

## Why CCA exists

Agent context is increasingly stored in ordinary repositories: instructions, task routers, stage contracts, source material, maintained knowledge, skills, configuration, vendor semantics, and working artifacts. Human knowledge systems already provide useful ways to organize, develop, and maintain that material. The problem is not that these systems need a single universal replacement; it is that their boundaries and semantics are interpreted differently by different agents.

ICM provides a filesystem architecture for staged, human-reviewable workflows. LLM Wiki provides a pattern for persistent knowledge that compounds across sessions. AGENTS.md provides portable repository instructions. Agent Skills provide focused portable capabilities. PARA, Zettelkasten, and Building a Second Brain address human organization, idea development, and knowledge-work lifecycle. Existing coding repositories already have their own structure and conventions.

CCA brings these ideas together through shared semantics, focused portable operations, compatibility rules, and existing open standards. It bridges human knowledge work and agentic work without replacing the systems that already work, making durable context easier to understand, reuse, and operate across different environments while keeping those patterns accessible to anyone.

Therefore, defining the shared ground between them, so an agent can answer five questions without forcing a migration:

1. **What type of workspace or boundary is this?**
2. **What context should I load for this task?**
3. **What capability should the operation perform?**
4. **What source conventions or methods already govern it?**
5. **What can I add without altering the native semantics?**

The objective is not to make every workspace look the same. The objective is to make different valid workspace forms **interoperable, navigable, and portable**.

### What CCA is

- a compatibility and composition layer for filesystem-native agent context;
- a set of shared semantics for routing, durable knowledge, handoffs, authority boundaries, and portability;
- a focused Agent Skills suite for designing, scaffolding, maintaining, querying, and validating workspaces;
- a way to add cross-agent guidance without destroying native tool behavior;
- a framework for deciding when to preserve, harden, intentionally conform, or simply compose existing methods.

> ***When an upstream convention, open standard, or existing method already solves the problem, preserve it.**

If an upstream changes, CCA should change toward it rather than freezing a near-compatible fork. \
Human methodologies remain method overlays unless CCA deliberately adopts a concrete machine-facing contract from them in a future revision.

See [Design principles](#design-principles).

### What CCA is not

- an agent runtime or orchestration framework;
- a real-time multi-agent message bus;
- a scheduler or queue;
- a vector database or retrieval engine;
- a replacement for MCP;
- a replacement for ICM, LLM Wiki, PARA, BASB, or Zettelkasten;
- a requirement that every repository use stages, a wiki, vendor semantics, a giant manifest, or one fixed directory tree.

### Where CCA works well

CCA is a strong fit when the work benefits from:

- persistent context across sessions;
- portability across agents/editors/runtimes;
- selective context loading;
- human-readable and versionable state;
- repeatable stage handoffs;
- maintained knowledge that compounds;
- PKM/second-brain methods connected to agent workflows without being replaced;
- scoped instructions in an existing codebase;
- optional infrastructure rather than a mandatory platform.

### Where CCA is not enough

As CCA core comes from the ICM/MWP PDLC framework, it still inherits their gaps and deliberately does not solve every systems problem.

1. **Real-time multi-agent collaboration**
    agents communicating dynamically in tight loops need message-passing/orchestration infrastructure.
2. **High-concurrency shared services**
    need queueing, isolation, locking/transactions, deployment, and other runtime concerns.
3. **Complex automated branching or scheduling**
    may need a workflow engine. CCA can still store the durable context and contracts that such a runtime consumes.
4. **Large-scale retrieval**
    may benefit from databases, embeddings, indexes, or graph systems. Those are compatible extensions as long as the durable workspace remains understandable without treating the external index as the only source of truth.

## The Convergence Model

CCA composes several different layers. They are not all the same kind of standard.

```mermaid
flowchart TB
    subgraph HUMANS["Human knowledge-work methods"]
        BASB["BASB / CODE\nCapture · Organize\nDistill · Express"]
        PARA["PARA\nProjects · Areas\nResources · Archives"]
        ZK["ZETTELKASTEN\nAddressable Linked Ideas"]
    end

    subgraph AGENTS["Agent context methods"]
        WIKI["LLM WIKI\nPersistent Maintained Synthesis"]
        ICM["ICM / MWP\nStages · Routing · Handoffs"]
    end

    subgraph STANDARDS["Open Standards & Ecosystem Conventions"]
        AGENTSMD["AGENTS.md\nSSOT · Scoped \n Portable Instructions"]
        SKILLSMD["SKILL.md\nFocused Capabilities"]
    end

    subgraph FRAMEWORKS["Frameworks and Methodologies"]
        FAA["Enterprise scaling\nSAFe · LeSS · DA"]
        FAB["Team delivery methods\nScrum · Kanban · DSDM · FDD · ASD · XP"]
        FAC["SE approaches\nTDD · MDE · RAD · IID · Lean SD · RUP / UP"]
        FAD["Process discipline\nPSP · TSP"]
        FAE["Delivery lifecycle\nDevOps"]
        FAF["Method engineering\nSEMAT"]
    end
```

```mermaid
flowchart TB
    CCA["CCA\nComposition + interoperability semantics"]

    FRAMEWORKS --> CCA
    METHODOLOGIES --> CCA
    STANDARDS --> CCA
    PRINCIPLES --> CCA
    AGENTS --> CCA
    HUMANS --> CCA

    CCA --> BRAIN["PKM / Second brains"]
    CCA --> CODE["Coding projects"]
    CCA --> RESEARCH["Research systems"]
    CCA --> CLIENT["Client workspaces"]
    CCA --> HYBRID["Hybrid workspaces"]
```

> While CCA’s foundational principles come from software engineering, **human principles should always take precedence**.
> Enforcing those principles is outside CCA’s scope and level of abstraction. CCA is not a doctrine. Use judgment and adapt to context, while keeping one core principle in mind: \
> — **Automation is the means; augmenting human capabilities is the goal.**

See [CCA Advisor skill](skills/cca-advisor/SKILL.md). Documentation lies inside it's references.

## The Compatibility Model

CCA deliberately separates three states:

| State | Meaning |
| --- | --- |
| **Native-compatible** | CCA can consume the upstream workspace without structural migration, and any generated/materially rewritten native profile satisfies that upstream's applicable acceptance surface. |
| **CCA-hardened** | Optional CCA routing, portability, provenance, or maintenance conventions were added without replacing the native profile. |
| **CCA-conformant** | The workspace intentionally adopts the CCA specification. |

An ICM workspace or LLM Wiki does not become “CCA” merely because CCA can understand it.

CCA also distinguishes **native ICM** from **ICM-derived**. A coding repository may borrow numbered stages, stage contracts, or output handoffs because those patterns are useful. That does not make the whole repository a native ICM workspace unless the full applicable ICM profile also passes.

Method overlays such as PARA, Zettelkasten, and BASB do not create additional native compatibility states. They are preserved and composed at their boundaries.

### How context routing works

CCA does not impose one universal router. It preserves the native entry point of the active workspace and adds portable guidance only where useful.

```mermaid
flowchart LR
    U["User intent"] --> N["Native + portable instructions"]
    N --> P{"Workspace boundary"}

    P -->|"Native ICM"| C["Root CONTEXT.md"]
    C --> S["Stage CONTEXT.md"]
    S --> X["Selected references + working artifacts"]
    X --> O["Stage output / human edit surface"]

    P -->|"LLM Wiki / knowledge"| I["Native wiki router / index"]
    I --> W["Relevant maintained synthesis"]
    W --> E["Evidence when verification is needed"]

    P -->|"Coding / method-organized project"| R["Existing filesystem structure"]
    R --> D["Scoped project instructions + relevant files"]

    N --> K["Matching SKILL.md when an operation is needed"]
    K --> Q["Skill-local resources loaded progressively"]
```

The routing principle is the same across forms: **load the smallest context that lets the agent act correctly.**

CCA should infer ordinary filesystem semantics when it can do so safely. It does not need a central YAML manifest merely to restate obvious paths such as Projects, Areas, Resources, Archives, stages, wiki folders, or skill collections.

See [Compatibility Details](docs/compatibility-details.md) for a complete list of how all diferent methodologies and frameworks connect.

### A native ICM stage contract

When the ICM profile is active, CCA preserves the upstream contract shape instead of inventing a near-equivalent variant:

```markdown
## Inputs

| Source         | File/Location               | Section/Scope | Why             |
| -------------- | --------------------------- | ------------- | --------------- |
| Previous stage | `../01-research/output/`    | Full file     | Source material |
| Style guide    | `../../_config/voice.md`    | "Voice Rules" | Tone guidance   |

## Process

1. Read the routed inputs.
2. Perform the stage's single job.
3. Run applicable checkpoints/audits.
4. Write the declared output.

## Outputs

| Artifact | Location                  | Format   |
| -------- | ------------------------- | -------- |
| Brief    | `output/example-brief.md` | Markdown |
```

The full native ICM profile includes more than this contract; see [`docs/standards.md`](docs/standards.md) and the upstream ICM conventions before claiming complete compatibility.

## The Validation Model

Validation follows the active profile instead of imposing the strictest known schema on everything.

```mermaid
flowchart TD
    A["Detect actual workspace profile + method boundaries"]
    A --> I["Native ICM?"]
    A --> L["Native LLM Wiki?"]
    A --> D["ICM-derived patterns?"]
    A --> C["Intentional CCA conformance?"]
    A --> M["Method overlays?"]

    I --> IV["Full applicable ICM + workspace-builder acceptance"]
    L --> LV["Validate native maintained-knowledge behavior"]
    D --> DV["Validate borrowed patterns only"]
    C --> CV["Validate adopted CCA requirements"]
    M --> MV["Check locally declared boundary preservation\nnot a native compatibility profile"]

    IV --> W["CCA fresh-agent walk test"]
    LV --> W
    DV --> W
    CV --> W
    MV --> W
```

The walk test asks whether a fresh agent with no chat memory can **orient, act, and report** from the durable workspace. It is useful across profiles, but it never overrides stricter upstream acceptance criteria.

## The CCA skill suite

CCA ships seven focused Agent Skills as one capability suite, following software engineering fundamentals and the key design principles of Agent Skills open standard:

| Skill | Purpose |
| --- | --- |
| [`cca-advisor`](skills/cca-advisor/) | Priors and judgment guidance for engineering work: artifact design, delivery process, adversarial security reasoning, agent and autonomous system design, learned-system practice, and escalation boundaries. |
| [`cca-architect`](skills/cca-architect/) | Design/restructure compound workspaces, choose forms, preserve boundaries, and coordinate focused CCA operations. |
| [`cca-scaffold`](skills/cca-scaffold/) | Add the smallest useful routing/context layer without restructuring existing content. |
| [`cca-sync`](skills/cca-sync/) | Reconcile routing/navigation with disk while preserving scope and native semantics. |
| [`cca-ingest`](skills/cca-ingest/) | Integrate new evidence into maintained knowledge using the workspace's own schema. |
| [`cca-query`](skills/cca-query/) | Query maintained synthesis and verify against source evidence as needed. |
| [`cca-lint`](skills/cca-lint/) | Validate the correct native/conformance profile and separate failures, method-preservation findings, and optional hardening. |

The split exists for precise triggering and progressive disclosure. `cca-architect` is the primary entry point for **compound architecture** questions, not a mandatory router for every request. A direct lint request should activate `cca-lint`; a direct ingest request should activate `cca-ingest`.

Cross-skill coordination uses semantic capability names such as `Use cca-lint to validate the selected profile`. A skill must not reach into a sibling skill directory or repository-global implementation file by relative path.

> These skills are not mandatory, neither they are a requirement, they were created only to make the process more efficient and simple.

```mermaid
flowchart TB
    CCA["CCA semantics"]

    CCA --> J["Judgment"]
    CCA --> A["Architecture"]
    CCA --> M["Maintenance"]
    CCA --> V["Validation"]

    J --> ADV["cca-advisor"]
    A --> ARCH["cca-architect"]
    A --> SC["cca-scaffold"]

    M --> SY["cca-sync"]
    M --> IN["cca-ingest"]
    M --> QU["cca-query"]

    V --> LI["cca-lint"]
```

> See the detailed visualization in [method composition](docs/method-composition.md)

## Getting started

You do not need to install a CCA runtime. Use the repository/files with an agent that can read them. When using the first-party CCA Agent Skills, install/distribute the **CCA skill suite** so focused capabilities can be discovered progressively.

### I already have an ICM workspace

Keep it as ICM. Do not rename stages, replace `CLAUDE.md`, rewrite contracts, or move references merely to satisfy CCA.

Use `cca-lint` in **ICM native compatibility** mode. Add CCA hardening only after native validation passes.

### I already have an LLM Wiki

Keep its schema and maintenance model. Use `cca-lint` in **LLM Wiki native compatibility** mode. Add optional CCA routing/provenance conventions only when they solve a real problem.

### I already use PARA, Zettelkasten, BASB, or another second-brain method

Keep it. Use `cca-architect` when you want to connect/restructure several methods or introduce nested workflow/knowledge boundaries. CCA should preserve the existing method and add only the routing needed for agents to understand it.

### I already have a coding project

Use `cca-scaffold` in its default quick mode. A useful change may be only a root `AGENTS.md` plus scoped instructions for subtrees. `CONTEXT.md`, stages, a wiki, `_config/`, or other structures are optional.

Do not reorganize application code around CCA unless the user explicitly wants restructuring.

### I want to build a new workspace

Use `cca-architect`. Describe the real workflow/knowledge problem first; let the form follow from it.

If you want a complete ICM workspace, request the **full native ICM profile**. If you only want sequential stage contracts inside another repository, request **ICM-derived stages** instead.

Read [`docs/getting-started.md`](docs/getting-started.md) for detailed paths, [`docs/method-composition.md`](docs/method-composition.md) for method composition.

See [FAQ](docs/faq.md) for a detailed list of common questions, doubts and concerns, including:

- Can all of them coexist in one workspace?
- Can CCA work with Claude Code, Codex, Cursor, Gemini, Copilot, and other agents?
- Can I use CCA with Obsidian?
- Can I use it in VS Code or another editor?
- Does a second brain need ICM?
- Does CCA require MCP, Git, a database, or a vector store?
- Does every workspace need CONTEXT.md, stages, or a wiki?
- How do AGENTS.md and CLAUDE.md coexist?
- How do BASB, PARA, Zettelkasten, LLM Wiki, and ICM fit together?
- How does CCA fit into multi-agent systems?
- What if I already have a coding project?
- Why are the seven CCA skills a suite rather than one giant skill?

## Design principles

1. **Convergence over invention.** \
    Adopt current standards/upstream shapes rather than minting competing ones.
2. **Plain files as the durable interface.** \
    Humans and agents can inspect the same state.
3. **Route the right context.** \
    Selective loading beats indiscriminate loading.
4. **One fact, one canonical home.** \
    Link instead of duplicating authoritative rules.
5. **Use structure only when it earns its cost.** \
    No mandatory pipeline/wiki/database for cosmetic consistency.
6. **Preserve native semantics before hardening.** \
    Compatibility comes before optional CCA improvements.
7. **Compose boundaries; do not flatten methods.** \
    Outer organization must not silently rewrite nested native semantics.
8. **Infer structure before declaring metadata.** \
    Do not mirror obvious filesystem paths into a central manifest without a real need.
9. **Every durable output can be an edit surface.** \
    Human changes remain visible to subsequent operations.
10. **Persistent synthesis when knowledge should compound.** \
    Do not repeatedly rebuild durable understanding when maintaining it is more useful.
11. **Stable context plane, replaceable execution plane.** \
    Models, runtimes, and providers may change without owning durable context.
12. **One runtime, many context-defined specializations.** \
    Focused skills and routed context specialize a general agent progressively.
13. **Optional infrastructure stays optional.** \
    Databases, vector stores, MCP, collaboration, and orchestration extend the system; they do not define CCA.
14. **Automation is infrastructure; augmentation is the objective.** \
    The workspace should increase human leverage without making its state opaque.

See [PRINCIPLES](docs/design-principles.md) for the extended rationale.

### Staying compatible as upstreams evolve

The standards tracks the upstream surfaces that materially constrain CCA and separates them from adjacent methodologies/influences. When an upstream changes, CCA should verify the primary source and update the spec, affected skills/templates, examples, compatibility guidance, and validation together.

That maintenance rule is part of the architecture: **compatibility is not a one-time claim.**

See [STANDARDS](docs/standards.md) for the detailed description.

### Why plain files matter

#### Portability

A filesystem-native workspace can be copied, versioned, inspected, edited, or handed to another compatible agent without requiring a proprietary state store. CCA treats databases, vector indexes, MCP servers, and orchestration as optional infrastructure around the durable workspace rather than prerequisites for understanding it.

For Agent Skills, portability means implementation file references remain inside the skill package and installation layout is not part of the capability contract. It does **not** mean every CCA skill must be an unrelated standalone product.

#### Observability

Instructions, references, intermediate artifacts, and maintained knowledge remain visible as files. When a result is wrong, a human can inspect the exact router, contract, reference, or prior artifact involved instead of relying on an opaque runtime state.

#### Human augmentation

Automation is infrastructure; augmentation is the objective. Durable edit surfaces let agents handle repetitive context/navigation work while humans retain the ability to inspect, steer, revise, and veto the state that subsequent operations consume.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md).

> Compatibility and composition changes should cite the relevant primary upstream/method source and update the full affected surface in one change.

## References

See [REFERENCES](docs/references.md) for the complete list of all referenced sources.

## Citation

Citation metadata is provided in [CITATION](CITATION.cff).

## License

MIT. See [LICENSE](LICENSE).
