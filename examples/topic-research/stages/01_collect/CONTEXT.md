# CONTEXT.md — Stage 01: collect

> Layer 2 contract. This week, what changed — pulled from the wiki.

## Inputs

| Source | File/Location | Section/Scope | Role | Why |
|---|---|---|---|---|
| Wiki index | `../../wiki/index.md` | Full file | catalog | Find pages updated this period |
| Chronicle | `../../log.md` | Entries since last collect | chronicle | What ingests/queries happened |
| Conventions | `../../_config/conventions.md` | "Knowledge" section | factory | Citation rules |

Load only what this table lists. Then read only the wiki pages the index and
log identify as changed since the last collect.

## Process

1. Determine the collection window from `log.md` (last `run | Stage 01`
   entry, or workspace init if none).
2. From the index and log, list pages created or updated in the window.
3. Read those pages; extract candidate findings: new facts, changed claims,
   flagged contradictions, resolved or new open questions.
4. Write the collection notes per the Outputs table: one finding per bullet,
   each with its wiki page link. Rank by likely interest to the brief's
   reader; flag anything uncertain rather than resolving it.

## Outputs

| Artifact | Location | Format |
|---|---|---|
| Collection notes | `output/YYYY-MM-DD-collect-notes.md` | Markdown: bulleted findings with page links, ranked, plus an "open items" section |

## Audit (run before writing output)

- [ ] Every bullet links the wiki page it came from.
- [ ] Nothing included from outside the collection window.
- [ ] Contradictions are carried forward as contradictions, not smoothed over.
