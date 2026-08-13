# AI Context Architecture: One Runtime, Many Skills

## Core Principle

The limiting factor in many AI systems is not model intelligence.

It is context organization.

A capable model may already know how to:

* read and write files
* reason over instructions
* execute tools
* inspect data
* modify code
* delegate work
* maintain local state
* iterate over a task

The harder problem is determining:

```text
Which instructions apply?

Which data is relevant?

Which tools are permitted?

Which workflow should be followed?

What context should be loaded now?

What should remain outside the active context?
```

This can be understood as a context-routing problem.

Instead of building a separate agent for every workflow, a more scalable architecture is:

```text
General Agent Runtime
        |
        v
Context Router
        |
        v
Relevant Skill
        |
        +-- Instructions
        +-- Tools
        +-- Data
        +-- References
        |
        v
Task Execution
```

The runtime remains general.

The specialization lives in the context package.

## The Context Wall

A useful abstraction is the "context wall."

The wall is not a literal limitation in the system.

It represents the architectural boundary between:

```text
Everything the organization knows
```

and:

```text
What the model needs for this task
```

An organization may contain:

```text
People
Processes
Policies
Customers
Projects
Documentation
Tools
Databases
Code
Decisions
Historical work
```

The model cannot consume all of this indiscriminately.

The real problem is therefore:

```text
Organizational Knowledge
        |
        v
Context Selection
        |
        v
Relevant Working Context
        |
        v
Model
```

A strong AI architecture solves this selection problem reliably.

## Context Is Usually Workflow-Scoped

Most organizational context only becomes meaningful relative to work being performed.

For example:

```text
Security Assessment
```

may require:

```text
Scope
Testing methodology
Client architecture
Tools
Reporting requirements
Previous findings
Rules of engagement
```

while:

```text
Invoice Processing
```

may require:

```text
Vendor information
Accounting policy
Approval rules
ERP access
Tax data
```

These are different contexts.

The organization therefore does not need one giant universal prompt.

It needs context packages aligned with actual workflows.

Conceptually:

```text
Organization
|
+-- Workflow A
|   +-- instructions
|   +-- data
|   +-- tools
|
+-- Workflow B
|   +-- instructions
|   +-- data
|   +-- tools
|
+-- Workflow C
    +-- instructions
    +-- data
    +-- tools
```

## Skills as Context Packages

A skill can be treated as a modular package describing how to perform a particular class of work.

For example:

```text
skills/
|
+-- vulnerability-triage/
|   +-- SKILL.md
|   +-- references/
|   +-- scripts/
|
+-- code-review/
|   +-- SKILL.md
|   +-- references/
|   +-- scripts/
|
+-- report-generation/
    +-- SKILL.md
    +-- templates/
    +-- references/
```

The instruction file describes:

```text
When the skill applies
What the objective is
How the task should be performed
What constraints exist
What output is expected
```

Supporting resources provide:

```text
Data
Tools
Scripts
Examples
Templates
References
```

The skill becomes a portable operational capability.

## Skill = Behavior + Context + Capability

A useful abstraction is:

```text
Skill
=
Instructions
+
Relevant Knowledge
+
Available Tools
+
Constraints
```

The model provides the general reasoning capability.

The skill provides specialization.

Therefore:

```text
General Model
      +
Security Skill
      =
Security-specialized execution
```

or:

```text
General Model
      +
Research Skill
      =
Research-specialized execution
```

The specialization does not necessarily require a separately implemented agent.

## One Runtime, Many Specializations

A common architecture creates multiple explicit agents:

```text
Research Agent
Security Agent
Writing Agent
Review Agent
Documentation Agent
Testing Agent
```

But if these agents primarily differ by:

```text
Instructions
Context
Tools
Permissions
Data
```

then separate agent implementations may be unnecessary.

A simpler architecture is:

```text
General Runtime
     |
     +-- Research Skill
     +-- Security Skill
     +-- Writing Skill
     +-- Review Skill
     +-- Documentation Skill
     +-- Testing Skill
```

The runtime becomes specialized dynamically according to the work.

This separates:

```text
Who executes
```

from:

```text
How the work should be performed
```

## Dynamic Agent Construction

A skill invocation can be viewed conceptually as temporary agent construction.

Before loading the skill:

```text
General Agent
```

After loading:

```text
General Agent
+
Task-specific instructions
+
Task-specific tools
+
Task-specific data
=
Task-specialized agent instance
```

The specialization exists for the duration of the task.

This avoids creating a permanently defined agent for every possible workflow.

Conceptually:

```text
Runtime
   |
   v
Load Skill A
   |
   v
Temporary Specialized Execution
   |
   v
Return to Runtime
```

Then:

```text
Runtime
   |
   v
Load Skill B
   |
   v
Different Specialized Execution
```

The same runtime supports many roles.

## Agents as Runtime Instances, Not Static Products

