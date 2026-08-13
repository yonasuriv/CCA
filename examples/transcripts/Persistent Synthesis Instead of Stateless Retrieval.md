# LLM Knowledge Architecture: Persistent Synthesis Instead of Stateless Retrieval

## Core Principle

Most document-based LLM systems are fundamentally retrieval systems.

The common architecture is:

```text
Raw Documents
      |
      v
Index / Embeddings
      |
      v
Query
      |
      v
Retrieve Relevant Chunks
      |
      v
LLM Synthesizes Answer
```

This works well for retrieving information.

But every question effectively begins another synthesis cycle.

The model must repeatedly:

```text
Find relevant information
        |
        v
Determine relationships
        |
        v
Resolve overlaps
        |
        v
Reconstruct context
        |
        v
Generate synthesis
```

The result of that reasoning usually disappears with the conversation.

A different architecture is to preserve the synthesis itself.

```text
Raw Sources
      |
      v
LLM Ingestion
      |
      v
Persistent Knowledge Layer
      |
      v
Query / Exploration
      |
      v
Further Knowledge Updates
```

The knowledge system therefore compounds rather than repeatedly rebuilding understanding from raw material.

## Retrieval vs. Knowledge Compilation

Traditional retrieval operates approximately like:

```text
Question
   |
   v
Search Raw Sources
   |
   v
Retrieve Chunks
   |
   v
Synthesize
   |
   v
Answer
```

A persistent knowledge architecture introduces an intermediate representation:

```text
Raw Sources
   |
   v
Extract
   |
   v
Normalize
   |
   v
Connect
   |
   v
Synthesize
   |
   v
Persistent Wiki
```

Queries then operate primarily against:

```text
Persistent Wiki
```

while the raw sources remain available for evidence, verification, and deeper inspection.

The architectural difference is important:

```text
RAG:
Knowledge is reconstructed at query time.

Persistent Wiki:
Knowledge is progressively compiled and maintained.
```

## The Wiki as a Compounding Artifact

The central asset is not the individual chat session.

It is the continuously maintained knowledge repository.

For example:

```text
wiki/
|
+-- overview.md
+-- concepts/
+-- entities/
+-- topics/
+-- comparisons/
+-- syntheses/
+-- decisions/
+-- index.md
+-- log.md
```

Each new source can modify the existing representation.

The system may:

```text
Add new entities
Update existing concepts
Strengthen previous conclusions
Challenge previous conclusions
Record contradictions
Add cross-references
Update summaries
Create new relationships
```

The repository therefore becomes progressively more useful as information accumulates.

This creates:

```text
Source
  |
  v
Knowledge Update
  |
  v
Better Existing Model
  |
  v
Next Source
  |
  v
Better Knowledge Update
```

rather than:

```text
Source A -> isolated summary
Source B -> isolated summary
Source C -> isolated summary
```

## Three-Layer Architecture

A clean implementation separates three concerns:

```text
+--------------------------------------+
| Raw Sources                          |
+--------------------------------------+
                  |
                  v
+--------------------------------------+
| Persistent Knowledge Representation  |
+--------------------------------------+
                  |
                  v
+--------------------------------------+
| Schema / Operating Instructions      |
+--------------------------------------+
```

More precisely:

```text
Raw Sources
    =
Evidence

Wiki
    =
Derived Knowledge

Schema
    =
Rules for maintaining that knowledge
```

These layers should remain distinct.

## Layer 1: Raw Sources

Raw sources are the evidence layer.

Examples:

```text
Papers
Articles
Books
Meeting transcripts
Slack exports
Reports
Datasets
Images
Research notes
Customer calls
```

The important property is immutability.

```text
raw/
|
+-- source-001.md
+-- source-002.pdf
+-- source-003.csv
```

The AI reads them.

It does not rewrite them.

This preserves:

```text
Provenance
Evidence
Original wording
Historical state
Auditability
```

The raw layer is therefore the source of truth for what was actually observed or imported.

