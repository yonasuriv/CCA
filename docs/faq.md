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

The complete profile specification/tooling/tests live inside `skills/cca/` so installation remains portable.

## Are `_state/`, `_runtime/`, `00-wiki/`, `10-inbox/`, or `CONTEXT.md` mandatory CCA paths?

No.

They are default bindings in the Hybrid Workspace Profile. The semantic keys are the stable identity. The profile explicitly treats binding changes as non-breaking where its frozen contract allows them.

## Why does the Hybrid Profile have `WORKSPACE.yaml` if CCA avoids manifests?

Because that optional profile needs a machine-readable bootstrap for stable semantic keys, configurable bindings, policy/authority, generation, and deterministic validation.

CCA core does not require every workspace to have `WORKSPACE.yaml`. The manifest is a profile-specific mechanism, not a universal CCA rule.

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

Use `architect` for compound architecture/profile/boundary decisions. A clearly scoped lint, sync, ingest, query, or scaffold request should route directly to that mode.

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

Use `lint` against the claims the boundary actually makes:

- upstream-native ICM → current ICM acceptance;
- ICM-derived → borrowed constructs only;
- LLM Wiki → its maintained-knowledge behavior;
- CCA-conformant → adopted CCA semantics;
- Hybrid Profile → bundled frozen-v1 audit plus generated-artifact check;
- human methods → preservation findings, not invented certification.

Then use the CCA fresh-agent walk test where applicable. The walk test supplements stricter upstream/profile validation; it never replaces it.

## Can CCA evolve without becoming another competing methodology?

That is a core design constraint.

CCA MUST adapt/version mappings when supported upstream changes affect compatibility, SHOULD converge toward materially better upstream solutions, and MUST NOT preserve inferior CCA-specific conventions merely because it introduced them first.

CCA remains valuable only while it makes distinct systems easier for humans and agents to operate together without taking ownership away from them.
