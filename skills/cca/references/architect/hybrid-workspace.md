# CCA Hybrid Workspace Profile

This reference defines the optional **CCA Hybrid Workspace Profile**. It is a CCA-owned profile for personal or team workspaces that combine durable knowledge, raw/source material, projects, operational state, reusable capabilities, and human/agent workflows in one filesystem-native environment.

It is **not** a new CCA mode and it is **not** a universal CCA tree. Use it only when `architect` selects this profile or an existing workspace already declares the bundled frozen-v1 contract.

## Relationship to CCA and upstreams

CCA core remains path-agnostic. The profile implements CCA semantics through:

```text
boundary + semantic role -> binding
```

The semantic key identifies the role. The binding is the concrete workspace-local path and may move where the profile's evolution contract allows it. Tools MUST resolve the semantic key before using a path and MUST NOT infer identity from default names such as `_state/`, `_runtime/`, `00-wiki/`, or `CONTEXT.md`.

The profile uses proven ICM navigation principles where they fit, but it does not redefine ICM and does not make the profile native ICM. A nested native ICM boundary remains governed by current upstream ICM. LLM Wiki, PARA, Zettelkasten, BASB/CODE, AGENTS.md, Agent Skills, and other upstream methods or standards retain their own authority; profile crosswalks are mappings/influences, not semantic equivalence.

## Portable reference implementation

The reference implementation is bundled with this installed skill under:

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
    └── test_adversarial_targeting.py
