# FAQ

This is explanatory. Normative answers live inside the installable skill, primarily [`../skills/cca/references/core/spec.md`](../skills/cca/references/core/spec.md) and [`../skills/cca/references/core/compatibility.md`](../skills/cca/references/core/compatibility.md).

## What is CCA?

Convergent Context Architecture (CCA) is an evolving, agent-agnostic interoperability architecture for filesystem-native AI context. It helps humans and agents understand, navigate, and operate across heterogeneous workspaces by using stable semantic roles, scoped boundaries, and configurable bindings.

Its objective is human augmentation:

> **Automation is the means; augmenting human capabilities is the goal.**

## What is CCA not?

CCA is not an agent runtime, message bus, orchestration framework, vector database, MCP replacement, universal directory tree, or replacement for ICM, LLM Wiki, AGENTS.md, Agent Skills, PARA, Zettelkasten, BASB, Scrum, or other methods/standards.

## What is the core resolution model?

```text
boundary + semantic role -> binding
```

The semantic role is stable meaning. The binding is the concrete local path/implementation and may change where the governing contract permits it.

## What do compatibility terms mean?

- **Upstream-native** — passes an upstream's own current rules.
- **CCA-compatible** — CCA can resolve/operate without structural migration or semantic replacement.
- **CCA-conformant** — explicitly adopts normative CCA interoperability semantics.
- **Profile-conformant** — passes a named optional CCA-owned profile.
- **CCA-hardened** — optional CCA capabilities added without invalidating native semantics.
- **ICM-derived** — selected ICM patterns used without claiming full native ICM.

These are independent claims, not a maturity ladder.

## Does a clean CCA lint mean the workspace has good context architecture?

No.

`lint` validates the claims and contracts that actually apply to the inspected boundary. It can tell you that an upstream-native, CCA-compatible/conformant, or named-profile claim passes without proving that the broader workspace is efficient to navigate.

For an audit/review of a repository or workspace's context architecture, use Architect Audit mode. That audit preserves the requested parent boundary, checks meaningful nested boundaries, evaluates human and agent navigation, context selectivity, authority clarity, canonicality, search dependency, drift resistance, and scalability, then uses `lint` only for the claim-validation portion.

A child-boundary pass does not make the parent audit done. If the requested workspace contains material boundaries that were not inspected, the result is partial/incomplete rather than a parent PASS.

## Is a valid native ICM workspace CCA-compatible?

Yes.

A valid native ICM workspace is CCA-compatible because CCA can resolve its native semantics without structural migration through the boundary/role/binding model.

That does not make ICM CCA-owned and does not require the workspace to become CCA-conformant. Current upstream ICM remains authoritative for native ICM semantics and acceptance.

## Is CCA just ICM with AGENTS.md?

No.

ICM provides a strong filesystem-native methodology for routing, progressive disclosure, contracts, handoffs, and human-reviewed workflow. CCA deliberately uses ICM where those abstractions already solve the problem well, instead of creating competing equivalents.

CCA's additional concern is interoperability across ICM, maintained knowledge, ordinary repos, human methods, different tools/runtimes, nested boundaries, and configurable bindings.

## Does CCA replace ICM's workspace-builder?

No as an upstream authority.

CCA may provide an interoperable builder experience for its own operations, but a result claiming upstream-native ICM must pass current ICM's own applicable acceptance surface. If the upstream repository requires its workspace-builder for contribution, that contribution rule still applies.

## What does ICM-derived mean?

A target is ICM-derived when it borrows selected ICM ideas such as staged folders, local contracts, selective routing, one-way dependencies, progressive disclosure, or output handoffs without satisfying/claiming the complete native ICM profile.

## Does every CCA-compatible workspace need ICM stages or `CONTEXT.md`?

No.

CCA compatibility is not “looks like ICM.” Native ICM keeps its required filenames/structure. Other systems keep their own structure. A CCA-owned profile may adopt ICM-proven navigation behavior without pretending to be native ICM.

## How do BASB, PARA, Zettelkasten, LLM Wiki, and ICM fit together?

They solve different concerns:

- BASB/CODE — human knowledge-work lifecycle;
- PARA — action-oriented organization;
- Zettelkasten — linked idea development;
- LLM Wiki — persistent maintained synthesis;
- ICM/MWP — filesystem-native agent workflow/context methodology;
- CCA — interoperability across those boundaries.

CCA does not merge them into one taxonomy. See [`method-composition.md`](method-composition.md).

## Are PARA, Zettelkasten, BASB/CODE, Scrum, etc. CCA profiles?

Not by default. They remain independent methods. CCA may map their scopes/artifacts but does not invent structural conformance tests for them.

## Can they coexist in one workspace?

Yes. The rule is:

> **Nest boundaries; do not merge schemas merely because they coexist.**

