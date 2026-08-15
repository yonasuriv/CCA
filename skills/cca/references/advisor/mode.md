# Advise mode

Use this mode for engineering judgment. The advisor corpus is independent from workspace architecture references: architect mode may consult it, but must not absorb, duplicate, or redefine it.

Read only the reference(s) required by the decision:

| Scope | File | Read it when |
|---|---|---|
| Artifact | `engineering-principles.md` | Design, implementation, review, refactoring, architecture, structural trade-offs |
| Process | `frameworks-and-methodologies.md` | Planning, delivery cadence, team structure, org design, methodology disputes |
| Adversary | `security-and-adversarial-thinking.md` | Threat modeling, trust boundaries, control design, incident response, untrusted input |
| Autonomy | `agent-system-design.md` | Agents, tool surfaces, multi-step automation, self-healing or self-modifying systems |
| Context | `context-engineering.md` | Prompt systems, RAG, knowledge bases, multi-step context routing |
| Learned components | `ai-ml-practice.md` | Evaluation design, deployment, metrics, production degradation |
| Hard stops | `escalation-triggers.md` | Legal, regulatory, scope, third-party, or irreversible external consequence |

These are seven references, not six.

## Application

- Treat the references as priors with explicit costs, not compliance checklists.
- Local evidence beats a prior except where `escalation-triggers.md` defines a hard stop.
- Do not summarize references back to the user unless that is the task.
- Cite the trade, not the name of a principle.
- A principle without its cost is being applied as ritual.
- Recommend and advise; never turn advisor guidance into an enforcement layer.
- When architect mode needs process judgment (for example Scrum vs Kanban, or whether an ICM stage belongs inside an existing delivery process), consult this domain lazily and leave the methodology itself authoritative.

## Precedence

`escalation-triggers.md` takes precedence over all other advisor references. If uncertain whether a trigger applies, read it.