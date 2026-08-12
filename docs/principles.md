# Design principles behind CCA

Explanatory, not normative. CCA inherits ideas from ICM, the LLM Wiki pattern, and broader context-engineering practice. This document explains the reasoning behind CCA without turning optional implementation choices into upstream requirements.

When this document conflicts with `spec/SPEC.md` or a current upstream primary source, the spec/upstream wins.

## Context principles

### 1. Route the right context, not bigger prompts

A better prompt does not compensate for a badly designed context system. Agent execution depends on instructions, memory, knowledge, tools, and state. The engineering problem is constructing the right context for this task, at this moment, within budget rather than loading everything available.

*Encoded as:* layered routing where appropriate; catalogs that point instead of store; progressive loading; Inputs tables that scope what a stage reads; profile-aware routing instead of one universal router.

### 2. Available context ≠ useful context

Large context windows do not make irrelevant material useful. Selective routing should reduce unnecessary context before compression or larger prompts are considered.

*Encoded as:* stage-scoped references and tools; selective section routing; compact routing files; lint checks for bloated or duplicative navigation.

### 3. The environment carries the system, not the prompt

When durable context lives in the workspace, short user intent can be enough because the agent navigates explicit files instead of reconstructing the operating model from chat history.

*Encoded as:* root/native instruction files, task routers, scoped references, durable state, and explicit compatibility/authority boundaries.

## Knowledge principles

### 4. Persistent synthesis when knowledge should compound

Some knowledge tasks benefit from maintaining synthesis across sessions rather than rebuilding the same understanding from source material for every query. This complements retrieval; it does not imply that every RAG system discards reasoning or that persistent synthesis should replace retrieval everywhere.

*Encoded as:* a source/synthesis distinction when the workspace adopts maintained knowledge; ingest as integration rather than isolated per-source summaries; verification against evidence when needed.

### 5. Build navigable knowledge, not a document dump

Storage creates capacity; navigation makes knowledge usable. A maintained knowledge workspace should make it possible to find what exists, understand relationships, and trace important claims without forcing a specific database or graph implementation.

*CCA hardening may encode this as:* an index/router, entity or concept pages, cross-links, provenance metadata, lifecycle fields, or structured frontmatter. These are optional CCA implementation choices unless the active workspace explicitly adopts them. Native LLM Wiki compatibility does not require this exact schema.

### 6. Provenance, contradiction, and lifecycle are valuable hardening layers

Where evidence traceability matters, derived claims should keep a path back to supporting material. Conflicting evidence should be preserved with enough context to understand the disagreement, and stale knowledge should remain distinguishable from current knowledge when history matters.

*CCA hardening may encode this as:* provenance fields, contradiction sections, lifecycle states, or a maintenance chronicle. None of those concrete mechanisms are universal LLM Wiki requirements, and the CCA spec only makes them normative for a workspace that intentionally adopts the corresponding profile/convention.

## Workflow principles

### 7. Start with the workflow, not the agent

Decompose the real process first; let the structure follow. A stage that fetches does not also filter. One stage, one job.

*Encoded as:* ICM's numbered stage folders, explicit `Inputs` / `Process` / `Outputs` contracts, one-way dependencies, and durable output handoffs when the workflow is pipeline-shaped.

Borrowing these constructs does not automatically make a repository a full native ICM workspace. Native ICM compatibility requires the complete applicable current ICM profile.

### 8. Every output can be an edit surface

For staged workflows, human review should happen on durable artifacts between stages rather than only in chat history. The next stage consumes what the human actually left on disk.

*Encoded as:* ICM `output/` handoff folders and, where the profile calls for them, checkpoints and stage audits.

### 9. Configure the factory, not the product

Stable preferences and system rules belong in durable configuration/reference material rather than being re-entered for every run. Repeated manual corrections are signals that the durable system may need improvement.

*Encoded as:* setup/onboarding for profiles that use it, canonical references, and shared constants for code-producing ICM workspaces where applicable.

## Product principles

### 10. Context packages before platforms

A large class of agent workflows can remain portable when their durable context is ordinary files. Software should be introduced for capabilities the filesystem cannot provide efficiently, not merely to make the architecture look more sophisticated.

*Encoded as:* the workspace-is-a-folder baseline; Git-friendly state; optional databases, indexes, MCP connections, and orchestration.

### 11. Build outcomes, not AI features

Evaluate the system by what changes for the user: quality, speed, cost, reliability, understanding, or decision leverage. Deterministic work should stay deterministic when a script or ordinary tool is more appropriate than a model.

*Encoded as:* CCA specifies context structure and operations rather than requiring a model or runtime for every step.

### 12. Automation as infrastructure, augmentation as the objective

Automation removes repetitive work; augmentation increases what a person can understand, decide, and create. The human remains able to inspect and steer durable artifacts while agents handle repeatable context/navigation work.

*Encoded as:* human-editable files, visible handoffs, profile-specific checkpoints where applicable, and filesystem observability.

## Convergence rule

CCA's own preferred forms are never allowed to erase upstream distinctions:

- Native ICM remains governed by current ICM conventions and acceptance.
- LLM Wiki remains implementation-flexible unless a specific implementation chooses stronger structure.
- `AGENTS.md` follows its own standard and nested-scope behavior.
- Agent Skills remain portable packages governed by the current Agent Skills specification.
- CCA-specific hardening must be labeled as CCA-specific hardening.

Prefer Mermaid for CCA's own explanatory architecture/routing diagrams, but preserve an upstream-required representation when compatibility depends on it.

---

Primary influences: the ICM repository and paper, Karpathy's LLM Wiki idea file, AGENTS.md, Agent Skills, and the context-engineering design notes that informed CCA. Normative claims belong in the specification or in the upstream standard itself, not in this explanatory document.
