# CCA scenarios

These scenarios are behavioral expectations, not mandatory directory templates.

## Existing code repository

**Default:** preserve `src/`, tests, docs, build configuration, issue/backlog tools,
and native harness instructions. Add only the smallest missing routing layer.
Do not ICM-ify a healthy application repository.

## Existing code repository using Scrum

Scrum remains process authority; the backlog remains in its real system of
record; Git remains code/history authority; CI/CD remains delivery authority.
CCA may route agents to those authorities and may use an ICM-derived workflow for
a bounded activity (for example a security review) without turning Scrum into a
filesystem schema.

## PARA second brain + Zettelkasten + LLM Wiki

PARA may organize Projects/Areas/Resources/Archives. Zettelkasten remains linked,
human-governed idea development. LLM Wiki remains maintained synthesis. A nested
project can contain an ordinary code repository or native ICM workspace. CCA
preserves each boundary and declares write/authority relationships instead of
flattening schemas.

## New personal hybrid (projects + notes + research + wiki)

When the user wants coding projects, notes/research/second-brain structure, and
the LLM Wiki split (immutable sources vs a wiki that grows)—especially under
deferred trust—use `cca` in `architect` mode and follow the **Personal hybrid**
defaults in `skills/cca/references/architect/methods.md`.

Expected outcomes (paths are flexible; authorities are not):

- projects shelf for normal repos;
- human notes distinct from write-once evidence;
- distinct immutable sources vs growing wiki, with **supersession** (not silent rewrite);
- capture affordance (`inbox/` and/or capture helper);
- seeded source→wiki citation on empty scaffolds;
- checkable integrity helpers from `skills/cca/assets/scripts/` when hardening;
- portable `AGENTS.md` (harness entry files as one-line pointers) with an **ICM / CCA skeleton map** (even when defaults are `CONTEXT.md`);
- **one folder contract per working folder** (default `CONTEXT.md`, or the mapped name) with Purpose / Inputs / Process / Outputs / Human check — cold-agent isomorphic with ICM;
- live factory stamps in the workspace (not only inside installed skills);
- declared status-without-memory scan surface;
- day-to-day `README.md` when the user will continue in a new session;
- daily operation self-describing without mandatory external skill modes.

Behavioral eval: `evals/personal-hybrid-intent/`. Blind ICM-skeleton checks use `cca` lint profile **ICM skeleton compatibility** or an icm-architect walk against the ten invariants without assuming CCA-only filenames.

## Native ICM

Preserve and validate the complete applicable upstream ICM profile. CCA's
portable AGENTS.md guidance may coexist with the harness-native entry, but must
not overwrite an existing native entry or weaken exact stage contracts.

## System Map

Use only when the user needs change-impact reasoning across a mutable repository,
vault, or mixed tree and existing navigation is insufficient. Map evidence and
impact; do not duplicate the system.

## Doing nothing is valid

If a fresh agent can already orient, act, and report with bounded context and the
workspace has clear authorities, CCA should recommend no structural change.
