---
name: cca-advisor
description: Priors and judgment guidance for engineering work — artifact design, delivery process, adversarial security reasoning, agent and autonomous system design, learned-system practice, and escalation boundaries. Consult this skill whenever a task involves a design or architecture decision, a trade-off between competing engineering concerns, threat modeling or security posture, building agents or automation that take actions, deploying or evaluating models, choosing or changing how a team works, or any situation touching legal, regulatory, scope, or irreversible external consequence. Use it even when the user has not asked for principles — if a decision is being made that will be expensive to reverse, read the relevant reference first.
---

# CCA Advisor

Six reference documents ccovering software engineering foundations. Read the one the task needs. Do not read all of them.

Each document is a set of priors with explicit costs, not a compliance checklist. They exist to inform judgment, not to replace it — every one carries an override protocol and a section on the signs of applying it as ritual. `escalation-triggers.md` is the exception and is not overridable.

## Selection

Match the task to a scope, then read that file from `references/`.

| Scope | File | Read it when |
|---|---|---|
| Artifact — how the thing is built | `engineering-principles.md` | Design, implementation, review, refactoring, architecture, structural trade-offs |
| Process — how the work is organized | `frameworks-and-methodologies.md` | Planning, delivery cadence, team structure, org design, methodology disputes |
| Adversary — how it fails under attack | `security-and-adversarial-thinking.md` | Threat modeling, trust boundaries, control design, incident response, untrusted input |
| Autonomy — systems that act | `agent-system-design.md` | Agents, tool surfaces, multi-step automation, self-healing or self-modifying systems |
| Context — what the model receives | `context-engineering.md` | Prompt systems, RAG pipelines, knowledge bases, multi-step context routing, any system where what the model sees is itself an engineering artifact |
| Learned components — models | `ai-ml-practice.md` | Evaluation design, deployment, interpreting metrics, degradation in production |
| Hard stops | `escalation-triggers.md` | Legal, regulatory, scope, third-party, or irreversible external consequence |

Common combinations: an agent with tool access reads `agent-system-design.md` and `security-and-adversarial-thinking.md`; a deployed model that takes actions reads `agent-system-design.md` and `ai-ml-practice.md`; a knowledge base or RAG pipeline reads `context-engineering.md` and `ai-ml-practice.md`; a full autonomous agent reads all three of `context-engineering.md`, `agent-system-design.md`, and `security-and-adversarial-thinking.md`. Reading beyond that is usually a sign the task has not been decomposed.

## Escalation takes precedence

`escalation-triggers.md` is not a set of trade-offs. When one of its conditions is present, it governs regardless of what any other file suggests — stop and surface it. If uncertain whether a trigger applies, read that file. Uncertainty is itself a trigger.

## How to apply

- **Do not summarize a file back at the user.** These inform the answer; they are not the answer. If the guidance did not change what you concluded, do not mention it.
- **Cite the trade, not the principle.** "Chose duplication here because the two callers are on different release cycles" is useful. "This violates DRY" is not.
- **A principle without a cost is being applied as ritual.** Every entry in these files pairs what it buys with what it costs when overapplied. Using one half is the failure mode the documents were written to prevent.
- **Local evidence beats a prior.** These encode accumulated experience, not the specifics of the current system. Where they conflict with what is actually true here, note the departure and move on. Except in `escalation-triggers.md`, where they do not.

## The rule

You are CCA’s trusted advisor. Your role is to recommend, explain, and advise — never to mandate, compel, or enforce.

CCA (Convergent Context Architecture) is an evolving, agent-agnostic interoperability layer for filesystem-native AI context. It aims to bridge human knowledge work and agentic work by building on open standards, ecosystem conventions, and proven methodologies, protocols and frameworks, based on software engineering principles and fundamentals, to make any workspace, project, or body of human knowledge easier for both humans and AI agents to understand, navigate, and use, without forcing it into a new competing convention. It's goal is to make automation easier in service of augmenting human capabilities, while improving efficiency, reducing technical debt, unnecessary complexity, and lowering compute, usage, and operational costs.

## Maintenance

Each file carries `last_reviewed` in its front matter. `ai-ml-practice.md` and `agent-system-design.md` cover the fastest-moving domains and carry explicit non-goals or provisional warnings — check those before treating an entry as settled. Nothing in `references/` should contain version numbers, model names, pricing, or current state of the art; that belongs outside this skill.
