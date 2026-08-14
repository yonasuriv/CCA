---
scope: Adversary — how systems fail when someone is actively trying to make them fail
read_when: Threat modeling, architecture with a trust boundary, incident response, control design, security review, anything handling credentials, untrusted input, or third-party code
skip_when: The failure mode under discussion is accidental rather than adversarial — use engineering-principles.md
companion: engineering-principles.md holds the artifact-level controls (least privilege, defense in depth, secure by default, validate at trust boundaries); this file does not restate them, it covers the reasoning that decides where and whether to apply them
last_reviewed: 2026-08
---

# Security and Adversarial Thinking

Priors for reasoning about an intelligent opponent, not a control checklist.

## How to read this file

Ordinary engineering assumes failures are accidental, independent, and roughly random. An adversary is none of those things. They select the failure, they combine failures that are individually harmless, and they specifically target whatever you assumed would hold. Every entry below exists because some property that is true under accidental failure is false under adversarial pressure.

This is not a control list. Controls are downstream of a threat model, and a control adopted without one is a cost with an unknown benefit. The most common failure in this domain is not a missing control — it is a complete-looking set of controls protecting against an adversary nobody characterized.

The working question for any entry is: **who is the adversary, what do they want, what can they reach, and what does this change cost them?** If the answer to the last part is "nothing," the control is theatre regardless of how much effort it took to deploy.

---

## The load-bearing few

**Assume breach.** Design as though some component is already compromised. Prevention fails eventually; what determines outcome is what the attacker can reach next and how fast you notice. A system whose security depends on no perimeter ever being crossed has one control, not many.

**Reason about cost, not possibility.** Everything is possible given unlimited effort. Security is the economics of making the attack cost more than the target is worth to that specific adversary. "Could someone do X" is nearly always yes and nearly always the wrong question.

**Trust is a boundary, not a property.** Name where untrusted becomes trusted and what happens at that line. Most serious vulnerabilities are a boundary that existed in the diagram but not in the code, or one that quietly moved when a component was reused somewhere new.

**The control must be cheaper than the bypass.** People route around friction. A control that makes legitimate work meaningfully harder produces workarounds that are worse than the risk it addressed. This is a design constraint, not a user-education problem.

**Detection is a control.** Prevention that cannot be verified and failures that cannot be seen leave you asserting security rather than knowing it. Time to detect and time to contain are security properties on equal footing with whether the door was locked.

---

## Reasoning about adversaries

**Threat modeling** — Characterizing who attacks, what they want, and how they reach it, before choosing controls. Buys a defensible reason for every control and reveals the assets nobody had listed. Costs time and produces a document that goes stale; the failure mode is a threat model produced once for compliance and never consulted again. Model the system as it is, not as the architecture diagram claims.

**Attacker economics** — Adversaries have budgets, skills, motives, and alternatives. A commodity criminal, a competitor, an insider, and a state actor are different problems with different mitigations, and defending against all of them equally means defending against none of them well. The cost asymmetry is structural: the defender must cover every path, the attacker needs one. Design to reduce paths rather than to cover them all.

**Attack surface** — Every input, endpoint, dependency, credential, integration, and human with access. Surface grows silently through convenience — a debug endpoint, an ops script, a fourth-party dependency of a third-party library. The most reliable security work is deletion, because removed surface cannot be misconfigured.

**Trust boundaries** — Where data or control crosses between components with different trust levels. Untrusted input is normalized and validated once, at the boundary, and treated as trusted inside. The dangerous case is a component moved to a new context where its old assumption about a caller no longer holds.

**Confused deputy** — A privileged component acting on an unprivileged caller's instruction. Server-side request forgery, injection through an over-broad service account, and most agent tool-use vulnerabilities are this pattern. Authority must be carried by the request, not by whatever the intermediary happens to hold.

**Insider and supply chain** — The adversary with legitimate access, and the adversary who compromises something you inherited. Both defeat perimeter reasoning entirely, which is why they justify segmentation, provenance, and audit rather than more perimeter.

---

## Structural properties

**Blast radius** — What one compromise reaches. This is the property that most determines whether an incident is an inconvenience or an existential event, and it is set by architecture, not by controls bolted on later. Segmentation, credential scoping, and network boundaries all buy the same thing: a smaller answer to "and then what?"

