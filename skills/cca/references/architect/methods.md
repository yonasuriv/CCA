# Method overlays and composition

Load this reference when the architecture request involves PARA, Zettelkasten, Building a Second Brain (BASB/CODE), second brains, PKM, LLM Wiki, ICM, or a hybrid of those methods.

These methods are not interchangeable. Preserve the concern each one owns.

| Method | Treat it as | Architecture implication |
|---|---|---|
| BASB / CODE | human knowledge-work lifecycle | Capture → Organize → Distill → Express can span several workspace forms; do not force one tree merely to represent the lifecycle. |
| PARA | action-oriented organization | Projects / Areas / Resources / Archives may organize an outer workspace while nested projects preserve their own native structure. |
| Zettelkasten | linked idea-development method | Preserve small addressable notes and link semantics. Do not assume every note is agent-maintained or safe to rewrite. |
| LLM Wiki | persistent maintained-synthesis pattern | Discover the wiki's own schema first. CCA hardening may add stronger routing/provenance but is not native LLM Wiki structure. |
| ICM / MWP | staged workflow/context architecture | A native ICM root remains governed by the complete current ICM profile even when nested inside PARA or another outer organization. |
| CCA | composition/interoperability layer | Route across boundaries without flattening them into a universal schema. |

## Core composition rule

**Nest boundaries; do not merge schemas just because they coexist.**

An outer method may organize where a nested workspace lives, but it must not silently redefine the nested workspace's native semantics.

### Two layers: outer method vs ICM skeleton

Keep these concerns separate on every build:

| Layer | Question | Adapts to the user? | Examples |
|---|---|---|---|
| **Outer organization** | Where does this kind of thing live? | **Yes** — use their method when they have one | PARA, Zettelkasten, Eisenhower matrix, GTD, BASB shelves, custom domains |
| **ICM skeleton (walkability)** | How does a cold agent operate? | **No** — same roles every time | L0 entry + role map, L1 router, L2 folder contracts, factory vs product, live stamps, declared status |

- Prefer the **user's named method** for outer shelves when they state one.
- Under deferred trust ("I don't know / do what's best"), pick the **smallest clear split** that fits the intent (PARA is a common default, not a requirement).
- Always apply the **ICM skeleton** to whatever shelves you create (`../core/spec.md` §2.1). Agents must not invent walk behavior; they may only customize names via the L0 map.
- Do **not** mint a CCA lint profile for Eisenhower, GTD, or similar — they remain overlays.

Example:

```text
workspace/
├── Projects/                         # PARA organization
│   └── client-acme/
│       ├── assessment/              # native ICM boundary
│       │   ├── CLAUDE.md            # native ICM entry semantics preserved
│       │   ├── AGENTS.md            # optional portable counterpart when useful
│       │   ├── CONTEXT.md
│       │   └── stages/
│       └── code/                    # ordinary coding repository
│           ├── AGENTS.md
│           ├── src/
│           └── tests/
├── Areas/
├── Resources/
│   └── knowledge/
│       ├── zettelkasten/            # linked idea notes
│       └── llm-wiki/                # maintained synthesis
└── Archives/
```

If `assessment/` claims native ICM compatibility, validate it as a native ICM root. Do not rename or reorganize its internals to make the outer PARA tree look more uniform.

## BASB / CODE

Use BASB as a lifecycle lens, not a compatibility profile:

- **Capture** → source material, inboxes, existing capture tooling.
- **Organize** → PARA or another existing organization system.
- **Distill** → Zettelkasten notes, maintained LLM Wiki synthesis, or other durable knowledge work.
- **Express** → coding work, documentation, client deliverables, ICM pipelines, or other production workflows.

Do not claim CCA implements BASB. CCA composes with it.

## PARA

Preserve the actionability distinction:

- **Projects** — current efforts with an outcome/finish condition.
- **Areas** — ongoing responsibilities.
- **Resources** — topics/material that may support future work.
- **Archives** — inactive material from the other categories.

