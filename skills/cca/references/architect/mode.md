# Architect mode

Design the smallest filesystem/context architecture that makes the work navigable, durable, human-understandable, and agent-agnostic.

Read `../core/spec.md` and `core.md` before designing or auditing. Read `forms.md` only when choosing a workspace form. Read `workspace-builder.md` when the request is to create, initialize, set up, report status for, or materially rebuild a workspace. Read `methods.md` when the request involves PARA, Zettelkasten, BASB/CODE, second brains, PKM, LLM Wiki/ICM composition, or another hybrid knowledge-work architecture. Read `hybrid-workspace.md` only when the optional CCA Hybrid Workspace Profile is selected or detected. Read `../core/adapters.md` only when a harness-specific adapter is needed.

## Role in the CCA skill

`architect` is the primary entry point for compound architecture requests: audit or review workspace context architecture, decide what the workspace should become, which upstreams/methods/profiles apply, where boundaries sit, which semantic roles are required, how those roles bind locally, and which focused mode should execute next.

It is not a mandatory gateway for already-clear operations. Direct claim lint, ingest, query, sync, or scaffold requests should use those modes directly. A request to "audit this repo/workspace using CCA" is not equivalent to claim linting unless the user explicitly limits the request to compatibility/conformance validation.

## Trigger routing

- **audit / review workspace context architecture** → use Audit mode; preserve the user-requested target boundary, inspect its meaningful nested boundaries, evaluate architecture quality, then delegate claim checks to `lint` where useful.
- **create / build / initialize workspace** → load `workspace-builder.md` and select/preserve the applicable form/profile.
- **personal/team hybrid profile** → load `workspace-builder.md`, `methods.md` only if method composition matters, then `hybrid-workspace.md` when the profile fits.
- **setup** for upstream-native ICM → load `workspace-builder.md` plus `native-icm-setup.md` and preserve current upstream onboarding semantics.
- **status** for upstream-native ICM → load `workspace-builder.md` and preserve current upstream status behavior.
- **restructure / migrate** → use Restructure mode; do not conflate migration with scaffold.

When another CCA capability is needed, delegate semantically by mode name, e.g. `Use scaffold mode to implement the approved structure` or `Use lint mode to validate the claims`. Never depend on removed sibling skill directories.

## Compatibility gate

Before changing structure, identify the current boundary, upstream-native claims, CCA claims, and method overlays.

- **Upstream-native ICM**: preserve the complete applicable current ICM profile and current upstream acceptance authority. A valid native ICM workspace is already CCA-compatible; do not structurally migrate it merely to make CCA understand it.
- **ICM-derived**: another target may borrow ICM navigation/stage/contract/handoff patterns without claiming full ICM.
- **LLM Wiki compatibility**: discover the implementation's own schema and maintenance conventions first.
- **Ordinary project**: preserve application layout unless restructuring is explicitly requested.
- **CCA-compatible**: CCA can resolve the target without structural migration or semantic replacement.
- **CCA-conformant**: preserve the normative CCA semantics the target intentionally adopted.
- **Profile-conformant**: preserve the named CCA-owned profile contract independently from other claims.
- **CCA Hybrid Workspace Profile**: optional CCA-owned profile; not a new mode and not native ICM. The current bundled schema is v2, preserving the frozen-v1 baseline and adding only `reference.curated`/`reference.collected` admission classifications. Stable semantic roles remain identity; bindings remain configurable where the current profile permits them.
- **Method overlays**: PARA, Zettelkasten, BASB/CODE, delivery methods, and similar systems remain their own authorities unless an explicit machine-facing contract says otherwise.

Compatibility is interoperability, not ownership and not an architecture-quality certification. Do not label an upstream workspace CCA-conformant merely because CCA can resolve it.

## Semantic design primitive

For CCA-owned/interoperable architecture decisions, reason through:

```text
boundary + semantic role -> binding
```

Then separately determine authority, mutability, lifecycle/status, provenance, classification, and indexing/visibility semantics where the selected contract requires them.

Do not use a concrete default path as the role identity. If a governing upstream makes a filename/path normative for native conformance, preserve that upstream requirement.

For the Hybrid Workspace Profile specifically, source admission classification is orthogonal to semantic role:

```text
reference.curated   ─┐
                     ├─> knowledge.reference
reference.collected ─┘
```

`reference.*` records how preserved evidence entered the corpus; it does not create a second reference ontology.

## Audit mode

Use this mode when the user asks to audit, review, assess, optimize, harden, or evaluate a repository/workspace's context, routing, knowledge, or navigation architecture. The goal is to determine whether the **requested audit boundary** is efficiently understandable and operable by humans and agents, not merely whether a local contract can be linted successfully.

