# Core reference: layers, roles, naming, token discipline

Read this before building or restructuring any workspace. Condensed from the
CCA specification; when in doubt, `spec/SPEC.md` in the CCA repo is normative.

## The five layers

| Layer | File(s) | Question | Budget |
|---|---|---|---|
| 0 | `AGENTS.md` | "Where am I?" | ~800 tok |
| 1 | `CONTEXT.md`, `wiki/index.md` | "Where do I go?" | ~300 tok |
| 2 | stage `CONTEXT.md` | "What do I do?" | 200–500 tok |
| 3 | `_config/`, `references/`, `raw/` | "What rules? What evidence?" | 500–2k tok, selective |
| 4 | `output/`, `wiki/` | "What am I working with? What do we know?" | varies |

Agents read down and stop when they have enough. Per-task delivered context
should land in 2,000–8,000 tokens. If a task needs more, the routing is
under-specified — fix structure, not prompt size.

Layer 3 is internalized as constraints (rules, evidence). Layer 4 is
processed as input (material to transform, knowledge to update). Keep them
structurally separate so the model never has to sort rules from inputs.

## The eight roles

| Role | Function | Mutability | Lives in |
|---|---|---|---|
| catalog | points at everything, stores ~nothing | rare | `AGENTS.md`, `CONTEXT.md`, `index.md` |
| contract | one unit of work: inputs/process/outputs | on redesign | stage `CONTEXT.md` |
| factory | stable rules, configured once | stable | `_config/`, `references/` |
| source | immutable evidence, cited never edited | immutable | `raw/` |
| synthesis | derived knowledge the agent maintains | evolves | `wiki/` |
| product | per-run artifacts, human-editable | every run | `output/` |
| chronicle | append-only history | append-only | `log.md` |
| dead | unreferenced, unowned | flag via lint | — |

Classification heuristics when auditing:
- Does it tell the agent where to go? → catalog.
- Does it define one task's inputs/process/outputs? → contract.
- Would changing it change every future run? → factory.
- Is it evidence the agent must not alter? → source.
- Is it maintained, cross-referenced knowledge? → synthesis.
- Is it regenerated each run? → product.
- Is it a timestamped record? → chronicle.
- Nothing references it and it references nothing? → dead.

## Naming and authority

Canonical: `AGENTS.md` > legacy `CLAUDE.md` > `IDENTITY.md` > `README.md`.
Tool adapters (`GEMINI.md`, `.cursorrules`, `.windsurfrules`,
`.github/copilot-instructions.md`) are 2–5 line pointers, never copies.
Wiki: `raw/`, `wiki/`, `wiki/index.md`, `log.md`. Pipelines:
`stages/NN_name/` (numbering encodes order), `_config/`, `setup/`.

## Contracts

Required sections: **Inputs** (table: source, location, section/scope, role,
why), **Process** (numbered steps), **Outputs** (table: artifact, location,
format). Creative stages add **Checkpoints** (human steering pauses) and
**Audit** (checks with unambiguous pass conditions, run before writing
output). Contracts < 80 lines; reference files < 200 lines.

## Wiki hygiene

Pages carry YAML frontmatter (`type`, `status`, `created`, `updated`,
`sources`, `tags`). Every source-derived claim links to its source.
Contradictions are preserved with dates, not overwritten. `index.md` updated
on every ingest; `log.md` entries start `## [YYYY-MM-DD] op | subject` so
`grep "^## \[" log.md` parses history.

## The five principles (from ICM, inherited)

1. One stage, one job.
2. Plain text as the interface.
3. Layered context loading.
4. Every output is an edit surface.
5. Configure the factory, not the product.

Plus two from the LLM Wiki pattern:

6. Persistent synthesis over stateless retrieval.
7. The human curates and steers; the agent does the bookkeeping.
