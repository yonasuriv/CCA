# FAQ

## What is CCA?

CCA is an interoperability layer for filesystem-native agent context. It defines shared semantics and maintenance practices that let agents work across ICM staged workspaces, LLM Wiki-style persistent knowledge bases, ordinary coding repositories, PKM/second-brain systems, and hybrids without requiring a proprietary runtime.

It prefers existing standards, upstream conventions, and useful human methodologies over inventing competing ones.

## What is CCA not?

CCA is not an agent runtime, orchestration framework, vector database, model protocol, replacement for MCP, replacement for ICM, replacement for LLM Wiki, replacement for PARA, replacement for Zettelkasten, or replacement for Building a Second Brain.

It does not provide real-time multi-agent message passing. Tight-loop coordination still belongs in runtimes/frameworks built for it.

## How do BASB, PARA, Zettelkasten, LLM Wiki, and ICM fit together?

They solve different layers of the problem:

- **BASB/CODE** describes a human knowledge-work lifecycle: Capture, Organize, Distill, Express.
- **PARA** organizes material by actionability: Projects, Areas, Resources, Archives.
- **Zettelkasten** develops knowledge through small addressable linked ideas.
- **LLM Wiki** maintains persistent agent-generated synthesis over durable sources.
- **ICM/MWP** structures sequential agent work through stages, routing, contracts, and handoffs.
- **CCA** defines how those boundaries can coexist without one silently redefining another.

See [`method-composition.md`](method-composition.md).

## Are PARA, Zettelkasten, and BASB CCA compatibility profiles?

No. CCA treats them as **method overlays**.

They can influence organization, knowledge development, and human workflow, but CCA does not invent a universal native conformance test for them. A workspace may be described as PARA-organized, Zettelkasten-style, or BASB-guided while its nested ICM/LLM Wiki/coding boundaries retain their own semantics.

## Can I use PARA with CCA?

Yes. PARA can organize the outer workspace while nested projects preserve their own structure.

For example, a native ICM workspace can live under `Projects/client-acme/assessment/`, an ordinary coding repo can live under another Project, and an LLM Wiki can live under `Resources/knowledge/`. CCA should not rewrite those nested boundaries merely to make the PARA tree more uniform.

## Can I use Zettelkasten with CCA?

Yes. CCA can treat Zettelkasten notes as linked knowledge/reference material without forcing them into an LLM Wiki schema.

Do not assume agents may rewrite every zettel. The local workspace decides whether notes are human-authored source/reference material, jointly maintained synthesis, working notes, or something else.

A common hybrid keeps Zettelkasten for idea-level thinking and LLM Wiki for maintained higher-level synthesis.

## Can I use Building a Second Brain with CCA?

Yes. BASB/CODE can remain the human lifecycle across the workspace. CCA does not claim to implement BASB; it can route the files, knowledge, and workflows that participate in Capture, Organize, Distill, and Express.

PARA often fits the Organize step; Zettelkasten or LLM Wiki may support Distill; coding projects, documentation, client deliverables, or ICM workflows may support Express.

## Can all of them coexist in one workspace?

Yes. The key rule is **nest boundaries; do not merge schemas merely because they coexist**.

An outer PARA structure may contain coding projects, client work, an LLM Wiki, Zettelkasten notes, and a native ICM root. Each nested native boundary remains valid for the consumer that owns it, while a CCA-aware agent can understand how the pieces relate.

## Does a second brain need ICM?

No. Use ICM only where a repeatable sequential workflow benefits from explicit stages, selective routing, and handoffs. A second brain can be purely knowledge-oriented, or it can contain one or more ICM/ICM-derived workflows for production tasks.

## Is CCA just ICM with AGENTS.md?

No. ICM is the primary upstream for CCA's staged workflow architecture: layered routing, stage contracts, selective loading, one-way references, canonical sources, human-editable handoffs, onboarding, and quality gates.

CCA adds an interoperability layer around those ideas, including agent-agnostic root guidance, portable skills, LLM Wiki compatibility, method-overlay composition, and cross-form maintenance. Where CCA claims native ICM compatibility, it preserves the complete applicable current ICM profile rather than only copying its stage-folder syntax.

## Does CCA conflict with ICM's workspace-builder?

It should not.

The upstream workspace-builder is itself an ICM workspace whose output is a validated ICM workspace. CCA treats upstream `_core/CONVENTIONS.md` as the canonical ICM semantic authority and the workspace-builder's final validation stage as the practical acceptance checklist for generated ICM workspaces.

