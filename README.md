# Convergent Context Architecture

> **CCA is an agent-agnostic interoperability layer for filesystem-native AI context. It makes ICM workspaces, LLM Wikis, AGENTS.md, Agent Skills, existing projects, and human knowledge-work methods easier to use together without forcing them into a new competing convention.**

CCA provides shared semantics, focused portable operations, and compatibility rules so durable context can remain understandable across agents, tools, editors, and runtimes.

It is not a replacement for ICM, LLM Wiki, AGENTS.md, Agent Skills, PARA, Zettelkasten, Building a Second Brain, MCP, or an agent runtime. Its core rule is: **when an upstream convention or existing method already solves the problem, preserve it.**

---

## Why CCA exists

Agent context is increasingly stored in ordinary repositories: instructions, task routers, stage contracts, source material, maintained knowledge, skills, configuration, and working artifacts. Human knowledge systems also already have useful ways to organize and develop that material. The problem is not that they need one universal replacement; it is that different boundaries are interpreted differently by different agents.

ICM provides a filesystem architecture for staged, human-reviewable workflows. LLM Wiki provides a pattern for persistent knowledge that compounds across sessions. AGENTS.md provides portable repository instructions. Agent Skills provide focused portable capabilities. PARA, Zettelkasten, and Building a Second Brain address human organization, idea development, and knowledge-work lifecycle. Existing coding repositories already have their own structure and conventions.

CCA defines the shared ground between them so an agent can answer five questions without forcing a migration:

1. **What kind of workspace or boundary is this?**
2. **Which upstream conventions or methods already govern it?**
3. **What context should I load for this task?**
4. **Which capability should perform the operation?**
5. **What can I add without breaking native semantics?**

The objective is not to make every workspace look the same. The objective is to make different valid workspace forms **interoperable, navigable, and portable**.

## The convergence model

CCA composes several different layers. They are not all the same kind of standard.

```mermaid
flowchart TB
    subgraph HUMAN["Human knowledge-work methods"]
        BASB["BASB / CODE\nCapture · Organize · Distill · Express"]
        PARA["PARA\nProjects · Areas · Resources · Archives"]
        ZK["Zettelkasten\nAddressable linked ideas"]
    end

    subgraph CONTEXT["Agent context methods"]
        ICM["ICM / Model Workspace Protocol\nStages · routing · handoffs"]
        WIKI["LLM Wiki\nPersistent maintained synthesis"]
    end

    subgraph STANDARDS["Ecosystem conventions"]
        AGENTS["AGENTS.md\nScoped portable instructions"]
        SKILLS["Agent Skills / SKILL.md\nFocused capabilities"]
    end

    CCA["CCA\nComposition + interoperability semantics"]

    BASB --> CCA
    PARA --> CCA
    ZK --> CCA
    ICM --> CCA
    WIKI --> CCA
    AGENTS --> CCA
    SKILLS --> CCA

    CCA --> CODE["Coding projects"]
    CCA --> BRAIN["Second brains / PKM"]
    CCA --> CLIENT["Client workspaces"]
    CCA --> RESEARCH["Research systems"]
    CCA --> HYBRID["Hybrid workspaces"]
```

If an upstream changes, CCA should change toward it rather than freezing a near-compatible fork. Human methodologies remain method overlays unless CCA deliberately adopts a concrete machine-facing contract from them in a future revision.

## How the methods fit together

A concise mental model:

- **BASB/CODE** tells the human how knowledge moves: Capture → Organize → Distill → Express.
- **PARA** tells the human where actionable material belongs: Projects, Areas, Resources, Archives.
- **Zettelkasten** supports idea-level knowledge development through addressable linked notes.
- **LLM Wiki** tells the agent how persistent maintained synthesis can compound across sessions.
- **ICM/MWP** tells the agent how sequential work is routed through stages, contracts, selective context, and durable handoffs.
- **AGENTS.md** gives compatible agents scoped operating guidance.
- **Agent Skills** package focused capabilities with progressive disclosure.
- **CCA** defines how those boundaries coexist without one convention silently swallowing another.

PARA, Zettelkasten, and BASB are **method overlays**, not CCA native compatibility profiles. The core composition rule is:

> **Nest boundaries; do not merge schemas merely because they coexist.**

For example, an outer PARA workspace can contain an ordinary coding repository, a native ICM client workflow, Zettelkasten notes, and an LLM Wiki. If one nested directory is a native ICM root, an ICM-only consumer must still be able to open that directory and operate it as ICM.

Read [`docs/method-composition.md`](docs/method-composition.md) for the full model and [`spec/method-composition.md`](spec/method-composition.md) for the normative rules.

## What CCA is, and what is not

CCA **is**:

