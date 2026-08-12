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
- [ ] If a workspace is described as **native ICM-compatible**, does it satisfy the complete applicable current ICM profile and workspace-builder-equivalent acceptance surface, not only stage naming/contracts?
- [ ] If only selected ICM constructs are used, are they labeled **ICM-derived** rather than promoted to full native compatibility?
- [ ] Are ICM stages still lowercase, zero-padded, and hyphenated (`01-name`)?
- [ ] Do ICM stage contracts retain the exact `Inputs` / `Process` / `Outputs` shape and canonical Inputs columns?
- [ ] Are selective section loading, one-way references, canonical sources, and human-editable output handoffs preserved?
- [ ] Where applicable, are native ICM `setup`/`status`, questionnaire, placeholder, prerequisite, checkpoint, audit, spec/value, shared-constant, and quality-guardrail rules preserved?
- [ ] Does native LLM Wiki remain implementation-flexible rather than being forced into CCA's preferred taxonomy/metadata?
- [ ] Are CCA-specific hardening choices clearly labeled as CCA choices?
- [ ] Does nested `AGENTS.md` scope remain intact?
- [ ] Does each skill remain independently portable, with skill-local relative resources and no required sibling/repository-global dependency?
- [ ] Is a new convention actually necessary, or does an upstream/ecosystem convention already solve it?

For ICM, treat the current upstream `_core/CONVENTIONS.md` as canonical semantics and the workspace-builder's final validation stage as the practical acceptance checklist for generated workspaces. CCA's walk test is supplemental, not a waiver for upstream failures.

## Documentation structure

- `spec/` is normative CCA behavior.
- `docs/` explains usage, migration/hardening, principles, FAQ, and tracked upstream standards.
- `skills/` must implement the spec without depending on repository-global files for core execution.
- `examples/` must be executable evidence of the profile they actually claim, not illustrative pseudo-state or overclaimed compatibility.

When a compatibility rule changes, update the full affected surface in one PR: spec, skills/templates, examples, migration/getting-started/FAQ, and `docs/standards.md` where relevant.

## Visuals

Prefer Mermaid for CCA-owned architecture, routing, lifecycle, and dependency diagrams. Use plain-text trees for literal filesystem layouts. If an active upstream profile requires a specific representation, preserve that representation rather than replacing it with a CCA preference.

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

The validator is a repository regression gate, not a substitute for upstream acceptance review. A passing check means the repository still satisfies the mechanical invariants it knows how to test; it does **not** certify an arbitrary workspace as fully native ICM-compatible.

For a native ICM claim, run or reproduce the complete applicable current upstream validation surface as well.

## Proposals

Prefer changes motivated by a real interoperability or maintenance problem. New semantics should explain:

1. what breaks without the change;
2. why an existing upstream convention cannot solve it;
3. how the change remains optional to consumers that do not need it;
4. how it degrades when a specific agent/runtime feature is unavailable.

Keep the specification smaller than the implementation possibilities. It is easier to add a necessary rule later than to remove a convention that downstream workspaces already copied.
