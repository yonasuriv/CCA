# AI Product Architecture: Build Software Inside the Service

## Core Principle

Many AI companies are building vertically around capabilities that model providers are rapidly absorbing.

A typical pattern looks like:

```text
Model
  |
  v
AI capability
  |
  v
Product feature
  |
  v
SaaS
```

Examples include:

```text
Summarization SaaS
Research SaaS
Writing SaaS
Support Agent SaaS
Sales Agent SaaS
Document Analysis SaaS
```

The problem is that the underlying capability is improving continuously at the model and platform layer.

What required a dedicated product today may become:

```text
Native model capability
Built-in tool
Platform feature
API primitive
```

tomorrow.

The more tightly a product's value maps to one model capability, the more exposed it is to capability compression.

A more durable architecture is:

```text
Domain Environment
      +
Structured Data
      +
Workflows
      +
Operational Knowledge
      +
AI Capabilities
      =
Service Outcome
```

The AI software exists inside the service.

It is not necessarily the service itself.

## SaaS vs. Software Inside a Service

Traditional SaaS generally packages software as the product:

```text
Customer
   |
   v
Software Application
   |
   v
Feature Set
```

In an AI-native service model, software may instead be one execution layer inside a broader operational system:

```text
Customer
   |
   v
Service
   |
   +-- Domain knowledge
   +-- Structured environment
   +-- Customer context
   +-- Data
   +-- Processes
   +-- AI
   +-- Automation
   +-- Human expertise
   |
   v
Outcome
```

The distinction is important.

In the first model:

```text
The software is the value proposition.
```

In the second:

```text
The software helps deliver the value proposition.
```

This makes the product less dependent on any individual AI primitive remaining scarce.

## The Vertical Feature Trap

Many AI startups build vertically from a model capability.

For example:

```text
LLM
 |
 v
Can analyze contracts
 |
 v
Contract Analysis Agent
 |
 v
Contract Analysis SaaS
```

The entire product is therefore coupled to the assumption that:

```text
Contract analysis remains difficult or unavailable elsewhere.
```

If the underlying model later performs high-quality contract analysis natively:

```text
Model update
    |
    v
Capability becomes commodity
    |
    v
Feature differentiation collapses
```

The product may still survive through distribution, integrations, data, workflow depth, compliance, or other advantages.

But if its only meaningful value was the AI capability itself, the product boundary was too low.

## Capability Compression

AI development creates a recurring pattern:

```text
Complex application behavior
        |
        v
Common workflow
        |
        v
Platform abstraction
        |
        v
Native capability
```

For example:

```text
Custom retrieval pipeline
        ->
Managed retrieval

Custom tool router
        ->
Native tool calling

Custom coding agent
        ->
General coding runtime

Custom document extraction
        ->
Native multimodal understanding
```

This process can be called capability compression.

Functionality that once justified substantial application code gradually collapses into infrastructure.

Products built directly around those capabilities are therefore structurally vulnerable.

## Build Around What Does Not Commoditize Easily

More durable value usually exists in things that cannot be reproduced merely by releasing a better model.

Examples include:

```text
Proprietary data
Historical data
Customer-specific context
Domain-specific workflows
Operational knowledge
Human expertise
Relationships between data
Business processes
Integrations
Feedback history
Decision history
Organizational structure
Trust
Distribution
```

These components create an environment around the model.

Conceptually:

```text
Commodity AI
     |
     v
Private Environment
     |
     +-- Data
     +-- Context
     +-- Processes
     +-- Relationships
     +-- History
     +-- Constraints
     |
     v
Domain-specific capability
```

The model may be interchangeable.

The environment is not.

## The Environment Is the Durable Layer

Consider two systems using the same frontier model.

System A:

```text
Model
  |
  v
Generic instructions
  |
  v
Generic output
```

System B:

```text
Model
  |
  v
Company environment
  |
  +-- Customer records
  +-- Internal knowledge
  +-- Historical decisions
  +-- Workflows
  +-- Domain rules
  +-- Tools
  +-- Permissions
  +-- Quality criteria
  |
  v
Operational output
```

