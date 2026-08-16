---
name: cca
description: Agent-agnostic interoperability and context architecture for filesystem-native work. Use to design or restructure context systems, create/setup native or hybrid workspaces, scaffold portable routing, synchronize navigation, ingest or query maintained knowledge, validate CCA/ICM/LLM-Wiki compatibility, or advise on engineering and methodology trade-offs. Supports existing code repositories, human knowledge systems, ICM, LLM Wiki, PARA, Zettelkasten, BASB/CODE, delivery methods, and hybrid workspaces without replacing their native authorities. Do not use for ordinary implementation, coding, editing, or project work when no CCA context, knowledge, compatibility, routing, or advisory operation is needed.
compatibility: Filesystem read/write access for mutating modes. No vendor-specific runtime required.
---

# CCA

CCA is one installable skill with seven lazily loaded modes. Select the smallest mode that directly matches the request, then load only that mode and the references it names.

If the task is ordinary implementation, coding, editing, testing, or project work and does not require CCA context architecture, maintained-knowledge operations, compatibility validation, routing, or advisory judgment, do not enter `architect` or another CCA mode. Continue with the task using the workspace's existing authority and stop loading CCA references.

## Modes

| Mode | Use for | Load first |
|---|---|---|
| `architect` | design, create/setup/status, restructure, boundary/profile selection, hybrid composition | `references/architect/mode.md` |
| `scaffold` | add minimal routing/context without restructuring | `references/operations/scaffold.md` |
| `sync` | reconcile routing/navigation with the filesystem | `references/operations/sync.md` |
| `ingest` | integrate evidence into maintained knowledge | `references/operations/ingest.md` |
| `query` | navigate/synthesize maintained knowledge | `references/operations/query.md` |
| `lint` | validate claimed compatibility/conformance profiles | `references/operations/lint.md` |
| `advise` | engineering judgment, process/method trade-offs, security/autonomy/model/context decisions | `references/advisor/mode.md` |

Do not load every mode or reference. Progressive disclosure is part of the architecture.

For workspace creation or material rebuild, Architect lazily loads `references/architect/workspace-builder.md`. For native ICM, that builder performs the inherited discovery, mapping, scaffolding, questionnaire, validation/repair, `setup`, and `status` behaviors while current upstream ICM remains the acceptance authority.

## Shared authority

Before making a claim about CCA semantics, compatibility, or composition, use only the skill-local canonical material needed for that claim under `references/core/`:

- `spec.md` — normative CCA semantics and operation model;
- `compatibility.md` — upstream profiles and preservation rules;
- `method-composition.md` — how methods coexist without being absorbed;
- `adapters.md` — harness-specific interoperability guidance;
- `icm-inheritance.md` — provenance map for preserving the current applicable ICM capability floor without redefining ICM.

Do not preload the whole core set. Load a core reference when the current operation actually depends on its authority.

For native ICM work, `icm-inheritance.md` is a compatibility map only. The current upstream ICM authority and acceptance surface still win if CCA documentation drifts.

These files are inside the installable skill so runtime behavior never depends on repository-global specification files that may not exist after installation.

## Domain boundaries

Keep these domains separate:

- `references/architect/` owns workspace forms, builder/onboarding behavior, boundaries, structural composition, and migration design.
- `references/advisor/` owns engineering judgment and methodology priors. Its seven references remain independent and are never folded into architect references.
- `references/operations/` owns focused operational procedures.
- `references/core/` owns normative CCA semantics shared by all modes plus compatibility/provenance maps for inherited upstream behavior.

Architect mode may consult advisor references when a structural decision requires engineering/process judgment. That is lazy consultation, not ownership transfer or duplication.

## Routing rules

1. Detect the existing workspace/profile before proposing structure.
2. Preserve native authorities and declared method boundaries.
3. Prefer the smallest intervention that solves the routing/context problem.
4. Existing code repositories keep their application structure unless restructuring is explicitly requested.
5. PARA, Zettelkasten, BASB/CODE, Scrum, Kanban, XP, DevOps, SAFe, LeSS, DA, and similar methods remain their own authorities; CCA maps relationships and routing rather than reimplementing them.
6. Native ICM and native LLM Wiki claims are validated against their own applicable semantics before optional CCA hardening. For native ICM, inherited ICM behavior is the compatibility floor: CCA may extend it but must not weaken or replace it.
7. Native ICM create/setup/status requests use Architect's `workspace-builder.md`; they do not require the upstream workspace-builder checkout at runtime, although upstream remains the semantic/acceptance authority.
8. Do not create structure merely because a template exists.
9. For destructive restructuring, surface the migration map before moves, merges, renames, or deletions unless the user has explicitly authorized direct remediation.
10. Use harness-native adapter files only where needed; portable guidance should remain canonical in the workspace's chosen portable authority.
11. When uncertainty crosses a hard-stop boundary, use `references/advisor/escalation-triggers.md`.

## Core rule

**Convergence over invention.** Preserve existing standards, frameworks, methodologies, protocols, and knowledge systems as distinct authorities. Make them interoperable through explicit semantics, scopes, mappings, routing, precedence, and compatibility boundaries. Automation is a means; augmenting human capability is the goal.
