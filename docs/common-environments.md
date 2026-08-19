## How CCA handles common environments

### Existing code repository

Preserve the project first. Inspect its existing instructions, source tree, tests, build/package configuration, architecture documentation, backlog system, and tool-native guidance.

CCA may add compact routing when it materially improves navigation. It should not introduce pipelines, wikis, PARA folders, manifests, or other structures merely because CCA knows how to work with them.

### Human knowledge workspace

Human organization and epistemic authority are separate concerns. For example:

- PARA may organize Projects, Areas, Resources, and Archives.
- Zettelkasten may govern linked human-authored thinking.
- BASB/CODE may describe the lifecycle through which information is captured, organized, distilled, and expressed.
- An LLM Wiki may maintain evolving synthesis.

All these can coexist at different layers. CCA identifies their boundaries and relationships without collapsing them into one taxonomy.

An LLM Wiki or other maintained agent knowledge system may coexist with human-authored durable knowledge without silently taking ownership of it.

### Native ICM

Keep native ICM native.

CCA is built on ICM principles and preserves current applicable ICM semantics when a workspace claims native ICM compatibility. When a boundary claims native ICM compatibility, its applicable entry behavior, routing, stage definitions, contracts, handoffs, setup/status behavior, progressive disclosure, and validation remain governed by ICM.

CCA may route into the boundary and expose it to surrounding systems OR may add interoperability around a native ICM boundary, but compatibility does not make that workspace CCA-owned.

It must not modify native ICM internals merely to make them resemble another CCA boundary.

Where execution instances need explicit representation, distinguish durable workflow definitions from execution state:

```text
pipeline/
├── stages/        # durable contracts / definitions
└── runs/          # execution instances when the implementation uses them
```

This distinction does not override a native profile's required structure.

### LLM Wiki and maintained knowledge

Discover the implementation's own maintenance model first.

CCA may distinguish:

- durable evidence;
- human-authored notes;
- maintained synthesis;
- provenance;
- freshness;
- supersession.

It does not impose one universal LLM Wiki directory tree.

Agent-maintained synthesis may be rewritten when authorized, provided durable mutations satisfy the boundary's recovery policy.

### Restricted workspaces

Restricted material should be represented as an explicit boundary with stricter access and discovery policy.

A parent boundary may know that the restricted boundary exists without globally indexing its contents.

```text
workspace
└── clients/
    └── acme/        # restricted boundary
```

Default discovery should not cross such a boundary implicitly.

Access requires explicit scope and applicable authority.

### Engineering and delivery methods

Scrum, Kanban, TDD, DevOps, SAFe, LeSS, Disciplined Agile, and other methods remain authorities over the concerns they define.

CCA may identify where those methods apply and route agents toward their relevant artifacts or rules.

It does not turn them into CCA filesystem schemas.

### Delivery and engineering methods

Methods remain authorities at their own scopes. Scrum does not become a filesystem schema. TDD does not become project organization. DevOps does not become a knowledge taxonomy.

CCA helps agents identify which method governs which decision and how those scopes interact, and route agents toward their relevant artifacts or rules.

See [Scenarios](./scenarios.md) and [Method composition](./method-composition.md).