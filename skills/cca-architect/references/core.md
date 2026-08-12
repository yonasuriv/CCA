# Core reference: compatibility, routing, and workspace invariants

Use this reference when designing or restructuring a workspace. CCA converges on upstream conventions; it does not make its preferred implementation mandatory for every compatible project.

## Compatibility states

- **Native-compatible**: CCA can consume an ICM workspace, LLM Wiki, or ordinary project without structural migration.
- **CCA-hardened**: optional CCA routing or maintenance conventions were added.
- **CCA-conformant**: the workspace intentionally adopts the CCA specification.

Never call an upstream workspace CCA-conformant merely because it can be read by CCA tooling.

## ICM pipeline invariants

For an ICM-compatible pipeline preserve:

1. five-layer routing;
2. native Layer 0 `CLAUDE.md` behavior;
3. root and stage `CONTEXT.md` routing;
4. stage folders named `01-name`, `02-name`, ...;
5. exact stage sections `Inputs`, `Process`, `Outputs`;
6. Inputs columns `Source | File/Location | Section/Scope | Why`;
7. selective section loading;
8. one-way references;
9. one fact, one canonical home;
10. per-stage `output/` handoffs that humans may edit.

Do not add required CCA columns to an ICM contract while calling the contract unchanged.

## Portable root guidance

`AGENTS.md` is CCA's preferred portable cross-agent guidance file where useful.

- Preserve nested `AGENTS.md` scopes; the closest applicable file governs its subtree under the AGENTS.md convention.
- `AGENTS.md` has no mandatory CCA heading schema.
- Do not assume it overrides a harness-specific instruction file; native harness discovery remains authoritative.
- Keep one substantive source of truth and use pointers/includes rather than duplicated rules.

## Knowledge invariants

For native LLM Wiki compatibility, discover the implementation's own schema first. The core behavior is durable sources plus maintained synthesis that compounds across sessions.

CCA may optionally harden a knowledge workspace with `raw/`, `wiki/`, `wiki/index.md`, `log.md`, frontmatter, provenance fields, contradiction sections, and lifecycle states. Those are CCA choices, not universal LLM Wiki requirements.

## CCA file roles

Roles classify function; they do not mandate locations.

| Role | Function |
|---|---|
| catalog | routes to context and stores little substantive content |
| contract | defines one unit of work: inputs, process, outputs |
| factory | stable constraints, references, reusable skills |
| source | durable evidence/input that synthesis should not silently mutate |
| synthesis | maintained derived knowledge |
| product | per-run or per-stage working artifact |
| chronicle | historical record |
| dead | unowned/unreferenced material requiring review |

## Context discipline

- Route before loading broadly.
- Keep routing files compact.
- Select exact sections when a full reference is unnecessary.
- Stable constraints belong in canonical reference/config files, not copied into every router.
- Previous outputs are artifacts, not authoritative quality templates.
- If a task needs excessive unrelated context, improve routing before increasing prompt size.

## Agent Skills discipline

A bundled skill must stand alone as a package:

- valid `SKILL.md` frontmatter;
- compact activation-time instructions;
- skill-local `references/`, `assets/`, and `scripts/` loaded progressively;
- relative paths that remain inside the skill package;
- no required sibling skill or repository-global file for core execution.

## Fresh-agent walk test

A structured workspace should let a fresh agent:

1. **Orient** — identify the workspace and applicable instruction scope.
2. **Act** — perform one representative operation using routed files.
3. **Report** — state what changed, what remains, and what is missing or ambiguous.

If a required decision exists only in chat history or someone's head, durable context is incomplete.
