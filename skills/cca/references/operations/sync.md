# Sync mode

Sync routing to reality without restructuring the workspace or inventing semantics.

## Discover scope first

Identify the routing/navigation files that actually govern the workspace:

- root and nested `AGENTS.md` files;
- native harness instruction files;
- the Layer-0 skeleton map when present (`spec.md` §5.1);
- root/stage contract files resolved from that map, else default `CONTEXT.md`;
- wiki indexes/maps/schema files;
- any explicitly adopted CCA history/catalog conventions;
- declared method-overlay boundaries when they affect routing.

Do not create missing CCA-preferred catalogs merely because sync knows about them. Creation belongs to an explicit scaffold/hardening request; use `cca` in `scaffold` mode when that is the actual operation.

## Procedure

1. **Snapshot relevant disk structure.** Inspect only the directories governed by the catalogs being synchronized.
2. **Read each catalog in its scope.** Nested `AGENTS.md` files govern their own subtrees; do not flatten their entries into the root. Resolve contract filenames from the L0 skeleton map before assuming `CONTEXT.md`.
3. **Diff references against disk.** Classify:
   - broken reference — target no longer resolves;
   - missing routing entry — a newly added item clearly belongs in this catalog's declared scope;
   - stale descriptive metadata — description/date/count no longer matches the target and can be verified;
   - scope leak — a parent catalog duplicates or overrides guidance owned by a nearer scoped file;
   - semantic decision — filesystem evidence alone is insufficient to decide routing.
4. **Apply only unambiguous repairs authorized by the request.** Preserve file structure, wording style, native profile semantics, and method boundaries.
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
- Preserve declared PARA/Zettelkasten/BASB boundaries rather than flattening them into CCA catalogs.
- Cross-skill coordination uses semantic skill names, never sibling filesystem paths.

## Verification

After edits, re-read every changed catalog and verify:

1. all modified path references resolve;
2. no routing entry was added outside that catalog's declared scope;
3. no parent/child instruction duplication was introduced;
4. no native compatibility rule or method boundary was replaced with a CCA preference.
