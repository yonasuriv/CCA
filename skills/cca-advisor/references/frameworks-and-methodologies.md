---
scope: Process — how work is selected, coordinated, validated, and delivered
read_when: Planning, org design, process change, delivery cadence, team structure, methodology disputes
skip_when: Implementation, debugging, code review, or any task where the question is about the artifact rather than the process producing it
companion: engineering-principles.md — governs properties of the artifact; this file governs properties of the process
last_reviewed: 2026-08
---

# Frameworks and Methodologies

Priors for choosing and combining ways of working, not a process to follow.

## How to read this file

Every framework, methodology, process, and approach below was created to solve a particular class of problems under particular assumptions. None is a universal operating model.

They do not all compete with one another. Some govern organizations, some coordinate teams, some shape engineering work, some discipline individual practice, and some exist specifically to describe or compose other methods. Every entry is tagged with its scope for this reason: the most damaging error in this space is not picking the wrong method, it is picking a method at the wrong altitude — installing an enterprise operating model to fix a team scheduling problem, or expecting a single engineering practice to resolve cross-team dependencies.

This is not a maturity ladder, a menu from which one winner should be selected, or a recipe for combining everything.

The working question for any entry is: **what problem does this solve here, what assumptions does it make, and what does adopting it cost?** If you cannot answer all three, adopting it because it is popular, certified, "agile," enterprise-grade, or already used elsewhere is cargo culting.

When approaches conflict — and they will — the resolution is not "the more comprehensive framework wins." Use the smallest amount of process that addresses the actual constraint, preserve the useful boundaries between approaches, and make the trade explicit.

---

## The load-bearing few

Most of the approaches below are different answers to a small number of recurring problems. When names and frameworks become noise, fall back to these.

**Shorten the feedback loop.** Discover wrong assumptions while they are still cheap to change. Iterations, tests, prototypes, deployments, reviews, flow metrics, and retrospectives are different mechanisms for getting reality back into the decision process sooner.

**Make work and constraints visible.** Hidden queues, dependencies, defects, assumptions, ownership, and bottlenecks do not disappear because a process ignores them. A useful method exposes enough of the system to reason about it.

**Match coordination to scale.** A five-person team and a hundred-team organization do not have the same coordination problem. Adding enterprise machinery to a small team is waste; pretending a large organization is merely many independent small teams ignores dependencies that already exist.

**Separate intent from mechanism.** The outcome matters more than the ceremony used to reach it. A sprint, board, test, model, release train, metric, or retrospective is useful only while it produces the feedback or coordination it exists to provide.

**Adapt the method to the context.** Methods encode assumptions. Context decides whether those assumptions hold. Tailoring is not failure to implement a method correctly; sometimes refusing to tailor it is.

Everything below is elaboration.

---

## Framing the problem before choosing

Most of this file assumes you already know what kind of problem you have. That assumption is usually wrong, and it is where method selection actually fails.

### Cynefin

**Scope:** Sense-making — sits above every entry below

Cynefin is a sense-making framework distinguishing domains by the relationship between cause and effect: **clear** (obvious causal relationships, best practice applies), **complicated** (knowable through analysis or expertise, good practice applies), **complex** (causality is only visible in retrospect, requires safe-to-fail probing), and **chaotic** (no discernible causality, requires action first to establish stability). It also names **confusion** — not knowing which domain you are in, which is the most common starting state.

**What it buys:** a vocabulary for the judgment every other entry silently depends on. Iterative, experiment-driven approaches assume complexity. Planning-heavy, sequential approaches assume the problem is complicated but knowable. Applying either where its causal assumption does not hold is the root of most methodology failure.

**What it costs when overapplied:** domain classification becomes a debate rather than a decision, or a single project is forced into one domain when different parts of it genuinely sit in different ones.

The practical use is narrow and worth it: before naming a method, decide whether the problem is knowable in advance or only discoverable by acting.

### Sequential vs. iterative as an explicit choice

The catalog below leans heavily iterative, which reflects where most contemporary software work sits — not a claim that sequential delivery is always wrong. Treat the choice as live. Sequential delivery earns its place where requirements are genuinely fixed and externally specified, where the cost of a wrong increment is not recoverable, where certification or safety evidence must be produced in a defined order, or where delivery is coupled to hardware, contract, or regulatory milestones that do not move.

Where any of those hold, an iterative method will produce iteration theatre: cycles that repeat without incorporating feedback, because there is no mechanism by which feedback can change the plan.

