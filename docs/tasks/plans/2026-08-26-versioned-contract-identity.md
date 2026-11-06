# Versioned CCA Contract Identity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make CCA compatibility/conformance identity depend only on the declared CCA contract version, expose and enforce that version from the installed skill, and migrate Symbiont away from a normative CCA commit pin.

**Architecture:** CCA 1.1.0 exposes one canonical SemVer identity through `skills/cca/SKILL.md` and keeps spec/citation/changelog surfaces coherent. Normative CCA guidance forbids source-revision identity for consumers while allowing source SHAs as non-normative provenance. A dedicated Git-aware CI gate enforces version bumps for contract-sensitive installed-skill changes. Symbiont then consumes `specification: 1.1.0` only and removes active commit-dependent validation.

**Tech Stack:** Markdown/YAML Agent Skill metadata, Python 3.12 `unittest`, Git, GitHub Actions, existing CCA/Symbiont validation harnesses.

**Spec:** `docs/superpowers/specs/2026-08-26-versioned-contract-identity-design.md`

## Global Constraints

- CCA compatibility, conformance, and CCA-owned profile identity MUST be version-based, never repository-commit-based.
- `skills/cca/SKILL.md` `metadata.version` is the canonical installed CCA contract identity.
- Skill version and normative CCA specification version are one SemVer identity and MUST NOT drift.
- Establish current CCA contract version as `1.1.0`.
- Commit/tree/blob/hash identities MAY appear only as non-normative source/audit/debug provenance unless an external upstream itself explicitly makes such identity normative.
- Do not weaken CCA's existing upstream-source provenance requirements; consumer CCA identity and upstream mapping provenance are separate concerns.
- Preserve Symbiont's historical evidence while removing active CCA commit coupling.
- Use TDD for validator/version-gate behavior.

---

### Task 1: Add failing CCA version-contract regressions

**Files:**
- Modify: `evals/tests/test_release_readiness.py`
- Create: `evals/tests/test_contract_versioning.py`

**Interfaces:**
- Consumes: current CCA `SKILL.md`, spec, citation metadata, lint/architect/builder references.
- Produces: deterministic tests defining `1.1.0`, version coherence, and the no-commit-identity rule.

- [ ] **Step 1: Add release-coherence test expectations**

Add tests that parse `skills/cca/SKILL.md` YAML frontmatter and assert `metadata.version == "1.1.0"`; assert `Version 1.1.0` in the normative spec; assert both CFF files contain `version: '1.1.0'`; assert `CHANGELOG.md` contains `## 1.1.0 - 2026-08-26`.

- [ ] **Step 2: Add no-commit-identity contract tests**

Create `test_contract_versioning.py` with assertions that `spec.md`, `compatibility.md`, `references/operations/lint.md`, `references/architect/mode.md`, and `references/architect/workspace-builder.md` explicitly distinguish version identity from source provenance and forbid commit/revision identity for CCA consumer conformance.

- [ ] **Step 3: Run focused tests and verify failure**

Run:

```bash
python -m unittest evals.tests.test_release_readiness evals.tests.test_contract_versioning -v
```

Expected: FAIL because `SKILL.md` lacks `metadata.version`, release surfaces still say `1.0.0`, and normative no-commit-identity wording is absent.

- [ ] **Step 4: Commit failing tests**

```bash
git add evals/tests/test_release_readiness.py evals/tests/test_contract_versioning.py
git commit -m "test: define versioned CCA contract identity"
```

### Task 2: Expose CCA 1.1.0 and encode the normative identity rule

**Files:**
- Modify: `skills/cca/SKILL.md`
- Modify: `skills/cca/references/core/spec.md`
- Modify: `skills/cca/references/core/compatibility.md`
- Modify: `skills/cca/references/operations/lint.md`
- Modify: `skills/cca/references/architect/mode.md`
- Modify: `skills/cca/references/architect/workspace-builder.md`
- Modify: `skills/cca/CITATION.cff`
- Modify: `CITATION.cff`
- Modify: `CHANGELOG.md`
- Modify: `CONTRIBUTING.md`

**Interfaces:**
- Consumes: Task 1 regression expectations.
- Produces: installed CCA contract version `1.1.0` and normative version-vs-provenance semantics used by all consumers.

- [ ] **Step 1: Add canonical skill metadata version**

Set `skills/cca/SKILL.md` frontmatter to include:

```yaml
metadata:
  version: "1.1.0"
```

- [ ] **Step 2: Version the normative specification**

Change the spec header to `Version 1.1.0` and add a normative contract-identity subsection stating that CCA consumer compatibility/conformance/profile identity MUST use the applicable CCA contract version and MUST NOT use repository/source revision identity. Explicitly allow source revisions only as non-normative provenance.

- [ ] **Step 3: Update compatibility and operation guidance**

Add the same distinction to `compatibility.md`. Update lint to report a normative commit/revision pin as a CCA conformance error while allowing historical/evidence provenance. Update Architect and workspace builder so generated/remediated CCA contracts record a version and never introduce commit identity.

