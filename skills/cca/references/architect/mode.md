# Architect mode

Design the smallest filesystem/context architecture that makes the work navigable, durable, human-understandable, and agent-agnostic.

Read `../core/spec.md` and `core.md` before designing. Read `forms.md` only when choosing a workspace form. Read `workspace-builder.md` when the request is to create, initialize, set up, report status for, or materially rebuild a workspace. Read `methods.md` when the request involves PARA, Zettelkasten, BASB/CODE, second brains, PKM, LLM Wiki/ICM composition, or another hybrid knowledge-work architecture. Read `hybrid-workspace.md` only when the optional CCA Hybrid Workspace Profile is selected or detected. Read `../core/adapters.md` only when a harness-specific adapter is needed.

## Role in the CCA skill

`architect` is the primary entry point for compound architecture requests: decide what the workspace should become, which upstreams/methods/profiles apply, where boundaries sit, which semantic roles are required, how those roles bind locally, and which focused mode should execute next.

It is not a mandatory gateway for already-clear operations. Direct lint, ingest, query, sync, or scaffold requests should use those modes directly.

## Trigger routing

- **create / build / initialize workspace** → load `workspace-builder.md` and select/preserve the applicable form/profile.
- **personal/team hybrid profile** → load `workspace-builder.md`, `methods.md` only if method composition matters, then `hybrid-workspace.md` when the profile fits.
- **setup** for upstream-native ICM → load `workspace-builder.md` plus `native-icm-setup.md` and preserve current upstream onboarding semantics.
- **status** for upstream-native ICM → load `workspace-builder.md` and preserve current upstream status behavior.
- **restructure / migrate** → use Restructure mode; do not conflate migration with scaffold.

When another CCA capability is needed, delegate semantically by mode name, e.g. `Use scaffold mode to implement the approved structure` or `Use lint mode to validate the claims`. Never depend on removed sibling skill directories.

## Compatibility gate

Before changing structure, identify the current boundary, upstream-native claims, CCA claims, and method overlays.

- **Upstream-native ICM**: preserve the complete applicable current ICM profile and current upstream acceptance authority. A valid native ICM workspace is already CCA-compatible; do not structurally migrate it merely to make CCA understand it.
- **ICM-derived**: another target may borrow ICM navigation/stage/contract/handoff patterns without claiming full ICM.
- **LLM Wiki compatibility**: discover the implementation's own schema and maintenance conventions first.
- **Ordinary project**: preserve application layout unless restructuring is explicitly requested.
- **CCA-compatible**: CCA can resolve the target without structural migration or semantic replacement.
- **CCA-conformant**: preserve the normative CCA semantics the target intentionally adopted.
- **Profile-conformant**: preserve the named CCA-owned profile contract independently from other claims.
- **CCA Hybrid Workspace Profile**: optional CCA-owned profile; not a new mode and not native ICM. Stable semantic keys remain identity; bindings remain configurable where frozen-v1 permits them.
- **Method overlays**: PARA, Zettelkasten, BASB/CODE, delivery methods, and similar systems remain their own authorities unless an explicit machine-facing contract says otherwise.

Compatibility is interoperability, not ownership. Do not label an upstream workspace CCA-conformant merely because CCA can resolve it.

## Semantic design primitive

For CCA-owned/interoperable architecture decisions, reason through:

```text
boundary + semantic role -> binding
```

Then separately determine authority, mutability, lifecycle/status, provenance, and indexing/visibility semantics where the selected contract requires them.

Do not use a concrete default path as the role identity. If a governing upstream makes a filename/path normative for native conformance, preserve that upstream requirement.

## Build mode

