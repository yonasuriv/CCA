# Standards

## Foundations

### Software engineering fundamentals

CCA applies established engineering principles to context architecture rather than treating AI workspaces as an entirely new discipline.

These include, but not limited to:

- **separation of concerns** — context, knowledge, state, execution, and artifacts should not become one undifferentiated layer;
- **explicit boundaries** — independent systems should expose clear interfaces and authority instead of relying on path guessing;
- **canonical authority** — substantive facts and rules should have one authoritative home;
- **loose coupling and high cohesion** — boundaries should depend on stable contracts rather than internal implementation details;
- **stable interfaces over implementations** — semantic roles remain stable even when their concrete bindings change;
- **progressive disclosure** — load the minimum context required for the current task;
- **least privilege** — agents should receive only the scope and mutation authority required for the operation;
- **recoverability** — durable mutations should be reversible, reconstructable, or explicitly superseded;
- **derived state over duplicated state** — indexes, dashboards, caches, and reports should be generated from canonical sources where practical;
- **deterministic validation** — checkable invariants should be validated mechanically rather than left entirely to runtime interpretation;
- **graceful fallback** — broad search should be a fallback when routing fails, not the default discovery mechanism;
- **portability** — durable context should remain understandable without requiring a proprietary model, runtime, database, or vendor.

### Open standards and ecosystem conventions

- **Agent entry points — `AGENTS.md`** for portable, scoped agent guidance.
- **Agent Skills — `SKILL.md`** for progressively disclosed reusable capabilities.
- **MCP and other runtimes/adapters** as optional execution and tool interfaces.

CCA preserves the authority and precedence rules of the environments in which these conventions operate rather than assuming it can override them.

### Agent context and maintained knowledge

- **ICM / Model Workspace Protocol** for filesystem structure as agent architecture, staged routing, handoffs, contracts, and progressive context loading.
- **LLM Wiki** as a pattern for persistent, maintained knowledge that compounds across sessions rather than being repeatedly reconstructed from raw sources.

CCA may compose with these systems or use patterns derived from them, but partial adoption does not imply native compatibility.

### Human knowledge work

- **PARA** for action-oriented organization across Projects, Areas, Resources, and Archives.
- **BASB / CODE** for the lifecycle of capturing, organizing, distilling, and expressing knowledge.
- **Zettelkasten** for durable, addressable, linked idea development.
- **Personal planning and execution techniques** such as GTD, Timeboxing, the Pomodoro Technique, and the Eisenhower Matrix.

CCA can map and route across their scopes without redefining their semantics or turning them into CCA-owned filesystem schemas. These remain independent methods.

### Engineering and delivery methods

CCA can reason about and compose with engineering and delivery methods such as ASD, Disciplined Agile, DevOps, DSDM, FDD, IID, Kanban, Lean Software Development, LeSS, MDE, MSF, PSP, RAD, RUP, SAFe, Scrum, SEMAT, TDD, TSP, UP, XP, and others.

CCA may identify which method governs a decision, workflow, artifact, or boundary and how that scope interacts with others. It does not absorb those methods into a universal CCA process. Their semantics remain theirs.