---

## Organizational scale and coordination

These approaches primarily address coordination beyond a single delivery team.

### SAFe — Scaled Agile Framework

**Scope:** Organization / operating model

SAFe provides an explicit operating structure for coordinating strategy, portfolios, programs, products, and delivery across large organizations. It introduces defined coordination mechanisms, planning horizons, roles, and synchronization points intended to align many teams around shared value delivery.

**What it buys:** common planning structures, cross-team synchronization, portfolio visibility, explicit coordination of dependencies, and a recognizable operating model for organizations where decentralized team-level practices alone do not resolve enterprise-scale coordination.

**What it costs when overapplied:** organizational machinery becomes the product. Roles multiply, planning events become compliance ceremonies, local teams lose decision authority, and "agility" becomes conformance to the framework rather than responsiveness to evidence. The structure can make existing bureaucracy more legible without making it smaller.

Use it because the coordination problem exists, not because the organization is large.

### LeSS — Large-Scale Scrum

**Scope:** Organization / multi-team product

LeSS extends Scrum to multiple teams working on one product while deliberately trying to preserve the simplicity of one-team Scrum. It emphasizes a single product, one Product Backlog, shared product ownership, feature teams, and organizational simplification rather than adding progressively more coordination layers.

**What it buys:** scaling with comparatively little additional process, strong product-level alignment, reduced organizational silos, and pressure to solve structural problems rather than coordinate around them indefinitely.

**What it costs when overapplied:** simplicity itself becomes dogma. Organizations with regulatory boundaries, genuinely separate products, strong specialist constraints, or unavoidable portfolio structures can spend more effort pretending those boundaries do not exist than managing them explicitly. LeSS also asks for organizational change that may be considerably harder than adopting new ceremonies.

Its most valuable question is often not "how do we coordinate all these teams?" but **"why do we need this much coordination?"**

### DA — Disciplined Agile

**Scope:** Organization / process selection

Disciplined Agile is a context-sensitive decision framework and knowledge base for choosing and evolving a way of working rather than prescribing one fixed process. It deliberately draws from Agile, Lean, traditional, and other approaches and treats process selection as contextual. It has been under PMI stewardship since 2019; check current positioning before assuming its independent trajectory.

**What it buys:** explicit acknowledgment that different contexts require different practices, a vocabulary for process choices, and guidance for composing a way of working without pretending one lifecycle fits every organization.

**What it costs when overapplied:** choice becomes its own form of complexity. A sufficiently large catalog can move the problem from "which framework should we follow?" to "which combination of hundreds of practices should we choose?" Tailoring without clear evidence can also become a sophisticated justification for keeping whatever the organization already does.

The useful part is **guided choice**. Lose the guidance and you have a catalog; lose the choice and you have another prescriptive framework.

### Sequential delivery — waterfall, stage-gate, V-model

**Scope:** Organization / project lifecycle

Sequential approaches complete defined phases in order, with review or approval gates between them. The V-model pairs each specification phase with a corresponding verification phase, which is why it persists in safety-critical, automotive, medical device, and defense contexts where traceability from requirement to test evidence is itself a deliverable.

**What it buys:** contractual clarity, auditable traceability, predictable budgeting against fixed scope, coordination with non-software dependencies that cannot be re-planned mid-flight, and a documentation trail that some regulatory regimes require regardless of how the software was actually built.

**What it costs when overapplied:** assumptions harden before they have been tested. Feedback arrives after the cost of acting on it has become prohibitive, integration risk is deferred to the end, and the plan becomes a thing to defend rather than a thing to learn from. Applied to genuinely uncertain problems, it converts discovery into scope change and scope change into conflict.

Most real work is a hybrid: sequential at the contract and compliance boundary, iterative inside it. Name which layer you are in, because the failure mode is applying one layer's assumptions to the other.

---

## Team delivery

These primarily organize how teams select, coordinate, inspect, and deliver work.

### Scrum

**Scope:** Team / framework

Scrum is a lightweight framework for complex work built around empiricism, defined accountabilities, artifacts, events, and repeated inspection and adaptation.

**What it buys:** a regular feedback cadence, explicit product ownership, a small set of coordination events, bounded planning horizons, and repeated opportunities to inspect both the product and the way the team works.

**What it costs when overapplied:** every problem becomes a Scrum problem. Events survive after their feedback function disappears, velocity becomes a performance metric, arbitrary work is forced through sprint boundaries, and teams optimize for completing the sprint rather than delivering value.

