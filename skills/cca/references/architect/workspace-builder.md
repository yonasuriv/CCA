# Workspace builder

Read this reference only when the user asks to create, initialize, set up, materially rebuild, migrate, or report status for a workspace. It is a first-class `architect` capability inside the single `cca` skill.

For an **upstream-native ICM** target, current upstream ICM semantics and acceptance remain authoritative. Preserve the upstream builder behavior; if upstream changes, CCA adapts instead of freezing a competing ICM fork.

For generic targets, reuse only orchestration mechanics that fit the actual problem. For the optional **CCA Hybrid Workspace Profile**, additionally load [`hybrid-workspace.md`](hybrid-workspace.md) and use the bundled implementation under `../../assets/hybrid-workspace/`.

Do not label a workspace upstream-native ICM unless its complete applicable upstream profile passes.

## Trigger routing

- **create / build / initialize** — discover the actual target form, choose/preserve the appropriate upstream/profile, then scaffold and validate it.
- **setup** on native ICM — run the workspace's native onboarding/setup contract.
- **status** on native staged ICM — preserve upstream status semantics.
- **hybrid profile init** — after profile selection, initialize the explicit target with bundled target-safe tooling.
- **rebuild / migrate** — inspect first; preserve authorities; load [`reference-integrity.md`](reference-integrity.md), verify move safety, and use an explicit migration map before destructive changes.

## Phase 1: Discovery

Discover the work before designing files.

1. Establish what the human starts with, what outcome they need, and who/what consumes intermediate artifacts.
2. Detect existing upstream-native systems, portable instructions, method overlays, knowledge systems, projects, restricted boundaries, and local authorities.
3. Identify natural work units/handoffs only where the workflow actually has them.
4. Identify inputs, outputs, stable references/constraints, tools, and human decisions.
5. Separate shared durable context from local/ephemeral state.
6. Separate system-level configuration from per-run input.
7. Identify optional capabilities and observable conditions controlling them.
8. Identify tool prerequisites and whether each is required/optional.
9. Discover reusable Agent Skills/capabilities when they can replace custom duplicated material.
10. Present materially ambiguous architecture assumptions before irreversible restructuring.

Discovery MUST determine whether the target should remain an existing form, become upstream-native to a supported system, adopt a named CCA profile, or use a custom CCA-compatible composition.

## Phase 2: Mapping

Map the discovered environment through CCA without replacing its authorities.

1. Identify boundaries.
2. Identify semantic roles needed inside each boundary.
3. Resolve/choose bindings.
4. Identify authority, mutability, lifecycle, and provenance rules.
5. Assign one canonical home per substantive rule/value.
6. Check dependencies for cycles where one-way flow is required.
7. Verify every produced artifact/state has an intended consumer or durable purpose.
8. Preserve upstream-native contracts exactly where they are part of the upstream conformance surface.
9. When existing paths may move, enumerate in-boundary, sibling-relative, symlink, and bounded known external referrers before proposing the migration; do not classify apparent disuse as move safety.

The CCA interoperability primitive is:

```text
boundary + semantic role -> binding
```

Do not turn a default path into semantic identity.

## Phase 3: Scaffolding

Create only structure justified by the selected form/profile.

### Upstream-native ICM

When native ICM is selected, scaffold the complete applicable current upstream surface, including where applicable:

- current native Layer-0 `CLAUDE.md` behavior;
- root `CONTEXT.md` routing;
- numbered `stages/NN-name/` folders;
- per-stage `CONTEXT.md` contracts;
- per-stage `output/` handoff folders and persistent-empty-folder conventions;
- stable Layer-3 references/factory material;
- setup/questionnaire material;
- tool setup/verification guidance;
- selected bundled Agent Skills;
- checkpoints/audits/value validation where upstream requires them;
- shared constants/configuration where applicable.

For each native stage contract, preserve the current upstream section shape and canonical Inputs columns exactly:

```text
Inputs
Source | File/Location | Section/Scope | Why
Process
Outputs
```

Preserve one-way dependency flow between stages and references where upstream requires it. Use the current upstream contract shape and naming exactly. Portable `AGENTS.md` MAY be added as interoperability hardening only if it does not replace or invalidate native authority.

### Generic/custom CCA-compatible target

Do not force ICM stages, ICM filenames, a wiki, PARA, a manifest, or a CCA-owned tree merely because CCA can model them. Preserve existing application/method structure and add only the routing/bindings needed for deterministic human+agent navigation.

Cold-agent walkability is desirable, but generic CCA compatibility does **not** mean every workspace must mimic an ICM pipeline or satisfy the Hybrid Workspace Profile.

### CCA Hybrid Workspace Profile

Use only when selected by architecture or already present. Read [`hybrid-workspace.md`](hybrid-workspace.md).

The complete implementation remains inside the installed skill:

```text
assets/hybrid-workspace/
├── WORKSPACE.yaml
├── AGENTS.md
├── schema.py
├── generate.py
├── audit.py
├── requirements.txt
└── tests/
```

Initialize an explicit target:

```bash
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --init
```

The generator MUST NOT use its own package directory as the workspace. `--init` copies only missing human-authored bootstrap templates, then all generated artifacts are written to `<workspace>` according to target bindings.

Customize the target by editing allowed bindings in its `WORKSPACE.yaml`; do not fork semantic keys to obtain a different folder name. Regenerate after binding changes.