**Containment over prevention** — At sufficient scale, prevention will fail. The design question is what happens next: can the compromise spread, does it persist, can it be evicted, can you rebuild from known-good state. Costs redundancy and operational complexity; the alternative is discovering these answers during an incident.

**Fail secure vs. fail open** — On failure, does the system deny or allow? Denying is correct for authorization and dangerous for safety-critical availability. Decide deliberately per control, because the default is whatever the implementation happened to do, and nobody finds out until it fails.

**Credential and secret lifecycle** — Issuance, scope, rotation, revocation, expiry. Long-lived broad credentials are the single most reliable escalation path in most environments. Short-lived scoped credentials cost infrastructure and buy the difference between a leaked secret being an incident and being a non-event.

**Auditability and provenance** — Knowing what happened, in what order, initiated by whom, from what. Without it, incident response is speculation and attribution is impossible. Logs that the compromised component can edit are not audit.

**Cryptographic humility** — Use vetted, current, well-integrated primitives and libraries. Custom protocols and novel constructions fail in ways that do not surface during testing. Where crypto matters, the risk concentrates in key management and integration, not in the algorithm.

---

## Practice and process

**Detection and response** — Instrumentation that surfaces adversarial behavior, and a rehearsed path from alert to containment. Costs tuning and on-call load; untuned detection produces alert fatigue, which is functionally the same as no detection.

**Least privilege in practice** — The principle is in the artifact doc. What belongs here is its operational failure: strict scoping produces sprawl, sprawl produces a wildcard grant at 3am to unblock a deploy, and that grant outlives the incident. Scope by role and lifecycle, make audited escalation fast enough that nobody routes around it, and expire elevation automatically.

**Secure defaults over secure configuration** — The shipped configuration is the one most deployments will run. Options that must be set correctly to be safe will be set incorrectly somewhere.

**Compliance is not security** — Frameworks encode a floor derived from past incidents in other organizations. Meeting the floor is often necessary and never sufficient, and optimizing for the audit reliably produces controls that satisfy evidence requirements without changing what an attacker can do.

**Disclosure and scope** — Testing has boundaries and findings have consequences beyond the tested system. Scope creep during an assessment, and what to do about a finding that implicates a third party, are decisions with legal and ethical weight. See `escalation-triggers.md` rather than reasoning through them alone.

---

## Where these actively conflict

| Tension | Failure when one side wins absolutely |
|---|---|
| Least privilege vs. operability | Permission sprawl and emergency wildcard grants, or a compromise that reaches everything |
| Prevention vs. detection investment | Hard shell with no visibility inside, or thorough monitoring of an easily entered system |
| Fail secure vs. availability | Denying legitimate access under load, or opening the door whenever a dependency times out |
| Defense in depth vs. complexity | Many weak layers substituting for one strong control, and an attack surface made of controls |
| Security friction vs. adoption | Users route around the control, and the workaround becomes the real system |
| Segmentation vs. operational simplicity | Blast radius nobody can bound, or an environment nobody can operate or debug |
| Logging depth vs. data minimization | Audit trails that are themselves a breach target, or incidents that cannot be reconstructed |
| Rapid patching vs. change stability | Known-exploited vulnerabilities left open, or outages caused by the remediation |
| Transparency vs. attacker information | Security through obscurity as a load-bearing control, or publishing the map |
| Compliance evidence vs. real posture | Controls designed to be auditable rather than effective |

---

## Using judgment

**Name the adversary before the control.** "Is this secure" has no answer. "Can an authenticated tenant reach another tenant's data" does.

**Price the mitigation in attacker cost.** If a change does not increase the effort, skill, time, or exposure required to succeed, it is not a mitigation. Say what it does buy — often compliance, or detection — and stop calling it security.

**Weight by blast radius and reversibility.** A compromise you can contain and roll back is an incident. One that exfiltrates data or destroys state is permanent. Spend accordingly, and treat anything irreversible as deserving disproportionate attention.

**Assume your assumptions are the target.** Whatever you believe is guaranteed — the network is internal, the client validates, the library is maintained, the input came from our own service — is the specific thing an adversary will test.

**Signs you're applying this document as ritual:** a control with no named threat; a threat model written once and never revisited; risk ratings with no reachability analysis behind them; a finding count reported as a security metric; hardening that has driven users to a shadow workflow; treating an audit pass as evidence of posture.

**The measure.** Whether an adversary's cheapest path to your most damaging outcome got more expensive, and whether you would see them taking it. If a change moves neither, it was not a security change.
