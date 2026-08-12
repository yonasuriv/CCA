# Compatibility: ICM ↔ LLM Wiki ↔ CCA

Normative companion to `SPEC.md`. This document defines how the three systems
map onto each other and what "swappable" concretely means.

## 1. Concept mapping

| CCA concept | ICM equivalent | LLM Wiki equivalent |
|---|---|---|
| Layer 0 catalog (`AGENTS.md`) | Layer 0 `CLAUDE.md` ("Where am I?") | The schema file ("e.g. CLAUDE.md or AGENTS.md") |
| Layer 1 catalog (`CONTEXT.md`) | Layer 1 `CONTEXT.md` ("Where do I go?") | `index.md` (content-oriented routing) |
| Layer 2 contract (stage `CONTEXT.md`) | Layer 2 stage contract | Ingest/query/lint procedures in the schema |
| factory role (`_config/`, `references/`) | Layer 3 reference material | Schema conventions (page formats, linking rules) |
| source role (`raw/`) | Layer 4 input material (user-provided) | **Raw sources** (immutable) |
| product role (`output/`) | Layer 4 working artifacts | (per-query answers, before filing back) |
| synthesis role (`wiki/`) | No equivalent — CCA adds it | **The wiki** (LLM-owned, maintained) |
| chronicle role (`log.md`) | Git history (implicit) | **log.md** (explicit, append-only) |
| run operation | Executing a stage per its contract | — |
| ingest / query / lint operations | — | The three Wiki operations |
| sync / scaffold operations | icm-template's `icm-sync` / `icm-scaffold` | — |
| walk test | ICM walk test / workspace validation | "The LLM is a disciplined wiki maintainer" |

The two parent systems are complementary halves:

- ICM models **work over time within one run** (stages, handoffs, gates).
- LLM Wiki models **knowledge over time across runs** (synthesis that compounds).
- CCA's union: pipelines read from and write into wikis; wikis feed pipelines.
  `raw/` is stable evidence (Layer 3 behavior); `wiki/` is maintained working
  knowledge (Layer 4 behavior that persists instead of resetting each run).

## 2. Root file resolution

An agent entering any workspace resolves the Layer 0 root in this order:

1. `AGENTS.md` — canonical (ecosystem standard)
2. `CLAUDE.md` — ICM legacy alias
3. `IDENTITY.md` — icm-template legacy alias
4. `README.md` — last-resort fallback

Rules:

- The first file found is authoritative. Lower-precedence files **must not**
  contradict it.
- A legacy file may *be* the full catalog (CCA-0/1 acceptable), or a thin
  adapter pointing to `AGENTS.md` (preferred).
- Tool-specific files (`GEMINI.md`, `.cursorrules`, `.windsurfrules`,
  `.github/copilot-instructions.md`) are **adapters only**: a two-to-five-line
  pointer. Never a fork of the rules. One fact, one home.

## 3. Swap guarantees

### 3.1 ICM workspace → CCA

An ICM workspace is CCA-0 as-is. To reach CCA-1:

1. Add `AGENTS.md` as the root catalog (use the template in
   `skills/cca-architect/assets/templates/AGENTS.md`).
2. Reduce `CLAUDE.md` to an adapter: "Read `AGENTS.md`; it is authoritative."
3. Everything else — `CONTEXT.md` files, stage folders, `_config/`, `output/`
   conventions — is already conformant. Stage contracts are CCA contracts
   unchanged.

### 3.2 LLM Wiki → CCA

An LLM Wiki is CCA-0 as-is. To reach CCA-1:

1. Add `AGENTS.md` as the root catalog. Its directory map lists `raw/`,
   `wiki/`, `wiki/index.md`, `log.md`; its routing rules point "ingest/query/
   lint" intents at the schema procedures.
2. Keep `raw/`, `wiki/`, `index.md`, `log.md` exactly as they are.
3. Schema conventions either stay where they are (catalog links to them) or
   move into `_config/`; the catalog must point at their home.

### 3.3 CCA → ICM tooling

CCA workspaces degrade gracefully for ICM-only agents:

- The `CLAUDE.md` adapter routes a Claude-hardcoded agent into the workspace.
- Stage contracts use ICM's exact Inputs/Process/Outputs format.
- Numbered stage folders, `references/`, `output/`, and review gates behave
  identically.
- CCA-only additions (`raw/`, `wiki/`, `log.md`) are plain folders an ICM
  agent can simply ignore or read as ordinary reference material.

### 3.4 CCA → LLM Wiki practice

- `raw/`, `wiki/`, `index.md`, `log.md` follow the Wiki pattern verbatim;
  Obsidian, git tooling, and Wiki-style prompting all work unchanged.
- The Wiki "schema" lives in `AGENTS.md` + `_config/`, both of which the Wiki
  pattern already names as valid schema locations.

### 3.5 ICM ↔ LLM Wiki (through CCA)

- Adding a wiki to an ICM workspace: create `raw/`, `wiki/`, `wiki/index.md`,
  `log.md`; add routing lines to the root catalog; adopt the ingest/query/lint
  procedures (or install the matching skills). The pipeline stages can then
  read `wiki/` pages as factory or source context.
- Adding a pipeline to an LLM Wiki: create `stages/NN_name/` folders with
  CCA contracts whose Inputs tables point at `wiki/` pages and `raw/` sources.
  The wiki becomes the pipeline's standing memory.

## 4. Non-goals

- CCA does not translate *behavioral quality* across models. Structure is
  portable; how a given model performs inside that structure is empirical.
- CCA does not version-pin ICM or LLM Wiki. It tracks them upstream; where
  they diverge from this document, file an issue — convergence is the goal.
