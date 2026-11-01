# CCA Hybrid Workspace Profile

This reference defines the optional **CCA Hybrid Workspace Profile**. It is a CCA-owned profile for personal or team workspaces that combine durable knowledge, preserved source material, projects, operational state, reusable capabilities, and human/agent workflows in one filesystem-native environment.

It is **not** a new CCA mode and it is **not** a universal CCA tree. Use it only when `architect` selects this profile or an existing workspace declares the profile contract.

## Current profile version

The bundled reference schema is **v3** (CCA 1.3.0). Schema **v2** remains supported unchanged: a target declaring `schema_version: 2` is audited and generated under exactly the v2 rules documented in [Schema v2 (supported)](#schema-v2-supported), and its generated output is byte-for-byte what the v2 implementation produced. A target opts into v3 by declaring `schema_version: 3`; nothing upgrades a v2 target silently.

V3 is a schema-version bump under the profile's own evolution contract because it:

- adds keys and vocabulary — `state.hotset`, `system.operations`, `system.documentation`, `asset.library`, `asset.templates`, and the `asset` category (`key_add_remove_or_rename`, `axis_or_vocab_change`);
- changes the meaning of `reference.curated` / `reference.collected` from *acquisition actor* to *curation state* (`key_meaning_change`);
- changes generation, provenance, and archive policy semantics (`policy_semantics_change`).

V3 preserves the complete frozen-v1 slot/policy/authority baseline and the v2 classification keys with their slot policies. It adds:

- **relocatable generated outputs** — no generated artifact has a fixed root filename; `WORKSPACE.yaml` is the only fixed bootstrap path;
- **workspace identity** — an optional machine-readable `identity` block in `WORKSPACE.yaml`;
- **actor-independent curation** — collected vs curated records explicit curation state, orthogonal to who or what acquired the bytes;
- **representation-aware provenance** — Markdown frontmatter, file sidecars, directory/corpus manifests, with organizational containers no longer mistaken for acquisition batches;
- **the state hotset**, **operating documentation**, and **human/editor asset** bindings;
- **scoped archive manifests** — required for formal semantic retirement, never for ordinary cold storage.

## Relationship to CCA and upstreams

CCA core remains path-agnostic. The profile implements CCA semantics through:

```text
boundary + semantic role -> binding
```

The semantic role identifies what material is. The binding is the concrete workspace-local representation and may move where the profile evolution contract permits it. Classification may add orthogonal meaning such as boundary class or source curation state without replacing the semantic role.

Tools MUST resolve declared keys/bindings and MUST NOT infer identity from default names such as `_state/`, `_runtime/`, `00-wiki/`, `20-sources/`, or `CONTEXT.md`.

The profile uses proven ICM navigation principles where they fit, but it does not redefine ICM and does not make the profile native ICM. A nested native ICM boundary remains governed by current upstream ICM. LLM Wiki, PARA, Zettelkasten, BASB/CODE, AGENTS.md, Agent Skills, and other upstream methods or standards retain their own authority; profile crosswalks are mappings/influences, not semantic equivalence.

## Reference curation classification (v3)

The source corpus is physically separated by **curation state**, not by semantic role and not by acquisition actor:

```text
20-sources/
├── curated/
└── collected/
```

Conceptually:

```text
20-sources/collected/clippings/article.md
  classification = reference.collected   (not explicitly curated)
  semantic.role  = knowledge.reference
  acquired_by    = human | agent | crawler | tool | integration | workflow

20-sources/curated/standard.pdf
  classification = reference.curated     (explicitly human-curated)
  semantic.role  = knowledge.reference
```

The invariants are:

```text
acquisition (who/how/when/origin/identity)
!= curation state (collected | curated)
!= content authorship
!= semantic role
```

`knowledge.reference` defines **WHAT** the material is: preserved source/evidence. `reference.curated` vs `reference.collected` defines whether it has been **explicitly curated**. `knowledge.durable` defines what the workspace **LEARNED** from evidence. `output.artifact` defines what the workspace deliberately **PRODUCED** for external consumption.

Research is an activity/workflow, not a new top-level knowledge role. A finite research effort is a `work.project`; it may traverse `context.capture` → `knowledge.reference` → `knowledge.durable` → `output.artifact` while tasks/state represent execution.

### `reference.collected`

- Preserved raw/reference material that has **not been explicitly promoted** to curated.
- Any actor may acquire it: a human clipping an article, saving a transcript, bookmark, or PDF; an agent, crawler, tool, integration, or workflow.
- Collected is a legitimate permanent home. It is not a queue and nothing implies that collected material is expected to become curated.
- Append/add-child: new provenance-bearing objects may be deposited; existing objects are frozen. The only sanctioned exit is human-authorized promotion (`privileged_operations.reference.collected.promotion: human-authorized`).
- Presence means preserved evidence, not truth or endorsement. Collected evidence may be unreviewed.

### `reference.curated`

- Deliberately human-admitted, **maintained** reference.
- Entered only by an explicit, human-authorized act: **promotion** of an existing collected object or **direct deliberate human admission**.
- Review alone never promotes. Agents may recommend curation; the human performs it.
- Promotion preserves the source bytes and their provenance and adds a curation record (`curated_by`, `curated_at`).
- Human-authoritative and agent-read-only. “Curated” means maintained, not “high quality,” “verified,” or “true.”

The parent `knowledge.reference` binding may not contain loose source objects. Most-specific binding policy wins for filesystem operations, so the human/read-only parent cannot erase the add-child capability of `reference.collected`, and a broader writable ancestor can never widen `reference.curated`.

### Provenance (v3)

Every object under either class MUST be able to answer: original source (`origin`), acquisition actor (`acquired_by`), acquisition method (`acquisition_method`), acquisition timestamp with timezone (`acquired_at`), and a **verifiable content identity**.

`acquired_at` is never invented. When the original acquisition time is unknown, record the time the object entered this workspace's custody with `acquired_at_basis: import` and `original_acquisition_time: unknown`.

The contract supports one representation per object type:

| object | representation | content identity |
|---|---|---|
| Markdown capture (`.md`) | the note's own frontmatter: a `provenance:` mapping, or the same canonical fields at the top level for capture tools that cannot write nested YAML | `content_hash: sha256:<hex>` of the **body** — every byte after the closing frontmatter line, exactly as stored — with `content_hash_scope: body` |
| any other file | `<file>.source.yaml` sidecar | `content_hash: sha256:<hex>` of the file bytes |
| acquisition batch, imported directory, or automated corpus | directory `.source.yaml` | either `content_identity: sha256-tree:<hex>` (one tree identity) or a `files:` mapping of relative path → `sha256:<hex>` (per-file identity, typical for generated corpus manifests) |

The body-scoped hash exists because a Markdown file cannot contain a hash of itself. Frontmatter (tags, review notes, provenance) may be extended without changing the evidence identity, and is therefore **not** protected by the hash; any change to the body is detected. The body is hashed byte-for-byte, so newline conversion (for example Git `core.autocrlf`) changes identity — keep reference captures out of newline normalisation (for example a `-text` Git attribute). `field_aliases` lets a capture tool's existing metadata satisfy a canonical field without duplication; a workspace whose clipper already records the page URL as `source` can declare `field_aliases: {origin: source}`. The bundled template declares no aliases.

`original_acquisition_time` records the original acquisition with honest precision: a timestamp with timezone, a calendar date, or `unknown`. `acquired_at` is always a full timestamp; a bare date is rejected rather than silently promoted to midnight.

`sha256-tree` is reproducible with coreutils from inside the directory:

```bash
find . -type f ! -path ./.source.yaml -printf '%P\0' | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum
```

**Containers are not batches** (`unmanifested_directories: container`). A directory that has no `.source.yaml` is an organizational container (for example `collected/clippings/`, `collected/transcripts/`, `collected/corpora/`) at any depth; each descendant object carries its own provenance. A directory with a manifest is one acquisition object and its contents are covered by that manifest. `.gitkeep` and common OS noise files (`.DS_Store`, `Thumbs.db`, `desktop.ini`) are ignored; symlinked source objects, orphan sidecars, and a `.source.yaml` that is not a regular file are rejected.

Identity is established at admission and is immutable afterwards. The bundled `provenance.py stamp <paths…>` helper is a **deposit-time** tool: given explicit paths under `reference.collected` that are being admitted now, it adds the body-scoped `content_hash` to Markdown captures that already carry the other provenance fields. It never runs over a whole class by default, refuses anything outside `reference.collected` (curated sources are never stamped), refuses a collected binding that escapes the workspace, never replaces an existing hash (that would launder a mutation), never invents other fields, verifies its insertion by re-parsing, and restores the original bytes on any failure. It is not a retrofit tool: material that already sat in a class without identity must be re-admitted deliberately, with its content checked against an independent source before identity is recorded.

Raw/reference evidence survives distillation and is never rewritten into cleaner prose. Agent-authored synthesis belongs in `knowledge.durable`; deliverables belong in `output.artifact`.

## Generated outputs, identity, state, assets, and archive (v3)

### Generated outputs are bindings

`generation_contract.outputs` declares every generated artifact and resolves its destination through a slot:

```yaml
generation_contract:
  outputs:
    context.router: {slot: context.router}
    spec: {slot: system.documentation, file: SPEC.md}
    paths: {slot: system.operations, file: paths.sh}
    mkdirs: {slot: system.operations, file: mkdirs.sh}
    host_index_adapter: {slot: system.operations, file: obsidian-excludes.txt}
  human_authored: [workspace.schema, agent.instructions]
  index_policy:
    spec: disabled
```

- `file` is one safe filename segment inside an agent-writable `derived` or `shared` `system`/`control` directory binding that is not nested inside a content binding; the destination's most-specific binding must be that declared slot; destinations may not collide (case-insensitively) with each other or with any declared binding; nothing defaults to the target root.
- Generated helpers never assume their own directory is the root. Each helper canonicalises its own path (following symlinks), walks back from its declared destination to the candidate root, and accepts it only if `WORKSPACE.yaml` is there **and** the declared destination under that root is the helper itself. A helper reached through a symlink therefore resolves its own workspace; a copied or misplaced helper fails closed (a failed `source` leaves `WS_ROOT` unset).
- Destinations are validated as text and after symlink resolution before any write, and the generator refuses to overwrite an existing file that is not a generated artifact.
- Relocating `system.operations` or `system.documentation` leaves the previous outputs in place; remove them deliberately (`--check` validates declared destinations, not orphans).
- The binding that contains a generated file never grants hand-edit authority over it (`invariants.generation`).
- `workspace.schema` MUST stay bound to `WORKSPACE.yaml`: it is the only fixed bootstrap path. `agent.instructions` is resolved through its binding.

### Workspace identity

An optional top-level block makes the workspace's system identity machine-readable:

```yaml
identity:
  endpoint: "brain://example"   # stable URI, never a filesystem path
  owner: human                  # human | agent | shared
```

Generated routers/specifications render it from this block. It is system identity, not durable knowledge, and must not be duplicated into a knowledge note.

### Operational state hotset

`state.hotset` binds the general operational-state tree (default `_state/`): quick actions, dashboards, canvases, active bookmarks, reminders, current working references — useful **now**, not durable knowledge. It is indexed `included` because the human needs it in search and quick switching; more-specific state bindings nested inside it (`state.current`, `state.tasks`) keep their own policy and indexing. Agents may add and edit hotset material; removal is a human decision.

### Operating documentation and system operations

- `system.documentation` (default `_runtime/docs/`) holds repository-operating documentation: how-to guides, the operating model, verification records, and the generated specification. It explains the workspace; it is not durable knowledge.
- `system.operations` (default `_runtime/operations/`) holds generated operational helpers; derived and regenerate-only.

### Human/editor assets

`asset.library` (default `_assets/`) holds human/editor-facing attachments, recordings, images, and media embedded in or used by human notes. `asset.templates` (default `_assets/templates/`) holds templates used by the human and their editor/plugins. They are distinct from `system.assets` and `system.templates`, which serve agents and system tooling. Agents read human assets and mutate them only where explicitly authorized. Template sources are never evaluated in place.

### Archive: cold storage vs semantic retirement

`lifecycle.archive` accepts ordinary human **cold storage** without ceremony: no manifest is required and none should be manufactured. **Formal semantic retirement** — an authorized operation that retires an existing canonical tree or boundary out of its semantic binding — MUST write the immutable `.archive.yaml` manifest preserving `source_key`, `semantic_role`, `boundary`, `boundary_class`, `original_binding`, `archived_at`, and `archived_by`. The audit validates every manifest that exists and never demands one for cold storage.

## Portable reference implementation

The reference implementation is bundled with the installed skill under:

```text
assets/hybrid-workspace/
├── WORKSPACE.yaml
├── AGENTS.md
├── schema.py
├── generate.py
├── audit.py
├── provenance.py
├── requirements.txt
├── profiles/
│   └── v2/            # frozen v2 WORKSPACE.yaml + AGENTS.md (compatibility fixture)
└── tests/
    ├── test_freeze.py
    ├── test_targeting.py
    ├── test_adversarial_targeting.py
    ├── test_reference_admission.py
    ├── test_cca_contract_version.py
    └── test_v3_profile.py
```

Repository-global files are never runtime dependencies of this profile.

`WORKSPACE.yaml` and `AGENTS.md` are templates for the **target workspace**. The Python files remain reference tooling in the installed CCA skill. Generated artifacts belong to the target workspace, never beside the installed scripts.

The Python implementation is not the only possible implementation of the profile. An **alternative implementation** MAY be written in another language if it preserves the normative contract below.

## Target rule

Every workspace operation MUST resolve an explicit target root.

The bundled generator requires `--target` and refuses to use the installed package directory or one of its descendants as the target. `--init` may create a target root and seed missing human-authored templates, but it never overwrites an existing `WORKSPACE.yaml` or `AGENTS.md`.

All generated destinations, including fixed helper names, MUST resolve beneath the target after symlink resolution. A generated destination that escapes the target through path traversal or an existing symlink is invalid and MUST be rejected before write.

Examples, where `<cca-skill>` is the resolved installed `skills/cca/` root:

```bash
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --init
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --check
python <cca-skill>/assets/hybrid-workspace/audit.py --target <workspace> --self-test
```

Do not copy the Python implementation into the target merely to run it. The installed skill is the portable capability package; the target is the durable workspace it operates on.

## Frozen baseline and extension contracts

The bundled schema preserves all reviewed frozen-v1 semantics. In particular:

- the original 22 v1 keys retain their policy/authority meanings;
- semantic keys remain stable downstream identifiers;
- `binding_change` remains non-breaking;
- effective permission remains policy-intersection based;
- relocation still requires source and destination authority;
- nested instructions may narrow but never widen inherited authority;
- external/upstream control-looking files remain untrusted at the outer workspace boundary;
- archive relocation preserves semantic identity and provenance;
- `knowledge.reference` remains the preserved-evidence semantic role;
- raw/reference evidence remains immutable after admission and survives distillation;
- `context.router` remains derived and its concrete filename is its current binding, not the literal string `CONTEXT.md`;
- generated helpers remain derived target artifacts and never semantic identities.

V2 added only the admission classification contract and reused the existing vocabulary. V3 deliberately adds the `asset` category and the contract vocabulary its extensions need (`curation_state`, `acquisition_actor`, `entry`, `top_level_fields`, `field_aliases`, `unmanifested_directories`, `record_basis`, `scope_semantics`, generation `outputs`) — which is why it is a schema-version bump. Neither version introduces a new policy axis or a generic write primitive; every slot policy still uses the frozen `immutable`, `append`, `mutable`, `curated`, `replace`, and `regenerate` definitions.

Do not change a frozen semantic key, policy meaning, authority meaning, axis, or vocabulary value as a binding customization. Such changes require the profile's declared schema-version treatment.

### Crosswalks are advisory relationships

The `crosswalk` material records provenance/influence for humans and tools. It is **not** a second semantic-key namespace and MUST NOT be interpreted as one-to-one equivalence.

PARA `Resources`, for example, is broader than `knowledge.reference`. A Resource may contain preserved evidence, a human-authored note, maintained synthesis, a dataset, or a nested workspace. The `reference.*` classifications do not alter that mapping; they classify curation state (v2: admission) inside the preserved-evidence role.

Consumers MUST use the target's actual boundary/role/authority semantics rather than infer epistemic type solely from a crosswalk label.

## Bootstrap and independent implementation contract

A consumer that knows the profile but does not have the CCA skill installed MUST be able to start from durable target files.

For current v3:

1. `WORKSPACE.yaml` at the target root is the machine-readable profile bootstrap and semantic binding/policy contract. It is the only path a consumer may assume without resolving it.
2. The `agent.instructions` binding (default `AGENTS.md`) is the human/agent control surface and identifies `workspace-contract:v3` (`workspace-contract:v2` for v2 targets).
3. Semantic resolution starts from the applicable boundary and declared slots; `slots[*].binding` gives the concrete target-local implementation.
4. `classification_roles` declares when a classification composes with another semantic role instead of replacing it.
5. `reference_contract` declares the curation/provenance, routing, integrity, and no-loose-parent-source rules.
6. `generation_contract.outputs` declares where every generated artifact lives; `identity`, when present, declares the workspace's system identity.
7. The value of a default binding is never the semantic identity. `context.router` remains the semantic generated-router role even when the binding is `CONTEXT.md`, `ROUTER.md`, or another valid profile binding.
8. An implementation MUST validate binding text and symlink-resolved containment before reading/writing generated/profile-controlled destinations.
9. For nested bindings, filesystem policy resolves from the most-specific matching binding; semantic composition remains separately visible.
10. Derived artifacts are rebuildable views/adapters. They MUST NOT become competing authority over `WORKSPACE.yaml`, human-authored control files, source evidence, or canonical workspace content.

### Generated artifact semantics

The profile distinguishes semantic outputs from reference-implementation filenames:

- **`context.router`** — semantic output role. It MUST be generated/validated at the slot's current binding. The v2 generation contract still carries the historical/default literal `CONTEXT.md` for compatibility with the bundled implementation; **consumers MUST interpret that entry as the `context.router` role**, **not as a fixed filename requirement**. V3 names the role directly (`outputs.context.router: {slot: context.router}`).
- **`spec`** (`SPEC.md`) — derived human-readable rendering of the target profile contract; non-authoritative.
- **`paths`** (`paths.sh`) — derived shell binding adapter used by the reference implementation; non-authoritative.
- **`mkdirs`** (`mkdirs.sh`) — derived reference helper for materializing declared directories/files; non-authoritative.
- **`host_index_adapter`** (`obsidian-excludes.txt`) — derived editor/indexing adapter; non-authoritative.

In v2 these helper filenames live at the target root and helpers infer the root from their own directory. In v3 each lives at its declared output destination and resolves the root independently.

An alternative implementation does not need byte-for-byte Python output to implement CCA core. To claim current Hybrid Workspace **profile conformance**, however, it must preserve the semantic content and safety guarantees promised by each profile-required derived artifact. The bundled `generate.py --check` performs byte-for-byte drift checking only for artifacts generated by this reference implementation; that check is a **reference-implementation regression mechanism**, not a language monopoly.

This distinction lets a Rust/Go/other implementation reproduce the profile from this contract and `WORKSPACE.yaml` without reverse-engineering Python control flow.

## Detection

Treat a workspace as this profile when its local `WORKSPACE.yaml` matches the bundled v3 contract (or the supported v2 contract) and the required human-authored control surface identifies the matching `workspace-contract:v3` / `workspace-contract:v2` marker. Do not classify arbitrary YAML manifests as this profile.

A profile workspace is:

- **CCA-compatible** by construction;
- **CCA-conformant** when it satisfies the applicable CCA core contract;
- **profile-conformant** when the current profile audit and required semantic/generated-artifact checks pass;
- **upstream-native** only for a nested or overlapping upstream boundary that independently passes that upstream's own acceptance rules.

## Mode routing

- `architect` selects/composes the profile and chooses bindings/authority boundaries.
- `scaffold` initializes the approved profile on an explicit target with `generate.py --target <workspace> --init`.
- `sync` reconciles derived artifacts after authorized schema/binding changes with `generate.py --target <workspace>`; `--check` is report-only.
- `lint` runs `audit.py --target <workspace>` and `generate.py --target <workspace> --check` and validates reference curation/provenance where applicable.
- `ingest` resolves source placement: unknown incoming material starts at `context.capture`; preserved raw/reference material — whoever acquired it — is deposited into `reference.collected` with required provenance (v3; `provenance.py stamp` completes Markdown identity at admission); explicit human-authorized curation goes to `reference.curated`. Under v2, the v2 rule applies: human admission goes to curated, automated acquisition to collected.
- `query` resolves both reference classifications as `knowledge.reference` and treats curation/review metadata separately from epistemic truth.
- `advise` may recommend a different profile or upstream method when it better serves the user's intent.

## Routing and scale

The root `context.router` is an orientation surface, not a universe-wide document manifest.

As collections grow, boundaries under `knowledge.durable`, `knowledge.reference`, projects, or other large roles MAY introduce local routers/catalogs/indexes. These local surfaces should enumerate or summarize only their own scope. The root router should route to the relevant boundary/role and let local navigation continue from there.

Derived local indexes, embeddings, search databases, or graph projections remain rebuildable accelerators unless another declared authority explicitly owns that data. The profile therefore scales by recursive/federated routing rather than by growing one root manifest indefinitely.

## Acceptance

Before describing a target as profile-conformant:

1. the frozen-v1 baseline plus the declared v2 or v3 extension audit passes;
2. the adversarial mutation/self-test passes when release-grade verification is requested;
3. `reference.curated` and `reference.collected` both resolve to `knowledge.reference` while retaining distinct curation policies;
4. no loose source object exists directly under the parent `knowledge.reference` binding;
5. source objects satisfy required provenance/content-identity checks (v3: every object in both classes, through containers at any depth; v2: first-level collected objects);
6. existing collected and curated evidence remains immutable to normal agent operation;
7. required generated semantic outputs are present and consistent with the target contract;
8. reference-implementation artifacts pass canonical-render drift checks when the bundled Python implementation produced/owns them;
9. the `agent.instructions` binding satisfies the declared profile control contract;
10. changing a non-breaking binding causes every generated consumer to follow the new binding;
11. changing `context.router` changes the generated router path without requiring a fixed `CONTEXT.md` identity;
12. no generated artifact leaks obsolete `_state/`, `_runtime/`, `20-sources/`, or other default paths after those bindings move;
13. all generated destinations remain beneath the explicit target after symlink resolution;
14. generation/audit operate on the explicit target and leave the installed skill package untouched;
15. applicable upstream-native boundaries still pass their own upstream acceptance surface;
16. a fresh human or agent can orient from durable files without relying on prior chat state;
17. (v3) no generated artifact is required at the target root; generated helpers resolve the actual workspace root from their declared destination;
18. (v3) every `.archive.yaml` present is a valid retirement record, and cold storage carries none.

## Schema v2 (supported)

A target declaring `schema_version: 2` keeps the v2 contract exactly:

- `reference.curated` — raw/reference evidence explicitly admitted by a human; agents read only.
- `reference.collected` — raw/reference evidence automatically acquired by an agent, crawler, API, integration, workflow, or equivalent tool; agents may deposit new children; a collected source remains collected after human review.
- Collected provenance uses `<source>.source.yaml` sidecars for first-level files and `.source.yaml` inside first-level directories, requiring `acquired_by`, `acquisition_method`, `origin`, `acquired_at`, and SHA-256 `content_hash` for files (`content_hash` or `content_identity` for directories).
- `generation_contract.derived` lists `paths.sh`, `mkdirs.sh`, `obsidian-excludes.txt`, `CONTEXT.md` (the `context.router` role), and `SPEC.md`; helpers are generated at the target root.
- Whole-tree retirement creates `.archive.yaml`.

The frozen v2 template is bundled at `assets/hybrid-workspace/profiles/v2/` and its regression tests remain part of the release suite. `generate.py --init` seeds the current v3 template; to start a new v2 target deliberately, copy the v2 template files from `profiles/v2/` instead.

### Migrating a v2 target to v3

Moving a v2 target to v3 is an explicit, human-authorized schema change. It never happens implicitly.

1. Snapshot the target (tracked and untracked content) outside the workspace.
2. Edit `WORKSPACE.yaml`: declare `schema_version: 3` and `cca.specification` ≥ `1.3.0`; adopt the v3 `generation_contract.outputs`, `reference_contract`, `archive_contract`, and `privileged_operations` blocks and the v3 slots; add `identity` if the workspace has an endpoint. Update the `agent.instructions` file to `workspace-contract:v3`.
3. Run `generate.py --target <workspace>`; delete the old root `paths.sh`, `mkdirs.sh`, `obsidian-excludes.txt`, and `SPEC.md` after the new outputs exist, and update every consumer that called them by their old path.
4. Bring reference objects under the v3 provenance contract. Existing v2 sidecars and directory manifests remain valid where their identity still verifies. Objects inside organizational containers need their own provenance. Never re-stamp or re-hash existing evidence to make the audit pass: if content no longer matches its recorded identity, investigate and re-admit it deliberately with an honest `acquired_at_basis`.
5. Give existing curated objects their curation record with `curated_at_basis: migration` (the time the record is written), never an invented original admission time.
6. Run `audit.py --target` and `generate.py --check`; review every finding before accepting the migration.