## Layer 2: The Wiki

The wiki is the derived knowledge layer.

It contains artifacts such as:

```text
Entity pages
Concept pages
Topic summaries
Comparisons
Timelines
Syntheses
Relationships
Open questions
Contradictions
```

For example:

```text
wiki/
|
+-- entities/
|   +-- company-a.md
|   +-- company-b.md
|
+-- concepts/
|   +-- agent-memory.md
|   +-- context-routing.md
|
+-- synthesis/
|   +-- current-thesis.md
|
+-- index.md
+-- log.md
```

Unlike raw sources, this layer is intentionally mutable.

The LLM may continuously revise it as new information arrives.

Conceptually:

```text
Previous Knowledge
        +
New Evidence
        |
        v
Reconciliation
        |
        v
Updated Knowledge
```

## Layer 3: The Schema

The schema defines how the AI should maintain the repository.

This can exist in files such as:

```text
AGENTS.md
CLAUDE.md
README.md
schema.md
```

The schema may define:

```text
Directory structure
Page types
Naming conventions
Frontmatter
Citation requirements
Linking conventions
Source handling
Ingestion procedure
Query procedure
Maintenance rules
Conflict resolution
Output formats
```

Conceptually:

```text
Schema
   |
   +-- How to ingest
   +-- How to classify
   +-- How to connect
   +-- How to cite
   +-- How to update
   +-- How to query
   +-- How to maintain
```

The schema turns a generic model into a disciplined knowledge-maintenance system.

## The Repository as an Intermediate Representation

The architecture can be understood as:

```text
Reality / Sources
        |
        v
Raw Evidence
        |
        v
LLM Interpretation
        |
        v
Structured Knowledge Representation
        |
        v
LLM Reasoning
        |
        v
Human Understanding
```

The wiki is therefore an intermediate representation between raw information and future reasoning.

This matters because future queries no longer need to begin from completely unprocessed evidence.

They can begin from accumulated understanding.

## Ingestion as Knowledge Integration

Ingestion should not mean:

```text
Read document
    |
    v
Create summary
```

A stronger ingestion process is:

```text
New Source
    |
    v
Extract Important Claims
    |
    v
Identify Existing Related Knowledge
    |
    v
Compare
    |
    +-- Supports existing claim
    +-- Extends existing claim
    +-- Contradicts existing claim
    +-- Creates new concept
    |
    v
Update Relevant Pages
    |
    v
Update Index
    |
    v
Record Ingestion
```

A single source may therefore modify many pages.

For example:

```text
research-paper.pdf
      |
      +-- updates concept-a.md
      +-- updates entity-x.md
      +-- challenges thesis.md
      +-- creates method-y.md
      +-- updates index.md
      +-- appends log.md
```

This is substantially different from generating one summary per source.

## Knowledge Should Be Integrated, Not Duplicated

Suppose five papers discuss:

```text
Agent Memory
```

A naive architecture might produce:

```text
paper-1-summary.md
paper-2-summary.md
paper-3-summary.md
paper-4-summary.md
paper-5-summary.md
```

A persistent synthesis architecture may additionally maintain:

```text
concepts/agent-memory.md
```

containing:

```text
Current understanding
Major approaches
Evidence supporting each approach
Conflicting evidence
Open questions
Links to all relevant sources
```

When paper six arrives:

```text
Paper 6
   |
   v
Update Existing Understanding
```

rather than:

```text
Paper 6
   |
   v
Create Another Isolated Summary
```

The difference is accumulation.

## Querying the Knowledge Layer

Queries operate primarily against the structured knowledge base.

A typical flow is:

```text
Question
  |
  v
Read Index
  |
  v
Locate Relevant Pages
  |
  v
Follow Relationships
  |
  v
Inspect Sources if Required
  |
  v
Synthesize Answer
```

The index therefore functions as a lightweight routing mechanism.

Instead of immediately searching every file:

