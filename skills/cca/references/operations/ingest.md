# Ingest mode

Ingestion is integration into maintained knowledge, not one-summary-per-document accumulation.

## Discover the knowledge profile first

Before changing anything:

1. Locate the workspace's own instruction/schema files and navigation entry points.
2. Identify where durable source material lives, where maintained synthesis lives, and how provenance is represented.
3. Identify the workspace's existing naming, metadata, index, and history conventions.
4. Identify whether nearby material belongs to a method overlay such as Zettelkasten or PARA and whether that material is source/reference, human-authored knowledge, or agent-maintained synthesis.
5. If the workspace is intentionally CCA-hardened, follow those conventions. If it is a native LLM Wiki implementation, preserve its own schema instead of imposing CCA's preferred layout.

If no maintained-knowledge structure exists, stop and explain what minimum structure is missing. Do not silently invent a full wiki during ingest. For architecture/design of a new knowledge system, use `cca` in `architect` mode; for focused in-place creation of an already-decided structure, use `cca` in `scaffold` mode.

## Procedure

1. **Establish source identity.** Determine the durable source artifact and a stable way to cite it. Do not overwrite source evidence while synthesizing.
2. **Read the source.** Extract material claims, entities, concepts, dates, relationships, and uncertainty. Keep source statements distinct from your inference.
3. **Navigate existing synthesis using the workspace's own router/index/schema.** Read only pages relevant to the new material.
4. **Respect authority boundaries.** Do not treat Zettelkasten notes, PARA resources, or other human-maintained material as writable synthesis unless the workspace explicitly permits it.
5. **Compare claim by claim:**
   - **supports** — strengthens existing knowledge;
   - **extends** — adds compatible detail;
   - **contradicts** — preserve both positions with source/time context rather than silently replacing one;
   - **creates** — introduces knowledge not represented yet.
6. **Update maintained synthesis** according to the workspace's existing page format and provenance policy. Prefer updating canonical pages over creating isolated source summaries when the knowledge belongs on existing pages.
7. **Update navigation/metadata/history** only where the workspace already defines those mechanisms or the user explicitly adopted a CCA-hardened profile.
8. **Verify references.** Every newly introduced source-backed assertion that the workspace promises to trace must resolve to the underlying evidence.
9. **Report** what changed, what evidence was added, which contradictions or uncertainties remain, and which files contain the durable result.

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
- Preserve human/method-overlay write boundaries unless an explicit maintenance contract says otherwise.
- Implementation files referenced by this skill remain skill-local.
- Cross-skill coordination uses semantic skill names, never sibling filesystem paths.
- Load only the pages required to integrate the source correctly.
