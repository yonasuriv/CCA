# Core reference: compatibility, routing, and workspace invariants

Use this reference when designing or restructuring a workspace. CCA converges on upstream conventions; it does not make its preferred implementation mandatory for every compatible project.

Read `methods.md` when the request involves PARA, Zettelkasten, BASB/CODE, second brains/PKM, or composition among human methods, LLM Wiki, ICM, and ordinary projects.

## Compatibility states

- **Native-compatible**: CCA can consume an ICM workspace, LLM Wiki, or ordinary project without structural migration.
- **CCA-hardened**: optional CCA routing or maintenance conventions were added.
- **CCA-conformant**: the workspace intentionally adopts the CCA specification.

Never call an upstream workspace CCA-conformant merely because it can be read by CCA tooling.

PARA, Zettelkasten, and BASB/CODE are method overlays, not additional native compatibility states.

## ICM: full profile vs derived patterns

Distinguish two cases:

- **Native ICM / full ICM profile**: the workspace claims ICM/MWP compatibility and therefore must satisfy the complete applicable current ICM convention and validation surface.
- **ICM-derived patterns**: another workspace borrows useful ICM constructs such as numbered stages, `CONTEXT.md` contracts, or output handoffs without claiming to be a complete native ICM workspace.

Do not use “ICM-compatible” as shorthand for “contains ICM-like stage folders.”

For a **full ICM profile**, preserve and validate all applicable current upstream rules, including:

1. the five-layer routing architecture, with `AGENTS.md` as the authoritative Layer-0 catalog and harness entry files (`CLAUDE.md`) created by directive as single-line `@AGENTS.md` includes where a harness path is needed;
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

A native ICM root may be nested inside a broader CCA/PARA/client workspace. The outer boundary may organize where it lives but must not rewrite the native ICM internals merely for uniformity.

## Portable root guidance

`AGENTS.md` is CCA's preferred portable cross-agent guidance file and the authoritative Layer-0 catalog in CCA-created and CCA-hardened workspaces.

- Preserve nested `AGENTS.md` scopes; the closest applicable file governs its subtree under the AGENTS.md convention.
- `AGENTS.md` has no mandatory CCA heading schema.
- Do not assume it overrides a harness-specific instruction file; native harness discovery remains authoritative.
- Keep one substantive source of truth. When a harness needs its own entry path (`CLAUDE.md`, `GEMINI.md`, ...), create it by directive as a single-line `@AGENTS.md` include, never a second copy of the routing.
- When operating on an existing native ICM workspace, preserve its native `CLAUDE.md` entry path; do not replace or break it merely to make `AGENTS.md` look canonical. If portability is wanted, derive the `AGENTS.md` counterpart from the native entry so the two interoperate under the open AGENTS.md convention.

## Context router file

`CONTEXT.md` is a recommended default for the context/router file, not an enforced requirement. A CCA-created or CCA-hardened workspace may use another name when the project's naming calls for it. When it does:

- declare the alternative name in `AGENTS.md` with a single pointer line so agents and humans can resolve it;
- keep the same mechanics ICM assigns to that layer (token/line allowances, routing behavior) as recommendations, not requirements.

Native ICM workspaces keep `CONTEXT.md` because the upstream profile requires that exact name.

## Knowledge invariants

For native LLM Wiki compatibility, discover the implementation's own schema first. The core behavior is durable sources plus maintained synthesis that compounds across sessions.

CCA may optionally harden a knowledge workspace with `raw/`, `wiki/`, `wiki/index.md`, `log.md`, frontmatter, provenance fields, contradiction sections, and lifecycle states. Those are CCA choices, not universal LLM Wiki requirements.

When Zettelkasten, PARA, or another human method is present beside maintained synthesis, determine authority before writing. Do not silently reinterpret human-authored reference notes as agent-maintained wiki content.

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
- Infer ordinary filesystem semantics when safe; do not create a giant manifest merely to restate obvious paths.
- If a task needs excessive unrelated context, improve routing before increasing prompt size.

## Agent Skills discipline

CCA's first-party Agent Skills are distributed as a suite of focused capabilities. Package portability means implementation paths remain local to each skill package; it does not mean every skill must be a sensible unrelated product when installed alone.

- valid `SKILL.md` frontmatter;
- compact activation-time instructions;
- skill-local `references/`, `assets/`, and `scripts/` loaded progressively;
- implementation file paths remain inside the skill package;
- never reach into a sibling skill directory or repository-global implementation file by relative path;
- semantic delegation to another installed capability is valid, for example `Use cca-lint to validate the selected profile`;
- `cca-architect` coordinates compound architecture work but is not a mandatory gateway for an already-clear lint, ingest, query, sync, or scaffold request.

## Fresh-agent walk test

The CCA walk test supplements profile-specific validation; it does not replace ICM acceptance or another upstream's own rules.

A structured workspace should let a fresh agent:

1. **Orient** — identify the workspace, applicable instruction scope, native profile, and relevant method boundaries.
2. **Act** — perform one representative operation using routed files.
3. **Report** — state what changed, what remains, and what is missing or ambiguous.

If a required decision exists only in chat history or someone's head, durable context is incomplete.