```text
Query
  |
  v
index.md
  |
  v
Relevant Domain
  |
  v
Relevant Pages
```

This can work surprisingly far before specialized retrieval infrastructure becomes necessary.

## Valuable Queries Should Become Knowledge

Some user questions produce new knowledge.

Examples:

```text
Compare architecture A and B.

How has our thesis changed?

What contradictions exist?

What are the strongest arguments against this approach?

How do these five papers relate?
```

The resulting synthesis should not necessarily disappear into chat history.

If valuable:

```text
Question
  |
  v
Analysis
  |
  v
Useful Synthesis
  |
  v
Persist as Wiki Page
```

This creates another compounding loop:

```text
Sources create knowledge.

Questions also create knowledge.
```

The system improves through both ingestion and exploration.

## Ingest, Query, Maintain

The architecture can be reduced to three fundamental operations.

### 1. Ingest

```text
Source
  |
  v
Read
  |
  v
Extract
  |
  v
Compare
  |
  v
Integrate
  |
  v
Update Knowledge
```

### 2. Query

```text
Question
  |
  v
Navigate Existing Knowledge
  |
  v
Inspect Supporting Evidence
  |
  v
Reason
  |
  v
Answer
```

### 3. Maintain

```text
Knowledge Base
      |
      v
Inspect Structure
      |
      +-- stale information
      +-- contradictions
      +-- orphan pages
      +-- missing links
      +-- duplicated concepts
      +-- missing concepts
      +-- unresolved questions
      |
      v
Repair
```

Maintenance is essential because persistent knowledge can become persistently wrong.

## Maintenance as Knowledge Linting

A useful analogy is source-code linting.

Software repositories periodically detect:

```text
Broken references
Dead code
Inconsistent formatting
Invalid dependencies
```

Knowledge repositories can similarly detect:

```text
Contradictory claims
Stale claims
Broken links
Missing citations
Orphan pages
Duplicated concepts
Missing relationships
Unsupported conclusions
Knowledge gaps
```

Conceptually:

```text
Knowledge Repository
        |
        v
Lint
        |
        +-- Structural problems
        +-- Semantic problems
        +-- Provenance problems
        +-- Freshness problems
```

A persistent knowledge system should have maintenance mechanisms from the beginning.

## Index and Log Serve Different Purposes

Two small artifacts provide significant value.

### index.md

The index represents the current structure.

```text
index.md
|
+-- Entities
+-- Concepts
+-- Topics
+-- Sources
+-- Syntheses
```

Each entry may include:

```text
Name
Link
Description
Date
Source count
Status
```

Its purpose is navigation.

### log.md

The log represents history.

```text
log.md
|
+-- ingest
+-- query
+-- maintenance
+-- restructuring
```

Example:

```text
[2026-08-11] ingest | Paper A
[2026-08-11] query | Compare A vs B
[2026-08-11] lint | Knowledge health pass
```

Its purpose is traceability.

The distinction is:

```text
index.md = What exists now

log.md = What happened over time
```

## Append-Only Operational History

The log should generally remain chronological and append-oriented.

This enables:

```text
Auditability
Debugging
Session recovery
Recent-change inspection
Simple CLI parsing
```

A machine-readable convention such as:

```text
## [DATE] operation | subject
```

also allows ordinary shell tools to inspect history.

This is another advantage of text-native architectures:

```text
grep
find
git
diff
sed
awk
```

can remain useful alongside LLM tooling.

## Start Simple Before Adding Retrieval Infrastructure

A small knowledge base may require nothing beyond:

```text
Filesystem
+
Markdown
+
index.md
+
Model
```

As scale increases:

```text
Hundreds of pages
        |
        v
Search becomes harder
```

Then additional capabilities may be introduced:

```text
Keyword search
BM25
Vector search
Hybrid retrieval
Re-ranking
Graph traversal
```

The architectural sequence should be:

```text
Simple Navigation
       |
       v
Observe Bottleneck
       |
       v
Add Retrieval Capability
```

