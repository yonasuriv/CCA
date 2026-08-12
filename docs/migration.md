# Compatibility and hardening guide

Native compatibility does not require migration. Use this guide only when adding CCA portability or maintenance conventions improves the workspace.

## Existing ICM workspace

Keep native ICM structure unchanged: `CLAUDE.md`, root/stage `CONTEXT.md`, `stages/01-name/`, references, and `output/` handoffs remain valid.

Optional hardening:

1. Add portable `AGENTS.md` guidance for agents that support it.
2. Keep native `CLAUDE.md` behavior intact. Where guidance is shared, use a minimal pointer/include instead of duplicated rules.
3. Add maintained knowledge only if the workflow needs synthesis that persists across runs.
4. Validate ICM native compatibility before checking optional CCA conventions.

Do not rename stages, change the canonical Inputs table, or rewrite stage contracts merely to make them look more CCA-specific.

## Existing LLM Wiki

Keep the implementation's own schema, directories, navigation, and maintenance procedures.

Optional hardening may add:

- portable `AGENTS.md` routing;
- stronger provenance or lifecycle metadata;
- an explicit index/history mechanism when the existing wiki would benefit from one;
- an ICM-compatible pipeline that consumes maintained knowledge.

CCA's preferred `raw/`, `wiki/`, `wiki/index.md`, `log.md`, frontmatter, and page taxonomies are implementation options, not universal LLM Wiki requirements.

## Existing coding repository

Start with the smallest useful change:

1. Add or improve root `AGENTS.md` if portable agent guidance is useful.
2. Preserve nested `AGENTS.md` scope in monorepos/subprojects.
3. Add `CONTEXT.md` only when explicit intent-to-context routing materially reduces exploration.
4. Do not move source code, tests, configuration, or docs into CCA-specific folders by default.
5. Add stages only for genuine sequential workflows; add maintained knowledge only when it should compound across sessions.

## Existing harness-specific instruction file

Do not blindly replace `CLAUDE.md`, `GEMINI.md`, or another native instruction file.

1. Determine how the target harness discovers and scopes instructions.
2. Identify unique substantive guidance in each file.
3. Choose one canonical body of shared rules where possible.
4. Use the harness's native include/import mechanism if available; otherwise use the smallest safe pointer.
5. Re-test the native harness after the change.

CCA cannot override a harness's own precedence rules.

## Unstructured folder

Use `cca-architect` in restructure mode:

1. audit the current structure and native conventions;
2. classify function without forcing relocations;
3. propose a migration map including compatibility impact;
4. obtain explicit approval before moves, merges, renames, or deletions;
5. apply only the approved map;
6. validate the original native profile first, then any intentional CCA conformance.

## After hardening

Check the profile you actually claim:

- **ICM:** native Layer 0 remains usable; stages are `01-name`; contracts retain `Inputs` / `Process` / `Outputs` and canonical Inputs columns; references remain one-way and selectively loaded.
- **LLM Wiki:** maintained synthesis still follows the implementation's own schema; CCA-specific metadata has not been mislabeled as upstream-required.
- **AGENTS.md:** nested scope remains intact; portable guidance does not contradict native harness instructions.
- **Agent Skills:** each skill can execute independently using skill-local relative resources.
- **CCA:** optional conventions are validated only where intentionally adopted.

Finally run a fresh-agent walk test: orient, perform one representative operation, and report state using durable files alone.
