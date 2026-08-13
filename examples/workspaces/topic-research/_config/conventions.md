# Conventions — topic-research

Role: factory. Workspace-wide rules; stage contracts may tighten them for
their stage but never loosen them.

## Files and naming

- Sources land in `raw/` named `YYYY-MM-DD-slug.ext` and are never edited.
- Wiki pages use kebab-case slugs; every page carries YAML frontmatter
  (`type`, `status`, `created`, `updated`, `sources`, `tags`).
- Stage outputs land in their stage's `output/` named `YYYY-MM-DD-slug.md`.

## Knowledge

- Every claim in the wiki links its source page. No uncited synthesis.
- Contradictions are recorded with dates, never silently resolved.
- `wiki/index.md` updates on every ingest; `log.md` is append-only with
  `## [YYYY-MM-DD] op | subject` entries.

## Review

- The human reviews each stage output before the next stage runs. Edits
  made at review are the input the next stage reads.
