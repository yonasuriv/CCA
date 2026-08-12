# Design principles behind CCA

Explanatory, not normative. CCA inherits its principles from ICM, from the
LLM Wiki pattern, and from a collection of curated whitepapers on AI system
design. This document distills them and explains how each is encoded in the
architecture.

## Context principles

### 1. Route the right context, not bigger prompts

A better prompt does not compensate for a badly designed context system.
Agent execution = instructions + memory + knowledge + tools + state. The
engineering problem is constructing the right context for this task, at this
moment, within budget — not writing the perfect prompt.

*Encoded as:* the five layers; catalogs that point instead of store;
progressive loading ("load broad context first, specific context only when
relevant"); token budgets per layer; Inputs tables that scope exactly what a
stage reads.

### 2. Available context ≠ useful context

Even large windows degrade under irrelevant material ("lost in the middle").
Context utility = relevant information / total loaded information. Prevention
beats compression.

*Encoded as:* the 2,000–8,000 token per-task target; stage-scoped tool and
reference loading; lint checks for bloated catalogs.

### 3. The environment carries the system, not the prompt

When persistent context lives in the environment, a short user intent
("review this") is sufficient. Reliability comes from structure: the agent
*navigates* the operating environment instead of *inferring* it.

*Encoded as:* root catalogs as navigation handbooks ("tell the runtime where
to look next"); authority orders made explicit rather than re-inferred.

## Knowledge principles

### 4. Persistent synthesis over stateless retrieval

RAG re-derives knowledge per query and discards the reasoning. A maintained
wiki compiles knowledge once and keeps it current; the repository compounds
instead of repeatedly rebuilding understanding from raw material.

*Encoded as:* the source / synthesis role split; ingest as integration
(supports / extends / contradicts / creates) rather than one-summary-per-
source; valuable query results filed back as pages.

### 5. Build navigable knowledge, not a document dump

Storage alone creates memory capacity; structure creates usable memory. A
knowledge base should represent what exists, what things mean, and how they
relate: entities and concepts as nodes, relationships as edges — "nouns as
nodes, verbs as edges". Decompose documents enough that independent facts
stay independently addressable (atomicity), so the same entity can
participate in many relationships without being duplicated across files.
And keep memory and context separate: memory is the durable store; context
is what gets selected from it for the task at hand. The filesystem already
expresses this graph — markdown links and frontmatter, no graph database
required until scale demands it.

*Encoded as:* `index.md` as the first routing stop; entity/concept pages
with relationship sections; frontmatter as machine-readable metadata; the
Context map form for modeling organizations; lint checks for orphan pages
and missing cross-references.

### 6. Provenance, contradiction, and lifecycle are first-class

Source claim ≠ wiki synthesis. Every derived claim keeps a path back to its
evidence — and relationships need provenance too: whether "Team owns
Service" came from current documentation, a six-month-old chat message, or
inference changes how much it should be trusted. Conflicting evidence is
preserved with temporal context rather than silently overwritten. And
knowledge has a lifecycle: people change roles, systems are replaced,
policies are superseded. A memory that only accumulates eventually becomes
a second junk drawer — supersession and archival are part of the
architecture, not an afterthought.

*Encoded as:* mandatory provenance in the spec; contradiction-preservation
rule; `status:` frontmatter (active / superseded / archived) instead of
deletion; `log.md` as append-only, machine-parseable history; lint as
knowledge linting (stale claims, unsupported conclusions, superseded pages
still cited as current).

## Workflow principles

### 7. Start with the workflow, not the agent

Decompose the real process first; let the structure follow. A stage that
fetches does not also filter. One stage, one job — Parnas's information
hiding, McIlroy's Unix philosophy.

*Encoded as:* numbered stage folders; contracts with explicit Inputs /
Process / Outputs; one-way dependencies between stages.

### 8. Every output is an edit surface

Human review happens on files between stages, not in chat history. The
system picks up whatever the human left. This is mixed-initiative design
with direct manipulation: visible, manipulable objects.

*Encoded as:* `output/` handoff folders; checkpoints and audits in creative
stage contracts; the walk test's "report status" step.

### 9. Configure the factory, not the product

Set up voice, conventions, and structure once; produce repeatedly. Editing
output fixes one run; editing source fixes every future run — recurring
output edits are debugging information pointing at fixable source problems.

*Encoded as:* the factory / product role split; setup questionnaires;
lint's detection of repeated manual fixes as a signal to amend contracts.

## Product principles

### 10. Context packages before platforms

A large class of AI systems needs no dedicated platform: model + structured
context + instructions + tools, packaged as a portable folder. The filesystem
is the context architecture; software supplies only what the filesystem
cannot.

*Encoded as:* the workspace-is-a-folder rule; Git-compatibility; handoff by
copying a directory.

### 11. Build outcomes, not AI features

Capabilities are commoditized; composed systems are not. Evaluate by what
changed for the user — cost, time, quality, error rate — not by how much AI
the system contains. Not every step should use AI; scripts handle the
mechanical work.

*Encoded as:* CCA specifies structure, not models; local scripts welcome for
deterministic work; stage contracts define value before drafting.

### 12. Automation as infrastructure, augmentation as the objective

Automation removes repetitive work; augmentation increases what a person can
understand, decide, and create. The human's job is curation, direction, and
judgment; the agent's job is the bookkeeping humans abandon.

*Encoded as:* review gates at every stage boundary; "the agent owns the
synthesis, the human owns direction"; observability as a side effect of
plain files (glass box, never opaque).

---

*Sources: the ICM paper (Van Clief & McDermott), Karpathy's LLM Wiki idea
file, and the curated whitepaper collection: "Route the Right Context, Not
Bigger Prompts", "Persistent Synthesis Instead of Stateless Retrieval",
"Build Navigable Knowledge, Not a Document Dump",
"Context Packages Before Platforms", "Build Outcomes, Not AI Features",
"Automation as Infrastructure, Augmentation as the Objective", "Build
Software Inside the Service", "From Local Context to Shared Environments",
"One Runtime, Many Skills", "Operate at the Durable Abstraction Layer",
"Start With the Workflow, Not the Agent", "Learn From Problems, Not From the
Feed", "Infrastructure Is a Layer, Not Necessarily the Company".*