This suggests a useful distinction.

Static architecture:

```text
Agent A
Agent B
Agent C
Agent D
Agent E
```

Dynamic architecture:

```text
Runtime
  |
  v
Task + Skill + Context
  |
  v
Agent Instance
```

The "agent" becomes an execution state rather than a permanently engineered component.

This can dramatically reduce architectural complexity when agent identities do not contain meaningful durable state.

## Workflows Can Compose Skills

A workflow may require several capabilities.

For example:

```text
Security Assessment
|
+-- scope-analysis
+-- reconnaissance
+-- testing
+-- evidence-validation
+-- finding-writing
+-- report-review
```

Each can exist as a skill:

```text
skills/
|
+-- scope-analysis/
+-- reconnaissance/
+-- evidence-validation/
+-- finding-writing/
+-- report-review/
```

The workflow can then compose them:

```text
Assessment Workflow
      |
      +-- use scope-analysis
      +-- use reconnaissance
      +-- use evidence-validation
      +-- use finding-writing
      +-- use report-review
```

This creates reusable primitives without requiring five independent agent systems.

## Skills and Workflows Are Different Layers

These concepts should remain separate.

```text
Skill = reusable capability

Workflow = ordered or conditional composition of capabilities
```

For example:

```text
Skill:
Validate vulnerability evidence
```

may appear in:

```text
Web application assessment
Internal network assessment
Cloud assessment
Code review
```

The reusable capability should therefore not be duplicated inside every workflow.

A stronger architecture is:

```text
Reusable Skills
      |
      v
Composable Workflows
      |
      v
Business Processes
```

## Employee Workflows as Context Boundaries

Different people in an organization perform different work.

Suppose:

```text
Employee A -> Sales
Employee B -> Engineering
Employee C -> Security
```

They may all use the same capable runtime.

What differs is the available environment:

```text
Employee A
   |
   +-- sales skills
   +-- CRM tools
   +-- account context
```

```text
Employee B
   |
   +-- engineering skills
   +-- repositories
   +-- CI tools
```

```text
Employee C
   |
   +-- security skills
   +-- assessment methodology
   +-- security tooling
```

The AI infrastructure can remain largely shared.

The context and authorization boundaries produce different capabilities.

## Context Routing Replaces Agent Proliferation

Instead of:

```text
Request
  |
  v
Which agent should handle this?
```

the system can ask:

```text
Request
  |
  v
Which workflow applies?
  |
  v
Which skills are relevant?
  |
  v
Which context is required?
```

This changes routing from identity-based:

```text
Choose Agent
```

to capability-based:

```text
Choose Knowledge + Tools + Instructions
```

The second model can be easier to maintain.

## Filesystem as the Routing Structure

A filesystem naturally represents hierarchical context.

For example:

```text
company/
|
+-- AGENTS.md
|
+-- skills/
|
+-- workflows/
|
+-- knowledge/
|
+-- tools/
|
+-- projects/
```

The root routing file explains where the model should look.

Then context can be progressively resolved:

```text
Request
  |
  v
Root Router
  |
  v
Workflow
  |
  v
Skill
  |
  v
References / Tools / Data
```

This creates bounded context discovery rather than loading everything globally.

## Progressive Disclosure

A strong context architecture should reveal information only when required.

Instead of:

```text
Start task
  |
  v
Load entire organization
```

use:

```text
Start task
  |
  v
Load routing context
  |
  v
Identify workflow
  |
  v
Load required skill
  |
  v
Load task-specific references
```

This provides:

* lower token consumption
* better relevance
* less distraction
* reduced instruction conflict
* clearer authority boundaries
* easier debugging

The context tree becomes a mechanism for progressive disclosure.

## Tools Should Be Attached to Capabilities

A skill may require access to external systems.

For example:

```text
github-review/
|
+-- SKILL.md
+-- tools/
    +-- github
```

The implementation behind that capability might be:

```text
MCP
API
CLI
SDK
Native model tool
```

The skill should ideally depend on the capability rather than the transport implementation.

Conceptually:

```text
Skill
  |
  v
Needs GitHub capability
  |
  v
Runtime provides implementation
```

This keeps the skill portable.

## Data Should Also Be Scoped

The same principle applies to data.

A skill should not automatically receive access to all organizational information.

Instead:

```text
Skill
  |
  v
Required Data Scope
```

For example:

```text
invoice-processing
    |
    +-- vendor records
    +-- invoice documents
    +-- accounting policy
```

not:

```text
invoice-processing
    |
    v
Entire company data lake
```

Context routing should therefore also function as a security boundary.

## Context Architecture Is Also Security Architecture

If context determines:

```text
What the model knows
What the model can access
What tools it can invoke
```

then context architecture directly affects security.

A production design should distinguish:

```text
Relevance
Authority
Capability
```

A resource may be relevant but unauthorized.

