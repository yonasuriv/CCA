# Query mode

Query maintained synthesis first; use source evidence when the answer requires verification.

## Discover routing

1. Read the applicable workspace instructions/schema.
2. Identify the knowledge navigation entry point: index, map, links, search procedure, or another schema-defined router.
3. Identify how the workspace represents provenance, admission classification, contradictions, and durable query results.
4. Identify whether nearby material belongs to a method overlay such as Zettelkasten or PARA and whether it is source/reference or maintained synthesis.
5. Preserve the native/profile contract. Do not invent CCA paths when the workspace uses another valid layout.

## Procedure

1. **Route before searching broadly.** Use the workspace's index/map/schema to identify relevant synthesis.
2. **Read the smallest sufficient set of pages.** Follow relevant links rather than loading the whole knowledge base.
3. **Respect authority boundaries.** Do not treat human-authored Zettelkasten/PARA material or human-admitted source evidence as writable synthesis unless the workspace explicitly permits it.
4. **Escalate to evidence when needed.** Inspect cited/source material for exact wording, numbers, dates, disputed claims, or confidence judgments.
5. **Preserve admission metadata separately from epistemic judgment.** In the Hybrid Workspace Profile, both `reference.curated` and `reference.collected` resolve to `knowledge.reference`; curated/collected says whether the source has been explicitly curated (v2: how it was admitted), not whether the source is true or endorsed and not who acquired it.
6. **Answer with traceability.** Distinguish maintained synthesis, direct evidence, source admission/review state where relevant, unresolved contradictions, and your inference.
7. **Expose gaps.** If the workspace does not contain enough evidence, say what is missing rather than filling the gap from unstated assumptions.
8. **Persist only when appropriate.** Write the result back only when the user requests it or the workspace explicitly defines query-to-knowledge maintenance as normal behavior. Follow the workspace's existing page/index/history conventions.

## Hybrid Workspace evidence routing

For a current Hybrid Workspace Profile target:

- resolve both `reference.curated` and `reference.collected` as semantic role `knowledge.reference`;
- use the most-specific binding to interpret admission policy/provenance;
- do not treat `reference.collected` as agent-authored content merely because an agent acquired it;
- do not treat `reference.curated` as verified truth merely because a human admitted it;
- a human-reviewed collected source remains collected; review state is metadata;
- conclusions/synthesis produced from either source class belong to `knowledge.durable` when persisted as maintained knowledge;
- reports/articles/PDFs deliberately produced for external use remain `output.artifact`;
- a research engagement/project remains `work.project` rather than becoming another knowledge category.

Query mode does not relocate or reclassify evidence merely because it was used successfully in an answer.

## Durable answers

A result is usually worth persisting when it creates reusable knowledge such as a comparison, timeline, synthesis, resolved relationship, or documented open question. Ephemeral lookups generally should remain conversational.

When persisting:

- update the canonical knowledge page where possible;
- preserve provenance to every source used;
- write synthesis as synthesis, not into the preserved evidence corpus;
- update navigation/history only according to the active schema;
- avoid creating duplicate pages that restate existing canonical knowledge.

## Production rules

- Never present maintained synthesis as direct source evidence.
- Never present admission into a reference corpus as proof of correctness or endorsement.
- Never silently choose one side of a recorded contradiction.
- Never fabricate citations, source locations, provenance, admission, or review state.
- Do not require `wiki/index.md`, `log.md`, or any CCA-specific taxonomy unless the workspace adopted them.
- Preserve human/method-overlay write boundaries.
- Implementation files referenced by this skill remain skill-local.
- Cross-skill coordination uses semantic skill names, never sibling filesystem paths.
- Keep navigation progressive: router → relevant synthesis → evidence only as needed.
