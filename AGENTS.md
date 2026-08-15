# AGENTS.md — CCA repository

> Portable root guidance for contributors and agents working in this repository. Keep this file small; detailed behavior belongs in the canonical spec or the relevant skill.

## What this repository is

CCA is an interoperability and evolution layer for filesystem-native agent context. It builds on ICM / Model Workspace Protocol and LLM Wiki, adopts portable ecosystem conventions such as AGENTS.md and Agent Skills, composes with human knowledge-work methodologies such as PARA, Zettelkasten, and Building a Second Brain, and prefers convergence over competing conventions.

## Directory map

| Path | Purpose |
|---|---|
| `spec/` | Normative CCA specification and compatibility boundaries |
| `docs/` | Getting started, FAQ, principles, method composition, hardening/migration, tracked upstream standards |
| `skills/` | CCA Agent Skills suite implementing focused operations |
| `examples/` | Worked examples: hybrid workspace under `workspaces/`, publication drafts under `articles/`, worked conversations under `conversations/` |
| `.github/scripts/` | Repository validation/regression tooling |
| `README.md` | Human-facing overview |
| `CITATION.cff` | Citation metadata |

## Routing

- Understand CCA semantics → `skills/cca/references/core/spec.md`.
- Check upstream compatibility boundaries → `skills/cca/references/core/compatibility.md` and `docs/standards.md`.
- Understand how PARA, Zettelkasten, BASB, LLM Wiki, ICM, and CCA compose → `docs/method-composition.md`.
- Start using CCA → `docs/getting-started.md`.
- Answer common integration questions → `docs/faq.md`.
- Change a skill → read that skill's `SKILL.md` and only its referenced local resources.
- Change repository behavior → update the normative spec first, then every affected skill/template/example/doc surface.
- Validate changes → `python .github/scripts/validate_repo.py`.

## Repository invariants

1. Native ICM and LLM Wiki compatibility comes before CCA hardening.
2. Distinguish **native ICM** from **ICM-derived** patterns. A native ICM claim requires the complete applicable current upstream profile and workspace-builder-equivalent acceptance; borrowing stage contracts alone is not enough.
3. Native ICM preserves current upstream naming, contracts, routing, onboarding, quality gates, and required representations. CCA preferences do not override upstream-required behavior.
4. LLM Wiki remains implementation-flexible; CCA-specific schemas are labeled optional hardening.
5. PARA, Zettelkasten, and BASB are **method overlays**, not structural compatibility profiles. Preserve their useful semantics without pretending CCA certifies a universal filesystem schema for them.
6. Nested native/upstream boundaries remain authoritative. An outer PARA or CCA organization must not rewrite a nested native ICM workspace or native LLM Wiki merely for consistency.
7. Nested `AGENTS.md` scope is preserved.
8. CCA skills are distributed as a suite of focused capabilities. Each skill's implementation resources remain package-local; cross-skill coordination uses semantic delegation such as `Use `lint` mode`, never sibling filesystem paths.
9. A skill may directly serve a matching request without routing through `cca` in `architect` mode. `cca` in `architect` mode coordinates compound architecture/workspace-design flows and lazy-loads methodology knowledge when relevant.
10. One fact, one canonical home. Link instead of duplicating normative rules.
11. Prefer Mermaid for CCA-owned architecture/routing diagrams and text trees for literal filesystem layouts, except where an upstream profile explicitly requires another representation.

## Authority

`spec/` defines CCA. Upstream primary sources define their own standards and override stale CCA descriptions of them. For native ICM, `_core/CONVENTIONS.md` is canonical and the workspace-builder validation stage is the practical acceptance surface for generated workspaces. `skills/`, `examples/`, and `docs/` must be updated toward both.
