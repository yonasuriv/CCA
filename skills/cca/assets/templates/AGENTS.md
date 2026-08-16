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

## ICM / CCA skeleton map

Cold agents MUST NOT assume contract filenames. Resolve each role from this table; if a role is omitted, use the default (`CONTEXT.md` for L1/L2). This map is what makes CCA and ICM workspaces walk the same way when names differ.

| Role | Path in this workspace |
|---|---|
| L0 entry | `AGENTS.md` |
| L1 workspace router | `CONTEXT.md` |
| L2 folder contract | `CONTEXT.md` |
| L3 factory stamps | `_templates/` |
| Status scan (no memory) | [e.g. `stages/*/output/` OR `Resources/knowledge/log.md` + wiki index] |
| Form | [pipeline \| umbrella \| knowledge bundle \| record library \| context map \| system map \| hybrid] |
| Native ICM pipeline | [yes \| no] |

Rename any non-native default only by editing this table. Keep role semantics unchanged. Under native ICM, keep upstream filenames (`CLAUDE.md`, `CONTEXT.md`) and mirror them here.