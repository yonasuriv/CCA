# Contributing to CCA

CCA has one governing rule: **converge on upstream conventions instead of creating near-compatible forks.**

## Before changing behavior

Identify which surface the change affects:

- ICM / Model Workspace Protocol
- LLM Wiki
- AGENTS.md
- Agent Skills / `SKILL.md`
- method-overlay composition such as PARA, Zettelkasten, or BASB/CODE
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
- [ ] Are PARA, Zettelkasten, BASB/CODE, and similar methods treated as overlays rather than invented native compatibility profiles?
- [ ] Do nested native/method boundaries remain intact when an outer organization changes?
- [ ] Does nested `AGENTS.md` scope remain intact?
- [ ] Do skill implementation references remain package-local, with no sibling/repository-global filesystem dependency?
- [ ] If skills coordinate, is that coordination expressed semantically by skill name rather than by sibling path?
- [ ] Is a new convention actually necessary, or does an upstream/ecosystem convention already solve it?

For ICM, treat the current upstream `_core/CONVENTIONS.md` as canonical semantics and the workspace-builder's final validation stage as the practical acceptance checklist for generated workspaces. CCA's walk test is supplemental, not a waiver for upstream failures.

## Documentation structure

- `spec/` is normative CCA behavior, including method-composition rules.
- `docs/` explains usage, migration/hardening, principles, FAQ, method composition, and tracked upstream standards.
- `skills/` implements the CCA capability suite through focused Agent Skill packages.
- `examples/` must be executable evidence of the profile they actually claim, not illustrative pseudo-state or overclaimed compatibility.

When a compatibility or composition rule changes, update the full affected surface in one PR: spec, skills/templates, examples, migration/getting-started/FAQ, and `docs/standards.md` where relevant.

## Visuals

Prefer Mermaid for CCA-owned architecture, routing, lifecycle, and dependency diagrams. Use plain-text trees for literal filesystem layouts. If an active upstream profile requires a specific representation, preserve that representation rather than replacing it with a CCA preference.

## Skills

Follow the current Agent Skills open standard specification and key design principles:

1. **Accepted Format**
   A single markdown file containing YAML frontmatter for metadata (name, description) and a markdown body for instructions.
2. **Context Efficiency**
   Skills body should all be under 5,000 tokens (ideally under 500 lines) and push detailed references, scripts, or assets into separate files as lazy-load references to avoid context pollution.
3. **Constraints**
   The name field must be lowercase with hyphens (max 64 characters), and description is limited to 1,024 characters.
4. **Precise Description**
   The description field is the primary trigger mechanism; it must be specific, include trigger keywords, and clearly define the skill's scope and boundaries to ensure accurate activation.
5. **Process Over Prose**
   Skills should define step-by-step workflows with exit criteria rather than serving as reference documentation; they must guide the agent on what to do, not just what to know.
6. **Constitutional Rules**
   Instructions should act as strict contracts with explicit guardrails, preventing the agent from guessing or overriding deterministic steps.
7. **Test-Driven Creation**
   Validate skills by testing against realistic prompts to ensure trigger accuracy and output quality, often using a RED-GAP-GREEN-REFACTOR cycle to bridge performance gaps.
8. **Progressive Disclosure**
   Agents load only the metadata initially, loading the full instructions only when the skill is triggered, keeping context costs low.

CCA's six first-party skills are intended to be distributed as a focused suite; the package split exists for precise triggering and progressive disclosure.

In particular:

- `name` must match the skill directory and satisfy current naming limits;
- `description` must explain both purpose and trigger conditions and remain within the current limit;
- keep `SKILL.md` compact and progressively disclose detailed material through skill-local resources;
- implementation file references must stay inside the skill package;
- never reach into a sibling skill directory or repository-global implementation file by relative path;
- cross-skill coordination may use semantic skill names such as `Use `lint` mode`;
- do not collapse focused operations into one monolithic skill merely to centralize routing;
- `cca` in `architect` mode may coordinate compound architecture flows but is not a mandatory gateway for direct lint/ingest/query/sync/scaffold requests.

## Validation

Before submitting changes, run the repository validator script _(automated github workflow)_:

```bash
python .github/scripts/validate_repo.py
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