not:

```text
Start Project
    |
    v
Immediately Build Vector Infrastructure
```

Infrastructure should appear when the corpus actually requires it.

## Filesystem-Native Knowledge

Markdown repositories provide several useful properties:

```text
Human-readable
LLM-readable
Diffable
Versionable
Portable
Searchable
Composable
Linkable
Tool-friendly
```

A Git-backed wiki therefore gains:

```text
Version history
Branches
Rollback
Collaboration
Change inspection
```

without requiring a specialized knowledge-management backend.

The repository itself becomes the database for many use cases.

## Structured Metadata Can Add Queryability

Markdown does not prevent structured data.

Frontmatter can encode metadata such as:

```yaml
type: concept
status: active
created: 2026-07-15
updated: 2026-08-11
sources: 7
tags:
  - ai-memory
  - context
```

This supports:

```text
Filtering
Dynamic indexes
Validation
Automation
Search
Maintenance
```

The architecture can therefore combine:

```text
Human-readable prose
        +
Machine-readable metadata
```

without abandoning plain files.

## Source-Derived Claims Need Provenance

A persistent wiki introduces an important distinction:

```text
Source claim
!=
Wiki synthesis
```

The system should preserve the path:

```text
Wiki Statement
      |
      v
Supporting Sources
```

This allows the model or human to determine:

```text
Where did this come from?

How strong is the evidence?

Does another source disagree?

Has the claim been superseded?
```

Without provenance, the wiki becomes an accumulation of model-generated claims rather than a trustworthy knowledge layer.

## Contradictions Should Be Preserved

When new evidence conflicts with existing knowledge, the correct operation is not automatically:

```text
Replace old claim
```

Instead:

```text
New Evidence
    |
    v
Conflict Detected
    |
    +-- old evidence
    +-- new evidence
    +-- confidence
    +-- temporal context
    |
    v
Update Synthesis
```

For example:

```text
Previous understanding:
X appears to improve Y.

New source:
X showed no measurable improvement in Y.

Updated synthesis:
Evidence is mixed. Earlier studies reported improvement,
while newer evidence challenges that conclusion.
```

Persistent synthesis should accumulate uncertainty as well as certainty.

## Human and LLM Responsibilities

A useful division of labor is:

```text
Human
|
+-- Select sources
+-- Define goals
+-- Ask questions
+-- Challenge conclusions
+-- Decide what matters
+-- Review important changes
```

while:

```text
LLM
|
+-- Summarize
+-- Classify
+-- Cross-reference
+-- Create pages
+-- Update pages
+-- Detect contradictions
+-- Maintain indexes
+-- Perform bookkeeping
```

This preserves human judgment while delegating high-volume maintenance.

The architecture is therefore augmentation rather than passive automation.

## Knowledge Maintenance Is the Expensive Part

Creating notes is easy.

Maintaining relationships between notes is harder.

As a knowledge base grows:

```text
More pages
    |
    v
More relationships
    |
    v
More maintenance work
```

Humans eventually stop maintaining:

```text
Cross-references
Indexes
Summaries
Contradictions
Metadata
```

LLMs are particularly useful here because the work is:

```text
High-volume
Textual
Structured
Repetitive
Context-dependent
```

The key opportunity is therefore not merely AI-generated notes.

It is AI-maintained knowledge.

## Knowledge Compilation

This architecture can be described as a form of knowledge compilation.

Raw information:

```text
Documents
```

is transformed into:

```text
Structured Concepts
Relationships
Syntheses
Indexes
```

which future reasoning can consume more efficiently.

Conceptually:

```text
Raw Knowledge
     |
     v
Compile
     |
     v
Structured Knowledge
     |
     v
Reason
```

The repository acts similarly to an intermediate compiled representation.

When new evidence arrives:

```text
Incremental Recompilation
```

updates only the affected knowledge.

This is more efficient than rebuilding the entire conceptual model for every question.

