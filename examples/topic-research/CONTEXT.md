# CONTEXT.md — topic-research routing

> Layer 1 catalog. Given an intent, where to go.

## Task routing

| If the user wants to… | Then… |
|---|---|
| Make this week's brief | Run `stages/01_collect/` per its contract, then `stages/02_brief/` after review |
| Add a source | Copy into `raw/`; write source page; update touched `wiki/` pages, `wiki/index.md`, `log.md` |
| Ask about the topic | Read `wiki/index.md` → relevant pages → answer with citations |
| Check health | Lint: catalogs vs disk, provenance, orphans, staleness |

## Shared resources (factory)

| Resource | Location | Used by |
|---|---|---|
| Brief voice | `_config/voice.md` | stage 02 |
| Conventions | `_config/conventions.md` | all operations |

## Current state

Last run: `01_collect` completed 2026-08-11; output reviewed and approved.
Next: run `02_brief` against `stages/01_collect/output/`.
