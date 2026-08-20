# CCA Hybrid Workspace Profile

This reference defines the optional **CCA Hybrid Workspace Profile**. It is a CCA-owned profile for personal or team workspaces that combine durable knowledge, preserved source material, projects, operational state, reusable capabilities, and human/agent workflows in one filesystem-native environment.

It is **not** a new CCA mode and it is **not** a universal CCA tree. Use it only when `architect` selects this profile or an existing workspace declares the profile contract.

## Current profile version

The bundled reference schema is **v2**. V2 preserves the complete frozen-v1 semantic-role, policy, authority, vocabulary, generation, and invariant baseline and adds one narrowly scoped extension: two admission classifications beneath `knowledge.reference`.

The version bump is required by the v1 evolution contract itself: adding semantic/classification keys is a `schema-version-bump`. The patch therefore does not pretend to remain schema v1 or silently mutate its frozen key set.

V2 adds:

- `reference.curated` — human-admitted source provenance;
- `reference.collected` — automatically acquired source provenance.

Neither is a new knowledge role. Both compose with `semantic.role = knowledge.reference`.

## Relationship to CCA and upstreams

CCA core remains path-agnostic. The profile implements CCA semantics through:

```text
boundary + semantic role -> binding
```

The semantic role identifies what material is. The binding is the concrete workspace-local representation and may move where the profile evolution contract permits it. Classification may add orthogonal meaning such as boundary class or source-admission provenance without replacing the semantic role.

Tools MUST resolve declared keys/bindings and MUST NOT infer identity from default names such as `_state/`, `_runtime/`, `00-wiki/`, `20-sources/`, or `CONTEXT.md`.

The profile uses proven ICM navigation principles where they fit, but it does not redefine ICM and does not make the profile native ICM. A nested native ICM boundary remains governed by current upstream ICM. LLM Wiki, PARA, Zettelkasten, BASB/CODE, AGENTS.md, Agent Skills, and other upstream methods or standards retain their own authority; profile crosswalks are mappings/influences, not semantic equivalence.

## Reference admission classification

The source corpus is physically separated by **admission provenance**, not by semantic role:

```text
20-sources/
├── curated/
└── collected/
```

Conceptually:

```text
20-sources/curated/paper.pdf
  classification = reference.curated
  semantic.role  = knowledge.reference

20-sources/collected/paper.pdf
  classification = reference.collected
  semantic.role  = knowledge.reference
```

The invariant is:

```text
source provenance/admission
!= content authorship
!= semantic role
```

`knowledge.reference` defines **WHAT** the material is: preserved source/evidence.

`reference.curated` vs `reference.collected` defines **HOW** that source entered the workspace.

`knowledge.durable` defines what the workspace **LEARNED** from evidence.

`output.artifact` defines what the workspace deliberately **PRODUCED** for external consumption.

Research is an activity/workflow, not a new top-level knowledge role. A finite research effort is a `work.project`; it may traverse `context.capture` → `knowledge.reference` → `knowledge.durable` → `output.artifact` while tasks/state represent execution.

### `reference.curated`

- Human-admitted raw/reference evidence.
- Human-authoritative.
- Agents may read but not admit, edit, replace, rename, relocate, or delete source objects.
- Existing evidence is immutable.
- “Curated” means human-admitted provenance, not “high quality,” “verified,” or “true.”

### `reference.collected`

- Raw/reference evidence automatically acquired by an agent, crawler, API, integration, workflow, or equivalent tool.
- Uses the existing `append` mutability semantics: agents may add new child objects; already-present source objects are frozen.
- Agent deposit is not generic authority to edit, replace, rename, relocate, or delete existing evidence.
- A collected source remains collected after human review because the classification records how it originally entered the corpus. Review/approval is metadata, not filesystem promotion.
- Presence means preserved evidence, not truth or endorsement. Collected evidence may be unreviewed.

The parent `knowledge.reference` binding may not contain loose source objects. Raw/reference objects must resolve through one of the two child classifications. Most-specific binding policy wins for filesystem operations, so the human/read-only parent cannot erase the append-only deposit capability of `reference.collected`, and a broader writable ancestor can never widen `reference.curated`.

