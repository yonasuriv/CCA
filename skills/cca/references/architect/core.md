# Core reference: compatibility, routing, and workspace invariants

Use this reference when designing or restructuring a workspace. CCA converges on upstream conventions; it does not make one preferred implementation mandatory for every compatible target.

Read `methods.md` when the request involves PARA, Zettelkasten, BASB/CODE, second brains/PKM, or composition among human methods, LLM Wiki, ICM, and ordinary projects. Read `hybrid-workspace.md` only when the optional CCA Hybrid Workspace Profile is selected or detected.

When the request claims or creates **upstream-native ICM**, also read `../core/icm-inheritance.md`. That file is a provenance/compatibility map, not a competing ICM specification. Current upstream ICM remains authoritative.

## Compatibility vocabulary

CCA uses independent claims:

- **Upstream-native** — the boundary satisfies the applicable upstream according to that upstream's own current authority and acceptance rules.
- **CCA-compatible** — CCA can resolve and operate on the boundary without structural migration or semantic replacement.
- **CCA-conformant** — the boundary intentionally adopts CCA's normative interoperability contract.
- **Profile-conformant** — the boundary satisfies a named optional CCA-owned profile.
- **CCA-hardened** — optional CCA capabilities were added without invalidating existing native semantics.

Never call an upstream workspace CCA-conformant merely because CCA can read it. PARA, Zettelkasten, BASB/CODE, and delivery methods remain method overlays/authorities rather than invented CCA compatibility states.

A valid native ICM workspace is **CCA-compatible** without migration.

## Semantic resolution

CCA reasons through:

```text
boundary + semantic role -> binding
```

The role/key is stable meaning. The binding is the current local representation.

Agents MUST resolve the applicable boundary and semantic role before assuming a concrete path. A default path is not identity unless the governing upstream/profile explicitly makes that path part of conformance.

For a CCA-owned or custom boundary, two implementations may therefore bind the same semantic role differently. For upstream-native ICM, preserve exact upstream filenames wherever ICM makes them normative.

## ICM: upstream-native vs derived/adopted behavior

Distinguish:

- **Upstream-native ICM** — complete applicable current ICM/MWP profile passes.
- **ICM-derived** — selected ICM constructs are borrowed without claiming the complete native profile.
- **CCA-owned profile adopting ICM navigation behavior** — a CCA profile may use ICM-proven cold-agent routing/progressive disclosure without becoming native ICM.

Do not use “ICM-compatible” as shorthand for “contains stage folders.” State the actual claim.

For upstream-native ICM, preserve and validate all applicable current upstream rules, including:

1. current native routing/layer semantics and Layer-0 behavior;
2. exact root/stage `CONTEXT.md` representation where required;
3. exact stage contract sections/Inputs columns;
4. current naming and intentionally empty persistent-folder rules;
5. per-stage output handoffs and downstream chain;
6. one-way dependencies and cycle-free references;
7. selective section routing and canonical-source discipline;
8. contract-file purity;
9. current `setup` and `status` behavior;
10. questionnaire/placeholder/conditional rules where applicable;
11. required-tool and bundled-skill behavior where applicable;
12. checkpoints, audits, specification WHAT/WHEN discipline, and value validation where applicable;
13. docs-over-outputs and shared-constant rules where applicable;
14. current size/readability/formatting guardrails;
15. workspace-builder-equivalent end-to-end validation before a generated native workspace is described as ready.

Upstream ICM `_core/CONVENTIONS.md` is canonical for ICM semantics. Current upstream workspace-builder validation is the practical generated-workspace acceptance surface. If either changes, CCA updates/version-pins its mapping rather than preserving a stale local interpretation.

A native ICM boundary may sit inside a broader CCA/PARA/client/hybrid workspace. The outer boundary may organize where it lives but must not rewrite native internals merely for uniformity.

## Portable instructions

CCA uses `AGENTS.md` as an existing portable convention where applicable. It does not declare AGENTS.md universally authoritative over every harness/upstream instruction system.

