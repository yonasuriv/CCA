---
name: cca-scaffold
description: Add a CCA context layer to an existing project without restructuring it — generates the AGENTS.md root catalog, CONTEXT.md task routing, and _config/ conventions in place. Use when the user wants to "add CCA/ICM to this project", "make this repo agent-friendly", "set up AGENTS.md", or "give agents orientation in this folder". Supports quick mode (routing only, existing folders untouched) and full mode (adds pipeline stages or a wiki). Works with any agent; emits thin tool adapters (CLAUDE.md, .cursorrules, etc.) on request.
---

# CCA Scaffold

Give an existing project immediate agent orientation with the smallest
possible footprint. Two files at the root — `AGENTS.md` and `CONTEXT.md` —
eliminate the "let me explore your filesystem" wasted turns at the start of
every session.

Scaffold **adds**; it never restructures, renames, or deletes existing
content. If the user wants reorganization, that is the cca-architect skill's
restructure mode.

## Mode selection

- **Quick mode (default):** routing and reference only. Use for existing
  projects whose layout is fine and whose folders should stay untouched.
- **Full mode:** adds physical structure for new capability — numbered stage
  folders with contracts (pipeline) or `raw/` + `wiki/` + `log.md`
  (knowledge). Use when the project has a repeated multi-step workflow or
  needs accumulating knowledge, and the user agrees.

Ask which mode only if the answer is not obvious from the request.

## Quick mode procedure

1. **Survey the project.** List top-level folders; read any existing
   instruction files (`README.md`, `CLAUDE.md`, `IDENTITY.md`,
   `.cursorrules`, …); sample a few key files to learn what the project is
   and how it is organized. Do not read everything.
2. **Write `AGENTS.md`** (root catalog, ≲ 800 tokens): what the project is,
   directory map of what actually exists, routing rules for the 3–6 most
   common intents, operating principles, authority order. Use the template
   at `../cca-architect/assets/templates/AGENTS.md` if available; otherwise
   follow its structure.
3. **Write `CONTEXT.md`** (task routing, ≲ 300 tokens): intent →
   folder/procedure table, shared resources, current state.
4. **Create `_config/`** with starter `conventions.md` (naming, style,
   review rules observed in the project) and `glossary.md` (domain terms
   found during the survey). Only include what the survey evidenced — do not
   invent conventions.
5. **Handle existing root files.** If `CLAUDE.md` or `IDENTITY.md` already
   exists and contains real content: merge unique content into `AGENTS.md`,
   then reduce the legacy file to a thin adapter pointing at `AGENTS.md`.
   Show the user the before/after of any file you modify.
6. **Emit adapters on request** for the tools the user names (see the CCA
   spec's adapter conventions: 2–5 lines, pointer only, never a copy).
7. **Report**: what was created, what was modified, and the first intent the
   user should test ("ask the agent to do X and watch it route").

## Full mode procedure

Quick mode, plus one or both of:

- **Pipeline:** for each stage of the workflow (extract stages from how the
  user describes the work — typically 2–5), create `stages/NN_name/` with a
  contract `CONTEXT.md` (Inputs / Process / Outputs, from the stage
  template), `references/`, and `output/`. Add a routing row per stage.
- **Wiki:** create `raw/` (with a note that it is immutable), `wiki/` with
  `overview.md`, `entities/`, `concepts/`, `sources/`, `syntheses/`, and
  `index.md`; create `log.md` with the init entry. Add ingest/query routing
  rows.

Then update `AGENTS.md` and `CONTEXT.md` to route to the new structure.

## Rules

- Never invent content: every catalog entry must correspond to something on
  disk or something this run just created.
- Never overwrite an existing file without showing the user the diff.
- Keep catalogs within token budgets (root ≲ 800, routing ≲ 300).
- The result should reach CCA-1 conformance; say so, and name what blocks
  CCA-2 (usually: the walk test and a lint pass — offer to run them).
