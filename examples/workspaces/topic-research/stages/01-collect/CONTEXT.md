# CONTEXT.md -- Stage 01: collect

> Layer 2 contract. Collect what changed during the current reporting window from maintained knowledge.

## Inputs

| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Wiki index | `../../wiki/index.md` | Full file | Find pages updated during the reporting window |
| Chronicle | `../../log.md` | Entries since the previous Stage 01 run | Identify ingests and queries since the last collection |
| Conventions | `../../_config/conventions.md` | "Knowledge" section | Apply citation and uncertainty rules |

Load only what this table lists. Then read only the wiki pages identified as changed during the reporting window.

## Process

1. Determine the collection window from `log.md`: after the previous `run | Stage 01-collect` entry, or workspace initialization if none exists.
2. Use the index and chronicle to identify pages created or updated in that window.
3. Read those pages and extract candidate findings: new facts, changed claims, contradictions, resolved questions, and new open questions.
4. Rank findings by likely value to the weekly brief. Preserve uncertainty and disagreement instead of resolving them implicitly.
5. Run the audit, then write the collection notes.

## Outputs

| Artifact | Location | Format |
|---|---|---|
| Collection notes | `output/YYYY-MM-DD-collect-notes.md` | Markdown; ranked findings with wiki links plus open items |

## Audit

- [ ] Every finding links to the maintained wiki page it came from.
- [ ] No finding falls outside the collection window.
- [ ] Contradictions remain visibly contradictory.
