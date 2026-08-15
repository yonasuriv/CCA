# CCA behavioral evaluations

This directory defines how to test CCA behavior against relevant upstream baselines. It does **not** contain simulated agent plans presented as behavioral evidence.

## Status

The evaluation **protocol and case contract are defined**, but the 14 scenario fixtures have not yet all been implemented or executed. No repository claim of behavioral superiority over ICM should be inferred from this directory until real isolated runs and their results are committed.

## Purpose

CCA makes two different promises and they must be evaluated separately:

1. **Native compatibility:** when CCA operates on a native upstream profile such as ICM, it must be no worse than that upstream's applicable semantics and acceptance surface.
2. **Broader interoperability:** CCA should improve outcomes when several authorities, methods, knowledge systems, existing project structures, or agent portability constraints must coexist.

A single aggregate score must not hide a native-compatibility regression behind wins on broader CCA scenarios.

## Execution protocol

Every comparison uses fresh isolated runs.

### Arm A — upstream baseline

Provide only the upstream material required by the case. For ICM comparisons this means the pinned/current ICM methodology and, when the tested behavior belongs to it, `icm-architect`.

### Arm B — CCA

Provide only the installable `skills/cca/` package plus the same task fixture. Do not provide repository docs that would not exist after skill installation unless the case explicitly tests repository contribution behavior.

### Hold constant

For both arms use the same:

- model and model configuration;
- task prompt;
- filesystem fixture;
- tool permissions;
- network policy;
- token/context budget;
- tool-call budget;
- time/step budget;
- external sources available to the agent.

Run order should be randomized when the harness permits it. Runs must not share chat memory, caches, generated files, or hidden evaluator notes.

## What counts as evidence

The agent must produce **actual filesystem changes or an explicit no-change decision**. A separate agent reading skill text and predicting what another agent would do is not a behavioral run.

Store, when the harness permits:

- initial fixture hash/tree;
- final filesystem tree and diff;
- deterministic assertion results;
- tool/read/write counts;
- tokens or equivalent context-use telemetry;
- human interventions/clarifications required;
- final user-facing answer;
- blind quality-judge result;
- model/runtime/version and upstream commit pins.

## Grading order

### 1. Deterministic invariants

Grade mechanically before qualitative judging. Examples:

- required native ICM files/contracts are valid;
- an existing code repository was not needlessly restructured;
- native authority files were preserved;
- references resolve;
- generated files are inside the authorized scope;
- a no-op case produces no cosmetic structure;
- a System Map cites real source-of-truth paths;
- a Record Library follows its declared template/schema and catalog authority.

A deterministic compatibility failure cannot be erased by a qualitative judge preferring the prose.

### 2. Blind pairwise quality

Give a judge the task and anonymized outputs without telling it which arm produced which result. Score only dimensions relevant to the case, for example correctness, completeness, navigability, unnecessary complexity, preservation of native semantics, and usability by a cold agent/human.

### 3. Cost and intervention

Compare:

- tokens/context loaded;
- files read;
- tool calls;
- files created/changed;
- clarifying questions or human interventions;
- unresolved ambiguity;
- cold-agent completion success.

CCA should not claim improvement merely because it created more structure.

## Scenario matrix

| ID | Scenario | Primary question |
|---|---|---|
| `01` | Native ICM pipeline | Does CCA preserve/produce the full applicable ICM semantics at least as reliably as upstream? |
| `02` | ICM-derived pipeline | Can useful ICM mechanics be borrowed without falsely claiming native ICM? |
| `03` | Existing code repository | Does CCA preserve a healthy codebase and add only context that earns its cost? |
| `04` | Existing code repo + Scrum | Can CCA route process/code/backlog authorities without filesystem-implementing Scrum? |
| `05` | PARA second brain | Does CCA preserve PARA semantics while making agent routing clearer? |
| `06` | PARA + Zettelkasten | Are organizational and idea-development authorities kept distinct? |
| `07` | LLM Wiki | Does CCA preserve native maintained-knowledge behavior/schema? |
| `08` | LLM Wiki + ICM workflow | Can persistent synthesis and staged production coexist without schema flattening? |
| `09` | Record Library | Are template/schema, identifier/status authority, lifecycle, and drift handled coherently? |
| `10` | Context Map | Are organizational/process/information relationships represented with evidence and useful operational fields? |
| `11` | System Map | Can a cold agent reason about source-backed change impact without duplicating the repository? |
| `12` | Hybrid workspace | Are nested native/method boundaries routed without being merged? |
| `13` | Existing-workspace restructure | Are moves/renames explicit, bounded, and semantics-preserving? |
| `14` | No-op / already healthy | Does CCA correctly recommend no structural change? |

The case contract lives under [`cases/`](cases/). Individual scenario directories and fixtures are added there as they are implemented.

## Interpretation

For native ICM cases, the success condition is not “CCA looks different” or “CCA wins.” It is **compatibility with no regression**, with lower cost or clearer routing considered secondary improvements.

For mixed/existing-workspace cases, CCA can demonstrate capability beyond the ICM baseline if it preserves more authorities, performs fewer unnecessary mutations, reduces context/exploration cost, or improves cold-agent success.

Do not publish “CCA is better than ICM” as a universal result. Report scenario-level evidence and the upstream/model/runtime pins used to obtain it.

## Runner usage

The repository ships `evals/runner.py`; it prepares and grades runs but does not choose or impersonate an agent.

```bash
# Arm B: CCA-only material. Everything after --command is the real agent command.
python evals/runner.py \
  --case 03 \
  --arm B \
  --runs /tmp/cca-evals \
  --cca-skill skills/cca \
  --command <agent-command> <agent-args>

# Arm A: upstream baseline material must be supplied for cases that require it.
python evals/runner.py \
  --case 01 \
  --arm A \
  --runs /tmp/cca-evals \
  --baseline-root /path/to/pinned/icm-material \
  --command <same-agent-command> <same-agent-args>
```

The invoked command runs with its working directory set to the isolated `workspace/`. It receives `CCA_EVAL_CASE`, `CCA_EVAL_ARM`, `CCA_EVAL_PROMPT`, and `CCA_EVAL_MATERIAL` environment variables. The caller is responsible for giving both arms the same model/configuration, tool permissions, network policy, context/token budget, tool-call budget, and time/step budget.

Each prepared run writes `result.json` containing command/exit/duration metadata (when a command was actually run) and deterministic filesystem assertion results. `behavioral_run_executed: false` means the runner only prepared/graded a workspace; such output is **not** behavioral evidence.

The 14 fixtures and harness are implemented. Real model A/B results are still unproven until actual external agent commands execute both arms under matched conditions and their artifacts are retained. Report results per scenario; never turn fixture existence or CI success into a universal “CCA is better than ICM” claim.
