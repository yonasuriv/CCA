# Agent Architecture: Operate at the Durable Abstraction Layer

> **Do not build permanent architecture around temporary model limitations.**
## Core Principle

The problem is not using agents.

The problem is unnecessarily building agent behavior at an implementation layer that increasingly belongs to the model runtime.

An AI system fundamentally needs to determine:

```text
What needs to be done?
Where is the relevant context?
Which instructions apply?
Which tools are available?
Which data is required?
What should happen next?
```

Historically, developers implemented much of this routing explicitly through application code and agent frameworks.

Increasingly capable model runtimes can perform more of that orchestration themselves.

This changes where durable application logic should live.

Instead of encoding the entire workflow as framework-specific control logic:

```text
Application Code
      |
      v
Agent Framework
      |
      +-- Router
      +-- Planner
      +-- Tool selector
      +-- Agent definitions
      +-- Workflow graph
      +-- Context loader
      |
      v
Model
```

much of the behavioral architecture can instead be expressed declaratively:

```text
Workflow
  |
  +-- Instructions
  +-- Tasks
  +-- Subtasks
  +-- Tools
  +-- Data
  +-- References
```

The model runtime becomes the execution engine.

The repository becomes the behavioral specification.

## The Real Agent Problem Is Routing

To perform useful work, a model needs appropriate context.

Conceptually:

```text
Request
   |
   v
Routing
   |
   +-- Correct instructions
   +-- Correct tools
   +-- Correct data
   |
   v
Execution
```

If routing fails, the system may:

- load irrelevant context
    
- follow the wrong workflow
    
- use inappropriate tools
    
- miss required data
    
- apply incorrect instructions
    
- execute unnecessary steps
    

A large portion of agent engineering therefore reduces to context and capability routing.

The architectural question becomes:

```text
How much routing logic actually needs to be implemented in code?
```

## Frameworks Encode Routing Mechanisms

Agent frameworks such as:

```text
LangChain
Semantic Kernel
Agent SDKs
Workflow engines
Custom orchestration systems
```

provide mechanisms for expressing concepts such as:

```text
Agents
Tools
Tasks
State
Routing
Planning
Memory
Subagents
Workflow transitions
```

These frameworks remain useful when application requirements demand explicit runtime control.

But the framework itself should not automatically become the architecture.

For many workflows, the durable information is actually:

```text
What the task is
How it should be performed
What resources it needs
What tools it may use
How it decomposes
```

Those concepts can often be represented independently from the framework executing them.

## File Trees as a Workflow Representation

Consider a workflow:

```text
Workflow
|
+-- Task 1
+-- Task 2
+-- Task 3
```

Each task may require:

```text
Instructions
Tools
Data
References
```

Task 2 may itself contain subtasks:

```text
Workflow
|
+-- task-1/
|
+-- task-2/
|   |
|   +-- subtask-a/
|   +-- subtask-b/
|
+-- task-3/
```

This maps naturally onto a filesystem:

```text
workflow/
|
+-- README.md
|
+-- task-1/
|   +-- instructions.md
|   +-- tools.md
|   +-- data/
|
+-- task-2/
|   +-- instructions.md
|   +-- tools.md
|   +-- data/
|   |
|   +-- subtasks/
|       |
|       +-- subtask-a/
|       |   +-- instructions.md
|       |
|       +-- subtask-b/
|           +-- instructions.md
|
+-- task-3/
    +-- instructions.md
    +-- tools.md
```

The directory hierarchy expresses decomposition.

The files express behavior.

The runtime interprets and executes them.

## Declarative vs. Imperative Agent Design

Framework-heavy systems frequently encode workflow behavior imperatively.

For example:

```text
if task == "research":
    load_research_agent()

if result.requires_validation:
    call_validation_agent()

if validation.failed:
    retry()
```

This embeds workflow semantics inside application code.

A declarative architecture instead describes the system:

```text
research/
|
+-- instructions.md
+-- validation.md
+-- tools.md
+-- references/
```

with routing instructions such as:

