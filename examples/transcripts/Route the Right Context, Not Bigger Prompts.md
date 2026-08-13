# Context Engineering: Route the Right Context, Not Bigger Prompts

## Core Principle

A better prompt does not compensate for a badly designed context system.

Agent quality depends heavily on whether the runtime can assemble the right information for the current task:

```text
Agent Execution
=
Instructions
+ Memory
+ Knowledge
+ Tools
+ State
```

The engineering problem is therefore not:

```text
How do we write the perfect prompt?
```

It is:

```text
How do we reliably construct the right context
for this task, at this moment, within the available budget?
```

Prompt engineering operates inside context engineering.

Context engineering determines what the model has available to reason over in the first place.

## The Five Context Components

A useful context model can be divided into five categories.

### 1. Instructions

Instructions define:

```text
What the agent should do
How it should behave
Which rules apply
Which workflows exist
How resources should be discovered
```

Examples include:

```text
AGENTS.md
Project instructions
Skill definitions
Workflow files
Policies
Output contracts
```

Instructions provide the operating model.

### 2. Memory

Memory provides durable information from previous work.

Examples:

```text
Past decisions
User preferences
Completed tasks
Historical context
Prior findings
Project evolution
```

Memory answers:

```text
What happened before that matters now?
```

### 3. Knowledge

Knowledge contains information about the domain or environment.

Examples:

```text
Documentation
Research
Architecture
Entities
Concepts
Organizational knowledge
Knowledge graphs
Reference repositories
```

Knowledge answers:

```text
What does the system need to know?
```

### 4. Tools

Tools define what the agent can do outside pure language generation.

Examples:

```text
Filesystem
Shell
Search
Browser
GitHub
Databases
APIs
MCP servers
Code execution
```

Tools answer:

```text
What capabilities can the agent invoke?
```

### 5. State

State describes the current execution environment.

Examples:

```text
Current task
Current project
Files modified
Execution progress
Pending decisions
Active branch
Intermediate results
Current plan
```

State answers:

```text
What is happening right now?
```

Together:

```text
               Context
                  |
     +------------+------------+
     |            |            |
 Instructions   Memory       Knowledge
     |                         |
     +------------+------------+
                  |
               Tools
                  |
                State
```

## Context Engineering vs. Prompt Engineering

Prompt engineering primarily manipulates:

```text
Current Instructions
```

Context engineering operates across:

```text
Instructions
Memory
Knowledge
Tools
State
```

This explains why a short request can outperform a long prompt when the surrounding environment is well designed.

For example:

```text
"Review this."
```

may be sufficient if the runtime already knows:

```text
Which project is active
What "review" means
Which standards apply
Where the code lives
Which review workflow to invoke
What previous decisions were made
What output format is expected
```

The apparent simplicity of the prompt is enabled by prior context architecture.

The complexity did not disappear.

It moved into the environment.

## The Prompt Should Not Carry the Entire System

A fragile architecture places everything into every user request:

```text
User Prompt
|
+-- role
+-- workflow
+-- project history
+-- policies
+-- tool instructions
+-- domain knowledge
+-- formatting
+-- task
```

This creates:

```text
Large prompts
Repeated tokens
Instruction drift
Human effort
Inconsistent behavior
```

A stronger architecture separates persistent context from task-specific intent:

```text
Persistent Environment
        |
        +-- instructions
        +-- workflows
        +-- knowledge
        +-- memory
        +-- tools
        |
        v
Short User Intent
        |
        v
Context Assembly
        |
        v
Execution
```

The user describes what they want.

The environment supplies how the organization performs it.

## Root Instructions as the Navigation Handbook

A root-level instruction file can act as the first routing layer for the agent.

Conceptually:

```text
Project Root
|
+-- AGENTS.md
+-- skills/
+-- workflows/
+-- knowledge/
+-- tools/
+-- projects/
```

The root instructions should not contain every piece of project knowledge.

They should explain how to discover it.

For example:

```text
AGENTS.md
|
+-- project purpose
+-- operating principles
+-- directory map
+-- routing rules
+-- authority hierarchy
+-- context loading rules
+-- available capabilities
```

This makes the root file a navigation contract.

Its primary job is:

```text
Tell the runtime where to look next.
```

## Hierarchical Context

Large systems need context at multiple scopes.

For example:

```text
Global
  |
  v
Repository
  |
  v
Domain
  |
  v
Workflow
  |
  v
Task
```

Each layer can add more specific instructions.

Conceptually:

```text
Global Rules
    |
    v
Repository Rules
    |
    v
Workflow Rules
    |
    v
Task Context
```