A Daily Scrum that exists because Scrum says so is a meeting. A Daily Scrum that changes what the team does today is a feedback mechanism.

### Kanban

**Scope:** Team / flow strategy

Kanban is a strategy for optimizing the flow of value through a process. Its core mechanisms include making work visible, explicitly controlling work in progress, and using evidence about flow to improve the system. The current Kanban Guide deliberately presents itself as minimal guidance that can coexist with other approaches.

**What it buys:** visibility into queues and bottlenecks, control over work in progress, flow-oriented metrics, incremental process change, and a way to improve delivery without requiring an entirely new organizational structure.

**What it costs when overapplied:** the board becomes the process. Cards move while systemic constraints remain untouched; teams optimize local cycle time at the expense of outcomes elsewhere; WIP limits become arbitrary rules instead of controls derived from the system.

Seeing work is not the same as understanding the system producing it.

### DSDM — Dynamic Systems Development Method

**Scope:** Team / project governance

DSDM is an Agile project-delivery framework with stronger project governance than many lightweight team methods. It combines iterative development with explicit roles, timeboxing, active business involvement, prioritization, and lifecycle guidance. The current Agile Business Consortium framework traces its lineage directly to DSDM.

**What it buys:** a bridge between iterative delivery and formal project governance, disciplined prioritization, clear business involvement, and structures useful where deadlines, budgets, organizational governance, and delivery teams must coexist.

**What it costs when overapplied:** governance consumes the adaptability it was intended to support. Roles and lifecycle artifacts accumulate, prioritization frameworks become mechanical, and timeboxing is preserved even when the nature of the work no longer benefits from it.

The project structure is useful where there is actually a project to govern.

### FDD — Feature-Driven Development

**Scope:** Team / decomposition and planning

Feature-Driven Development organizes software development around small, client-valued features and short design-and-build cycles, historically combining domain modeling with feature-oriented planning and delivery. It is one of the established pre-Manifesto Agile methods.

**What it buys:** concrete decomposition of large systems, visible progress at feature granularity, regular delivery, and a useful connection between domain understanding and implementation planning.

**What it costs when overapplied:** the feature becomes the unit of value whether or not it should be. Teams drift toward feature factories, systemic work becomes difficult to represent, and an early domain model can gain authority long after evidence has invalidated it.

A feature is a useful unit of work, not proof that the work is useful.

### ASD — Adaptive Software Development

**Scope:** Team / lifecycle under uncertainty

Adaptive Software Development was created for high-change, uncertain software environments and treats adaptation and learning as normal rather than exceptional. Its central cycle is commonly expressed as **speculate, collaborate, learn**. Jim Highsmith created ASD before becoming one of the Agile Manifesto authors.

**What it buys:** explicit permission to treat plans as hypotheses, strong emphasis on collaboration, and a lifecycle built around learning rather than pretending uncertainty can be planned away.

**What it costs when overapplied:** adaptability becomes an excuse for vagueness. If speculation has no constraints, collaboration no decision structure, and learning no observable evidence, uncertainty is merely being renamed rather than managed.

Plans being provisional does not make planning optional.

### XP — Extreme Programming

**Scope:** Team / engineering practices

Extreme Programming is an Agile software-development framework with unusually strong emphasis on concrete engineering practices. Its practices include short feedback cycles and techniques such as test-first development, continuous integration, refactoring, simple design, collective ownership, and pair programming.

**What it buys:** tight technical feedback, continuously changeable code, quality built into development rather than inspected afterward, shared understanding, and engineering practices capable of supporting frequent change.

**What it costs when overapplied:** practices become identity tests. Pairing, TDD, collective ownership, or continuous integration are defended because they are XP rather than because they improve the system. The social and technical discipline required can also be substantial.

XP is strongest when its practices reinforce one another. Selecting the visible ceremonies while dropping the engineering discipline loses much of the point.

### RAD — Rapid Application Development

**Scope:** Team / delivery approach

RAD emphasizes rapid, iterative development, prototyping, timeboxing, and frequent user feedback rather than long sequential specification and construction phases. Its early formulation helped establish the use of timeboxed iterative development.

**What it buys:** fast validation of requirements, short distance between users and implementations, early visibility of the product, and reduced investment in assumptions that have not yet survived contact with users.

