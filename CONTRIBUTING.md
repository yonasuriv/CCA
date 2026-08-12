# Contributing to CCA

CCA has one governing rule: **converge on upstream conventions instead of creating near-compatible forks.**

## Before changing behavior

Identify which surface the change affects:

- ICM / Model Workspace Protocol
- LLM Wiki
- AGENTS.md
- Agent Skills / `SKILL.md`
- CCA-only semantics

If an upstream is affected, verify its current primary source before editing. Do not rely on CCA's existing wording as evidence that upstream still behaves the same way.

## Compatibility checklist

A contribution should answer all applicable questions:

- [ ] Does native ICM still work without structural migration?
- [ ] Are ICM stages still lowercase, zero-padded, and hyphenated (`01-name`)?
- [ ] Do ICM stage contracts retain the exact `Inputs` / `Process` / `Outputs` shape and canonical Inputs columns?
- [ ] Are selective section loading, one-way references, canonical sources, and human-editable output handoffs preserved?
- [ ] Does native LLM Wiki remain implementation-flexible rather than being forced into CCA's preferred taxonomy/metadata?
- [ ] Are CCA-specific hardening choices clearly labeled as CCA choices?
- [ ] Does nested `AGENTS.md` scope remain intact?
- [ ] Does each skill remain independently portable, with skill-local relative resources and no required sibling/repository-global dependency?
- [ ] Is a new convention actually necessary, or does an upstream/ecosystem convention already solve it?

## Documentation structure

- `spec/` is normative CCA behavior.
- `docs/` explains usage, migration/hardening, principles, FAQ, and tracked upstream standards.
- `skills/` must implement the spec without depending on repository-global files for core execution.
- `examples/` must be executable evidence of the documented conventions, not illustrative pseudo-state.

When a compatibility rule changes, update the full affected surface in one PR: spec, skills/templates, examples, migration/getting-started/FAQ, and `docs/standards.md` where relevant.

## Visuals

Prefer Mermaid for architecture, routing, lifecycle, and dependency diagrams. Use plain-text trees for literal filesystem layouts where a tree is clearer than a graph.

## Skills

Follow the current Agent Skills specification. In particular:

- `name` must match the skill directory and satisfy current naming limits;
- `description` must explain both purpose and trigger conditions and remain within the current limit;
- keep `SKILL.md` compact and progressively disclose detailed material through skill-local resources;
- use relative references from the skill root;
- core execution must work if the skill is copied by itself.

## Validation

Run:

```bash
python scripts/validate_repo.py
```

The validator is a regression gate, not a substitute for upstream review. A passing check means the repository still satisfies the mechanical invariants it knows how to test.

## Proposals

Prefer changes motivated by a real interoperability or maintenance problem. New semantics should explain:

1. what breaks without the change;
2. why an existing upstream convention cannot solve it;
3. how the change remains optional to consumers that do not need it;
4. how it degrades when a specific agent/runtime feature is unavailable.

Keep the specification smaller than the implementation possibilities. It is easier to add a necessary rule later than to remove a convention that downstream workspaces already copied.