An outer organizational method can contain normal repos, native ICM boundaries, human notes, and maintained wikis without rewriting each nested system.

## What is the CCA Hybrid Workspace Profile?

It is an optional CCA-owned profile for a recurring personal/team environment containing projects, preserved sources, human notes/research, maintained knowledge, tasks/state, reusable capabilities, and human + agent operation.

It is not a new mode, not native ICM, and not a universal CCA tree.

The current bundled schema is **v3**; v2 remains supported unchanged. Both preserve the frozen-v1 semantic/policy baseline. V2 added two classifications beneath `knowledge.reference`; v3 defines them as curation state independent of who acquired the source, makes every generated artifact a declared binding so `WORKSPACE.yaml` is the only fixed root file, and adds optional workspace identity, a state hotset, operating documentation, human/editor asset bindings, and scoped archive manifests.

The complete profile specification/tooling/tests live inside `skills/cca/` so installation remains portable.

## Why are there `curated/` and `collected/` source directories?

To make **curation state** obvious from the filesystem without changing what a reference is.

Default Hybrid bindings are:

```text
20-sources/
├── curated/      # reference.curated
└── collected/    # reference.collected
```

Both resolve to:

```text
semantic.role = knowledge.reference
```

The distinction is:

```text
acquisition != curation state != content authorship != semantic role
```

- `reference.collected` means preserved raw/reference material that has not been explicitly promoted. Any actor may acquire it — a human clipping an article or saving a transcript, an agent, crawler, tool, or integration. New children may be deposited under append/additive semantics; existing collected source objects may not be edited, replaced, renamed, relocated, or deleted. Collected is a legitimate permanent home, not a queue.
- `reference.curated` means deliberately human-admitted, maintained reference, entered by explicit human-authorized promotion or direct human admission. Agents may read but not add or mutate it.
- Every source object carries provenance and verifiable content identity. Markdown captures may keep it in frontmatter with a hash of the body; other files use a `.source.yaml` sidecar; a batch or corpus uses a directory manifest. Folders without a manifest are just containers.
- Review alone never promotes a collected source. Promotion is explicit, human-authorized, and recorded.
- Neither class implies truth, correctness, quality, or endorsement. (Schema v2 targets keep the v2 meaning: curated = human-admitted, collected = automatically acquired.)

An agent downloading an arXiv PDF therefore creates preserved evidence under `reference.collected`; the conclusions the agent writes from it belong to `knowledge.durable`.

## Why not make `collected` a new knowledge role?

Because it answers a different question.

`knowledge.reference` answers **what the material is**: preserved source/evidence.

`reference.curated` / `reference.collected` answers **whether it has been explicitly curated**.

`knowledge.durable` answers what the workspace learned/synthesized from evidence.

`output.artifact` answers what the workspace deliberately produced for delivery/publication.

Research itself is an activity/workflow, normally bounded by `work.project` and task state; it is not another top-level semantic knowledge category.

## Can source files live directly under `20-sources/`?

Not in the Hybrid profile (v2 or v3).

The parent `knowledge.reference` binding is a semantic/source-corpus root. Raw/reference source objects must resolve through `reference.curated` or `reference.collected`. The profile audit rejects loose/unknown source objects directly under the parent binding.

## Does a parent source permission override `curated` or `collected`?

No.

When profile bindings nest, semantic classification composes, but filesystem mutation policy resolves from the **most-specific matching binding**. Parent permissions cannot widen a child policy, and the parent human/read-only policy does not erase the deliberately narrower append/deposit operation allowed by `reference.collected`.

## Are `_state/`, `_runtime/`, `00-wiki/`, `10-inbox/`, `20-sources/`, or `CONTEXT.md` mandatory CCA paths?

No.

They are default bindings in the Hybrid Workspace Profile. The semantic keys are the stable identity. The profile treats binding changes as non-breaking where its evolution contract allows them.

For the source corpus, if `knowledge.reference` moves, its `reference.curated` and `reference.collected` bindings must remain declared nested children so classification/policy resolution stays deterministic.

## Why does the Hybrid Profile have `WORKSPACE.yaml` if CCA avoids manifests?

Because that optional profile needs a machine-readable bootstrap for stable semantic keys, configurable bindings, policy/authority, generation, and deterministic validation.

CCA core does not require every workspace to have `WORKSPACE.yaml`. The manifest is a profile-specific mechanism, not a universal CCA rule.

## Why did the Hybrid schema become v2, then v3?

Because frozen v1 explicitly declared that adding/removing/renaming keys requires a schema-version bump.

Adding `reference.curated` and `reference.collected` while pretending the schema was still v1 would violate the profile's own evolution contract. V2 preserves all 22 original v1 slot semantics and existing policy vocabulary, then adds only the two admission classifications and their provenance/routing contract.

