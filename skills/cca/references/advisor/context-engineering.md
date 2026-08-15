---
scope: Context — what gets constructed before a model sees anything, and how
read_when: Designing prompt systems, RAG pipelines, knowledge bases, multi-step workflows, agent context routing, or any system where what the model receives is itself an engineering artifact
skip_when: The question is about what the model does once running — authority, actions, failure containment — that is agent-system-design.md
companion: agent-system-design.md covers the runtime side of the same lifecycle; ai-ml-practice.md covers evaluation; engineering-principles.md covers the artifact properties of the surrounding system
last_reviewed: 2026-08
---

# Context Engineering

Priors for constructing what a model receives, not for choosing or operating the model.

## How to read this file

Context is the input. Everything else — the model, the runtime, the orchestration — operates on it. Most prompt quality problems are context construction problems: the wrong material loaded, the right material absent, the budget spent on things the task did not need, or the structure of the context not matching the structure of the task.

The discipline here predates agents. It applies wherever a human or a system decides what a model sees: a single prompt, a RAG pipeline, a multi-step workflow, a knowledge base query, or a fully autonomous agent. The scope is construction, not execution.

The working question for any entry: **what did loading this cost in attention, and what did the model gain from it?** If the gain cannot be stated, the load was a tax.

---

## The load-bearing few

**Route the right context, not bigger context.** A larger context window makes it possible to load more; it does not make more of what you load useful. The engineering problem is selecting the right material for this task at this moment, within budget — not fitting everything available into the window.

**Available is not useful.** Irrelevant material competes for the same attention as relevant material, and it does not disappear because the budget is large. Load less; load better.

**The environment should carry the system.** When durable context lives in reachable files or structures — instructions, knowledge, state, tool descriptions — short user intent is enough, because the model navigates explicit material rather than reconstructing the operating model from conversation history. History is the fallback, not the foundation.

**Structure matches task.** A pipeline task needs different context than a retrieval task, which needs different context than a generation task. Context that was well-constructed for one stage misleads the next if the stage boundary is not also a context boundary.

**Synthesis compounds; retrieval fetches.** Some knowledge benefits from being maintained as accumulated understanding across sessions rather than rebuilt from source material on every query. Both patterns are valid; the failure is applying retrieval where the value comes from accumulated synthesis, or maintaining synthesis where freshness requires going back to source.

---

## Selection and routing

**Selective loading** — Load what this task, at this stage, needs. Not what the system has available, not what a previous stage needed, not what might conceivably be relevant. The cost of under-loading is a worse answer; the cost of over-loading is degraded attention on everything, including the material that mattered.

**Catalog over storage** — A pointer to retrievable material costs nothing in context; the material itself costs its full length. Index and retrieve rather than pre-load when the material is only conditionally needed. The router reads the catalog; the task reads the payload.

**Progressive loading** — Start with the minimum required to route. Load deeper material only when the routing decision has confirmed it is needed. Costs architecture discipline; buys a context budget that scales with task complexity rather than with everything that might be relevant.

**Stage-scoped context** — Each stage of a multi-step workflow defines what it reads and what it produces. A stage that fetches does not also synthesize. A stage that filters does not also generate. One job per stage means one well-defined context per stage, which means errors localize rather than compound through the pipeline.

**Profile-aware routing** — Different task types, user roles, or system states warrant different context compositions. A single universal context that tries to serve all cases serves none of them well. The routing logic is the engineering artifact; the context it produces is the evidence.

---

## Construction

**Recency and relevance are different signals.** The most recently retrieved document and the most relevant document are not the same thing. Retrieval ranking, recency weighting, and semantic relevance all produce different selections. Know which one the task requires and which one the system is actually providing.

**Structure the context to match the task's reasoning path.** A model asked to compare will use context differently than one asked to summarize, classify, or generate. Front-loading the decision criteria before the evidence performs better than appending them after, for the same reason a brief before evidence performs better than evidence before brief in human reasoning.

**Token cost is not uniform.** Early context and late context receive different attention under most architectures. Material that must be reliably retained belongs near the instruction anchor, not buried in a long middle. Structural signals — headers, explicit labels, format — reduce the cost of finding what matters.

**Compression is a last resort.** Summarization, truncation, and lossy compression of source material all introduce error. The right order is: route better, load less, structure tighter, then compress what remains if still over budget. Compression-first produces confident summaries of the wrong things.

**Separate instruction from content.** Instructions that tell the model what to do belong in a stable, clearly delimited section. Content the model operates on belongs separately. Mixing them produces instructions that get processed as content and content that shapes instruction-following.

---

## Knowledge and memory

**Persistent synthesis** — For knowledge that benefits from accumulating across sessions, maintain a synthesized form that integrates new material into existing understanding rather than growing a pile of isolated documents. Costs a maintenance step per ingest; buys a baseline of understanding that compounds rather than resets.

