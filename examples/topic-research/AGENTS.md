# AGENTS.md — topic-research example

> Portable root guidance for a synthetic worked example: maintained research knowledge feeding a two-stage ICM-derived weekly-brief pipeline.

This example deliberately demonstrates **composition**, not a complete native ICM workspace. Its stages preserve selected ICM patterns — numbered stage folders, exact `Inputs` / `Process` / `Outputs` contract shape, selective routing, one-way dependencies, and human-editable output handoffs — while the surrounding hybrid adopts CCA-specific maintained-knowledge conventions.

## Directory map

| Path | Purpose |
|---|---|
| `CONTEXT.md` | Root task routing for this hybrid example |
| `raw/` | Durable synthetic source documents |
| `wiki/` | Maintained synthesis and its index |
| `log.md` | Example CCA maintenance chronicle |
| `stages/01-collect/` | ICM-derived collection stage |
| `stages/02-brief/` | ICM-derived brief stage |
| `_config/` | Stable conventions used by the example |
| `setup/questionnaire.md` | Example CCA/hybrid onboarding artifact |

## Routing

- **Run the weekly brief** → read `CONTEXT.md`, then start at `stages/01-collect/CONTEXT.md`.
- **Ingest a source** → follow this example's knowledge conventions in `CONTEXT.md` and `_config/conventions.md`.
- **Ask about the topic** → start at `wiki/index.md`, then load only relevant pages and supporting evidence as needed.
- **Inspect current pipeline state** → read `CONTEXT.md` and the stage output folders.

## Operating rules

1. Load only context required for the current operation.
2. Keep source material distinct from maintained synthesis.
3. One fact, one canonical home; route with links instead of duplicated rules.
4. Preserve contradictions and uncertainty in maintained knowledge.
5. Stage outputs are human-editable handoff surfaces.
6. The pipeline preserves the ICM-derived patterns this example explicitly adopts; do not infer full native ICM compatibility from those patterns alone.

## Instruction interoperability

`AGENTS.md` provides portable guidance for agents that support it. `CLAUDE.md` is a thin Claude-compatible pointer to the same guidance for this example. That adapter does not turn the hybrid into a complete native ICM workspace.
