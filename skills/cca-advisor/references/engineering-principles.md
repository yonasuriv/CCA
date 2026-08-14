---
scope: Artifact — how systems are structured, written, secured, and operated
read_when: Design, implementation, review, refactoring, architecture decisions, security posture, debugging a change that is expensive to make
skip_when: Planning, org design, delivery cadence, team structure, or any task where the question is about the process rather than the thing being built
companion: frameworks-and-methodologies.md — governs properties of the process; this file governs properties of the artifact
last_reviewed: 2026-08
---

# Engineering Principles

Priors for judgment, not gates for compliance.

## How to read this file

Every principle below was extracted from a specific context by someone solving a specific problem. None of them carry their original context with them. Applied without it, each one has a failure mode, and several of them fail by pulling directly against another principle in this same file.

So this is not a checklist and passing it is not a goal. Nothing here is a precondition for shipping. If you find yourself citing an entry as the reason a design is unacceptable, you have converted a heuristic into a rule and lost the reasoning that made it useful.

The working question for any entry is: **what does applying this buy me here, and what does it cost when the requirement changes?** If you can't answer both halves, you're applying it as ritual. Skip it.

When two entries conflict — and they will — the resolution is never "the more famous principle wins." It's a judgment about which cost is worse in this specific case, made explicit and moved past.

---

## The load-bearing few

Most of the vocabulary below is a restatement of a small number of ideas. When the detailed guidance is ambiguous or in conflict, fall back to these.

**Manage coupling.** The cost of a change is the number of places it forces you to touch and the number of things that can break silently when you do. Nearly every principle in this file is a tactic for reducing that number.

**Hide what is likely to change.** Stable things become interfaces. Volatile things go behind them. Getting this boundary right matters more than any structural rule about how the code is arranged.

**Make the wrong thing hard.** Prefer designs where invalid states can't be constructed, unsafe operations require deliberate effort, and the default path is the correct one. This outperforms documentation, review, and discipline.

**Keep feedback fast and truthful.** Fast tests, real observability, short deploy cycles. A system you can't observe or can't change quickly will be reasoned about incorrectly, no matter how well it was designed.

**Preserve the ability to change your mind.** Reversibility, migration paths, and small blast radius are worth more than getting the decision right the first time, because you won't.

Everything below is elaboration.

---

## Structure and design

Each entry: what it buys, what it costs when overapplied.

**Separation of concerns** — Isolates reasons to change. Overapplied, it scatters a single behavior across layers that must all be edited together.

**Modularity** — Bounds what you must understand at once. Overapplied, module count exceeds the complexity it was supposed to contain.

**Abstraction** — Lets callers ignore mechanism. Overapplied, the abstraction leaks and callers must now understand both it and what it hides.

**Encapsulation** — Protects invariants by controlling access. Overapplied, produces objects that are mostly pass-through delegation.

**Information hiding** — Confines the impact of a decision to one place. This is the most durable idea in this section; the cost is only that hiding the wrong thing is expensive to undo.

**Loose coupling** — Lets parts change independently. Overapplied, indirection replaces structure and nothing is traceable end to end.

**High cohesion** — Keeps things that change together in the same place. Directly limits how far you should take separation of concerns.

**Single responsibility** — One axis of change per unit. Overapplied at method granularity, it produces shotgun surgery — the exact failure it exists to prevent. Define responsibility at the level of the stakeholder or reason to change, not the operation.

**Composition over inheritance** — Avoids fragile base classes and unintended coupling through the hierarchy. Occasionally inheritance genuinely models the domain; the guidance is a default, not a prohibition.

**Dependency inversion** — Lets policy stay independent of mechanism. Overapplied, you get an interface per class and a stack trace no one can follow. Invert at boundaries you intend to swap, fake, or isolate — I/O, clocks, randomness, external services. Pure logic doesn't need it to be testable.

**Open/closed** — Extension without modification. Almost always recognized in hindsight. Building extension points before the second real use case is speculative generality.

**Interface segregation** — Callers depend only on what they use. Cost is interface proliferation; merge when the split isn't buying independence.

