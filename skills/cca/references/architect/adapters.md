# Portable adapter guidance

Use this reference only when a target harness needs its own instruction file.

## Invariant

Keep one canonical body of substantive guidance. An adapter routes into it; it does not duplicate it.

Prefer a tool's native include/import mechanism when available. Otherwise use a short pointer that tells the harness which shared file to read next.

Examples must remain tool-neutral in the skill itself because adapter syntax and native instruction precedence can change independently of CCA.

## Safety rules

- Do not delete a native ICM `CLAUDE.md` merely because `AGENTS.md` exists.
- Do not claim `AGENTS.md` overrides a harness's native discovery rules.
- Do not copy whole routing tables or conventions into multiple root files.
- If two root files already contain unique substantive rules, reconcile them into one canonical source before reducing the other to an adapter.
- If the target tool already reads `AGENTS.md` natively, do not create an unnecessary adapter.

When exact adapter syntax matters, consult the current primary documentation for that harness before writing it.
