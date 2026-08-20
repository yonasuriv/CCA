# Personal-hybrid intent eval

Behavioral check that `cca` architect builds a useful personal hybrid from **user intent** without baking one preferred folder tree or an undeclared ICM navigation profile into the score.

The prompts ask for projects, notes/research/second-brain use, durable source material versus maintained knowledge, human + agent navigation, and continued use from later sessions. The eval scores those outcomes and the architectural consequences needed to keep them usable as the workspace grows.

## Protocol

1. Fresh agent context. CCA skill only. Empty target directory.
2. Give prompts from [`HUMAN_PROMPTS.md`](HUMAN_PROMPTS.md) verbatim (A → answer B if asked → C).
3. Do **not** show rankings, prior workspaces, or ideal trees to the builder or judge.
4. Score the resulting filesystem with:

```bash
python3 evals/personal-hybrid-intent/tests/score_intent.py /path/to/workspace \
  --skill skills/cca
```

5. Unit smoke (prompt-not-in-skill + scorer contract):

```bash
python3 -m unittest evals/personal-hybrid-intent.tests.test_score_intent -v
```

## What is scored

Path-flexible properties derived from the human prompts and CCA's current architecture:

- a home for outcome/coding projects;
- a distinct home for human notes/thinking;
- durable source/reference material with preservation/supersession behavior;
- maintained knowledge/synthesis distinct from raw evidence;
- capture affordance;
- durable agent/human navigation;
- README/day-to-day continuation guidance;
- at least one worked source → maintained-knowledge citation chain where an empty scaffold would otherwise be ambiguous;
- contradiction/provenance-aware maintenance language;
- self-describing daily operation without requiring an installed skill mode;
- bounded **route-before-search** behavior so a growing workspace can narrow from an entry/router to a relevant collection/local index before broad search;
- no requirement that one root manifest enumerate the whole corpus.

The eval does **not** award points merely for ICM-shaped Layer 0/1/2 files, `CONTEXT.md`, four per-folder contracts, factory stamps, or native ICM `status` behavior. Those belong only when the target is upstream-native ICM, explicitly ICM-derived, or a named profile that adopts them.

If Architect selects the optional CCA Hybrid Workspace Profile, that profile is validated separately by its own frozen/adversarial suite. This intent eval asks whether the produced workspace solves the user's problem, not whether every personal workspace resembles that profile.

The skill must **not** contain the human prompt text. Resolution must come from general architect/method-composition guidance.