Do not encode these obvious paths into CCA metadata merely to restate the filesystem. Add explicit metadata only when a real workspace-specific fact cannot be inferred safely.

PARA can wrap coding repos, native ICM roots, LLM Wikis, or ordinary folders. The nested boundary keeps its own semantics.

## Zettelkasten

Treat zettels as addressable linked ideas whose authority is defined by the workspace, not by CCA.

Before changing notes, determine whether they are:

- human-authored source/reference material;
- jointly maintained synthesis;
- generated working notes;
- immutable evidence.

Do not silently convert a Zettelkasten into an agent-written wiki. A common hybrid keeps Zettelkasten for idea-level thinking and LLM Wiki for maintained higher-level synthesis.

## LLM Wiki + Zettelkasten

A useful relationship is:

```text
zettelkasten/
    context-engineering.md
    context-routing.md
    progressive-disclosure.md

wiki/
    concepts/context-architecture.md
    comparisons/context-methods.md
    synthesis/current-context-thesis.md
```

The exact tree is not normative. The important distinction is idea-level linked notes versus maintained synthesis.

## Personal hybrid (projects + notes + research + maintained wiki)

Load this section when the request combines **coding/outcome work** with **notes/research/second-brain** and wants **durable evidence separate from growing synthesis** (the LLM Wiki idea), including when the user defers details ("do what's best").

### Epistemic layers (do not conflate)

These are different authorities even when nested under an outer method's shelves (PARA Resources, a custom "Research/" domain, an Eisenhower quadrant, etc.):

| Layer | Role | Mutability | Default owner |
|---|---|---|---|
| Capture / inbox | Frictionless landing before taxonomy | Mutable | Anyone |
| Sources / raw | Evidence from the world | **Write-once** after deposit | Capture process |
| Notes / zettel | The human's own thinking | Mutable | Human (agents cite; rewrite only if asked) |
| Wiki | Current maintained understanding | Mutable / rewritable | Human + agent |
| Projects / outcomes | Outcome-bound building | Project-local | Project / human |

**Organizational shelves** (whatever outer method) answer *where something lives*. **Epistemic layers** answer *what kind of knowledge it is*. Keep both; do not file personal notes as immutable evidence, and do not treat wiki synthesis as a source dump.

### Defaults when the user trusts you

Use the smallest hybrid that preserves the epistemic layers above **and** remains cold-agent isomorphic with ICM (`../core/spec.md` §2.1): same walkable skeleton, optional different names via the L0 map.