1. Extract the human goal, workflow, knowledge boundaries, organizational methods, and authority lines already implied by the request.
2. Detect and preserve existing upstream-native boundaries before designing CCA additions.
3. Choose the smallest useful form: ordinary repo, native upstream workspace, maintained knowledge system, custom CCA-compatible composition, or named CCA profile.
4. If building a complete workspace, load `workspace-builder.md` and use its discovery → mapping → scaffolding → onboarding-if-needed → validation flow.
5. If human knowledge-work methods are involved, load `methods.md` and preserve them as independent methods/overlays rather than silently turning them into CCA semantics.
6. Decide explicitly whether ICM usage is upstream-native or merely ICM-derived/adopted navigation behavior.
7. Identify nested native boundaries. Outer organization may place them but does not rewrite their internals merely for consistency.
8. If the CCA Hybrid Workspace Profile fits the requested hybrid, prefer the reviewed profile instead of inventing an equivalent custom schema; load `hybrid-workspace.md` and keep its implementation under the existing skill-local asset boundary.
9. If the Hybrid profile does **not** fit, compose a custom CCA-compatible target rather than mutating frozen profile semantics ad hoc.
10. Implement only what the selected form/profile actually needs. Use scaffold mode for focused materialization.
11. Add adapters only when needed and only after reading `../core/adapters.md`.
12. Validate upstream-native claims first, CCA/profile claims next, and the fresh-agent portability walk last.

## Restructure mode

1. **Audit** the actual target and read enough content to classify confidently.
2. **Preserve upstream semantics** before proposing CCA hardening.
3. **Preserve method boundaries** before proposing taxonomy changes.
4. **Map semantics before paths**: current boundary/role/binding → intended boundary/role/binding.
5. **Propose a migration map**: current path → function/authority → destination → action → compatibility impact.
6. **Stop for explicit approval** before moves, merges, renames, or deletions unless the user already authorized direct remediation.
7. Apply only the approved map and preserve content unless deletion was explicitly approved.
8. Use sync mode after structural/binding changes.
9. Validate upstream-native claims, then intentional CCA/profile conformance.

## Hybrid profile target rule

When Architect selects the Hybrid Workspace Profile, it chooses the target and bindings; it does not make the installed skill directory the workspace.

Materialization is delegated to scaffold using the bundled implementation:

```bash
python <cca-skill>/assets/hybrid-workspace/generate.py --target <workspace> --init
```

The target MUST be explicitly resolved outside the installed package. The implementation's own templates/scripts/tests remain within `skills/cca/` for portability.

## Invariants

- Human augmentation is the objective; automation is a means.
- One fact, one canonical home.
- Route before broad search.
- Routing files point; they do not become knowledge dumps.
- Load minimum sufficient context for the active operation.
- Nest boundaries; do not merge schemas merely because several methods coexist.
- Stable semantic roles are distinct from concrete bindings.
- Bindings may move where their governing contract permits; consumers follow the semantic role.
- Upstream-native systems retain their upstream authority.
- Human methods remain independent rather than being absorbed into CCA.
- Cross-mode coordination uses semantic mode names, not sibling filesystem paths.
- `skills/cca/` remains the portable CCA distribution boundary.
- Never invent a competing convention where a proven upstream already solves the problem better.
- Never use CCA compatibility to bypass an upstream repository's own contribution/process rules.
- Never substitute the CCA walk test for stricter upstream/profile acceptance.

## Walk test

After applicable upstream/profile validation, simulate a fresh consumer with no prior chat memory:

1. **Orient**: identify the boundary, authority/profile/methods, and routed context.
2. **Act**: perform one representative operation using only the files/tools exposed by the target.
3. **Report**: state what changed, what was produced, what remains, and what is ambiguous.

If required operating knowledge exists only in chat history or someone's head, improve the durable target rather than explaining around the gap.

## Advisor consultation boundary

Architecture owns workspace structure/composition; advisor owns engineering judgment. When a structural choice depends on process/security/autonomy/model trade-offs, lazily read only the relevant file under `../advisor/`. Do not copy advisor material into architect references and do not turn an advisory methodology into a CCA structural profile.
