# Methodology Evaluation Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the Record Library identifier regression and add a separate 20-case methodology/framework behavioral evaluation suite without weakening the existing 14-case interoperability benchmark.

**Architecture:** Keep `evals/cases/` as the stable core suite and add `evals/methodologies/` using the same manifest/prompt/fixture/assertion contract. Extend the existing standard-library runner with suite selection, strengthen repository validation for corpus breadth and both suite contracts, and make the Record Library full-name slug fallback explicit while preserving local identifier authority.

**Tech Stack:** Markdown/JSON fixtures, Python 3 standard library, `unittest`, repository regression validator, GitHub Actions.

## Global Constraints

- Preserve external methodologies/frameworks as independent authorities; CCA routes and advises rather than redefines them.
- Do not restore the seven-skill package layout; advisor remains an independent lazy domain inside the one installable `cca` skill.
- Keep `evals/cases/` exactly 14 cases and interpret existing results only against those frozen cases.
- Add exactly 20 methodology cases under `evals/methodologies/`.
- CI/harness mechanics are not behavioral evidence; real external agent runs remain required.
- Use only Python standard library for evaluation/validation code.
- Existing explicit identifier/catalog/template/schema rules always outrank fallback slug derivation.

---

### Task 1: Add failing regression tests for suite separation and Record Library semantics

**Files:**
- Modify: `evals/tests/test_runner.py`
- Modify: `.github/scripts/validate_repo.py`

**Interfaces:**
- Consumes: current `runner.discover_cases(root)` and existing validator conventions.
- Produces: failing expectations for `evals/methodologies/`, `--suite` support, methodology corpus anchors, and the `beta-corp` fallback semantic.

- [x] **Step 1: Add tests that expect 14 core cases and 20 methodology cases**

Add a test that discovers `EVALS / "cases"` and `EVALS / "methodologies"` separately and requires sequential IDs `01..14` and `01..20`.

- [x] **Step 2: Add a runner CLI/root-selection test**

Expose a small `suite_root(evals_root: Path, suite: str) -> Path` helper and test that `core` resolves to `cases`, `methodologies` resolves to `methodologies`, and an unknown suite raises `ValueError`.

- [x] **Step 3: Extend validator expectations before creating the new suite**

Require the 20 methodology case directories, methodology corpus anchor names, and Record Library guidance fragments `full display name` and `beta-corp`.

- [x] **Step 4: Run CI/tests and verify RED**

Verified by the intentionally failing validation run on commit `5cdfcc889eedbd28cb4fb023058de70a48345ba6`, before the methodology suite and runner support existed.

### Task 2: Implement runner suite selection

**Files:**
- Modify: `evals/runner.py`

**Interfaces:**
- Produces: `suite_root(evals_root: Path, suite: str) -> Path`; CLI `--suite {core,methodologies}` default `core`.

- [x] **Step 1: Implement `suite_root` minimally**
- [x] **Step 2: Add `--suite` parser argument**
- [x] **Step 3: Resolve discovery root through `suite_root`**
- [x] **Step 4: Run `python -m unittest discover -s evals/tests -v` and confirm runner tests pass after the suite fixtures land**

### Task 3: Fix Record Library identifier fallback

**Files:**
- Modify: `skills/cca/references/architect/forms.md`

**Interfaces:**
- Consumes: workspace-local template/catalog/schema conventions.
- Produces: explicit full-display-name slug fallback only when evidenced by the existing library.

- [x] **Step 1: Add the local-authority rule**

Explicit IDs and declared catalog/template/schema/domain rules always win.

- [x] **Step 2: Add full-name fallback**

When the local library clearly derives slug IDs from display names and no explicit ID exists, slugify the complete display name; do not abbreviate/truncate. Example: `Beta Corp` -> `beta-corp` under that convention.

- [x] **Step 3: Keep existing lifecycle/half-created/schema-drift semantics unchanged**

### Task 4: Add the 20-case methodology suite

**Files:**
- Create: `evals/methodologies/README.md`
- Create: `evals/methodologies/01-*` through `20-*`, each with `case.json`, `prompt.md`, `fixture/`, `assertions.json`.

**Interfaces:**
- Consumes: existing generic runner assertion types.
- Produces: isolated decision-oriented methodology fixtures.

- [x] **Step 1: Create cases 01-05** — Cynefin; enterprise scaling; sequential constraints; Scrum-vs-Kanban conflict; Kanban flow.
- [x] **Step 2: Create cases 06-10** — DSDM; FDD; ASD; XP; RAD.
- [x] **Step 3: Create cases 11-15** — IID; Lean; RUP/UP; DevOps; TDD.
- [x] **Step 4: Create cases 16-20** — MDE; PSP/TSP; SEMAT/Essence; cross-scope composition; ordinary-task non-trigger.
- [x] **Step 5: Make every fixture non-empty and every assertion set non-empty**

Each process case asks the worker to create `decision.md` with `Scope:`, `Recommendation:`, `Preserve:`, and `Avoid:`. Assertions check case-specific semantic anchors and absence of inappropriate method-named scaffolding where relevant. The non-trigger case asserts the implementation repair and absence of methodology/process scaffolding.

### Task 5: Strengthen permanent repository validation and docs

**Files:**
- Modify: `.github/scripts/validate_repo.py`
- Modify: `evals/README.md`
- Modify: `evals/cases/README.md`
- Create/modify: `evals/methodologies/README.md`

**Interfaces:**
- Produces: explicit evidence boundary and regression guards for methodology breadth.

- [x] **Step 1: Validate both suite contracts**
- [x] **Step 2: Validate methodology corpus anchors**
- [x] **Step 3: Update evaluation docs to distinguish core vs methodology suites**
- [x] **Step 4: Correct stale status wording in `evals/README.md`**
- [x] **Step 5: State that the existing three-way report covers only the 14 core cases**

### Task 6: Full verification

**Files:** none beyond prior tasks.

- [x] **Step 1: Run `python -m unittest discover -s evals/tests -v`**

Passed in the self-cleaning finalization workflow.

- [x] **Step 2: Run `python .github/scripts/validate_repo.py`**

Passed in the self-cleaning finalization workflow.

- [x] **Step 3: Verify methodology fixture preparation with the runner**

Case `04` was prepared without `--command`; it returned the expected assertion failure before agent execution, wrote `result.json`, and recorded `behavioral_run_executed: false`.

- [x] **Step 4: Verify branch diff remains ahead of `main` with no unintended deletion of advisor corpus**

The advisor corpus remains inside `skills/cca/references/advisor/`; the final branch comparison is performed after this bookkeeping commit.

- [x] **Step 5: Mark this plan complete with final-head verification evidence**

This bookkeeping commit is deliberately the last content mutation. The permanent `Validate CCA` workflow is run against this exact resulting head before any completion claim. Its exact run/head evidence is reported externally rather than appended here, which would itself create a new unverified head.

## Implementation status

Implementation work is complete at the repository level. The core benchmark remains 14 frozen cases; the separate methodology suite contains 20 cases. The Record Library regression is addressed without imposing a universal identifier scheme. Repository tests prove harness and regression mechanics only: no real external-agent methodology A/B results are claimed by this plan.