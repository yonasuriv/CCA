# AGENTS.md -- [WORKSPACE NAME]

> Portable agent guidance. Keep this file compact and scoped to this directory tree. Nested `AGENTS.md` files may add more specific instructions for subtrees.

## What this is

[One to three sentences: what this workspace produces, maintains, or contains.]

## Directory map

| Path | Purpose |
|---|---|
| `[path]` | [What lives here and when an agent should read it] |
| `[path]` | [What lives here and when an agent should read it] |

List only directories/files that actually exist or are being created now. Do not force pipeline/wiki rows into a workspace that does not need them.

## Routing rules

- **[common intent]** → [smallest relevant router/file/folder]
- **[common intent]** → [smallest relevant router/file/folder]
- **[common intent]** → [smallest relevant router/file/folder]

## Operating rules

1. Load only context needed for the current task.
2. Keep one canonical home for substantive rules; link instead of duplicating them.
3. Preserve native workspace conventions and harness-specific entry points.
4. Treat human-edited files as authoritative handoffs where the workflow defines them that way.
5. Do not infer completion, authority, or freshness from file existence alone unless this workspace explicitly defines that rule.

## Instruction interoperability

`AGENTS.md` is the authoritative Layer-0 catalog in this workspace. It does not override a harness's native discovery rules. If a harness needs its own entry file (`CLAUDE.md`, `GEMINI.md`, ...), that file is created by directive as a single-line `@ AGENTS.md` include, never a second hand-maintained copy of this routing.

## Context router

This workspace's context/router file is the root `CONTEXT.md` by default. If this workspace renames it, the name is declared here as a single line, and the declared file keeps the same mechanics (preferred tokens/lines and routing behavior) ICM assigns to that layer, as recommendations:

- Context router: `CONTEXT.md`