This allows progressively specialized execution without loading every instruction globally.

The rule should generally be:

```text
Load broad context first.
Load specific context only when relevant.
```

## Context Budget

Every model operates under finite working-context constraints.

Even when context windows become very large, using them efficiently still matters because unnecessary context can increase:

```text
Cost
Latency
Noise
Conflicting instructions
Retrieval ambiguity
Reasoning burden
```

Therefore:

```text
Available Context
!=
Useful Context
```

The objective is not maximum context.

It is maximum relevant signal.

Conceptually:

```text
Context Utility
=
Relevant Information
/
Total Loaded Information
```

A good context architecture attempts to maximize that ratio.

## Progressive Context Loading

Instead of:

```text
Load everything
      |
      v
Ask model to identify what matters
```

prefer:

```text
User Request
     |
     v
Root Router
     |
     v
Relevant Workflow
     |
     v
Relevant Skill
     |
     v
Required Knowledge
     |
     v
Required Data / Tools
```

Each step narrows the search space.

This is progressive disclosure.

The model receives increasingly detailed context only as the task requires it.

## Knowledge Graphs as a Knowledge-Routing Mechanism

The knowledge component can be represented as a graph.

A graph contains:

```text
Nodes
+
Edges
```

where a useful conceptual mapping is:

```text
Node
=
Entity / concept / data point
```

and:

```text
Edge
=
Relationship
```

For example:

```text
[Social Post]
      |
   posted-on
      |
      v
[2026-08-01]
```

and:

```text
[Social Post]
      |
    type
      |
      v
[Technical Tutorial]
```

and:

```text
[Social Post]
      |
   produced
      |
      v
[120K Views]
```

The graph does not merely store facts.

It stores how facts relate.

## Relationships Enable Multi-Hop Context

Suppose the user asks:

```text
Which technical posts performed best last month?
```

A graph-oriented system can traverse:

```text
[Content]
   |
   +-- type -> [Technical]
   |
   +-- posted-on -> [Date]
   |
   +-- produced -> [Analytics]
```

The answer requires multiple relationships.

This differs from retrieving documents merely because they contain similar words.

Graph navigation can provide:

```text
Structural relevance
```

while semantic retrieval provides:

```text
Similarity relevance
```

The two can complement each other.

## Knowledge Graphs Do Not Necessarily Require Graph Databases

The graph is a conceptual model.

Its implementation can be:

```text
Markdown links
YAML metadata
JSON
SQL
Filesystem relationships
Graph databases
Search indexes
```

For example:

```text
content/post-001.md
```

might contain:

```yaml
type: technical
posted: 2026-08-01
analytics: analytics/post-001.md
topic: context-engineering
```

The filesystem already expresses a navigable graph.

Use specialized graph infrastructure only when the required scale or query patterns justify it.

## Scoring Knowledge

Not every piece of information should have equal retrieval priority.

The source proposes scoring graph nodes according to properties such as:

```text
Relevance
Recency
```

This can be generalized into a retrieval score.

For example:

```text
Priority(node)
=
f(
    relevance,
    recency,
    authority,
    confidence,
    task fit
)
```

Possible dimensions include:

```text
Relevance
How closely does this information match the current task?

Recency
How recent is it?

Authority
Is this an authoritative source?

Confidence
How reliable is the information?

Specificity
How directly does it address the request?
```

The purpose is not to create arbitrary scores.

The purpose is to provide a systematic way to prioritize competing context.

## Recency Is Not Authority

Scoring dimensions should remain independent.

For example:

```text
New Slack message
```

may have:

```text
High recency
Low authority
```

while:

```text
Approved architecture decision
```

may have:

```text
Lower recency
High authority
```

Therefore:

```text
Newest
!=
Most correct
```

A robust retrieval system should avoid collapsing all dimensions into one simplistic ranking signal.

## Authority Should Usually Dominate Convenience

Consider:

```text
Architecture Decision Record
```

versus:

```text
Developer comment from yesterday
```

If they disagree, the agent should know whether one is authoritative.

A useful priority model may resemble:

```text
Authority
   |
   v
Applicability
   |
   v
Relevance
   |
   v
Recency
```

The exact ordering depends on the domain.

The important part is making the policy explicit rather than asking the model to infer it repeatedly.

## Graph Engineering Is Part of Context Engineering

Graph engineering belongs primarily inside the knowledge layer.

Conceptually:

```text
Context Engineering
|
+-- Instructions
+-- Memory
+-- Knowledge
|     |
|     +-- Graph structure
|     +-- Retrieval
|     +-- Ranking
|     +-- Provenance
|
+-- Tools
+-- State
```

