# Personal-hybrid intent eval

Behavioral check that `cca` architect builds a useful personal hybrid (projects + notes/research + immutable sources vs growing wiki) from **user intent**, without baking any specific user prompt into the skill.

## Protocol

1. Fresh agent context. CCA skill only. Empty target directory.
2. Give prompts from [`HUMAN_PROMPTS.md`](HUMAN_PROMPTS.md) verbatim (A → answer B if asked → C).
3. Do **not** show rankings, prior workspaces, or ideal trees to the builder or judge.
4. Score the resulting filesystem with:

```bash
python3 evals/personal-hybrid-intent/tests/score_intent.py /path/to/workspace \
  --skill skills/cca
```

5. Unit smoke (prompt-not-in-skill + module load):

```bash
python3 -m unittest evals/personal-hybrid-intent.tests.test_score_intent -v
```

## What is scored

Path-flexible intent properties derived from the human prompts (projects, notes, immutable sources, growing wiki, agent navigation, README day-to-day), plus consequences of those claims (supersession or checkable integrity, seeded source→wiki chain, capture affordance, self-describing operation).

Also scores **ICM skeleton / cold-agent isomorphism** (path-flexible): L0 skeleton map, folder contracts with Inputs / Process / Outputs / Human check, live factory stamps, declared status-without-memory scan. This does **not** require a native ICM pipeline.

The skill must **not** contain the human prompt text. Resolution must come from architect/methods personal-hybrid guidance.
