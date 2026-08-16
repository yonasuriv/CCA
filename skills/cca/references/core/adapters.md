# Adapter conventions

Adapters bridge a harness's native instruction entry point to shared portable workspace guidance without forking substantive rules.

## Core rule

> **One canonical body of shared guidance; the smallest native bridge necessary for each harness.**

CCA does not define or override harness instruction precedence. Before creating or changing an adapter, verify the current primary documentation for that harness.

## Preferred order

1. If the harness natively supports the applicable `AGENTS.md` convention, use it directly and do not add a redundant adapter.
2. If the harness supports an include/import mechanism, use that to load shared guidance from its native instruction file.
3. Otherwise use a minimal pointer that tells the harness which shared file to read next.
4. Keep unique harness-only instructions in the harness-native file only when they genuinely cannot live in shared portable guidance.

## ICM compatibility

ICM uses `CLAUDE.md` as its native Layer 0 entry point. CCA must not delete or invalidate that entry path merely to make `AGENTS.md` appear canonical.

A CCA-hardened ICM workspace may use `CLAUDE.md` to include or point at shared portable guidance, but the resulting workspace must still behave correctly for a native ICM/Claude consumer.

## Adapter invariants

- Do not duplicate whole routing tables, policies, or conventions across files.
- Do not claim one file overrides another unless the target harness actually implements that precedence.
- Preserve nested instruction scope where the harness/standard supports it.
- Do not emit adapters for tools the user does not use.
- Do not freeze tool-specific filenames or syntax into CCA as permanent standards; adapters are compatibility edges and may change as tools evolve.
- If a tool gains native support for the shared portable convention, remove the now-redundant adapter when safe.

## Detecting drift

`lint` mode should flag:

- contradictory instructions across root files;
- large adapter files that duplicate shared guidance;
- stale pointers to files that no longer exist;
- adapters whose documented syntax no longer matches the target harness;
- flattening of nested instruction scopes into a single global file.

Repair by preserving unique semantics, choosing one canonical source for shared rules, and using the current native bridge supported by the target harness.

## Why examples are not normative here

Tool-specific instruction filenames and import syntax evolve faster than CCA's filesystem semantics. Keeping static copy-paste adapters in the normative specification would make CCA stale by construction.

CCA therefore bundles stable adapter principles in this single core reference. When exact syntax matters, verify current harness documentation at execution time.