Graph design therefore does not replace context engineering.

It improves one part of it:

```text
How knowledge is represented and discovered.
```

## Context Routing Should Combine Multiple Signals

A robust context retrieval pipeline can combine:

```text
Task classification
+
Filesystem routing
+
Semantic search
+
Graph relationships
+
Metadata filtering
+
Authority rules
+
Recency
```

For example:

```text
Question
   |
   v
Identify Workflow
   |
   v
Identify Relevant Entities
   |
   +------------------+
   |                  |
   v                  v
Graph Traversal   Semantic Search
   |                  |
   +---------+--------+
             |
             v
       Rank Candidates
             |
             v
       Load Context
```

Different retrieval mechanisms solve different parts of the problem.

## Context Selection Is an Optimization Problem

The ideal context set is not:

```text
All available information
```

It is:

```text
Smallest sufficient set of information
required to execute correctly.
```

Formally:

```text
Minimize:
Context size

Subject to:
Sufficient evidence
Correct instructions
Required capabilities
Required state
Authorization constraints
```

This reframes context engineering as an optimization problem.

## Context Routing Is Also a Security Boundary

An agent may know where sensitive information exists without being authorized to read it.

Therefore:

```text
Discoverable
!=
Readable
```

Likewise:

```text
Tool exists
!=
Tool permitted
```

Context construction must therefore evaluate:

```text
Relevance
AND
Authorization
```

before loading information.

For example:

```text
Request
   |
   v
Relevant Data Found
   |
   v
Authorized?
   |
   +-- Yes -> Load
   |
   +-- No -> Exclude
```

Context engineering and access control cannot be treated as completely independent systems.

## Context Quality Can Reduce Prompt Complexity

Consider two environments.

### Poor Context Architecture

The user must repeatedly write:

```text
You are a security engineer.
Use this methodology.
Check these files.
Remember this architectural decision.
Use GitHub.
Follow this reporting format.
Do not modify production.
...
```

### Strong Context Architecture

The user writes:

```text
Review the implementation.
```

The runtime discovers:

```text
Repository instructions
Review skill
Architecture decisions
Relevant files
Review criteria
Allowed tools
Output contract
```

The shorter prompt is not better because fewer words are inherently superior.

It is better because system knowledge has been encoded where it belongs.

## Agent Reliability Comes From Environmental Structure

A well-designed agent environment reduces repeated inference.

Instead of asking the model to infer:

```text
Where should I look?

Which policy applies?

What does "review" mean?

What tools may I use?

Which source is authoritative?
```

the system encodes those answers explicitly.

This changes:

```text
Infer operating environment
```

into:

```text
Navigate operating environment
```

Less inference means fewer opportunities for inconsistent behavior.

## Project-Specific Knowledge Environments

Each significant project can maintain its own context environment.

For example:

```text
project/
|
+-- AGENTS.md
|
+-- knowledge/
|   +-- entities/
|   +-- concepts/
|   +-- architecture/
|
+-- workflows/
|
+-- skills/
|
+-- decisions/
|
+-- state/
```

The exact layout is domain-dependent.

The important properties are:

```text
Explicit routing
Structured knowledge
Scoped instructions
Inspectable state
Clear authority
Progressive loading
```

## Example: Social Media Knowledge Model

The source uses social-media analysis as an example.

A structured representation might include:

```text
[Post]
   |
   +-- published-at -> [Date]
   |
   +-- type -> [Content Type]
   |
   +-- topic -> [Topic]
   |
   +-- generated -> [Analytics]
```

Analytics might contain:

```text
Views
Engagement
Shares
Comments
Conversions
```

A question such as:

```text
What technical posts performed best in July?
```

can then resolve:

```text
Content Type -> Technical
        |
        v
Publication Date -> July
        |
        v
Analytics
        |
        v
Rank by selected performance metric
```

The model does not need to scan unrelated organizational information.

The graph provides a bounded route toward relevant data.

## Memory, Knowledge, and State Should Not Collapse Together

These concepts are related but should remain distinct.

```text
Memory
=
Durable information from previous execution
```

```text
Knowledge
=
Information describing the domain or environment
```

```text
State
=
Current execution condition
```

For example:

```text
"User prefers concise reports"
-> Memory
```

```text
"Service A depends on PostgreSQL"
-> Knowledge
```

```text
"Migration task is currently blocked"
-> State
```

Different lifecycles and retrieval policies may apply to each.

Treating all three as generic "memory" makes systems harder to reason about.

## Tools Are Context Too

Tool definitions consume context and influence model behavior.

