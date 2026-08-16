# CCA Specification

**Version 0.1.0** — Status: Draft, tracking ICM, LLM Wiki, AGENTS.md, and Agent Skills upstream.

Normative. CCA runtime behavior and CCA-conformant examples must conform to this document. Method composition is additionally governed by [`method-composition.md`](method-composition.md).

The key words **must**, **should**, and **may** are to be interpreted as in RFC 2119.

## 1. What CCA is

CCA (Convergent Context Architecture) is an interoperability and evolution layer for filesystem-native agent context. It defines shared semantics that let agents navigate plain-file workspaces without requiring a proprietary runtime, database, or model vendor.

CCA builds on:

- **ICM / Model Workspace Protocol** for layered routing, stage contracts, selective context loading, canonical sources, one-way dependencies, and file-based human review.
- **LLM Wiki** for persistent LLM-maintained synthesis that compounds across sessions instead of re-deriving knowledge from raw documents on every query.
- **AGENTS.md** for portable agent guidance.
- **Agent Skills (`SKILL.md`)** for portable, progressively disclosed capabilities.

CCA can also compose with human knowledge-work methodologies such as PARA, Zettelkasten, and Building a Second Brain without promoting them to structural compatibility profiles.

CCA does not replace those upstreams or methods. Where an upstream already defines a useful shape, CCA should preserve it rather than minting a competing convention.

## 2. Core principle

**Convergence over invention.**

CCA may add optional semantics where upstreams leave implementation open, but it must not:

1. redefine an upstream convention and still call the result identical;
2. make a CCA-specific choice appear mandatory for ICM or LLM Wiki compatibility;
3. require a proprietary runtime to understand the workspace;
4. duplicate canonical rules across adapters or catalogs;
5. force a pipeline, wiki, database, agent framework, or organizational taxonomy where the work does not need one.

## 3. Compatibility states

CCA distinguishes:

- **Native-compatible**: CCA tooling can consume the upstream workspace without structural migration.
- **CCA-hardened**: optional CCA routing, portability, provenance, or maintenance conventions were added.
- **CCA-conformant**: the workspace intentionally adopts the CCA specification.

Compatibility is an acceptance guarantee, not a claim that every upstream workspace is itself a CCA workspace.

CCA also distinguishes a **native upstream profile** from **derived use of upstream patterns**. Borrowing an upstream construct does not by itself justify claiming full compatibility with that upstream.

PARA, Zettelkasten, BASB/CODE, and similar human methods are **method overlays**, not additional compatibility states.

## 4. Workspace model

A workspace is a folder containing durable files that an agent and human can inspect and edit. Markdown is preferred for prose; JSON/YAML may be used for structured data.

CCA requires no database, server, vector store, or binary state. Such infrastructure may be added when useful, but the durable operating context should remain understandable from files.

A workspace may be:

- an ICM-style pipeline;
- an LLM Wiki-style knowledge base;
- an ordinary coding repository with portable agent guidance;
- a hybrid of those forms;
- a second brain or PKM system using method overlays such as PARA or Zettelkasten;
- another filesystem-native form whose boundaries improve routing and maintenance.

### 4.1 Boundary composition

CCA composes heterogeneous methods and profiles by preserving boundaries rather than forcing one universal tree.

- An outer organizational method may determine where a nested workspace lives.
- A nested native ICM root remains governed by the complete applicable ICM profile.
- A nested LLM Wiki remains governed by its own schema and maintenance instructions.
- Human-authored knowledge such as Zettelkasten notes must not be assumed agent-writable without local authority.
- Ordinary filesystem semantics should be inferred when safe rather than serialized into a giant CCA manifest that merely restates paths.

See [`method-composition.md`](method-composition.md).

## 5. Layered context routing

For pipeline-oriented work, CCA adopts ICM's five-layer architecture when the ICM profile is active:

| Layer | Typical file(s) | Question |
|---|---|---|
| 0 | native harness entry plus portable guidance (`AGENTS.md` in CCA-hardened workspaces; native `CLAUDE.md` remains authoritative where ICM/harness semantics require it) | Where am I? |
| 1 | root `CONTEXT.md` (recommended default) | Where do I go? |
| 2 | stage `CONTEXT.md` (contract per stage) | What do I do? |
| 3 | references, configuration, skills | What rules apply? |
| 4 | working artifacts, previous outputs, user-provided inputs | What am I working with? |

Agents read down the layers and stop when they have enough context for the current task.

The root `CONTEXT.md` is a recommended default for the workspace's context/router file, not an enforced requirement. A CCA-created or CCA-hardened workspace may use a different name for its context/router file when the project's naming makes sense that way. When it does:

- the alternative name must be declared in the Layer-0 catalog (`AGENTS.md`) with a single pointer line so agents and humans can resolve it without guessing;
- the file must keep the same mechanics as root `CONTEXT.md` (the same preferred token and line allowances and routing behavior ICM assigns to that layer), treated as recommendations, not requirements.

Stage `CONTEXT.md` is a per-stage contract that describes that stage's Inputs/Process/Outputs; it is not a routing default and is not interchangeable under this rule.

A workspace may use analogous routing for non-pipeline forms, but it must not force LLM Wiki, PARA, Zettelkasten, BASB, or ordinary repositories into ICM layers merely for cosmetic consistency.

## 6. Portable root guidance

CCA prefers `AGENTS.md` for portable cross-agent repository guidance because it is an existing ecosystem convention.

Rules:

1. `AGENTS.md` should orient and route rather than become a knowledge dump.
2. Nested `AGENTS.md` files are valid and should preserve subtree scope; the closest applicable file wins under the AGENTS.md convention.
3. `AGENTS.md` has no required heading schema. CCA templates are recommendations only.
4. Tool-specific instruction files may coexist when required by a harness.
5. CCA must not claim it can override a harness's native instruction precedence.
6. Contradictory copies of the same rule across root/adapter files are forbidden by the one-fact-one-home principle.
7. In CCA-created or CCA-hardened workspaces that do not already have a stricter native profile, `AGENTS.md` is the preferred canonical portable guidance surface. A harness-native entry may bridge to that guidance using the harness's current supported mechanism. In a native upstream profile such as ICM, preserve the upstream's own entry semantics first; portable guidance is an interoperable counterpart, not a declaration that it overrides the native entry.

When CCA operates on an existing **native ICM** workspace that already has a `CLAUDE.md`, it must not replace or break the native entry merely to make `AGENTS.md` look canonical; preserve it and, when portability is wanted, derive the `AGENTS.md` counterpart so both files interoperate under the open AGENTS.md convention.

## 7. ICM pipeline profile

CCA recognizes two different uses of ICM concepts:

- **Native ICM compatibility**: the workspace claims to be an ICM/MWP workspace and must satisfy the complete applicable current upstream ICM profile.
- **ICM-derived patterns**: another workspace borrows constructs such as numbered stages, stage contracts, selective routing, or output handoffs without claiming the complete ICM profile.

CCA must not call a partial ICM-derived scaffold “native ICM-compatible.”

### 7.1 Stage naming

For native ICM and ICM-derived stages that intentionally preserve ICM syntax, use lowercase, hyphenated, zero-padded stage folders:

```text
stages/
├── 01-collect/
├── 02-synthesize/
└── 03-publish/
```

Do not introduce underscore variants such as `01_collect` while claiming to preserve the current ICM naming convention.

### 7.2 Stage contracts

Every native ICM stage `CONTEXT.md` uses the canonical sections:

```markdown
## Inputs

| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Previous stage | `../01-collect/output/notes.md` | Full file | Source material |
| Voice guide | `../../_config/voice.md` | "Tone" | Style constraints |

## Process

1. Read only the listed inputs.
2. Perform the stage's single job.
3. Run any checkpoint or audit required by this stage.

## Outputs

| Artifact | Location | Format |
|---|---|---|
| Brief | `output/example-brief.md` | Markdown |
```

CCA must not add required columns to the ICM Inputs table while claiming the shape is exact. Additional semantics such as CCA file roles may be documented elsewhere or treated as optional metadata.

Layer-3 folder names (for example `_config/`, `references/`, `shared/`, `brand-vault/`, or `design-system/`) are workspace-native; upstream ICM does not mandate one name. CCA examples and templates typically use `_config/` as a default, but an existing workspace's own Layer-3 homes are authoritative and must be preserved. CCA must not require renaming them to `_config/` for compatibility.

### 7.3 Core pipeline invariants

- One stage, one job.
- One-way cross-references; downstream stages may depend on upstream stages, not vice versa.
- Inputs tables scope files and, when useful, exact sections.
- Each stage writes to its own `output/` folder.
- Human edits to output files are valid handoffs; the next stage consumes the edited file.
- Stable rules live in references/configuration, not copied into stage routers.
- Previous outputs are artifacts, not canonical templates for future quality rules.
- Shared configurable code values should have one canonical source where applicable.

These invariants are useful outside a native ICM workspace, but using them alone does not establish native ICM compatibility.

### 7.4 Full native ICM acceptance

When CCA creates, modifies, or validates a workspace that **claims native ICM compatibility**, it must validate the complete applicable current upstream ICM convention surface. The canonical semantic authority is upstream ICM `_core/CONVENTIONS.md`; the workspace-builder's validation stage is the practical acceptance checklist for generated workspaces. CCA's own walk test is supplemental and must not replace these upstream checks.