> See [References](#references).

## Core rule

**Convergence over invention.**

CCA must not replace, absorb, supersede, or silently redefine an existing framework, methodology, standard, protocol, convention, or knowledge system merely to make everything appear uniform.

Preserve distinct authorities.

Connect them through explicit semantics, boundaries, bindings, mappings, routing, precedence, and compatibility rules.

If an existing workspace is already clear, navigable, maintainable, and interoperable, doing nothing is a valid CCA outcome.

## Upstream standards tracked by CCA

CCA converges on existing conventions where they already solve the problem. This file is the maintenance surface for standards/upstreams that materially constrain CCA. It is not a catalog of every AI or knowledge-management method.

| Standard / upstream | CCA dependency | Compatibility rule |
|---|---|---|
| [AGENTS.md](https://agents.md) | Portable agent instructions and nested directory-scoped guidance | Use `AGENTS.md` as the canonical portable instruction file where the standard is applicable. Respect nearest-file precedence in nested trees. Do not invent a competing portable root filename. |
| [Agent Skills](https://agentskills.io) | Portable `SKILL.md` packages | Every bundled skill must satisfy the current Agent Skills specification, keep `SKILL.md` compact, keep implementation file references inside the package, and preserve progressive disclosure. CCA skills may coordinate by semantic skill name without relying on sibling filesystem paths. |
| [ICM / Model Workspace Protocol](https://github.com/RinDig/Interpretable-Context-Methodology) | Five-layer routing, stage contracts, one-way references, selective section loading, canonical sources, human-editable handoffs, onboarding, quality gates | Preserve ICM shapes and semantics unchanged where CCA claims native ICM compatibility. Treat `_core/CONVENTIONS.md` as the canonical semantic authority and the workspace-builder validation stage as the practical acceptance checklist for generated workspaces. CCA extensions must remain optional to an ICM consumer. |
| [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | Persistent LLM-maintained synthesis over durable source material | Preserve the idea file's intentionally flexible implementation surface. CCA may recommend stronger conventions, but must not mislabel CCA-specific schema, frontmatter, directory, or logging choices as LLM Wiki requirements. |
| [MCP](https://modelcontextprotocol.io) | Tool/context transport outside the filesystem workspace | Treat MCP as an adjacent runtime/tool protocol, not a CCA replacement or required dependency. Filesystem-native CCA workspaces remain useful without MCP. |

## Adjacent methodologies and influences

CCA also composes with methodologies that shape human organization or knowledge work but do **not** currently define structural CCA compatibility profiles.

| Methodology | Role in CCA | Composition rule |
|---|---|---|
| **Building a Second Brain / CODE** | Human knowledge-work lifecycle: Capture, Organize, Distill, Express | Treat as a method overlay. CCA may route the files/workflows participating in the lifecycle but must not claim to implement BASB as a filesystem standard. |
| **PARA** | Action-oriented organization: Projects, Areas, Resources, Archives | May organize an outer workspace while nested coding projects, ICM roots, LLM Wikis, or other boundaries retain their own semantics. |
| **Zettelkasten** | Linked idea-development / note method | Preserve addressable linked notes and determine local write authority. Do not silently reinterpret every zettel as agent-maintained wiki synthesis. |

These belong in [`method-composition.md`](method-composition.md), not in the structural compatibility matrix above. If one of these methodologies later publishes a concrete machine-facing contract that CCA intentionally adopts, its status can be reconsidered.

## ICM compatibility authority

CCA must distinguish **native ICM compatibility** from merely borrowing ICM patterns.

For a native ICM claim, check the current upstream in this order:

1. `_core/CONVENTIONS.md` — canonical ICM/MWP rules and patterns.
2. `workspaces/workspace-builder/stages/05-validation/CONTEXT.md` — practical validation/acceptance checklist used by the upstream builder.
3. Root README contribution/PR checklist — additional repository-level expectations for contributed workspaces.
4. The actual workspace's own `CLAUDE.md`, root `CONTEXT.md`, stage contracts, references, setup files, and outputs.

CCA's own walk test is supplemental. It must not replace a stricter upstream acceptance surface.

A project that uses `stages/01-name/` and ICM-style stage contracts but omits the rest of the native ICM profile should be described as **ICM-derived**, not as fully native ICM-compatible.

Where upstream ICM prescribes a specific trigger or representation, CCA preferences such as Mermaid diagrams do not override it.

### Current upstream mechanics snapshot

The following concrete mechanics are normative *in the current upstream* and are authoritative when CCA performs native ICM validation. They are recorded here as the tracked snapshot so CCA can act without re-fetching manuals; if upstream changes any value, CCA must converge toward the new upstream per the upstream-change rule below, never treat this table as a frozen fork.

CCA's own Layer-0 convention is a superset: in CCA-created and CCA-hardened workspaces, `AGENTS.md` is the authoritative Layer-0 catalog and harness entry files (`CLAUDE.md`) are created by directive as single-line `@AGENTS.md` includes, not shipped as template assets. When a workspace claims upstream native ICM compatibility, the upstream conventions in this table still govern its `CLAUDE.md` entry path; CCA does not rewrite an existing native entry merely for uniformity.

| Upstream mechanic | Current upstream value | CCA behavior |
|---|---|---|
| Five-layer token budgets | Layer 0 `CLAUDE.md` ~800 tokens; Layer 1 root `CONTEXT.md` ~300 tokens; Layer 2 stage `CONTEXT.md` ~200-500 tokens; Layer 3/4 selective | Enforce selective loading; do not restate new budgets in stage contracts |
| `setup` trigger | Reads `setup/questionnaire.md`, asks questions conversationally, replaces placeholders workspace-wide, scans for remaining `{{` patterns, completes only when zero remain | Validate the onboarding flow resolves placeholders with zero remaining |
| `status` trigger | Scans all `stages/*/output/` folders; renders an ASCII pipeline diagram with COMPLETE/PENDING per stage (files other than `.gitkeep` = COMPLETE) | Validate status renders per current ICM convention (CCA Mermaid does not substitute where upstream specifies ASCII) |
| Placeholder syntax | `{{SCREAMING_SNAKE_CASE}}`; may appear in any markdown file except `CLAUDE.md`, top-level `CONTEXT.md`, and `questionnaire.md` itself | Lint placeholder coverage; flag placeholders in the negative list as invalid |
| Conditional placeholders | `{{?SECTION}}...{{/SECTION}}` blocks may only wrap whole sections (a heading and its content), never inline content | Validate conditional blocks wrap complete sections only |
| Guardrail line limits | `CONTEXT.md` under 80 lines; reference files under 200 lines | Enforce in native ICM lint |
| Guardrail formatting | Plain English; **no em dashes** in the repository (replace with `--`) | Enforce in native ICM lint and in CCA-generated workspace artifacts |
| Persistent empty folders | Contain `.gitkeep` | Validate presence |
| Naming | `lowercase-with-hyphens`; zero-padded stage prefixes `01-`, `02-`; output artifacts `[topic-slug]-[artifact-type].md` | Match CCA SPEC §7.1 |
| Questionnaire design | Flat, all-at-once, system-level, derive-don't-ask, sensible defaults/examples, ask-once | Validate flow matches; encourage examples over adjective-only descriptions |
| Layered loading target | Streaming (not monolithic): full stage context ~2,000-8,000 tokens | Keep routing small; route before loading |

## Upstream-change rule

When an upstream convention changes:

1. Verify the current primary source.
2. Identify whether CCA mirrors, aliases, or merely interoperates with the changed behavior.
3. Prefer changing CCA over freezing an obsolete fork.
4. Keep compatibility additions optional unless the upstream itself makes them mandatory.
5. Update the spec, affected skills/templates, examples, migration guidance, and this matrix in the same change.
6. Re-run the relevant upstream-profile acceptance checks before claiming compatibility.

When an adjacent methodology changes materially, update the explanatory composition guidance as needed without silently promoting it into a structural compatibility profile.

## Compatibility vocabulary

CCA uses these terms deliberately:

- **Native-compatible**: an upstream workspace can be consumed without structural migration and, where CCA generates or materially rewrites that profile, the applicable upstream acceptance surface passes.
- **ICM-derived**: a non-ICM workspace intentionally borrows selected ICM patterns without claiming the full native ICM profile.
- **CCA-hardened**: optional CCA conventions were added for stronger portability, routing, provenance, or maintenance.
- **CCA-conformant**: the workspace intentionally adopts the CCA specification.
- **Method overlay**: a human organization/knowledge-work method such as PARA, Zettelkasten, or BASB that CCA preserves/composes without treating it as a native structural compatibility profile.

Native compatibility does **not** imply that an ICM workspace or LLM Wiki is itself a CCA workspace, and CCA conformance must never be retroactively imposed on upstream projects.
