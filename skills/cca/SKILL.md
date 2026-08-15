---
name: cca
description: Agent-agnostic context architecture and engineering judgment for filesystem-native work. Use to design or restructure workspaces, scaffold portable routing, synchronize navigation, ingest or query maintained knowledge, validate CCA/ICM/LLM-Wiki compatibility, or advise on engineering and methodology trade-offs. Supports existing code repositories, second brains/PKM, ICM, LLM Wiki, PARA, Zettelkasten, BASB/CODE, delivery methods, and hybrid workspaces without replacing their native authorities.
compatibility: Filesystem read/write access for mutating modes. No vendor-specific runtime required.
---

# CCA

CCA is one installable skill with seven lazily loaded modes. Select the smallest mode that directly matches the request, then load only that mode and the references it names.

## Modes

| Mode | Use for | Load first |
|---|---|---|
| `architect` | design, restructure, boundary/profile selection, hybrid composition | `references/architect/mode.md` |
| `scaffold` | add minimal routing/context without restructuring | `references/operations/scaffold.md` |
| `sync` | reconcile routing/navigation with the filesystem | `references/operations/sync.md` |
| `ingest` | integrate evidence into maintained knowledge | `references/operations/ingest.md` |
| `query` | navigate/synthesize maintained knowledge | `references/operations/query.md` |
| `lint` | validate claimed compatibility/conformance profiles | `references/operations/lint.md` |
| `advise` | engineering judgment, process/method trade-offs, security/autonomy/model/context decisions | `references/advisor/mode.md` |

Do not load every mode or reference. Progressive disclosure is part of the architecture.

## Shared authority

Before making a claim about CCA semantics, compatibility, or composition, use the skill-local canonical material under `references/core/`:

- `spec.md` — normative CCA semantics and operation model;
- `compatibility.md` — upstream profiles and preservation rules;
- `method-composition.md` — how methods coexist without being absorbed;
- `adapters.md` — harness-specific interoperability guidance.

These files are inside the installable skill so runtime behavior never depends on repository-global `spec/` files that may not exist after installation.

## Domain boundaries

Keep these domains separate:

- `references/architect/` owns workspace forms, boundaries, structural composition, and migration design.
- `references/advisor/` owns engineering judgment and methodology priors. Its seven references remain independent and are never folded into architect references.
- `references/operations/` owns focused operational procedures.
- `references/core/` owns normative CCA semantics shared by all modes.

Architect mode may consult advisor references when a structural decision requires engineering/process judgment. That is lazy consultation, not ownership transfer or duplication.

## Routing rules

1. Detect the existing workspace/profile before proposing structure.
2. Preserve native authorities and declared method boundaries.
3. Prefer the smallest intervention that solves the routing/context problem.
4. Existing code repositories keep their application structure unless restructuring is explicitly requested.
5. PARA, Zettelkasten, BASB/CODE, Scrum, Kanban, XP, DevOps, SAFe, LeSS, DA, and similar methods remain their own authorities; CCA maps relationships and routing rather than reimplementing them.
6. Native ICM and native LLM Wiki claims are validated against their own applicable semantics before optional CCA hardening.
7. Do not create structure merely because a template exists.
8. For destructive restructuring, surface the migration map before moves, merges, renames, or deletions unless the user has explicitly authorized direct remediation.
9. Use harness-native adapter files only where needed; portable guidance should remain canonical in the workspace's chosen portable authority.
10. When uncertainty crosses a hard-stop boundary, use `references/advisor/escalation-triggers.md`.

## Core rule

**Convergence over invention.** Preserve existing standards, frameworks, methodologies, and knowledge systems as distinct authorities. Make them interoperable through explicit semantics, scopes, mappings, routing, precedence, and compatibility boundaries. Automation is a means; augmenting human capability is the goal.
