# Method overlays and composition

Load this reference when the architecture request involves PARA, Zettelkasten, Building a Second Brain (BASB/CODE), second brains, PKM, LLM Wiki, ICM, or a hybrid of those methods.

These methods are not interchangeable. Preserve the concern each one owns.

| Method | Treat it as | Architecture implication |
|---|---|---|
| BASB / CODE | human knowledge-work lifecycle | Capture → Organize → Distill → Express can span several workspace forms; do not force one tree merely to represent the lifecycle. |
| PARA | action-oriented organization | Projects / Areas / Resources / Archives may organize an outer workspace while nested projects preserve their own native structure. |
| Zettelkasten | linked idea-development method | Preserve small addressable notes and link semantics. Do not assume every note is agent-maintained or safe to rewrite. |
| LLM Wiki | persistent maintained-synthesis pattern | Discover the wiki's own schema first. CCA hardening may add stronger routing/provenance but is not an LLM Wiki requirement. |
| ICM / MWP | staged workflow/context methodology | A native ICM root remains governed by the complete current ICM profile even when nested inside PARA or another outer organization. |
| CCA | composition/interoperability layer | Route across boundaries without flattening them into a universal schema. |

## Core composition rule

**Nest boundaries; do not merge schemas just because they coexist.**

An outer method may organize where a nested workspace lives, but it must not silently redefine the nested workspace's native semantics.

## Organization and navigation are separate decisions

Keep these questions independent:

| Concern | Question | Examples |
|---|---|---|
| **Organization** | Where does this kind of thing live for the human/workflow? | PARA, Zettelkasten, GTD, BASB/CODE, custom domains |
| **Epistemic role** | What kind of information is this? | capture, preserved evidence, human note, maintained synthesis, operational state |
| **Navigation** | How does a consumer discover the relevant boundary/context? | native upstream router, existing index, scoped AGENTS.md, ICM-derived contract, profile-defined router, ordinary filesystem structure |

A human method does not determine epistemic authority. A navigation pattern does not determine the organizational shelf.

For navigation:

- preserve a native upstream's own bootstrap and routing exactly when that upstream is claimed;
- use ICM-derived local contracts/progressive disclosure when the actual workflow benefits from them;
- use the CCA Hybrid Workspace Profile's declared router/bindings only when that optional profile is selected or already present;
- for an ordinary/custom CCA-compatible workspace, add only the smallest routing surface required to resolve the relevant boundary and semantic role;
- do not require a root router, per-folder contract, factory/product split, live stamps, or status protocol merely because CCA can model those concepts.

Example:

```text
workspace/
├── Projects/                         # PARA organization
│   └── client-acme/
│       ├── assessment/              # upstream-native ICM boundary
│       │   ├── CLAUDE.md
│       │   ├── CONTEXT.md
│       │   └── stages/
│       └── code/                    # ordinary coding repository
│           ├── AGENTS.md
│           ├── src/
│           └── tests/
├── Areas/
├── Resources/
│   └── knowledge/
│       ├── zettelkasten/            # linked human ideas
│       └── llm-wiki/                # maintained synthesis
└── Archives/
```

If `assessment/` claims upstream-native ICM, validate it as native ICM. Do not rename or reorganize its internals to make the outer PARA tree uniform.

## BASB / CODE

Use BASB as a lifecycle lens, not a compatibility profile:

- **Capture** → source material, inboxes, existing capture tooling.
- **Organize** → PARA or another existing organization system.
- **Distill** → human notes, Zettelkasten, maintained synthesis, or other durable knowledge work.
- **Express** → code, documentation, client deliverables, pipelines, or other production workflows.

Do not claim CCA implements BASB. CCA composes with it.

## PARA

Preserve the actionability distinction:

- **Projects** — current efforts with an outcome/finish condition.
- **Areas** — ongoing responsibilities.
- **Resources** — topics/material that may support future work.
- **Archives** — inactive material from the other categories.

These are organizational shelves, not epistemic types. A PARA Resource can contain an external source, a human note, maintained synthesis, a dataset, or another nested boundary. Do not equate `Resources` with `knowledge.reference`.

Do not serialize obvious PARA paths into CCA metadata merely to restate the filesystem. Add explicit metadata only when a semantic/authority/binding fact cannot be inferred safely or a selected profile requires it.

## Zettelkasten

Treat zettels as addressable linked ideas whose authority is defined by the workspace, not by CCA.

Before changing notes, determine whether they are:

- human-authored thinking;
- jointly maintained synthesis;
- generated working notes;
- preserved evidence.

Do not silently convert a Zettelkasten into an agent-written wiki.

## LLM Wiki + Zettelkasten

A useful relationship can be:

```text
zettelkasten/
    context-engineering.md
    context-routing.md

wiki/
    concepts/context-architecture.md
    synthesis/current-context-thesis.md
```

The tree is illustrative only. The important distinction is idea-level linked notes versus maintained synthesis and the local authority that governs each.

## Personal hybrid: projects + notes + research + maintained knowledge

Load this section when the user wants one filesystem-native environment containing outcome work, raw/captured material, personal thinking, maintained synthesis, operational state, and reusable capabilities.

### Epistemic roles are independent of shelves

| Role | Meaning | Typical authority |
|---|---|---|
| Capture / inbox | low-friction unclassified landing | shared/ingest policy |
| Preserved source/reference | evidence that should retain provenance | profile/local source policy |
| Human note / zettel | the human's own thinking | human unless explicitly shared |
| Maintained synthesis | current reconciled understanding | shared/maintainer policy |
| Project/output | outcome-bound work | project/local policy |
| Operational state | tasks/current execution state | local state policy |

Do not infer authority from the folder brand. Organizational shelves answer **where it lives**; epistemic roles answer **what it is**.

### Architecture procedure

1. Preserve the user's existing organization when it works. If the user defers, choose the smallest understandable organization; PARA is one possible default, never a CCA requirement.
2. Identify nested native/upstream boundaries before adding CCA routing.
3. Separate capture, evidence, human notes, maintained synthesis, projects/outcomes, and operational state where their authority/lifecycle actually differs.
4. Decide whether ICM is needed:
   - use upstream-native ICM for a workflow that should be ICM;
   - use specific ICM-derived patterns only when staged/local contracts improve the workflow;
   - do not apply ICM-shaped contracts to unrelated shelves by default.
5. Consider the optional CCA Hybrid Workspace Profile when its reviewed frozen-v1 semantics match the requested personal/team hybrid. If it does not fit, compose a smaller custom CCA-compatible target rather than mutating the profile into a new hidden standard.
6. Give large collections bounded local navigation when scale requires it. Prefer boundary-local routers/catalogs/indexes over one giant root manifest.
7. Keep derived indexes rebuildable and non-authoritative.
8. Preserve immutable/preserved material through explicit supersession or local provenance rules where needed; do not rely on folder names as enforcement.
9. Seed examples only when they materially improve onboarding/pattern discovery.
10. Add stronger retrieval infrastructure only after local routing/search becomes insufficient.

### Rejected collapses

- Projects-only when durable cross-project knowledge is required.
- Wiki-only when real project/application boundaries matter.
- PARA `Resources` treated as synonymous with preserved raw evidence.
- Human notes silently reclassified as agent-maintained synthesis.
- Generic CCA compatibility made dependent on ICM Layer 0/1/2 files.
- Per-folder contracts added where ordinary filesystem structure already provides sufficient navigation.
- A single root manifest required to enumerate every document or nested project.
- Templates/skills made authoritative for knowledge that must remain usable without the installed CCA skill.
- Calling an ICM-derived target upstream-native ICM.
- Inventing native conformance profiles for PARA, Zettelkasten, BASB/CODE, GTD, or similar human methods.

## Architecture questions to resolve

When methods appear together, determine:

1. What is the outer organizational boundary, if any?
2. Which nested directories claim upstream-native compatibility?
3. Which material is capture, preserved evidence, human thinking, maintained synthesis, project work, and operational state?
4. Which workflows actually benefit from native ICM or selected ICM-derived patterns?
5. Which human methods are overlays rather than machine-facing profiles?
6. What is the smallest routing surface a fresh consumer needs before targeted search?
7. Where should local routing/indexing appear as the workspace grows?

## Skill coordination

For compound architecture work, `cca` in `architect` mode chooses the form and may then semantically delegate focused operations:

- use `scaffold` to materialize an approved structure;
- use `sync` to reconcile routing/bindings after approved changes;
- use `ingest` to integrate evidence into maintained synthesis;
- use `query` to navigate maintained knowledge/evidence;
- use `lint` to validate the claims actually made.

Do not reference sibling skill paths or repository-global implementation resources. The semantic mode name is the coordination boundary.

Direct requests still route directly to the focused mode. `architect` is not required for a request already clearly matching another mode.
