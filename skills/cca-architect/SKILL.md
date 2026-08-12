---
name: cca-architect
description: Design any process, idea, or problem into a CCA workspace (filesystem-native agent context), or restructure an existing folder, repo, or vault into one. Use when the user wants to "build a workspace for X", "structure this for agents", "CCA/ICM this", "organize this folder for LLM use", create a knowledge base or wiki for an agent, or migrate an existing ICM workspace or LLM Wiki to the Convergent Context Architecture. Produces agent-agnostic workspaces: AGENTS.md root catalog, CONTEXT.md routing and stage contracts, raw/wiki/output layers, and thin tool adapters.
---

# CCA Architect

Design workspaces where the folder structure is the agent architecture. One
agent, reading the right files at the right moment, does the work of a
multi-agent framework — and a human can open any folder and see exactly what
state the system is in.

Two modes:

- **Build** — a new workspace from a described workflow or knowledge domain.
- **Restructure** — an existing folder, repo, ICM workspace, or LLM Wiki into
  CCA conformance.

Before either mode, read `references/core.md` for the invariants (layers,
roles, naming, token discipline). Consult `references/forms.md` when choosing
or recognizing a workspace form. Copy starter files from `assets/templates/`
rather than writing them from scratch.

## Invariants (never violate, in either mode)

1. `AGENTS.md` is the Layer 0 root catalog. Legacy roots (`CLAUDE.md`,
   `IDENTITY.md`) become thin adapters pointing at it. Never fork content
   into adapters.
2. Catalogs point; they do not store. Root ≲ 800 tokens, routing ≲ 300,
   contracts 200–500 tokens and under 80 lines.
3. Every file gets exactly one role: catalog, contract, factory, source,
   synthesis, product, chronicle — or dead (flag it, don't keep it).
4. One fact, one home. Link, don't duplicate.
5. `raw/` is immutable. The agent reads and cites sources; it never edits them.
6. Numbered stage folders encode execution order; each stage has a contract
   with an Inputs table scoping exactly which files (and sections) it loads.
7. Plain text only. No binary state, no required databases, no servers.
8. Every workspace must pass the walk test (below) before delivery.

## Build mode

1. **Extract the structure already present in the user's description.**
   Listen for: the stages (what happens in what order), the human gates
   (where review matters), what is stable vs per-run (factory vs product),
   and what is evidence vs derived knowledge (source vs synthesis). Ask only
   about gaps — never interrogate for information the description implies.
2. **Pick one form.** Read `references/forms.md` and choose the smallest of:
   Pipeline, Umbrella, Record library, Knowledge bundle, Context map. Forms
   compose; a knowledge bundle feeding a pipeline is a common hybrid. If the
   user's need is pure knowledge accumulation, that is the Knowledge bundle
   (the LLM Wiki pattern) — do not force stages onto it.
3. **Scaffold the smallest workspace that carries the form.** Copy templates
   from `assets/templates/` and fill them from the description:
   - Root `AGENTS.md` (catalog), root `CONTEXT.md` (routing).
   - For pipelines: `stages/NN_name/` folders, each with a contract
     (`CONTEXT.md` template), `references/`, `output/`.
   - For knowledge: `raw/`, `wiki/` with `index.md`, `log.md`, starter
     `overview.md`.
   - `_config/` for stable conventions; `setup/questionnaire.md` for one-time
     onboarding (configure the factory, not the product).
4. **Emit adapters on request.** If the user names tools (Claude Code,
   Cursor, Copilot, Windsurf, Gemini), write thin adapter files per
   `spec/adapters.md` in the repo root. Two to five lines each.
5. **Validate with the walk test.** Then report what was built, which form,
   and the first operation the user should run.

## Restructure mode

1. **Audit.** Inventory the folder. Classify every file by role: catalog,
   contract, factory, source, synthesis, product, chronicle, dead. Detect the
   current root file(s) and any existing conventions (ICM layers, Wiki
   triad). Read enough content to classify confidently — do not guess from
   filenames alone.
2. **Propose a migration map.** A table: file → role → destination → action
   (keep / move / merge / adapt / flag-dead). Include the new catalogs and
   contracts to be generated. **Stop here and get explicit approval.** The
   map is the review gate; never restructure without it.
3. **Migrate.** Execute the approved map. Preserve all content — moves and
   merges, no silent deletions. Generate `AGENTS.md`, `CONTEXT.md`, missing
   stage contracts or wiki triad files. Convert legacy roots to adapters.
4. **Validate.** Run the walk test. Then run a lint pass (see the cca-lint
   skill) and fix what it flags. Report before/after structure.

## The walk test

The acceptance test for every workspace you build or restructure. Simulate a
fresh agent with no memory:

1. **Orient** — from `AGENTS.md` (+ `CONTEXT.md`) alone, state what the
   workspace is, which forms it contains, and where things live.
2. **Act** — perform one real operation (run a stage from its contract,
   ingest a sample source, or answer a query from the wiki) following only
   instructions found in files.
3. **Report** — what was done, what was produced, what happens next, what is
   missing or broken.

If any step needs knowledge that exists only in someone's head or in chat
history, the workspace fails. Fix the files, not the explanation.

## Anti-patterns to refuse or repair

- A root catalog stuffed with content that belongs in `_config/` or `wiki/`.
- Stage contracts without Inputs tables (agent guesses context → bloat).
- Pipelines forced onto knowledge-accumulation problems, or wikis forced
  onto sequential production problems. Match the form to the work.
- Adapters that restate rules (forks that will drift).
- `output/` artifacts committed as if they were configuration.
- Any convention invented where an ecosystem standard exists (use
  `AGENTS.md`, `SKILL.md`, `CONTEXT.md`, `index.md`, `log.md`).
