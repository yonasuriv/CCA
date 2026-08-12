# Compatibility: ICM ↔ LLM Wiki ↔ CCA

Normative companion to `SPEC.md`. This document defines compatibility boundaries. CCA must preserve upstream validity before applying CCA-specific hardening.

## 1. Compatibility principle

CCA distinguishes three states:

- **Native-compatible** — CCA can consume the workspace without structural migration.
- **CCA-hardened** — optional CCA routing, portability, provenance, or maintenance conventions were added.
- **CCA-conformant** — the workspace intentionally adopts the CCA specification.

An ICM workspace or LLM Wiki does not become "CCA" merely because CCA can understand it. Compatibility is an acceptance guarantee, not retroactive ownership of upstream semantics.

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

CCA claims ICM compatibility only when it preserves the current ICM conventions it uses:

1. Five-layer routing architecture.
2. `CLAUDE.md` as ICM's native Layer 0 entry point.
3. Root and stage `CONTEXT.md` routing.
4. Stage contracts with the canonical sections `Inputs`, `Process`, `Outputs`.
5. ICM's canonical Inputs table shape: `Source | File/Location | Section/Scope | Why`.
6. Zero-padded, lowercase, hyphenated stage folders such as `01-collect`.
7. One-way cross-references.
8. Selective section routing.
9. One fact, one canonical home.
10. Human-editable handoffs through each stage's `output/` folder.

CCA extensions must be ignorable by an ICM-only consumer.

### Portable `AGENTS.md` with ICM

Adding `AGENTS.md` is optional hardening. Do not delete or invalidate a native `CLAUDE.md` merely to satisfy CCA.

Where both exist:

- Keep substantive guidance canonical in one place.
- Use tool-supported include/import behavior where available.
- Otherwise keep the secondary file as a minimal pointer that does not fork rules.
- Never claim CCA can override a harness's own instruction-discovery precedence.

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

CCA tooling must be able to inspect and operate on a native ICM workspace without first renaming stages, rewriting contracts, or replacing `CLAUDE.md`.

Optional hardening may add portable `AGENTS.md` guidance or knowledge capabilities, but the ICM workflow remains valid.

### LLM Wiki → CCA tooling

CCA tooling must accept a legitimate LLM Wiki implementation without requiring CCA's preferred page taxonomy or metadata. It should discover the implementation's own schema/instructions first.

Optional hardening may add portable routing, provenance metadata, indexes, or lifecycle conventions if the user wants them.

### CCA → ICM consumer

The pipeline subset of a CCA-conformant workspace must preserve ICM stage naming, contracts, routing semantics, one-way references, and handoffs so an ICM consumer can ignore CCA-only additions.

### CCA → LLM Wiki practice

A CCA knowledge bundle must preserve the LLM Wiki core idea: persistent, agent-maintained synthesis over durable source material. CCA-specific metadata and maintenance structure must remain implementation choices, not reinterpretations of the upstream pattern.

## 8. Upstream drift

CCA does not freeze upstream behavior. When ICM, LLM Wiki, AGENTS.md, or Agent Skills evolves, verify the primary source and update CCA toward it unless doing so would contradict CCA's core principle of filesystem-native, portable, inspectable context.

See `docs/standards.md` for the tracked upstream surface.
