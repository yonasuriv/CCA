# Workspace forms

Forms are design heuristics, not compatibility requirements. Choose the smallest shape that improves routing or maintenance. Preserve an existing ICM or LLM Wiki implementation before applying a CCA-preferred form.

## 1. Pipeline

Use for sequential work with explicit handoffs and review gates.

First choose whether the user needs a **full native ICM workspace** or only **ICM-derived stage contracts** inside another project.

### ICM-derived pipeline

A minimal derived pipeline may look like:

```text
workspace/
├── AGENTS.md                 # optional portable guidance
├── CONTEXT.md                # task router when useful
├── stages/
│   ├── 01-research/
│   │   ├── CONTEXT.md
│   │   ├── references/
│   │   └── output/
│   ├── 02-draft/
│   │   ├── CONTEXT.md
│   │   ├── references/
│   │   └── output/
│   └── 03-produce/
│       ├── CONTEXT.md
│       ├── references/
│       └── output/
└── [stable shared references/configuration]
```

This may borrow ICM naming, contracts, selective routing, one-way dependencies, and output handoffs, but it is **not** a native ICM workspace merely because this tree exists.

### Full native ICM pipeline

When native ICM compatibility is requested, implement the complete applicable current ICM profile: native `CLAUDE.md`, five-layer routing, root and stage contracts, `setup`/`status` behavior, flat all-at-once questionnaire, naming and placeholder rules, tool prerequisites where needed, applicable checkpoints/audits/spec/value/shared-constant patterns, quality guardrails, and workspace-builder-equivalent validation.

Do not reduce that profile to the minimal tree above.

Use pipelines when the same multi-step workflow runs repeatedly and stage boundaries make review or context isolation clearer.

Failure modes: multi-job stages, missing/oversized contracts, downstream-to-upstream back-references, quality rules copied from old outputs instead of canonical references, and partial ICM-derived structures mislabeled as native ICM.

## 2. Umbrella

Use when several independent workspaces share a small amount of top-level guidance.

```text
org/
├── AGENTS.md
├── CONTEXT.md
├── shared/
├── weekly-report/
├── client-onboarding/
└── research-digest/
```

Members may consume shared canonical references. Avoid coupling members to one another's internal working outputs.

## 3. Record library

Use for many same-shaped records such as clients, projects, people, incidents, or sessions.

```text
clients/
├── AGENTS.md
├── index.md
├── record-template/
├── acme-corp/
└── globex/
```

Use an index when it materially improves navigation. Do not force a fixed record schema onto an existing project that already has one.

## 4. Knowledge bundle

Use for maintained knowledge that compounds across sessions.

The LLM Wiki pattern does **not** require one concrete tree. Discover and preserve an existing wiki's own schema.

When starting fresh and the user wants an opinionated CCA-hardened layout, one useful option is:

```text
brain/
├── AGENTS.md
├── raw/
├── wiki/
│   └── index.md
└── log.md
```

Additional entity/concept/source/synthesis directories and metadata are optional implementation choices.

Failure modes: isolated summaries instead of integrated synthesis, invented provenance, silent contradiction overwrite, and indexes that drift from the knowledge they route to.

## 5. Context map

Use when the primary need is orientation across systems, teams, projects, decisions, workflows, or other linked entities.

```text
map/
├── AGENTS.md
├── index.md
├── areas/
├── workflows/
├── decisions/
└── interfaces/
```

Markdown links and lightweight metadata can express relationships without requiring a graph database. Add stronger graph infrastructure only when scale or query needs justify it.

## Composition

Forms may compose when the work naturally crosses boundaries. A common example is a maintained knowledge base feeding an ICM-derived pipeline inside a broader CCA workspace. A full native ICM profile is also possible, but must satisfy its complete upstream acceptance surface.

```mermaid
flowchart LR
    S["Durable sources"] --> W["Maintained synthesis"]
    W --> P1["01-research"]
    P1 --> P2["02-draft"]
    P2 --> O["Human-editable output"]
    O -. "optional knowledge update" .-> W
```

Do not create the reverse dependency merely for symmetry: pipeline stages may consume canonical knowledge, but shared knowledge should not depend on a downstream stage's internals unless the workspace explicitly defines that maintenance operation.
