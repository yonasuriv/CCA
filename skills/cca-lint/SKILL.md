---
name: cca-lint
description: Health-check a CCA/ICM/LLM Wiki workspace — detects structural problems (dead files, broken links, drifted catalogs, forked adapters, missing contracts) and knowledge problems (contradictions, stale claims, orphan pages, missing provenance, unsupported conclusions), then reports findings with a CCA conformance level (CCA-0/1/2). Use when the user asks to "lint", "health-check", "validate", or "audit" a workspace or wiki, before handing a workspace to someone else, or periodically as knowledge maintenance.
---

# CCA Lint

Knowledge repositories and routing layers both rot: links break, catalogs
drift, claims go stale, pages orphan. Lint finds it. Persistent knowledge can
become persistently wrong — maintenance is not optional.

Lint **reports and repairs conservatively**. It fixes what is unambiguous
(broken links, stale dates, missing index entries) and surfaces everything
else for human decision.

## Structural checks

1. **Root resolution** — exactly one authoritative root (`AGENTS.md`, else
   legacy alias); adapters are thin pointers (≲ 15 lines, no restated rules).
2. **Catalog integrity** — every path referenced in `AGENTS.md`,
   `CONTEXT.md`, `index.md` exists; every in-scope file on disk is
   referenced somewhere (no dead files, no unrouted folders).
3. **Budgets** — root catalog ≲ 800 tokens, routing ≲ 300, contracts < 80
   lines, reference files < 200 lines. Flag bloat; suggest where content
   should move.
4. **Contracts** — every stage folder has a `CONTEXT.md` with Inputs /
   Process / Outputs; Inputs tables reference real files and sections.
5. **One-way references** — no circular dependencies between stages or
   between catalogs.
6. **Chronicle format** — `log.md` entries match `## [YYYY-MM-DD] op |
   subject`; file is append-only (no edited history).

## Knowledge checks (wikis)

7. **Provenance** — every source-derived claim links a source; every source
   in `raw/` has a source page in `wiki/sources/`; every source page lists
   what it changed.
8. **Orphans** — pages with no inbound links; concepts mentioned across
   pages but lacking their own page.
9. **Contradictions** — claims across pages that conflict without a
   contradictions section acknowledging it; contradictions sections that
   newer sources may have resolved.
10. **Staleness and lifecycle** — pages whose claims predate newer ingested
    sources on the same topic; `updated:` frontmatter far behind the log's
    activity; pages or relationships that reality has superseded (roles
    changed, systems replaced, processes deprecated) but whose `status:`
    still says active; superseded pages still cited as authoritative by
    other pages. Recommend `status: superseded` or `archived` — flag, never
    silently delete.
11. **Open questions** — index open questions that ingests have since
    answered (promote to pages) or that suggest sources to seek.

## Procedure

1. Snapshot disk (folders, files, dates) — truth lives on disk.
2. Run structural checks 1–6, then knowledge checks 7–11 where a wiki exists.
3. Repair the unambiguous: broken link targets (if the file moved, repoint),
   missing index entries, stale `updated:` fields after verifying content.
4. Compile findings into a report (below). Never silently rewrite claims,
   resolve contradictions, or delete dead files — those are human decisions.
5. Append `## [YYYY-MM-DD] lint | Health check` to `log.md` with finding
   counts and actions taken.

## Report format

```
## Lint report — [workspace] — [date]
Conformance: CCA-[0/1/2] — [what blocks the next level]

### Errors (repair recommended)      [n]
### Warnings (human decision needed) [n]
### Repaired automatically           [n]
### Suggested next actions
- [ingest X, create page for Y, run sync, run walk test, …]
```

## Conformance levels (for the report)

- **CCA-0 Detectable** — root instruction file + plain-text artifacts.
- **CCA-1 Conformant** — canonical/aliased root catalog with map and
  routing; files classifiable into the eight roles; contracts for pipelines;
  index + log for wikis; thin adapters.
- **CCA-2 Verified** — CCA-1 plus a passing walk test (fresh agent orients,
  acts, reports from files alone), clean structural lint, parseable
  append-only log, provenance on wiki claims.

## Cadence

Suggest lint after bulk ingests, before sharing a workspace, and on a loose
periodic rhythm for active wikis. Lint is cheap; persistent wrongness is
expensive.