## Persistent Memory vs. Conversation Memory

The wiki should also be distinguished from chat memory.

Conversation memory is typically:

```text
User-specific
Session-oriented
Implicit
Small
Behavioral
```

A persistent knowledge repository is:

```text
Explicit
Inspectable
Structured
Versioned
Domain-oriented
Shareable
```

The repository therefore acts as durable external memory independent of any one conversation.

## The Memex Pattern

The architecture resembles the broader idea of a personal knowledge system built around associative connections.

The interesting modern addition is automated maintenance.

Historically, the difficult part of linked knowledge systems was:

```text
Who creates the links?

Who updates the summaries?

Who reorganizes the knowledge?

Who keeps it consistent?
```

With an LLM operating directly over the repository, much of that bookkeeping can become inexpensive enough to perform continuously.

## Key Notes

* Traditional RAG primarily retrieves raw information at query time.
* Retrieval alone does not preserve previous synthesis.
* A persistent wiki introduces a durable intermediate knowledge representation.
* New sources should update existing knowledge rather than merely create isolated summaries.
* The architecture should separate raw evidence, derived knowledge, and maintenance rules.
* Raw sources should remain immutable.
* The wiki should remain mutable.
* The schema defines how the model maintains the wiki.
* Ingestion is knowledge integration, not merely summarization.
* Valuable query results can themselves become durable knowledge.
* Ingest, query, and lint form the core operational lifecycle.
* Persistent knowledge requires active maintenance.
* Contradictions, stale claims, missing links, and orphan pages should be detected explicitly.
* `index.md` represents current structure.
* `log.md` represents historical activity.
* Small repositories may not require embedding infrastructure.
* Retrieval systems should be introduced when scale creates an actual navigation problem.
* Markdown provides a strong common representation for humans, LLMs, Git, and CLI tooling.
* Structured frontmatter can augment Markdown with machine-readable metadata.
* Provenance must remain connected to synthesized knowledge.
* Contradictions should be represented rather than silently overwritten.
* Humans should primarily curate, direct, question, and review.
* LLMs are well suited to continuous summarization, linking, classification, and bookkeeping.
* The durable asset is not the chat history.
* The durable asset is the evolving knowledge representation.
* The architecture can be understood as incremental knowledge compilation.

## Design Heuristic

When introducing a new source, do not ask only:

```text
What does this document say?
```

Ask:

```text
What existing knowledge does this modify?
```

Then:

```text
Which entities does it affect?

Which concepts does it strengthen?

Which claims does it challenge?

Which relationships should change?

What new questions does it create?
```

Likewise, after a valuable query, ask:

```text
Did this conversation produce knowledge
that should survive the conversation?
```

If yes:

```text
Persist it.
Connect it.
Cite it.
Maintain it.
```

## A Minimal Architecture

A practical starting point can remain extremely small:

```text
knowledge-base/
|
+-- AGENTS.md
|
+-- raw/
|
+-- wiki/
|   +-- index.md
|   +-- concepts/
|   +-- entities/
|   +-- synthesis/
|
+-- log.md
```

Where:

```text
raw/
    = immutable evidence

wiki/
    = evolving knowledge

AGENTS.md
    = maintenance contract

index.md
    = navigation

log.md
    = history
```

Only introduce additional tooling when this structure stops being sufficient.

## Final Principle

A strong LLM knowledge system should not force the model to reconstruct the same understanding from raw documents every time it receives a question.

Instead:

```text
Sources
   |
   v
Incremental Integration
   |
   v
Persistent Knowledge
   |
   v
Exploration
   |
   v
New Synthesis
   |
   v
Persistent Knowledge
```

The system compounds.

The key architectural shift is:

```text
Retrieval from documents
```

toward:

```text
Maintenance of understanding
```

The raw documents remain the evidence.

The LLM-maintained wiki becomes the evolving model of that evidence.

And the schema defines how that model should remain coherent as both the information and the user's understanding evolve.
