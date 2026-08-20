# CCA scenarios

These scenarios are behavioral expectations, not mandatory directory templates.

## Existing code repository

**Default:** preserve `src/`, tests, docs, build configuration, issue/backlog tools, and native harness instructions. Add only the smallest missing routing layer. Do not ICM-ify a healthy application repository.

## Existing code repository using Scrum

Scrum remains process authority; the backlog remains in its real system of record; Git remains code/history authority; CI/CD remains delivery authority. CCA may route agents to those authorities and may use an ICM-derived workflow for a bounded activity (for example a security review) without turning Scrum into a filesystem schema.

## PARA second brain + Zettelkasten + LLM Wiki

PARA may organize Projects/Areas/Resources/Archives. Zettelkasten remains linked human-governed idea development. An LLM Wiki boundary retains its own published/local ownership and maintenance schema. A nested project can contain an ordinary code repository or upstream-native ICM workspace. CCA preserves each boundary and declares only the relationships/authority needed to operate across them instead of flattening schemas.

PARA `Resources` is organizational, not an epistemic synonym for preserved evidence. A Resource may contain a source, human note, maintained synthesis, dataset, or nested workspace.

## New personal hybrid: projects + notes + research + maintained knowledge

When the user wants coding projects, notes/research/second-brain structure, maintained synthesis, and operational material in one environment, use `cca` in `architect` mode and follow the **Personal hybrid** guidance in `skills/cca/references/architect/methods.md`.

Expected architecture decisions:

- preserve the user's chosen outer organization when it works; PARA is one possible default, not a CCA requirement;
- distinguish capture, preserved evidence, human notes, maintained synthesis, projects/outcomes, and operational state when their authority/lifecycle differs;
- preserve ordinary code repositories as ordinary repositories unless they independently adopt another profile;
- use upstream-native ICM only where the work should actually be an ICM workspace;
- use selected ICM-derived contracts/progressive disclosure only where they improve the workflow;
- consider the optional CCA Hybrid Workspace Profile when its current v2 contract fits the requested hybrid; v2 preserves the frozen-v1 baseline and adds only source-admission classifications beneath `knowledge.reference`;
- when the Hybrid profile is selected, distinguish human-admitted `reference.curated` from automatically acquired `reference.collected` without treating them as different knowledge roles;
- keep automatically collected evidence provenance-preserving and append/deposit-only; human review changes review metadata, not original admission classification;
- route synthesis from either source class into `knowledge.durable`, deliberate deliverables into `output.artifact`, and finite research work into `work.project`;
- otherwise add the smallest custom CCA-compatible routing/semantic layer instead of forcing the profile;
- route large collections through boundary-local routers/catalogs/indexes before broad filesystem search;
- keep derived indexes rebuildable rather than canonical;
- make daily operation understandable from durable workspace files without requiring prior chat memory.

The Hybrid Workspace Profile has its own profile-conformance checks. A custom personal hybrid is not required to mimic that profile or an ICM Layer 0/1/2 structure merely to be CCA-compatible.

## Upstream-native ICM

Preserve and validate the complete applicable current upstream ICM profile. CCA's portable `AGENTS.md` guidance may coexist with the harness-native entry, but must not overwrite native `CLAUDE.md` authority or weaken exact stage contracts.

## System Map

Use only when the user needs change-impact reasoning across a mutable repository, vault, or mixed tree and existing navigation is insufficient. Map evidence and impact; do not duplicate the system.

## Doing nothing is valid

If a fresh consumer can already orient, resolve the relevant authority/context, act with bounded context, and report without broad blind search, CCA should recommend no structural change.
