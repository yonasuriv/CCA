---
name: cca
description: Use to design or restructure context systems, audit workspace context/routing architecture, create or set up native or hybrid workspaces, scaffold portable routing, synchronize navigation, ingest or query maintained knowledge, validate CCA/ICM/LLM-Wiki compatibility, or advise on engineering judgment, software engineering principle/framework/methodology/process trade-offs, and security, autonomy, model, and context decisions. Supports existing code repositories, human knowledge systems, ICM, LLM Wiki, PARA, Zettelkasten, BASB/CODE, delivery methods, and hybrid workspaces without replacing their native authorities. Trigger whenever a request touches how context, knowledge, or navigation is structured for humans and agents together, even when the user never names CCA. Do not use for ordinary implementation, coding, editing, or project work when no context, knowledge, compatibility, routing, or advisory operation is involved.
metadata:
  version: "1.3.0"
---

# CCA

Convergent Context Architecture (CCA) is an evolving, agent-agnostic interoperability architecture for filesystem-native AI context. It helps humans and AI agents understand, navigate, and operate across workspaces, projects, and bodies of knowledge by defining stable semantic roles, scoped boundaries, and configurable bindings that preserve meaning even when their concrete paths or implementations change.

CCA aims to bridge human knowledge work and agentic work without forcing existing systems into a new competing convention, by building on open standards, ecosystem conventions, established methodologies, protocols and frameworks, and based on software-engineering principles and fundamentals.

Its goal is to make automation easier in service of augmenting human capabilities while improving efficiency, reducing technical debt and unnecessary complexity, and lowering compute, context, usage, and operational costs.

> **Automation is the means; augmenting human capabilities is the goal.**

This is one installable skill with seven lazily loaded modes. Select the smallest mode that directly matches the request, then load only that mode and the references it names.

If the task is ordinary implementation, coding, editing, testing, or project work and does not require CCA context architecture, maintained-knowledge operations, compatibility validation, routing, or advisory judgment, do not enter `architect` or another CCA mode. Continue with the task using the workspace's existing authority and stop loading CCA references.

## Modes

| Mode | Use for | Load first |
|---|---|---|
| `architect` | workspace architecture audit/review, design, create/setup/status, restructure, boundary/profile selection, hybrid composition | `references/architect/mode.md` |
| `scaffold` | add minimal routing/context without restructuring | `references/operations/scaffold.md` |
| `sync` | reconcile routing/navigation with the filesystem | `references/operations/sync.md` |
| `ingest` | integrate evidence into maintained knowledge | `references/operations/ingest.md` |
| `query` | navigate/synthesize maintained knowledge | `references/operations/query.md` |
| `lint` | validate claimed compatibility/conformance profiles | `references/operations/lint.md` |
| `advise` | engineering judgment, process/method trade-offs, security/autonomy/model/context decisions | `references/advisor/mode.md` |

Do not load every mode or reference. Progressive disclosure is part of the architecture.

A workspace architecture audit or review is compound architecture work: use `architect` to preserve the requested boundary, inspect nested boundaries, evaluate navigation/context quality, and decide whether remediation is warranted. Lint is claim validation; use `lint` directly only when the user is asking whether specific upstream/CCA/profile claims pass, or delegate to it from Architect for the claim-validation portion of a broader audit. A child-boundary lint pass never completes a parent/workspace architecture audit.

For workspace creation or material rebuild, Architect lazily loads `references/architect/workspace-builder.md`. For path-changing restructures/migrations, Architect additionally loads `references/architect/reference-integrity.md` before the approval/execution boundary. For the optional CCA Hybrid Workspace Profile, Architect additionally loads `references/architect/hybrid-workspace.md`; its complete reviewed reference implementation is bundled under `assets/hybrid-workspace/`. This profile is not an eighth mode.

For native ICM (Interpretable Context Methodology), the builder performs the inherited discovery, mapping, scaffolding, questionnaire, validation/repair, `setup`, `status`, and current restructure-safety behaviors while current upstream ICM remains the acceptance authority.

## Shared authority

Before making a claim about CCA semantics, compatibility, composition, contract identity, or versioned conformance, use only the skill-local canonical material needed for that claim under `references/core/`:

- `spec.md` — normative CCA semantics and operation model;
- `versioning.md` — normative CCA contract identity, SemVer evolution, and version-versus-source-provenance rules;
- `compatibility.md` — upstream/CCA/profile compatibility vocabulary and preservation rules;
- `method-composition.md` — how methods coexist without being absorbed;
- `adapters.md` — harness-specific interoperability guidance;
- `icm-inheritance.md` — provenance map for preserving the current applicable ICM capability floor without redefining ICM.

