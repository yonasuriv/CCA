---
name: cca-sync
description: Keep CCA/ICM routing files accurate by reconciling AGENTS.md, CONTEXT.md, and wiki/index.md with what is actually on disk. Use when the user says "sync the catalogs", "update the routing", "refresh AGENTS.md / the index", after files or folders were added/moved/deleted, or when routing feels stale. Sync reports drift, prunes dead entries, and adds missing ones — it never invents content and never restructures.
---

# CCA Sync

Catalogs point at the filesystem; the filesystem changes; catalogs drift.
Sync reconciles them. It is the maintenance half of "catalogs point, they do
not store".

## What syncs

| Catalog | Syncs against |
|---|---|
| `AGENTS.md` (or legacy root) | Top-level directory map, routing targets, authority order |
| `CONTEXT.md` (root and stage-level) | Stages, shared resources, current-state line |
| `wiki/index.md` | Every page in `wiki/`: existence, one-line summary, updated date, source counts |
| `log.md` | Never edited — append-only. Sync may append a sync entry. |

## Procedure

1. **Snapshot disk.** List the actual folders and files: top level,
   `stages/`, `_config/`, `raw/`, `wiki/` (recursively). Note counts and
   modification dates.
2. **Read each catalog.** Extract every entry: path references, routing
   rows, index lines, resource tables.
3. **Diff.** Classify each discrepancy:
   - **Dead entry** — catalog points at something no longer on disk.
   - **Missing entry** — something on disk matches a catalog's scope but is
     not listed (new stage, new wiki page, new `_config/` file).
   - **Stale metadata** — index summaries, dates, or source counts that no
     longer match the target file. Re-read the target before rewriting its
     one-liner; never fabricate a summary.
   - **Forked adapter** — an adapter file carrying substantive rules instead
     of a pointer. Flag it; repair only with user approval.
4. **Apply repairs.** Prune dead entries, add missing ones, refresh stale
   metadata. Preserve each catalog's existing structure, tone, and token
   budget — sync edits entries, it does not rewrite files.
5. **Update state lines.** Refresh `CONTEXT.md`'s current-state section
   (latest stage output, pending reviews) from what is actually in
   `output/` folders.
6. **Append a log entry** if a `log.md` exists:
   `## [YYYY-MM-DD] sync | Catalog reconciliation` with the counts of what
   changed.
7. **Report** a compact table: per catalog — entries pruned, added,
   refreshed; anything that needs a human decision (e.g. a folder nothing
   routes to: keep, wire in, or flag dead).

## Rules

- Truth lives on disk. The catalog is always the thing being corrected.
- Never invent: every catalog entry after sync must correspond to a real
  file or folder.
- Never move, rename, or delete content files — that is restructuring
  (cca-architect's mode, with an approved migration map).
- If the same rule text appears in both a catalog and a `_config/` file,
  keep it in `_config/` and make the catalog point. One fact, one home.
- Run after: bulk file changes, completed ingests that skipped index
  updates, stage additions/removals, or any time an agent reports
  "the routing said X but X isn't there".
