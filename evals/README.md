# CCA behavioral evaluations

This directory defines evaluation contracts and mechanics. It does **not** treat static documentation, fixture existence, or simulated agent plans as behavioral evidence.

## Evaluation layers

CCA makes two claims that must remain separately visible:

1. **ICM inheritance:** for every applicable native ICM behavior CCA claims to inherit, CCA must be at least parity with pinned/current ICM. A regression cannot be offset by unrelated CCA wins.
2. **CCA extension value:** broader interoperability must demonstrate useful behavior in cases that actually require cross-authority composition, maintained knowledge, profile-aware validation, or method reasoning.

The benchmark also uses a **no-skill control** so easy cases do not mistake generic model competence for repository capability.

## Three-arm protocol

Use fresh isolated contexts for every case/arm.

### Arm A — reference/baseline

Provide only the pinned repository/runtime material required by the comparison, typically current/pinned ICM for inherited-capability tests.

### Arm B — CCA

Provide only the installable `skills/cca/` package plus the same neutral fixture and task. Do not give repository-global docs that a normal installed skill would not have.

### Arm C — no-skill control

Provide the identical task and fixture with **no ICM or CCA repository material**. This measures what the model can solve from generic competence and the fixture itself.

Interpretation:

```text
A = B = C   likely non-discriminative / generic model competence
A = B > C   both architectures add value; CCA parity, no improvement proven
B > A >= C  CCA improvement on the tested capability
A > B >= C  CCA regression when the capability is inherited
```

Do not force numerical ordering when outputs are qualitatively incomparable; record the reason.

## Hold constant

Across applicable arms use the same model/version/configuration, task prompt, fixture, tools, permissions, network policy, token/context budget, tool-call/step/time budgets, and neutral external authorities. Randomize arm order. Do not share chat history, caches, generated artifacts, results, or evaluator notes.

## Evidence hierarchy

1. applicable external/native authority;
2. deterministic assertions;
3. actual filesystem/task outcome;
4. blind qualitative judgment;
5. context/tool/step/intervention efficiency;
6. package/structural simplicity;
7. documentation claims.

A real behavioral run requires an actual agent to inspect/act on the isolated workspace or explicitly choose no change after inspection. `behavioral_run_executed: false` is not behavioral evidence.

## Suites

### `cases/` — 14 core interoperability cases

The stable broad regression suite: native/derived ICM, ordinary code repositories, PARA/Zettelkasten, LLM Wiki, forms, hybrid boundaries, approved restructure, and no-op behavior. Historical results remain tied to their exact freezes.

### `methodologies/` — 20 methodology/advisor cases

Tests sense-making, enterprise scaling, sequential constraints, team-delivery methods, engineering/lifecycle disciplines, same-scope conflict, cross-scope composition, and an ordinary-task non-trigger.

### `icm-parity/` — granular ICM inheritance catalog

`capabilities.json` contains **40** atomic/integration/compound contracts. The final audit must instantiate neutral executable cases from this catalog and run pinned ICM, CCA, and the no-skill control where applicable.

Coverage includes Layer 0-4 routing, exact stage contracts, output handoffs, one-way dependencies, selective loading, canonical sources, CONTEXT purity, prerequisites, setup/status, questionnaire behavior, placeholders/conditionals, skill discovery/bundling, specs/checkpoints/audits/value validation, docs-over-outputs, shared constants, naming/quality rules, cold-agent walking, build/restructure, factory/product distinction, end-to-end workspace building, adversarial repairs, and progressive-disclosure efficiency.

For an inherited capability classify CCA as **PARITY**, **IMPROVEMENT**, or **REGRESSION**. Do not classify it as an ICM-only feature merely because ICM originated it.

### `cca-extensions/` — discriminative CCA extension catalog

`capabilities.json` contains **20** extension contracts. These are deliberately not simple coexistence tests. They must require cross-authority reasoning or CCA operations such as PARA+Zettelkasten routing, LLM Wiki ingest/query, ICM+Wiki composition, human-vs-agent knowledge authority, profile-aware linting, nested profiles, method composition/conflict, non-trigger behavior, hybrid lifecycle routing, portable guidance, generic workspace building, forms, contradiction handling, escalation, and progressive-disclosure efficiency.

ICM is not marked as failing for an extension outside its claims. Observe its behavior, classify out-of-scope where appropriate, and compare whether CCA adds value beyond both ICM and the no-skill control.

### `personal-hybrid-intent/` — personal hybrid builder from user intent

Checks that architect/workspace-builder produces a useful projects + notes + immutable-sources + growing-wiki workspace from the same human dialogue prompts **without** hardcoding those prompts into the skill. See [`personal-hybrid-intent/README.md`](personal-hybrid-intent/README.md).

## Workspace-builder parity

`skills/cca/references/architect/workspace-builder.md` is first-class Architect runtime behavior. For native ICM it preserves the upstream builder contract inside the installed CCA package:

```text
Discovery
→ Mapping
→ Scaffolding
→ Questionnaire design
→ Validation and repair
→ setup
→ status
→ fresh-agent verification
```

Current upstream ICM remains the semantic and acceptance authority. The point of the CCA implementation is runtime parity without requiring a neighboring upstream checkout.

The final audit must test the builder atomically and end-to-end. Documentation presence is not enough.

## Context-efficiency requirement

Correctness is first. When outcomes are equivalent, measure minimum sufficient context:

- files/references read;
- repeated reads/wrong turns;
- tokens/context if available;
- tool calls and steps;
- files created/changed;
- clarifying questions/interventions;
- duration when comparable.

A broader CCA scope is a regression if it routinely loads advisor/method/knowledge material for simple native or ordinary tasks that do not need it.

## Runner

`evals/runner.py` prepares isolated case directories and deterministic grading; it does not choose or impersonate an agent.

Supported executable suite selectors:

```text
core
methodologies
icm-parity
cca-extensions
```

The granular suites currently expose capability catalogs for the final neutral audit; the orchestrator may materialize frozen executable cases from them before behavioral execution. Once frozen, prompts/fixtures/assertions must not change after results are observed.

Supported arms:

```text
A  baseline/reference material
B  installed CCA skill
C  no-skill control
```

Example:

```bash
python evals/runner.py --suite core --case 01 --arm A \
  --baseline-root /path/to/pinned/icm --command <agent-command>

python evals/runner.py --suite core --case 01 --arm B \
  --cca-skill skills/cca --command <same-agent-command>

python evals/runner.py --suite core --case 01 --arm C \
  --command <same-agent-command>
```

Arm C receives an empty `CCA_EVAL_MATERIAL` and no `baseline/` or `cca/` directory.

## Final success bar

Do not conclude that CCA is an ICM evolution/superset from broad ties alone. The evidence bar is:

1. every applicable `icm-parity` capability is PARITY or IMPROVEMENT for CCA;
2. compound ICM workflows, especially workspace-builder and edited handoffs, are parity or better;
3. CCA extensions outperform or materially add capability beyond controls in scenarios that require them;
4. CCA's breadth does not impose a correctness, context, structural, or intervention tax on native ICM or ordinary tasks.

Report exactly what was behaviorally executed and retain repository/model/runtime/freeze pins with raw artifacts.
