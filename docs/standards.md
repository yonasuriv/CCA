# Standards and upstreams

Explanatory maintenance surface. Normative compatibility semantics live inside the installable skill at [`../skills/cca/references/core/compatibility.md`](../skills/cca/references/core/compatibility.md) and [`../skills/cca/references/core/spec.md`](../skills/cca/references/core/spec.md).

## Foundations

CCA applies established software-engineering principles to context architecture:

- separation of concerns;
- explicit boundaries/interfaces;
- canonical authority / one fact, one home;
- loose coupling and high cohesion;
- stable interfaces/semantics over replaceable implementations/bindings;
- progressive disclosure and minimum sufficient context;
- least privilege;
- recoverability and explicit supersession;
- derived state over duplicated state;
- deterministic validation where practical;
- graceful fallback;
- portability and agnosticism.

The CCA resolution primitive is:

```text
boundary + semantic role -> binding
```

## Tracked upstreams

| Upstream / standard | What CCA uses | CCA rule |
|---|---|---|
| [ICM / Model Workspace Protocol](https://github.com/RinDig/Interpretable-Context-Methodology) | filesystem-native routing, layered context, contracts, selective loading, handoffs, canonical sources, human review | A valid native ICM workspace is CCA-compatible without structural migration. Native ICM remains governed by current upstream ICM. |
| [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | persistent maintained synthesis over durable source material | Preserve implementation flexibility; CCA hardening/profile choices must not be relabeled as LLM Wiki requirements. |
| [AGENTS.md](https://agents.md) | portable scoped agent guidance | Preserve the standard's scoped behavior; CCA does not invent a competing portable filename or universal harness precedence. |
| [Agent Skills](https://agentskills.io) | portable `SKILL.md` capabilities with progressive disclosure | `skills/cca/` remains a valid, self-contained Agent Skill distribution; implementation resources stay skill-local. |
| [MCP](https://modelcontextprotocol.io) | optional tool/context transport | Adjacent infrastructure, not required by CCA and not replaced by CCA. |

## Human methods and engineering methods

CCA can compose with independent methods such as:

- BASB/CODE;
- PARA;
- Zettelkasten;
- GTD, timeboxing, Pomodoro, Eisenhower;
- Scrum, Kanban, XP, DevOps;
- SAFe, LeSS, Disciplined Agile;
- TDD, MDE, RAD, IID, Lean Software Development, RUP/UP;
- PSP/TSP;
- SEMAT;
- other relevant organizational, engineering, delivery, research, or knowledge-work methods.

CCA does not absorb these methods or manufacture filesystem taxonomies that pretend to implement them. It preserves their scopes and maps how their authorities/artifacts interact with filesystem-native context.

## Core rule

**Convergence over invention.**

CCA MUST preserve supported upstream authority when claiming compatibility. It MUST NOT silently redefine an upstream merely to make the ecosystem appear uniform.

If an existing workspace is already clear, navigable, maintainable, and interoperable, doing nothing is a valid CCA outcome.

## Compatibility vocabulary

- **Upstream-native** — passes the upstream's own current rules.
- **CCA-compatible** — CCA resolves and operates without structural migration or semantic replacement.
- **CCA-conformant** — explicitly adopts normative CCA interoperability semantics.
- **Profile-conformant** — satisfies a named optional CCA-owned profile.
- **CCA-hardened** — optional CCA capabilities added without invalidating native semantics.
- **ICM-derived** — selected ICM patterns used without claiming upstream-native ICM.

An upstream-native system can be CCA-compatible without becoming CCA-conformant.

## ICM authority

For upstream-native ICM claims, current upstream ICM is the authority. CCA's local compatibility material is a mapping/operational aid, not a fork.

CCA must preserve current applicable ICM requirements such as its native entry/routing layers, exact contract representation, naming, handoff/dependency semantics, selective loading, canonical-source discipline, setup/status behavior, onboarding/placeholder rules, tooling, checkpoints/audits/value validation, shared constants, quality guardrails, restructure move-safety (including workspace-root durability confirmation, referrer discovery, case-fold checks, copy-verify-remove discipline, and post-move verification), System Map inbound/reverse-walk behavior, and workspace-builder-equivalent acceptance where applicable.

If upstream ICM changes any of these, CCA must re-verify the primary source and adapt/version its mapping rather than freezing stale local wording.

CCA does **not** declare `AGENTS.md` universally authoritative over native ICM `CLAUDE.md`. Portable AGENTS.md guidance may coexist as interoperability hardening, but native upstream semantics remain native.

## Agent Skills distribution

CCA uses one installable `cca` skill with seven modes:

`architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`, `advise`.

Progressive disclosure is achieved through the existing `references/`, `assets/`, and other skill-local resources rather than separate CCA skill packages.

The optional Hybrid Workspace Profile is bundled within this one skill. It is a profile, not a mode.

## Upstream-change rule

When a supported upstream changes:

1. verify the current primary authority;
2. identify which CCA mapping/compatibility claim is affected;
3. CCA **MUST** update or explicitly version/pin the affected mapping;
4. CCA **SHOULD** converge toward a materially better upstream solution to the same problem, provided CCA's core principles remain intact;
5. CCA **MUST NOT** preserve an inferior CCA-specific convention merely because it was introduced first;
6. update the skill-local specification/compatibility/modes/assets/tests first, then explanatory repository docs/examples;
7. rerun CCA regression gates and the upstream's own acceptance checks for any upstream-native claim.

This is the mechanism by which CCA remains evolving and agnostic rather than becoming another frozen competing methodology.
