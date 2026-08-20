# Design principles behind CCA

Explanatory, not normative. Normative semantics live inside the installable skill at [`../skills/cca/references/core/spec.md`](../skills/cca/references/core/spec.md). Compatibility claims live in [`../skills/cca/references/core/compatibility.md`](../skills/cca/references/core/compatibility.md). If this document conflicts with those references or a supported upstream's current primary authority, the normative/upstream authority wins.

## 1. Augmentation is the objective

> **Automation is the means; augmenting human capabilities is the goal.**

CCA should increase human agency, comprehension, portability, and effective capability while reducing unnecessary human toil and machine work. Human-centered does not mean forcing humans to perform work an agent can safely automate; it means preserving inspectability, authority, provenance, and the ability to steer/override durable outcomes.

## 2. Converge instead of inventing

CCA should use existing standards, methodologies, protocols, and proven conventions where they already solve the problem well.

When an upstream changes in a way that affects CCA compatibility, CCA adapts or versions/pins the mapping. When a better upstream solution emerges, CCA should converge toward it rather than preserving a weaker CCA-specific convention for historical pride.

## 3. Stable semantics, replaceable bindings

CCA separates meaning from implementation:

```text
boundary + semantic role -> binding
```

Semantic roles remain stable while concrete paths or implementations may change where the governing contract permits it. This is the same engineering principle as stable interfaces over replaceable implementations.

A default path is not identity merely because it is convenient.

## 4. Route the right context, not bigger prompts

Large context windows do not make irrelevant material useful. Resolve the applicable boundary, authority, semantic role, and binding before searching broadly.

CCA therefore prefers:

```text
boundary
  -> authority/instructions
  -> semantic role
  -> binding/router
  -> local catalog/contract/index
  -> targeted search
  -> optional derived index
  -> broad search fallback
```

## 5. The environment carries durable context

When instructions, knowledge, state, contracts, and provenance live in durable filesystem-native form, short human intent can be enough. Agents navigate the environment instead of requiring the user to repeatedly reconstruct the operating model in prompts.

## 6. Persistent synthesis where knowledge should compound

Some knowledge work benefits from maintained synthesis that survives sessions. CCA adopts the useful core of LLM Wiki without assuming every knowledge problem needs a wiki or that retrieval becomes obsolete.

Preserved evidence, human notes, and maintained synthesis are different epistemic roles and should not be silently collapsed.

## 7. Start with the workflow, not the agent

When work is sequential, decompose the real process and handoffs first. ICM provides a strong proven methodology for explicit routing, local contracts, selective context loading, one-way dependencies, and durable output handoffs.

CCA should use native ICM directly when native ICM is the right solution. Borrowed ICM patterns remain ICM-derived unless the full upstream-native profile passes.

## 8. Durable artifacts are human edit surfaces

Human review should be able to occur on inspectable durable artifacts rather than only in chat history. A later agent should consume the artifact the human actually left behind.

## 9. Configure the factory, not every product

Stable preferences, constraints, schemas, templates, and rules belong in durable canonical homes. Repeated manual correction is evidence that the durable system may need improvement.

## 10. Context packages before platforms

Plain files are often enough for durable context. Add databases, indexes, MCP, orchestration, messaging, transactions, or services when they solve a real capability/scaling problem rather than because infrastructure looks more sophisticated.

## 11. Build outcomes, not AI features

Use deterministic scripts/tools for deterministic work. Use models where reasoning/generation adds value. Evaluate the result in human outcomes such as quality, speed, cost, reliability, understanding, and decision leverage.

## 12. Stable context plane, replaceable execution plane

Durable context should survive changes in model vendor, harness, runtime, or orchestration system. Host-specific adapters are replaceable implementations, not the canonical home of CCA semantics.

## 13. One portable skill, multiple lazy modes

CCA is distributed as **one self-contained `cca` Agent Skill with seven modes**: `architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`, and `advise`.

Progressive disclosure comes from mode-specific skill-local references/assets/scripts, not from splitting one semantic authority across separately installable CCA packages.

`skills/cca/` is therefore the portable distribution boundary: repository docs may explain CCA, but installed meaning cannot depend on repository-global files.

## 14. Modes and profiles are different dimensions

A mode describes what the agent is doing. A profile describes an optional workspace contract.

The CCA Hybrid Workspace Profile is not an eighth mode. Existing modes architect it, scaffold it, sync it, query/ingest through its semantic bindings, and lint it.

## 15. Compose boundaries; do not flatten methods

PARA, Zettelkasten, BASB/CODE, ICM, LLM Wiki, coding repositories, delivery methods, and other systems solve different concerns.

An outer method may organize where a nested boundary lives without becoming authoritative for the nested boundary's internal semantics.

## 16. Infer ordinary structure before declaring metadata

Do not create a manifest merely to restate obvious filesystem paths. Explicit metadata should capture semantic/authority/binding facts that cannot safely be inferred or that an adopted profile/upstream explicitly requires.

The optional Hybrid Workspace Profile intentionally uses `WORKSPACE.yaml` as its machine-readable bootstrap because that profile needs configurable semantic bindings and deterministic validation. That choice is profile-specific, not universal CCA.

## 17. Derived state should remain derived

Indexes, dashboards, routers, caches, reports, and generated specifications should be reproducible from canonical sources where practical. A derived artifact should not silently become the authoritative source of truth.

## 18. Collaboration/runtime infrastructure is a separate layer

Filesystem-native durable context supports asynchronous handoffs, shared history, and inspectability. It does not replace message buses, schedulers, authorization systems, transactions, or high-concurrency runtime infrastructure.

CCA can sit beneath those systems as a durable context/interoperability layer.

## 19. Validate what can be deterministic

Checkable invariants should be mechanically validated rather than deferred entirely to model judgment. The Hybrid Workspace Profile carries its schema, generator, audit logic, and adversarial tests inside the installed skill for this reason.

## 20. Preserve upstream authority

- Native ICM remains governed by current ICM.
- LLM Wiki remains implementation-flexible unless a specific implementation/profile chooses stronger structure.
- AGENTS.md retains its own scoped-instruction convention.
- Agent Skills retains its own package/progressive-disclosure contract.
- Human methodologies remain independent methods.
- CCA-owned hardening/profile choices must be labeled as CCA choices.

CCA succeeds when interoperability increases without making upstream systems less themselves.