- a compatibility and composition layer for filesystem-native agent context;
- a set of shared semantics for routing, durable knowledge, handoffs, authority boundaries, and portability;
- a focused Agent Skills suite for designing, scaffolding, maintaining, querying, and validating workspaces;
- a way to add cross-agent guidance without destroying native tool behavior;
- a framework for deciding when to preserve, harden, intentionally conform, or simply compose existing methods.

CCA **is not**:

- an agent runtime or orchestration framework;
- a real-time multi-agent message bus;
- a scheduler or queue;
- a vector database or retrieval engine;
- a replacement for MCP;
- a replacement for ICM, LLM Wiki, PARA, Zettelkasten, or BASB;
- a requirement that every repository use stages, a wiki, `CONTEXT.md`, a giant manifest, or one fixed directory tree.

## Compatibility model

CCA deliberately separates three states:

| State | Meaning |
|---|---|
| **Native-compatible** | CCA can consume the upstream workspace without structural migration, and any generated/materially rewritten native profile satisfies that upstream's applicable acceptance surface. |
| **CCA-hardened** | Optional CCA routing, portability, provenance, or maintenance conventions were added without replacing the native profile. |
| **CCA-conformant** | The workspace intentionally adopts the CCA specification. |

An ICM workspace or LLM Wiki does not become “CCA” merely because CCA can understand it.

CCA also distinguishes **native ICM** from **ICM-derived**. A coding repository may borrow numbered stages, stage contracts, or output handoffs because those patterns are useful. That does not make the whole repository a native ICM workspace unless the full applicable ICM profile also passes.

Method overlays such as PARA, Zettelkasten, and BASB do not create additional native compatibility states. They are preserved and composed at their boundaries.

## How context routing works

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

## ICM compatibility

CCA accepts a valid ICM workspace without requiring it to migrate into a CCA directory structure.

For native ICM, CCA preserves the ICM concepts it depends on: the five-layer routing architecture, native `CLAUDE.md`, root/stage `CONTEXT.md`, exact stage contracts, selective section loading, one-way dependencies, canonical sources, numbered stage folders, human-editable `output/` handoffs, onboarding, quality gates, and other applicable upstream patterns.

A native ICM root may live inside a broader CCA, PARA, client, or coding workspace. The outer structure may determine where it lives; it must not rewrite the ICM internals merely for consistency.

### Does CCA conflict with ICM's workspace-builder?

It should not.

The ICM workspace-builder is itself an ICM workspace whose output is a new validated ICM workspace. CCA treats upstream ICM `_core/CONVENTIONS.md` as the canonical semantic authority and the workspace-builder's final validation stage as the practical acceptance checklist for generated ICM workspaces.

CCA can provide a different architecture/scaffolding interaction, but if the result claims **native ICM compatibility**, it should pass the same applicable upstream acceptance surface. CCA's fresh-agent walk test is an additional portability check, not a replacement for ICM validation.

```mermaid
flowchart LR
    A["Create or modify native ICM workspace"] --> C["Apply current ICM conventions"]
    C --> V["Run workspace-builder-equivalent validation"]
    V -->|"Pass"| W["Run CCA fresh-agent walk test"]
    V -->|"Fail"| F["Fix native ICM issues first"]
    F --> V
    W --> H["Optionally add CCA hardening"]
```

If CCA documentation and current upstream ICM ever disagree, upstream ICM wins and CCA should be updated.

## LLM Wiki compatibility

CCA preserves LLM Wiki as an intentionally flexible idea pattern: durable source material plus maintained LLM-owned synthesis that compounds across sessions.

CCA may recommend stronger organization when useful, for example an index, provenance metadata, lifecycle fields, contradiction tracking, or a `raw/` + `wiki/` split, but these are **CCA hardening choices**, not universal requirements of LLM Wiki.

A pre-existing LLM Wiki should be understood through its own schema and maintenance instructions before CCA adds anything. It may live inside a PARA Resources tree or beside Zettelkasten notes without being structurally merged with them.

## Choose the smallest workspace form

CCA starts from the work, not from a preferred tree.

| Need | Good starting form |
|---|---|
| Repeatable sequential workflow with explicit human handoffs | **Full native ICM pipeline** if you want complete ICM semantics, or **ICM-derived stages** if you only need the stage-contract pattern inside another project |
| Knowledge that should compound across sessions | **LLM Wiki-style maintained knowledge** |
| Human PKM / second brain | Keep the useful **PARA / Zettelkasten / BASB** organization and add agent routing only where it earns its cost |
| Existing software repository | **Keep the existing repository**, add only useful portable/scoped routing |
| Several valid methods/profiles in one workspace | **Hybrid** with explicit nested boundaries |
| Real-time agent-to-agent coordination | Use an orchestration/message-passing system; CCA may provide the durable shared context beneath it |

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

