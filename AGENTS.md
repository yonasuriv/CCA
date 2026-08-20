# AGENTS.md — CCA repository

> Portable root guidance for contributors and agents working in this repository. Keep this file small; detailed behavior belongs in the canonical skill-local spec or the relevant reference.

## What this repository is

CCA is an agent-agnostic interoperability architecture for filesystem-native context. It builds on ICM / Model Workspace Protocol and LLM Wiki, adopts portable ecosystem conventions such as AGENTS.md and Agent Skills, and composes with human knowledge-work and delivery methodologies without replacing their authorities. It is deliberately evolvable as those upstream systems and ecosystem conventions change.

## Directory map

| Path | Purpose |
|---|---|
| `skills/cca/` | The single installable CCA Agent Skill: router, canonical runtime spec, architect/advisor domains, operation modes, templates, and validation material |
| `docs/` | Getting started, FAQ, design principles, scenarios, method composition, migration, and tracked upstream standards |
| `examples/workspaces/` | Worked filesystem-native workspace examples |
| `examples/publications/` | Non-normative blog, article, and paper expressions of CCA |
| `examples/conversations/` | Worked conversations used as explanatory material |
| `examples/transcripts/` | Source/inspiration transcripts; not normative CCA authority |
| `.github/scripts/` | Repository validation/regression tooling |
| `README.md` | Human-facing overview |
| `CITATION.cff` | Citation metadata |

## Routing

- Understand normative CCA semantics → `skills/cca/references/core/spec.md`.
- Check upstream compatibility boundaries → `skills/cca/references/core/compatibility.md` and `docs/standards.md`.
- Understand method composition → `skills/cca/references/core/method-composition.md` and `docs/method-composition.md`.
- Work on workspace architecture/forms → `skills/cca/references/architect/`.
- Work on engineering/process judgment → `skills/cca/references/advisor/`. Keep this corpus separate from architect references.
- Work on scaffold/sync/ingest/query/lint behavior → `skills/cca/references/operations/`.
- Start using CCA → `docs/getting-started.md`.
- Inspect scenario behavior → `docs/scenarios.md`.
- Answer common integration questions → `docs/faq.md`.
- Validate changes → `python .github/scripts/validate_repo.py`.

## Repository invariants

1. **Convergence over invention.** Never replace, absorb, supersede, or redefine an existing framework, methodology, standard, or knowledge system merely to make it look like CCA.
2. Native ICM and LLM Wiki compatibility comes before optional CCA hardening.
3. Distinguish **upstream-native ICM** from **ICM-derived** patterns. Borrowing stage contracts alone does not establish native compatibility.
4. Upstream-native ICM preserves the complete applicable upstream profile, including its native harness entry semantics. Portable `AGENTS.md` guidance may coexist without erasing a native `CLAUDE.md` authority.
5. LLM Wiki remains implementation-flexible; CCA-specific schemas are optional hardening unless explicitly adopted.
6. PARA, Zettelkasten, BASB/CODE, Scrum, Kanban, XP, DevOps, SAFe, LeSS, DA, and similar methods remain authorities at their own scopes. CCA maps and routes their relationships; it does not implement them as a universal filesystem taxonomy.
7. Nested native/upstream boundaries remain authoritative. Outer organization must not rewrite nested semantics merely for consistency.
8. CCA ships as **one `cca` skill with seven lazy modes**: `architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`, and `advise`.
9. Architect and advisor are separate reference domains. Architect may lazily consult advisor judgment, but must not duplicate or absorb it.
10. One fact, one canonical home. Link instead of duplicating normative rules.
11. Existing repositories are preserved by default. Add structure only when it materially improves routing, context, knowledge maintenance, or execution.
12. Prefer Mermaid for CCA-owned architecture/routing diagrams and text trees for literal filesystem layouts, except where an upstream profile requires another representation.

## Authority

`skills/cca/references/core/spec.md` defines CCA runtime semantics and ships with every installation. Upstream primary sources define their own standards and override stale CCA descriptions of them. `docs/` and `examples/` explain or demonstrate the architecture but are not runtime authority.

When changing normative behavior, update the skill-local core reference first, then every affected mode, template, example, document, publication, and regression check in the same change.

## Design principles

1. **Convergence over invention.** Preserve useful existing authorities before creating new ones.
2. **Human agency first.** Automation exists to augment human capability.
3. **Boundaries before taxonomy.** Identify independent scopes and authorities before reorganizing their contents.
4. **Stable semantics over stable paths.** Roles remain meaningful when implementations move or change.
5. **Route before search.** Deterministic semantic resolution should precede broad discovery.
6. **One fact, one canonical authority.** Derive views instead of maintaining competing copies.
7. **Least authority.** Grant only the scope and mutation capability required for the operation.
8. **Serialized canonical mutation where necessary.** Shared authority does not imply uncontrolled concurrent writes.
9. **Recover durable mutations.** Reversible, reconstructable, or superseded state is safer than irreversible mutation.
10. **Derived state stays derived.** Indexes, dashboards, reports, graphs, embeddings, and caches must not silently become canonical state.
11. **Freshness is semantic.** Apply temporal review where information can become stale; do not impose expiry universally.
12. **Compose boundaries; do not flatten schemas.** Outer organization does not erase nested native semantics.
13. **Infer before serializing metadata.** Explicitly model information only when inference would be ambiguous or unsafe.
14. **Structure must earn its cost.** Avoid directories, metadata, IDs, manifests, and processes that do not improve correctness or navigation.
15. **Progressive disclosure.** Load only the context and capability required for the current operation.
16. **Plain files remain the durable interface.** Humans and agents should be able to inspect canonical context directly where practical.
17. **Stable context plane, replaceable execution plane.** Models, harnesses, runtimes, databases, and providers must not own durable context.
18. **Native compatibility before hardening.** Optional CCA improvements must not silently break the system they are intended to help.
19. **Restricted means explicit.** Sensitive boundaries must not be traversed, indexed, or mutated through accidental ambient access.
20. **Efficiency is architectural.** Context, compute, maintenance, and operational costs should be reduced where correctness is preserved.

> If the above design principles grow, `docs/design-principles.md` must be updated, and the other way around. \
> This applies to any repository documentation cross-reference.
