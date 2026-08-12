---
name: cca-ingest
description: Integrate a new source into a CCA/LLM Wiki knowledge base — reads the source, extracts key claims, compares them against existing wiki pages (supports / extends / contradicts / creates), updates entity and concept pages, writes the source summary page, refreshes the index, and appends to the log. Use when the user drops a new document into raw/ or says "ingest this", "process this source", "add this article/paper/transcript to the wiki/knowledge base". Preserves provenance and flags contradictions instead of overwriting.
---

# CCA Ingest

Ingestion is knowledge integration, not summarization. One source may touch
many pages. The wiki compounds; it does not accumulate isolated summaries.

Preconditions: a knowledge workspace with `raw/`, `wiki/`, `wiki/index.md`,
and `log.md`. If any are missing, scaffold them first (cca-scaffold, full
mode) or confirm intent with the user.

## Procedure

1. **Read the source** from `raw/` (never modify it). If the user referenced
   an external document, first place a copy in `raw/` — the wiki cites
   immutable local evidence, not URLs alone.
2. **Extract the key claims, entities, and concepts.** Distinguish what the
   source *says* from what it *implies for existing knowledge*.
3. **Read `wiki/index.md`** and identify every existing page the source
   relates to. Read those pages. (At small scale the index suffices; if the
   wiki has a search tool, use it as well.)
4. **Compare**, claim by claim, against what the wiki currently holds:
   - **Supports** — strengthen the existing statement; add the citation.
   - **Extends** — add the new detail, attributed.
   - **Contradicts** — do *not* overwrite. Record both positions with dates
     and sources in the page's contradictions section, and adjust the
     synthesis to reflect the conflict (e.g. "as of 2026-08, evidence
     diverges: …").
   - **Creates** — a genuinely new entity/concept gets a new page from the
     wiki page templates (entity / concept), with frontmatter.
5. **Update the touched pages.** Keep prose current (synthesis reflects
   everything known *now*), bump `updated:` and `sources:` in frontmatter,
   add cross-links both directions.
6. **Write the source page** at `wiki/sources/[slug].md` (source template):
   faithful summary, key claims with locations in the raw file, and a "what
   this source changed" list linking every touched page.
7. **Update `wiki/index.md`**: new/changed pages, one-line summaries, dates.
8. **Append to `log.md`**: `## [YYYY-MM-DD] ingest | [Source title]` with
   pages touched and contradictions flagged.
9. **Report to the human**: key takeaways, what changed in the wiki, any
   contradictions or open questions the source raised, and what to read to
   verify. Stay available for guidance on what to emphasize — ingestion is
   supervised by default unless the user asked for batch mode.

## Batch mode

When the user asks to ingest many sources with less supervision: process one
source at a time through the full procedure (never merge sources into one
pass — per-source pages and log entries keep provenance clean), then deliver
one consolidated report at the end.

## Rules

- Provenance is mandatory: every claim added to a page links its source.
- Never delete or rewrite an existing claim merely because a new source
  disagrees — preserve, date, and contextualize.
- Keep pages under ~200 lines; split rather than bloat.
- The index and log updates are part of ingest, not optional follow-ups.
