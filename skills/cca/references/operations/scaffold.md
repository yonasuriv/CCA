# Scaffold mode

Add context structure in place. Do not reorganize the project unless the user explicitly asks for restructuring.

## First: detect what already exists

Survey only enough of the project to understand its current routing and organization:

- root and nested `AGENTS.md` files;
- native harness instruction files such as `CLAUDE.md`;
- root/stage `CONTEXT.md` files;
- existing wiki/schema instructions;
- obvious method overlays such as PARA Projects/Areas/Resources/Archives or Zettelkasten note collections;
- top-level application, documentation, test, and configuration directories.

Preserve native profiles and method boundaries. An ICM workspace is not a blank project, an existing LLM Wiki must be interpreted through its own schema before CCA conventions are added, and an outer PARA tree is not permission to rewrite a nested native workspace.

If the request is actually about choosing among several methods/forms or restructuring boundaries, switch to `architect` mode rather than turning scaffold into architecture design.

## Quick mode — default

Use when the repository layout already works.

1. Build a compact map of the directories and existing instruction scopes.
2. Add or improve a root `AGENTS.md` only when portable guidance is useful.
3. Preserve nested `AGENTS.md` scope. Do not flatten subtree-specific instructions into the root.
4. Add a small root `CONTEXT.md` only when explicit intent-to-context routing materially reduces exploration. It is optional for ordinary coding repositories.
5. Externalize stable conventions only when they already exist and would otherwise be duplicated. Do not invent `_config/` merely to satisfy a template.
6. If a harness-specific instruction file contains unique rules, preserve them until a safe canonicalization plan is clear.
7. Preserve recognizable method organization. Do not add CCA metadata merely to restate obvious PARA, Zettelkasten, project, or wiki paths.
8. Report every file created or changed and why it was necessary.

## Full mode

Use only when the project actually needs a new capability and the desired architecture is already clear.

**Pipeline:** add ICM-derived stages using lowercase hyphenated names such as `stages/01-collect/`. Every stage gets a small `CONTEXT.md` with the exact ICM `Inputs` / `Process` / `Outputs` shape and its own `output/` handoff folder.

Adding ICM-derived stage contracts to an ordinary repository does not by itself make that repository a native ICM workspace. Only claim native compatibility after the full applicable ICM profile passes.

**Maintained knowledge:** discover whether the project already has a knowledge schema. If not, create the smallest knowledge structure the user needs. A CCA-hardened `raw/`, `wiki/`, `wiki/index.md`, `log.md` layout is an option, not a universal LLM Wiki requirement.

**Method-organized workspace:** preserve declared PARA/Zettelkasten/BASB organization. Scaffold routing around existing boundaries rather than normalizing them into one CCA tree.

## Change safety

Before writing:

1. Read the target file if it exists.
2. Preserve unrelated content, native semantics, and method boundaries.
3. For changes that replace, merge, move, or substantially rewrite existing instructions, present the proposed migration/diff unless direct remediation was already authorized.
4. Never delete or rename application content in scaffold mode.

## Verification

After scaffolding, simulate a fresh agent:

1. Can it identify the repository, applicable instruction scope, and relevant method/native boundary?
2. Can it route one representative task without broad filesystem exploration?
3. If a pipeline was added, can it execute one stage from the contract alone?
4. If maintained knowledge was added, can it find the implementation's own navigation/schema instructions?
5. If native ICM compatibility is claimed, did the complete applicable ICM acceptance surface pass?

Use `lint` mode for profile-aware validation.