```text
For research tasks:
- use the research workflow
- validate primary claims
- invoke the configured search capability when external evidence is required
- escalate unresolved conflicts for review
```

The runtime decides how to execute those instructions.

This separates:

```text
Intent
```

from:

```text
Execution mechanism
```

That separation becomes increasingly valuable as model capabilities change.

## The Filesystem as an Intermediate Representation

The filesystem can be treated as an intermediate representation between human intent and model execution.

Conceptually:

```text
Human / Organization
        |
        v
Workflow Knowledge
        |
        v
Filesystem Representation
        |
        v
Model Runtime
        |
        v
Execution
```

This representation can encode:

```text
workflow hierarchy
task decomposition
instructions
knowledge
tools
constraints
examples
references
output contracts
```

The important property is portability.

The same workflow may potentially be executed by different runtimes:

```text
Portable Workflow
      |
      +-- Runtime A
      +-- Runtime B
      +-- Runtime C
      +-- Future Runtime
```

The workflow survives even if the execution engine changes.

## Move Stable Logic Up the Stack

An important architectural principle is:

> Put stable knowledge and intent at a higher abstraction layer than volatile execution mechanisms.

For example:

```text
Stable:
- business process
- task definitions
- constraints
- domain knowledge
- quality criteria
- required outputs

Less stable:
- model provider
- SDK
- agent framework
- orchestration API
- tool-calling protocol
- runtime implementation
```

If stable behavior is tightly encoded into volatile infrastructure:

```text
Workflow
    |
    v
Framework-specific implementation
```

then infrastructure changes can force architectural rewrites.

A stronger separation is:

```text
Portable Workflow Definition
          |
          v
Execution Adapter
          |
          v
Current Runtime
```

Now the implementation can evolve without rewriting the process itself.

## Model Improvements Should Collapse Infrastructure

Suppose a custom system contains:

```text
Custom planner
Custom tool router
Custom subagent manager
Custom context selector
```

A future model runtime may provide some of those capabilities natively.

Poorly separated architecture:

```text
Native capability appears
        |
        v
Custom architecture becomes redundant
        |
        v
Rewrite application
```

Portable architecture:

```text
Native capability appears
        |
        v
Replace implementation mechanism
        |
        v
Workflow remains unchanged
```

The feature can simply become another runtime capability.

For example:

```text
Before:

workflow/
    |
    v
custom planner implementation
```

After:

```text
workflow/
    |
    v
native planning tool
```

The process survives.

Only the execution primitive changes.

## Feature Compression

Model evolution frequently compresses previously complex infrastructure into simpler primitives.

Something that once required:

```text
500 lines of orchestration code
```

may eventually become:

```text
native tool
```

or:

```text
model capability
```

This does not necessarily invalidate the higher-level workflow.

Instead:

```text
Old subsystem
     |
     v
New primitive
```

The workflow can absorb the new capability.

For example:

```text
workflow/
|
+-- research/
|   +-- search-tool
|
+-- implementation/
|   +-- coding-agent
|
+-- review/
    +-- native-review-capability
```

If a provider eventually implements the entire review mechanism natively, the workflow may simply reference that capability rather than implementing it itself.

## Subtasks Are More Durable Than Artificial Agents

Suppose an application defines:

```text
Research Agent
Writing Agent
Review Agent
Publishing Agent
```

Ask whether these are actually autonomous identities or merely workflow responsibilities.

Frequently they are better represented as:

```text
workflow/
|
+-- research/
+-- write/
+-- review/
+-- publish/
```

The distinction matters.

An "agent" implies a runtime abstraction.

A "task" describes the work.

Tasks are usually more stable than the mechanism performing them.

Today:

```text
review/
    |
    v
Subagent
```

Tomorrow:

```text
review/
    |
    v
Native model capability
```

Later:

```text
review/
    |
    v
Deterministic validator
```

The workflow remains valid because it specifies the required operation rather than unnecessarily binding it to an executor.

## Tools Should Be Replaceable Capabilities

The same principle applies to tools.

A workflow should ideally depend on capabilities rather than specific implementations.

