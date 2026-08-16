# Getting started

CCA is a filesystem-native interoperability layer for agent context. You do not install a runtime to use it. Start from the workspace you already have, then add only the structure that improves routing or portability.

CCA's first-party Agent Skills are intended as a **suite of focused capabilities**. `cca` in `architect` mode handles compound workspace-design questions; direct lint, ingest, query, sync, or scaffold requests can route straight to their focused skill.

## Choose your starting point

```mermaid
flowchart TD
    A["What do you already have?"]
    A -->|"ICM workspace"| B["Keep the ICM structure unchanged"]
    A -->|"LLM Wiki"| C["Keep the wiki implementation unchanged"]
    A -->|"PARA / Zettelkasten / BASB / second brain"| P["Preserve the method and identify nested boundaries"]
    A -->|"Coding project / existing repo"| D["Add portable routing in place"]
    A -->|"New workflow or knowledge space"| E["Design the smallest suitable workspace"]

    B --> F["Validate full native ICM profile"]
    C --> G["Validate native wiki behavior"]
    P --> I["Use cca-architect for composition changes"]
    D --> H["Use `scaffold` mode"]
    E --> I

    F --> J["Optionally add CCA hardening"]
    G --> J
    H --> K["Use `lint` mode for adopted profiles"]
    I --> K
    K --> J
```

## 1. Existing ICM workspace

Do **not** rename stages, rewrite contracts, relocate references, or replace native `CLAUDE.md` behavior just to satisfy CCA. Native ICM structure is accepted as-is when it satisfies the current upstream ICM profile.

For broader agent portability, you may add a root `AGENTS.md` that routes agents into the existing ICM files while keeping `CLAUDE.md` available for ICM/Claude consumers. Do not duplicate substantive rules between them.

If you create or materially rewrite an ICM workspace, native compatibility means more than stage naming. Validate the complete applicable current ICM surface: five-layer routing, root/stage contracts, naming, output handoffs, one-way references, selective loading, `setup`/`status`, questionnaire behavior, placeholder coverage, applicable checkpoints/audits/spec/value/shared-constant patterns, tool prerequisites, quality guardrails, and workspace-builder-equivalent validation.

For new stages, keep ICM's canonical naming and contract conventions:

```text
stages/
├── 01-collect/
│   ├── CONTEXT.md
│   └── output/
└── 02-brief/
    ├── CONTEXT.md
    └── output/
```

Each stage contract keeps the ICM `Inputs` / `Process` / `Outputs` shape and uses selective section routing.

### What about ICM's workspace-builder?

CCA does not replace it and should not conflict with it.

The upstream workspace-builder is itself an ICM workspace whose output is a validated ICM workspace. For a **native ICM** claim, CCA treats upstream `_core/CONVENTIONS.md` as canonical and the workspace-builder's final validation stage as the practical acceptance checklist. If CCA's local description drifts, upstream ICM wins and CCA should be updated.

A CCA tool may build the same kind of workspace through a different user interaction, but the resulting native ICM workspace should pass the same applicable acceptance surface.

## 2. Existing LLM Wiki

Keep the implementation you already have. Karpathy's LLM Wiki is intentionally an idea pattern whose concrete schema and layout are built with the agent/user.

CCA can recognize common concepts such as durable evidence, maintained synthesis, navigation, and maintenance procedures, but it must not require CCA-specific frontmatter, page taxonomy, log syntax, or directory names for native LLM Wiki compatibility.

Add CCA hardening only when useful: portable `AGENTS.md` routing, stronger provenance conventions, lifecycle metadata, or a pipeline that consumes the wiki.

## 3. Existing PARA, Zettelkasten, BASB, or second brain

Keep it. These are **method overlays**, not structures CCA needs to replace.

- **PARA** can remain the outer organization for Projects, Areas, Resources, and Archives.
- **Zettelkasten** notes can remain linked idea-level knowledge; do not assume agents may rewrite them.
- **BASB/CODE** can remain the human lifecycle across Capture, Organize, Distill, and Express.
- **LLM Wiki** can coexist as maintained agent synthesis where that is useful.
- **ICM** can exist as a nested workflow boundary for repeatable staged work.

A typical hybrid may look like:

```text
workspace/
├── AGENTS.md
├── Projects/
│   ├── software-project/
│   │   ├── AGENTS.md
│   │   ├── src/
│   │   └── tests/
│   └── client-work/
│       └── assessment/
│           ├── CLAUDE.md
│           ├── CONTEXT.md
│           └── stages/
├── Areas/
├── Resources/
│   └── knowledge/
│       ├── zettelkasten/
│       └── llm-wiki/
└── Archives/
```

The key rule is **nest boundaries; do not merge schemas merely because they coexist**. If `assessment/` is a native ICM root, validate and operate that directory as ICM even though PARA determines where it lives.

Use `cca` in `architect` mode when you want to design/restructure this composition. Read [`method-composition.md`](method-composition.md) for the full model.

## 4. Existing coding project

Use `cca` in `scaffold` mode in quick mode. It should add context routing without reorganizing application code.

A minimal result may be:

```text
project/
├── AGENTS.md          # portable project instructions and routing
├── CONTEXT.md         # optional task/context router
├── src/
├── tests/
└── ...existing files
```

Add `_config/`, references, a wiki, or stages only when the project actually needs them.

