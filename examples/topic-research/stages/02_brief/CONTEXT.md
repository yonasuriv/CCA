# CONTEXT.md — Stage 02: brief

> Layer 2 contract. Compile the reviewed collect notes into the weekly brief.

## Inputs

| Source | File/Location | Section/Scope | Role | Why |
|---|---|---|---|---|
| Previous stage | `../01_collect/output/` (latest notes file) | Full file | product | This week's findings |
| Voice guide | `../../_config/voice.md` | Full file | factory | Register, structure, hard constraints |
| Thesis page | `../../wiki/syntheses/current-thesis.md` | Full file | synthesis | Frame findings against the standing thesis |

Load only what this table lists. Do not re-read the whole wiki.

## Process

1. Read the collect notes (whatever the human left after review — edits are
   the input).
2. Select the findings that matter for a five-minute read; drop the rest.
3. Draft the brief: what changed this week first, one short paragraph per
   finding, every claim attributed. Under 400 words.
4. Check each finding against the current thesis: does it support, extend,
   or challenge it? Say which, in one clause.
5. Run the audit, then write the output.

## Outputs

| Artifact | Location | Format |
|---|---|---|
| Weekly brief | `output/YYYY-MM-DD-weekly-brief.md` | Markdown with frontmatter (`stage`, `date`, `inputs`) |

## Checkpoint

After step 2, present the selected findings and the dropped ones; wait for
the human to confirm or adjust the selection before drafting.

## Audit (run before writing output)

- [ ] Under 400 words; no bullet carries more than one claim.
- [ ] Every finding attributed to a wiki page (and thereby to its sources).
- [ ] Contested findings are presented as contested, with confidence notes.
- [ ] Voice rules in `_config/voice.md` followed (no hype, change-first).