Conceptually:

```text
Workflow requires:
    web_search
```

rather than:

```text
Workflow fundamentally depends on:
    CustomSearchAgentV4
```

The capability may currently be provided through:

```text
MCP server
API
CLI tool
SDK
native model integration
custom service
```

The workflow does not need to care unless implementation-specific behavior matters.

This creates:

```text
Workflow
   |
   v
Capability Contract
   |
   v
Current Tool Implementation
```

instead of:

```text
Workflow
   |
   v
Vendor-specific implementation
```

## External Capabilities Extend the Tree

A filesystem-based workflow does not imply that everything must exist locally.

External capabilities can still be attached through tools.

For example:

```text
workflow/
|
+-- research/
|   +-- instructions.md
|   +-- tools.md
|
+-- implementation/
|   +-- instructions.md
|
+-- review/
    +-- instructions.md
```

The research task might declare access to:

```text
Web search
GitHub
Database
Internal documentation
Browser
```

These could be exposed through:

```text
MCP
CLI
API
SDK
native runtime tools
```

The file tree describes when and why capabilities should be used.

The runtime handles how they are invoked.

## Subagents Become an Execution Primitive

The same applies to subagents.

A workflow might contain:

```text
workflow/
|
+-- discovery/
+-- implementation/
+-- independent-review/
```

The runtime may choose to execute this as:

```text
Main Agent
   |
   +-- Subagent: discovery
   +-- Subagent: implementation
   +-- Subagent: review
```

But the workflow itself does not necessarily need to define permanent agent identities.

Subagents become one possible execution strategy.

Other strategies might include:

```text
Sequential execution
Parallel model calls
Human delegation
External worker
Deterministic automation
```

This separates:

```text
Work decomposition
```

from:

```text
Worker topology
```

which is a stronger abstraction boundary.

## Model Runtime as Operating Environment

Modern coding agents increasingly provide capabilities that previously required substantial custom infrastructure:

```text
Filesystem access
Shell execution
Code modification
Tool calling
External integrations
Context discovery
Subagent spawning
Planning
Iteration
State inspection
```

This means the runtime increasingly resembles an operating environment for AI workflows.

The architecture can therefore shift from:

```text
Build custom agent runtime
        |
        v
Execute workflow
```

toward:

```text
Define workflow
      |
      v
Attach to capable runtime
      |
      v
Execute
```

This is similar to other abstractions in computing.

Developers generally do not implement their own:

```text
filesystem
process scheduler
network stack
database engine
```

unless the problem requires it.

Likewise, as model runtimes mature, fewer applications should need to rebuild generic agent infrastructure.

## The Abstraction-Layer Test

When an AI architecture appears threatened by every new model release, ask:

```text
Which layer contains our actual value?
```

If the answer is:

```text
Custom prompt router
Custom tool loop
Custom planner
Custom agent wrapper
```

then the system may be operating too close to the infrastructure layer.

If the answer is:

```text
Domain workflow
Operational knowledge
Task decomposition
Quality criteria
Data
Constraints
Integrations
Outcome
```

then model improvements are more likely to improve the system rather than replace it.

This is the key distinction.

## Build Against Capabilities, Not Limitations

A common architectural mistake is building permanent infrastructure around temporary model limitations.

For example:

```text
Model cannot reliably choose context
        |
        v
Build custom context router
```

This may be reasonable today.

But it should remain replaceable.

Otherwise:

```text
Temporary limitation
        |
        v
Permanent architecture
```

creates technical debt.

A better pattern is:

```text
Workflow Requirement
        |
        v
Capability Interface
        |
        v
Current Workaround
```

When the model improves:

```text
Workflow Requirement
        |
        v
Capability Interface
        |
        v
Native Capability
```

No workflow redesign is required.

## Stable Core, Replaceable Runtime

A durable AI architecture can therefore be modeled as:

