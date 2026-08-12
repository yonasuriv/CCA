# Compatibility: ICM ↔ LLM Wiki ↔ CCA

Normative companion to `SPEC.md`. This document defines compatibility boundaries. CCA must preserve upstream validity before applying CCA-specific hardening.

## 1. Compatibility principle

CCA distinguishes three states:

- **Native-compatible** — CCA can consume the workspace without structural migration and, when CCA generates or materially rewrites that native profile, the applicable upstream acceptance surface passes.
- **CCA-hardened** — optional CCA routing, portability, provenance, or maintenance conventions were added.
- **CCA-conformant** — the workspace intentionally adopts the CCA specification.

An ICM workspace or LLM Wiki does not become "CCA" merely because CCA can understand it. Compatibility is an acceptance guarantee, not retroactive ownership of upstream semantics.

CCA also distinguishes a **native upstream profile** from **derived use of upstream patterns**. Borrowing part of a convention does not justify claiming full compatibility with that upstream.

## 2. Concept mapping

| CCA concept | ICM equivalent | LLM Wiki analogue |
|---|---|---|
| Portable root guidance (`AGENTS.md`) | Native Layer 0 is `CLAUDE.md` | Schema/instruction file may be chosen by the implementation |
| Routing (`CONTEXT.md`) | Layer 1 `CONTEXT.md` | Index/schema-defined navigation |
| Stage contract | Stage `CONTEXT.md` with Inputs / Process / Outputs | Ingest/query/lint procedures defined by the implementation |
| Factory/reference context | Layer 3 reference material | Stable schema/conventions |
| Working input/product | Layer 4 working artifacts | Query/ingest working material |
| Raw evidence | User-provided source material | Raw/source material |
| Maintained synthesis | No direct ICM equivalent | Core LLM Wiki behavior |
| Chronicle/log | Git/history may provide this | Optional implementation detail unless adopted by the wiki |

The overlap is semantic, not an excuse to force identical directory trees.

## 3. ICM compatibility profile

### Native ICM

CCA claims **native ICM compatibility** only when the workspace satisfies the complete applicable current ICM profile. CCA treats upstream `_core/CONVENTIONS.md` as the canonical semantic authority and the workspace-builder validation stage as the practical acceptance checklist for generated ICM workspaces.

Native ICM validation includes, where applicable:

1. five-layer routing and native Layer 0 `CLAUDE.md`;
2. root and per-stage `CONTEXT.md` routing;
3. exact `Inputs` / `Process` / `Outputs` stage contracts and canonical Inputs columns;
4. current ICM naming conventions, including zero-padded lowercase-hyphenated stages;
5. per-stage `output/` handoffs and an unbroken handoff chain;
6. cross-reference integrity and an acyclic one-way dependency graph;
7. selective section routing and one canonical home per substantive rule;
8. `CONTEXT.md` purity;
9. current `setup` and `status` trigger behavior;
10. a flat, all-at-once, system-level questionnaire with complete placeholder coverage where setup placeholders are used;
11. valid conditional placeholder syntax where used;
12. tool prerequisite/setup/verification guidance where required;
13. bundled-skill behavior where the optional ICM pattern is used;
14. spec stages that define WHAT/WHEN rather than implementation HOW where applicable;
15. checkpoints for applicable creative stages;
16. audits for applicable creative/build stages;
17. value validation for applicable content-producing stages;
18. docs-over-outputs discipline;
19. shared constants in applicable code-producing workspaces;
20. current ICM quality guardrails, including routing/reference size and formatting/readability rules;
21. workspace-builder-equivalent end-to-end validation before a generated workspace is described as ready.

CCA extensions must be ignorable by an ICM-only consumer. If current upstream ICM changes this acceptance surface, CCA must converge toward the current upstream rather than treat this list as frozen authority.

### ICM-derived patterns

A non-ICM workspace may intentionally borrow ICM constructs such as:

- numbered stage folders;
- stage `CONTEXT.md` contracts;
- selective Inputs routing;
- one-way dependencies;
- per-stage output handoffs.

That is **ICM-derived**, not native ICM compatibility, unless the rest of the applicable ICM profile also passes.

### Portable `AGENTS.md` with ICM

Adding `AGENTS.md` is optional hardening. Do not delete or invalidate a native `CLAUDE.md` merely to satisfy CCA.