**What it costs when overapplied:** speed borrows from the future. Prototypes silently become production systems, architecture receives only local attention, non-functional requirements arrive late, and rapid visible progress hides accumulating operational or structural debt.

Fast feedback is valuable. Fast construction without feedback is merely fast construction.

### IID — Iterative and Incremental Development

**Scope:** Team / development strategy

Iterative and incremental development builds a system through repeated cycles while growing the delivered system in usable increments. It is a broad development strategy rather than a single branded methodology and predates many modern Agile frameworks.

**What it buys:** earlier integration, staged risk reduction, repeated opportunities to learn from working software, and the ability to change direction before the entire system depends on the original plan.

**What it costs when overapplied:** iteration becomes a calendar artifact. Teams run a sequence of miniature waterfalls, increments are independently "complete" but do not form a coherent architecture, or work is arbitrarily sliced simply to fit an iteration.

The value comes from incorporating feedback between iterations, not from repeating the same process several times.

---

## Cross-cutting philosophies

These are not delivery methods. They supply the reasoning other methods apply.

### Lean

**Scope:** Cross-cutting / systems thinking

Lean thinking applied to software and knowledge work emphasizes value, flow, quality, learning, reduction of waste, and continuous improvement. Lean itself is broader than software and explicitly focuses on creating needed value with fewer resources while continually learning from the work. Kanban's flow orientation and much of DevOps' systems framing descend from it.

**What it buys:** system-level attention to flow, pressure to remove work that does not contribute value, shorter queues, built-in quality, and an orientation toward continuous improvement rather than process conformance.

**What it costs when overapplied:** "waste" is defined too narrowly. Slack, exploration, documentation, redundancy, training, or resilience are removed because they do not produce immediate visible output, leaving a locally efficient system that is globally fragile.

Unused capacity can be waste. So can a system with no capacity to absorb change.

---

## Lifecycle processes

### RUP / UP — Rational Unified Process / Unified Process

**Scope:** Project / configurable lifecycle process

The Unified Process family structures development as iterative, architecture-conscious, risk-oriented work across lifecycle phases. RUP is Rational/IBM's concrete and configurable process implementation, providing process guidance and tools around software-engineering practices.

**What it buys:** explicit architectural attention, early treatment of major risks, lifecycle coverage, disciplined requirements and design practices, and a process that can be tailored rather than requiring every project to use every artifact.

**What it costs when overapplied:** "tailorable" quietly becomes "everything included." Roles, artifacts, models, approvals, and tooling accumulate until iteration survives in name while execution behaves sequentially. The process description becomes more elaborate than the product-development problem.

RUP's weight is largely a property of how much of it you instantiate.

### DevOps

**Scope:** Organization and team / delivery and operations

DevOps joins software development and operations through shared responsibility, rapid feedback, automation, continuous delivery, observability, and organizational practices intended to make software delivery both faster and more reliable. DORA's long-running research treats delivery and operational capabilities as part of an interconnected organizational system rather than a tooling category.

**What it buys:** shorter path from code to production evidence, shared operational ownership, reproducible delivery, faster recovery, and the ability to improve development using information from real operation.

**What it costs when overapplied:** DevOps becomes a toolchain or job title. Teams inherit operational burden without the platform capabilities needed to carry it, automation accelerates a broken process, and "you build it, you run it" becomes a way to transfer infrastructure complexity rather than remove it.

Automation multiplies the properties of the process underneath it. Automating waste produces waste faster.

---

## Engineering practices

These shape how software itself is designed, implemented, or validated. They are practices, not operating models — adopting one does not require adopting a methodology around it.

### TDD — Test-Driven Development

**Scope:** Engineering practice

TDD tightly interweaves testing, coding, and design through a short test-first and refactoring feedback cycle.

**What it buys:** rapid executable feedback, pressure toward testable design, regression protection, and a mechanism for making assumptions concrete before implementation grows around them.

**What it costs when overapplied:** tests become architecture. Excessive mocking mirrors implementation details, refactoring requires rewriting the test suite, trivial behavior receives ceremonial tests, and passing unit tests creates confidence about properties they never measured.

A test is evidence about a property. It is not evidence about every property of the system.

### MDE — Model-Driven Engineering

**Scope:** Engineering paradigm

Model-driven approaches make models and transformations central engineering artifacts rather than treating diagrams merely as documentation. OMG's Model Driven Architecture is one concrete model-driven approach built around separating platform-independent concerns from platform-specific realization.