1. **Outer organization (adapts)** — If the user names a method (PARA, Zettelkasten-first, Eisenhower, GTD, custom domains), use **that** for shelves. If they defer, use PARA (`Projects/`, `Areas/`, `Resources/`, `Archives/`) or another equally clear actionability split — PARA is a convenience default, not a CCA requirement. Coding projects stay normal repositories; do not force wiki schema into project internals.
2. **Nested knowledge bundle** — under the method's knowledge/resources home (or equivalent): `inbox/` (optional but preferred), immutable `raw/` (or `sources/raw/`), human `notes/` or `zettelkasten/`, growing `wiki/` with `index.md` + `log.md`.
3. **Portable agent entry** — canonical `AGENTS.md`; harness files (`CLAUDE.md`, …) are one-line pointers, not second hand-maintained copies. Record the outer method name in the skeleton map / directory map so cold agents know the shelf logic without assuming PARA.
4. **ICM skeleton map in L0** — always write the role→path table (defaults `CONTEXT.md` for L1/L2). Cold agents must not guess names. Skeleton roles do **not** change when the outer method changes.
5. **One folder contract per working folder** — every working shelf and knowledge subfolder that an agent may operate in gets a local contract file at the **mapped L2 name** (default `CONTEXT.md`). Copy shape from `assets/templates/folder-context.md`: Purpose, Inputs, Process, Outputs, Human check. Do **not** substitute a nested `AGENTS.md` for that contract unless the L0 map explicitly sets L2 = that nested `AGENTS.md` **and** that file contains the same sections.
6. **Root L1 router** — one workspace router (default `CONTEXT.md`) that only routes tasks to folders/procedures; no payload.
7. **Repeating knowledge jobs** — capture / deposit / weave / query are either covered by the folder contracts of the folders that own them, or by short procedure contracts the L1 router points at — always with exact paths and Human check. Numbered `01_` stages are optional (YAGNI); missing contracts are not.
8. **Factory vs product** — live stamps under the mapped L3 path (knowledge `_templates/` plus stubs for new units the outer method creates). Product = wiki/notes/project trees / run outputs. Skills are not the only stamp home.
9. **Status without memory** — root router (or L0) declares how a cold agent answers “what’s the state?” Do not leave status as “only pipeline `output/`” when there is no pipeline.
10. **Immutability is operational, not slogan** — never rewrite deposited raw files; correct via **supersession**. For CCA-hardened bundles, install checkable integrity (`bin/capture`, `bin/verify` or equivalent).
11. **Seed a worked example** — one real source → wiki citation (+ note if notes were requested) + log line.
12. **Self-describing** — daily use works from workspace files alone; no mandatory external skill names.
13. **YAGNI** — no numeric ID factories, multi-stage ingest pipelines, or vector DBs until repeated use proves the need.
14. **Human day-to-day guide** — `README.md` when the user will continue in a new session.

Outer path names follow the user's method. Cold-agent behaviors (entry, map, per-folder contracts, factory vs product, stamps, declared status) are normative.

### Rejected collapses

- Projects-only (brain trapped in repos) or wiki-only (no home for code)
- Notes filed only under immutable sources
- Prose "never rewrite raw" with no supersession rule and no way to detect edits
- Scaffold with zero example source→wiki citation
- Requiring "use CCA ingest mode" / invented skill names for basic capture
- Shelf `AGENTS.md` / README **without** a mapped L2 folder contract (cold agent cannot find Inputs / Process / Outputs / Human check)
- Templates only inside installed skills, not live in the workspace
- Calling the hybrid ICM-skeleton-compatible when a cold agent must guess filenames or invent missing contracts
- Forcing PARA (or any single overlay) when the user named a different outer method
- Treating Eisenhower / GTD / custom domains as CCA native lint profiles

## Architecture questions to resolve

When these methods appear together, determine:

1. What is the outer organizational boundary (user-named method, or deferred-trust default)?
2. Which nested directories claim native compatibility with an upstream convention?
3. Which material is source/reference versus agent-maintained synthesis?
4. Which workflows are sequential enough to benefit from ICM or ICM-derived stages (and thus may need setup/questionnaire)?
5. Which methods are merely human organizational overlays and therefore should not become lint profiles?
6. What is the smallest routing layer needed for a fresh agent to understand the relationships?
7. Is the ICM skeleton (map, folder contracts, factory, status) applied to the actual shelves, not only to a PARA-shaped example?

## Skill coordination

For compound architecture work, `cca` in `architect` mode chooses the form and may then semantically delegate focused operations:

- use `cca` in `scaffold` mode to add the selected minimal structure;
- use `cca` in `sync` mode to reconcile existing routing/navigation after approved structural changes;
- use `cca` in `ingest` mode when evidence must be integrated into maintained synthesis;
- use `cca` in `query` mode when maintained knowledge must be queried/synthesized;
- use `cca` in `lint` mode to validate the profiles actually claimed.

Do not reference sibling skill paths or implementation resources. The semantic mode name is the coordination boundary.

Direct requests still route directly to the focused mode. `cca` in `architect` mode is not required for a request that is already clearly a lint, ingest, query, sync, or scaffold operation.
