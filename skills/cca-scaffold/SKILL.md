---
name: cca-scaffold
description: Add the smallest useful CCA-compatible routing layer to an existing repository without restructuring application or knowledge content. Use when the user wants to make a project easier for agents to navigate, add portable AGENTS.md guidance, add lightweight task routing, or introduce optional ICM-style stages or maintained knowledge while preserving the project's existing structure and native instruction files.
compatibility: Filesystem read/write access. No sibling skill or vendor-specific runtime required.
---

# CCA Scaffold

Add context structure in place. Do not reorganize the project unless the user explicitly asks for restructuring.

## First: detect what already exists

Survey only enough of the project to understand its current routing:

- root and nested `AGENTS.md` files;
- native harness instruction files such as `CLAUDE.md`;
- root/stage `CONTEXT.md` files;
- existing wiki/schema instructions;
- top-level application, documentation, test, and configuration directories.

Preserve native profiles. An ICM workspace is not a blank project, and an existing LLM Wiki must be interpreted through its own schema before CCA conventions are added.

## Modes

### Quick mode — default

Use when the repository layout already works.

1. Build a compact map of the directories and existing instruction scopes.
2. Add or improve a root `AGENTS.md` only when portable guidance is useful.
3. Preserve nested `AGENTS.md` scope. Do not flatten subtree-specific instructions into the root.
4. Add a small root `CONTEXT.md` only when explicit intent-to-context routing materially reduces exploration. It is optional for ordinary coding repositories.
5. Externalize stable conventions into a dedicated reference/config file only when those conventions already exist and would otherwise be duplicated. Do not invent `_config/` merely to satisfy a template.
6. If a harness-specific instruction file contains unique rules, preserve them until a safe canonicalization plan is clear. Never erase native behavior just to make `AGENTS.md` canonical on paper.
7. Report every file created or changed and why it was necessary.

### Full mode

Use only when the project actually needs a new capability.

**Pipeline:** add ICM-compatible stages using lowercase hyphenated names such as `stages/01-collect/`. Every stage gets a small `CONTEXT.md` with the exact `Inputs` / `Process` / `Outputs` shape and its own `output/` handoff folder.

**Maintained knowledge:** discover whether the project already has a knowledge schema. If not, create the smallest knowledge structure the user needs. A CCA-hardened `raw/`, `wiki/`, `wiki/index.md`, `log.md` layout is an option, not a universal LLM Wiki requirement.

## Change safety

Before writing:

1. Read the target file if it exists.
2. Preserve unrelated content and native semantics.
3. For any change that would replace, merge, move, or substantially rewrite existing instructions, present the proposed change or diff and obtain approval unless the user explicitly authorized direct remediation.
4. Never delete or rename application content in scaffold mode.

## Production rules

- Every routing entry must resolve to something real or something created in the same operation.
- One fact, one canonical home; pointers are cheaper than duplicated rules.
- Keep routing compact and load context selectively.
- Do not assume a universal precedence between `AGENTS.md` and harness-specific instruction files.
- Do not require another CCA skill to finish this skill's core operation.
- Do not claim CCA conformance unless the workspace intentionally adopted the relevant CCA profile and was validated against it.

## Verification

After scaffolding, simulate a fresh agent:

1. Can it identify the repository and applicable instruction scope?
2. Can it route one representative task without broad filesystem exploration?
3. If a pipeline was added, can it execute one stage from the contract alone?
4. If maintained knowledge was added, can it find the implementation's own navigation/schema instructions?

Report native compatibility separately from optional CCA hardening opportunities.
