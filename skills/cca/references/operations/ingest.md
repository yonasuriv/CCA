# Ingest mode

Ingestion is integration into maintained knowledge, not one-summary-per-document accumulation.

## Discover the knowledge profile first

Before changing anything:

1. Locate the workspace's own instruction/schema files and navigation entry points.
2. Identify where durable source material lives, where maintained synthesis lives, and how provenance/admission is represented.
3. Identify the workspace's existing naming, metadata, index, and history conventions.
4. Identify whether nearby material belongs to a method overlay such as Zettelkasten or PARA and whether that material is source/reference, human-authored knowledge, or agent-maintained synthesis.
5. If the workspace is intentionally CCA-hardened or profile-conformant, follow those conventions. If it is a native LLM Wiki implementation, preserve its own schema instead of imposing CCA's preferred layout.

If no maintained-knowledge structure exists, stop and explain what minimum structure is missing. Do not silently invent a full wiki during ingest. For architecture/design of a new knowledge system, use `cca` in `architect` mode; for focused in-place creation of an already-decided structure, use `cca` in `scaffold` mode.

## Procedure

1. **Establish source identity.** Determine the durable source artifact and a stable way to cite it. Do not overwrite source evidence while synthesizing.
2. **Resolve curation policy.** If the current target is the CCA Hybrid Workspace Profile (v3), preserved raw/reference material is `reference.collected` whoever acquired it; only an explicit human-authorized curation puts it in `reference.curated`; material whose role is still unclear stays in `context.capture`. Do not infer this from content authorship or acquisition actor. (Schema v2 targets: human-admitted → curated, automatically acquired → collected.)
3. **Read the source.** Extract material claims, entities, concepts, dates, relationships, and uncertainty. Keep source statements distinct from your inference.
4. **Navigate existing synthesis using the workspace's own router/index/schema.** Read only pages relevant to the new material.
5. **Respect authority boundaries.** Do not treat Zettelkasten notes, PARA resources, curated source evidence, or other human-maintained material as writable synthesis unless the workspace explicitly permits it.
6. **Compare claim by claim:**
   - **supports** — strengthens existing knowledge;
   - **extends** — adds compatible detail;
   - **contradicts** — preserve both positions with source/time context rather than silently replacing one;
   - **creates** — introduces knowledge not represented yet.
7. **Update maintained synthesis** according to the workspace's existing page format and provenance policy. Prefer updating canonical pages over creating isolated source summaries when the knowledge belongs on existing pages.
8. **Update navigation/metadata/history** only where the workspace already defines those mechanisms or the user explicitly adopted a CCA-hardened/profile contract.
9. **Verify references.** Every newly introduced source-backed assertion that the workspace promises to trace must resolve to the underlying evidence.
10. **Report** what changed, what evidence was added, which contradictions or uncertainties remain, and which files contain the durable result.

## Hybrid Workspace source curation

When the active target is the current CCA Hybrid Workspace Profile (v3):

```text
explicitly curated (human)  -> reference.curated   -> knowledge.reference
preserved raw, any acquirer -> reference.collected -> knowledge.reference
unclassified incoming       -> context.capture
agent-authored synthesis    -> knowledge.durable
external deliverable        -> output.artifact
finite research effort      -> work.project
```

The left side describes admission/workflow; the right side preserves semantic roles. `reference.curated` and `reference.collected` are classifications, not competing knowledge roles.

For `reference.curated`:

- agents may read but may not add or mutate source objects;
- human admission is required.

For `reference.collected`:

- an agent/tool may deposit a **new** child source object;
- required acquisition provenance and content identity/hash must be written with the deposit;
- an existing collected source may not be edited, replaced, renamed, relocated, or deleted by normal agent operation;
- human review does not move/reclassify the source as curated; review is metadata;
- presence means evidence, not truth, quality, or endorsement.

Never place source objects loose under the parent `knowledge.reference` binding. Resolve the most-specific child binding before filesystem mutation.

## Optional CCA-hardened profile

If another workspace explicitly uses CCA's hardened knowledge-bundle conventions rather than the Hybrid Workspace Profile, its conventions may include:

- durable evidence under `raw/`;
- maintained synthesis under `wiki/`;
- `wiki/index.md` as navigation;
- `log.md` as a maintenance chronicle;
- frontmatter/lifecycle/provenance metadata.

Follow those conventions when present. Do not describe them as universal LLM Wiki requirements or silently substitute the Hybrid profile's source classes.

## Batch ingestion

When processing multiple sources:

- integrate sources one at a time so provenance and contradiction effects remain attributable;
- avoid combining unrelated sources into a single synthetic "source" record;
- update shared synthesis incrementally;
- preserve each source's admission classification independently;
- deliver one consolidated final report unless the workspace requires per-source review gates.

## Production rules

- Never rewrite durable evidence as though it were synthesis.
- Never resolve a contradiction by silently deleting the older claim.
- Never fabricate provenance, source locations, dates, hashes, review state, or confidence.
- Preserve the knowledge base's native schema unless an explicit migration/hardening change was requested.
- Preserve human/method-overlay write boundaries unless an explicit maintenance contract says otherwise.
- Source provenance/admission, content authorship, and semantic role remain separate.
- Implementation files referenced by this skill remain skill-local.
- Cross-skill coordination uses semantic skill names, never sibling filesystem paths.
- Load only the pages required to integrate the source correctly.
