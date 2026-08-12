# CCA — Convergent Context Architecture

> **CCA is an interoperability and agnostic evolution layer for filesystem-native agent context. \
> It builds on ICM and LLM Wiki, follows ecosystem standards such as AGENTS.md and SKILL.md (and growing), \
> and prefers convergence over introducing competing conventions.**

CCA unifies two proven patterns for structuring agent context as plain files:

- **LLM Wiki** — Andrej Karpathy's pattern for a persistent, LLM-maintained knowledge base: immutable raw sources, a compounding markdown wiki, and a schema that disciplines the agent. (ingest → query → lint)
- **ICM (Interpretable Context Methodology)** — folder structure as agent architecture: numbered stages, layered context loading, stage contracts, human review gates.

CCA does **not** replace either one. It defines the shared ground that lets an ICM workspace, an LLM Wiki, and a CCA workspace be read by the same agent, maintained by the same skills, and swapped for one another without breaking. ICM workspaces and LLM Wikis are already valid CCA workspaces; CCA is the upgraded, agent-agnostic form of both.

> See [Lineage and Credits](#lineage-and-credits) at the bottom of this file.

## Why CCA exists

Both parent patterns are strong, and both have a gap:

| | ICM | LLM Wiki |
| --- | --- | --- |
| **Great at** | Sequential pipelines with human review gates | Accumulating knowledge that compounds over time |
| **Root file** | Hardcoded to `CLAUDE.md` (Claude-only assumption) | "e.g. CLAUDE.md or AGENTS.md" — left open |
| **Knowledge** | Layer 3/4 split, no persistence model across runs | Raw → wiki synthesis, but no pipeline model |
| **Form** | A protocol + reference workspaces | An intentionally abstract idea file |
| **Agent support** | Tested on one model family | "Your agent will build out the specifics" |

Meanwhile the ecosystem has been converging: `AGENTS.md` is now read by most coding agents, and `SKILL.md` is the emerging cross-vendor skill package format. \
CCA's move is to **adopt those standards instead of adding new ones**, give ICM and LLM Wiki one shared vocabulary (layers, file roles, operations), and ship the skills that make any agent — Claude Code, Codex, Cursor, Gemini, open-weight harnesses — a disciplined operator of both.

If ICM gave us the factory floor and LLM Wiki gave us the library, CCA is the building code that lets both coexist under one roof.

## The model in 60 seconds

A CCA workspace is a folder. Agents navigate **five layers** and stop when they
have what they need:

```txt
Layer 0  AGENTS.md               "Where am I?"                catalog               ~800 tok
Layer 1  CONTEXT.md / index.md   "Where do I go?"             catalog               ~300 tok
Layer 2  Stage CONTEXT.md        "What do I do?"              contract              200–500 tok
Layer 3  _config/ + raw/         "What rules and evidence?"   factory + source
Layer 4  output/ + wiki/         "What am I working with?"    product + synthesis
```

Every file in a workspace plays one of eight **roles**:

| Role | What it is | Examples |
| --- | --- | --- |
| **catalog** | Points at everything, stores almost nothing | `AGENTS.md`, `CONTEXT.md`, `wiki/index.md` |
| **contract** | Defines one unit of work: inputs, process, outputs | stage `CONTEXT.md` |
| **factory** | Stable rules, configured once; internalize as constraints | `_config/voice.md`, `references/` |
| **source** | Immutable raw evidence; cite it, never edit it | `raw/` |
| **synthesis** | Derived knowledge the agent owns and maintains | `wiki/` |
| **product** | Per-run artifacts; produced, reviewed, handed off | `output/` |
| **chronicle** | Append-only history | `log.md` |
| **dead** | Unreferenced and unowned — flagged by lint | — |

Agents perform six **operations**, each shipped as a skill:

| Operation | Skill | One line |
| --- | --- | --- |
| architect | `cca-architect` | Design a new workspace, or restructure an existing folder into one. |
| scaffold | `cca-scaffold` | Add a CCA layer to an existing project without disturbing it. |
| sync | `cca-sync` | Reconcile catalogs with what is actually on disk. |
| ingest | `cca-ingest` | Integrate a new source into the wiki — update pages, index, log. |
| query | `cca-query` | Answer from the wiki with citations; file valuable answers back. |
| lint | `cca-lint` | Health-check structure and knowledge; report conformance level. |

That's the whole model. Everything else in this repo is specification, templates, and examples of these layers, roles, and operations.

## Compatibility: the swap guarantee

CCA is designed so the three systems interoperate:

| From | To CCA | To the other |
| --- | --- | --- |
| **LLM Wiki** | Already conformant. The schema section moves into (or is referenced by) the root `AGENTS.md` catalog. | An ICM pipeline drops in as stages that read from `wiki/` and write to `output/`. |
| **ICM workspace** | Already conformant. Rename or alias `CLAUDE.md` → thin adapter pointing at `AGENTS.md`. Stage contracts are already CCA contracts. | An LLM Wiki drops in as a knowledge-bundle form: `raw/`, `wiki/`, `index.md`, `log.md` are standard CCA roles. |
| **CCA workspace** | — | Degrades gracefully: ICM tooling reads the `CLAUDE.md` adapter + `CONTEXT.md` contracts; Wiki tooling reads `raw/`, `wiki/`, `index.md`, `log.md`. Nothing is CCA-only. |

The full mapping, authority order for root files (`AGENTS.md` canonical; `CLAUDE.md`, `IDENTITY.md` legacy aliases), and conformance levels are in [`spec/compatibility.md`](spec/compatibility.md).

**Conformance at a glance:**

- **CCA-0 Detectable** — a folder with a root instruction file and plain-text artifacts. Every existing ICM workspace and LLM Wiki already qualifies.
- **CCA-1 Conformant** — canonical catalogs, files classifiable into the eight roles, contracts for pipelines, index + log for wikis, thin adapters.
- **CCA-2 Verified** — passes the **walk test**: an agent with no memory can orient, act, and report status from the files alone; lint is clean.

## Quickstart

**I have an ICM workspace.** You are done — it is CCA-0 already. To upgrade: add an `AGENTS.md` root catalog (template in `skills/cca-architect/assets/templates/AGENTS.md`) and reduce `CLAUDE.md` to a two-line adapter. See [`docs/migration.md`](docs/migration.md).
**I have an LLM Wiki.** Same story: add the root catalog, keep `raw/`, `wiki/`, `index.md`, `log.md` exactly as they are. Your schema conventions become part of the catalog or `_config/`.
**I am starting fresh.** Point your agent at this repo and ask it to `cca-architect` a workspace for your workflow — or copy `examples/topic-research/` and reshape it.
**I want the skills.** Each skill under `skills/` is a standard `SKILL.md` package. Copy any of them into your agent's skills directory (e.g. `~/.claude/skills/`, `.agents/skills/`, or your tool's equivalent). They are agent-agnostic by design; nothing in them assumes a specific vendor.