Nested `AGENTS.md` files may be used for subprojects or packages. Follow the AGENTS.md standard: the closest applicable file wins.

If you add numbered ICM-style stages to a coding repository but do not implement the full ICM profile, describe them as **ICM-derived stage contracts** rather than calling the whole repository native ICM-compatible.

## 5. New workspace

Use `cca` in `architect` mode and start from the work, not from a preferred folder tree.

Choose the smallest form that fits:

- **Full native ICM pipeline** for a repeatable sequential workflow when you want complete ICM compatibility, including its onboarding and validation model.
- **ICM-derived pipeline** when explicit stages/handoffs help but the host project does not need the complete ICM workspace profile.
- **Knowledge bundle** for persistent synthesis that compounds across sessions.
- **Method-organized PKM/second brain** when PARA, Zettelkasten, BASB, or another human method already expresses the work well.
- **Hybrid** when a pipeline consumes or updates maintained knowledge or when several valid boundaries coexist.
- **Ordinary project routing** when the existing repository structure already expresses the work well.

## Skill routing

CCA uses Agent Skills progressive disclosure rather than one monolithic skill.

```mermaid
flowchart TD
    U["User request"]
    U -->|"Design / combine methods / restructure"| A["cca-architect"]
    U -->|"Add routing/context"| S["cca-scaffold"]
    U -->|"Repair stale navigation"| Y["cca-sync"]
    U -->|"Integrate evidence"| I["cca-ingest"]
    U -->|"Query knowledge"| Q["cca-query"]
    U -->|"Validate"| L["cca-lint"]

    A --> M["Lazy-load forms/method references"]
    A -. "semantic delegation" .-> S
    A -. "semantic delegation" .-> Y
    A -. "semantic delegation" .-> I
    A -. "semantic delegation" .-> Q
    A -. "semantic delegation" .-> L
```

Cross-skill coordination is by semantic skill name, never by reaching into sibling skill directories. Package portability means implementation references stay inside each skill package; the seven CCA modes are intended to be distributed as a suite.

## How CCA routes context

CCA does not require one universal router for every form. It preserves the active profile's native entry points and adds portable routing only when useful.

```mermaid
flowchart LR
    U["User intent"] --> N["Native + portable instructions"]
    N --> P{"Active workspace form"}
    P -->|"Native ICM"| C["Root CONTEXT.md"]
    C --> S["Stage CONTEXT.md"]
    S --> X["Selective references + working artifacts"]
    P -->|"Knowledge workspace"| I["Native wiki router / index"]
    I --> W["Relevant synthesis"]
    W --> E["Evidence when verification is needed"]
    P -->|"Ordinary / method-organized project"| R["Existing structure + scoped instructions"]
    N --> K["Matching SKILL.md when an operation is needed"]
    K --> Q["Skill-local resources loaded as needed"]
```

## Validate before calling it done

Run `cca` in `lint` mode with the correct profile:

- **ICM native compatibility**: verify the complete applicable current ICM profile and workspace-builder-equivalent acceptance surface.
- **ICM-derived patterns**: verify the borrowed stage/routing patterns without pretending the host repository is a full native ICM workspace.
- **LLM Wiki native compatibility**: verify the core maintained-wiki behavior without imposing one concrete implementation.
- **CCA conformance**: verify the additional CCA conventions the workspace intentionally adopted.

PARA, Zettelkasten, and BASB are reported as method overlays/preservation constraints when relevant, not invented native profiles.

Then perform the CCA walk test: a fresh agent should be able to orient, perform a representative operation, and report state using the files alone. The walk test supplements upstream validation; it does not replace it.

## Where CCA fits well

CCA is useful when you want one or more of these properties:

- agent context that survives across sessions and runtimes;
- plain-file state that humans can inspect, edit, diff, and version;
- selective context loading instead of one growing prompt;
- portable instructions and skills without forcing a single agent vendor;
- repeatable staged workflows with durable handoffs;
- persistent maintained knowledge that compounds over time;
- existing PKM/second-brain methods connected to agent workflows without being replaced;
- an existing coding or knowledge repository made easier for agents to navigate without restructuring it.

CCA is less useful when the problem is primarily real-time message passing, high-concurrency orchestration, queueing, scheduling, or a service/database problem. Those can sit above or beside CCA, but CCA does not try to replace them.

## Next reading

- [`../README.md`](../README.md) — project overview, mental model, and compatibility model.
- [`../skills/cca/references/core/spec.md`](../skills/cca/references/core/spec.md) — normative CCA specification.
- [`../skills/cca/references/core/compatibility.md`](../skills/cca/references/core/compatibility.md) — compatibility boundaries.
- [`../skills/cca/references/core/method-composition.md`](../skills/cca/references/core/method-composition.md) — normative method-overlay and skill-suite rules.
- [`method-composition.md`](method-composition.md) — explanatory composition model and examples.
- [`migration.md`](migration.md) — optional hardening/migration paths.
- [`faq.md`](faq.md) — common usage questions.
- [`standards.md`](standards.md) — upstream conventions CCA tracks.


## One skill, seven modes

Install `skills/cca/`. The package is self-contained: its normative CCA semantics,
compatibility rules, architect references, advisor corpus, operation procedures,
templates, and validation material live inside the skill. Modes are selected
lazily so a lint request does not load architecture or advisor material, and an
advice request does not load workspace templates.
