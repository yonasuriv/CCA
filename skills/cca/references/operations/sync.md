# Sync mode

Sync routing and derived navigation to reality without restructuring the target or inventing semantics.

## Discover scope first

Identify the boundary and routing/navigation files that actually govern the target:

- root and nested `AGENTS.md` files;
- native harness/upstream instruction files;
- semantic-role/binding declarations where present;
- root/local contracts required by the active upstream/profile;
- wiki indexes/maps/schema files;
- any explicitly adopted CCA history/catalog conventions;
- declared method-overlay boundaries when they affect routing;
- the CCA Hybrid Workspace Profile contract when the target matches it.

Do not create missing CCA-preferred catalogs merely because sync knows about them. Creation belongs to an explicit scaffold/profile-init request.

## Procedure

1. **Resolve the target boundary.** Never treat the installed CCA skill directory as the workspace.
2. **Snapshot relevant disk structure.** Inspect only directories governed by the bindings/catalogs being synchronized.
3. **Read each applicable authority in scope.** Nested instructions govern their subtrees; do not flatten them into the root. Resolve semantic roles and their bindings rather than guessing default filenames.
4. **Diff references against disk.** Classify:
   - broken reference — target no longer resolves;
   - missing routing entry — a new item clearly belongs in a catalog's declared scope;
   - stale descriptive metadata — description/date/count no longer matches verifiable target state;
   - binding drift — a derived consumer still points to a previous binding;
   - scope leak — a parent catalog duplicates/overrides guidance owned by a nearer boundary;
   - semantic decision — filesystem evidence alone is insufficient.
5. **Apply only unambiguous repairs authorized by the request.** Preserve structure, style, native semantics, human authority, and method boundaries.
6. **Do not infer semantic state from timestamps or folder existence alone.** Presence proves existence, not completion, authority, freshness, or correctness unless the governing contract defines that inference.
7. **Update history only when the active workspace defines a history mechanism and synchronization is supposed to mutate it.**
8. **Report** changed entries, unresolved semantic decisions, and optional hardening separately.

## CCA Hybrid Workspace Profile

Load `../architect/hybrid-workspace.md` when the target matches the bundled **v3** profile or the supported **v2** profile.

After an authorized edit to `WORKSPACE.yaml`, reconcile derived artifacts with the installed skill's bundled implementation:

```bash
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace>
```

Report-only drift check:

```bash
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --check
```

Rules:

- the command MUST receive an explicit target;
- never invoke generation against `skills/cca/` or `assets/hybrid-workspace/` itself;
- `binding_change` remains non-breaking, so all generated consumers MUST follow the new binding;
- `context.router` MUST be generated at its current binding, not hardcoded as `CONTEXT.md`; under v3 every other generated artifact MUST be generated at its declared `generation_contract.outputs` destination, never at an assumed root filename;
- if `_state/`, `_runtime/`, `20-sources/`, or any other default binding is moved, obsolete defaults MUST NOT remain in regenerated routing/spec/path artifacts;
- `reference.curated` and `reference.collected` bindings move as children of the current `knowledge.reference` binding; their semantic role remains `knowledge.reference`;
- a binding move MUST NOT change provenance, curation state, effective child policy, or review state;
- `sync` never moves a reviewed collected source into curated; promotion is an explicit human-authorized operation;
- `sync` does not silently change frozen semantic keys/policies/authorities to make a binding move easier.

## Production rules

- Disk is authoritative for path existence; applicable contracts/instructions are authoritative for meaning.
- Resolve `boundary + semantic role -> binding` before path assumptions.
- Resolve mutation policy from the most-specific matching binding when bindings nest; parent permissions do not override child policy.
- Never move, rename, merge, or delete user/application content in sync mode.
- Never fabricate summaries, dates, counts, completion state, or provenance.
- Preserve upstream-native requirements, including ICM one-way references/selective routing where applicable.
- Preserve nested `AGENTS.md` scope.
- Preserve a native LLM Wiki's own index/schema conventions.
- Preserve declared human-method boundaries rather than flattening them into CCA catalogs.
- Skill-local tooling may be executed from any working directory; its target must remain explicit.

## Verification

After edits:

1. all modified path references resolve;
2. no routing entry was added outside its declared scope;
3. no parent/child authority duplication was introduced;
4. no upstream-native rule or method boundary was replaced with a CCA preference;
5. for the Hybrid Workspace Profile, `generate.py --target <workspace> --check` passes and no obsolete binding leaks remain;
6. reference classification still resolves both curated and collected evidence to `knowledge.reference`, with collected provenance/integrity intact.