## Phase 4: Questionnaire/onboarding

Only create onboarding when the selected upstream/profile/workspace actually needs it.

For native ICM, preserve the current upstream questionnaire/setup semantics, including system-level vs per-run separation, derivation of inferable values, complete placeholder mapping, defaults/examples, conditionals, and acceptance checks.

For the Hybrid Workspace Profile, initial binding/authority choices are architectural configuration. Ask only decisions that cannot be safely inferred from user intent/existing filesystem evidence. Do not ask the user to choose defaults merely because the schema lists them.

For ordinary/custom targets, do not invent a setup questionnaire just because the builder has one for other profiles.

## Setup execution for native ICM

When the workspace receives native `setup`:

1. read its current setup/questionnaire state;
2. do not silently re-run completed setup;
3. collect the required current upstream system-level answers;
4. apply answers/derivations/defaults to canonical destinations;
5. resolve native conditionals/optional structures;
6. resolve applicable placeholders using current upstream syntax;
7. configure required tooling/selected skills;
8. scan for unresolved/orphaned configuration;
9. complete setup only after current upstream acceptance passes.

## Migration/rebuild safety

When rebuild/migrate changes existing paths, [`reference-integrity.md`](reference-integrity.md) is mandatory before the approval/execution boundary.

1. Add referrers to the migration map: `current path -> function/authority -> destination -> action -> referrers -> compatibility impact`.
2. Check each destination case-folded before copy/rename so case-insensitive aliases cannot silently overwrite an existing path.
3. Treat live referrers as blockers unless the same change updates them or intentionally preserves compatibility.
4. Prefer copy -> verify parity -> remove rather than move-and-hope for substantive existing content.
5. After migration, re-run every pre-move reference expected to survive before calling the restructure valid.

These mechanics do not create a CCA-specific fork of native ICM. For upstream-native ICM, current upstream restructure acceptance remains the floor.

## Phase 5: Validation and repair

Validate the claim actually being made.

### Upstream-native ICM

Current upstream acceptance is the floor. Validate the complete applicable surface including routing, contracts, naming, handoffs, dependency direction, selective loading, canonical sources, setup/status, placeholders/conditionals, tooling, checkpoints/audits/value validation, docs-over-outputs, shared constants, quality guardrails, current restructure/reference-integrity behavior, and workspace-builder-equivalent acceptance.

Repair failures before describing the generated native workspace as ready.

### Hybrid Workspace Profile

Use the bundled implementation on the explicit target:

```bash
python <cca-skill>/assets/hybrid-workspace/audit.py --target <workspace> --self-test
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --check
```

Profile acceptance MUST verify at least:

1. frozen semantic/policy/authority contract;
2. binding/path safety;
3. generated-artifact integrity;
4. human-authored `AGENTS.md` control contract;
5. non-breaking binding relocation across all generated consumers;
6. `context.router` output follows its binding rather than a hardcoded `CONTEXT.md`;
7. moved `_state/`, `_runtime/`, or other defaults do not leak into generated artifacts;
8. generation/audit touch the explicit target, not the installed skill package;
9. nested upstream-native boundaries remain valid under their own authorities;
10. fresh human/agent orientation works from durable target files.

### Generic/custom target

Validate only the contracts intentionally adopted. Do not fail the target for missing a profile it never chose.

## Status execution

For upstream-native staged ICM, preserve current ICM status semantics and presentation. COMPLETE requires a real output artifact; a placeholder whose only purpose is to keep an empty directory present does not count. Do not infer completion from chat history or mere directory existence.

For the Hybrid Workspace Profile or a custom CCA-conformant target, status is governed by its declared state/binding semantics; do not invent native ICM status behavior.

## Fresh-agent verification

After applicable upstream/profile acceptance passes, perform the CCA portability walk where the target claims it:

1. **Orient** from durable files without prior chat memory.
2. **Act** through one representative route using resolved authority/semantic bindings.
3. **Report** changes, outputs, remaining work, and ambiguity.

For restructures, also verify pre-existing references expected to survive still resolve after the move.

This supplements upstream/profile acceptance; it never converts a failed native/profile contract into a pass.

## Personal hybrid architecture

When discovery shows a personal/team hybrid combining coding projects, human notes/research, preserved sources, maintained wiki/knowledge, tasks/state, and reusable capabilities:

1. preserve the user's chosen human organizational method rather than forcing PARA;
2. separate epistemic roles (capture, source/reference, human notes, durable synthesis) from organizational shelves/lenses;
3. keep ordinary repos capable of remaining ordinary repos or native child boundaries;
4. ensure agents route before broad search as the workspace grows;
5. prefer stable semantic roles with movable bindings over hardcoded folder names;
6. select the CCA Hybrid Workspace Profile when its reviewed semantics fit rather than rebuilding an equivalent custom schema;
7. if the profile does not fit, compose a custom CCA-compatible target instead of mutating the frozen profile contract ad hoc.

Load `methods.md` only when method composition is relevant. Load `hybrid-workspace.md` only when the optional profile is selected/detected.

## Production rule

The builder succeeds when the target remains understandable and operable by humans and agents, preserves upstream/native authority, exposes enough deterministic routing to avoid unnecessary broad search, and passes every acceptance surface it actually claims.
