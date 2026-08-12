# AGENTS.md — [WORKSPACE NAME]

> Layer 0 root catalog. Role: **catalog** — point at everything, store almost
> nothing. Budget ≲ 800 tokens. If this file grows content, move the content
> to its canonical home and keep a link here.

## What this is

[One to three sentences: what this workspace produces or knows, and for whom.]

## Directory map

| Path | Role | Contents |
|---|---|---|
| `CONTEXT.md` | catalog | Task routing — given an intent, which stage/folder handles it |
| `stages/` | contract | [Numbered pipeline stages, if this workspace has a pipeline] |
| `raw/` | source | [Immutable source evidence, if this workspace has a wiki] |
| `wiki/` | synthesis | [Agent-maintained knowledge: pages, `index.md`] |
| `log.md` | chronicle | [Append-only history, if present] |
| `_config/` | factory | Stable conventions: voice, style, glossary, decisions |
| `setup/questionnaire.md` | factory | One-time onboarding |
| `output/` | product | [Per-run deliverables] |

[Delete rows that do not apply. Add rows for workspace-specific folders.]

## Routing rules

- **"[common intent 1]"** → [where to go, e.g. run `stages/01_research/` per its contract]
- **"[common intent 2]"** → [e.g. read `wiki/index.md`, then relevant pages]
- **"ingest [source]"** → [follow the ingest procedure: update pages, index, log]
- **"health check"** → [lint: structure + knowledge checks]

## Operating principles

1. Plain text is the interface; every artifact is readable and editable.
2. Load only the context the current task needs (see `CONTEXT.md` first).
3. `raw/` is immutable. Cite sources; never edit them.
4. One fact, one home — link, don't duplicate.
5. Every output is an edit surface; the human reviews between stages.

## Authority order

`AGENTS.md` (this file) is authoritative. Tool-specific files (`CLAUDE.md`,
`GEMINI.md`, `.cursorrules`, …) are thin adapters and must never contradict
it. `_config/` conventions override defaults; stage contracts override
`_config/` for their stage.
