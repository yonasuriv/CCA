---
scope: Learned systems — how models are evaluated, deployed, and trusted
read_when: Building or deploying anything with a learned component, designing evaluation, interpreting benchmark or metric claims, deciding where a model's output is trusted, diagnosing performance that degraded in production
skip_when: The question is about a specific model, framework, API, or current capability — that dates fast and does not belong in a foundations doc
companion: agent-system-design.md for systems where models take actions; engineering-principles.md for the surrounding artifact
last_reviewed: 2026-08
non_goals: Model names, context windows, pricing, framework APIs, current state of the art. Deliberately excluded — anything with a version number rots faster than this file is reviewed.
---

# AI/ML Practice

Priors for building on components that learn, not a guide to any model.

## How to read this file

Everything here is about the durable part: how learned systems fail, how evaluation misleads, and where trust is placed. None of it depends on which model you are using, and none of it stops being true when a new one ships.

The distinguishing property of a learned component is that its behavior is induced from data rather than specified, which means you never have a complete statement of what it does. You have measurements. Every entry below is about the gap between a measurement and the property you actually care about.

The working question: **what does this number measure, on what distribution, and how is production different?** Most deployment failures are answered by that sentence.

---

## The load-bearing few

**A benchmark is evidence about a benchmark.** Performance transfers to production only insofar as the evaluation distribution matches it. It usually does not, and the mismatch is rarely visible in the score.

**Evaluate before you deploy, and keep evaluating.** A model's environment moves. Static evaluation measures a moment. Without continuous measurement you learn about degradation from users.

**Errors are not symmetric.** False positives and false negatives have different costs in every real application, and aggregate accuracy hides which one you are buying. Decide the ratio deliberately, at the threshold, rather than accepting whatever the default produced.

**Data quality dominates model choice.** Label noise, leakage, sampling bias, and stale distributions cap achievable performance regardless of what sits on top. Effort spent here beats effort spent on architecture for nearly all applied work.

**Know where the human is.** Every learned component sits somewhere on a line from advisory to autonomous. The position determines what accuracy is sufficient and what failures cost, and it should be a decision rather than an accident of how the interface got built.

---

## Evaluation

**Held-out discipline** — Test data the model has not seen, and has not seen a correlated version of. Leakage through duplicated records, temporal overlap, preprocessing fitted on the full set, or repeated tuning against the test set inflates every number downstream. The costliest form is the one nobody detects, because the resulting confidence is fully sincere.

**Evaluation distribution** — The set you measure on defines the claim you can make. If it was collected differently from production traffic, the score is a statement about the collection process. Where production is unrepresented, say so explicitly rather than reporting a single headline number.

**Metric selection** — Aggregate accuracy conceals class imbalance, subgroup disparity, and tail behavior. Precision, recall, and their trade-off make the error asymmetry visible; per-slice reporting makes the failure population visible. Costs reporting complexity and buys the ability to see who the system fails.

**Calibration** — Whether a confidence score corresponds to an actual probability. Uncalibrated confidence is worse than no confidence, because downstream logic and humans both act on it. A model can be accurate and badly calibrated, which specifically breaks any design that routes by confidence.

**Baselines** — Compare against the simple thing: a heuristic, the majority class, the existing process. A substantial fraction of learned systems do not beat theirs, and without one you cannot tell whether the model is contributing.

**Regression testing for behavior** — A fixed suite of cases with known-correct handling, run on every change. This is the mechanism that catches a "better" model that broke something specific and important. Costs curation and buys the ability to change models without discovering the damage in production.

---

## Data

**Provenance and lineage** — Where data came from, how it was transformed, what version trained what. Without it, reproducing a result or diagnosing a regression is guesswork. Costs metadata infrastructure and is unrecoverable retroactively.

**Leakage** — Information present at training time that will not exist at inference time, or target information encoded in a feature. Produces excellent offline numbers and immediate production failure. Look for it whenever results are surprisingly good.

**Sampling bias** — The training population differs from the deployment population in ways that correlate with the target. The model learns the difference and applies it confidently to people it never saw.

**Label quality** — Labels are opinions with a process behind them. Inter-annotator disagreement bounds achievable accuracy, and systematic annotator bias becomes model bias. Measuring agreement before scaling annotation is cheap and rarely done.

**Distribution shift** — Inputs drift, relationships change, populations move. Covariate shift, concept drift, and seasonality all degrade a static model. Monitor input distributions as well as outcomes, because outcome labels usually arrive too late to be your alarm.

