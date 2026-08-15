# Workspace forms

Forms are design heuristics, not compatibility requirements. Choose the smallest shape that improves routing or maintenance. Preserve an existing ICM or LLM Wiki implementation before applying a CCA-preferred form. When PARA, Zettelkasten, BASB/CODE, or other human methods are involved, read [methods.md](methods.md) and preserve them as method overlays rather than forcing them into one CCA tree.

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

When native ICM compatibility is requested, implement the complete applicable current ICM profile: `AGENTS.md` as the authoritative Layer-0 catalog, five-layer routing, root and stage contracts, `setup`/`status` behavior, flat all-at-once questionnaire, naming and placeholder rules, tool prerequisites where needed, applicable checkpoints/audits/spec/value/shared-constant patterns, quality guardrails, and workspace-builder-equivalent validation. Create a harness entry (`CLAUDE.md`) as a single-line `@AGENTS.md` include only when a harness needs it. When operating on an existing upstream workspace, preserve its native `CLAUDE.md` entry path.

Do not reduce that profile to the minimal tree above.

A native ICM pipeline may be nested inside an outer PARA/client/project hierarchy. The outer organization can determine where the ICM root lives but must not rewrite the native ICM internals merely for uniformity.

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

An umbrella can also be method-organized, for example with PARA at the outer level. Treat member workspaces as nested boundaries rather than flattening them into the umbrella schema.

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

A knowledge bundle may coexist beside Zettelkasten notes or inside a PARA Resources tree. Do not silently reinterpret human-authored notes as agent-maintained synthesis; determine authority from the workspace instructions.

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

For the context-map operating model, copy the node and schema starters: `node.md` defines one entity/process card (frontmatter labels, Purpose/Inputs/Process/Outputs, human checks, links), and `schema.md` declares the closed set of node types, labels, and naming rules so the map stays queryable.

Do not create a context map merely to duplicate an already-obvious PARA tree, repository layout, ICM router, or wiki index. Structure should earn its maintenance cost.

## Composition

Forms and method overlays may compose when the work naturally crosses boundaries. A common example is a maintained knowledge base feeding an ICM-derived pipeline inside a broader CCA workspace. A full native ICM profile is also possible, but must satisfy its complete upstream acceptance surface.

```mermaid
flowchart LR
    S["Durable sources"] --> W["Maintained synthesis"]
    W --> P1["01-research"]
    P1 --> P2["02-draft"]
    P2 --> O["Human-editable output"]
    O -. "optional knowledge update" .-> W
```

Another common composition is an outer PARA hierarchy containing coding projects, native ICM roots, Zettelkasten notes, and LLM Wiki synthesis. In that case, **nest boundaries; do not merge schemas merely because they coexist**.

Do not create reverse dependencies merely for symmetry: pipeline stages may consume canonical knowledge, but shared knowledge should not depend on a downstream stage's internals unless the workspace explicitly defines that maintenance operation.


## System Map

Use for mutable code/file/vault systems where change-impact reasoning is the
primary problem. Read `system-map.md`. Do not collapse this into Context Map:
Context Map models organizational/process/data relationships; System Map models
concrete mutable objects, processes, effects, and impact.

## Record Library defaults

For a fresh Record Library, treat the record template as the schema: create new
records by copying it rather than starting blank. Keep identifier/status
authority in one declared catalog when the library uses those fields, define a
small lifecycle only when needed, and detect half-created records or schema drift.
Existing libraries keep their own schema and lifecycle.

## Context Map operational fields

When useful for the actual mapping question, nodes may include `frequency` in
addition to ownership, value, pain, governance, inputs, outputs, and interfaces.
Workshop observations are evidence, not automatically canonical truth. Promote a
pattern only when the workspace's evidence rule is satisfied; three independent
occurrences is a useful default, not a universal law.