## Repository layout

```txt
cca/
├── AGENTS.md                  Root catalog for this repo (CCA dogfooding itself)
├── README.md                  You are here
├── LICENSE                    MIT
├── spec/
│   ├── SPEC.md                The canonical specification (normative)
│   ├── compatibility.md       ICM ↔ LLM Wiki ↔ CCA mapping, swap guarantees
│   └── adapters.md            Per-tool adapter conventions (CLAUDE.md, .cursorrules, …)
├── docs/
│   ├── principles.md          The design principles behind CCA
│   └── migration.md           Migrating from ICM, from an LLM Wiki, from CLAUDE.md-only repos
├── skills/
│   ├── cca-architect/         Build or restructure workspaces (+ references, templates)
│   ├── cca-scaffold/          Add CCA structure to an existing project
│   ├── cca-sync/              Keep catalogs accurate with disk
│   ├── cca-ingest/            Integrate new sources into a wiki
│   ├── cca-query/             Answer from a wiki, file answers back
│   └── cca-lint/              Structural + knowledge health checks, conformance report
└── examples/
    └── topic-research/        Worked example: a wiki feeding a two-stage pipeline
```

## Design principles

CCA inherits its principles; it does not invent them. The short list (full
treatment in [`docs/principles.md`](docs/principles.md)):

1. **One stage, one job.** Decompose by what each unit hides from the rest.
2. **Plain text as the interface.** Any tool that reads text can participate; any human with an editor holds the control surface.
3. **Layered context loading.** Route the right context, not bigger prompts. Prevention, not compression.
4. **Every output is an edit surface.** Human review happens on files, between stages — not in chat history.
5. **Configure the factory, not the product.** Set up once; produce repeatedly.
6. **Persistent synthesis over stateless retrieval.** Knowledge compiles once and is kept current, not re-derived per query.
7. **Convergence over convention.** Adopt ecosystem standards; never mint a competing filename where one exists.

## References

CCA stands on public work by others:

- **[ICM / Model Workspace Protocol](https://github.com/RinDig/Interpretable-Context-Methodology)** — Jake Van Clief & David McDermott,
  _[Interpretable Context Methodology: Folder Structure as Agent Architecture](https://arxiv.org/pdf/2603.16021)_
- **[LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)** — Andrej Karpathy's idea pattern file for LLM-maintained persistent knowledge bases.
- **Ecosystem standards** — [AGENTS.md](https://agents.md) and the Agent Skills [SKILL.md](https://agentskills.io) format.

ICM and LLM Wiki remain independent projects. CCA tracks them; when they evolve, CCA evolves toward them — convergence, not competition.

## Contributing

If you would like to contribute by submitting a PR, ensure the following check passes:

- [ ] If used, would it break ICM principles?
- [ ] If used, would it break LLM Wiki principles?
- [ ] If it's a new convention, is it a GenAI/LLM standard?

## License

MIT. See [LICENSE](LICENSE).