### Scope and coverage

1. Resolve the requested audit boundary from the user's target before descending into nested repositories, modules, submodules, stages, or knowledge systems.
2. Discover meaningful nested boundaries and existing authority/routing surfaces. Do not silently substitute an active child task, convenient submodule, or already-known component for the requested parent target.
3. Record which boundaries were inspected, which were excluded, and which remain unresolved.
4. Inspect child boundaries at their own scope, preserving native/profile/method authority.
5. **A child-boundary PASS MUST NOT close a parent/workspace audit.**
6. If material portions of the requested boundary remain uninspected, report the parent audit as partial/incomplete and leave completion open.

### Architecture-quality evaluation

Evaluate the actual target with evidence. Do not invent a profile or require files merely to make the audit scoreable. Cover the dimensions that materially apply:

- **boundary discovery** — can a fresh consumer identify the workspace and meaningful nested scopes?
- **root orientation** — can a human or agent entering at the requested root understand where to start and what governs the workspace?
- **intent routing** — can representative intents resolve to the correct boundary and semantic role without guessing?
- **context selectivity** — can consumers load minimum sufficient context rather than broad, repeated discovery?
- **authority clarity** — are instruction, governance, canonical-source, and mutation authorities distinguishable?
- **canonicality** — are substantive rules/facts owned once rather than duplicated across registries, adapters, routers, or docs?
- **human navigation** — can a person locate important context and understand the structure without tribal knowledge?
- **agent navigation** — can a fresh agent orient and act from durable workspace files without prior chat memory?
- **boundary portability / outward coupling** — if a nested boundary is independently addressable, can it orient locally when detached, or does required routing escape through parent-only paths or assumptions?
- **search dependency** — how often does successful routing still require broad filesystem search, excessive hops, or path guessing?
- **drift resistance** — are stale/broken routes, bindings, generated views, or duplicate authorities detectable?
- **scalability** — can local/federated routing grow without requiring one global manifest or ever-expanding root context?

Do not fabricate numeric precision. Use qualitative status/severity plus concrete evidence unless the active workspace/profile already defines a scoring rubric.

### Audit procedure

1. Identify existing human and agent entry points before adding new ones.
2. Identify existing registries, routers, indexes, manifests, contracts, and instruction scopes; reuse canonical surfaces where possible instead of creating a second routing authority.
3. Map representative high-value routes through `boundary + semantic role -> binding` and record authority/ownership where ambiguity matters.
4. For independently addressable repositories, submodules, packages, plugins, or workspaces, inspect required routing for **escaping relative** references, parent-only routers/configuration needed merely to orient, and assumptions about an **exact embedding path**. Distinguish intentional declared parent coupling from incidental filesystem coupling.
5. Test common root-to-leaf intents from the requested audit boundary, not from a preselected child directory.
6. Where practical, test independently addressable child boundaries from their own root as if detached from the parent; do not require full application execution when only context/routing portability is under review.
7. Run both human-oriented and fresh-agent navigation checks where practical.
8. Separate architecture-quality findings from compatibility/conformance findings.
9. Use `lint` for the claim-validation portion; a clean lint result is evidence about claims, not proof that the architecture is efficient.
10. Identify the smallest hardening/remediation that would materially improve routing, context efficiency, authority clarity, portability, or drift resistance.
11. If remediation is authorized, delegate focused implementation to `scaffold` and/or `sync`, then repeat the affected routes and claim checks.
12. Close the audit only when requested-boundary coverage is complete or explicitly narrowed by the user.

### Audit report

```text
# CCA architecture audit — [requested target]

Requested audit boundary: [target]
Inspected boundaries: [list]
Excluded/unresolved boundaries: [list | none]
Coverage: COMPLETE | PARTIAL | BLOCKED

## Existing routing/authority model
[entry points, routers/registries, semantic bindings, native/profile/method boundaries]

## Architecture-quality findings
[boundary discovery, root orientation, intent routing, context selectivity,
authority clarity, canonicality, human navigation, agent navigation,
boundary portability/outward coupling, search dependency, drift resistance,
scalability — only where material]

## Claim lint summary
[upstream/CCA/profile claims, explicitly separate from architecture quality]

## Hardening/remediation
[smallest changes that materially improve the target]

## Verification
[root-to-leaf human/agent walks, detached-boundary checks where applicable,
validator/CI evidence, remaining limits]

Completion: DONE | PARTIAL | BLOCKED
```

