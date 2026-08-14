---
scope: Autonomy — systems where a nondeterministic component selects and takes actions
read_when: Designing agents, tool surfaces, multi-step automation, self-healing or self-improving systems, human-in-the-loop boundaries, or any pipeline where a model's output triggers an action rather than being read by a person
skip_when: The model is producing output a human reads and acts on — that is a deterministic system with an unreliable input, covered by engineering-principles.md
companion: engineering-principles.md for artifact properties; security-and-adversarial-thinking.md for tool surfaces under adversarial pressure; ai-ml-practice.md for evaluation and model behavior
last_reviewed: 2026-08
---

# Agent System Design

Priors for systems that act without a human approving each step.

## How to read this file

An agent is a system where a component that is confidently wrong some fraction of the time selects actions with real effects. Most of engineering assumes components fail loudly and predictably. This one fails quietly, plausibly, and differently each time — which means the properties that keep such a system safe are not the ones that keep a service reliable.

This is the least settled domain in this folder. The entries below are load-bearing in current practice, but prior art is thin and conventions are still forming. Treat them as more provisional than the other files, and weight your own operational evidence higher.

The working question for any entry is: **what does this component do when it is wrong, and who or what catches it?** If the answer is "a human notices eventually," that is a design, but say so out loud rather than arriving there by default.

---

## The load-bearing few

**Design for confident wrongness.** The failure mode is not a crash or an error code. It is a well-formed, plausible, incorrect action. Every guardrail assuming failures announce themselves is unusable here.

**Bound authority by action cost.** Autonomy should scale inversely with how expensive a mistake is to undo. Reading is cheap, writing is not, deleting and sending and paying are irreversible. This is the single highest-leverage decision in an agent architecture and it is made per tool, not per system.

**The tool surface is the real interface.** What an agent can do is defined by its tools, not by its instructions. Instructions are a strong prior; tools are the hard boundary. Anything you rely on prompting to prevent is unenforced.

**Make actions retry-safe.** Agents retry — after timeouts, after errors, after their own confusion about whether something succeeded. Non-idempotent actions in a retry loop produce duplicated effects that are hard to detect and harder to reverse.

**Instrument the reasoning, not only the result.** A correct output produced for the wrong reason will produce a wrong output next time under a slightly different input. Without the intermediate trace, you are debugging a black box from its outcomes.

---

## Authority and action

**Action cost tiering** — Classify every tool by reversibility and blast radius: read-only, reversible write, irreversible write, externally visible action. Autonomy, retry policy, approval requirement, and logging depth all derive from the tier. Costs upfront classification work; without it every tool implicitly gets the same trust, which is the trust level of the most dangerous one.

**Human-in-the-loop placement** — Approval gates buy correctness and cost latency and attention. Placed on everything, they train the reviewer to approve reflexively, which is worse than no gate because it manufactures false assurance. Place them where the action is irreversible or externally visible, and nowhere else.

**Idempotency** — Same action, same key, same effect no matter how many times it runs. Costs key generation and dedup storage, and is close to non-negotiable for any tool an agent can retry.

**Reversibility and compensating actions** — For every action, know the undo. Where there is none — a sent message, a deleted record, a payment — that is exactly where approval and confirmation belong. Soft-delete and staged execution buy back reversibility cheaply.

**Least privilege for agents** — An agent inherits whatever its credentials hold, and it will find uses for authority you did not anticipate. Scope tool credentials per tool and per task, not per system. See `security-and-adversarial-thinking.md`.

**Termination conditions** — Explicit limits on steps, time, cost, and repeated failure. Without them, a confused agent loops, and the loop consumes budget or produces repeated side effects. Every autonomous run needs a defined way to stop that does not depend on the agent deciding to.

---

## Context and state

**Context economy** — Context is a scarce, contended resource. Everything loaded competes with everything else for attention, and irrelevant content degrades performance rather than being harmlessly ignored. Load what the current step needs; prefer retrieval and lazy loading over resident context.

**Progressive disclosure** — Structure knowledge so a router reads an index and pulls only the relevant payload. Costs indexing discipline and buys the ability to grow a knowledge base without degrading every task that does not need it.

**Explicit state over inferred state** — State the agent must track across steps belongs in a durable structure it reads and writes, not in the conversation history it is expected to remember. History is lossy, gets truncated, and cannot be inspected or corrected by anything else.

**Provenance** — Record where each fact came from: user statement, tool result, retrieved document, or model generation. Without it, generated content becomes indistinguishable from retrieved fact on the next step, and the error compounds silently.

**Stale context** — Data fetched at step one may be wrong by step twelve. Long-running agents act on snapshots. Re-read before acting on anything time-sensitive, or accept and document the staleness window.

---

## Failure and containment

