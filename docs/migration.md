# Migration guide

How to bring an existing project into CCA. Every path ends at CCA-1
(conformant); run the walk test from `spec/SPEC.md` to claim CCA-2.

The fastest route for all of these: point your agent at this repo and ask it
to use `cca-scaffold` (add structure in place) or `cca-architect` (full
restructure). What follows is the manual equivalent.

## Path A — From an ICM workspace

You need: an ICM workspace with `CLAUDE.md`, `CONTEXT.md`, `stages/`,
`_config/`.

1. **Add the canonical root.** Create `AGENTS.md` from
   `skills/cca-architect/assets/templates/AGENTS.md`. Fill in the directory
   map and routing rules for your workspace.
2. **Demote `CLAUDE.md` to an adapter** (see `spec/adapters.md`):
   ```markdown
   # CLAUDE.md
   This workspace follows the Convergent Context Architecture.
   Read `AGENTS.md` — it is the authoritative root catalog.
   ```
   Move any content that only existed in `CLAUDE.md` into `AGENTS.md` first.
3. **Done.** Your `CONTEXT.md` routing, stage contracts, `_config/`, and
   `output/` handoffs are already conformant — that format *is* CCA's.
4. Optional: add knowledge capability later by creating `raw/`, `wiki/`,
   `wiki/index.md`, `log.md` and routing ingest/query/lint (see Path B, in
   reverse).

Nothing is renamed, deleted, or reformatted. ICM tooling keeps working.

## Path B — From an LLM Wiki

You need: `raw/`, `wiki/`, `index.md`, `log.md`, and a schema file
(`CLAUDE.md`, `AGENTS.md`, or similar).

1. **Add (or upgrade) the root catalog.** If you already have `AGENTS.md`
   as your schema, add a directory map and routing rules if missing. If your
   schema lives in `CLAUDE.md` or `schema.md`, move its conventions into
   `AGENTS.md` (or `_config/`) and leave a thin adapter behind.
2. **Keep everything else exactly as-is.** `raw/` is the source role,
   `wiki/` is synthesis, `index.md` is a catalog, `log.md` is the chronicle.
   You were already speaking CCA.
3. **Check the wiki hygiene rules:** frontmatter on pages, provenance links
   to sources, log entries with a consistent `## [DATE] op | subject`
   prefix. `cca-lint` will report gaps.
4. Optional: add a pipeline later — `stages/01_.../` folders whose contracts
   read from `wiki/` and write to `output/` (see `examples/topic-research/`).

## Path C — From a CLAUDE.md-only repo (no structure yet)

You need: a project with a single instruction file and folders that grew
organically.

1. Run `cca-scaffold` in quick mode, or manually:
   - Write `AGENTS.md`: what this project is, the directory map, routing
     rules ("for X, look in Y"), authority order.
   - Write `CONTEXT.md`: given common tasks, which folder or procedure
     handles each.
   - Create `_config/` for stable conventions (style, glossary, decisions).
2. Leave all existing folders untouched. Quick mode adds a routing layer; it
   does not restructure.
3. If the project has a repeated multi-step workflow, promote it to full
   mode: numbered stage folders with contracts. If it has accumulating
   knowledge, add the wiki triad (`raw/`, `wiki/`, `index.md` + `log.md`).

## Path D — From an unstructured folder ("organize this mess")

Use `cca-architect` in restructure mode. It will:

1. Audit the folder and classify every file by role (catalog / contract /
   factory / source / synthesis / product / chronicle / dead).
2. Propose a migration map — where each file should live — for your approval
   *before* moving anything.
3. Migrate, generate the missing catalogs and contracts, then run the walk
   test to validate.

Never let the agent skip step 2. The map is the review gate.

## After any migration

- [ ] `AGENTS.md` exists, is a catalog (points, doesn't store), ≤ ~800 tokens
- [ ] Root authority order respected; adapters are thin pointers
- [ ] Every file classifiable into one of the eight roles
- [ ] Pipelines: every stage has a contract with an Inputs table
- [ ] Wikis: `index.md` current, `log.md` append-only and parseable
- [ ] `cca-lint` passes with no structural errors
- [ ] Walk test: a fresh agent orients, acts, and reports from files alone
