# CCA Specification

**Version 0.1.0** — Status: Draft, tracking ICM, LLM Wiki, AGENTS.md, and Agent Skills upstream.

Normative. Skills and examples in this repository must conform to this document.

The key words **must**, **should**, and **may** are to be interpreted as in RFC 2119.

## 1. What CCA is

CCA (Convergent Context Architecture) is an interoperability and evolution layer for filesystem-native agent context. It defines shared semantics that let agents navigate plain-file workspaces without requiring a proprietary runtime, database, or model vendor.

CCA builds on:

- **ICM / Model Workspace Protocol** for layered routing, stage contracts, selective context loading, canonical sources, one-way dependencies, and file-based human review.
- **LLM Wiki** for persistent LLM-maintained synthesis that compounds across sessions instead of re-deriving knowledge from raw documents on every query.
- **AGENTS.md** for portable agent guidance.
- **Agent Skills (`SKILL.md`)** for portable, progressively disclosed capabilities.

CCA does not replace those upstreams. Where an upstream already defines a useful shape, CCA should preserve it rather than minting a competing convention.

## 2. Core principle

**Convergence over invention.**

CCA may add optional semantics where upstreams leave implementation open, but it must not:

1. redefine an upstream convention and still call the result identical;
2. make a CCA-specific choice appear mandatory for ICM or LLM Wiki compatibility;
3. require a proprietary runtime to understand the workspace;
4. duplicate canonical rules across adapters or catalogs;
5. force a pipeline, wiki, database, or agent framework where the work does not need one.

## 3. Compatibility states

CCA distinguishes:

- **Native-compatible**: CCA tooling can consume the upstream workspace without structural migration.
- **CCA-hardened**: optional CCA routing, portability, provenance, or maintenance conventions were added.
- **CCA-conformant**: the workspace intentionally adopts the CCA specification.

Compatibility is an acceptance guarantee, not a claim that every upstream workspace is itself a CCA workspace.

## 4. Workspace model

A workspace is a folder containing durable files that an agent and human can inspect and edit. Markdown is preferred for prose; JSON/YAML may be used for structured data.

CCA requires no database, server, vector store, or binary state. Such infrastructure may be added when useful, but the durable operating context should remain understandable from files.

A workspace may be:

- an ICM-style pipeline;
- an LLM Wiki-style knowledge base;
- an ordinary coding repository with portable agent guidance;
- a hybrid of those forms;
- another filesystem-native form whose boundaries improve routing and maintenance.

## 5. Layered context routing

For pipeline-oriented work, CCA adopts ICM's five-layer architecture:

| Layer | Typical file(s) | Question |
|---|---|---|
| 0 | `CLAUDE.md` in native ICM; portable `AGENTS.md` may coexist | Where am I? |
| 1 | root `CONTEXT.md` | Where do I go? |
| 2 | stage `CONTEXT.md` | What do I do? |
| 3 | references, configuration, skills | What rules apply? |
| 4 | working artifacts, previous outputs, user-provided inputs | What am I working with? |

Agents read down the layers and stop when they have enough context for the current task.

CCA may use analogous routing for non-pipeline forms, but it must not force LLM Wiki or ordinary repositories into ICM layers merely for cosmetic consistency.

## 6. Portable root guidance

CCA prefers `AGENTS.md` for portable cross-agent repository guidance because it is an existing ecosystem convention.

Rules:

1. `AGENTS.md` should orient and route rather than become a knowledge dump.
2. Nested `AGENTS.md` files are valid and should preserve subtree scope; the closest applicable file wins under the AGENTS.md convention.
3. `AGENTS.md` has no required heading schema. CCA templates are recommendations only.
4. Tool-specific instruction files may coexist when required by a harness.
5. CCA must not claim it can override a harness's native instruction precedence.
6. Contradictory copies of the same rule across root/adaptor files are forbidden by the one-fact-one-home principle.

## 7. ICM pipeline profile

A CCA-conformant pipeline that claims ICM compatibility must preserve current ICM conventions.

### 7.1 Stage naming

Use lowercase, hyphenated, zero-padded stage folders:

```text
stages/
├── 01-collect/
├── 02-synthesize/
└── 03-publish/
```

Do not introduce underscore variants such as `01_collect` in new ICM-compatible workspaces.

### 7.2 Stage contracts

Every stage `CONTEXT.md` uses the canonical three sections:

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

### 7.3 Pipeline invariants

- One stage, one job.
- One-way cross-references; downstream stages may depend on upstream stages, not vice versa.
- Inputs tables scope files and, when useful, exact sections.
- Each stage writes to its own `output/` folder.
- Human edits to output files are valid handoffs; the next stage consumes the edited file.
- Stable rules live in references/configuration, not copied into stage routers.
- Previous outputs are artifacts, not canonical templates for future quality rules.
- Shared configurable code values should have one canonical source where applicable.

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
raw/             durable source material
wiki/            maintained synthesis
wiki/index.md     navigation catalog
log.md            maintenance chronicle
```

Optional hardening may also include YAML frontmatter, lifecycle states, provenance fields, contradiction sections, entity/concept taxonomies, and machine-parseable log prefixes.

These are **CCA conventions**, not universal requirements of Karpathy's LLM Wiki idea.

### 8.2 Knowledge invariants

When adopted by a workspace:

- source material should not be silently rewritten by synthesis operations;
- derived claims should retain provenance when the workspace promises evidence traceability;
- contradictions should be represented rather than silently overwritten;
- stale or superseded knowledge should remain inspectable when history matters;
- indexes should route rather than duplicate full page content.

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
- paths referenced by a skill are relative to that skill root;
- core execution must not depend on a sibling skill or a repository-global file that will disappear when the skill is copied elsewhere.

A skill may recommend another skill for an optional follow-up, but absence of that sibling cannot make the active skill unusable.

## 12. Operations

CCA currently defines six portable operations:

| Operation | Purpose |
|---|---|
| `architect` | design a new filesystem-native workspace or restructure an existing one with an explicit migration gate |
| `scaffold` | add the smallest useful routing/context layer without restructuring existing content |
| `sync` | reconcile routing/catalog files with disk without inventing content |
| `ingest` | integrate new evidence into maintained synthesis |
| `query` | navigate maintained synthesis, verify against evidence when needed, and preserve durable new knowledge when useful |
| `lint` | validate the workspace using the correct compatibility/conformance profile |

## 13. Profile-aware linting

Linting must distinguish upstream validity from optional CCA hardening.

At minimum, `cca-lint` supports:

- **ICM native compatibility** — validate ICM layer/stage conventions without requiring CCA wiki metadata.
- **LLM Wiki native compatibility** — validate the core maintained-wiki behavior without imposing one CCA filesystem schema.
- **CCA conformance** — validate whichever additional CCA conventions the workspace explicitly adopted.

A missing CCA optional convention may be reported as a hardening opportunity, but not as an upstream compatibility failure.

## 14. Walk test

For intentionally structured CCA workspaces, the acceptance test is:

> A fresh agent with no prior chat memory can orient, perform a representative operation, and report status using the workspace files alone.

- **Orient**: identify what the workspace is and where relevant context lives.
- **Act**: perform one representative operation using only routed files and available tools.
- **Report**: state what changed, what was produced, what remains, and what is missing or ambiguous.

If a required decision exists only in chat history or someone's memory, the durable workspace is incomplete.

## 15. Size and context discipline

CCA inherits ICM's preference for small routing files and selective loading.

Guidelines, not universal laws:

- root routing/instruction files should remain compact;
- stage `CONTEXT.md` files should remain under ICM's practical size guardrails;
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
- a requirement to use Markdown for every artifact;
- a claim that all filesystem layouts should look identical.

Real-time multi-agent collaboration, where agents need to communicate dynamically in tight loops, requires message-passing/orchestration infrastructure. CCA can provide durable shared context beneath such systems, but does not replace them.

## 17. Upstream evolution

CCA tracks its upstreams. When ICM, LLM Wiki, AGENTS.md, Agent Skills, or a directly relevant adjacent standard changes, CCA should verify the primary source and adapt toward it.

See `docs/standards.md` for the tracked compatibility surface and update procedure.
