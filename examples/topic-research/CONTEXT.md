# CONTEXT.md — topic-research routing

> Root task router for the worked hybrid example. The two pipeline stages intentionally use ICM-derived contracts; this repository example does not claim the complete native ICM profile.

## Task routing

| If the user wants to… | Then… |
|---|---|
| Make this week's brief | Run `stages/01-collect/` per its contract, then `stages/02-brief/` after human review |
| Add a source | Follow the example's knowledge conventions: preserve the source, update relevant maintained pages and navigation, then record the operation |
| Ask about the topic | Read `wiki/index.md`, then relevant synthesis, then source evidence only as needed |
| Check health | Validate the adopted ICM-derived stage invariants, routing links, knowledge provenance, and this example's adopted CCA conventions |

## Shared resources

| Resource | Location | Used by |
|---|---|---|
| Brief voice | `_config/voice.md` | Stage 02 |
| Conventions | `_config/conventions.md` | Knowledge maintenance and pipeline operations |

## Current state

Stage 01 completed on 2026-08-11 and its output was reviewed. The next pipeline action is `stages/02-brief/`, using `stages/01-collect/output/2026-08-11-collect-notes.md` as the human-editable handoff.