A tool may be available globally but forbidden for a particular workflow.

Therefore:

```text
Relevant
!=
Authorized
```

and:

```text
Available
!=
Permitted
```

Skill activation should not automatically imply unrestricted capability.

## Subagents Become Cheap Execution Units

Once the runtime can dynamically specialize itself, additional instances can perform independent work.

Conceptually:

```text
Main Runtime
    |
    +-- Instance A + Skill A
    +-- Instance B + Skill B
    +-- Instance C + Skill C
```

This makes subagents useful as execution units rather than requiring a separate architecture for each one.

For example:

```text
Main Task
  |
  +-- Research subtask
  +-- Implementation subtask
  +-- Independent review subtask
```

Each worker can receive a bounded context package.

The durable architecture remains the workflow and skill definitions.

## Scaling Comes From Composition

Suppose there are:

```text
20 reusable skills
```

and:

```text
10 workflows
```

You do not necessarily need:

```text
200 separately engineered agents
```

Instead:

```text
Skills
   |
   +-- composed differently
   |
   v
Workflows
```

The combinatorial value comes from composition.

Conceptually:

```text
Small set of reusable capabilities
            |
            v
Many possible task configurations
```

This is more maintainable than agent proliferation.

## The Context Plane and Execution Plane

A useful architectural split is:

```text
+--------------------------------+
| Context Plane                  |
|                                |
| Skills                         |
| Workflows                      |
| Knowledge                      |
| Instructions                   |
| Data routing                   |
| Capability declarations        |
+--------------------------------+
              |
              v
+--------------------------------+
| Execution Plane                |
|                                |
| Model runtime                  |
| Tool execution                 |
| Filesystem                     |
| Subagents                      |
| APIs                           |
| Shell                          |
+--------------------------------+
```

The context plane defines:

```text
What should happen
```

The execution plane provides:

```text
How it can happen
```

This separation makes both layers easier to evolve.

## Context Becomes the Durable Asset

As general-purpose runtimes improve, more execution capabilities become standardized.

The durable differentiation increasingly moves toward:

```text
Domain instructions
Workflow design
Organizational knowledge
Private data
Quality criteria
Permissions
Operational history
```

In other words:

```text
Runtime capability becomes commodity.

Context architecture remains organization-specific.
```

A better runtime can consume the same context package and improve execution without requiring the organization to rewrite its operational knowledge.

## Key Notes

* The primary bottleneck in many AI systems is context organization rather than raw model capability.
* The "context wall" represents the difficulty of selecting the correct organizational knowledge for a task.
* Context is naturally scoped around workflows.
* Skills can package instructions, tools, data, references, and constraints.
* A general runtime can become task-specialized by loading the relevant skill.
* Many separately defined agents can instead be represented as dynamic combinations of runtime + skill + context.
* Skills describe reusable capabilities.
* Workflows compose those capabilities.
* Business processes compose workflows.
* Routing by capability and context can be simpler than routing by named agent identity.
* Filesystems naturally support hierarchical context routing.
* Progressive context loading improves relevance and reduces unnecessary context consumption.
* Tools should be exposed through capability contracts where practical.
* Data access should be scoped to the workflow that requires it.
* Context architecture is also part of the authorization and security model.
* Relevant information is not automatically authorized information.
* Subagents can be treated as temporary execution workers receiving bounded skill contexts.
* Agent proliferation is often a symptom of encoding specialization in runtime identities instead of reusable context modules.
* A small set of reusable skills can support many workflows.
* Separating the context plane from the execution plane produces a more durable architecture.
* As runtimes improve, organizational context becomes increasingly important as the durable differentiator.

## Design Heuristic

When considering a new agent, ask:

```text
What actually makes this agent different?
```

If the answer is primarily:

```text
Different instructions
Different tools
Different data
Different references
```

then consider representing it as:

```text
Skill
```

instead of:

```text
New Agent Implementation
```

Then ask:

```text
Can the existing runtime execute this capability
if given the correct context?
```

If yes:

```text
Reuse the runtime.
Package the specialization.
```

Finally:

```text
Does this require a new execution mechanism,
or only a new description of the work?
```

That distinction determines whether you need:

```text
Infrastructure
```

or simply:

```text
Context.
```

## Final Principle

A capable AI runtime should not require a separately engineered agent for every task in an organization.

A more durable architecture is:

```text
General Runtime
      +
Structured Context
      +
Skills
      +
Tools
      +
Scoped Data
      =
Dynamic Specialized Execution
```

The filesystem can provide the routing structure.

Skills can provide task-specific behavior.

Workflows can compose skills.

The runtime can provide reasoning, execution, and delegation.

Instead of building hundreds of static agents, build a structured environment from which specialized agent behavior can be instantiated when needed.

The scalable primitive is not necessarily the agent.

It is the context package that tells a capable runtime how to become the agent required for the current task.
