# AGENTS.md — topic-research (example workspace)

> Layer 0 root catalog. Role: **catalog**. This is a worked CCA example: a
> knowledge bundle (wiki) feeding a two-stage pipeline (weekly brief).
> All content is synthetic sample data for demonstration.

## What this is

A research workspace that accumulates knowledge about a topic over time
(sources → wiki) and compiles a short weekly brief from that knowledge
(wiki → pipeline → brief). Demonstrates every CCA role and all six
operations at small scale.

## Directory map

| Path | Role | Contents |
|---|---|---|
| `CONTEXT.md` | catalog | Task routing: run, ingest, query, lint |
| `raw/` | source | Immutable source documents (sample articles) |
| `wiki/` | synthesis | Agent-maintained pages + `index.md` |
| `log.md` | chronicle | Append-only history |
| `stages/01_collect/` | contract | Pulls this week's new findings from the wiki |
| `stages/02_brief/` | contract | Compiles findings into the weekly brief |
| `_config/` | factory | Voice and conventions, configured once |
| `setup/questionnaire.md` | factory | Completed onboarding (example) |

## Routing rules

- **"run the pipeline" / "make this week's brief"** → start at
  `stages/01_collect/CONTEXT.md`; when its output is reviewed, run
  `stages/02_brief/`.
- **"ingest [source]"** → place it in `raw/`, then follow the ingest
  procedure (source page → update pages → index → log).
- **questions about the topic** → read `wiki/index.md`, then relevant pages;
  cite pages and sources.
- **"health check"** → lint structure + knowledge; report conformance.

## Operating principles

1. Plain text is the interface; every artifact is readable and editable.
2. Load only what the current task needs — start at `CONTEXT.md`.
3. `raw/` is immutable; cite it, never edit it.
4. One fact, one home — link, don't duplicate.
5. The human reviews every stage output before the next stage runs.

## Authority order

`AGENTS.md` is authoritative. `CLAUDE.md` is a thin adapter. `_config/`
conventions govern all stages; stage contracts govern their stage.
