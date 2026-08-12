# CCA Specification

**Version 0.1.0** — Status: Draft, tracking ICM and LLM Wiki upstream.
Normative. Skills and examples in this repo must conform to this document.

The key words **must**, **should**, and **may** are to be interpreted as in
RFC 2119.

---

## 1. What CCA is

CCA (Convergent Context Architecture) is an interoperability and evolution layer
for filesystem-native agent context. It specifies how a folder of plain-text
files is organized so that any agent, reading the right files at the right
moment, can orient itself, perform work, and maintain knowledge — without
framework code, and without assuming a specific model or vendor.

CCA unifies:

- **ICM** (Interpretable Context Methodology): staged pipelines, layered
  context loading, stage contracts, human review gates.
- **LLM Wiki**: immutable raw sources, an LLM-maintained wiki synthesis, and
  schema-driven maintenance (ingest / query / lint).

CCA adopts ecosystem standards — `AGENTS.md` for root instructions, `SKILL.md`
for skill packages — and introduces no competing conventions.

## 2. The workspace

A **workspace** is a folder. It carries its own prompts, context structure,
knowledge, and stage definitions. It can be copied, zipped, committed to Git,
or handed to another person or agent with no environment setup.

All workspace state lives in plain-text files (Markdown by default, JSON/YAML
for structured data). There is no binary state, no database requirement, no
server. Workspaces **should** be Git-compatible by default.

## 3. The five layers

Agents read down the layers and stop when they have what the current task
needs. No agent reads everything.

| Layer | Canonical file(s) | Question it answers | Role | Budget |
|---|---|---|---|---|
| 0 | `AGENTS.md` | "Where am I?" | catalog | ~800 tokens |
| 1 | `CONTEXT.md`, `wiki/index.md` | "Where do I go?" | catalog | ~300 tokens |
| 2 | stage `CONTEXT.md` | "What do I do?" | contract | 200–500 tokens |
| 3 | `_config/`, `references/`, `raw/` | "What rules apply? What's the evidence?" | factory, source | 500–2,000 tokens (selective) |
| 4 | `output/`, `wiki/` | "What am I working with? What do we know?" | product, synthesis | varies |

- **Layers 0–2 are structural.** They route and instruct. They change rarely.
- **Layers 3–4 are content.** They are what the agent reads as material and
  writes as output.
- A rendering or routing task may need only Layers 0–2. A content task reads
  down to Layer 4. Total delivered context per task **should** stay in the
  2,000–8,000 token range.

### 3.1 Layer 3 vs Layer 4

Layer 3 material is **internalized as constraints**: write like this, follow
these conventions, cite this evidence. Layer 4 material is **processed as
input**: transform this research into a brief, update this page with this
source. Mixing the two in an undifferentiated context forces the model to sort
them on its own; the folder structure must sort them instead.

## 4. The eight file roles

Every file in a workspace plays exactly one primary role. Classification is by
function, not location.

| Role | Definition | Mutability | Canonical locations |
|---|---|---|---|
| **catalog** | Points at everything; stores almost nothing. Routing, not content. | Rarely changes | `AGENTS.md`, `CONTEXT.md`, `wiki/index.md` |
| **contract** | Defines one unit of work: inputs, process, outputs. | Changes on redesign | stage `CONTEXT.md` |
| **factory** | Stable rules and conventions, configured once. Internalize as constraints. | Stable across runs | `_config/`, `references/`, `skills/` |
| **source** | Immutable raw evidence. Read and cited, never modified by the agent. | Immutable | `raw/` |
| **synthesis** | Derived knowledge the agent owns, maintains, and keeps current. | Evolves with use | `wiki/` |
| **product** | Per-run working artifacts. Produced, reviewed, edited, handed off. | Changes every run | `output/` |
| **chronicle** | Append-only record of what happened and when. | Append-only | `log.md` |
| **dead** | Unreferenced and unowned. Not a role a file should keep. | Flagged by lint | anywhere |

Rules:

1. **One fact, one home.** Every piece of information has a canonical file;
   other files link to it. Duplicated rules drift.
2. **Catalogs point, they do not store.** A catalog that grows content is
   refactored: content moves to a factory or synthesis file, the catalog keeps
   a link.
3. **Sources are sacred.** The agent never edits `raw/`. Derived claims must
   be traceable back to sources (provenance).
4. **The agent owns the synthesis; the human owns direction.** Humans curate
   sources, review products, and steer. Agents do the bookkeeping.

## 5. Canonical filenames and authority order

Canonical names (use these in new workspaces):

```
AGENTS.md        Layer 0 root catalog          (ecosystem standard)
CONTEXT.md       Layer 1 routing / Layer 2 contract
index.md         wiki catalog                  (LLM Wiki convention)
log.md           chronicle                     (LLM Wiki convention)
raw/  wiki/  output/  _config/  references/  stages/  setup/  skills/
```

Legacy aliases, honored for compatibility (see `compatibility.md`):

```
CLAUDE.md        → alias for the Layer 0 root (ICM default)
IDENTITY.md      → alias for the Layer 0 root (icm-template)
GEMINI.md, .cursorrules, .windsurfrules, .github/copilot-instructions.md
                 → tool-specific adapters (thin pointers only)
schema.md        → alias for wiki schema content (folds into AGENTS.md or _config/)
```

**Authority order.** If several root files exist, precedence is:
`AGENTS.md` → `CLAUDE.md` → `IDENTITY.md` → `README.md`. Lower-precedence
files must not contradict higher ones; adapters contain only a pointer, never
a divergent copy of the rules. One fact, one home.

## 6. Stage contracts (pipelines)

Each stage in a pipeline is a numbered folder with a `CONTEXT.md` contract.
The numbering encodes execution order; the folder boundary enforces separation
of concerns.

A contract has three required parts:

```markdown
## Inputs
| Source | File/Location | Section/Scope | Role | Why |
|---|---|---|---|---|
| Previous stage | ../01_collect/output/notes.md | Full file | product | Source material |
| Voice guide | ../../_config/voice.md | "Tone" section | factory | Style constraints |

## Process
1. Read the inputs listed above.
2. …

## Outputs
| Artifact | Location | Format |
|---|---|---|
| Brief | output/[slug]-brief.md | Markdown with frontmatter |
```

- The **Inputs** table is the control point: it scopes exactly which files —
  and which sections — the agent loads. It makes context selection explicit,
  editable, and auditable. Without it the agent loads everything or guesses.
- Creative stages **should** add **Checkpoints** (pause points for human
  steering) and an **Audit** section (quality checks with unambiguous pass
  conditions, run before writing output).
- Contracts **must** stay under 80 lines. Reference files **should** stay
  under 200 lines.
- One stage, one job. A stage that collects does not also synthesize; a stage
  that drafts does not also publish.

**Handoffs.** A stage writes to its own `output/`; the next stage reads from
it. A human may edit any output between stages — every output is an edit
surface — and the next stage picks up whatever the human left.

## 7. Wiki conventions (knowledge)

A knowledge workspace (or the knowledge side of a hybrid) has three parts:

```
raw/        role: source     — immutable evidence. The agent reads, never writes.
wiki/       role: synthesis  — pages the agent owns: overview, entities,
                               concepts, syntheses, comparisons.
wiki/index.md  role: catalog — what exists now: every page, one-line summary.
log.md      role: chronicle  — what happened over time, append-only.
```

- `index.md` is content-oriented; the agent reads it first when navigating.
  It is updated on every ingest.
- `log.md` is chronological and append-only. Entries **must** start with a
  consistent prefix, e.g. `## [2026-08-12] ingest | Source Title`, so ordinary
  shell tools can parse history (`grep "^## \[" log.md | tail -5`).
- Wiki pages **should** carry YAML frontmatter (`type`, `status`, `created`,
  `updated`, `sources`, `tags`) so metadata stays machine-readable while prose
  stays human-readable.