**Liskov substitution** — Subtypes honor the supertype's contract. This one has few downsides; violations are usually a signal the hierarchy is wrong.

**Design by contract** — Explicit pre/post-conditions and invariants. Valuable at module boundaries, heavy everywhere else.

**Stable interfaces** — Volatility belongs behind boundaries, not on them. Cost is that a wrong stable interface is expensive to correct.

**Explicit ownership and boundaries** — Someone owns each piece of state and each decision. Cost is friction at handoffs; that friction is usually cheaper than ambiguity.

**Make invalid states unrepresentable** — Push correctness into types and constructors so errors become impossible rather than caught. Cost is type-level complexity that can exceed the problem.

**Single source of truth** — One authoritative location per fact. Cost is a coordination point and sometimes a bottleneck; caches and projections are fine as long as authority is unambiguous.

**Minimize shared mutable state** — Removes whole categories of concurrency and ordering bugs. Cost is copying and plumbing.

---

## Writing and simplicity

**Simplicity / KISS** — The cheapest system to operate and change. Cost is that some problems are irreducibly complex and forcing simplicity onto them just hides the complexity somewhere worse.

**DRY** — Deduplicate *knowledge*, not text. Two code blocks that look alike but change for different reasons were never duplicates. Merging them couples unrelated callers through a shared helper that grows flags. Duplication is cheaper than the wrong abstraction; prefer waiting for a third occurrence, and inline an abstraction back out when it starts sprouting per-caller conditionals.

**YAGNI** — Don't build for requirements that haven't arrived. Directly opposes speculative applications of open/closed, extensibility, and abstraction. The counterweight is that some decisions are genuinely hard to reverse later — for those, thinking ahead is not speculation.

**Explicit over implicit** — Behavior visible at the call site. Costs verbosity, and directly opposes convention over configuration.

**Convention over configuration** — Reduces decisions and boilerplate. Costs discoverability and surprises anyone who doesn't know the convention. Choose based on how large and how transient the audience is.

**Principle of least astonishment** — Match the reader's existing model. Cost is that it anchors you to existing conventions even when they're bad.

**Progressive disclosure of complexity** — Simple things simple, complex things possible. Cost is maintaining two surfaces.

**Avoid premature optimization** — Preserves clarity and avoids optimizing the wrong thing. Not a license to ignore obvious algorithmic complexity or known-hot paths; the word doing the work is *premature*, not *optimization*.

**Measure before optimizing** — Intuitions about where time goes are usually wrong. Cost is the measurement setup, which is nearly always worth it.

**Optimize for change** — Design against the change you actually expect. Requires a real prediction; without one this collapses into speculative generality.

---

## Reliability and operations

**Fail fast** — Surface violated assumptions immediately. Directly opposes graceful degradation. Resolve by scope: fail fast on programmer errors and broken invariants, degrade on expected operational failures. Validate hard at trust boundaries, assume validity inside them.

**Graceful degradation** — Partial service beats none. Cost is that suppressing failures hides them; degradation must be observable or it becomes silent data corruption.

**Fault isolation** — Contain blast radius. Cost is duplication of infrastructure and resources.

**Idempotency** — Makes retries safe and recovery simple. Cost is key management and dedup storage. Nearly always worth it at boundaries that can be retried.

**Determinism where possible** — Reproducible behavior makes debugging tractable. Push nondeterminism (time, randomness, ordering, external calls) to the edges where it can be injected and controlled.

**Reversibility** — Every change should have a way back. Feature flags, migrations that work in both directions, deploys that roll back. Costs discipline; buys the freedom to be wrong.

**Observability** — You cannot operate what you cannot see. Costs cardinality, storage, and instrumentation effort. Under-observability is the more common failure by a wide margin.

**Testability** — Testable designs are usually well-factored designs. When testing requires exposing internals, that's a design signal, not a reason to break encapsulation.

**Automate repetitive work** — Consistency and reclaimed time. Cost is a second system to maintain; automation of a process that changes weekly is a liability.