- [ ] **Step 4: Update release/version surfaces**

Set root and skill CFF versions to `1.1.0` and release date to `2026-08-26`. Move the current `Unreleased` user-visible behavioral changes into `## 1.1.0 - 2026-08-26`, leaving a fresh `## Unreleased` section above it. Document versioned consumer identity in the 1.1.0 entry.

- [ ] **Step 5: Document SemVer contribution policy**

In `CONTRIBUTING.md`, define MAJOR/MINOR/PATCH/no-bump rules and require contract-sensitive behavior changes to update `SKILL.md` metadata version in the same change.

- [ ] **Step 6: Run focused tests and verify pass**

Run:

```bash
python -m unittest evals.tests.test_release_readiness evals.tests.test_contract_versioning -v
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add skills/cca/SKILL.md skills/cca/references/core/spec.md skills/cca/references/core/compatibility.md skills/cca/references/operations/lint.md skills/cca/references/architect/mode.md skills/cca/references/architect/workspace-builder.md skills/cca/CITATION.cff CITATION.cff CHANGELOG.md CONTRIBUTING.md
git commit -m "feat: version CCA contract identity"
```

### Task 3: Add a CI version-bump gate

**Files:**
- Create: `.github/scripts/validate_contract_version.py`
- Create: `evals/tests/test_contract_version_gate.py`
- Modify: `.github/workflows/validate.yml`
- Modify: `CONTRIBUTING.md`
- Modify: `docs/README.md`

**Interfaces:**
- Consumes: `skills/cca/SKILL.md` `metadata.version`, Git baseline/current tree.
- Produces: CLI `python .github/scripts/validate_contract_version.py [--base <ref>]` returning zero when no contract-sensitive change exists or the version differs from the baseline; non-zero when contract-sensitive changes occur without a version bump.

- [ ] **Step 1: Write failing unit tests for the gate**

Use temporary Git repositories in `test_contract_version_gate.py` to prove:

1. docs-only change with unchanged version passes;
2. `skills/cca/references/core/spec.md` change with unchanged version fails;
3. same contract change with `metadata.version` bump passes;
4. `skills/cca/SKILL.md` behavioral/body change with unchanged version fails;
5. version-only release change passes.

- [ ] **Step 2: Run the new tests and verify failure**

Run:

```bash
python -m unittest evals.tests.test_contract_version_gate -v
```

Expected: FAIL because the script does not exist.

- [ ] **Step 3: Implement the gate**

Implement Python 3.12 stdlib-only logic that:

- parses `metadata.version` from `skills/cca/SKILL.md` with a minimal frontmatter parser;
- determines base from `--base`, `CCA_VERSION_BASE`, `GITHUB_BASE_REF`/`origin/<base>`, or `HEAD^` fallback;
- obtains changed paths via `git diff --name-only <base>...HEAD` with a two-dot fallback where needed;
- treats installed CCA behavior paths as contract-sensitive;
- reads the baseline version via `git show <base>:skills/cca/SKILL.md`;
- fails with a precise diagnostic if sensitive files changed and current version equals baseline version.

- [ ] **Step 4: Run gate tests and verify pass**

Run:

```bash
python -m unittest evals.tests.test_contract_version_gate -v
```

Expected: PASS.

- [ ] **Step 5: Wire CI and contributor docs**

Change checkout to `fetch-depth: 0`; invoke `python .github/scripts/validate_contract_version.py` before the full suite. Add the command to `CONTRIBUTING.md` and `docs/README.md` validation surfaces.

- [ ] **Step 6: Commit**

```bash
git add .github/scripts/validate_contract_version.py evals/tests/test_contract_version_gate.py .github/workflows/validate.yml CONTRIBUTING.md docs/README.md
git commit -m "test: enforce CCA contract version bumps"
```

### Task 4: Run complete CCA validation and integrate

**Files:**
- Modify only files required by failures discovered from the exact branch head.

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: green CCA 1.1.0 branch with no validator regressions.

- [ ] **Step 1: Run complete validation surface**

```bash
python -m unittest discover -s evals/tests -v
python evals/personal-hybrid-intent/tests/test_score_intent.py
python -m pip install -r skills/cca/assets/hybrid-workspace/requirements.txt
python -m unittest discover -s skills/cca/assets/hybrid-workspace/tests -v
python skills/cca/assets/hybrid-workspace/audit.py --self-test
python .github/scripts/validate_repo.py
python .github/scripts/validate_distribution.py
```

Expected: all PASS.

- [ ] **Step 2: Verify version gate against the branch base**

```bash
python .github/scripts/validate_contract_version.py --base origin/main
```

Expected: PASS because contract-sensitive changes are accompanied by `1.0.0 -> 1.1.0`.

- [ ] **Step 3: Review branch diff for scope**

Confirm no unrelated structural/profile changes and no consumer commit-pin language remains in normative CCA runtime guidance.

