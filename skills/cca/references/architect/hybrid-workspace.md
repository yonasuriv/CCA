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

## Portable implementation

The complete reference implementation is bundled with this installed skill under:

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
    └── test_targeting.py
```

Repository-global files are never runtime dependencies of this profile.

`WORKSPACE.yaml` and `AGENTS.md` are templates for the **target workspace**. The Python files remain tooling in the installed CCA skill. Generated artifacts belong to the target workspace, never beside the installed scripts.

## Target rule

Every workspace operation MUST resolve an explicit target root.

The bundled generator intentionally requires `--target` and refuses to use the installed package directory or one of its descendants as the target. `--init` may create a target root and seed missing human-authored templates, but it never overwrites an existing `WORKSPACE.yaml` or `AGENTS.md`.

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

## Detection

Treat a workspace as this profile when its local `WORKSPACE.yaml` matches the bundled frozen-v1 key/policy contract and the required human-authored control surface identifies `workspace-contract:v1`. Do not classify any arbitrary YAML manifest as this profile.

A profile workspace is:

- **CCA-compatible** by construction;
- **CCA-conformant** when it satisfies the applicable CCA core contract;
- **profile-conformant** when the frozen-v1 profile audit and generated-artifact checks pass;
- **upstream-native** only for a nested or overlapping upstream boundary that independently passes that upstream's own acceptance rules.

## Mode routing

- `architect` selects/composes the profile and chooses bindings/authority boundaries.
- `scaffold` initializes the approved profile on an explicit target with `generate.py --target <workspace> --init`.
- `sync` reconciles derived artifacts after authorized schema/binding changes with `generate.py --target <workspace>`; `--check` is report-only.
- `lint` runs `audit.py --target <workspace>` and `generate.py --target <workspace> --check` for profile conformance/drift.
- `ingest` and `query` resolve semantic keys and bindings from the target contract; they do not assume the profile's default paths.
- `advise` may recommend a different profile or upstream method when it better serves the user's intent.

## Acceptance

Before describing a target as profile-conformant:

1. the frozen schema audit passes;
2. the adversarial mutation/self-test passes when release-grade verification is requested;
3. generated artifacts match the canonical render;
4. `AGENTS.md` satisfies the profile control contract;
5. changing a non-breaking binding causes every generated consumer to follow the new binding;
6. changing `context.router` changes the generated router path without requiring a hardcoded `CONTEXT.md`;
7. no generated artifact leaks obsolete `_state/`, `_runtime/`, or other default paths after those bindings move;
8. generation/audit operate on the explicit target and leave the installed skill package untouched;
9. applicable upstream-native boundaries still pass their own upstream acceptance surface;
10. a fresh human or agent can orient from durable files without relying on prior chat state.