**Preserve provenance and traceability** — Know where a value came from and why a decision was made. Costs metadata and storage; irreplaceable during incidents and audits.

---

## Security

**Principle of least privilege** — Limits what a compromise can reach. The real-world cost is permission sprawl, and the resulting failure is someone granting a wildcard at 3am to unblock a deploy — worse than a moderately scoped policy nobody feels compelled to bypass. Scope by role and lifecycle, make escalation fast and audited, and use time-bounded elevation as the pressure valve.

**Defense in depth** — No single control is load-bearing. Cost is operational complexity and the false confidence of many weak layers standing in for one strong one.

**Secure by default** — The out-of-the-box configuration is the safe one. Cost is friction for legitimate use, which drives workarounds if it's too high.

**Validate at trust boundaries** — Untrusted input is normalized and checked once, at the edge, and treated as trusted inside. Validating everywhere is noise; validating nowhere is the bug.

---

## Change and longevity

**Maintainability** — Optimize for the reader, who will usually be someone else with less context.

**Extensibility** — Anticipated growth without rewrite. Guard hard against building this before a real second case exists.

**Portability** — Freedom to move. Costs abstraction layers over things you may never move; price it against the actual probability.

**Interoperability** — Standard formats and protocols over bespoke ones. Cost is fitting to a standard that doesn't quite match your domain.

**Backward compatibility** — Consumers don't break on your schedule. Cost is accumulated surface you can never remove. Set explicit deprecation policy up front or this compounds forever.

---

## Where these actively conflict

Naming the tension is more useful than resolving it in advance, because the resolution is context-dependent every time.

| Tension | Failure when one side wins absolutely |
|---|---|
| DRY vs. loose coupling | A shared helper couples unrelated callers and grows a flag per caller |
| DRY / open-closed vs. YAGNI | Plugin architecture serving exactly one plugin |
| SRP vs. cohesion and KISS | Behavior fragmented across files that always change together |
| Dependency inversion vs. simplicity | Interface per class, unfollowable traces, DI container as the real architecture |
| Explicit vs. convention over configuration | Either ceremony everywhere or invisible magic |
| Fail fast vs. graceful degradation | Crashing under normal load, or silently corrupting under abnormal load |
| Least privilege vs. operability | Emergency wildcard grants routing around the whole model |
| Encapsulation vs. testability | Internals exposed for tests, or behavior tested through a keyhole |
| Backward compatibility vs. simplicity | Permanent support surface, or broken downstream consumers |
| Loose coupling vs. cohesion at service scale | Distributed monolith: independently deployable in theory, lockstep in practice |
| Abstraction vs. least astonishment | Elegant model no one can predict the behavior of |
| Optimize for change vs. YAGNI | Flexibility built for a future that arrives in a different shape |

---

## Using judgment

**Deviation is expected.** These are priors. Local evidence beats a prior. A constraint the author of a principle never encountered — a hard latency budget, a regulatory requirement, a language that makes the idiomatic form impossible, a codebase whose existing convention is more valuable than the improvement — is sufficient reason to depart.

**State the trade, don't argue the principle.** When departing, the useful artifact is one line about what was traded and what would make it worth revisiting: *chose duplication over a shared helper because the two callers are on different release cycles; merge if they converge.* Not a justification, a note for whoever hits it next.

**Weight by reversibility.** Cheap-to-reverse decisions get made quickly and revised on evidence. Expensive-to-reverse ones — data models, public interfaces, service boundaries, security posture — deserve more of this file's attention up front. Spending equal deliberation on both is a waste in one direction and a risk in the other.

**Weight by lifespan and audience.** A script read once by its author and a library consumed by twenty teams warrant almost none of the same principles. Most of this file assumes the second case.

**Signs you're applying this document as ritual:** an abstraction with one implementation; a rule cited without a cost; structure added that no requirement asked for; a change that improved conformance to this file without improving anything else; a decision defended by the name of a principle rather than by what it prevents.

The measure of any application of any principle here is whether the next change gets cheaper. If it doesn't, the principle wasn't the point.