**Source and synthesis are different artifacts.** Source material is what was retrieved or ingested. Synthesis is what was understood and integrated. A system that conflates them cannot tell a model to trust one more than the other, verify a claim against its origin, or reason about whether synthesis has drifted from source.

**Navigable knowledge, not a document dump.** Storage creates capacity; navigation makes it usable. A knowledge system that cannot be queried for what exists, how concepts relate, or where a claim came from is not usable at context-construction time regardless of how much it contains.

**Infer structure before declaring metadata.** Filesystem-native or document-native structure should be read before requiring an explicit manifest. Metadata should represent facts that cannot safely be inferred from structure — not restate the directory tree, the naming convention, or the role that is already obvious from position.

**Contradiction is information.** Conflicting evidence should be preserved with enough context to understand the disagreement, not resolved silently toward whichever source arrived last. A synthesis that hides contradiction is more confident than the evidence warrants.

**Lifecycle and staleness are visible properties.** Knowledge has a date and a domain. Current knowledge and stale knowledge look identical without an explicit signal. When history matters, the age and update status of a piece of knowledge belong in the structure, not in the reader's memory.

---

## Boundaries and portability

**Stable context plane, replaceable execution plane.** Instructions, knowledge, workflow definitions, and capability descriptions should survive changes in model, runtime, orchestration framework, or deployment environment. Durable semantics belong in the context layer; runtime-specific configuration belongs in adapters. A context package that works only with one model version is technical debt with an expiry date.

**One runtime, many context-defined specializations.** A general model becomes specialized by receiving the right context, not by being a permanently named and separately maintained agent. Focused context packages are cheaper to route, easier to replace, and simpler to reason about than a proliferation of static configurations.

**Compose boundaries; do not flatten methods.** Different organizational structures — knowledge bases, workflow pipelines, coding repositories, documentation systems — solve different concerns and may legitimately coexist. Interoperability works best when each nested boundary remains understandable to the convention that owns it, rather than being rewritten to fit a single outer container's vocabulary.

**Collaboration and execution are separate layers.** Durable context files support asynchronous handoffs and shared history. They are not a substitute for message buses, authorization systems, transactions, or high-concurrency services. Keep those concerns separate; the context layer should remain usable beneath them without depending on them.

---

## Where these actively conflict

| Tension | Failure when one side wins absolutely |
|---|---|
| Selective loading vs. completeness | Missing material the task needed, or attention degraded by everything that might be relevant |
| Progressive loading vs. routing overhead | Architecture too complex to maintain, or context too flat to scale |
| Persistent synthesis vs. source freshness | Synthesis drifted from source, or retrieval that rebuilds from scratch what is already understood |
| Structured context vs. flexibility | Rigid formats that break on atypical tasks, or unstructured input that leaves the model inferring what to attend to |
| Compression vs. fidelity | Confident summaries of the wrong things, or context that exceeds budget before the task begins |
| Inferred structure vs. explicit metadata | Silent misreads of ambiguous structure, or manifests that duplicate what the filesystem already says |
| Stable context plane vs. capability evolution | Context packages that cannot use new capabilities, or packages that break every time the runtime changes |
| Synthesis persistence vs. contradiction preservation | Hidden disagreement presented as settled understanding, or a knowledge base too cautious to synthesize anything |
| Context boundary per stage vs. continuity | Each stage missing the context the previous one established, or a single undifferentiated context blob that grows through the pipeline |

---

## Using judgment

**State what loading this buys.** For every document, section, or retrieved chunk that enters context: what decision does it enable, what answer does it improve? If you cannot name it, the load is speculative. Speculative loads are a tax on every token of the context that follows.

**Measure attention cost, not just token count.** A 200-token instruction in the middle of 8,000 tokens of retrieved documents may receive less attention than 20 tokens at the top. Position, structure, and surrounding material all affect what the model can use, and token count alone does not capture that.

**Route before retrieving.** Determine what the task needs from a lightweight routing step before performing expensive retrieval or synthesis. A router that reads an index is far cheaper than a retriever that embeds and ranks the entire knowledge base for every query.

**Treat context construction as a first-class engineering concern.** It is not a prompt. It is not a system message. It is the artifact on which everything the model does depends, and it deserves architecture, testing, and iteration on the same footing as the surrounding code.

**Signs you're applying this document as ritual:** loading everything available because the window allows it; compressing before routing; a universal context that serves all task types equally poorly; metadata that duplicates structure the filesystem already expresses; synthesis that cannot be traced back to source; a knowledge base that grows but cannot be navigated; context boundaries that exist in the diagram but not in the code.

**The measure.** Whether the model received what it needed to do the task well, and nothing it did not — and whether you can verify that without running the task. If context construction requires running the task to validate, the feedback loop is too slow to improve it.