```

Repository-global files are never runtime dependencies of this profile.

`WORKSPACE.yaml` and `AGENTS.md` are templates for the **target workspace**. The Python files remain reference tooling in the installed CCA skill. Generated artifacts belong to the target workspace, never beside the installed scripts.

The Python implementation is not the only possible implementation of the profile. An independent implementation MAY be written in another language if it preserves the normative contract below.

## Target rule

Every workspace operation MUST resolve an explicit target root.

The bundled generator intentionally requires `--target` and refuses to use the installed package directory or one of its descendants as the target. `--init` may create a target root and seed missing human-authored templates, but it never overwrites an existing `WORKSPACE.yaml` or `AGENTS.md`.

All generated destinations, including fixed helper names, MUST resolve beneath the target after symlink resolution. A generated destination that escapes the target through path traversal or an existing symlink is invalid and MUST be rejected before write.

Examples, where `<cca-skill>` is the resolved installed `skills/cca/` root:

```bash
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --init
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --check
python <cca-skill>/assets/hybrid-workspace/audit.py --target <workspace> --self-test
```

Do not copy the Python implementation into the target merely to run it. The installed skill is the portable capability package; the target is the durable workspace it operates on.

## Frozen-v1 contract

The bundled schema preserves the reviewed v1 semantic and policy matrix. In particular:

- semantic `key` values are stable downstream identifiers;
- `binding_change` is non-breaking;
- effective permission is the intersection of mutability, authority, agent access, and boundary policy;
- relocation requires source and destination authority;
- nested instructions may narrow but never widen inherited authority;
- external/upstream control-looking files are untrusted at the outer workspace boundary;
- archive relocation preserves semantic identity and provenance;
- `knowledge.reference` is human-authoritative and immutable to agents in frozen v1;
- promotion into human-authoritative material remains human-authorized;
- `context.router` is derived and its concrete filename is its current binding, not the literal string `CONTEXT.md`;
- generated helpers are derived target artifacts and never semantic identities.

Do not change a frozen semantic key, policy meaning, authority meaning, axis, or vocabulary value as a binding customization. Such changes require the profile's declared schema-version treatment.

### Crosswalks are advisory relationships

The `crosswalk` material in frozen-v1 records provenance/influence for humans and tools. It is **not** a second semantic-key namespace and MUST NOT be interpreted as one-to-one equivalence.

In particular, PARA `Resources` is broader than `knowledge.reference`. A Resource may contain preserved evidence, a human-authored note, maintained synthesis, a dataset, or a nested workspace. Consumers MUST use the target's actual boundary/role/authority semantics rather than infer epistemic type solely from a crosswalk label.

Changing the machine representation of the frozen crosswalk itself is a profile-version concern; frozen-v1 consumers must therefore treat the current simple mapping as advisory/partial unless an entry is independently proven exact.

## Bootstrap and independent implementation contract

A consumer that knows the profile but does not have the CCA skill installed MUST be able to start from durable target files.

For frozen-v1:

1. `WORKSPACE.yaml` at the target root is the machine-readable profile bootstrap and semantic binding/policy contract.
2. `AGENTS.md` is the human/agent control surface and must identify `workspace-contract:v1` as required by the profile.
3. Semantic resolution starts from the applicable boundary and `slots[*].key`; `slots[*].binding` gives the concrete target-local implementation.
4. The value of a default binding is never the semantic identity. `context.router` is the semantic generated-router role even when the current binding is `CONTEXT.md`, `ROUTER.md`, or another valid profile binding.
5. An implementation MUST validate binding text and symlink-resolved containment before reading/writing generated/profile-controlled destinations.
6. Authority, mutability, agent access, boundary trust, privileged operations, archive identity, and promotion gates are interpreted from the declared schema contract, not reconstructed from default folder names.
7. Derived artifacts are rebuildable views/adapters. They MUST NOT become a competing authority over `WORKSPACE.yaml`, human-authored control files, or canonical workspace content.

### Generated artifact semantics

The profile distinguishes semantic outputs from reference-implementation filenames:

- **`context.router`** — semantic output role. It MUST be generated/validated at the slot's current binding. The frozen-v1 `generation_contract.derived` list still carries the historical/default literal `CONTEXT.md` for compatibility with the current bundled implementation; consumers MUST interpret that entry as the `context.router` role, not as a fixed filename requirement.
- **`SPEC.md`** — derived human-readable rendering of the target profile contract; non-authoritative.
- **`paths.sh`** — derived shell binding adapter used by the reference implementation; non-authoritative.
- **`mkdirs.sh`** — derived reference helper for materializing declared directories/files; non-authoritative.
- **`obsidian-excludes.txt`** — derived editor/indexing adapter; non-authoritative.

An alternative implementation does **not** need byte-for-byte Python output to implement CCA core. To claim frozen-v1 **profile conformance**, however, it must preserve the semantic content and safety guarantees promised by each profile-required derived artifact. The bundled `generate.py --check` performs byte-for-byte drift checking only for artifacts generated by this reference implementation; that check is a reference-implementation regression mechanism, not a language monopoly.

This distinction lets a Rust/Go/other implementation reproduce the profile from this contract and `WORKSPACE.yaml` without reverse-engineering Python control flow.

## Detection

Treat a workspace as this profile when its local `WORKSPACE.yaml` matches the bundled frozen-v1 key/policy contract and the required human-authored control surface identifies `workspace-contract:v1`. Do not classify any arbitrary YAML manifest as this profile.

A profile workspace is:

- **CCA-compatible** by construction;
- **CCA-conformant** when it satisfies the applicable CCA core contract;
- **profile-conformant** when the frozen-v1 profile audit and required semantic/generated-artifact checks pass;
- **upstream-native** only for a nested or overlapping upstream boundary that independently passes that upstream's own acceptance rules.

## Mode routing

- `architect` selects/composes the profile and chooses bindings/authority boundaries.
- `scaffold` initializes the approved profile on an explicit target with `generate.py --target <workspace> --init`.
- `sync` reconciles derived artifacts after authorized schema/binding changes with `generate.py --target <workspace>`; `--check` is report-only.
- `lint` runs `audit.py --target <workspace>` and `generate.py --target <workspace> --check` for the bundled reference implementation and validates profile semantics independently of language-specific rendering details.
- `ingest` and `query` resolve semantic keys and bindings from the target contract; they do not assume the profile's default paths.
- `advise` may recommend a different profile or upstream method when it better serves the user's intent.

## Routing and scale

The root `context.router` is an orientation surface, not a universe-wide document manifest.

As collections grow, boundaries under `knowledge.durable`, `knowledge.reference`, projects, or other large roles MAY introduce local routers/catalogs/indexes. These local surfaces should enumerate or summarize only their own scope. The root router should route to the relevant boundary/role and let local navigation continue from there.

Derived local indexes, embeddings, search databases, or graph projections remain rebuildable accelerators unless another declared authority explicitly owns that data. The profile therefore scales by recursive/federated routing rather than by growing one root manifest indefinitely.

## Acceptance

Before describing a target as profile-conformant:

1. the frozen schema audit passes;
2. the adversarial mutation/self-test passes when release-grade verification is requested;
3. required generated semantic outputs are present and consistent with the target contract;
4. reference-implementation artifacts pass canonical-render drift checks when the bundled Python implementation produced/owns them;
5. `AGENTS.md` satisfies the profile control contract;
6. changing a non-breaking binding causes every generated consumer to follow the new binding;
7. changing `context.router` changes the generated router path without requiring a fixed `CONTEXT.md` identity;
8. no generated artifact leaks obsolete `_state/`, `_runtime/`, or other default paths after those bindings move;
9. all generated destinations remain beneath the explicit target after symlink resolution;
10. generation/audit operate on the explicit target and leave the installed skill package untouched;
11. applicable upstream-native boundaries still pass their own upstream acceptance surface;
12. a fresh human or agent can orient from durable files without relying on prior chat state.