System B has access to information and structure that the base model cannot provide independently.

The model is no longer the primary source of differentiation.

The environment is.

## Structured Data Matters More as Models Improve

Better models reduce the amount of application logic required to interpret information.

This makes high-quality context more valuable, not less.

As model capability increases:

```text
Need for custom reasoning code
          decreases

Value of high-quality context
          increases
```

A sufficiently capable model can potentially perform many workflows if given:

```text
the right instructions
the right data
the right tools
the right constraints
the right environment
```

The strategic problem therefore shifts from:

```text
How do we build smarter agent logic?
```

toward:

```text
How do we construct the environment in which a capable model can operate reliably?
```

## Environment Engineering

An AI environment can contain:

```text
environment/
|
+-- organization/
|   +-- teams/
|   +-- responsibilities/
|
+-- knowledge/
|   +-- domain/
|   +-- policies/
|
+-- workflows/
|   +-- intake/
|   +-- analysis/
|   +-- delivery/
|
+-- customers/
|
+-- decisions/
|
+-- tools/
|
+-- schemas/
|
+-- examples/
|
+-- AGENTS.md
```

The environment provides more than retrieval.

It describes:

```text
What exists
How things relate
What should happen
Who owns what
Which rules apply
Which tools are available
What good output looks like
```

AI then operates inside that structure.

## From Product Feature to Operating Environment

Consider a hypothetical vulnerability-management product.

Feature-centric architecture:

```text
Vulnerability
      |
      v
AI remediation generator
      |
      v
Recommendation
```

This capability is highly exposed to model commoditization.

Environment-centric architecture:

```text
Vulnerability
      |
      v
Organization Context
      |
      +-- Asset ownership
      +-- Architecture
      +-- Existing controls
      +-- Business criticality
      +-- Code repositories
      +-- Previous findings
      +-- Accepted risks
      +-- Remediation policies
      +-- Engineering workflows
      |
      v
AI-assisted reasoning
      |
      v
Organization-specific remediation process
```

A better base model improves this system.

It does not replace the surrounding environment.

## The Model Should Be Replaceable

A useful architectural test is:

```text
What happens if the underlying model becomes 10x better?
```

Weak architecture:

```text
Better model
   |
   v
Our product feature becomes redundant
```

Stronger architecture:

```text
Better model
   |
   v
Our environment becomes more capable
```

This suggests another principle:

> The model should ideally be a replaceable capability provider rather than the location of the product's durable value.

Conceptually:

```text
Durable Service Layer
        |
        v
AI Capability Interface
        |
        +-- Model A
        +-- Model B
        +-- Model C
        +-- Future Model
```

The service survives model turnover.

## Opinionated Structure Can Also Be Valuable

Not all differentiated context must be proprietary data.

A company may also encode a valuable way of working.

For example:

```text
Domain methodology
Decision framework
Evaluation criteria
Workflow design
Operational playbook
Taxonomy
Quality standards
```

These represent opinionated structure.

Two companies may have access to the same raw information and the same models but produce different outcomes because they organize and interpret that information differently.

Therefore:

```text
Data
+
Structure
+
Methodology
+
Execution
=
Differentiated service
```

The structure itself can become intellectual property.

## Capture the Work, Not Just the Output

A strong AI service should accumulate knowledge through use.

Instead of each execution disappearing after completion:

```text
Request
  |
  v
AI
  |
  v
Output
  |
  X
```

the system can capture:

```text
Request
  |
  v
Execution
  |
  +-- Context used
  +-- Decisions made
  +-- Corrections
  +-- Human feedback
  +-- Outcome
  |
  v
Updated environment
```

This creates a feedback loop:

```text
Use
 |
 v
More structured knowledge
 |
 v
Better future execution
 |
 v
More use
```

The environment becomes progressively more valuable.

## Service as a Learning System

The resulting service can behave as a compounding system:

```text
Initial Domain Knowledge
        |
        v
Customer Work
        |
        v
New Context + Feedback
        |
        v
Structured Memory
        |
        v
Improved Execution
        |
        v
Better Outcome
```

