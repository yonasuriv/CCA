---
name: cca-sync
description: Reconcile filesystem-native routing and navigation files with the actual workspace while preserving instruction scope and native ICM, LLM Wiki, or CCA semantics. Use after files move, routing becomes stale, indexes drift, or the user asks to sync AGENTS.md, CONTEXT.md, or knowledge navigation. Updates only catalogs that actually exist or were explicitly requested and never treats CCA-preferred files as mandatory.
compatibility: Filesystem read/write access to the target workspace. No sibling skill required.
---

# CCA Sync

Sync routing to reality without restructuring the workspace or inventing semantics.

## Discover scope first

Identify the routing/navigation files that actually govern the workspace:

- root and nested `AGENTS.md` files;
- native harness instruction files;
- root/stage `CONTEXT.md` files;
- wiki indexes/maps/schema files;
- any explicitly adopted CCA history/catalog conventions.

Do not create missing CCA-preferred catalogs merely because sync knows about them. Creation belongs to an explicit scaffold/hardening request.

## Procedure

1. **Snapshot relevant disk structure.** Inspect only the directories governed by the catalogs being synchronized.
2. **Read each catalog in its scope.** Nested `AGENTS.md` files govern their own subtrees; do not flatten their entries into the root.
3. **Diff references against disk.** Classify:
   - broken reference — target no longer resolves;
   - missing routing entry — a newly added item clearly belongs in this catalog's declared scope;
   - stale descriptive metadata — description/date/count no longer matches the target and can be verified;
   - scope leak — a parent catalog duplicates or overrides guidance owned by a nearer scoped file;
   - semantic decision — filesystem evidence alone is insufficient to decide routing.
4. **Apply only unambiguous repairs authorized by the request.** Preserve file structure, wording style, and native profile semantics.
5. **Do not infer semantic state from timestamps or folder existence alone.** A file's presence proves existence, not completion, authority, freshness, or correctness unless the workspace explicitly defines that inference.
6. **Update history only when the active workspace defines a history mechanism and synchronization is supposed to mutate it.** Never invent a `log.md` convention for a native wiki that does not use one.
7. **Report** changed entries, unresolved semantic decisions, and any optional hardening opportunities separately.

## Production rules

- Disk is authoritative for path existence; workspace contracts/instructions are authoritative for meaning.
- Never move, rename, merge, or delete content in sync mode.
- Never fabricate summaries, dates, counts, completion state, or provenance.
- Preserve ICM's one-way references and selective routing.
- Preserve nested AGENTS.md scope.
- Preserve a native LLM Wiki's own index/schema conventions.
- Do not depend on another CCA skill for core execution.

## Verification

After edits, re-read every changed catalog and verify:

1. all modified path references resolve;
2. no routing entry was added outside that catalog's declared scope;
3. no parent/child instruction duplication was introduced;
4. no native compatibility rule was replaced with a CCA preference.
