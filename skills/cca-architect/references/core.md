# Core reference: compatibility, routing, and workspace invariants

Use this reference when designing or restructuring a workspace. CCA converges on upstream conventions; it does not make its preferred implementation mandatory for every compatible project.

## Compatibility states

- **Native-compatible**: CCA can consume an ICM workspace, LLM Wiki, or ordinary project without structural migration.
- **CCA-hardened**: optional CCA routing or maintenance conventions were added.
- **CCA-conformant**: the workspace intentionally adopts the CCA specification.

Never call an upstream workspace CCA-conformant merely because it can be read by CCA tooling.

## ICM: full profile vs derived patterns

Distinguish two cases:

- **Native ICM / full ICM profile**: the workspace claims ICM/MWP compatibility and therefore must satisfy the complete applicable current ICM convention and validation surface.
- **ICM-derived patterns**: another workspace borrows useful ICM constructs such as numbered stages, `CONTEXT.md` contracts, or output handoffs without claiming to be a complete native ICM workspace.

Do not use “ICM-compatible” as shorthand for “contains ICM-like stage folders.”

For a **full ICM profile**, preserve and validate all applicable current upstream rules, including:

1. the five-layer routing architecture and native Layer 0 `CLAUDE.md`;
2. one root `CONTEXT.md` and one stage `CONTEXT.md` per stage;
3. exact stage contract sections `Inputs`, `Process`, `Outputs` and canonical Inputs columns `Source | File/Location | Section/Scope | Why`;
4. lowercase-with-hyphens naming, zero-padded stage prefixes, output-artifact naming, and `.gitkeep` for intentionally empty persistent folders;
5. per-stage `output/` handoffs with an unbroken downstream chain;
6. one-way dependencies and a cycle-free reference graph;
7. selective section routing and one canonical home per substantive rule;
8. `CONTEXT.md` purity: routing/process, not embedded reference material;
9. `setup` and `status` trigger behavior as defined by current ICM, including a flat all-at-once system-level questionnaire;
10. complete placeholder coverage and valid conditional placeholder blocks where placeholders are used;
11. tool prerequisite guides and verification when external system tools are required;
12. checkpoints for applicable creative stages and audits for applicable creative/build stages;
13. specification stages that define WHAT/WHEN rather than implementation HOW;
14. value validation for applicable content-producing stages;
15. docs-over-outputs discipline: prior products are not authoritative quality templates;
16. shared constants for configurable values in applicable code-producing workspaces;
17. current ICM quality guardrails, including routing/reference size limits, readable plain language, and ICM-specific formatting rules;
18. a clean end-to-end validation equivalent to the current ICM workspace-builder validation stage before claiming the generated workspace is ready.

The upstream ICM `_core/CONVENTIONS.md` is canonical for ICM semantics. The workspace-builder’s validation stage is the practical acceptance checklist for generated ICM workspaces. If either changes, prefer the current upstream over a stale CCA snapshot.

CCA may prefer Mermaid for its own explanatory diagrams, but it must not replace an output format that the active upstream profile explicitly requires.

## Portable root guidance

`AGENTS.md` is CCA's preferred portable cross-agent guidance file where useful.

- Preserve nested `AGENTS.md` scopes; the closest applicable file governs its subtree under the AGENTS.md convention.
- `AGENTS.md` has no mandatory CCA heading schema.
- Do not assume it overrides a harness-specific instruction file; native harness discovery remains authoritative.
- Keep one substantive source of truth and use pointers/includes rather than duplicated rules.
- In a native ICM workspace, adding `AGENTS.md` must not replace or break the ICM `CLAUDE.md` entry path.

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

The CCA walk test supplements profile-specific validation; it does not replace ICM acceptance or another upstream's own rules.

A structured workspace should let a fresh agent:

1. **Orient** — identify the workspace and applicable instruction scope.
2. **Act** — perform one representative operation using routed files.
3. **Report** — state what changed, what remains, and what is missing or ambiguous.

If a required decision exists only in chat history or someone's head, durable context is incomplete.