CCA can provide a different user interaction for architecture/scaffolding, but if the result claims **native ICM compatibility**, it should pass the same applicable upstream acceptance surface.

## Can CCA replace workspace-builder when contributing a workspace to the ICM repository?

Not when the current ICM contribution policy requires `workspace-builder`.

Compatibility and contribution policy are different layers. CCA may independently create or maintain a native-compatible ICM workspace for use elsewhere, provided the complete applicable ICM profile passes. But if that workspace is being submitted to the upstream ICM repository, follow that repository's current contribution requirements — including using `workspace-builder` when required — rather than treating CCA compatibility as an exemption.

## Is there an ICM `ACCEPTANCE.md` file CCA follows?

Not in the current upstream repository. The effective acceptance surface is distributed across the canonical `_core/CONVENTIONS.md`, the workspace-builder's `05-validation` stage, and repository-level contribution checks.

CCA's own fresh-agent walk test is supplemental. It does not replace those ICM checks.

## What does “ICM-derived” mean?

A workspace is **ICM-derived** when it borrows useful ICM constructs — for example `stages/01-name/`, stage `CONTEXT.md` contracts, selective routing, one-way dependencies, or output handoffs — without implementing the complete native ICM workspace profile.

This distinction lets ordinary coding repositories reuse good ICM patterns without falsely claiming full ICM interchangeability.

## Is CCA just an implementation of LLM Wiki?

No. LLM Wiki is intentionally an idea pattern, not a rigid filesystem specification. CCA can provide one hardened implementation profile, but must not present its own page taxonomy, frontmatter, logging syntax, or folder choices as requirements of LLM Wiki itself.

## Can I use CCA with Obsidian?

Yes. CCA uses ordinary files, primarily Markdown, so an Obsidian vault can also be a CCA workspace or contain a CCA-compatible knowledge area.

Keep Obsidian-specific metadata and plugins optional. Agents should still be able to navigate the workspace through plain files and links without requiring Obsidian to be running.

## Can I use CCA in VS Code?

Yes. CCA has no editor dependency. VS Code, Cursor, Zed, Vim, Obsidian, a terminal, or any other editor that preserves normal files can be used.

Agent-specific integration belongs in thin adapters or the agent's own configuration, not in duplicated copies of workspace rules.

## What if I already have a coding project?

Do not reorganize the project around CCA by default. Add the smallest routing layer that helps agents understand the existing repository.

Typically that means a useful root `AGENTS.md`, optionally a small `CONTEXT.md` router, and only those stable reference/configuration files that are actually needed. Add pipeline stages or a wiki only if the work benefits from them.

If you add ICM-style stages without implementing the complete ICM profile, call them ICM-derived rather than describing the whole project as native ICM-compatible.

## Does every CCA workspace need `CONTEXT.md`?

No for native compatibility; yes only when a workspace intentionally adopts a CCA/ICM-style routing layer that needs it.

An existing LLM Wiki can remain native-compatible without being forced into an ICM pipeline shape. An ordinary coding repo may need only `AGENTS.md`.

## Does every CCA workspace need a wiki?

No. Pipelines, coding repositories, record libraries, PARA-organized environments, and other filesystem-native workspaces can use CCA semantics without persistent wiki synthesis.

## Does every CCA workspace need stages?

No. Stages are appropriate for sequential workflows with explicit handoffs. Do not add them to knowledge accumulation or simple coding work just to satisfy a folder template.

## Can CCA work with Claude Code, Codex, Gemini, Cursor, Copilot, or other agents?

Yes, provided the agent can read the workspace files. `AGENTS.md` is the portable root convention CCA prefers where supported. Tool-specific files should be thin adapters only when a harness needs them.

Do not assume every harness implements identical instruction precedence. Native harness behavior remains authoritative; CCA adapters should route into shared canonical files rather than copy rules.

## Why `AGENTS.md`?

Because it is an existing cross-agent convention rather than a CCA-specific filename. The AGENTS.md standard also supports nested files, where the nearest applicable instructions take precedence for a subproject.

## Why keep `CLAUDE.md` at all?

For compatibility with tools and ICM workspaces that already use it. In a CCA-hardened workspace, it can remain the native ICM root or act as a thin adapter to shared portable guidance depending on the workspace's compatibility goal.

CCA must not break native ICM behavior merely to make `AGENTS.md` look canonical.

## Is `AGENTS.md` always authoritative over `CLAUDE.md`?

