# Documentation Index

CCA keeps runtime authority inside the installable `skills/cca/` package. Repository documentation explains that authority; it does not duplicate a second specification.

## Start here

- [Getting started](getting-started.md) — choose the smallest useful CCA mode for an existing or new workspace.
- [FAQ](faq.md) — common integration and compatibility questions.
- [Scenarios](scenarios.md) — expected behavior for code repositories, second brains, ICM, mixed methods, and no-op cases.
- [Common environments](common-environments.md) — how CCA applies across common workspace types without imposing one tree.
- [Compatibility details](compatibility-details.md) — explanatory framework/methodology compatibility using the current composable vocabulary.
- [Method composition](method-composition.md) — how human, agent, delivery, and engineering methods coexist without being flattened.
- [Design principles](design-principles.md) — reasoning behind the architecture.
- [Standards](standards.md) — tracked upstream compatibility surfaces.
- [References](references.md) — upstream, methodology, and citation links.
- [Migration](migration.md) — preserving existing structures while adopting CCA guidance.
- [Contributing](../CONTRIBUTING.md) — contribution workflow and the complete validation suite.
- [Pull request template](../.github/PULL_REQUEST_TEMPLATE.md) — review checklist for authority, compatibility, documentation, and validation.
- [Evaluation protocol](../evals/README.md) — behavioral-evaluation contracts, release-test boundaries, and benchmark methodology.
- [Changelog](../CHANGELOG.md) — released CCA milestones and the current unreleased change bucket.

The root [`README.md`](../README.md) is the public product overview. This file is the exhaustive documentation/repository index. Both must link every current public page under `docs/`; they should not duplicate the same explanatory content.

## Runtime authority

The canonical installable surface is:

```text
skills/cca/
├── SKILL.md
├── CITATION.cff
├── references/
│   ├── core/
│   │   ├── spec.md
│   │   ├── compatibility.md
│   │   ├── method-composition.md
│   │   ├── adapters.md
│   │   ├── icm-inheritance.md
│   │   └── diagram-models.md
│   ├── architect/
│   │   ├── mode.md
│   │   ├── core.md
│   │   ├── forms.md
│   │   ├── methods.md
│   │   ├── workspace-builder.md
│   │   ├── native-icm-setup.md
│   │   ├── hybrid-workspace.md
│   │   └── system-map.md
│   ├── advisor/
│   │   ├── mode.md
│   │   ├── engineering-principles.md
│   │   ├── frameworks-and-methodologies.md
│   │   ├── security-and-adversarial-thinking.md
│   │   ├── agent-system-design.md
│   │   ├── context-engineering.md
│   │   ├── ai-ml-practice.md
│   │   └── escalation-triggers.md
│   └── operations/
│       ├── scaffold.md
│       ├── sync.md
│       ├── ingest.md
│       ├── query.md
│       └── lint.md
└── assets/
    ├── hybrid-workspace/    # profile schema, templates, generator, audit, tests
    ├── scripts/             # reusable source/knowledge helpers
    └── templates/           # portable workspace/context templates
```

Architect and advisor references are deliberately separate domains. Architect owns workspace structure and composition; advisor owns engineering/process judgment. Architect may consult advisor references lazily, but does not absorb or duplicate them.

The Hybrid Workspace Profile is optional and CCA-owned. Its current bundled schema is v2; the complete reference implementation and adversarial tests travel inside `skills/cca/assets/hybrid-workspace/` so the installed skill remains self-contained.

## Repository layout

```text
CCA/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── CONTRIBUTING.md
├── CITATION.cff
├── CHANGELOG.md
├── docs/
├── skills/
│   └── cca/
├── examples/
│   ├── workspaces/
│   ├── publications/
│   ├── conversations/
│   └── transcripts/
├── evals/
│   ├── cases/
│   ├── methodologies/
│   ├── personal-hybrid-intent/
│   └── tests/
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md
    ├── workflows/
    │   └── validate.yml
    └── scripts/
        ├── validate_repo.py
        └── validate_distribution.py
```

`examples/` and `docs/` are explanatory/non-normative unless a file explicitly says otherwise. Normative CCA runtime semantics live under `skills/cca/references/core/` so they remain available after the skill is installed. `docs/_wip.md` is historical/development material and must not be treated as normative or current release authority.

`evals/` and `.github/` are repository-development surfaces rather than installed CCA runtime authority. They exist to exercise behavioral claims, release-readiness invariants, Hybrid profile behavior, and distribution integrity against the exact repository candidate.
