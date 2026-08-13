# CONTEXT.md -- [WORKSPACE NAME] routing

> Layer 1 catalog. Budget ≲ 300 tokens. Given what the user wants to do, this
> file says which stage, folder, or procedure handles it -- and what shared
> resources exist. Point, don't store.

## Task routing

| If the user wants to… | Then… |
|---|---|
| [start the pipeline / produce X] | Run `stages/01-[name]/` per its contract |
| [continue after reviewing stage N] | Run `stages/0[N+1]-[name]/` against `stages/0[N]-[name]/output/` |
| [add a source to the knowledge base] | Ingest: read source → update `wiki/` pages → update `wiki/index.md` → append `log.md` |
| [ask a question about the domain] | Read `wiki/index.md` → relevant pages → answer with citations |
| [check workspace health] | Lint structure + knowledge; report findings |

## Shared resources (factory -- stable across runs)

| Resource | Location | Used by |
|---|---|---|
| Voice / tone rules | `_config/voice.md` | [stages that write prose] |
| Conventions | `_config/conventions.md` | all stages |
| [Domain glossary] | `_config/glossary.md` | [stages] |

## Current state

[One or two lines, updated by sync: e.g. "Last run: 02-draft completed
2026-08-10, awaiting review." Delete this section if the workspace is a pure
knowledge bundle -- `log.md` carries its history.]
