# CCA Method Composition

Normative companion to `SPEC.md` and `compatibility.md`.

## 1. Purpose

CCA may coexist with human knowledge-work methodologies and organizational systems without redefining them as CCA compatibility profiles.

CCA currently recognizes **PARA**, **Zettelkasten**, and **Building a Second Brain (BASB/CODE)** as common method overlays. This list is descriptive rather than closed; another filesystem-compatible method may be composed under the same rules.

## 2. Method overlays

A **method overlay** is a methodology that influences organization, knowledge development, or human workflow without defining a CCA-native structural compatibility profile.

CCA must not treat an overlay as equivalent to native ICM compatibility, native LLM Wiki compatibility, AGENTS.md conformance, or Agent Skills conformance unless that methodology publishes a concrete applicable machine-facing contract that CCA intentionally adopts in a future revision.

Examples:

- **PARA** may organize material into Projects, Areas, Resources, and Archives.
- **Zettelkasten** may organize knowledge as addressable linked notes.
- **BASB/CODE** may guide the lifecycle Capture → Organize → Distill → Express.

CCA may describe a workspace as PARA-organized, Zettelkasten-style, or BASB-guided, but those labels are not additional CCA compatibility states.

## 3. Boundary composition

**Nested boundaries must remain independently interpretable by the convention that owns them.**

An outer organizational method may determine where a nested workspace lives, but must not silently rewrite the nested workspace's native semantics merely for uniformity.

Therefore:

1. A native ICM root nested under a PARA Project remains governed by the complete applicable current ICM profile.
2. An LLM Wiki nested under a Resources tree remains governed by its own maintenance/schema instructions.
3. A coding repository nested under a broader second-brain hierarchy retains its application structure and scoped instructions.
4. Zettelkasten notes are not assumed to be agent-writable; their authority/maintenance behavior comes from the local workspace instructions.
5. CCA routing may connect these boundaries, but must not merge their schemas merely because they coexist.

A CCA-aware agent should be able to understand the relationship between boundaries while an upstream-specific consumer can still enter the nested native root and operate without CCA-only semantics.

## 4. Metadata discipline

CCA should infer ordinary filesystem semantics when doing so is safe. It must not require a universal manifest that merely restates obvious directory roles or duplicates native routing.

Explicit metadata is appropriate when:

- a workspace-specific fact cannot safely be inferred;
- authority or write policy would otherwise be ambiguous;
- the active upstream/profile requires the metadata;
- a user intentionally adopts an optional CCA hardening convention.

PARA directories, Zettelkasten folders, ICM stages, wiki folders, projects, areas, resources, archives, and skill collections do not require CCA metadata solely to announce their path names.

## 5. CCA skill package and modes

CCA is **one installable Agent Skill** named `cca`. It exposes seven lazy modes: six workspace operations (`architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`) plus the separate `advise` judgment capability.

Package portability means:

1. every runtime resource referenced by path remains inside `skills/cca/` after installation;
2. no mode depends on removed sibling skill packages or repository-global implementation files;
3. installation location is not part of CCA semantics;
4. modes coordinate by semantic mode name, not filesystem package boundaries;
5. architect and advisor remain separate reference domains even though they share one package.

`architect` mode is the primary entry point for compound architecture/design requests and may lazy-load form/method references or consult the advisor domain for judgment. It is not a mandatory gateway for an operation whose intent already matches another mode directly.

## 6. Progressive disclosure

CCA uses Agent Skills progressive disclosure *inside the single package* rather than splitting tightly coupled operations into separately installable skills or loading all references at activation time.

- `SKILL.md` routes intent to one mode;
- a mode loads only the core/form/method/advisor references required by the task;
- detailed methodology knowledge stays behind architect references;
- advisor references stay behind `advise` or explicit architect consultation;
- focused operations do not need to load unrelated architecture or advisor material.

Creating dedicated PARA, Zettelkasten, BASB, Scrum, or similar CCA skills is not justified merely to store methodology knowledge. Those external methods remain authorities and are loaded only when the active problem crosses their boundary.

## 7. Validation

`lint` mode must not invent native PARA, Zettelkasten, or BASB profiles.

It may verify locally declared method-preservation constraints when a workspace explicitly defines them, but those findings must be distinguished from upstream/native compatibility claims.

Method composition is healthy when:

- nested native profiles remain valid;
- file authority/write behavior is clear enough for the requested operation;
- routing crosses boundaries without duplicating or flattening their rules;
- the fresh-agent walk test can identify the relevant boundary and load the smallest sufficient context.