- Preserve nested AGENTS.md scope.
- AGENTS.md has no CCA-required heading schema.
- Do not assume AGENTS.md overrides harness-specific discovery/precedence.
- Preserve one substantive source of truth; use verified bridges/includes when they avoid duplicated rules.
- On native ICM, preserve native ICM instruction/entry semantics. Add portable guidance only as compatible hardening.

## Routers and local contracts

A CCA-aware consumer resolves router/contract **roles**, then uses their bindings.

Outside upstream-native profiles, concrete names may vary when the applicable CCA/custom/profile contract declares them. Do not assume `CONTEXT.md` merely because it is a common/default name.

Inside upstream-native ICM, keep exact upstream filenames and contract shape.

Routers should route rather than accumulate unrelated payload. Local working contracts should define only the job/inputs/process/outputs/checks required by their governing profile.

## Knowledge invariants

For LLM Wiki compatibility, discover the implementation's own schema first. The core behavior is persistent maintained synthesis over durable source material.

CCA may optionally harden knowledge systems with capture, preserved evidence, human notes, synthesis, indexes, provenance, contradiction/supersession, lifecycle, integrity, or logs. Those remain CCA/profile choices unless an upstream requires them.

When human methods coexist with maintained synthesis:

- determine authority before writing;
- do not silently reinterpret human-authored notes as agent-maintained synthesis;
- keep preserved evidence distinct from cleaned/synthesized knowledge;
- prefer explicit supersession/provenance over silent source rewrites;
- use derived indexes/caches for scale without making them the only canonical knowledge surface.

## CCA file/semantic roles

Roles classify function; they do not mandate locations.

| Role | Function |
|---|---|
| catalog/router | routes to other context with little substantive payload |
| contract | defines one unit/folder of work |
| factory | stable constraints, references, templates, reusable capabilities |
| source/reference | preserved evidence/input |
| synthesis | maintained derived knowledge |
| product/output | working or shipped artifact |
| chronicle | historical/maintenance record |
| state | operational state |

Inside native ICM, preserve upstream Layer-3 reference/factory versus Layer-4 working/product distinctions. Generic CCA vocabulary describes interoperability; it does not replace native meanings.

## Context discipline

- Route before loading/searching broadly.
- Load minimum sufficient context.
- Select exact sections when full files are unnecessary.
- Keep stable constraints in canonical homes rather than copy them into every router.
- Previous outputs are artifacts, not authoritative quality templates.
- Infer ordinary filesystem semantics when safe; do not require manifests merely to restate obvious paths.
- If a task requires excessive unrelated context, improve routing before increasing prompt size.

## Agent Skills discipline

CCA ships one self-contained `cca` Agent Skill with seven lazy modes. `skills/cca/` is the portable distribution boundary.

- keep `SKILL.md` compact enough for activation/routing;
- progressively load skill-local `references/`, `assets/`, and scripts/tools;
- implementation dependencies required by advertised behavior remain inside the skill package, except declared external runtime libraries/tools;
- never depend on removed sibling CCA skill directories or repository-global implementation files;
- coordinate operations semantically by mode name rather than filesystem package coupling;
- profiles are workspace contracts, not additional modes.

The optional Hybrid Workspace Profile bundles its schema/templates/generator/audit/tests under `assets/hybrid-workspace/` and always operates on an explicit target outside the installed tool package.

## Fresh-agent walk test

For CCA-conformant/structured targets that claim this portability property, a fresh agent should be able to:

1. **Orient** — identify boundary, applicable authority/profile, and routed context from durable files.
2. **Act** — resolve the required semantic role/binding and perform one representative operation with minimum sufficient context.
3. **Report** — state what changed, what remains, and what is ambiguous from durable state.

This test is supplemental. It never replaces stricter upstream-native or named-profile acceptance.

If a required decision exists only in chat history or someone's head, durable context is incomplete.

## Upstream-change rule

CCA MUST adapt or explicitly version/pin a mapping when an upstream change affects a supported compatibility claim. CCA SHOULD converge toward a materially better upstream solution to the same problem, and MUST NOT preserve an inferior CCA-specific convention merely because it was introduced first.
