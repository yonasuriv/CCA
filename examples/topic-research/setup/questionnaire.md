# Setup questionnaire — topic-research (completed example)

> One-time onboarding, answered in a single pass. These answers populated
> `_config/`, the catalogs, and the stage contracts. Never re-asked per run.

## Identity

1. **What is this workspace, and what does it produce?**
   A research workspace on electric aviation. It accumulates sources into a
   maintained wiki and produces a five-minute weekly brief.
2. **Who reviews, and what do they care about?**
   The domain lead. Cares about what changed and what it means for the
   adoption thesis; allergic to hype and unsourced claims.

## Voice and conventions

3. **Good-output examples:** two past briefs pasted during setup; voice
   extracted into `_config/voice.md` (direct, change-first, attributed).
4. **Never:** predictions without confidence notes; multi-claim bullets;
   over 400 words.
5. **Formats:** markdown everywhere; frontmatter on wiki pages and outputs.

## Domain and knowledge

6. **Core tracking:** operators (entities), battery density and
   certification (concepts), one standing thesis.
7. **Source flow:** articles clipped to `raw/` by the human, one at a time;
   ingestion is supervised, not batch.

## Workflow

8. **One real run:** collect from wiki → review → draft brief → review →
   send. Reviews happen at both gates; selection of findings (stage 02
   checkpoint) is the moment that matters most.
9. **Mechanical work:** none yet. If clipping volume grows, a script will
   fetch and rename sources into `raw/` — the agent should not do that.

## Tooling

10. **Agents used:** Claude Code primarily, occasionally others — so
    `CLAUDE.md` ships as a thin adapter and `AGENTS.md` stays canonical.
