# Scaffold mode

Add context structure in place. Do not reorganize the project unless the user explicitly asks for restructuring.

## First: detect what already exists

Survey only enough of the target to understand its current routing and organization:

- root and nested `AGENTS.md` files;
- native harness instruction files such as `CLAUDE.md`;
- applicable native/upstream boundaries;
- declared CCA semantic-role/binding maps when present;
- root/stage contract files required by the active upstream/profile;
- existing wiki/schema instructions;
- obvious method overlays such as PARA or Zettelkasten;
- top-level application, documentation, test, and configuration directories.

Preserve native profiles and method boundaries. An upstream-native ICM workspace is not a blank project, an existing LLM Wiki must be interpreted through its own schema before CCA hardening is added, and an outer organizational method is not permission to rewrite a nested native workspace.

If the request is about choosing among methods/forms, adopting the CCA Hybrid Workspace Profile, or restructuring boundaries, use `architect` first. Scaffold implements an already-selected shape.

## Quick mode — default

Use when the repository layout already works.

1. Build a compact map of existing boundaries, directories, and instruction scopes.
2. Add or improve portable guidance only when useful; preserve harness/upstream-specific authority.
3. Preserve nested instruction scope. Do not flatten subtree-specific rules into the root.
4. Add a small workspace router only when intent-to-context routing materially reduces exploration.
5. When adding local contracts, use the filename/path required by the applicable upstream/profile or declared semantic binding; do not guess from a CCA default.
6. Externalize stable conventions only when they already exist and would otherwise be duplicated.
7. Preserve recognizable method organization and existing application structure.
8. Report every file created or changed and why it was necessary.

## Full mode

Use only when the target actually needs a new capability and the desired architecture is already clear.

### Native or ICM-derived pipeline

If the boundary is upstream-native ICM, preserve current upstream ICM exactly and validate the complete applicable acceptance surface. If the target merely borrows stages, contracts, selective routing, one-way references, or output handoffs, describe that usage as ICM-derived rather than upstream-native.

Do not label a partial scaffold as native ICM.

### Maintained knowledge

Discover the target's existing knowledge schema first. If none exists, create only the knowledge capabilities the user needs. Raw/reference, notes, wiki, index, log, provenance, supersession, and integrity mechanisms are optional CCA hardening unless a named profile makes them contractual.

### Method-organized workspace

Preserve declared PARA/Zettelkasten/BASB or other organization. Scaffold routing around those boundaries rather than normalizing them into one CCA tree.

## CCA Hybrid Workspace Profile

Use this path only after `architect` selected the optional profile or the target already matches the bundled **v3** contract (or the supported v2 contract). `--init` seeds the v3 template. Load `../architect/hybrid-workspace.md` before acting.

The implementation lives inside the installed skill at `../../assets/hybrid-workspace/` relative to this reference's skill package. Resolve the actual installed skill root; do not depend on a repository-global path.

### New target

Initialize the approved profile on an explicit target:

```bash
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --init
```

Rules:

1. `<workspace>` is the durable target workspace, never the installed skill/package directory.
2. `--init` seeds only missing `WORKSPACE.yaml` and `AGENTS.md`; it does not overwrite existing human-authored control files.
3. Review/customize semantic bindings in the target contract rather than renaming generated defaults ad hoc.
4. Run generation again after authorized binding edits so derived artifacts follow the new bindings.
5. Do not copy the Python implementation into the target merely to execute it.
6. Required reference materialization creates the parent `knowledge.reference` binding plus its `reference.curated` and `reference.collected` child bindings. Do not create loose source objects at the parent.

### Source curation

Scaffold does not reinterpret curation state as content authorship, acquisition actor, or a new knowledge role.

- Preserved raw/reference material goes through `reference.collected`, whoever acquired it; any actor may add new child objects only under the append/additive policy.
- Explicitly human-curated, maintained reference goes through `reference.curated` and remains agent-read-only.
- Existing collected sources are not edited, replaced, renamed, relocated, or deleted by normal agent operation.
- Source objects require the provenance/content-identity metadata declared by `reference_contract`.
- Review does not move collected evidence to curated; only an explicit human-authorized promotion does.
- Agent-authored synthesis routes to `knowledge.durable`; deliverables route to `output.artifact`; finite research work routes to `work.project`.

### Existing profile target

Do not use `--init` as a reset mechanism. Read the target's existing `WORKSPACE.yaml`, preserve human-authored `AGENTS.md`, and use `sync`/`lint` for reconciliation or validation.

A v1 or v2 target is not silently rewritten as though its frozen schema had always contained the new keys or meanings. The current bundled profile is v3 because the profile's own evolution contract requires a schema-version bump for key additions and meaning/policy changes. Treat an upgrade as an explicit, human-authorized profile-version migration.

## Change safety

Before writing:

1. Resolve the target boundary explicitly.
2. Read a target file before replacing it.
3. Preserve unrelated content, native semantics, and method boundaries.
4. For changes that replace, merge, move, or substantially rewrite existing instructions/content, present the migration/diff and obtain approval unless direct remediation was already authorized.
5. Never delete or rename application content merely to satisfy scaffold defaults.
6. Never materialize profile output inside `skills/cca/` or its bundled tool directory.
7. For nested bindings, resolve filesystem mutation policy from the most-specific applicable binding; parent permissions do not widen child policy.

## Production rules

- Every routing entry must resolve to something real or something created in the same operation.
- Resolve `boundary + semantic role -> binding` before using a CCA path assumption.
- One fact, one canonical home; pointers are cheaper than duplicated rules.
- Route before broad search and keep routing compact.
- Infer ordinary filesystem semantics when safe; do not create manifests merely to restate paths.
- Do not claim a universal precedence between `AGENTS.md` and harness-specific instruction files.
- Do not claim CCA conformance unless the boundary intentionally adopted the applicable CCA contract.
- Do not claim upstream-native ICM for a repository that only borrows ICM patterns.
- Do not invent PARA, Zettelkasten, or BASB native compatibility claims.

## Verification

After scaffolding, simulate a fresh human/agent consumer:

1. Can it identify the target boundary and applicable authority?
2. Can it resolve the relevant semantic role/binding without broad filesystem exploration?
3. If a pipeline was added, can it follow the applicable local contract?
4. If maintained knowledge was added, can it find the implementation's own navigation/schema instructions?
5. If upstream-native compatibility is claimed, did that upstream's complete applicable acceptance surface pass?
6. If the Hybrid Workspace Profile is claimed, do the bundled profile audit and generated-artifact check pass on the explicit target, including reference admission/provenance rules?

Use `lint` mode for profile-aware validation. Report upstream-native validity, CCA compatibility/conformance, named-profile conformance, and optional hardening separately.
