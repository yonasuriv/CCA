# Workspace builder

Read this reference only when the user asks to create, initialize, set up, materially rebuild, or report status for a workspace. It is a first-class `architect` capability, not a pointer that requires the upstream ICM repository to be installed beside CCA.

For a **native ICM** target, current upstream ICM semantics and acceptance remain authoritative. This workflow preserves the upstream builder behavior inside CCA; if upstream changes, update this reference rather than freezing a competing ICM fork.

For generic or hybrid targets, reuse only the orchestration mechanics that fit the problem. Do not label a workspace native ICM unless its complete applicable upstream profile passes.

## Trigger routing

- **create / build / initialize a workspace**: run the builder from Discovery through Validation and repair.
- **setup** on a native ICM workspace: run the generated workspace onboarding contract, hydrate configuration, resolve conditionals, verify zero unresolved placeholders, and mark setup complete.
- **status** on a native staged workspace: scan stage output folders and render the native COMPLETE/PENDING pipeline state.
- **rebuild / migrate**: inspect first; preserve existing authorities; use Restructure mode when moves, merges, renames, or deletions are required.

Do not run setup again after successful configuration unless the user explicitly requests reset/reconfiguration or the workspace's own native rules require it.

## Phase 1: Discovery

Discover the actual workflow before designing files.

1. Establish what the user starts with, what they need to end with, and who reviews or consumes intermediate artifacts.
2. Identify natural stages and handoff points. Each stage needs one clear responsibility and one named primary output.
3. For every stage identify inputs, outputs, stable references/constraints, tools, and human decisions.
4. Separate shared context from stage-specific context.
5. Separate system-level configuration from per-run input.
6. Identify user-specific variables that must become explicit configurable fields/placeholders.
7. Identify optional stages and the observable condition controlling each one.
8. Identify tool prerequisites. Record which stage needs each tool, whether it is required/optional, install guidance needed, and a verification command.
9. Perform skill discovery when domain skills could replace custom reference material or bundled tooling:
   - inspect available local Agent Skills/skill directories exposed by the runtime;
   - search an allowed upstream/package source when network access is available and the user permits it;
   - present relevant candidates with scope and provenance;
   - bundle only selected/allowed skills needed at runtime;
   - do not duplicate reference material already authoritatively covered by the selected skill.
10. Present the workflow map and dependency assumptions for human correction before irreversible structure is created when the workflow is materially ambiguous.

Discovery output must capture stages, inputs/outputs, shared context, configurable variables, optional stages, tools, and selected skills.

## Phase 2: Mapping

Convert discovery into explicit contracts and authority boundaries.

1. Write a contract for every stage.
2. For native ICM use the exact contract sections and Inputs columns:

```text
Inputs
Source | File/Location | Section/Scope | Why
Process
Outputs
```

3. Map which outputs feed which later stages.
4. Assign one canonical home per substantive rule/value. Consumers point to the authority; they do not create competing copies.
5. Check the dependency graph for cycles. Dependencies flow one way.
6. Verify every non-final output has an intended downstream consumer or an explicitly documented human/external consumer.
7. Identify where checkpoints are justified by creative/decision-heavy work and where audits are justified by creative/build work.
8. For specification stages, preserve WHAT/WHEN as the contract and keep implementation HOW in later build/execution stages.

For native ICM, do not change naming, Layer 0-4 semantics, contract columns, handoff conventions, or other current upstream requirements because another CCA profile would prefer something else.

## Phase 3: Scaffolding

Create only structure justified by the mapped workflow.

For native ICM, scaffold the complete applicable native surface, including:

- native Layer 0 `CLAUDE.md` entry behavior;
- root `CONTEXT.md` task routing;
- numbered `stages/NN-name/` folders;
- stage `CONTEXT.md` contracts;
- per-stage `output/` handoff folders and `.gitkeep` where intentionally empty;
- stable references/factory material outside working outputs;
- shared references only when genuinely shared;
- setup/questionnaire material;
- tool setup guides with verification steps when system prerequisites exist;
- bundled selected Agent Skills when the workspace requires them;
- checkpoints/audits where applicable;
- value framework material where applicable to content-producing work;
- shared constants/configurable values where applicable to code-producing work.

Keep `CONTEXT.md` as routing/process rather than substantive reference content. Route to exact sections when a whole reference is unnecessary.

CCA may add an `AGENTS.md` portable counterpart only when it improves cross-agent use without replacing or invalidating the native `CLAUDE.md` path.

## Phase 4: Questionnaire design

Build onboarding from the scaffolded configuration surface, not from a generic fixed questionnaire.

1. Scan the generated workspace for configurable placeholders/fields and conditional blocks.
2. Split variables into:
   - **system-level**: stable across runs; eligible for setup questions;
   - **per-run**: changes each run; collect at the appropriate entry stage, not global setup.
3. Create one flat numbered list of system-level questions.
4. Ask all setup questions in one pass so the user can answer in one message.
5. Every question must have a sensible default or concrete example where a default is meaningful.
6. Derive values from prior answers/filesystem evidence instead of asking duplicate questions.
7. Record every derived field under the answer/source that determines it.
8. Map each answer to its canonical destination and every configurable destination back to one answer, derivation, or explicit default.
9. For optional stages/sections, map a yes/no or observable condition to removal/retention behavior.
10. Prefer concrete examples for style/voice configuration when pattern evidence is more useful than abstract labels.
11. If generated rules require interpretation, present the derived rules for human review before finalizing.

