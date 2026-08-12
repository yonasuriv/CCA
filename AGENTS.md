# AGENTS.md — CCA repository

> Layer 0 root catalog for this repository. Role: **catalog** — it points at
> everything and stores almost nothing. If you are an agent entering this repo,
> this file is your map. Keep it under ~800 tokens when editing.

## What this is

CCA (Convergent Context Architecture) — an interoperability and evolution layer for
filesystem-native agent context. It unifies ICM (Interpretable Context
Methodology) and the LLM Wiki pattern behind ecosystem standards (AGENTS.md,
SKILL.md), staying agent-agnostic. This repository contains the specification,
the skills, and worked examples. It is itself a CCA-conformant workspace.

## Directory map

| Path | Role | Contents |
|---|---|---|
| `spec/` | factory | The canonical specification, compatibility rules, adapter conventions. Normative. |
| `skills/` | factory | Six agent-agnostic skills (`cca-architect`, `cca-scaffold`, `cca-sync`, `cca-ingest`, `cca-query`, `cca-lint`), each a standard `SKILL.md` package. |
| `examples/topic-research/` | product (example) | A worked workspace showing a knowledge bundle (raw/wiki) feeding a two-stage pipeline. |
| `docs/` | factory | Design principles, migration guides. Explanatory, not normative. |
| `README.md` | catalog | Human-facing entry point. |
| `LICENSE` | factory | MIT. |

## Routing rules

- **Understand the model** → read `spec/SPEC.md` first, then `spec/compatibility.md`.
- **Build or restructure a workspace** → use `skills/cca-architect/SKILL.md`.
- **Add CCA to an existing project** → use `skills/cca-scaffold/SKILL.md`.
- **Fix drift between catalogs and disk** → use `skills/cca-sync/SKILL.md`.
- **Add a source to a wiki** → use `skills/cca-ingest/SKILL.md`.
- **Answer questions from a wiki** → use `skills/cca-query/SKILL.md`.
- **Health-check a workspace** → use `skills/cca-lint/SKILL.md`.
- **See it working end to end** → walk `examples/topic-research/` top to bottom.
- **Migrate an ICM workspace or an LLM Wiki** → read `docs/migration.md`.

## Operating principles

1. Plain text is the interface. Every artifact is a readable, editable file.
2. Catalogs point; they do not store. Keep routing files small and stable.
3. One fact, one home. Link, don't duplicate.
4. Load only the context the current task needs.
5. Every output is an edit surface for the human.

## Authority order in this repo

`spec/` is normative. `skills/` must conform to `spec/`. `examples/` must pass the walk test defined in `spec/SPEC.md`. `docs/` explains but never overrides.
