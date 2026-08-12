---
name: cca-query
description: Answer questions against a CCA/LLM Wiki knowledge base using index-first navigation and cited synthesis, and file valuable answers back into the wiki as new pages so exploration compounds. Use when the user asks questions of a wiki or knowledge workspace ("what do we know about X", "compare A and B", "what contradicts this"), when a workspace has wiki/ and index.md, or when a good answer should be persisted rather than lost to chat history.
---

# CCA Query

Queries run against the maintained synthesis, not the raw pile. The wiki is
the compiled knowledge; `raw/` is for evidence and verification. Good answers
are knowledge too — file them back.

## Procedure

1. **Read `wiki/index.md` first.** It is the routing layer: what exists, one
   line per page. Do not start by searching every file.
2. **Drill into the relevant pages** the index names. Follow cross-links
   (concepts → entities → syntheses). Load only what the question needs.
3. **Inspect sources when required**: when the question hinges on exact
   wording, numbers, or evidence strength, open the cited source page and,
   if needed, the raw file. Prefer the wiki's synthesis for orientation and
   the raw layer for verification.
4. **Answer with citations.** Name the wiki pages (and sources behind them)
   that support each part of the answer. If the wiki is silent or
   contradictory on the question, say so plainly — that is a finding, not a
   failure. Note it as an open question.
5. **Decide whether to file the answer back.** File it when the answer
   produced durable knowledge: a comparison, an analysis, a discovered
   connection, a resolved contradiction, a timeline. Do not file ephemeral
   lookups. When in doubt, offer: "worth keeping as a page?"
   - To file: create the page under the right `wiki/` subfolder
     (`comparisons/`, `syntheses/`, …) with frontmatter and links to the
     pages it drew from; update `wiki/index.md`; append a
     `## [YYYY-MM-DD] query | …` entry to `log.md` naming what was filed.
6. **Note gaps.** If the question exposed a missing concept page, a stale
   claim, or thin source coverage, say so and add it to the index's open
   questions (or suggest an ingest / a lint pass).

## Answer forms

Match the artifact to the question: inline answer, a markdown page, a
comparison table, a timeline. The conversational answer and the filed page
may differ — the page is written to stand alone for a future reader.

## Rules

- Cite wiki pages for synthesis, raw sources for evidence. Never present
  uncited synthesis as sourced fact.
- Respect contradictions recorded in pages — report both positions with
  their dates rather than picking one silently.
- Keep navigation cheap: index → pages → sources, in that order. Escalate to
  full-text search only when the index fails.
- Filing back is what makes exploration compound; skipping it turns the wiki
  back into stateless retrieval.
