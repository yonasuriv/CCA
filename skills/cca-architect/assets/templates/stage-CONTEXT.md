# CONTEXT.md — Stage [NN]: [NAME]

> Layer 2 contract. 200–500 tokens, under 80 lines. This file is the control
> point: it scopes exactly what the agent loads, does, and writes.

## Inputs

| Source | File/Location | Section/Scope | Role | Why |
|---|---|---|---|---|
| Previous stage | `../0[N-1]_[name]/output/[file].md` | Full file | product | Source material for this stage |
| [Convention] | `../../_config/[file].md` | [Section name] | factory | [Constraint to internalize] |
| [Domain knowledge] | `../../wiki/[page].md` | [Section name] | synthesis | [Background to apply] |
| [Evidence] | `../../raw/[source]` | [Pages/sections] | source | [Evidence to cite] |

Load only what this table lists. Do not read other stages' folders.

## Process

1. [Read the inputs listed above.]
2. [Transform: what the agent actually does, in order.]
3. [Reference any audit or checkpoint below.]
4. Write output(s) per the Outputs table.

## Outputs

| Artifact | Location | Format |
|---|---|---|
| [name] | `output/[slug]-[name].md` | Markdown with frontmatter (`stage`, `date`, `inputs`) |

## Checkpoint (creative stages; delete if linear)

After step [N], pause: present [options / draft direction] and wait for human
steering before continuing.

## Audit (run before writing output; delete if not needed)

- [ ] [Check with an unambiguous pass condition, e.g. "Every claim cites a source from raw/"]
- [ ] [e.g. "Output follows the structure in _config/[template].md"]
- [ ] [e.g. "No content from stages other than those in Inputs"]
