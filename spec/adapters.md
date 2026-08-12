# Adapter conventions

CCA's canonical root is `AGENTS.md`. Many agent tools read their own
instruction file. Adapters bridge the two without forking content.

## The rule

> An adapter is a pointer, not a copy. Two to five lines. It names the
> authoritative file and nothing else.

If a tool upgrades to natively read `AGENTS.md`, delete the adapter.

## Reference adapters

**`CLAUDE.md`** (Claude Code, and ICM's historical Layer 0):

```markdown
# CLAUDE.md

This workspace follows the Convergent Context Architecture.
Read `AGENTS.md` in this directory — it is the authoritative root catalog.
Then read `CONTEXT.md` for task routing.
```

**`GEMINI.md`** (Gemini CLI):

```markdown
# GEMINI.md

Read `AGENTS.md` in this directory; it is the authoritative root catalog
for this workspace. Follow its routing rules.
```

**`.cursorrules`** (Cursor):

```text
This workspace follows the Convergent Context Architecture. Before acting, read
AGENTS.md (authoritative root catalog) and CONTEXT.md (task routing). Follow
their routing and context-loading rules.
```

**`.windsurfrules`** (Windsurf):

```text
Read AGENTS.md first — it is the authoritative root catalog for this
workspace. Follow its routing rules and load only the context your task needs.
```

**`.github/copilot-instructions.md`** (GitHub Copilot):

```markdown
This repository follows the Convergent Context Architecture. Read `AGENTS.md`
for the directory map and routing rules; read `CONTEXT.md` files for
stage-specific contracts. `AGENTS.md` is authoritative.
```

## Generating adapters

`cca-scaffold` and `cca-architect` offer to emit adapters for the tools the
user names. When writing one:

1. Keep it under five lines.
2. Point at `AGENTS.md` by name; call it authoritative.
3. Never restate rules, directory contents, or conventions — that creates a
   second home for facts, and two homes drift.
4. If the tool supports file inclusion/import syntax, prefer that over prose.

## Detecting and repairing forked adapters

`cca-lint` flags adapters that contain substantive rules (heuristic: an
adapter longer than ~15 lines, or one whose content duplicates sections of
`AGENTS.md`). Repair by moving the content into the canonical home and
replacing it with a pointer.
