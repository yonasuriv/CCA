# Setup questionnaire — [WORKSPACE NAME]

> One-time onboarding. Configure the factory, not the product: answers here
> populate `_config/`, catalogs, and contracts — the system, not one run.
> Ask everything at once, in one pass. Never re-ask on later runs.

## Identity

1. What is this workspace called, and what does it produce (or know)?
2. Who reviews its output, and what do they care most about?

## Voice and conventions (content workspaces)

3. Paste 2–3 examples of output you consider *good*. (Concrete examples beat
   descriptions — the agent extracts voice from samples, not adjectives.)
4. What should the output never do? (hard constraints, banned patterns)
5. Any required formats, lengths, structures, or citation styles?

## Domain and knowledge (knowledge workspaces)

6. What are the 3–5 core entities and concepts this workspace must track?
7. Where do sources come from (articles, papers, transcripts, exports), and
   how do they arrive (you drop them in `raw/`? clipped? synced?)?

## Workflow

8. Walk through one real run, step by step. Where do you want to review or
   redirect before the next step continues? (These become stage boundaries
   and checkpoints.)
9. What is mechanical here — fetching, moving, formatting, sending — that a
   plain script should do instead of the agent?

## Tooling

10. Which agent tools will operate this workspace? (Determines which adapter
    files to generate: CLAUDE.md, GEMINI.md, .cursorrules, …)
