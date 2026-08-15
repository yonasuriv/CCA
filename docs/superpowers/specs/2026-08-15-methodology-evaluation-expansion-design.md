# Methodology Evaluation Expansion Design

## Problem

The 14-case interoperability suite validates native/derived ICM, existing code, one Scrum coexistence scenario, PARA, Zettelkasten, LLM Wiki, Record Library, Context Map, System Map, hybrid boundaries, approved restructure, and no-op behavior. It does not behaviorally validate the full advisor methodology corpus.

The three-way evaluation dated 2026-08-15 found one real `cca-dev` regression in Record Library identifier derivation: `Beta Corp` became `beta` rather than the existing full-name slug convention `beta-corp`. It also confirmed that the current methodology coverage is too narrow to support a broad claim of advisor/process parity.

## Goals

1. Fix Record Library identifier derivation without inventing a universal identifier scheme.
2. Preserve the existing 14-case interoperability suite as its own stable benchmark.
3. Add a separate executable methodology/framework suite so process reasoning is tested without bloating or conflating the interoperability suite.
4. Cover method selection, scope, composition, conflict, and non-trigger behavior.
5. Protect the retained methodology corpus from accidental future deletion or narrowing.
6. Keep progressive disclosure measurable: methodology references should be relevant to process decisions and should not be required for an ordinary implementation task.

## Runtime semantic fix

Record Library must continue to obey the workspace's declared identifier authority. When no explicit identifier is supplied and the existing library convention clearly derives a slug from the entity display name, derive the identifier from the complete display name rather than abbreviating or truncating it. Example: under a full-name slug convention, `Beta Corp` becomes `beta-corp`, not `beta`.

This is a fallback only when the local convention is evidenced. Existing explicit IDs, catalogs, templates, schemas, or domain-specific rules remain authoritative.

## Benchmark architecture

Keep:

```text
evals/cases/                 # 14 interoperability/core cases
```

Add:

```text
evals/methodologies/         # 20 process/methodology cases
```

Both suites use the same case contract:

```text
NN-case-name/
├── case.json
├── prompt.md
├── fixture/
└── assertions.json
```

The runner gains `--suite core|methodologies`, defaulting to `core`. Arm isolation and real-agent execution remain unchanged.

## Methodology suite coverage

The suite contains 20 cases:

1. Cynefin / problem classification before method prescription.
2. SAFe vs LeSS vs Disciplined Agile at enterprise/multi-team scope.
3. Sequential constraints: waterfall, stage-gate, V-model.
4. Scrum vs Kanban conflict at the same team-delivery scope.
5. Kanban continuous-flow reasoning.
6. DSDM project governance.
7. FDD feature-oriented decomposition.
8. ASD adaptation under uncertainty.
9. XP team/engineering practice coherence.
10. RAD rapid validation and prototype trade-offs.
11. IID iterative/incremental strategy without equating it to Scrum.
12. Lean systems/value/flow reasoning.
13. RUP/UP configurable lifecycle and architecture/risk attention.
14. DevOps delivery/operations ownership without reducing it to CI/CD tooling.
15. TDD as an engineering practice, not an organization method.
16. MDE as an engineering paradigm, not a delivery framework.
17. PSP/TSP individual/team process discipline.
18. SEMAT/Essence as method-engineering/common-vocabulary support without assimilation.
19. Cross-scope composition: Scrum + XP + DevOps + Lean remain distinct but composable.
20. Non-trigger: an ordinary implementation task must not require methodology restructuring or process ceremony.

The existing core Scrum case remains useful as a real repository coexistence case; the methodology suite tests the broader reasoning surface.

## Case design

Each methodology fixture contains enough process evidence to make the method question answerable. The worker is asked to write a small `decision.md` evaluation artifact with explicit `Scope`, `Recommendation`, `Preserve`, and `Avoid` lines. Deterministic assertions verify the important semantic distinction while also checking that the fixture is not restructured into method-named folders or unrelated CCA scaffolding.

The benchmark tests behavior, not architectural similarity. A method may be retained, rejected, combined, or left untouched depending on the evidence.

## Validation

Permanent repository validation must enforce:

- core cases remain exactly `01..14`;
- methodology cases remain exactly `01..20`;
- every case has manifest, prompt, assertions, and a non-empty fixture;
- the runner can discover both suites;
- the advisor methodology reference still contains the named coverage anchors for Cynefin, SAFe, LeSS, DA, waterfall/stage-gate/V-model, Scrum, Kanban, DSDM, FDD, ASD, XP, RAD, IID, Lean, RUP/UP, DevOps, TDD, MDE, PSP, TSP, and SEMAT/Essence;
- Record Library guidance contains the full-name slug fallback and `beta-corp` regression example.

## Evidence boundary

Repository CI validates suite mechanics, fixture contracts, semantic anchors, and deterministic harness behavior. It does not prove model behavior. Real matched agent runs must still be executed externally before claiming methodology parity or superiority.

The existing three-way report remains valid for the 14 frozen cases it actually executed; its `READY WITH MINOR FIXES` conclusion must not be generalized to the new methodology suite until those cases are run.