Read [`docs/getting-started.md`](docs/getting-started.md) for detailed paths, [`docs/method-composition.md`](docs/method-composition.md) for method composition, and [`docs/faq.md`](docs/faq.md) for common questions about Obsidian, VS Code, coding projects, second brains, MCP, databases, nested `AGENTS.md`, multi-agent work, and more.

## A native ICM stage contract

When the ICM profile is active, CCA preserves the upstream contract shape instead of inventing a near-equivalent variant:

```markdown
## Inputs

| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Previous stage | `../01-research/output/` | Full file | Source material |
| Style guide | `../../references/voice.md` | "Voice Rules" | Tone guidance |

## Process

1. Read the routed inputs.
2. Perform the stage's single job.
3. Run applicable checkpoints/audits.
4. Write the declared output.

## Outputs

| Artifact | Location | Format |
|---|---|---|
| Brief | `output/example-brief.md` | Markdown |
```

The full native ICM profile includes more than this contract; see [`docs/standards.md`](docs/standards.md) and the upstream ICM conventions before claiming complete compatibility.

## Why plain files matter

### Portability

A filesystem-native workspace can be copied, versioned, inspected, edited, or handed to another compatible agent without requiring a proprietary state store. CCA treats databases, vector indexes, MCP servers, and orchestration as optional infrastructure around the durable workspace rather than prerequisites for understanding it.

For Agent Skills, portability means implementation file references remain inside the skill package and installation layout is not part of the capability contract. It does **not** mean every CCA skill must be an unrelated standalone product.

### Observability

Instructions, references, intermediate artifacts, and maintained knowledge remain visible as files. When a result is wrong, a human can inspect the exact router, contract, reference, or prior artifact involved instead of relying on an opaque runtime state.

### Human augmentation

Automation is infrastructure; augmentation is the objective. Durable edit surfaces let agents handle repetitive context/navigation work while humans retain the ability to inspect, steer, revise, and veto the state that subsequent operations consume.

## Where CCA works well

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

## Where CCA is not enough

CCA deliberately does not solve every systems problem.

**Real-time multi-agent collaboration**: agents communicating dynamically in tight loops need message-passing/orchestration infrastructure.

**High-concurrency shared services**: need queueing, isolation, locking/transactions, deployment, and other runtime concerns.

**Complex automated branching or scheduling** may need a workflow engine. CCA can still store the durable context and contracts that such a runtime consumes.

**Large-scale retrieval** may benefit from databases, embeddings, indexes, or graph systems. Those are compatible extensions as long as the durable workspace remains understandable without treating the external index as the only source of truth.

## CCA skill suite

CCA ships six focused Agent Skills as one capability suite:

| Skill | Purpose |
|---|---|
| [`cca-architect`](skills/cca-architect/) | Design/restructure compound workspaces, choose forms, preserve boundaries, and coordinate focused CCA operations. |
| [`cca-scaffold`](skills/cca-scaffold/) | Add the smallest useful routing/context layer without restructuring existing content. |
| [`cca-sync`](skills/cca-sync/) | Reconcile routing/navigation with disk while preserving scope and native semantics. |
| [`cca-ingest`](skills/cca-ingest/) | Integrate new evidence into maintained knowledge using the workspace's own schema. |
| [`cca-query`](skills/cca-query/) | Query maintained synthesis and verify against source evidence as needed. |
| [`cca-lint`](skills/cca-lint/) | Validate the correct native/conformance profile and separate failures, method-preservation findings, and optional hardening. |

The split exists for precise triggering and progressive disclosure. `cca-architect` is the primary entry point for **compound architecture** questions, not a mandatory router for every request. A direct lint request should activate `cca-lint`; a direct ingest request should activate `cca-ingest`.

Cross-skill coordination uses semantic capability names such as `Use cca-lint to validate the selected profile`. A skill must not reach into a sibling skill directory or repository-global implementation file by relative path.

```mermaid
flowchart TD
    U["User intent"]
    U -->|"Design / combine methods / restructure"| A["cca-architect"]
    U -->|"Add routing/context"| S["cca-scaffold"]
    U -->|"Repair stale navigation"| Y["cca-sync"]
    U -->|"Integrate evidence"| I["cca-ingest"]
    U -->|"Query knowledge"| Q["cca-query"]
    U -->|"Validate"| L["cca-lint"]

    A --> M["Lazy-load forms / methods / compatibility references"]
    A -. "semantic delegation" .-> S
    A -. "semantic delegation" .-> Y
    A -. "semantic delegation" .-> I
    A -. "semantic delegation" .-> Q
    A -. "semantic delegation" .-> L
```

