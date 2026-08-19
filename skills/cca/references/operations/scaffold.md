# Scaffold mode

Add context structure in place. Do not reorganize the project unless the user explicitly asks for restructuring.

## First: detect what already exists

Survey only enough of the project to understand its current routing and organization:

- root and nested `AGENTS.md` files;
- native harness instruction files such as `CLAUDE.md`;
- the Layer-0 skeleton map when present;
- root/stage contract files resolved from that map, else default `CONTEXT.md`;
- existing wiki/schema instructions;
- obvious method overlays such as PARA Projects/Areas/Resources/Archives or Zettelkasten note collections;
- top-level application, documentation, test, and configuration directories.

Preserve native profiles and method boundaries. An ICM workspace is not a blank project, an existing LLM Wiki must be interpreted through its own schema before CCA conventions are added, and an outer PARA tree is not permission to rewrite a nested native workspace.

If the request is actually about choosing among several methods/forms or restructuring boundaries, use `cca` in `architect` mode rather than turning scaffold into architecture design.

## Modes

### Quick mode — default

Use when the repository layout already works.

1. Build a compact map of the directories and existing instruction scopes.
2. Add or improve a root `AGENTS.md` only when portable guidance is useful. When creating or updating it, include an ICM / CCA skeleton map (roles → paths), even if every path is still the default `CONTEXT.md`.
3. Preserve nested `AGENTS.md` scope. Do not flatten subtree-specific instructions into the root.
4. Add a small root workspace router (default `CONTEXT.md`, or the mapped name) only when explicit intent-to-context routing materially reduces exploration. It is optional for ordinary coding repositories. If using a non-default name, update the L0 skeleton map in the same edit.
5. When adding folder contracts, write the mapped L2 filename (default `CONTEXT.md`) and keep the L0 map in sync.
6. Externalize stable conventions into a dedicated reference/config file only when those conventions already exist and would otherwise be duplicated. Do not invent `_config/` merely to satisfy a template.
7. If a harness-specific instruction file contains unique rules, preserve them until a safe canonicalization plan is clear. Never erase native behavior just to make `AGENTS.md` canonical on paper.
8. Preserve recognizable method organization. Do not add CCA metadata merely to restate obvious PARA, Zettelkasten, project, or wiki paths.
9. Report every file created or changed and why it was necessary.

### Full mode

Use only when the project actually needs a new capability and the desired architecture is already clear.

**Pipeline:** add ICM-derived stages using lowercase hyphenated names such as `stages/01-collect/`. Every stage gets a small folder contract (default `CONTEXT.md`, or the L0-mapped name outside native ICM) with the exact ICM `Inputs` / `Process` / `Outputs` shape and its own `output/` handoff folder. Keep the L0 skeleton map updated.

Adding ICM-derived stage contracts to an ordinary repository does **not** by itself make that repository a native ICM workspace. Only claim **ICM native compatibility** after the full applicable ICM profile passes: five-layer routing, native `CLAUDE.md`, root routing, setup/status behavior, questionnaire rules, naming, handoffs, one-way references, selective loading, CONTEXT purity, quality guardrails, and all other applicable current ICM conventions and workspace-builder validation checks.

If the user explicitly requests a complete native ICM workspace, use `cca` in `architect` mode for the architecture/profile decision when available, then scaffold the approved shape. Do not label a partial scaffold as fully ICM-compatible.

**Maintained knowledge:** discover whether the project already has a knowledge schema. If not, create the smallest knowledge structure the user needs. A CCA-hardened `raw/`, `wiki/`, `wiki/index.md`, `log.md` layout is an option, not a universal LLM Wiki requirement. When creating a hardened bundle from scratch, also add human `notes/` (or zettelkasten) if notes were requested, document supersession for raw, seed one source→wiki citation, and copy `assets/scripts/capture-source.py` / `verify-sources.py` into the workspace when hardening immutability.

**Method-organized workspace:** preserve declared PARA/Zettelkasten/BASB organization. Scaffold routing around existing boundaries rather than normalizing them into one CCA tree. For personal hybrids (projects + notes/research + wiki), follow `../architect/methods.md` Personal hybrid defaults.

## Change safety

Before writing:

1. Read the target file if it exists.
2. Preserve unrelated content, native semantics, and method boundaries.
3. For any change that would replace, merge, move, or substantially rewrite existing instructions, present the proposed change or diff and obtain approval unless the user explicitly authorized direct remediation.
4. Never delete or rename application content in scaffold mode.

## Production rules

- Every routing entry must resolve to something real or something created in the same operation.
- One fact, one canonical home; pointers are cheaper than duplicated rules.
- Keep routing compact and load context selectively.
- Infer ordinary filesystem semantics when safe; do not build a manifest merely to restate paths.
- Do not assume a universal precedence between `AGENTS.md` and harness-specific instruction files.
- Cross-skill coordination uses semantic skill names, never sibling filesystem paths.
- Do not claim CCA conformance unless the workspace intentionally adopted the relevant CCA profile and was validated against it.
- Do not claim native ICM compatibility for a repository that merely borrows ICM stage-contract patterns.
- Do not invent PARA, Zettelkasten, or BASB native compatibility claims.
- Do not assume contract filenames: resolve from the L0 skeleton map, else default to `CONTEXT.md`.

## Verification

After scaffolding, simulate a fresh agent:

1. Can it identify the repository, applicable instruction scope, and any relevant method/native boundary?
2. Can it route one representative task without broad filesystem exploration?
3. If a pipeline was added, can it execute one stage from the contract alone?
4. If maintained knowledge was added, can it find the implementation's own navigation/schema instructions?
5. If native ICM compatibility is claimed, did the complete applicable ICM acceptance surface pass rather than only the stage-contract subset?

When the CCA suite is available, use `cca` in `lint` mode for profile-aware validation. Report native compatibility separately from optional CCA hardening or method-preservation findings.
