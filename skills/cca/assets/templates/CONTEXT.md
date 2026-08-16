# CONTEXT.md -- [WORKSPACE NAME] routing

> Layer 1 catalog. Budget ≲ 300 tokens. Given what the user wants to do, this
> file says which stage, folder, or procedure handles it -- and what shared
> resources exist. Point, don't store.
> Default filename `CONTEXT.md`; if renamed, the L0 skeleton map must say so.

## Task routing

| If the user wants to… | Then… |
|---|---|
| [start the pipeline / produce X] | Run `stages/01-[name]/` per its contract |
| [continue after reviewing stage N] | Run `stages/0[N+1]-[name]/` against `stages/0[N]-[name]/output/` |
| [add a source to the knowledge base] | Follow the deposit/weave folder contracts (mapped L2 files) |
| [ask a question about the domain] | Read `wiki/index.md` → relevant pages → answer with citations |
| [check workspace health] | Lint structure + knowledge; report findings |
| [check status without prior memory] | [Scan: e.g. `stages/*/output/` OR `log.md` + wiki index + inbox] |

## Shared resources (factory -- stable across runs)

| Resource | Location | Used by |
|---|---|---|
| Voice / tone rules | `_config/voice.md` | [stages that write prose] |
| Conventions | `_config/conventions.md` | all stages |
| Page / record stamps | `_templates/` | new notes, wiki pages, records |
| [Domain glossary] | `_config/glossary.md` | [stages] |

## Current state

[One or two lines, updated by sync: e.g. "Last run: 02-draft completed
2026-08-10, awaiting review." For knowledge hybrids, point at the declared
status scan surface instead of inventing pipeline completion.]
