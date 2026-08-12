# AGENTS.md — CCA repository

> Portable root guidance for contributors and agents working in this repository. Keep this file small; detailed behavior belongs in the canonical spec or the relevant skill.

## What this repository is

CCA is an interoperability and evolution layer for filesystem-native agent context. It builds on ICM / Model Workspace Protocol and LLM Wiki, adopts portable ecosystem conventions such as AGENTS.md and Agent Skills, and prefers convergence over competing conventions.

## Directory map

| Path | Purpose |
|---|---|
| `spec/` | Normative CCA specification and compatibility boundaries |
| `docs/` | Getting started, FAQ, principles, hardening/migration, tracked upstream standards |
| `skills/` | Six standalone Agent Skills packages implementing CCA operations |
| `examples/topic-research/` | Worked hybrid: maintained knowledge feeding an ICM-compatible pipeline |
| `scripts/` | Repository validation/regression tooling |
| `README.md` | Human-facing overview |
| `CITATION.cff` | Citation metadata |

## Routing

- Understand CCA semantics → `spec/SPEC.md`.
- Check upstream compatibility boundaries → `spec/compatibility.md` and `docs/standards.md`.
- Start using CCA → `docs/getting-started.md`.
- Answer common integration questions → `docs/faq.md`.
- Change a skill → read that skill's `SKILL.md` and only its referenced local resources.
- Change repository behavior → update the normative spec first, then every affected skill/template/example/doc surface.
- Validate changes → `python scripts/validate_repo.py`.

## Repository invariants

1. Native ICM and LLM Wiki compatibility comes before CCA hardening.
2. ICM-compatible stages use `01-name` and exact `Inputs` / `Process` / `Outputs` contracts with canonical Inputs columns.
3. LLM Wiki remains implementation-flexible; CCA-specific schemas are labeled optional hardening.
4. Nested `AGENTS.md` scope is preserved.
5. Every skill remains standalone and uses only skill-local relative resources for core execution.
6. One fact, one canonical home. Link instead of duplicating normative rules.
7. Prefer Mermaid for architecture/routing diagrams and text trees for literal filesystem layouts.

## Authority

`spec/` defines CCA. Upstream primary sources define their own standards and override stale CCA descriptions of them. `skills/`, `examples/`, and `docs/` must be updated toward both.