### Task 5: Add failing Symbiont regressions for version-only CCA identity

**Files:**
- Modify: `evals/tests/validate_contracts.py`
- Modify: `evals/tests/test_validate.py` where existing CCA contract tests live
- Modify: `schemas/registry.schema.yaml`

**Interfaces:**
- Consumes: released CCA contract identity `1.1.0` from Tasks 1-4.
- Produces: tests proving Symbiont accepts `cca.specification: 1.1.0`, rejects active `cca.reference_commit`, and does not require a CCA source commit for conformance.

- [ ] **Step 1: Add failing schema/contract tests**

Assert canonical `registry.yaml` contains `cca.specification == "1.1.0"` and no `reference_commit`. Add a negative fixture/mutation proving active `reference_commit` is rejected by the registry schema or validator.

- [ ] **Step 2: Replace commit-identity validator expectations**

Update tests that currently expect `CCA_REFERENCE_COMMIT` or exact `reference_commit` so they instead expect version identity and permit source SHA only inside historical/evidence provenance.

- [ ] **Step 3: Run focused tests and verify failure**

```bash
python -m unittest evals.tests.test_validate evals.tests.validate_contracts -v
```

Expected: FAIL against the existing commit-pinned Symbiont implementation.

- [ ] **Step 4: Commit failing tests**

```bash
git add evals/tests/validate_contracts.py evals/tests/test_validate.py schemas/registry.schema.yaml
git commit -m "test: define version-only CCA identity"
```

### Task 6: Migrate Symbiont to CCA 1.1.0

**Files:**
- Modify: `registry.yaml`
- Modify: `schemas/registry.schema.yaml`
- Modify: `evals/validate.py`
- Modify: `evals/cca-conformance.yaml`
- Modify: active CCA evidence/attestation files only where they currently treat source commit as conformance identity
- Modify: `_agent-home/core.md`
- Modify: `_agent-home/journal/2026-08.md`
- Modify: `state/current.md` if current state materially changes

**Interfaces:**
- Consumes: CCA 1.1.0 versioned contract.
- Produces: Symbiont active CCA conformance based on version only; historical SHAs retained solely as provenance.

- [ ] **Step 1: Remove active commit identity**

Set:

```yaml
cca:
  specification: 1.1.0
```

and remove `reference_commit` from the live registry/schema/validator claim identity.

- [ ] **Step 2: Refactor validator constants and checks**

Remove `CCA_REFERENCE_COMMIT` and any validation path requiring the workspace's live `cca` block or conformance matrix to equal a CCA source commit. Preserve CCA source-document hashes/requirement hashes only if they are explicitly historical attestation evidence rather than current CCA identity; relabel/document them where necessary so their role cannot be confused.

- [ ] **Step 3: Update conformance matrix/evidence semantics**

Change active CCA claim metadata to `1.1.0`. Historical evidence may continue to state which source checkout was inspected on 2026-08-22, but it must say that SHA is provenance and not the current contract identity.

- [ ] **Step 4: Admit the generalized operating lesson**

Add to `_agent-home/core.md` a concise durable rule: external architecture/standard/skill/protocol/framework compatibility binds to the declared versioned contract, not repository commit; source revisions are provenance/debugging evidence unless the external contract explicitly makes revision identity normative. Record the correction in the journal.

- [ ] **Step 5: Run focused tests and verify pass**

```bash
python -m unittest evals.tests.test_validate evals.tests.validate_contracts -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add registry.yaml schemas/registry.schema.yaml evals/validate.py evals/cca-conformance.yaml evidence ledger _agent-home/core.md _agent-home/journal/2026-08.md state/current.md
git commit -m "fix: bind Symbiont to CCA contract version"
```

### Task 7: Run complete Symbiont validation and integrate both repositories

**Files:**
- Modify only files required by exact-head failures.

**Interfaces:**
- Consumes: green CCA 1.1.0 branch and migrated Symbiont branch.
- Produces: both repositories green with version-only interoperability identity.

- [ ] **Step 1: Run Symbiont complete validation**

```bash
python -m unittest discover -s evals/tests -p 'test_*.py' -v
python evals/validate.py
```

Expected: all tests `OK`; validator `PASS`; CCA conformance reports specification `1.1.0` without source-commit identity.

- [ ] **Step 2: Run GitHub CI on exact heads**

Confirm branch CI succeeds for CCA and Symbiont.

- [ ] **Step 3: Review final diffs**

Confirm:

- no live CCA consumer contract contains `reference_commit`;
- CCA `SKILL.md` exposes `metadata.version: "1.1.0"`;
- version and release surfaces agree;
- source SHAs remain only where their role is clearly provenance;
- Symbiont's durable learning contains the generalized rule;
- no unrelated architecture changes were introduced.

- [ ] **Step 4: Integrate only after verification**

Merge the verified CCA branch first, then update/verify Symbiont against that merged CCA 1.1.0 contract and merge Symbiont second.