### Collected provenance

Automatically collected source objects MUST preserve acquisition provenance. The bundled v2 contract requires at least:

- acquisition actor (`acquired_by`);
- acquisition method (`acquisition_method`);
- original source/origin (`origin`);
- acquisition timestamp with timezone (`acquired_at`);
- content identity, with SHA-256 `content_hash` required for ordinary file objects.

The reference implementation represents file provenance beside the source as `<source>.source.yaml`; collected directory objects use `.source.yaml` inside the directory. Another conforming implementation may expose equivalent durable metadata only if it preserves the same semantic guarantees and remains independently auditable.

Changing collected content without updating its identity is detected as integrity failure. Updating metadata to conceal a source mutation is itself outside normal agent authority; provenance is evidence, not disposable bookkeeping.

Raw/reference evidence survives distillation and is never rewritten into cleaner prose. Agent-authored synthesis belongs in `knowledge.durable`; deliverables belong in `output.artifact`.

## Portable reference implementation

The reference implementation is bundled with the installed skill under:

```text
assets/hybrid-workspace/
├── WORKSPACE.yaml
├── AGENTS.md
├── schema.py
├── generate.py
├── audit.py
├── requirements.txt
└── tests/
    ├── test_freeze.py
    ├── test_targeting.py
    ├── test_adversarial_targeting.py
    └── test_reference_admission.py
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

## Frozen baseline and v2 extension contract

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

V2 adds only the admission-provenance classification contract described above. It deliberately reuses existing `immutable`, `append`, `human`, `shared`, `read-only`, and `write` vocabulary values; no new policy axis or generic write primitive was invented.

Do not change a frozen semantic key, policy meaning, authority meaning, axis, or vocabulary value as a binding customization. Such changes require the profile's declared schema-version treatment.

### Crosswalks are advisory relationships

The `crosswalk` material records provenance/influence for humans and tools. It is **not** a second semantic-key namespace and MUST NOT be interpreted as one-to-one equivalence.

PARA `Resources`, for example, is broader than `knowledge.reference`. A Resource may contain preserved evidence, a human-authored note, maintained synthesis, a dataset, or a nested workspace. The new `reference.*` classifications do not alter that mapping; they classify admission provenance inside the preserved-evidence role.

Consumers MUST use the target's actual boundary/role/authority semantics rather than infer epistemic type solely from a crosswalk label.

## Bootstrap and independent implementation contract

A consumer that knows the profile but does not have the CCA skill installed MUST be able to start from durable target files.

For current v2:

1. `WORKSPACE.yaml` at the target root is the machine-readable profile bootstrap and semantic binding/policy contract.
2. `AGENTS.md` is the human/agent control surface and identifies `workspace-contract:v2`.
3. Semantic resolution starts from the applicable boundary and declared slots; `slots[*].binding` gives the concrete target-local implementation.
4. `classification_roles` declares when a classification composes with another semantic role instead of replacing it.
5. `reference_contract` declares the admission/provenance, routing, integrity, and no-loose-parent-source rules.
6. The value of a default binding is never the semantic identity. `context.router` remains the semantic generated-router role even when the binding is `CONTEXT.md`, `ROUTER.md`, or another valid profile binding.
7. An implementation MUST validate binding text and symlink-resolved containment before reading/writing generated/profile-controlled destinations.
8. For nested bindings, filesystem policy resolves from the most-specific matching binding; semantic composition remains separately visible.
9. Derived artifacts are rebuildable views/adapters. They MUST NOT become competing authority over `WORKSPACE.yaml`, human-authored control files, source evidence, or canonical workspace content.

### Generated artifact semantics

The profile distinguishes semantic outputs from reference-implementation filenames:

- **`context.router`** — semantic output role. It MUST be generated/validated at the slot's current binding. The generation contract still carries the historical/default literal `CONTEXT.md` for compatibility with the bundled implementation; **consumers MUST interpret that entry as the `context.router` role**, **not as a fixed filename requirement**.
- **`SPEC.md`** — derived human-readable rendering of the target profile contract; non-authoritative.
- **`paths.sh`** — derived shell binding adapter used by the reference implementation; non-authoritative.
- **`mkdirs.sh`** — derived reference helper for materializing declared directories/files; non-authoritative.
- **`obsidian-excludes.txt`** — derived editor/indexing adapter; non-authoritative.

An alternative implementation does not need byte-for-byte Python output to implement CCA core. To claim current Hybrid Workspace **profile conformance**, however, it must preserve the semantic content and safety guarantees promised by each profile-required derived artifact. The bundled `generate.py --check` performs byte-for-byte drift checking only for artifacts generated by this reference implementation; that check is a **reference-implementation regression mechanism**, not a language monopoly.

This distinction lets a Rust/Go/other implementation reproduce the profile from this contract and `WORKSPACE.yaml` without reverse-engineering Python control flow.

## Detection

Treat a workspace as the current profile when its local `WORKSPACE.yaml` matches the bundled v2 baseline/extension contract and the required human-authored control surface identifies `workspace-contract:v2`. Do not classify arbitrary YAML manifests as this profile.

A profile workspace is:

- **CCA-compatible** by construction;
- **CCA-conformant** when it satisfies the applicable CCA core contract;
- **profile-conformant** when the current profile audit and required semantic/generated-artifact checks pass;
- **upstream-native** only for a nested or overlapping upstream boundary that independently passes that upstream's own acceptance rules.

## Mode routing

- `architect` selects/composes the profile and chooses bindings/authority boundaries.
- `scaffold` initializes the approved profile on an explicit target with `generate.py --target <workspace> --init`.
- `sync` reconciles derived artifacts after authorized schema/binding changes with `generate.py --target <workspace>`; `--check` is report-only.
- `lint` runs `audit.py --target <workspace>` and `generate.py --target <workspace> --check` and validates reference admission/provenance where applicable.
- `ingest` resolves source admission: unknown incoming material starts at `context.capture`; human admission goes to `reference.curated`; automated preserved evidence may be deposited into `reference.collected` with required provenance.
- `query` resolves both reference classifications as `knowledge.reference` and treats their admission/review metadata separately from epistemic truth.
- `advise` may recommend a different profile or upstream method when it better serves the user's intent.

## Routing and scale

The root `context.router` is an orientation surface, not a universe-wide document manifest.

As collections grow, boundaries under `knowledge.durable`, `knowledge.reference`, projects, or other large roles MAY introduce local routers/catalogs/indexes. These local surfaces should enumerate or summarize only their own scope. The root router should route to the relevant boundary/role and let local navigation continue from there.

Derived local indexes, embeddings, search databases, or graph projections remain rebuildable accelerators unless another declared authority explicitly owns that data. The profile therefore scales by recursive/federated routing rather than by growing one root manifest indefinitely.

## Acceptance

Before describing a target as profile-conformant:

1. the frozen-v1 baseline plus current v2 extension audit passes;
2. the adversarial mutation/self-test passes when release-grade verification is requested;
3. `reference.curated` and `reference.collected` both resolve to `knowledge.reference` while retaining distinct admission policies;
4. no loose source object exists directly under the parent `knowledge.reference` binding;
5. collected source objects satisfy required provenance/content-identity checks;
6. existing collected and curated evidence remains immutable to normal agent operation;
7. required generated semantic outputs are present and consistent with the target contract;
8. reference-implementation artifacts pass canonical-render drift checks when the bundled Python implementation produced/owns them;
9. `AGENTS.md` satisfies the v2 profile control contract;
10. changing a non-breaking binding causes every generated consumer to follow the new binding;
11. changing `context.router` changes the generated router path without requiring a fixed `CONTEXT.md` identity;
12. no generated artifact leaks obsolete `_state/`, `_runtime/`, `20-sources/`, or other default paths after those bindings move;
13. all generated destinations remain beneath the explicit target after symlink resolution;
14. generation/audit operate on the explicit target and leave the installed skill package untouched;
15. applicable upstream-native boundaries still pass their own upstream acceptance surface;
16. a fresh human or agent can orient from durable files without relying on prior chat state.
