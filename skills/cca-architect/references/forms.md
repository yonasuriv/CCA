# Forms: the five workspace shapes

Every CCA workspace is one of five forms — or a composition. Forms recurse:
a stage can contain a workspace; an umbrella's member can be a full pipeline.
Choose the smallest form that carries the work. (Forms adapted from
icm-architect; knowledge bundle aligned with the LLM Wiki pattern.)

## 1. Pipeline

A production line. Sequential stages, numbered folders, human review gates
between them.

```
workspace/
├── AGENTS.md  CONTEXT.md
├── stages/
│   ├── 01_research/   CONTEXT.md  references/  output/
│   ├── 02_draft/      CONTEXT.md  references/  output/
│   └── 03_produce/    CONTEXT.md  references/  output/
├── _config/           voice.md, conventions.md
└── setup/questionnaire.md
```

Use when: the same multi-step workflow runs repeatedly with different input,
and a human should review each step's output. Content production, report
generation, course material, audit procedures.

Failure modes: stages with more than one job; missing Inputs tables; gates
removed "for speed" until quality drifts.

## 2. Umbrella

A portfolio of pipelines under one root catalog. Shared `_config/` at the
top; each member workspace is self-contained.

```
org/
├── AGENTS.md  CONTEXT.md        # routes to members
├── _config/                     # org-wide conventions
├── weekly-report/               # a Pipeline
├── client-onboarding/           # a Pipeline
└── research-digest/             # a Pipeline
```

Use when: several related workflows share conventions and one operator (or
team) runs all of them.

Failure modes: members depending on each other's internals (keep one-way
references: members may read shared `_config/`, never sibling `output/`);
root catalog bloating with member details.

## 3. Record library

Many same-shaped records — people, clients, projects, sessions — each a
folder with the same internal structure, plus a catalog that indexes them.

```
clients/
├── AGENTS.md  CONTEXT.md
├── _config/record-template/
├── acme-corp/        overview.md  sessions/  output/
├── globex/           overview.md  sessions/  output/
└── index.md                     # every record, one line each
```

Use when: work is per-entity rather than per-run ("prepare for the Acme
call", "update the Globex file").

Failure modes: records drifting out of shape (enforce the template);
catalog staleness (sync often).

## 4. Knowledge bundle

A navigable, maintained brain — the LLM Wiki pattern. Immutable sources,
agent-owned synthesis, index and log.

```
brain/
├── AGENTS.md  CONTEXT.md        # schema + routing
├── raw/                         # sources, immutable
├── wiki/
│   ├── overview.md
│   ├── entities/  concepts/  syntheses/
│   └── index.md
└── log.md
```

Use when: knowledge accumulates over weeks or months and must compound —
research programs, competitive analysis, personal knowledge, team memory.
Operations are ingest / query / lint, not staged runs.

Failure modes: summaries-per-source instead of integrated pages; lost
provenance; contradictions silently overwritten; index drift.

## 5. Context map

An organization or domain expressed as a graph of linked files — a partial
machine-readable model of how the environment operates, maintained for
orientation rather than production. Model it as nodes and edges: nouns as
nodes (people, teams, systems, projects, decisions, concepts), verbs as
edges (owns, uses, depends-on, produces, supersedes). Workflows are
first-class nodes with their own folders, not prose buried in other
documents. The graph lives in markdown links and frontmatter — no graph
database required until scale demands it.

```
map/
├── AGENTS.md  CONTEXT.md
├── areas/       # domains, teams, systems — one page per node
├── workflows/   # processes as first-class entities (inputs/outputs/owner)
├── decisions/   # ADRs and why
├── interfaces/  # how the nodes connect
└── index.md
```

Use when: the primary need is orientation — new agents (or humans) must
quickly learn what exists, who owns it, what depends on what, and which
artifact is authoritative. Relationship claims carry provenance (current
docs vs. stale chat message vs. inference) and `status:` frontmatter, so
superseded structure is archived, not deleted.

Failure modes: duplicating content that belongs in the mapped systems
(point, don't copy); no owner per node; relationships asserted without
provenance; accumulating without archival until the map becomes a junk
drawer.

## Composition

The most common real-world shape is **Knowledge bundle + Pipeline**: the
wiki accumulates domain knowledge; a pipeline periodically compiles it into
a product (brief, digest, report). Wire it by having stage contracts list
`wiki/` pages and `raw/` sources in their Inputs tables, and having the
pipeline's final stage file its product back into the wiki. See
`examples/topic-research/` in the CCA repo.

Rule of thumb: if the work is *making the same thing repeatedly*, start from
Pipeline. If it is *knowing more over time*, start from Knowledge bundle. If
it is *many of the same thing*, Record library. If it is *several workflows
under one roof*, Umbrella. If it is *understanding a system*, Context map.
