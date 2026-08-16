# Exact human prompts

Builders and judges MUST use these verbatim.
Do NOT copy these into `skills/cca/`.
Do NOT score against a memorized ideal tree — score against intent properties in `score_intent.py`.

## Prompt A — initial request

```
So I would like to create a space where I can have my coding projects, my notes, research, second brain, etc, everything structured so it's easy for me to navigate and also for agents, i like the llm wiki idea of having a separation between source files that are inmutable and the wiki that grows, how can i approach this?
```

## Prompt B — when the builder asks clarifying questions

```
idk, do what you consider whats best, i trust you
```

## Prompt C — session handoff

```
ill continue on a new session, create a readme.md with a guide or anything missing that is only on prose, how it works day to day, etc
```

## Judge protocol

1. Fresh context. No ranking memory. No `wp7-idea-*`. No other `workspaceN` contents. No `cca-icm*` for judgment.
2. Give the subject only Prompt A (plus CCA skill if this is the CCA arm).
3. If it asks questions, answer only with Prompt B.
4. Then give Prompt C.
5. Score the resulting filesystem with `score_intent.py` (deterministic intent checklist).
6. Optional second judge: same prompts only; must not see prior scores.