**What it buys:** higher-level representations, systematic transformation, reuse across target platforms, architectural separation of concerns, and the possibility of generating repetitive implementation from more stable models.

**What it costs when overapplied:** the modeling system becomes another software system that must itself be engineered. Toolchains, generators, metamodels, and domain-specific languages accumulate complexity; abstractions leak; and a model that no longer faithfully controls or describes the implementation becomes expensive fiction.

Raising the abstraction level only helps if the new abstraction is cheaper to maintain than what it hides.

---

## Individual and team process discipline

These focus less on choosing work and more on improving how individuals and teams perform it.

### PSP — Personal Software Process

**Scope:** Individual practice

PSP provides an individual engineer with a structured way to plan, measure, and improve personal software work using data about effort, size, defects, and quality.

**What it buys:** empirical knowledge about one's own work, improved estimation, deliberate defect prevention, and feedback based on personal evidence rather than intuition alone.

**What it costs when overapplied:** measurement becomes the work. Developers optimize what is recorded, tracking overhead exceeds the value of the data, individual metrics are misused for comparison, and Goodhart's law arrives wearing a spreadsheet.

Personal process data is feedback for the engineer, not a leaderboard for management.

### TSP — Team Software Process

**Scope:** Team practice

TSP extends disciplined measurement, planning, quality management, and process improvement to engineering teams, historically building on PSP and emphasizing self-directed teams and quantitative management.

**What it buys:** explicit team planning, quality ownership, measurable process improvement, clearer commitments, and a structured way for teams to reason about their own performance.

**What it costs when overapplied:** the cost of measuring and managing the process exceeds the uncertainty it removes. Quantitative targets harden into performance measures, adaptation becomes expensive, and teams operating in highly volatile environments spend disproportionate effort maintaining plans whose assumptions expire quickly.

Measurement should reduce uncertainty. If maintaining the measurement system creates more work than the uncertainty did, stop.

---

## Method engineering

### SEMAT / Essence

**Scope:** Meta / describing and composing methods

SEMAT — Software Engineering Method and Theory — emerged from an effort to establish a common ground for software-engineering methods. Its major standardized result is **Essence**, an OMG standard providing a kernel and language for describing, composing, comparing, and evolving engineering practices and methods.

**What it buys:** a shared vocabulary above individual methodologies, explicit representation of practices, the ability to compose methods without pretending they originated as one system, and a way to reason about common elements across otherwise incompatible process vocabularies.

**What it costs when overapplied:** the meta-model becomes the work. Teams describe how they work more precisely without improving how they work, simple practices acquire a translation layer nobody needed, and a vocabulary intended to make methodologies interoperable becomes another methodology demanding conformance.

A common language should make existing methods easier to understand together. If everything must first be rewritten into the common language before it can be used, interoperability has become assimilation.

---

## Where these actively conflict

Naming the tension is more useful than resolving it in advance, because the resolution depends on the scale, constraints, product, organization, and people involved. Some rows below are method against method; others are a method against a concern it structurally underweights.

| Tension | Failure when one side wins absolutely |
|---|---|
| SAFe coordination vs. LeSS/team autonomy | Enterprise dependencies remain unmanaged, or teams become execution units of central planning |
| LeSS simplification vs. real structural boundaries | Necessary boundaries are denied, or coordination machinery survives that simplification could have removed |
| DA contextual choice vs. organizational standardization | Every team invents a process, or one process is imposed where its assumptions do not hold |
| Sequential predictability vs. iterative discovery | Plans defended past their evidence, or no stable commitment where the contract requires one |
| Scrum cadence vs. Kanban continuous flow | Interrupt-driven work forced into artificial sprints, or useful inspection cadence disappears entirely |
| Scrum commitment vs. ASD adaptation | Plans become contracts, or plans become meaningless |
| Kanban local throughput vs. product outcomes | Cycle time improves while the thing being delivered does not |
| DSDM governance vs. lightweight team delivery | Governance dominates delivery, or necessary organizational controls are ignored |
| FDD feature decomposition vs. RUP/UP architectural attention | Feature throughput hides architecture, reliability, research, or platform work |
| XP practice coherence vs. selective adoption | Practices become ritual, or the feedback mechanisms that make rapid change safe are discarded |
| TDD isolation vs. system-level realism | Tests become fast but fictional, or feedback only arrives through slow end-to-end systems |
| MDE abstraction vs. direct implementation | The model becomes an expensive second system, or repeated low-level work ignores stable higher-level structure |
| RAD speed vs. architectural longevity | The prototype becomes permanent, or validation is delayed while speculative architecture is perfected |
| IID iteration vs. architectural coherence | Each increment works locally while the system fragments globally |
| Lean efficiency vs. resilience and slack | Slack is eliminated until the system cannot absorb variation or learning |
| RUP rigor vs. process economy | Lifecycle discipline becomes bureaucracy, or important risks and architectural decisions remain implicit |
| PSP/TSP measurement vs. professional judgment | Metrics replace reasoning, or useful empirical feedback is discarded because measurement is inconvenient |
| DevOps ownership vs. team cognitive load | Teams own production but also inherit every infrastructure concern |
| SEMAT common vocabulary vs. methodological independence | Methods become comparable, or they are flattened into a meta-model that erases distinctions worth preserving |

