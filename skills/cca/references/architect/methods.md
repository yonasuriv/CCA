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

## Architecture questions to resolve

When these methods appear together, determine:

1. What is the outer organizational boundary?
2. Which nested directories claim native compatibility with an upstream convention?
3. Which material is source/reference versus agent-maintained synthesis?
4. Which workflows are sequential enough to benefit from ICM or ICM-derived stages?
5. Which methods are merely human organizational overlays and therefore should not become lint profiles?
6. What is the smallest routing layer needed for a fresh agent to understand the relationships?

## Skill coordination

For compound architecture work, `cca` in `architect` mode chooses the form and may then semantically delegate focused operations:

- use `cca` in `scaffold` mode to add the selected minimal structure;
- use `cca` in `sync` mode to reconcile existing routing/navigation after approved structural changes;
- use `cca` in `ingest` mode when evidence must be integrated into maintained synthesis;
- use `cca` in `query` mode when maintained knowledge must be queried/synthesized;
- use `cca` in `lint` mode to validate the profiles actually claimed.

Do not reference sibling skill paths or implementation resources. The semantic mode name is the coordination boundary.

Direct requests still route directly to the focused mode. `cca` in `architect` mode is not required for a request that is already clearly a lint, ingest, query, sync, or scaffold operation.