Giving the model 100 tools when it needs three creates its own context problem.

Therefore tool routing should also be progressive:

```text
Task
  |
  v
Required Capability
  |
  v
Expose Relevant Tools
```

rather than:

```text
Task
  |
  v
Expose Everything
```

The same principle applies across the entire context system:

```text
Load what is needed.
Do not load everything that exists.
```

## Five-Layer Context Model

The complete architecture can be represented as:

```text
+--------------------------------------+
| Instructions                         |
|                                      |
| Rules                                |
| Workflows                            |
| Skills                               |
| Routing                              |
+--------------------------------------+
                  |
                  v
+--------------------------------------+
| Memory                               |
|                                      |
| Previous decisions                   |
| User/project history                 |
| Learned context                      |
+--------------------------------------+
                  |
                  v
+--------------------------------------+
| Knowledge                            |
|                                      |
| Documents                            |
| Graphs                               |
| Entities                             |
| Relationships                        |
| References                           |
+--------------------------------------+
                  |
                  v
+--------------------------------------+
| Tools                                |
|                                      |
| Search                               |
| Filesystem                           |
| APIs                                 |
| Execution                            |
+--------------------------------------+
                  |
                  v
+--------------------------------------+
| State                                |
|                                      |
| Current task                         |
| Progress                             |
| Environment                          |
| Intermediate results                 |
+--------------------------------------+
                  |
                  v
                 LLM
```

In practice these layers interact rather than executing strictly sequentially.

The separation is conceptual: each solves a different context problem.

## Key Notes

* Prompt engineering is a subset of context engineering.
* Agent quality depends on receiving the right context, not merely longer or more elaborate prompts.
* A useful context model consists of instructions, memory, knowledge, tools, and state.
* Root instruction files should primarily act as routing and operating contracts.
* Large projects benefit from hierarchical context rather than one universal instruction file.
* Context windows should be treated as budgets, not storage targets.
* More context is not automatically better context.
* Progressive disclosure reduces noise and unnecessary token consumption.
* Knowledge graphs model entities and their relationships.
* Graph traversal and semantic retrieval provide different forms of relevance.
* Knowledge graphs do not require graph databases.
* Filesystem structures and explicit metadata can encode graph relationships.
* Ranking context by relevance, recency, authority, confidence, or task fit can improve retrieval.
* Recency and authority should not be conflated.
* Graph engineering belongs primarily within the knowledge component of context engineering.
* Context routing can combine hierarchy, search, graphs, metadata, and ranking.
* The ideal context is the smallest sufficient context required for correct execution.
* Context selection must enforce authorization as well as relevance.
* Strong environmental structure allows user prompts to become simpler.
* Memory, knowledge, and state should remain separate concepts.
* Tool exposure should also be contextually scoped.
* Explicit context architecture reduces repeated model inference and improves reproducibility.

## Design Heuristic

When an agent produces poor results, do not immediately ask:

```text
How can I rewrite the prompt?
```

First inspect:

```text
Did it receive the correct instructions?

Did it retrieve the relevant memory?

Did it find the authoritative knowledge?

Did it have the required tools?

Did it understand the current state?
```

Then ask:

```text
Was irrelevant context competing with useful context?
```

Then:

```text
Could the system have discovered the required information
without the user explicitly placing it in the prompt?
```

If not, the problem may be architectural rather than linguistic.

## Context Engineering Loop

A useful implementation process is:

```text
1. Model the workflow.
2. Identify required context.
3. Classify context:
   - instructions
   - memory
   - knowledge
   - tools
   - state
4. Determine authoritative sources.
5. Create routing paths.
6. Add structured relationships where useful.
7. Add retrieval/ranking only where required.
8. Scope tools and data by authorization.
9. Load context progressively.
10. Measure task quality and context cost.
11. Refine routing based on failures.
```

The system should improve by correcting context failures rather than continually expanding prompts.

## Final Principle

The objective of context engineering is not to stuff more information into the model.

It is to make the correct information discoverable at the correct moment.

The architecture is:

```text
User Intent
     |
     v
Context Router
     |
     +-- Instructions
     +-- Memory
     +-- Knowledge
     +-- Tools
     +-- State
     |
     v
Smallest Sufficient Context
     |
     v
Agent Execution
```

Graph structures can improve navigation through the knowledge layer.

Scores and metadata can improve prioritization.

Root instruction files can define how context should be discovered.

But the central principle remains simple:

```text
Agent quality depends less on how much context exists
than on whether the right context arrives when it is needed.
```

That is the difference between repeatedly explaining everything to the model and engineering an environment that already knows how to find what matters.