Do not preload the whole core set. Load a core reference when the current operation actually depends on its authority. Any operation that creates, validates, migrates, or reports a CCA compatibility/conformance/profile identity MUST load `references/core/versioning.md`.

For native ICM work, `icm-inheritance.md` is a compatibility map only. The current upstream ICM authority and acceptance surface still win if CCA documentation drifts.

These files are inside the installable skill so runtime behavior never depends on repository-global specification files that may not exist after installation.

## Contract version

The installed CCA skill and normative CCA interoperability contract share one SemVer identity. The canonical contract version is `metadata.version` in this file; current version is **1.3.0**. Consumer CCA identity is version-based. Repository/source revisions are optional provenance and never substitute for the CCA contract version; see `references/core/versioning.md`.

## Portable distribution boundary

`skills/cca/` is CCA's self-contained installable distribution boundary.

Any CCA-owned reference, schema, template, executable, fixture, or validation resource required to understand, resolve, generate, operate, validate, or maintain behavior advertised by this skill MUST be available inside this package. Repository-global documentation may elaborate, illustrate, research, or publish CCA but MUST NOT be the sole authority for runtime-required or normative semantics.

Bundled tooling MUST operate on an explicitly resolved target workspace. The skill/package directory is capability implementation, never an implicit workspace target.

## Domain boundaries

Keep these domains separate:

- `references/core/` owns normative CCA semantics shared by all modes plus compatibility/provenance maps for inherited upstream behavior.
- `references/advisor/` owns engineering judgment and methodology priors. Its seven references remain independent and are never folded into architect references.
- `references/architect/` owns workspace forms, builder/onboarding behavior, boundaries, structural composition, restructure reference integrity, optional profile definitions, and migration design.
- `references/operations/` owns focused operational procedures.
- `assets/` owns skill-local templates, executable/reference tooling, and other portable implementation resources already used by the current package topology.

Architect mode may consult advisor references when a structural decision requires engineering/process judgment. That is lazy consultation, not ownership transfer or duplication.

## Routing rules

1. Detect the existing boundary/workspace/profile before proposing structure.
2. Resolve CCA operations through `boundary + semantic role → binding`; semantic identity MUST NOT depend on a default path where the governing contract allows bindings to move.
3. Preserve upstream-native authorities and declared method boundaries.
4. Prefer the smallest intervention that solves the routing/context problem.
5. Existing code repositories keep their application structure unless restructuring is explicitly requested.
6. PARA, Zettelkasten, BASB/CODE, Scrum, Kanban, XP, DevOps, SAFe, LeSS, DA, and similar methods remain their own authorities; CCA maps relationships and routing rather than reimplementing them.
7. A valid native ICM workspace is CCA-compatible without structural migration; native ICM remains governed and validated by current upstream ICM. CCA may extend/harden it but must not weaken or replace it.
8. Native ICM create/setup/status requests use Architect's `workspace-builder.md`; they do not require the upstream workspace-builder checkout at runtime, although upstream remains the semantic/acceptance authority.
9. The optional Hybrid Workspace Profile is CCA-owned and profile-conformant only when its bundled contract passes. Its default bindings are not semantic identities.
10. Do not create structure merely because a template exists.
11. For destructive or path-changing restructuring, load `references/architect/reference-integrity.md`, verify referrers and destination safety, then surface the evidence-bearing migration map before moves, merges, renames, archives, or deletions unless the user has explicitly authorized direct remediation.
12. Use harness-native adapter files only where needed; portable guidance should remain canonical in the workspace's chosen portable authority.
13. When uncertainty crosses a hard-stop boundary, use `references/advisor/escalation-triggers.md`.
14. Preserve the user-requested audit boundary: inspecting or validating a nested child does not silently narrow a parent/workspace audit.
15. An independently addressable child boundary SHOULD remain locally orientable when detached unless parent dependence is intentional and declared; do not make required routing depend on incidental parent filesystem placement.

## Upstream-change rule

CCA MUST update or explicitly version/pin a compatibility mapping when a supported upstream changes in a way that affects a compatibility claim. CCA SHOULD converge toward an upstream approach that demonstrates a materially better solution to the same problem, provided it does not violate CCA's core principles. CCA MUST NOT preserve an inferior CCA-specific convention merely because CCA introduced it first.

## Core rule

Preserve existing standards, frameworks, methodologies, protocols, and knowledge systems as distinct authorities. Make them interoperable through explicit semantics, scopes, mappings, routing, precedence, and compatibility boundaries.

Always advise; never enforce or assume. When a decision is left to you, first determine the user's intent, then choose the path most likely to produce the best possible outcome.

For reference metadata and upstream attribution, see [CITATION](CITATION.cff).
