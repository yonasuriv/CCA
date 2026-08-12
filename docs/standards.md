# Upstream standards tracked by CCA

CCA converges on existing conventions where they already solve the problem. This file is the maintenance surface for standards that materially constrain CCA. It is not a catalog of every AI standard.

| Standard / upstream | CCA dependency | Compatibility rule |
|---|---|---|
| [AGENTS.md](https://agents.md) | Portable agent instructions and nested directory-scoped guidance | Use `AGENTS.md` as the canonical portable instruction file where the standard is applicable. Respect nearest-file precedence in nested trees. Do not invent a competing portable root filename. |
| [Agent Skills](https://agentskills.io) | Portable `SKILL.md` packages | Every bundled skill must satisfy the current Agent Skills specification, keep `SKILL.md` compact, use relative self-contained resources, and preserve progressive disclosure. |
| [ICM / Model Workspace Protocol](https://github.com/RinDig/Interpretable-Context-Methodology) | Five-layer routing, stage contracts, one-way references, selective section loading, canonical sources, human-editable handoffs, onboarding, quality gates | Preserve ICM shapes and semantics unchanged where CCA claims native ICM compatibility. Treat `_core/CONVENTIONS.md` as the canonical semantic authority and the workspace-builder validation stage as the practical acceptance checklist for generated workspaces. CCA extensions must remain optional to an ICM consumer. |
| [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | Persistent LLM-maintained synthesis over durable source material | Preserve the idea file's intentionally flexible implementation surface. CCA may recommend stronger conventions, but must not mislabel CCA-specific schema, frontmatter, directory, or logging choices as LLM Wiki requirements. |
| [MCP](https://modelcontextprotocol.io) | Tool/context transport outside the filesystem workspace | Treat MCP as an adjacent runtime/tool protocol, not a CCA replacement or required dependency. Filesystem-native CCA workspaces remain useful without MCP. |

## ICM compatibility authority

CCA must distinguish **native ICM compatibility** from merely borrowing ICM patterns.

For a native ICM claim, check the current upstream in this order:

1. `_core/CONVENTIONS.md` — canonical ICM/MWP rules and patterns.
2. `workspaces/workspace-builder/stages/05-validation/CONTEXT.md` — practical validation/acceptance checklist used by the upstream builder.
3. Root README contribution/PR checklist — additional repository-level expectations for contributed workspaces.
4. The actual workspace's own `CLAUDE.md`, root `CONTEXT.md`, stage contracts, references, setup files, and outputs.

CCA's own walk test is supplemental. It must not replace a stricter upstream acceptance surface.

A project that uses `stages/01-name/` and ICM-style stage contracts but omits the rest of the native ICM profile should be described as **ICM-derived**, not as fully native ICM-compatible.

Where upstream ICM prescribes a specific trigger or representation, CCA preferences such as Mermaid diagrams do not override it.

## Upstream-change rule

When an upstream convention changes:

1. Verify the current primary source.
2. Identify whether CCA mirrors, aliases, or merely interoperates with the changed behavior.
3. Prefer changing CCA over freezing an obsolete fork.
4. Keep compatibility additions optional unless the upstream itself makes them mandatory.
5. Update the spec, affected skills/templates, examples, migration guidance, and this matrix in the same change.
6. Re-run the relevant upstream-profile acceptance checks before claiming compatibility.

## Compatibility vocabulary

CCA uses these terms deliberately:

- **Native-compatible**: an upstream workspace can be consumed without structural migration and, where CCA generates or materially rewrites that profile, the applicable upstream acceptance surface passes.
- **ICM-derived**: a non-ICM workspace intentionally borrows selected ICM patterns without claiming the full native ICM profile.
- **CCA-hardened**: optional CCA conventions were added for stronger portability, routing, provenance, or maintenance.
- **CCA-conformant**: the workspace intentionally adopts the CCA specification.

Native compatibility does **not** imply that an ICM workspace or LLM Wiki is itself a CCA workspace, and CCA conformance must never be retroactively imposed on upstream projects.