## Validation model

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

## Repository layout

The CCA repository separates normative specification, explanatory guidance, focused skills, examples, and validation tooling:

```text
CCA/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── CONTRIBUTING.md
├── CITATION.cff
├── spec/
│   ├── SPEC.md
│   ├── compatibility.md
│   ├── method-composition.md
│   └── adapters.md
├── docs/
│   ├── getting-started.md
│   ├── faq.md
│   ├── method-composition.md
│   ├── migration.md
│   ├── principles.md
│   └── standards.md
├── skills/
│   ├── cca-architect/
│   ├── cca-scaffold/
│   ├── cca-sync/
│   ├── cca-ingest/
│   ├── cca-query/
│   └── cca-lint/
├── examples/
│   └── topic-research/
└── scripts/
    └── validate_repo.py
```

## Design principles

1. **Convergence over invention.** Adopt current standards/upstream shapes rather than minting competing ones.
2. **Plain files as the durable interface.** Humans and agents can inspect the same state.
3. **Route the right context.** Selective loading beats indiscriminate loading.
4. **One fact, one canonical home.** Link instead of duplicating authoritative rules.
5. **Use structure only when it earns its cost.** No mandatory pipeline/wiki/database for cosmetic consistency.
6. **Preserve native semantics before hardening.** Compatibility comes before optional CCA improvements.
7. **Compose boundaries; do not flatten methods.** Outer organization must not silently rewrite nested native semantics.
8. **Infer structure before declaring metadata.** Do not mirror obvious filesystem paths into a central manifest without a real need.
9. **Every durable output can be an edit surface.** Human changes remain visible to subsequent operations.
10. **Persistent synthesis when knowledge should compound.** Do not repeatedly rebuild durable understanding when maintaining it is more useful.
11. **Stable context plane, replaceable execution plane.** Models, runtimes, and providers may change without owning durable context.
12. **One runtime, many context-defined specializations.** Focused skills and routed context specialize a general agent progressively.
13. **Optional infrastructure stays optional.** Databases, vector stores, MCP, collaboration, and orchestration extend the system; they do not define CCA.
14. **Automation is infrastructure; augmentation is the objective.** The workspace should increase human leverage without making its state opaque.

See [`docs/principles.md`](docs/principles.md) for the extended rationale.

## Staying compatible as upstreams evolve

[`docs/standards.md`](docs/standards.md) tracks the upstream surfaces that materially constrain CCA and separates them from adjacent methodologies/influences. When an upstream changes, CCA should verify the primary source and update the spec, affected skills/templates, examples, compatibility guidance, and validation together.

That maintenance rule is part of the architecture: **compatibility is not a one-time claim.**

## FAQ

The full FAQ is in [`docs/faq.md`](docs/faq.md), including:

- How do BASB, PARA, Zettelkasten, LLM Wiki, and ICM fit together?
- Can all of them coexist in one workspace?
- Does a second brain need ICM?
- Why are the six CCA skills a suite rather than one giant skill?
- Can I use CCA with Obsidian?
- Can I use it in VS Code or another editor?
- What if I already have a coding project?
- Does every workspace need `CONTEXT.md`, stages, or a wiki?
- How do `AGENTS.md` and `CLAUDE.md` coexist?
- Can CCA work with Claude Code, Codex, Cursor, Gemini, Copilot, and other agents?
- Does CCA require MCP, Git, a database, or a vector store?
- How does CCA fit into multi-agent systems?

## References

- **[ICM / Model Workspace Protocol](https://github.com/RinDig/Interpretable-Context-Methodology)**: Jake Van Clief & David McDermott \
    [Interpretable Context Methodology: Folder Structure as Agent Architecture Paper](https://arxiv.org/pdf/2603.16021)
- **[LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)**: Andrej Karpathy's idea pattern for LLM-maintained persistent knowledge bases
- **[AGENTS.md](https://agents.md)**: portable agent instructions
- **[Agent Skills](https://agentskills.io)**: portable `SKILL.md` packages
- **[PARA / Building a Second Brain](https://fortelabs.com/para/)**: action-oriented organization and broader knowledge-work methodology
- **[Niklas Luhmann Archive](https://niklas-luhmann-archiv.de/)**: primary archive for Luhmann's Zettelkasten and its linking/navigation practices

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Compatibility and composition changes should cite the relevant primary upstream/method source and update the full affected surface in one change.

Run the repository validator before submitting changes:

```bash
python scripts/validate_repo.py
```

## Citation

Citation metadata is provided in [`CITATION.cff`](CITATION.cff).

## License

MIT. See [`LICENSE`](LICENSE).