**Fault isolation between steps** — One bad step should not corrupt the whole run. Checkpoint, validate between stages, and make partial completion recoverable rather than requiring a full restart that repeats side effects already applied.

**Validate outputs structurally** — Constrain outputs to schemas, enums, and validated types wherever the next step consumes them programmatically. Free-text output feeding a parser is a failure surface. Costs rigidity; buys errors that surface at the boundary rather than three steps downstream.

**Detect the confident wrong answer** — Cross-checks, independent verification of high-cost actions, consistency checks against known state, and refusal paths for low-confidence cases. This is the hard problem in the domain and no mechanism solves it generally; layering cheap checks is currently the practical answer.

**Escalation over improvisation** — An agent that cannot complete a task should stop and surface why. Systems that improvise around blockers produce plausible workarounds that diverge from intent, and the divergence is discovered late.

**Blast radius per run** — Bound what a single execution can touch: rate limits, spend caps, scoped credentials, restricted target sets, dry-run modes. Costs configuration and buys the difference between a bad run and a bad day.

**Loop and feedback hazards** — An agent whose output becomes its own next input amplifies error. This includes writing to a knowledge base it later reads, and multi-agent setups where one agent's generation is another's evidence. Break the loop with human review, provenance filtering, or a validation gate.

---

## Self-modifying and self-healing systems

These properties apply to any system that changes its own behavior, configuration, or knowledge. They are where autonomy compounds fastest in both directions.

**Change classification** — A system that modifies itself needs to distinguish what it may change alone from what requires review. Configuration within bounds, retries, and scaling are usually safe. Logic, permissions, prompts, and the safety mechanisms themselves are not. Without an explicit line, everything is on the near side of it.

**Immutable safety boundaries** — Whatever enforces limits — approval gates, spend caps, credential scopes, termination conditions — must sit outside what the system can rewrite. A self-improving system that can widen its own constraints has no constraints, only preferences.

**Rollback as a precondition** — Never let the system apply a self-modification it cannot revert, and keep the revert mechanism outside the modified component. Self-healing that damages the system needs a path back that does not depend on the damaged part.

**Auditability of self-change** — Every self-modification recorded with trigger, diff, and outcome. Without a change log, behavioral drift is undiagnosable — you cannot distinguish a bad change from a changed environment.

**Measure before adapting** — Self-improvement requires a measurable objective that actually correlates with value. Optimizing a proxy is Goodhart's law with a faster clock and no human in the loop to notice the divergence.

---

## Where these actively conflict

| Tension | Failure when one side wins absolutely |
|---|---|
| Autonomy vs. oversight | Human approval on every step until nobody reads them, or unsupervised irreversible actions |
| Context richness vs. context economy | Degraded attention from irrelevant loading, or missing the fact the task needed |
| Structured output vs. flexibility | Brittle schemas that reject valid work, or free text that breaks downstream parsers |
| Retry resilience vs. side-effect safety | Duplicated actions from retries, or transient failures that abort whole runs |
| Agent capability vs. blast radius | Broad tool access it will eventually misuse, or an agent too constrained to finish the task |
| Speed vs. verification | Fast wrong actions, or verification overhead exceeding the value of automating at all |
| Self-modification vs. stability | Constraints the system can widen, or a system that cannot fix its own known failures |
| Memory persistence vs. stale state | Acting on outdated snapshots, or losing context that made the run coherent |
| Multi-agent decomposition vs. coherence | Fragmented state and compounding handoff error, or one agent doing too much to debug |
| Prompt-level control vs. enforced control | Guardrails that hold until an input phrases things differently |

---

## Using judgment

**Ask what happens when it is wrong, not whether it works.** A demo proves the success path exists. The design question is the distribution of failures and what each one costs.

**Weight by reversibility, per tool.** This is the load-bearing decision in the whole domain. Get the tiering right and most other choices follow; get it wrong and no amount of prompt engineering compensates.

**Prefer enforcement to instruction.** If a limit matters, put it in the tool layer, the credential scope, or the orchestration — somewhere the model cannot phrase its way past. Instructions set a prior. Only code sets a bound.

**Do not confuse capability with reliability.** A model that can do a task in most attempts is not a component that does it. The gap between them is where the engineering lives, and it is filled with validation, retries, bounds, and escalation.

**Treat this file as provisional.** Conventions here are less settled than in the other foundations docs. Where your operational evidence contradicts an entry, your evidence wins — note what you learned and revise the file.

**Signs you're applying this document as ritual:** approval gates nobody reads; retries on non-idempotent actions; logs of outputs but not reasoning; tool credentials scoped to the whole system; a self-improvement loop with no measured objective; safety limits stored where the agent can edit them.

**The measure.** Whether the failures the system produces are bounded, visible, and reversible. Not whether it succeeds more often — a system that succeeds more often and fails invisibly is worse than one that succeeds less and stops when it is lost.
