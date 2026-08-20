## Summary

What problem does this pull request solve, what changed, and what is the resulting behavior?

## Why

Why is this change needed now? Include the concrete failure mode, user need, audit finding, upstream change, or maintenance problem that justifies it.

## Scope

What is intentionally included in this change?

- 

## Non-goals

What is intentionally **not** being changed? Call out adjacent architecture, compatibility, cleanup, migration, or follow-up work that this PR deliberately leaves alone.

- 

## What changed

Summarize the actual implementation/documentation changes. Prefer concrete bullets over file-by-file narration.

- 

## Authority and scope

- [ ] **Upstream authority:** I identified every external or CCA-owned authority affected by this change.
- [ ] If an upstream claim changes, I verified the current primary source rather than relying on stale CCA wording.
- [ ] The change preserves nested/native authority and does not replace an existing framework, methodology, protocol, standard, or knowledge system with a CCA-specific imitation.

Affected authority/boundary:

<!-- e.g. CCA core, Hybrid Workspace Profile, upstream-native ICM, Agent Skills, repository-only docs/tooling -->

## Compatibility / version impact

Compatibility / conformance claims — check only claims this PR actually makes:

- [ ] Upstream-native
- [ ] CCA-compatible
- [ ] CCA-conformant
- [ ] Profile-conformant
- [ ] CCA-hardened
- [ ] ICM-derived only
- [ ] Repository-only / no compatibility claim

Explain any changed compatibility/conformance claim, migration requirement, schema/spec version impact, or why none is required:

## Semantic impact

- [ ] This change preserves `boundary + semantic role -> binding` and does not turn a default path into semantic identity.
- [ ] New semantics are necessary for interoperability and are not duplicating an existing upstream/ecosystem convention.
- [ ] Binding-only changes remain binding-only where the governing contract permits relocation.
- [ ] Authority, provenance/admission, lifecycle, mutability, and semantic role remain distinct axes where applicable.

Semantic axes affected, if any:

<!-- boundary / role / classification / binding / authority / policy / provenance / lifecycle / freshness / none -->

## Documentation and distribution

- [ ] `skills/cca/` remains a self-contained portable distribution boundary.
- [ ] Runtime/normative references do not escape to repository-only files.
- [ ] All affected skill references, repository docs, examples, publications, indexes/maps, citation metadata, and changelog entries were updated together where applicable.
- [ ] No stale compatibility terminology, obsolete paths, placeholders, or contradictory current guidance were introduced.

## Verification

Run the complete suite documented in `CONTRIBUTING.md` when applicable:

```bash
python -m unittest discover -s evals/tests -v
python evals/personal-hybrid-intent/tests/test_score_intent.py
python -m pip install -r skills/cca/assets/hybrid-workspace/requirements.txt
python -m unittest discover -s skills/cca/assets/hybrid-workspace/tests -v
python skills/cca/assets/hybrid-workspace/audit.py --self-test
python .github/scripts/validate_repo.py
python .github/scripts/validate_distribution.py
```

- [ ] All applicable commands pass on the exact PR head.
- [ ] Behavioral changes include failing regression/adversarial coverage before the implementation fix where practical.
- [ ] Upstream-native claims also pass the upstream's own current acceptance requirements; CCA validation does not waive upstream failures.

Exact tested head / merge candidate:

```text
<commit SHA>
```

Evidence / notable test results:

```text
<tests, validators, audit counts, or intentionally not-applicable checks>
```

## Follow-up / known debt

List unresolved questions, intentional exceptions, deferred cleanup, migration concerns, or future work. Write `None` if there is no known follow-up.

- 

Do not hide unresolved architectural or compatibility questions behind a passing test suite.
