---
name: cca-ingest
description: Integrate new source material into a filesystem-native maintained knowledge base while preserving its native schema, provenance rules, and contradiction handling. Use when the user asks to ingest, process, or incorporate a document, article, paper, transcript, note, or other evidence into an LLM Wiki or CCA knowledge workspace. Discovers the workspace's own maintenance conventions first and never requires a fixed CCA directory taxonomy.
compatibility: Filesystem read/write access to the target knowledge workspace. No sibling skill required.
---

# CCA Ingest

Ingestion is integration into maintained knowledge, not one-summary-per-document accumulation.

## Discover the knowledge profile first

Before changing anything:

1. Locate the workspace's own instruction/schema files and navigation entry points.
2. Identify where durable source material lives, where maintained synthesis lives, and how provenance is represented.
3. Identify the workspace's existing naming, metadata, index, and history conventions.
4. If the workspace is intentionally CCA-hardened, follow those conventions. If it is a native LLM Wiki implementation, preserve its own schema instead of imposing CCA's preferred layout.

If no maintained-knowledge structure exists, stop and explain what minimum structure is missing. Do not silently invent a full wiki during ingest.

## Procedure

1. **Establish source identity.** Determine the durable source artifact and a stable way to cite it. Do not overwrite source evidence while synthesizing.
2. **Read the source.** Extract material claims, entities, concepts, dates, relationships, and uncertainty. Keep source statements distinct from your inference.
3. **Navigate existing synthesis using the workspace's own router/index/schema.** Read only pages relevant to the new material.
4. **Compare claim by claim:**
   - **supports** — strengthens existing knowledge;
   - **extends** — adds compatible detail;
   - **contradicts** — preserve both positions with source/time context rather than silently replacing one;
   - **creates** — introduces knowledge not represented yet.
5. **Update maintained synthesis** according to the workspace's existing page format and provenance policy. Prefer updating canonical pages over creating isolated source summaries when the knowledge belongs on existing pages.
6. **Update navigation/metadata/history** only where the workspace already defines those mechanisms or the user explicitly adopted a CCA-hardened profile.
7. **Verify references.** Every newly introduced source-backed assertion that the workspace promises to trace must resolve to the underlying evidence.
8. **Report** what changed, what evidence was added, which contradictions or uncertainties remain, and which files contain the durable result.

## Optional CCA-hardened profile

If the workspace explicitly uses CCA's hardened knowledge bundle, its common conventions may include:

- durable evidence under `raw/`;
- maintained synthesis under `wiki/`;
- `wiki/index.md` as navigation;
- `log.md` as a maintenance chronicle;
- frontmatter/lifecycle/provenance metadata.

Follow those conventions when present. Do not describe them as universal LLM Wiki requirements.

## Batch ingestion

When processing multiple sources:

- integrate sources one at a time so provenance and contradiction effects remain attributable;
- avoid combining unrelated sources into a single synthetic "source" record;
- update shared synthesis incrementally;
- deliver one consolidated final report unless the workspace requires per-source review gates.

## Production rules

- Never rewrite durable evidence as though it were synthesis.
- Never resolve a contradiction by silently deleting the older claim.
- Never fabricate provenance, source locations, dates, or confidence.
- Preserve the knowledge base's native schema unless an explicit migration/hardening change was requested.
- Do not depend on templates or files outside this skill package.
- Load only the pages required to integrate the source correctly.