**Feedback loops** — The model's outputs influence the data it later trains on. Recommendations shape what gets clicked; a fraud model's blocks remove the counterfactual; an agent's writing becomes the next corpus. Left unbroken, the system optimizes toward its own past behavior and away from reality.

---

## Deployment and operation

**Reproducibility under nondeterminism** — Seeds, versions, data snapshots, and environment pinned well enough to reproduce a result. Full determinism is often unattainable; knowing precisely which factors are uncontrolled is attainable and nearly as useful.

**Model versioning as an interface change** — A model swap changes behavior for every consumer, silently, without a schema change. Version and stage it like a breaking API change, because for downstream logic tuned to the old behavior, it is one.

**Shadow and staged rollout** — Run the new model against real traffic without acting on it, then expose gradually. Costs infrastructure and buys the only realistic measurement of production behavior before commitment.

**Monitoring beyond accuracy** — Input distributions, output distributions, confidence distributions, latency, refusal and fallback rates, and per-segment outcomes. Accuracy alone is often unavailable in production because labels lag, so the leading indicators are distributional.

**Fallback behavior** — What happens when the model is unavailable, slow, or low-confidence. A defined degraded path is a design decision; without one, the fallback is whatever the caller does with a timeout.

**Cost and latency as design constraints** — Inference cost and latency shape architecture as much as accuracy does. An accurate model too slow or expensive for its call path is not a solution to the problem.

---

## Trust and consequence

**Match autonomy to error cost** — The accuracy required is a function of what a wrong answer does, not a universal bar. Advisory output tolerates far more error than automated action. Set the threshold from the consequence.

**Explainability where decisions land on people** — When output affects someone's access, price, treatment, or opportunity, being able to say why matters independently of accuracy. Costs model choice constraints and post-hoc tooling; the requirement is often external and non-negotiable.

**Subgroup performance** — Aggregate metrics hide disparate failure. A model that performs well overall and poorly for a population is a system that fails specific people consistently. Measure by slice, and treat a large gap as a defect rather than a footnote.

**Automation bias** — People over-trust model output, especially when it is confident and well-formatted. A human-in-the-loop who rubber-stamps is not a control. Interfaces that surface uncertainty and disagreement work better than ones that present a clean answer.

**Privacy in training data** — Models can memorize and reproduce training examples. Anything sensitive in training data is potentially reachable through outputs. See `escalation-triggers.md` for regulated categories.

---

## Where these actively conflict

| Tension | Failure when one side wins absolutely |
|---|---|
| Model performance vs. explainability | Uninterpretable decisions about people, or a weaker model where accuracy carries real consequence |
| Aggregate accuracy vs. subgroup performance | Good averages concealing consistent failure for a population |
| Precision vs. recall | Missed detections, or an alert stream nobody can process |
| Offline evaluation vs. production reality | Confident deployment of a benchmark artifact, or no gate before exposure |
| Rapid iteration vs. reproducibility | Results nobody can reproduce, or an experiment cadence too slow to learn |
| Fresh data vs. stability | Retraining into a feedback loop, or a model drifting away from its population |
| Automation vs. human oversight | Rubber-stamped output, or review overhead exceeding the value of automating |
| Model capability vs. cost and latency | Unaffordable or unusable inference, or a model too weak for the task |
| Confidence exposure vs. usability | Uncertainty nobody knows how to act on, or clean answers that hide their unreliability |

---

## Using judgment

**Ask what the number measures.** Every reported metric has a distribution, a slice, and a threshold behind it. A score without those three is a claim, not evidence.

**Look for leakage when results are good.** Surprisingly strong offline performance is more often a data problem than a modeling success. Check before you present it.

**Set the threshold from consequence, not from the ROC curve.** The optimal operating point is a business and ethical decision about which error you would rather make.

**Treat the model as the least stable component.** It degrades without code changes, behaves differently on inputs nobody anticipated, and gets replaced. Build the surrounding system so that swapping it is routine.

**Signs you're applying this document as ritual:** a single headline metric; evaluation on data collected the same way as training; no baseline; confidence scores used for routing without a calibration check; monitoring that only tracks uptime; a human reviewer with no mechanism to disagree; per-slice performance that was measured once and never reported.

**The measure.** Whether you can state what the system does badly, for whom, and how you would know it got worse. If you cannot, you have a deployment rather than an understanding.
