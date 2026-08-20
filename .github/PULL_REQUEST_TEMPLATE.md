# Summary

Describe the problem, the change, and why it belongs in CCA.

## Authority and scope

- [ ] **Upstream authority:** I identified every external or CCA-owned authority affected by this change.
- [ ] If an upstream claim changes, I verified the current primary source rather than relying on stale CCA wording.
- [ ] The change preserves nested/native authority and does not replace an existing framework, methodology, protocol, standard, or knowledge system with a CCA-specific imitation.

Affected authority/boundary:

<!-- e.g. CCA core, Hybrid Workspace Profile, upstream-native ICM, Agent Skills, repository-only docs/tooling -->

## Compatibility / conformance claims

Check only claims this PR actually makes:

- [ ] Upstream-native
- [ ] CCA-compatible
- [ ] CCA-conformant
- [ ] Profile-conformant
- [ ] CCA-hardened
- [ ] ICM-derived only
- [ ] Repository-only / no compatibility claim

Explain any changed claim or acceptance surface:

## Semantic impact

- [ ] This change preserves `boundary + semantic role -> binding` and does not turn a default path into semantic identity.
- [ ] New semantics are necessary for interoperability and are not duplicating an existing upstream/ecosystem convention.
- [ ] Binding-only changes remain binding-only where the governing contract permits relocation.
- [ ] Authority, provenance/admission, lifecycle, mutability, and semantic role remain distinct axes where applicable.

Breaking or versioned impact:

<!-- State none, or explain the required version treatment. -->

## Documentation and distribution

- [ ] `skills/cca/` remains a self-contained portable distribution boundary.
- [ ] Runtime/normative references do not escape to repository-only files.
- [ ] All affected skill references, repository docs, examples, publications, indexes/maps, citation metadata, and changelog entries were updated together where applicable.
- [ ] No stale compatibility terminology, obsolete paths, placeholders, or contradictory current guidance were introduced.

## Validation

Run the complete suite documented in `CONTRIBUTING.md`:

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

Evidence / notable test results:

## Review notes

Call out ambiguity, debt, intentional exceptions, migration concerns, or follow-up work. Do not hide unresolved architectural or compatibility questions behind a passing test suite.
