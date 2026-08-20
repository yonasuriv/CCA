# Contributing to CCA

CCA has one governing rule: **converge on proven upstream conventions instead of creating near-compatible forks.**

The human objective remains explicit: **automation is the means; augmenting human capabilities is the goal.**

## Before changing behavior

Identify which authority the change affects:

- ICM / Model Workspace Protocol;
- LLM Wiki;
- AGENTS.md;
- Agent Skills / `SKILL.md`;
- a human methodology such as PARA, Zettelkasten, BASB/CODE, Scrum, Kanban, etc.;
- a CCA-owned semantic/profile/operation;
- repository-only development/documentation infrastructure.

If an upstream compatibility claim is affected, verify the current primary source before editing. CCA's existing wording is not evidence that the upstream still behaves the same way.

## Core contribution checks

- [ ] Does the change preserve upstream authority rather than redefine it?
- [ ] Does a valid upstream-native workspace remain CCA-compatible without structural migration?
- [ ] Are partial upstream patterns clearly distinguished from upstream-native conformance?
- [ ] Does the change resolve through `boundary + semantic role -> binding` rather than turn a default path into identity?
- [ ] Are nested boundaries and instruction scopes preserved?
- [ ] Is a new CCA convention actually necessary, or does an upstream/ecosystem convention already solve it better?
- [ ] Does the change improve or preserve human agency, comprehension, portability, and inspectability?
- [ ] Are deterministic invariants mechanically testable where practical?

## Compatibility vocabulary

Use these terms consistently:

- **Upstream-native** — passes the upstream's own current rules.
- **CCA-compatible** — CCA resolves/operates without structural migration or semantic replacement.
- **CCA-conformant** — explicitly adopts normative CCA interoperability semantics.
- **Profile-conformant** — passes a named optional CCA-owned profile.
- **CCA-hardened** — optional CCA capabilities added without invalidating native semantics.
- **ICM-derived** — selected ICM patterns used without claiming upstream-native ICM.

Do not revive ambiguous `Native-compatible` terminology.

## Portable distribution boundary

`skills/cca/` is the complete installable CCA distribution.

Any resource required to understand, resolve, generate, operate, validate, or maintain behavior advertised by the skill MUST live inside `skills/cca/`.

Repository-level files MAY provide development tooling, CI, examples, research, publications, and human-facing explanation, but MUST NOT be the sole authority for installed runtime/normative CCA semantics.

Consequences:

- `skills/cca/SKILL.md` is the installed entry/router;
- `skills/cca/references/core/` carries shared normative semantics/compatibility;
- `skills/cca/references/architect/`, `advisor/`, and `operations/` preserve their existing domain boundaries;
- `skills/cca/assets/` carries portable templates/scripts/reference implementations according to the existing package topology;
- runtime references must not escape to repository-global docs or removed sibling skills;
- repository docs should point back to the skill-local authority rather than create a second specification.

## One skill, seven modes

CCA ships one `cca` Agent Skill with seven lazily loaded modes:

`architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`, `advise`.

Do not reintroduce separate `cca-architect`, `cca-lint`, etc. packages. Modes are operation surfaces inside one portable semantic authority. Progressive disclosure comes from skill-local references/assets/scripts.

Profiles are a separate dimension. A new workspace profile is not automatically a new mode.

## Hybrid Workspace Profile changes

The optional CCA Hybrid Workspace Profile lives completely inside the installed skill.

The **current bundled schema is v2**. It preserves the complete frozen-v1 semantic/policy/authority baseline and adds only `reference.curated` and `reference.collected` admission classifications beneath `knowledge.reference`. The v2 bump is deliberate: frozen v1 already declared that key additions require a schema-version bump.

Do not casually change either the v1 baseline or the v2 admission extension. Before changing the profile:

