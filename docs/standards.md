# Upstream standards tracked by CCA

CCA converges on existing conventions where they already solve the problem. This file is the maintenance surface for standards that materially constrain CCA. It is not a catalog of every AI standard.

| Standard / upstream | CCA dependency | Compatibility rule |
|---|---|---|
| [AGENTS.md](https://agents.md) | Portable agent instructions and nested directory-scoped guidance | Use `AGENTS.md` as the canonical portable instruction file. Respect nearest-file precedence in nested trees. Do not invent a competing portable root filename. |
| [Agent Skills](https://agentskills.io) | Portable `SKILL.md` packages | Every bundled skill must satisfy the current Agent Skills specification, keep `SKILL.md` compact, use relative self-contained resources, and preserve progressive disclosure. |
| [ICM / Model Workspace Protocol](https://github.com/RinDig/Interpretable-Context-Methodology) | Five-layer routing, stage contracts, one-way references, selective section loading, canonical sources, human-editable handoffs | Preserve ICM shapes and semantics unchanged where CCA claims ICM compatibility. CCA extensions must remain optional to an ICM consumer. |
| [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | Persistent LLM-maintained synthesis over immutable/raw source material | Preserve the idea file's intentionally flexible implementation surface. CCA may recommend stronger conventions, but must not mislabel CCA-specific schema, frontmatter, directory, or logging choices as LLM Wiki requirements. |
| [MCP](https://modelcontextprotocol.io) | Tool/context transport outside the filesystem workspace | Treat MCP as an adjacent runtime/tool protocol, not a CCA replacement or required dependency. Filesystem-native CCA workspaces remain useful without MCP. |

## Upstream-change rule

When an upstream convention changes:

1. Verify the current primary source.
2. Identify whether CCA mirrors, aliases, or merely interoperates with the changed behavior.
3. Prefer changing CCA over freezing an obsolete fork.
4. Keep compatibility additions optional unless the upstream itself makes them mandatory.
5. Update the spec, affected skills/templates, examples, migration guidance, and this matrix in the same change.

## Compatibility vocabulary

CCA uses these terms deliberately:

- **Native-compatible**: an upstream workspace can be consumed without structural migration.
- **CCA-hardened**: optional CCA conventions were added for stronger portability, routing, provenance, or maintenance.
- **CCA-conformant**: the workspace intentionally adopts the CCA specification.

Native compatibility does **not** imply that an ICM workspace or LLM Wiki is itself a CCA workspace, and CCA conformance must never be retroactively imposed on upstream projects.