Where both exist:

- Keep substantive guidance canonical in one place.
- Use tool-supported include/import behavior where available.
- Otherwise keep the secondary file as a minimal pointer that does not fork rules.
- Never claim CCA can override a harness's own instruction-discovery precedence.

Where native ICM specifies a concrete trigger output or representation, CCA preferences such as Mermaid do not replace that upstream-required form.

## 4. LLM Wiki compatibility profile

Karpathy's LLM Wiki is intentionally an idea pattern: the agent and user build the specifics together. Therefore CCA native compatibility must preserve that flexibility.

Core compatibility checks should focus on behavior rather than one folder schema:

- There is durable source material/evidence.
- There is maintained synthesis that compounds across sessions rather than being rebuilt from scratch for every query.
- The agent has explicit maintenance behavior for incorporating new material and keeping the synthesis useful.
- The human can inspect and edit the knowledge base directly.

CCA may recommend, but must not attribute to LLM Wiki as mandatory:

- a specific `raw/` / `wiki/` directory taxonomy;
- `wiki/index.md` as a required path;
- `log.md` or a specific log syntax;
- YAML frontmatter fields;
- entity/concept/source/synthesis subdirectories;
- CCA conformance levels.

Those are CCA hardening conventions when a workspace chooses them.

## 5. AGENTS.md compatibility profile

CCA uses `AGENTS.md` because it is an existing open convention.

- Root `AGENTS.md` may provide portable repository guidance.
- Nested `AGENTS.md` files are valid and useful; the closest applicable file takes precedence for that subtree under the AGENTS.md convention.
- CCA must not flatten nested instructions into one global catalog when doing so would destroy scope.
- `AGENTS.md` has no required heading schema; CCA templates are recommendations, not requirements of the standard.

## 6. Agent Skills compatibility profile

Every bundled skill must remain a valid standalone Agent Skills package:

- `SKILL.md` contains valid YAML frontmatter with `name` and `description`.
- Name uses lowercase letters/numbers/hyphens and remains within the current spec limits.
- Description says what the skill does and when to use it.
- Detailed material is progressively disclosed through skill-local `references/`, `assets/`, or `scripts/`.
- File references are relative to the skill root.
- A skill must not require a sibling skill or repository-global file merely to execute its core behavior.

Cross-skill suggestions are allowed, but they must be optional: if the sibling skill is absent, the active skill still works or explains the missing optional capability.

## 7. Swap guarantees

### ICM → CCA tooling

CCA tooling must be able to inspect and operate on a native ICM workspace without first renaming stages, rewriting contracts, replacing `CLAUDE.md`, or forcing CCA-only metadata.

Optional hardening may add portable `AGENTS.md` guidance or knowledge capabilities, but the ICM workflow remains valid.

### LLM Wiki → CCA tooling

CCA tooling must accept a legitimate LLM Wiki implementation without requiring CCA's preferred page taxonomy or metadata. It should discover the implementation's own schema/instructions first.

Optional hardening may add portable routing, provenance metadata, indexes, or lifecycle conventions if the user wants them.

### CCA → ICM consumer

If a CCA-conformant workspace claims a **native ICM profile**, that profile must preserve the full applicable current ICM acceptance surface so an ICM consumer can operate it without depending on CCA-only semantics.

If a CCA workspace only borrows ICM stage-contract patterns, it must describe that part as **ICM-derived** rather than promise native ICM interchangeability.

### CCA → LLM Wiki practice

A CCA knowledge bundle must preserve the LLM Wiki core idea: persistent, agent-maintained synthesis over durable source material. CCA-specific metadata and maintenance structure must remain implementation choices, not reinterpretations of the upstream pattern.

## 8. Validation precedence

Validation order is:

1. detect the actual native/upstream profile;
2. validate that profile against its current upstream rules;
3. validate any intentionally adopted CCA conformance;
4. run the CCA fresh-agent walk test as a supplemental portability check;
5. report optional hardening separately.

CCA must not use a successful walk test to waive a failed upstream acceptance check.

## 9. Upstream drift

CCA does not freeze upstream behavior. When ICM, LLM Wiki, AGENTS.md, or Agent Skills evolves, verify the primary source and update CCA toward it unless doing so would contradict CCA's core principle of filesystem-native, portable, inspectable context.

See `docs/standards.md` for the tracked upstream surface.
