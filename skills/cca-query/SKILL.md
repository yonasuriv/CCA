---
name: cca-query
description: Answer questions from a filesystem-native maintained knowledge base using its own navigation and provenance conventions, escalating to source evidence when verification is needed. Use when the user asks what a CCA or LLM Wiki workspace knows, requests a comparison or synthesis, or wants a durable finding incorporated back into maintained knowledge. Preserves native schemas and does not assume fixed wiki/index.md or log.md paths.
compatibility: Read access to the target knowledge workspace; write access only when persistence is requested or defined by workspace policy.
---

# CCA Query

Query maintained synthesis first; use source evidence when the answer requires verification.

## Discover routing

1. Read the applicable workspace instructions/schema.
2. Identify the knowledge navigation entry point: index, map, links, search procedure, or another schema-defined router.
3. Identify how the workspace represents provenance, contradictions, and durable query results.
4. Preserve the native profile. Do not invent CCA paths when the workspace uses another valid layout.

## Procedure

1. **Route before searching broadly.** Use the workspace's index/map/schema to identify relevant synthesis.
2. **Read the smallest sufficient set of pages.** Follow relevant links rather than loading the whole knowledge base.
3. **Escalate to evidence when needed.** Inspect cited/source material for exact wording, numbers, dates, disputed claims, or confidence judgments.
4. **Answer with traceability.** Distinguish maintained synthesis, direct evidence, unresolved contradictions, and your inference.
5. **Expose gaps.** If the workspace does not contain enough evidence, say what is missing rather than filling the gap from unstated assumptions.
6. **Persist only when appropriate.** Write the result back only when the user requests it or the workspace explicitly defines query-to-knowledge maintenance as normal behavior. Follow the workspace's existing page/index/history conventions.

## Durable answers

A result is usually worth persisting when it creates reusable knowledge such as a comparison, timeline, synthesis, resolved relationship, or documented open question. Ephemeral lookups generally should remain conversational.

When persisting:

- update the canonical knowledge page where possible;
- preserve provenance to every source used;
- update navigation/history only according to the active schema;
- avoid creating duplicate pages that restate existing canonical knowledge.

## Production rules

- Never present maintained synthesis as direct source evidence.
- Never silently choose one side of a recorded contradiction.
- Never fabricate citations or source locations.
- Do not require `wiki/index.md`, `log.md`, or any CCA-specific taxonomy unless the workspace adopted them.
- Do not require another CCA skill for core execution.
- Keep navigation progressive: router → relevant synthesis → evidence only as needed.
