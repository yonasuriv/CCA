# Convergent Context Architecture

CCA (Convergent Context Architecture) is an evolving, agent-agnostic interoperability layer for filesystem-native AI context. Its purpose is not to replace existing knowledge systems, software-development methods, agent conventions, or workflow architectures. It makes their boundaries explicit enough that humans and AI agents can navigate and use them together without forcing everything into a new competing convention.

The core rule is **convergence over invention**: preserve an existing authority when it already solves the problem, add the smallest missing compatibility layer, and keep automation in service of human augmentation.

## The problem

AI systems increasingly act on ordinary repositories. Instructions, source code, task state, stage contracts, research, maintained knowledge, configuration, and intermediate artifacts all live as files. That is useful because files are inspectable, versionable, and portable, but files do not explain their own semantics. One agent may treat a note as source evidence while another treats it as writable synthesis. A delivery framework may own task state while a repository contains a second, stale representation. A native workflow may be nested inside a broader personal-knowledge system whose rules apply only outside that boundary.

At the same time, useful methods already exist at different layers. PARA organizes actionable material. BASB/CODE describes a human knowledge-work lifecycle. Zettelkasten develops linked ideas. LLM Wiki maintains persistent synthesis. ICM/MWP provides staged routing and durable handoffs. AGENTS.md and Agent Skills provide portable agent guidance and progressively disclosed capabilities. Scrum, Kanban, XP, DevOps, SAFe, LeSS, DA, and other approaches govern process at different organizational altitudes.

The problem is not that one of these should win. The problem is that their interfaces are usually implicit.

## What CCA adds

CCA defines enough shared semantics for an agent to answer five questions before it acts:

1. What workspace or boundary am I in?
2. What authority already governs it?
3. What context is required for this task?
4. What operation should be performed?
5. What may be added or changed without breaking native semantics?

The answer can differ by subtree. A PARA `Projects/` directory can contain an ordinary code repository and a native ICM assessment workspace. A Zettelkasten can remain human-governed while an adjacent LLM Wiki is agent-maintained synthesis. Jira can remain the Scrum backlog authority while Git remains the code/history authority. CCA connects those boundaries; it does not flatten them.

## One skill, seven modes

CCA is distributed as one self-contained Agent Skill. Its compact `SKILL.md` routes requests to seven lazily loaded modes:

- `architect` for workspace structure, forms, boundaries, and method composition;
- `scaffold` for minimal in-place routing/context additions;
- `sync` for reconciling navigation with the filesystem;
- `ingest` for integrating evidence into maintained knowledge;
- `query` for querying synthesis and escalating to evidence;
- `lint` for profile-aware compatibility/conformance validation;
- `advise` for engineering and methodology judgment.

The package contains four deliberately separate reference domains. `core/` owns normative CCA semantics. `architect/` owns workspace structure. `operations/` owns focused procedures. `advisor/` owns an independent judgment corpus covering engineering principles, frameworks and methodologies, adversarial security reasoning, agent-system design, context engineering, AI/ML practice, and escalation triggers.

Architect may consult advisor when a structural decision requires judgment, but it does not absorb advisor content. That separation matters: knowing how Scrum works is not the same concern as deciding whether a repository needs a `CONTEXT.md`.

## Existing code repositories

CCA starts with preservation. It reads the repository's existing instruction files, source tree, tests, architecture docs, package/build configuration, and external authorities before proposing structure.

If the repository is already navigable, CCA should not add a pipeline, wiki, `_config/`, PARA tree, or large manifest. A root or nested `AGENTS.md` may be useful when scoped portable guidance is missing. In some repositories the correct result is no structural change at all.

This is an important difference between a compatibility architecture and a preferred template: the latter asks how to instantiate its shape; the former first asks whether a new shape is warranted.

## Second brains and knowledge systems

CCA treats common knowledge methods according to the concern they own:

- **PARA**: action-oriented outer organization;
- **BASB/CODE**: Capture → Organize → Distill → Express as a lifecycle lens;
- **Zettelkasten**: addressable linked idea development;
- **LLM Wiki**: persistent maintained synthesis;
- **ICM/MWP**: staged context routing and handoffs where sequential work benefits from them.

These can coexist without becoming a single CCA taxonomy. A human-authored Zettelkasten is not silently converted into an agent-written wiki. A nested native ICM root continues to obey ICM. PARA can decide where a project lives without redefining the project internally.

## Delivery methods such as Scrum

CCA does not implement Scrum with `sprints/`, `standups/`, or `retrospectives/` directories. Scrum remains a team/process framework. If Jira holds the Product and Sprint Backlogs, CCA routes agents to Jira rather than duplicating that state into Markdown. If Git and CI/CD are authoritative for implementation and delivery state, those authorities remain in place.

A bounded activity inside the delivery process can still use another suitable form. A repeatable security review, for example, may benefit from an ICM-derived pipeline with explicit collect → test → review → report handoffs. That does not turn ICM into project management or Scrum into context architecture.

CCA's advisor corpus exists for exactly this type of decision: choose the smallest process or practice that addresses the actual constraint, and keep it at the correct scope.

## Workspace forms

CCA architecture currently recognizes six useful forms:

1. **Pipeline** for staged sequential work;
2. **Umbrella** for routing across several independent/nested boundaries;
3. **Record Library** for repeated records sharing a template/schema and declared lifecycle/catalog authority;
4. **Knowledge Bundle** for durable evidence plus maintained synthesis;
5. **Context Map** for organizational/process/information relationships;
6. **System Map** for source-backed objects, processes, effects, and change-impact reasoning across mutable code/files/vaults.

They are choices, not a maturity ladder. A form should be added only when it makes the workspace easier to orient, operate, validate, or maintain.

## Compatibility before hardening

CCA separates native compatibility from optional improvements. A native ICM workspace must satisfy the applicable current ICM semantics. An LLM Wiki keeps its implementation's own schema and maintenance behavior. CCA hardening—portable routing, provenance, additional catalogs, or other conventions—comes after native behavior is understood and preserved.

This also prevents partial adoption from being mislabeled. A code repository that borrows ICM-style stage contracts is **ICM-derived**; it is not automatically a native ICM workspace.

## Is CCA better than ICM?

Not as an unqualified statement.

For a native ICM task, CCA should be no worse than current upstream ICM. Diverging while claiming native compatibility would be a CCA bug. CCA is intended to add value when the problem extends beyond ICM's scope: existing repositories that should not be transformed into pipelines, second brains, maintained knowledge systems, delivery methods, nested authorities, System Maps, and cross-agent portability.

Whether it actually produces better behavior must be measured. The repository therefore defines an A/B evaluation protocol using fresh isolated agents, identical prompts/fixtures/budgets, actual filesystem outputs, deterministic invariants, blind qualitative judging, and context/tool/intervention measurements. Simulated predictions of what an agent would probably do are not accepted as behavioral evidence.

The defensible claim today is therefore narrower: **CCA is designed as a broader interoperability and compatibility architecture; superiority over an upstream method must be demonstrated per scenario.**

## Human augmentation

The long-term reason for this architecture is not folder cleanliness. It is human agency.

Models, runtimes, vendors, and interfaces will change. Human knowledge and working systems should not become unreadable every time the execution layer changes. Durable files, explicit authority, progressive context loading, and compatibility boundaries make it possible to replace the execution plane without surrendering the context plane.

Automation is infrastructure. The objective is to increase what people can understand and accomplish while keeping the state that shapes automated behavior inspectable, editable, and portable.