```text
+----------------------------------+
| Stable Layer                     |
|                                  |
| Outcomes                         |
| Workflows                        |
| Tasks                            |
| Instructions                     |
| Knowledge                        |
| Constraints                      |
| Quality criteria                 |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Capability Layer                 |
|                                  |
| Search                           |
| Execution                        |
| Retrieval                        |
| Delegation                       |
| Validation                       |
| Communication                    |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Replaceable Runtime Layer        |
|                                  |
| Model                            |
| Agent SDK                        |
| MCP                              |
| Framework                        |
| API                              |
| CLI                              |
| Provider                         |
+----------------------------------+
```

Changes should become cheaper as they move downward.

The durable knowledge should remain above them.

## When Frameworks Are Still Appropriate

This does not mean agent frameworks are useless.

Explicit orchestration remains valuable when requirements include:

- deterministic state transitions
    
- strict workflow guarantees
    
- long-running execution
    
- durable distributed state
    
- resumability
    
- event processing
    
- complex concurrency
    
- transactional behavior
    
- fine-grained authorization
    
- extensive observability
    
- large-scale multi-tenant execution
    
- regulated execution paths
    
- strict cost or latency controls
    

In those cases, code is not accidental complexity.

It implements required system properties.

The mistake is using that infrastructure when the model runtime and a declarative workflow already provide everything the application needs.

## Key Notes

- Using agents and building agent infrastructure are different concerns.
    
- Agent systems primarily need effective routing between instructions, tools, data, and tasks.
    
- Many workflow structures map naturally onto directory trees.
    
- Tasks and subtasks are generally more durable abstractions than named agents.
    
- Instructions, tools, data, and references can be represented independently from the runtime executing them.
    
- Filesystems can act as declarative workflow representations.
    
- The repository can function as an intermediate representation between human process knowledge and model execution.
    
- Stable workflow knowledge should not be unnecessarily coupled to volatile frameworks.
    
- Model providers will continue absorbing capabilities previously implemented through custom orchestration.
    
- Native capabilities should replace lower-level infrastructure without forcing higher-level workflow redesign.
    
- New model features can often be treated as tools or execution primitives inside an existing workflow.
    
- Build against capability contracts rather than vendor-specific implementations where practical.
    
- Subagents should often be treated as an execution strategy rather than the primary unit of workflow design.
    
- Work decomposition and worker topology are separate architectural concerns.
    
- Modern agent runtimes increasingly provide generic execution capabilities that applications previously had to implement themselves.
    
- Do not build permanent architecture around temporary model limitations.
    
- Frameworks remain justified when they provide actual system properties that the model runtime cannot provide reliably.
    
- If every model release threatens the architecture, too much application value may be encoded at the wrong layer.
    
- If model improvements make the system simpler or more capable without changing its workflow definition, the abstraction boundaries are probably healthier.
    

## Design Heuristic

When considering custom agent infrastructure, ask:

```text
What durable requirement does this code represent?
```

If the answer is:

```text
This is how our workflow works
```

consider moving that knowledge into a portable workflow representation.

If the answer is:

```text
This provides a runtime guarantee we actually require
```

code may be the correct layer.

Then ask:

```text
Would a future model capability eliminate this implementation
without changing the underlying workflow?
```

If yes:

```text
Keep the implementation replaceable.
```

The architecture should evolve from:

```text
Workflow encoded in framework
```

toward:

```text
Workflow
   |
   v
Capability contracts
   |
   v
Replaceable execution runtime
```

## Final Principle

The durable unit of an AI system is usually not the agent implementation.

It is the description of the work:

```text
Outcome
   |
   v
Workflow
   |
   v
Tasks
   |
   +-- Instructions
   +-- Tools
   +-- Data
   +-- Constraints
```

Everything below that is execution infrastructure.

As models become more capable, more orchestration will move into the runtime.

Architectures that encode their value in workflows, context, capabilities, and domain knowledge can absorb those improvements.

Architectures that encode their value primarily in custom routing and agent plumbing risk having their implementation compressed into a native feature.

The objective is therefore not to predict which agent framework will survive.

It is to place your system's durable knowledge at an abstraction layer where better models make the architecture stronger instead of obsolete.