This is much harder to commoditize than a static AI feature.

A competitor may obtain the same model.

They do not automatically obtain:

```text
your accumulated context
your workflow knowledge
your customer history
your corrections
your operational graph
your domain structure
```

## Wrong Abstraction Layer

The broader architectural issue is abstraction.

Too low:

```text
Prompt
Agent
Model wrapper
Tool router
Automation
```

More durable:

```text
Workflow
Environment
Knowledge
Data
Process
Outcome
```

The lower layers will continue changing rapidly.

The higher layers describe the actual work.

An architecture that places its durable value higher in the stack is more capable of absorbing technological change.

## A Better Stack

A durable AI service can be represented as:

```text
+--------------------------------------+
| Outcome                              |
+--------------------------------------+
                  |
                  v
+--------------------------------------+
| Service                              |
|                                      |
| Domain process                       |
| Customer experience                  |
| Human expertise                      |
| Operational guarantees               |
+--------------------------------------+
                  |
                  v
+--------------------------------------+
| Environment                          |
|                                      |
| Structured data                      |
| Knowledge                            |
| Workflows                            |
| Memory                               |
| Relationships                        |
| Policies                             |
+--------------------------------------+
                  |
                  v
+--------------------------------------+
| Capabilities                         |
|                                      |
| Reasoning                            |
| Search                               |
| Generation                           |
| Tool use                             |
| Automation                           |
+--------------------------------------+
                  |
                  v
+--------------------------------------+
| Replaceable Infrastructure           |
|                                      |
| Models                               |
| APIs                                 |
| Agent runtimes                       |
| Frameworks                           |
+--------------------------------------+
```

The durable value should generally concentrate toward the top.

## Key Notes

- Many AI startups are packaging individual model capabilities as standalone SaaS products.
    
- Capabilities that are currently difficult may become native model or platform features.
    
- Products tightly coupled to one AI capability are exposed to capability compression.
    
- The durable product boundary should generally sit above commodity AI primitives.
    
- Software can exist inside a service rather than being the entire service.
    
- The service should be organized around the customer outcome.
    
- Proprietary and customer-specific data become increasingly important as models commoditize.
    
- Structured environments can create stronger differentiation than custom agent logic.
    
- Domain workflows, methodologies, relationships, and historical context are difficult for a base model to reproduce independently.
    
- Better models should improve the product rather than invalidate it.
    
- Model implementations should therefore remain replaceable where possible.
    
- Opinionated structure can itself be valuable intellectual property.
    
- AI services should capture corrections, decisions, outcomes, and operational knowledge during execution.
    
- Accumulated context can create a compounding advantage.
    
- The environment surrounding the model is increasingly part of the product.
    
- Building at the prompt, wrapper, or agent layer alone is often too low-level to provide durable differentiation.
    
- Stable value generally exists closer to workflows, environments, data, and outcomes.
    

## Design Heuristic

When evaluating an AI product idea, ask:

```text
If the frontier model gets dramatically better next year,
what remains valuable?
```

If the answer is:

```text
Our AI feature
```

the product may be fragile.

If the answer is:

```text
Our data
Our environment
Our workflows
Our methodology
Our integrations
Our customer history
Our operational knowledge
Our ability to produce the outcome
```

the architecture is operating at a more durable layer.

Then ask:

```text
Does a better model compete with us,
or does a better model make our service better?
```

The preferred answer is:

```text
Better models improve the service.
```

## Final Principle

Do not build the company around capabilities that the underlying AI platform is likely to commoditize.

Build the company around the environment in which those capabilities become useful.

The durable architecture is closer to:

```text
Structured Environment
        +
Domain Knowledge
        +
Private Data
        +
Workflows
        +
Replaceable AI
        =
Service Outcome
```

than:

```text
AI Feature
   =
Product
```

The software still matters.

The model still matters.

The agents still matter when they are useful.

But they are implementation components inside the service.

The durable value is the structured system surrounding them and the outcome that system consistently produces.