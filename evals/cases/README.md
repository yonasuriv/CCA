# Evaluation case contract

Each behavioral case should be a directory named `NN-short-name/` containing enough material for a runner to execute the task without hidden evaluator knowledge.

Recommended case surface:

```text
NN-case/
├── prompt.md
├── fixture/
├── assertions.md
└── judge.md
```

- `prompt.md` — identical user/task prompt for both arms.
- `fixture/` — identical starting filesystem state.
- `assertions.md` — deterministic invariants, forbidden behaviors, and case-specific native compatibility checks.
- `judge.md` — blind qualitative dimensions and tie-breaking guidance; never identify which output is CCA/upstream.

A runner may add machine-readable assertion files later, but the Markdown contract remains the human-auditable source.

## Required case properties

1. Do not use an existing upstream output as “ground truth” unless byte/shape identity is actually normative.
2. Grade semantics and acceptance invariants, not resemblance to one implementation.
3. Include at least one forbidden behavior where over-structuring is a plausible failure.
4. When the case claims native compatibility, identify the exact upstream authority/pin used by the run.
5. When the case tests composition, identify each independent authority and what CCA is allowed to add between them.
6. A no-change result must be gradeable as success where intervention is unnecessary.

The scenario matrix and execution rules are defined in the parent [evaluation protocol](../README.md).

## Implemented cases

Directories `01-` through `14-` are executable fixture contracts, not recorded model outcomes. Each contains `case.json`, `prompt.md`, `fixture/`, and `assertions.json`. Assertions intentionally target semantic invariants and preservation boundaries rather than byte-for-byte reproduction of a pre-existing upstream golden workspace.

This is the **core interoperability suite**. Broader process/methodology reasoning is tested separately under [`../methodologies/`](../methodologies/); do not infer that the 14 core cases cover the full advisor corpus.
