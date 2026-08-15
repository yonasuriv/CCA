# Documentation Index

CCA keeps runtime authority inside the installable `skills/cca/` package. Repository documentation explains that authority; it does not duplicate a second specification.

## Start here

- [Getting started](getting-started.md) — choose the smallest useful CCA mode for an existing or new workspace.
- [FAQ](faq.md) — common integration and compatibility questions.
- [Scenarios](scenarios.md) — expected behavior for code repositories, second brains, ICM, mixed methods, and no-op cases.
- [Method composition](method-composition.md) — how human, agent, delivery, and engineering methods coexist without being flattened.
- [Design principles](design-principles.md) — reasoning behind the architecture.
- [Standards](standards.md) — tracked upstream compatibility surfaces.
- [Migration](migration.md) — preserving existing structures while adopting CCA guidance.

## Runtime authority

The canonical installable surface is:

```text
skills/cca/
├── SKILL.md
├── references/
│   ├── core/
│   │   ├── spec.md
│   │   ├── compatibility.md
│   │   ├── method-composition.md
│   │   └── adapters.md
│   ├── architect/
│   │   ├── mode.md
│   │   ├── core.md
│   │   ├── forms.md
│   │   ├── methods.md
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
    └── templates/
```

Architect and advisor references are deliberately separate domains. Architect owns workspace structure and composition; advisor owns engineering/process judgment. Architect may consult advisor references lazily, but does not absorb or duplicate them.

## Repository layout

```text
CCA/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── CONTRIBUTING.md
├── CITATION.cff
├── docs/
├── skills/
│   └── cca/
├── examples/
│   ├── workspaces/
│   ├── publications/
│   ├── conversations/
│   └── transcripts/
└── .github/
    ├── workflows/
    └── scripts/
        └── validate_repo.py
```

`examples/` and `docs/` are explanatory/non-normative unless a file explicitly says otherwise. Normative CCA runtime semantics live under `skills/cca/references/core/` so they remain available after the skill is installed.