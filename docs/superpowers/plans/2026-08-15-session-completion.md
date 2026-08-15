# Session Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the CCA unified-skill refactor by encoding all session conclusions into runtime semantics, deterministic regression checks, and a real-agent A/B evaluation harness with 14 valid scenario fixtures.

**Architecture:** Keep `skills/cca/` as the only runtime package. Add a standard-library Python evaluation harness under `evals/` that prepares isolated A/B workspaces and executes caller-provided real-agent commands without pretending simulated plans are behavioral evidence. Extend repository validation to guard the corrected Layer-0/profile semantics and fixture completeness.

**Tech Stack:** Markdown, Python 3.12 standard library, GitHub Actions.

## Global Constraints

- Preserve external methods/standards as distinct authorities; never absorb or redefine them.
- One installable `cca` skill; seven lazy modes; architect and advisor remain separate domains.
- No repository-only runtime dependency inside `skills/cca/`.
- Native ICM entry/profile semantics take precedence inside a native ICM boundary.
- The four-column native ICM stage Inputs contract remains exact.
- ICM-specific style/size rules remain profile-scoped.
- Real behavioral superiority cannot be claimed from simulated or documentation-only runs.

---

### Task 1: Evaluation Harness Tests and Core

**Files:**
- Create: `evals/tests/test_runner.py`
- Create: `evals/runner.py`

**Interfaces:**
- Produces `discover_cases(root)`, `load_case(case_dir)`, `prepare_run(case, arm, run_root, cca_skill, baseline_root)`, `run_agent(command, workspace, env)`, `evaluate_case(case, workspace)`, and `write_result(result, path)`.

- [ ] Write failing tests for discovery of exactly 14 numbered cases, required manifest/prompt/fixture/assertion files, isolation of A/B workspaces, command execution against the prepared workspace, and deterministic assertion reporting.
- [ ] Run `python -m unittest discover -s evals/tests -v` and confirm failures are caused by missing runner/cases.
- [ ] Implement the minimal standard-library runner.
- [ ] Re-run unit tests and keep them green.

### Task 2: Fourteen Real-Evaluation Case Fixtures

**Files:**
- Create under `evals/cases/01-native-icm/` through `evals/cases/14-no-op/`: `case.json`, `prompt.md`, `fixture/`, `assertions.json`.

**Interfaces:**
- Each `case.json` declares `id`, `name`, `baseline`, `profiles`, and `expected_behavior`.
- Each `assertions.json` uses only runner-supported deterministic assertions.

- [ ] Add the 14 cases from the design matrix with minimal fixtures that make the intended boundary/problem observable.
- [ ] Native cases assert required invariants; preservation/no-op cases assert forbidden mutations or unchanged sentinel hashes; form cases assert their distinguishing semantics rather than exact upstream trees.
- [ ] Run the evaluation unit tests and case validation.

### Task 3: Runtime Semantic Corrections

**Files:**
- Modify: `skills/cca/references/architect/forms.md`
- Modify: `skills/cca/references/architect/methods.md`
- Modify: `skills/cca/references/core/compatibility.md`
- Modify: `skills/cca/references/core/method-composition.md`
- Modify: `skills/cca/references/core/spec.md` as required.

- [ ] Add regression tests/checks that fail on pre-correction native-ICM Layer-0 wording and removed multi-package wording.
- [ ] Correct full-native ICM wording so native `CLAUDE.md` entry semantics are preserved and portable `AGENTS.md` is interoperable rather than universally authoritative.
- [ ] Replace remaining multi-package/sibling-skill language with one-package/seven-mode semantics.
- [ ] Ensure no runtime pointer depends on repository-only docs.
- [ ] Run repository validation.

### Task 4: Form and Setup Specialization

**Files:**
- Modify: `skills/cca/references/architect/system-map.md`
- Modify: `skills/cca/references/architect/forms.md`
- Modify: `skills/cca/assets/templates/setup-questionnaire.md`
- Create: `skills/cca/references/architect/native-icm-setup.md`

- [ ] Add deterministic checks for System Map distinctness, Record Library schema-copy semantics, Context Map frequency/evidence semantics, and native setup answer↔placeholder mapping.
- [ ] Expand System Map with slice gates, evidence/cold-walk requirements, optional shelf creation and no-duplicate-source rules.
- [ ] Make Record Library and Context Map guidance operational enough to distinguish them in cases 9/10.
- [ ] Add native ICM setup reference mapping answers to files/placeholders/conditional stages and require bidirectional coverage verification.
- [ ] Route architect mode to the native setup reference only for full native ICM generation.

### Task 5: Documentation and Evaluation Truthfulness

**Files:**
- Modify: `evals/README.md`
- Modify: `evals/cases/README.md`
- Modify: `README.md` if needed.

- [ ] Document exact runner commands and result schema.
- [ ] State that fixtures/harness exist but real model runs are external and results are unproven until executed.
- [ ] Document equal-budget requirements and scenario-level reporting.

### Task 6: Final Verification

**Files:**
- Modify: `.github/scripts/validate_repo.py`

- [ ] Add fixture completeness and semantic drift checks to the permanent validator.
- [ ] Run `python -m unittest discover -s evals/tests -v`.
- [ ] Run `python .github/scripts/validate_repo.py`.
- [ ] Confirm only `skills/cca/` exists as a first-party skill package and no temporary migration/finalizer workflow remains.
- [ ] Confirm final GitHub Actions `Validate CCA` succeeds on the final branch head.
- [ ] Report real-agent behavioral A/B execution as pending unless actual agent commands were run and produced artifacts.