At minimum, native ICM validation must cover the applicable current upstream requirements for:

1. five-layer routing with the current native ICM Layer-0 entry semantics preserved; when portable `AGENTS.md` guidance is added, it interoperates with rather than replaces or overrides the native `CLAUDE.md` entry path;
2. one root `CONTEXT.md` and one stage `CONTEXT.md` per stage;
3. exact stage contract shape and canonical Inputs columns;
4. lowercase-with-hyphens naming, zero-padded stages, output naming, and `.gitkeep` for intentionally empty persistent folders;
5. unbroken stage handoffs through per-stage `output/` folders;
6. cross-reference integrity and an acyclic, one-way dependency graph;
7. selective section routing and canonical-source discipline;
8. `CONTEXT.md` purity: routing/process contract, not embedded reference material;
9. `setup` and `status` trigger behavior as currently defined by ICM;
10. a flat, all-at-once, system-level setup questionnaire that derives inferable fields and uses sensible defaults/examples;
11. complete placeholder coverage and valid conditional placeholder blocks where those mechanisms are used;
12. tool prerequisite/setup/verification guidance when external system tools are required;
13. bundled skills behavior when the workspace uses that optional ICM pattern;
14. specification stages that define WHAT/WHEN rather than implementation HOW when applicable;
15. checkpoints in applicable creative stages;
16. audits in applicable creative/build stages;
17. value validation in applicable content-producing stages;
18. docs-over-outputs discipline;
19. shared constants in applicable code-producing workspaces;
20. current ICM quality guardrails for routing/reference size, readable language, formatting, and persistent empty folders;
21. an end-to-end workspace-builder-equivalent validation before a generated workspace is described as ready or fully native-compatible.

Where current ICM requires a specific representation or trigger output, CCA presentation preferences such as Mermaid do not override that upstream requirement.

If upstream ICM changes these requirements, CCA must converge toward the current upstream rather than freeze this list as a divergent fork.

## 8. Knowledge profile

CCA adopts the LLM Wiki core idea: durable source material plus LLM-maintained synthesis that compounds over time.

Native LLM Wiki compatibility is behavioral, not tied to one directory tree. A compatible implementation should provide:

1. durable source material or evidence;
2. maintained synthesis that persists across sessions;
3. explicit maintenance behavior for integrating new material and querying existing knowledge;
4. a human-editable filesystem representation.

### 8.1 Optional CCA hardened knowledge bundle

CCA may recommend the following implementation when a user wants stronger interoperability and maintenance:

```text
inbox/            optional staging before deposit
raw/              durable source material (write-once)
notes/            optional human-owned thinking (not raw, not wiki)
wiki/             maintained synthesis
wiki/index.md     navigation catalog
log.md            maintenance chronicle
```

Optional hardening may also include YAML frontmatter, lifecycle states, provenance fields, contradiction sections, entity/concept taxonomies, machine-parseable log prefixes, a source index with supersession rows, and a checkable integrity mechanism (hash manifest and/or verify script).

These are **CCA conventions**, not universal requirements of Karpathy's LLM Wiki idea.

When scaffolding an empty hardened bundle, CCA should seed at least one real source and one citing wiki page so operators can pattern-match the maintenance loop.

### 8.2 Knowledge invariants

When adopted by a workspace:

- source material should not be silently rewritten by synthesis operations;
- corrections to evidence should **supersede** (add a new source and record the relationship) rather than mutate deposited raw files;
- derived claims should retain provenance when the workspace promises evidence traceability;
- contradictions should be represented rather than silently overwritten;
- stale or superseded knowledge should remain inspectable when history matters;
- indexes should route rather than duplicate full page content;
- human-authored notes, when present as a separate layer, must not be treated as silently agent-rewritable wiki pages.

## 9. File roles

CCA uses file roles as an internal reasoning model. They are classifications by function, not mandatory directories.

| Role | Function |
|---|---|
| **catalog** | routes to other context; stores little substantive content |
| **contract** | defines one unit of work: inputs, process, outputs |
| **factory** | stable constraints, conventions, references, reusable skill material |
| **source** | durable evidence/input that synthesis should not silently mutate |
| **synthesis** | maintained derived knowledge |
| **product** | per-run or per-stage working artifact |
| **chronicle** | historical record |
| **dead** | unowned/unreferenced material that requires review |

A file has one primary role for maintenance purposes, but this classification must not force upstream workspaces to move files solely to match CCA labels.

## 10. Canonical sources and adapters

**One fact, one home.** If the same substantive rule appears in multiple files as authoritative text, CCA considers that drift risk.

Adapters should point to canonical guidance rather than copy it. Prefer native include/import mechanisms when a tool supports them.

A tool-specific file may contain minimal bootstrapping required by that tool, but must not become a divergent second specification of the workspace.

