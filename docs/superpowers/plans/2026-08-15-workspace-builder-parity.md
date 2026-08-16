# Workspace Builder Parity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add first-class native ICM workspace-builder behavior to `cca` Architect and upgrade the evaluation harness with atomic ICM parity, CCA-extension, and no-skill-control coverage.

**Architecture:** Preserve upstream ICM as the native semantic floor while implementing the builder workflow inside the installed CCA skill. Extend the existing deterministic eval harness without rewriting the frozen 14-case core or 20-case methodology suites.

**Tech Stack:** Markdown Agent Skill references, Python unittest evaluation harness, JSON benchmark manifests/fixtures, GitHub Actions.

## Global Constraints

- Never redefine or weaken native ICM.
- Do not copy the upstream workspace-builder tree wholesale; preserve behavior through a focused Architect reference.
- Existing 14 core and 20 methodology suites remain intact.
- No-skill control receives no repository material.
- Behavioral superiority claims require real agent execution; CI validates contracts/mechanics only.

---

### Task 1: Guard workspace-builder parity

**Files:**
- Create: `evals/tests/test_workspace_builder.py`
- Modify: `evals/tests/test_icm_inheritance.py`

- [ ] Add failing tests requiring an Architect `workspace-builder.md` reference, routing from Architect mode/SKILL, first-class setup/status behavior, the five builder phases, and inherited-not-delegated setup/status classification.
- [ ] Run CI and confirm RED before runtime changes.

### Task 2: Implement Architect workspace builder

**Files:**
- Create: `skills/cca/references/architect/workspace-builder.md`
- Modify: `skills/cca/references/architect/mode.md`
- Modify: `skills/cca/references/architect/core.md`
- Modify: `skills/cca/references/architect/native-icm-setup.md`
- Modify: `skills/cca/references/core/icm-inheritance.md`
- Modify: `skills/cca/SKILL.md`

- [ ] Encode discovery, mapping, scaffolding, questionnaire, validation/repair, setup, status, and fresh-agent verification.
- [ ] Route create/setup/status/full-native generation lazily to the builder.
- [ ] Keep upstream acceptance authoritative and CCA extensions additive.
- [ ] Re-run tests and validator to GREEN.

### Task 3: Add no-skill control to runner

**Files:**
- Modify: `evals/runner.py`
- Modify: `evals/tests/test_runner.py`

- [ ] Write failing tests for arm `C` with fixture/prompt but no `baseline/` or `cca/` material.
- [ ] Implement arm C and record empty material path semantics without breaking A/B.
- [ ] Verify existing suites still pass mechanically.

### Task 4: Add granular benchmark catalogs

**Files:**
- Create: `evals/icm-parity/README.md`
- Create: `evals/icm-parity/capabilities.json`
- Create: `evals/cca-extensions/README.md`
- Create: `evals/cca-extensions/capabilities.json`
- Modify: `evals/README.md`
- Modify: `.github/scripts/validate_repo.py`

- [ ] Add at least 35 atomic/compound ICM capability contracts with provenance and expected comparison semantics.
- [ ] Add CCA-extension cases that require composition/authority/routing behavior rather than generic preservation.
- [ ] Add validator coverage for suite counts, unique IDs, required fields, and control-arm semantics.
- [ ] State clearly that catalogs define final-audit contracts; real external-agent runs remain required.

### Task 5: Final verification

- [ ] Run unit tests.
- [ ] Run repository validator.
- [ ] Confirm permanent `Validate CCA` workflow passes on the exact final head.
- [ ] Record final commit/run and any remaining untested behavioral claims.