V3 is a further bump for the same reason: it adds keys and a category, changes the meaning of the two reference classes from acquisition actor to curation state, and changes generation/provenance/archive policy. Redefining v2 in place would silently change the meaning of existing v2 workspaces, so v2 stays supported and v3 is opt-in.

## How is the Hybrid Profile created?

Through existing `cca` modes, not a new mode.

`architect` selects/composes the profile, `scaffold` initializes it, `sync` regenerates derived artifacts after authorized changes, and `lint` validates it.

The bundled generator always operates on an explicit target:

```bash
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --init
```

It must never treat the installed skill/tool directory as the workspace target.

## What happens if I rename a Hybrid Profile binding?

Consumers and generated artifacts should follow the semantic key to its new binding.

For example, `context.router` may move from `CONTEXT.md` to `ROUTER.md` in this non-native CCA profile. The generator must then create/check `ROUTER.md`, not continue depending on the old default.

Native ICM is different: if upstream ICM makes `CONTEXT.md` part of native conformance, keep that exact upstream filename while claiming native ICM.

## Why keep the audit/schema/tests inside the skill?

Portability.

If installed behavior depended on repository-global scripts or docs, copying/installing only `skills/cca/` would lose part of CCA's meaning. The shipped skill therefore carries the Hybrid Profile's schema, templates, generator, audit, dependency declaration, and adversarial regression tests.

## Does the Hybrid tool copy its scripts into my target workspace?

No by default.

The scripts remain capability machinery inside the installed CCA skill. They operate on the explicit target. The target receives its own durable workspace/bootstrap/generated files, not a duplicate copy of the implementation merely to make the tooling run.

## Does CCA require PyYAML?

CCA core does not. The current Hybrid Workspace reference implementation uses PyYAML and carries its dependency declaration inside `skills/cca/assets/hybrid-workspace/requirements.txt`.

That dependency belongs to the optional implementation, not the CCA interoperability model itself.

## Is CCA one skill or seven skills?

One skill.

Install `skills/cca/`. It contains seven lazily loaded modes:

`architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`, `advise`.

Progressive disclosure is achieved through skill-local references/assets/scripts. Do not install or reference removed `cca-architect`, `cca-lint`, etc. sibling packages.

## Is architect the router for every operation?

No.

Use `architect` for compound architecture/profile/boundary decisions, including workspace architecture audits/reviews. A clearly scoped claim lint, sync, ingest, query, or scaffold request should route directly to that mode.

## Can CCA work with Obsidian, VS Code, Cursor, Codex, Claude Code, Gemini, etc.?

Yes where the tool can operate on the filesystem and applicable instruction conventions. CCA semantic identity does not depend on a specific editor, model, vendor, or harness.

Host-specific adapters should remain thin and must not become a second canonical specification.

## Is `AGENTS.md` always authoritative over `CLAUDE.md`?

No universal claim is safe.

CCA uses AGENTS.md as a portable convention where applicable, but harness/upstream authority remains specific to that environment. A native ICM boundary may require its native `CLAUDE.md` behavior. Portable guidance can coexist without falsely overriding it.

## Does CCA require a wiki, Git, MCP, database, or vector store?

No.

All may be useful. None is a universal CCA prerequisite. Filesystem-native durable context remains the baseline interoperability surface.

## How does CCA scale without agents grepping thousands of files?

CCA uses route before search:

```text
boundary
  -> authority/instructions
  -> semantic role
  -> binding/router
  -> local catalog/contract/index
  -> targeted search
  -> optional derived index/cache
  -> broad filesystem search only as fallback
```

Indexes/caches may improve scale, but canonical durable files remain understandable without them.

## How does CCA handle real-time multi-agent collaboration?

It does not replace the runtime/message-passing layer. Tight-loop collaboration belongs in orchestration infrastructure designed for it. CCA can provide the durable shared context beneath that runtime.

## How do I know a workspace is healthy?

First decide what question you are asking.

For claim validity, use `lint` against the claims the boundary actually makes:

- upstream-native ICM → current ICM acceptance;
- ICM-derived → borrowed constructs only;
- LLM Wiki → its maintained-knowledge behavior;
- CCA-conformant → adopted CCA semantics;
- Hybrid Profile → frozen-v1 baseline + declared v2/v3 extension audit (curation/provenance) plus generated-artifact check;
- human methods → preservation findings, not invented certification.

For broader context-architecture health, use Architect Audit mode from the requested workspace root. Then use the CCA fresh-agent walk test where applicable. The walk test supplements stricter upstream/profile validation; it never replaces it.

## Can CCA evolve without becoming another competing methodology?

That is a core design constraint.

CCA MUST adapt/version mappings when supported upstream changes affect compatibility, SHOULD converge toward materially better upstream solutions, and MUST NOT preserve inferior CCA-specific conventions merely because it introduced them first.

CCA remains valuable only while it makes distinct systems easier for humans and agents to operate together without taking ownership away from them.