- **Provenance is mandatory.** Every source-derived claim must link back to
  its source(s). A wiki without provenance is an accumulation of
  model-generated claims, not a knowledge layer.
- **Contradictions are preserved, not overwritten.** When new evidence
  conflicts with an existing claim, record both, with temporal context and
  confidence, and update the synthesis to reflect the conflict — do not
  silently replace.
- **Knowledge has a lifecycle.** Pages and relationships are created,
  validated, used, superseded, and archived. Mark superseded material via
  `status:` frontmatter (`active` / `superseded` / `archived`) rather than
  deleting it — history stays, authority stays clear, and the wiki never
  becomes an accumulating junk drawer.

## 8. Operations

Six operations cover the lifecycle. Each ships as a `SKILL.md` package under
`skills/` and works on any conformant workspace.

| Operation | Trigger | Summary |
|---|---|---|
| **architect** | "build me a workspace for X", "structure this folder for agents" | Design a new workspace (pick a form, scaffold the smallest skeleton) or restructure an existing folder (audit → classify → migrate → validate). |
| **scaffold** | "add CCA to this project" | Generate root catalog, routing, and `_config/` in place; optionally add stages or a wiki. Never disturbs existing files. |
| **sync** | "update the routing", "sync the catalogs" | Reconcile every catalog with disk; prune dead entries; report what changed. Never invents content. |
| **ingest** | "process this source" | Read source → extract claims → compare against existing pages → update/create pages → update index → append log. One source may touch many pages. |
| **query** | any question against the wiki | Index-first navigation → read relevant pages → answer with citations → offer to file valuable answers back as pages. |
| **lint** | "health-check the workspace/wiki" | Detect dead files, broken links, drifted catalogs, contradictions, stale claims, orphan pages, missing provenance; report findings and conformance level. |

## 9. The walk test

The acceptance test for any workspace, inherited from ICM:

> An agent with no memory of the workspace must be able to **orient**, **act**,
> and **report status** from the files alone.

- **Orient**: read the Layer 0 catalog and say what this workspace is, what
  forms it contains, and where things live.
- **Act**: perform one operation (run a stage, ingest a source, answer a
  query) following only the instructions found in files.
- **Report**: state what it did, what it produced, what happens next, and
  what is missing or broken.

If any step requires knowledge that exists only in someone's head or in chat
history, the workspace fails. Fix the files, not the agent.

## 10. Conformance levels

| Level | Name | Requirements |
|---|---|---|
| **CCA-0** | Detectable | A folder with a root instruction file (canonical or legacy alias) and plain-text artifacts. Every existing ICM workspace and LLM Wiki is CCA-0. |
| **CCA-1** | Conformant | CCA-0, plus: canonical or correctly-aliased root catalog with directory map and routing rules; every file classifiable into a live role; contracts for pipelines; index + log for wikis; adapters thin. |
| **CCA-2** | Verified | CCA-1, plus: passes the walk test; lint reports no structural errors; log is append-only and machine-parseable; wiki claims carry provenance. |

`cca-lint` reports the level a workspace reaches and what blocks the next one.

## 11. Token and size discipline

Inherited from ICM practice; treat as defaults, not law:

- Layer 0 catalog ≲ 800 tokens. Layer 1 ≲ 300. Layer 2 contracts 200–500.
- Contracts under 80 lines; reference files under 200 lines.
- Per-task delivered context: 2,000–8,000 tokens. If a task routinely needs
  more, the routing is under-specified — fix the structure before enlarging
  the prompt.
- Available context ≠ useful context. The objective is maximum relevant
  signal: the smallest sufficient set of information to execute correctly.

## 12. Out of scope

CCA is not an agent framework, a runtime, a protocol for tool access (that is
MCP's layer), or a replacement for ICM or LLM Wiki. It does not handle
real-time multi-agent collaboration, high-concurrency serving, or automated
mid-pipeline branching — the same boundaries ICM documents. CCA specifies
structure and conventions; harnesses supply execution.
