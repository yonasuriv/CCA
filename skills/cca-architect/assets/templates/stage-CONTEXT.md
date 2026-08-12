# CONTEXT.md — Stage [NN]: [NAME]

> Layer 2 contract. Keep this file small. It scopes exactly what the agent loads, does, and writes.

## Inputs

| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Previous stage | `../0[N-1]-[name]/output/[file].md` | Full file | Source material for this stage |
| [Convention] | `../../_config/[file].md` | [Section name] | Constraint to apply |
| [Domain knowledge] | `../../wiki/[page].md` | [Section name] | Background needed for this stage |
| [Evidence] | `../../raw/[source]` | [Pages/sections] | Evidence to verify or cite |

Load only what this table lists. Do not read unrelated stages.

## Process

1. Read the inputs listed above.
2. Perform this stage's single job.
3. Run any checkpoint or audit below.
4. Write output(s) per the Outputs table.

## Outputs

| Artifact | Location | Format |
|---|---|---|
| [name] | `output/[slug]-[name].md` | Markdown |

## Checkpoint

Delete this section for linear stages. For creative work, pause after a complete unit of work and present the decision the human needs to make before continuing.

## Audit

Delete this section when not useful.

- [ ] [Check with an unambiguous pass condition]
- [ ] [Check that required source/reference sections were followed]
- [ ] [Check that no unlisted context was treated as authoritative]