---

## Combining approaches

**Combination is expected.** These approaches operate at different scopes and many were designed to coexist with practices from elsewhere. A team might use Scrum for delivery cadence, XP engineering practices, Kanban to understand flow, DevOps for delivery and operations, and Lean reasoning about the whole system without those becoming one new methodology.

**Check scope before combining.** Two entries at the same scope usually compete; two at different scopes usually compose. Scrum and Kanban at team scope need a deliberate reconciliation. Scrum and TDD do not — one is a team framework, the other an engineering practice, and they never contest the same decision.

**Composition does not erase provenance.** If a practice comes from Scrum, XP, Kanban, Lean, DSDM, DA, or another source, retain enough of that context to understand the assumptions behind it. A borrowed ceremony with its reasoning removed is just choreography.

**Overlap is not equivalence.** Two approaches may both discuss iteration, flow, quality, feedback, or teams while meaning materially different things by them. Similar vocabulary is not sufficient reason to collapse them.

**Use the narrowest sufficient mechanism.** Do not install an enterprise framework to solve a team scheduling problem. Do not impose a delivery methodology to obtain one engineering practice. Do not build a meta-method because two teams use different names for the same artifact.

**Preserve local authority.** A framework remains authoritative for the concepts it defines. Integration should map or coordinate those concepts where useful, not silently redefine them to fit another framework's vocabulary.

**Prefer evidence over methodological purity.** If the mechanism is not producing the outcome for which it was adopted, inspect the assumptions before increasing compliance.

---

## Using judgment

**Deviation is expected.** A methodology captures accumulated experience, not the future state of every project. Local constraints, regulation, organizational structure, system criticality, team maturity, product uncertainty, and operational reality are sufficient reasons to adapt.

**State the problem before naming the method.** "We need SAFe," "we should use Scrum," or "this should be Kanban" are conclusions. Start with the coordination, feedback, quality, flow, uncertainty, or governance problem that led there — and with whether that problem is knowable in advance or only discoverable by acting.

**Adopt mechanisms, not brands.** If limiting work in progress solves the problem, you may not need a Kanban transformation. If test-first development improves a component, you do not need to become an XP organization. If several teams need synchronized planning, that alone does not establish the need for an enterprise framework.

**Weight adoption by reversibility.** Trying a retrospective format for two weeks is cheap. Reorganizing hundreds of people around a scaling model is not. The harder an adoption is to reverse, the stronger the evidence it should require.

**Weight process by coordination cost.** Process exists partly because people must coordinate. As the number and significance of dependencies rise, explicit coordination becomes more valuable. As they fall, the process coordinating them should disappear with them.

**Do not optimize for framework compliance.** A perfectly implemented methodology producing the wrong outcome is a failed implementation of work.

**Signs you're applying this document as ritual:** debating whether something is "real Scrum" instead of whether it works; adding roles because a diagram contains them; preserving meetings after their feedback value disappears; rejecting a useful practice because it originated in another method; measuring process conformance instead of outcomes; combining frameworks until every possible practice has somewhere to live; or inventing a new methodology whose primary purpose is to reconcile the existing ones.

**The measure.** Whether the work gets easier to understand, coordinate, change, validate, and deliver — and that has observable proxies. Lead time from commit to production, deployment frequency, change failure rate, and time to restore service cover delivery health. Coordination cost per unit of delivered change covers the rest: if a process addition does not reduce the number of people, meetings, or handoffs required to ship a given change, it is not paying for itself.

If removing it improves those numbers, remove it.