## 11. Agent Skills profile

Every bundled skill must satisfy the current Agent Skills specification.

Requirements:

- one skill directory with a valid `SKILL.md`;
- valid `name` and `description` frontmatter;
- name uses lowercase letters, numbers, and hyphens and stays within the current standard limits;
- description states what the skill does and when it should trigger;
- `SKILL.md` remains compact enough for activation-time loading;
- detailed material lives in skill-local `references/`, `assets/`, or `scripts/` and is loaded only when required;
- implementation files referenced by path remain inside that skill package;
- sibling filesystem paths and repository-global implementation paths are not part of a skill's execution contract.

CCA is distributed as **one installable `cca` skill with seven lazily loaded modes**. Six modes are portable workspace operations (`architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`); `advise` is a separate judgment capability inside the same package. Runtime references, templates, and scripts required by those modes must remain skill-local so installation is self-contained. Architect and advisor reference domains remain separate even though they share one package.

## 12. Operations

CCA defines six portable workspace operations plus one advisory mode:

| Operation | Purpose |
|---|---|
| `architect` | design a new filesystem-native workspace or restructure an existing one with an explicit migration gate; coordinate compound method/profile composition |
| `scaffold` | add the smallest useful routing/context layer without restructuring existing content |
| `sync` | reconcile routing/catalog files with disk without inventing content |
| `ingest` | integrate new evidence into maintained synthesis |
| `query` | navigate maintained synthesis, verify against evidence when needed, and preserve durable new knowledge when useful |
| `lint` | validate the workspace using the correct compatibility/conformance profile |
| `advise` | apply engineering/process/security/autonomy/context/model judgment without turning priors into enforcement |

## 13. Profile-aware linting

Linting must distinguish upstream validity from optional CCA hardening and method overlays.

At minimum, `lint` mode supports:

- **ICM native compatibility** — validate the complete applicable current ICM profile and workspace-builder-equivalent acceptance surface.
- **ICM-derived patterns** — validate borrowed ICM constructs without falsely promoting the host repository to native ICM compatibility.
- **LLM Wiki native compatibility** — validate the core maintained-wiki behavior without imposing one CCA filesystem schema.
- **CCA conformance** — validate whichever additional CCA conventions the workspace explicitly adopted.

PARA, Zettelkasten, BASB/CODE, and similar overlays must not be invented as native lint profiles. Locally declared preservation constraints may be checked as workspace rules.

A missing CCA optional convention may be reported as a hardening opportunity, but not as an upstream compatibility failure.

## 14. CCA walk test

For intentionally structured CCA workspaces, the CCA portability walk test is:

> A fresh agent with no prior chat memory can orient, perform a representative operation, and report status using the workspace files alone.

- **Orient**: identify what the workspace is, which profile/method boundary is active, and where relevant context lives.
- **Act**: perform one representative operation using only routed files and available tools.
- **Report**: state what changed, what was produced, what remains, and what is missing or ambiguous.

If a required decision exists only in chat history or someone's memory, the durable workspace is incomplete.

This walk test is **not** a substitute for profile-specific acceptance. A native ICM claim must also pass the full applicable ICM validation surface; another upstream profile remains governed by its own current rules.

## 15. Size and context discipline

CCA inherits ICM's preference for small routing files and selective loading.

Guidelines, not universal laws outside a profile that makes them normative:

- root routing/instruction files should remain compact;
- native ICM stage `CONTEXT.md` and reference files must respect current ICM guardrails;
- large reference documents should be split or selectively routed when only sections are needed;
- available context is not automatically useful context;
- fix under-specified routing before solving context bloat by simply loading more files.

## 16. Out of scope

CCA is not:

- an agent runtime;
- a real-time multi-agent messaging layer;
- a replacement for MCP;
- a vector database or retrieval engine;
- a workflow scheduler;
- a replacement for PARA, Zettelkasten, BASB, ICM, LLM Wiki, AGENTS.md, or Agent Skills;
- a requirement to use Markdown for every artifact;
- a claim that all filesystem layouts should look identical.

Real-time multi-agent collaboration, where agents need to communicate dynamically in tight loops, requires message-passing/orchestration infrastructure. CCA can provide durable shared context beneath such systems, but does not replace them.

## 17. Upstream evolution

CCA tracks its upstreams. When ICM, LLM Wiki, AGENTS.md, Agent Skills, or a directly relevant adjacent standard changes, CCA should verify the primary source and adapt toward it.

Method-overlay guidance should likewise be updated when the methods it describes materially change, without silently promoting them to structural compatibility profiles.

Repository maintainers should track the current primary upstream compatibility surfaces and update this skill-local specification, compatibility reference, affected modes, templates, examples, and regression checks together. The installed skill must not depend on repository-only documentation to execute correctly.