No system-level placeholder may be orphaned. No question may exist without a consumer.

## Setup execution

When the workspace receives the native `setup` trigger:

1. Read its setup questionnaire and current configured state.
2. If setup was already completed, do not silently re-run it; report that state and ask only if the user explicitly wants reconfiguration.
3. Ask the flat questionnaire conversationally in one pass.
4. Apply direct answers, derived values, and defaults to their canonical destinations.
5. Resolve optional/conditional blocks and stages according to their declared conditions.
6. Replace every applicable `{{SCREAMING_SNAKE_CASE}}` placeholder and valid conditional block using current native ICM syntax.
7. Remove optional structures that the native condition says should not exist rather than leaving dead hidden stages.
8. Configure tool/setup guidance and selected bundled skills.
9. Scan the entire workspace for unresolved placeholders, orphan questions, invalid conditional sections, and duplicate competing configuration homes.
10. Present any interpreted rules requiring human review, apply corrections, then mark setup complete only after acceptance passes.

## Phase 5: Validation and repair

Validate the generated workspace before calling it ready. For native ICM, current upstream validation is the acceptance floor.

Check at least:

1. every routed file/reference exists;
2. the dependency graph is acyclic;
3. every placeholder has one source and every setup question has a consumer;
4. conditional sections/stages use valid complete-section semantics;
5. stage handoffs form the intended unbroken chain;
6. `CONTEXT.md` files contain routing/contracts rather than copied reference material;
7. applicable creative stages contain usable human checkpoints;
8. applicable creative/build stages contain specific audits;
9. specification stages define WHAT/WHEN rather than implementation HOW;
10. native line/size/naming/format rules pass against the current upstream profile;
11. tool prerequisites have install and verification guidance;
12. selected bundled skills resolve and are actually referenced where needed;
13. previous generated outputs are not used as authority over stable docs;
14. shared constants/configurable values have one canonical home where applicable;
15. native Layer 0-4 semantics remain intact;
16. CCA additions do not override upstream-native behavior.

If a check fails, repair the generated workspace and re-run the failed check. A validation report that merely lists known failures is not acceptance.

## Status execution

For native staged workspaces, `status` preserves ICM semantics:

1. enumerate numbered stage folders in pipeline order;
2. inspect each stage's `output/` folder;
3. ignore `.gitkeep` when deciding completion;
4. mark a stage **COMPLETE** when output contains a real artifact and list the artifact name(s);
5. otherwise mark it **PENDING**;
6. render a compact ASCII pipeline using the workspace/stage names.

Do not infer completion from chat history, plans, or a stage directory merely existing.

## Fresh-agent verification

After native/profile validation passes, run the CCA fresh-agent walk:

1. **Orient** from durable Layer 0/root routing without chat memory.
2. **Act** through one representative route using only files/tools the workspace exposes.
3. **Report** produced artifacts, changes, remaining work, and unresolved ambiguity.

This supplements upstream acceptance; it never turns an upstream failure into a pass.

## Generic and hybrid builder use

The builder may also construct ordinary code-context workspaces, PARA/PKM arrangements, LLM Wiki integrations, Record Libraries, Context Maps, System Maps, or nested hybrids. In those cases:

- detect the existing/local authority first;
- load `methods.md` or advisor material only when needed;
- do not impose ICM stages merely because the builder itself uses staged reasoning;
- do not copy ICM-native trigger/naming/size rules into a non-ICM workspace unless the target deliberately adopts them;
- preserve nested native boundaries rather than flattening them into one CCA schema.

When discovery shows a **personal hybrid** (coding projects + notes/research/second brain + immutable sources vs growing wiki), load the Personal hybrid section in `methods.md` and satisfy its defaults before calling the workspace ready—especially under deferred trust.

### Fresh personal-hybrid acceptance (non-ICM)

Before describing such a scaffold as ready:

1. Projects shelf exists and is allowed to hold normal repos.
2. Human notes shelf exists and is **not** the immutable source shelf.
3. Immutable source area and growing wiki area are distinct; raw rewrite is forbidden; **supersession** is documented.
4. Capture affordance exists (`inbox/` and/or a capture script).
5. Agent routing exists (`AGENTS.md` or profile-native entry + portable pointer pattern).
6. A **seeded** source→wiki citation chain exists (real file bodies, not only empty dirs / `.gitkeep`).
7. CCA-hardened bundles include a **checkable** integrity path (copy `assets/scripts/verify-sources.py` / `capture-source.py` into the workspace `bin/` or equivalent, or implement the same behavior).
8. Workspace daily use does not require inventing mandatory external skill modes.
9. If the user asked for a new-session handoff, `README.md` covers day-to-day flows.
10. Run the fresh-agent walk: orient → open wiki index → reach the seeded page → follow citation to raw.

Copy scripts and templates from this skill's `assets/` into the workspace; do not leave the workspace depending on the skill path at runtime.

The builder is successful when the resulting workspace is simpler to operate correctly, not when it looks maximally CCA-shaped.
