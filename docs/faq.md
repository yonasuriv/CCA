# FAQ

## What is CCA?

CCA is an interoperability layer for filesystem-native agent context. It defines shared semantics and maintenance practices that let agents work across ICM-style staged workspaces, LLM Wiki-style persistent knowledge bases, ordinary coding repositories, and hybrids without requiring a proprietary runtime.

It prefers existing standards and upstream conventions over inventing new ones.

## What is CCA not?

CCA is not an agent runtime, orchestration framework, vector database, model protocol, replacement for MCP, replacement for ICM, or replacement for LLM Wiki.

It does not provide real-time multi-agent message passing. Tight-loop coordination still belongs in runtimes/frameworks built for it.

## Is CCA just ICM with AGENTS.md?

No. ICM is the primary upstream for CCA's staged workflow architecture: layered routing, stage contracts, selective loading, one-way references, canonical sources, and human-editable handoffs.

CCA adds an interoperability layer around those ideas, including agent-agnostic root guidance, portable skills, LLM Wiki compatibility, and cross-form maintenance. Where CCA claims ICM compatibility, it should preserve ICM's native shapes rather than fork them.

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

## Does every CCA workspace need `CONTEXT.md`?

No for native compatibility; yes only when a workspace intentionally adopts a CCA/ICM-style routing layer that needs it.

An existing LLM Wiki can remain native-compatible without being forced into an ICM pipeline shape. An ordinary coding repo may need only `AGENTS.md`.

## Does every CCA workspace need a wiki?

No. Pipelines, coding repositories, record libraries, and other filesystem-native workspaces can use CCA semantics without persistent wiki synthesis.

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

## Does CCA require Git?

No. Git is strongly compatible with CCA because plain files make history, review, diffing, and rollback cheap, but the workspace model does not require a specific VCS.

## Does CCA require MCP?

No. MCP is complementary. CCA structures durable filesystem context; MCP can expose tools and external context. Either can exist without the other.

## Does CCA require a database or vector store?

No. The baseline is filesystem-native. Search indexes, graph databases, embeddings, or databases may be added when scale warrants them, but they must remain optional infrastructure rather than prerequisites for understanding the workspace.

## How does CCA handle multi-agent work?

For asynchronous or loose coordination, agents can hand off through durable files. For real-time collaboration where agents must communicate dynamically in tight loops, use message-passing/orchestration infrastructure. CCA can still provide the shared durable context beneath that runtime.

## How do I know whether a workspace is healthy?

Run `cca-lint` using the correct profile and then perform the walk test: a fresh agent should be able to orient, act, and report state from the files alone.

The lint result must distinguish upstream compatibility findings from optional CCA hardening findings.

## Can CCA evolve without breaking old workspaces?

That is a core design constraint. CCA should track upstream ICM, LLM Wiki, AGENTS.md, Agent Skills, and relevant adjacent standards. Changes should prefer additive aliases, optional hardening, and migration guidance over breaking reinterpretations of upstream conventions.

See [`standards.md`](standards.md) for the upstream-change rule.