Not universally. Harness-native precedence is determined by the harness. CCA may define an internal authority policy for a workspace, but it cannot override how an external tool discovers instructions.

For portability, avoid contradictory rules across root files. Prefer one canonical body of guidance and thin adapters/includes where the tool supports them.

## Can I use nested `AGENTS.md` files?

Yes. This is part of the AGENTS.md convention and is useful in monorepos or repositories with independently governed subprojects. The closest applicable `AGENTS.md` should contain only the instructions that differ or become more specific for that subtree.

## Are `raw/`, `wiki/`, `index.md`, and `log.md` mandatory?

Only for the specific CCA hardened knowledge-bundle profile that chooses those conventions. They are not universal requirements for all CCA-compatible workspaces, and CCA must not claim they are mandatory parts of Karpathy's LLM Wiki idea.

## Is YAML frontmatter mandatory on wiki pages?

No for LLM Wiki native compatibility. CCA may recommend frontmatter for lifecycle, provenance, and machine-readable maintenance, but that is an optional hardening convention unless a particular workspace adopts it.

CCA also does not require a giant workspace manifest merely to map obvious paths such as Projects, Areas, Resources, Archives, stages, or wiki folders. Infer ordinary filesystem semantics when safe; declare only facts that genuinely need explicit metadata.

## Are the six CCA skills supposed to be installed separately?

They are **focused Agent Skill packages intended to be distributed as the CCA skill suite**. The package split exists for precise triggering and progressive disclosure, not because each capability is meant to be an unrelated standalone product.

Package portability means implementation file references remain inside the skill package and installation paths do not become architecture. A skill may coordinate another installed CCA capability by semantic name, for example `Use cca-lint`, without reaching into the sibling skill's directory.

## Is `cca-architect` the router for every CCA operation?

No. It is the primary entry point for compound architecture/design requests: choosing forms, combining methods, deciding boundaries, or planning restructuring.

A request that is already clearly an ingest, lint, query, sync, or scaffold operation should route directly to the focused skill. `cca-architect` may semantically delegate those capabilities when they are part of a larger architecture workflow.

## Why not one giant `cca` or `cca-architect` skill?

Because Agent Skills progressive disclosure works better when focused capabilities have precise trigger descriptions and lazily loaded resources. A monolithic skill would load unrelated procedures and make routing less precise.

CCA unifies the **methodology and capability model**, not every operation into one `SKILL.md`.

## Why not create `cca-para`, `cca-zettelkasten`, or `cca-second-brain` skills?

Because those names describe methodologies/forms, not distinct executable operations. Their composition knowledge belongs as a lazy-loaded architecture reference behind `cca-architect` unless a future operation becomes distinct enough to justify its own skill.

## Does CCA require Git?

No. Git is strongly compatible with CCA because plain files make history, review, diffing, and rollback cheap, but the workspace model does not require a specific VCS.

## Does CCA require MCP?

No. MCP is complementary. CCA structures durable filesystem context; MCP can expose tools and external context. Either can exist without the other.

## Does CCA require a database or vector store?

No. The baseline is filesystem-native. Search indexes, graph databases, embeddings, or databases may be added when scale warrants them, but they must remain optional infrastructure rather than prerequisites for understanding the workspace.

## How does CCA handle multi-agent work?

For asynchronous or loose coordination, agents can hand off through durable files. For real-time collaboration where agents must communicate dynamically in tight loops, use message-passing/orchestration infrastructure. CCA can still provide the shared durable context beneath that runtime.

## How do I know whether a workspace is healthy?

Run `cca-lint` using the correct profile.

For native ICM, that means the complete applicable current ICM profile and workspace-builder-equivalent acceptance surface. For ICM-derived patterns, validate only what was actually adopted. For LLM Wiki, validate the implementation's maintained-knowledge behavior without forcing CCA's optional schema. Method overlays may produce preservation findings but are not invented native profiles.

Then perform the CCA walk test: a fresh agent should be able to orient, act, and report state from the files alone. The lint result must distinguish upstream compatibility findings from optional CCA hardening and method-preservation findings.

## Can CCA evolve without breaking old workspaces?

That is a core design constraint. CCA should track upstream ICM, LLM Wiki, AGENTS.md, Agent Skills, and relevant adjacent standards. Changes should prefer additive aliases, optional hardening, boundary preservation, and migration guidance over breaking reinterpretations of upstream conventions or user methodologies.

See [`standards.md`](standards.md) for the upstream-change rule and [`method-composition.md`](method-composition.md) for the method-overlay model.
