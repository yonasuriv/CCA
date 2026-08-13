# Agentic Systems: Start With the Workflow, Not the Agent

## Core Principle

Do not begin with the assumption that a problem requires an AI agent.

An agent is an implementation mechanism, not a business requirement and not inherently an improvement over simpler software.

The correct sequence is:

```text
Problem
  |
  v
Desired outcome
  |
  v
Manual workflow
  |
  v
Steps + decisions + dependencies
  |
  v
Bottlenecks
  |
  v
Appropriate tools
  |
  +-- Conventional software
  +-- Scripts
  +-- APIs
  +-- Databases
  +-- Deterministic automation
  +-- LLM calls
  +-- Human operators
  +-- Agents
```

Agents should appear at the end of the reasoning process, not at the beginning.

## Problem Before Technology

Every useful system starts with an outcome someone actually needs.

In a commercial context, this usually means:

- A real problem exists.
    
- Someone values solving that problem.
    
- There is a reproducible process that produces the desired outcome.
    
- The process contains steps, decisions, inputs, outputs, and constraints.
    

AI does not create this foundation.

If the underlying process cannot be clearly executed manually, adding agents generally makes the system harder to understand rather than more capable.

Before introducing AI, the workflow should be understood well enough to answer:

- What is the desired outcome?
    
- What inputs are required?
    
- What steps produce that outcome?
    
- Which steps require judgment?
    
- Which steps are deterministic?
    
- Where does information come from?
    
- What are the failure modes?
    
- Which steps are expensive, repetitive, slow, or difficult?
    
- What needs to remain under human authority?
    

Only then should implementation technologies be selected.

## Manual Execution as the Reference Implementation

A manual workflow is often the first useful implementation of a system.

This is important because manual execution exposes information that premature automation hides:

- implicit assumptions
    
- undocumented decisions
    
- required context
    
- exceptions
    
- edge cases
    
- dependencies
    
- quality criteria
    
- handoff boundaries
    

If a skilled human cannot reliably describe and reproduce the process, there is usually not enough information to automate it safely.

A practical progression is:

```text
1. Perform the work manually.
2. Make the outcome reproducible.
3. Document the process.
4. Identify repeated operations.
5. Identify decision points.
6. Identify required context.
7. Select tools for each operation.
8. Delegate or automate appropriate steps.
9. Measure whether the outcome improves.
```

The manual workflow therefore acts as the reference implementation against which automation can be evaluated.

## Do Not Confuse Agents With AI

Many AI-assisted workflows do not require agents.

A useful system may consist of nothing more than:

```text
Instructions
+ Context
+ Data
+ Model
= Useful AI-assisted execution
```

An agent introduces additional properties such as autonomous iteration, tool selection, state management, environmental interaction, planning, or execution loops.

Those capabilities are useful when the problem requires them.

They are overhead when it does not.

For example, this:

```text
Input
  |
  v
Prompt + context
  |
  v
LLM
  |
  v
Structured output
```

may be sufficient.

There is no reason to introduce:

```text
Planner
  |
  v
Agent
  |
  +-- Memory
  +-- Tool router
  +-- Retry loop
  +-- State machine
  +-- Subagents
  +-- Event bus
  +-- Workflow orchestrator
```

unless those mechanisms solve an actual constraint.

## The Agent Complexity Tax

Agentic architectures introduce real engineering costs.

These can include:

- nondeterministic execution
    
- larger failure surfaces
    
- state-management complexity
    
- context-management problems
    
- observability requirements
    
- tool permission boundaries
    
- retry and recovery logic
    
- higher token and inference cost
    
- increased latency
    
- difficult reproducibility
    
- harder debugging
    
- more complex evaluation
    
- coordination failures between agents
    
- unclear responsibility and authority boundaries
    

Therefore, an agent should justify its complexity.

A useful engineering rule is:

> Use the least autonomous mechanism capable of reliably producing the required outcome.

This produces a natural hierarchy:

```text
Static logic
    |
    v
Script
    |
    v
Traditional automation
    |
    v
Single LLM call
    |
    v
LLM workflow
    |
    v
Tool-using agent
    |
    v
Multi-agent system
```

Move downward only when the previous level cannot adequately solve the problem.

## Workflow Decomposition Before Agent Design

Suppose the objective is:

```text
Produce a high-quality client security assessment
```

Do not immediately create:

```text
Recon Agent
Pentest Agent
Research Agent
Reporting Agent
QA Agent
Manager Agent
```

First decompose the actual workflow:

```text
Client requirements
      |
      v
Scope interpretation
      |
      v
Environment discovery
      |
      v
Testing
      |
      v
Evidence collection
      |
      v
Finding validation
      |
      v
Risk assessment
      |
      v
Report construction
      |
      v
Quality review
      |
      v
Client deliverable
```

Then inspect each step independently.

Some may benefit from agents.

Others may be better implemented as deterministic scripts, templates, existing tools, retrieval systems, simple model calls, or human judgment.

The architecture should emerge from this decomposition.

## Instructions Are a Form of Process Encoding

One of the simplest ways to determine whether work can be delegated is to document how an experienced operator performs it.

For example:

```text
workflow/
|
+-- README.md
+-- instructions.md
+-- quality-criteria.md
+-- examples/
+-- references/
+-- templates/
```

Give that material to another competent person with access to an AI model.

If they can reproduce the original outcome, something important has happened:

The process has become transferable.

That means part of the operator's tacit knowledge has been converted into explicit operational knowledge.

This is often more valuable than prematurely building a sophisticated agent framework.

## Delegation Before Automation

Human delegation is also a useful test for automation readiness.

If a workflow cannot be handed from one competent person to another, it will usually be difficult to delegate reliably to an agent.

The progression can therefore be:

```text
Expert performs task
        |
        v
Expert documents task
        |
        v
Another human executes instructions
        |
        v
Process is refined
        |
        v
AI assists execution
        |
        v
Individual steps are automated
        |
        v
Agent autonomy added where justified
```

This creates a much stronger foundation than:

```text
Idea
  |
  v
Build agent
  |
  v
Hope useful behavior emerges
```

## Harnesses Still Matter

Rejecting agent-first architecture does not mean that agent infrastructure is irrelevant.

Harness design, context engineering, memory, tool interfaces, evaluation, permissions, state, and orchestration become important once autonomous execution is justified.

The distinction is architectural sequencing.

Bad sequence:

```text
Agent platform
    |
    v
Agents
    |
    v
Agent orchestration
    |
    v
Search for problems to solve
```

Better sequence:

```text
Problem
    |
    v
Reliable process
    |
    v
Known bottlenecks
    |
    v
Automation opportunities
    |
    v
Agent requirements
    |
    v
Harness architecture
```

Infrastructure should be pulled into the system by requirements.

Requirements should not be invented to justify infrastructure.

## Multi-Agent Systems Require Stronger Justification

Adding agents is conceptually similar to adding people to an organization.

More workers do not automatically produce a better result.

Additional participants introduce:

- communication overhead
    
- coordination cost
    
- duplicated work
    
- conflicting decisions
    
- synchronization problems
    
- context loss
    
- unclear ownership
    

The same applies to agents.

A multi-agent system should therefore exist because the task has meaningful independent or specialized work that benefits from decomposition.

For example:

```text
Complex workload
      |
      +-- Independent task A
      |
      +-- Independent task B
      |
      +-- Independent task C
      |
      v
Verified aggregation
```

This may justify parallel agents.

But replacing one coherent workflow with ten artificial personas usually does not.

## Scale the Proven Process

Automation should scale something that already works.

The objective is not:

```text
Add agents -> become scalable
```

It is:

```text
Proven outcome
    |
    v
Repeatable process
    |
    v
Encoded knowledge
    |
    v
Delegation
    |
    v
Automation
    |
    v
Autonomy where beneficial
    |
    v
Scale
```

This distinction matters because automation multiplies the properties of the underlying process.

Good process:

```text
Good process * automation = scalable good process
```

Bad process:

```text
Bad process * automation = scalable bad process
```

Agentic autonomy does not repair an undefined workflow.

It executes the undefined workflow faster and with additional nondeterminism.

## Architecture Selection Principle

For every workflow step, ask:

```text
What is the simplest mechanism that can reliably perform this operation?
```

Possible answers include:

```text
Human judgment
Static documentation
Checklist
Template
Shell script
Application code
Database query
API integration
Scheduled job
Workflow engine
Single LLM call
RAG pipeline
Tool-using LLM
Agent
Multiple agents
```

"Agent" is one option in the toolbox.

It should not be the default.

## Key Notes

- Start from the problem and required outcome, not AI.
    
- A workflow should generally exist before it is automated.
    
- Manual execution provides the reference implementation.
    
- Documenting the process converts tacit knowledge into transferable operational knowledge.
    
- If another competent person cannot reproduce the result from the instructions, agent automation is probably premature.
    
- AI does not imply agents.
    
- Many valuable AI systems require only prompts, context, data, and deterministic orchestration.
    
- Agents introduce autonomy and therefore additional complexity and failure modes.
    
- Use the least autonomous architecture that reliably solves the problem.
    
- Traditional software should remain the default for deterministic operations.
    
- Use LLMs where interpretation, synthesis, generation, or probabilistic reasoning provides value.
    
- Use agents when iterative autonomous decision-making or environmental interaction is actually required.
    
- Use multiple agents only when decomposition, specialization, isolation, or parallelism produces measurable value.
    
- Agent harnesses should be designed from discovered execution requirements, not built before requirements exist.
    
- Adding agents does not inherently increase quality.
    
- Coordination has a cost, whether the workers are humans or models.
    
- Automation should scale a proven process rather than compensate for an undefined one.
    
- Agent architecture should emerge from workflow decomposition.
    

## Design Heuristics

Before creating an agent, ask:

```text
Can this be solved deterministically?
```

Then:

```text
Can this be solved with a single model invocation?
```

Then:

```text
Can this be solved with a bounded LLM workflow?
```

Only then:

```text
Does the system actually need autonomous iteration,
tool selection, state, or decision-making?
```

If yes, an agent may be justified.

For multiple agents, add another question:

```text
What property of the problem becomes materially better
when responsibility is distributed across multiple agents?
```

If there is no concrete answer such as parallelism, isolation, specialization, independent verification, or context separation, the multi-agent architecture is probably unnecessary.

## Final Principle

The goal is not to build agents.

The goal is to reliably produce valuable outcomes.

Agents, models, workflows, scripts, APIs, humans, and conventional software are implementation components that can contribute to that outcome.

The architecture should be selected based on the work.

The work should never be invented to justify the architecture.