1. determine whether the issue is actually a movable `binding` rather than a semantic-key/classification problem;
2. preserve existing key/policy/authority meanings for non-breaking binding changes;
3. require the declared schema-version treatment for changes the profile marks breaking;
4. keep `reference.curated`/`reference.collected` as admission classifications composing with `knowledge.reference`, not competing knowledge roles;
5. preserve the distinction `source admission/provenance != content authorship != semantic role`;
6. add a failing regression/adversarial test before implementation changes;
7. verify generation/audit operate on an explicit target workspace, never the installed tool/package directory;
8. verify `context.router` follows its declared binding;
9. verify moved `_state/`, `_runtime/`, `20-sources/`, and other defaults do not leak into generated artifacts;
10. verify most-specific nested binding policy prevents parent permissions from widening child source policy;
11. verify collected-source acquisition provenance/content identity and no-loose-parent-source invariants;
12. keep the reviewed scripts/templates/tests within `skills/cca/`.

For source admission specifically:

- `reference.curated` is human-admitted/read-only to agents;
- `reference.collected` uses existing append/add-child semantics for agent/tool deposits, not unrestricted mutation;
- existing collected objects remain immutable to normal agent operation;
- human review changes review metadata, not original admission classification;
- evidence presence never implies truth/endorsement;
- synthesis remains `knowledge.durable`, deliverables remain `output.artifact`, finite research work remains `work.project`.

The profile is not native ICM. Nested upstream-native ICM boundaries remain governed by current ICM.

## ICM contribution checks

For an upstream-native ICM claim, current upstream ICM is authoritative. Validate the complete applicable acceptance surface, including current routing/layer semantics, exact contract representation, naming, handoffs, dependency direction, selective loading, canonical sources, setup/status, questionnaire/placeholder behavior, tools, checkpoints/audits/value validation, shared constants, quality guardrails, and workspace-builder-equivalent validation where applicable.

CCA's walk test is supplemental, never a waiver for upstream failures.

If contributing a workspace to the ICM repository, also follow that repository's current contribution policy. Interoperability does not bypass upstream contribution rules.

## Documentation structure

- `skills/cca/references/core/` — normative installed CCA semantics and compatibility.
- `skills/cca/references/...` — installed architecture/operation/advisor knowledge.
- `skills/cca/assets/` — installed portable implementation resources.
- `docs/` — explanatory usage/design/migration/FAQ/standards material that must remain consistent with skill-local authority.
- `examples/` — evidence/examples for the claims they actually make.
- `.github/` and `evals/` — repository development/validation infrastructure.

When semantics change, update the affected skill-local authority first, then update explanatory docs/examples and regression checks in the same change.

## Agent Skills rules

Follow the current Agent Skills standard. In particular:

- valid `SKILL.md` frontmatter;
- precise trigger description;
- compact activation-time instructions;
- progressive disclosure through skill-local resources;
- no package-escaping implementation dependencies;
- scripts/assets may be bundled when they make the capability portable;
- deterministic tests should exercise real installed resources, not a separate duplicate implementation.

## Validation

Before proposing integration, run:

```bash
python -m unittest discover -s evals/tests -v
python -m pip install -r skills/cca/assets/hybrid-workspace/requirements.txt
python -m unittest discover -s skills/cca/assets/hybrid-workspace/tests -v
python skills/cca/assets/hybrid-workspace/audit.py --self-test
python .github/scripts/validate_repo.py
python .github/scripts/validate_distribution.py
```

These are CCA repository/profile regression gates. They do not replace a supported upstream's own acceptance tests for an upstream-native claim.

## Proposals

A new CCA semantic should answer:

1. What real interoperability/maintenance problem breaks without it?
2. Why does an existing upstream or ordinary filesystem convention not already solve it?
3. Which boundary owns the semantic?
4. What remains optional for consumers that do not need it?
5. How does it remain agent/vendor/runtime/path agnostic?
6. How is it validated and evolved without silently redefining existing systems?

Keep the normative architecture smaller than the implementation possibilities.
