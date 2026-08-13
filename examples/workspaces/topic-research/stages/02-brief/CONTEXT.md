# CONTEXT.md -- Stage 02: brief

> Layer 2 contract. Compile the human-reviewed collection notes into the weekly brief.

## Inputs

| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Previous stage | `../01-collect/output/` (latest notes file) | Full file | Reviewed findings for this reporting window |
| Voice guide | `../../_config/voice.md` | Full file | Register, structure, and writing constraints |
| Thesis page | `../../wiki/syntheses/current-thesis.md` | Full file | Frame findings against the standing thesis |

Load only what this table lists. Do not re-read the whole wiki.

## Process

1. Read the collect notes exactly as the human left them after review.
2. Select the findings that matter for a five-minute read; identify dropped findings explicitly.
3. At the checkpoint, present selected and dropped findings for human steering.
4. Draft under 400 words with change-first structure and attributed claims.
5. State whether each material finding supports, extends, or challenges the current thesis.
6. Run the audit, then write the brief.

## Outputs

| Artifact | Location | Format |
|---|---|---|
| Weekly brief | `output/YYYY-MM-DD-weekly-brief.md` | Markdown |

## Checkpoint

After step 2, present selected and dropped findings. Continue only after the human confirms or adjusts the selection.

## Audit

- [ ] Under 400 words.
- [ ] Every material finding is traceable through the collection notes to maintained knowledge.
- [ ] Contested findings remain visibly contested.
- [ ] `_config/voice.md` constraints are satisfied.