A `DONE` audit means the requested boundary was actually covered. It MUST NOT mean only that one inspected child passed its local checks.

## Build mode

1. Extract the human goal, workflow, knowledge boundaries, organizational methods, and authority lines already implied by the request.
2. Detect and preserve existing upstream-native boundaries before designing CCA additions.
3. Choose the smallest useful form: ordinary repo, native upstream workspace, maintained knowledge system, custom CCA-compatible composition, or named CCA profile.
4. If building a complete workspace, load `workspace-builder.md` and use its discovery → mapping → scaffolding → onboarding-if-needed → validation flow.
5. If human knowledge-work methods are involved, load `methods.md` and preserve them as independent methods/overlays rather than silently turning them into CCA semantics.
6. Decide explicitly whether ICM usage is upstream-native or merely ICM-derived/adopted navigation behavior.
7. Identify nested native boundaries. Outer organization may place them but does not rewrite their internals merely for consistency.
8. If the CCA Hybrid Workspace Profile fits the requested hybrid, prefer the reviewed profile instead of inventing an equivalent custom schema; load `hybrid-workspace.md` and keep its implementation under the existing skill-local asset boundary.
9. If the Hybrid profile does **not** fit, compose a custom CCA-compatible target rather than mutating frozen profile semantics ad hoc.
10. Implement only what the selected form/profile actually needs. Use scaffold mode for focused materialization.
11. Add adapters only when needed and only after reading `../core/adapters.md`.
12. Validate upstream-native claims first, CCA/profile claims next, and the fresh-agent portability walk last.

## Restructure mode

1. **Audit** the actual target and read enough content to classify confidently.
2. **Preserve upstream semantics** before proposing CCA hardening.
3. **Preserve method boundaries** before proposing taxonomy changes.
4. **Map semantics before paths**: current boundary/role/binding → intended boundary/role/binding.
5. **Propose a migration map**: current path → function/authority → destination → action → compatibility impact.
6. **Stop for explicit approval** before moves, merges, renames, or deletions unless the user already authorized direct remediation.
7. Apply only the approved map and preserve content unless deletion was explicitly approved.
8. Use sync mode after structural/binding changes.
9. Validate upstream-native claims, then intentional CCA/profile conformance.

## Hybrid profile target rule

When Architect selects the Hybrid Workspace Profile, it chooses the target and bindings; it does not make the installed skill directory the workspace.

Materialization is delegated to scaffold using the bundled implementation:

```bash
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --init
```

The target MUST be explicitly resolved outside the installed package. The implementation's own templates/scripts/tests remain within `skills/cca/` for portability.

## Invariants

- Human augmentation is the objective; automation is a means.
- One fact, one canonical home.
- Route before broad search.
- Routing files point; they do not become knowledge dumps.
- Load minimum sufficient context for the active operation.
- Preserve the requested audit boundary until coverage is complete or the user explicitly narrows it.
- Independently addressable boundaries remain locally orientable when detached unless parent dependence is intentional and declared.
- Nest boundaries; do not merge schemas merely because several methods coexist.
- Stable semantic roles are distinct from concrete bindings and orthogonal classifications.
- Bindings may move where their governing contract permits; consumers follow the semantic role.
- Upstream-native systems retain their upstream authority.
- Human methods remain independent rather than being absorbed into CCA.
- Cross-mode coordination uses semantic mode names, not sibling filesystem paths.
- `skills/cca/` remains the portable CCA distribution boundary.
- Never invent a competing convention where a proven upstream already solves the problem better.
- Never use CCA compatibility to bypass an upstream repository's own contribution/process rules.
- Never substitute the CCA walk test for stricter upstream/profile acceptance.

## Walk test

After applicable upstream/profile validation, simulate a fresh consumer with no prior chat memory:

1. **Orient**: identify the boundary, authority/profile/methods, and routed context.
2. **Act**: perform one representative operation using only the files/tools exposed by the target.
3. **Report**: state what changed, what was produced, what remains, and what is ambiguous.

For architecture audits, start the walk at the requested audit boundary. Starting inside a child boundary proves only that child's navigation. For independently addressable child boundaries, also perform a detached-orientation walk from that child root when practical.

If required operating knowledge exists only in chat history or someone's head, improve the durable target rather than explaining around the gap.

## Advisor consultation boundary

Architecture owns workspace structure/composition; advisor owns engineering judgment. When a structural choice depends on process/security/autonomy/model trade-offs, lazily read only the relevant file under `../advisor/`. Do not copy advisor material into architect references and do not turn an advisory methodology into a CCA structural profile.