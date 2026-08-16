# Core reference: compatibility, routing, and workspace invariants

Use this reference when designing or restructuring a workspace. CCA converges on upstream conventions; it does not make its preferred implementation mandatory for every compatible project.

Read `methods.md` when the request involves PARA, Zettelkasten, BASB/CODE, second brains/PKM, or composition among human methods, LLM Wiki, ICM, and ordinary projects.

When the request claims or creates **native ICM**, also read `../core/icm-inheritance.md`. That file is a provenance/compatibility map, not a competing ICM specification. Current upstream ICM remains authoritative.

## Compatibility states

- **Native-compatible**: CCA can consume an ICM workspace, LLM Wiki, or ordinary project without structural migration.
- **CCA-hardened**: optional CCA routing or maintenance conventions were added.
- **CCA-conformant**: the workspace intentionally adopts the CCA specification.

Never call an upstream workspace CCA-conformant merely because it can be read by CCA tooling.

PARA, Zettelkasten, and BASB/CODE are method overlays, not additional native compatibility states.

## ICM: full profile vs derived patterns

Distinguish three cases:

- **Native ICM / full ICM profile**: the workspace claims ICM/MWP compatibility and therefore must satisfy the complete applicable current ICM convention and validation surface.
- **ICM skeleton compatibility**: same layer roles and walkable contracts; filenames default to ICM names or are declared in the L0 skeleton map (`../core/spec.md` §5.1). Not a claim of native pipeline acceptance.
- **ICM-derived patterns**: another workspace borrows useful ICM constructs such as numbered stage contracts, folder contracts (default `CONTEXT.md`), or output handoffs without claiming to be a complete native ICM workspace.

Do not use “ICM-compatible” as shorthand for “contains ICM-like stage folders.” Prefer the precise profile name. Agents must not assume contract filenames — resolve from the L0 map, else default to `CONTEXT.md`.

For a **full ICM profile**, preserve and validate all applicable current upstream rules, including:

1. the native five-layer routing architecture, preserving upstream Layer-0 `CLAUDE.md` semantics and the current upstream discovery/entry behavior; portable `AGENTS.md` guidance may be added only as an interoperable counterpart when it does not replace or invalidate the native entry path;
2. one root `CONTEXT.md` and one stage `CONTEXT.md` per stage (exact upstream filenames);
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

`AGENTS.md` is CCA's preferred portable cross-agent guidance file and the authoritative Layer-0 catalog only in CCA-created or CCA-hardened workspaces that intentionally adopt that convention. It is not retroactively the native ICM Layer-0 file.

- Preserve nested `AGENTS.md` scopes; the closest applicable file governs its subtree under the AGENTS.md convention.
- `AGENTS.md` has no mandatory CCA heading schema.
- Do not assume it overrides a harness-specific instruction file; native harness discovery remains authoritative.
- Keep one substantive source of truth. When a harness supports a bridge/include to portable guidance, use that mechanism only when it is verified and compatible with the active profile; do not duplicate routing merely to create parallel instruction files.
- When operating on an existing native ICM workspace, preserve its native `CLAUDE.md` entry path and semantics; do not replace or break it merely to make `AGENTS.md` look canonical. If portability is wanted, add an `AGENTS.md` counterpart only where the harness/profile can consume it without invalidating native ICM.

## Contract files (router + folder contracts)

Default names: root workspace router `CONTEXT.md`; per-working-folder contract `CONTEXT.md`.

Agents MUST NOT assume those filenames. Resolve paths from the Layer-0 skeleton map first; if a role is omitted from the map, use the default. See `../core/spec.md` §5.1.

Outside **native ICM**, either file may be renamed when declared in that L0 map. Native ICM keeps exact upstream names (`CLAUDE.md`, root `CONTEXT.md`, per-stage `CONTEXT.md`).

Folder contracts (whatever named) must still encode one job and, for working folders, Inputs / Process / Outputs / Human check. Shelves that only route (for example PARA maps) may use a short purpose/catalog file; they must not pretend to be stages.

CCA-created and CCA-hardened workspaces SHOULD include the skeleton map even when every path is still the default, so consumers never invent filenames.

## Knowledge invariants

For native LLM Wiki compatibility, discover the implementation's own schema first. The core behavior is durable sources plus maintained synthesis that compounds across sessions.

CCA may optionally harden a knowledge workspace with `raw/`, `wiki/`, `wiki/index.md`, `log.md`, frontmatter, provenance fields, contradiction sections, and lifecycle states. Those are CCA choices, not universal LLM Wiki requirements.

When Zettelkasten, PARA, or another human method is present beside maintained synthesis, determine authority before writing. Do not silently reinterpret human-authored reference notes as agent-maintained wiki content.

For CCA-hardened or freshly built personal hybrids:

- treat human notes and immutable evidence as different layers;
- forbid silent raw rewrites; correct via **supersession** (new source + index);
- prefer checkable integrity (manifest/verify) over prose-only immutability;
- seed a minimal source→wiki citation chain on empty scaffolds;
- keep daily operation self-describing without mandatory external skill modes.

See `methods.md` (Personal hybrid) when projects, notes, research, and wiki intent appear together.

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

Inside native ICM, preserve the upstream Layer-3 factory/reference versus Layer-4 product/working-artifact distinction. The generic CCA role vocabulary may describe broader workspaces but does not replace that native distinction.

## Context discipline

- Route before loading broadly.
- Keep routing files compact.
- Select exact sections when a full reference is unnecessary.
- Stable constraints belong in canonical reference/config files, not copied into every router.
- Previous outputs are artifacts, not authoritative quality templates.
- Infer ordinary filesystem semantics when safe; do not create a giant manifest merely to restate obvious paths.
- If a task needs excessive unrelated context, improve routing before increasing prompt size.

## Agent Skills discipline

CCA's first-party Agent Skill is one installable `cca` package with focused lazily loaded modes. Package portability means implementation paths remain local to the skill package; it does not mean every internal mode becomes a separate product.

- valid `SKILL.md` frontmatter;
- compact activation-time instructions;
- skill-local `references/`, `assets/`, and `scripts/` loaded progressively;
- implementation file paths remain inside the skill package;
- never reach into a removed sibling skill directory or repository-global implementation file by relative path;
- semantic routing between modes is valid, for example `Use lint mode to validate the selected profile`;
- `cca` in `architect` mode coordinates compound architecture work but is not a mandatory gateway for an already-clear lint, ingest, query, sync, or scaffold request.

## Fresh-agent walk test

The CCA walk test inherits and generalizes the cold-agent validation idea while remaining supplemental to profile-specific validation; it does not replace ICM acceptance or another upstream's own rules.

A structured workspace should let a fresh agent:

1. **Orient** — identify the workspace from L0; resolve L1/L2 filenames from the skeleton map (else default `CONTEXT.md`); note native profile and method boundaries.
2. **Act** — open one folder contract; load only its Inputs; perform one representative operation; honor Human check.
3. **Report** — state what changed, what remains, and status from the declared scan surface (pipeline `output/` or hybrid equivalent).

If a required decision exists only in chat history or someone's head, durable context is incomplete.

**ICM skeleton bar:** if the same cold agent could walk an ICM-built workspace of the same form but cannot walk this one without knowing it was “CCA,” the skeleton claim fails (`../core/spec.md` §2.1).
