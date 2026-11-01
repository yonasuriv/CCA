# CCA Method Composition

Normative companion to `spec.md` and `compatibility.md`.

## 1. Purpose

CCA may coexist with human knowledge-work methodologies and organizational systems without redefining them as CCA compatibility profiles.

CCA currently recognizes **PARA**, **Zettelkasten**, and **Building a Second Brain (BASB/CODE)** as common method overlays. This list is descriptive rather than closed; another filesystem-compatible method may be composed under the same rules.

## 2. Method overlays

A **method overlay** is a methodology that influences organization, knowledge development, or human workflow without defining a CCA-native structural compatibility profile.

CCA MUST NOT treat an overlay as equivalent to upstream-native ICM, LLM Wiki compatibility, AGENTS.md conformance, Agent Skills conformance, or a named CCA profile unless that methodology publishes a concrete applicable machine-facing contract that CCA intentionally adopts in a future revision.

Examples:

- **PARA** may organize material into Projects, Areas, Resources, and Archives.
- **Zettelkasten** may organize knowledge as addressable linked notes.
- **BASB/CODE** may guide the lifecycle Capture → Organize → Distill → Express.
- **GTD / custom shelves** may organize by next-action, domain, or another human concern.

CCA may describe a workspace as PARA-organized, Zettelkasten-style, BASB-guided, or otherwise overlay-shaped, but those labels are not additional CCA compatibility states.

### Organization, epistemic role, admission provenance, and navigation

These are separate concerns:

- an organizational shelf answers **where material lives**;
- an epistemic/semantic role answers **what kind of information it is** and often implies different authority/lifecycle expectations;
- an admission/provenance classification may answer **how a source entered a particular corpus** without replacing the source's semantic role;
- a navigation contract answers **how a consumer discovers the relevant boundary and context**.

Therefore PARA `Resources` is not semantically equivalent to CCA `knowledge.reference`. A Resource may contain external evidence, a human note, maintained synthesis, a dataset, or a nested workspace. Crosswalks MUST describe partial/composed relationships where one-to-one equivalence is false.

The current CCA Hybrid Workspace Profile demonstrates admission classification without ontology replacement:

```text
reference.curated   -> knowledge.reference
reference.collected -> knowledge.reference
```

`knowledge.reference` remains the semantic role: preserved source/evidence. `reference.curated` and `reference.collected` classify the curation state of evidence in that profile's reference corpus (under the supported v2 schema: how it was admitted). They MUST NOT be interpreted as separate knowledge roles, content authorship, acquisition actor, truth, or endorsement.

Similarly, finite research work remains project/workflow activity rather than a new knowledge category: capture, preserved references, maintained synthesis, and outputs retain their own semantic roles as research traverses them.

CCA core does not mandate those Hybrid classifications for every `knowledge.reference` implementation. They are profile-owned semantics. CCA core only requires consumers to preserve declared classification/role composition rather than collapsing the two dimensions.

CCA core does not mandate an ICM-shaped navigation skeleton for every overlay or CCA-compatible workspace. Use:

- exact current ICM routing when the boundary is upstream-native ICM;
- selected ICM-derived patterns when the target explicitly adopts them;
- a named CCA profile's own bootstrap/routing contract when that profile is selected;
- the target's existing router/index/instruction convention when it already provides sufficient deterministic navigation;
- ordinary filesystem inference when no stronger declaration is required.

## 3. Boundary composition

**Nested boundaries must remain independently interpretable by the convention that owns them.**

An outer organizational method may determine where a nested workspace lives, but MUST NOT silently rewrite the nested workspace's native semantics merely for uniformity.

Therefore:

1. A native ICM root nested under a PARA Project remains governed by the complete applicable current ICM profile.
2. An LLM Wiki-style maintained knowledge base nested under a Resources tree remains governed by its own maintenance/schema instructions.
3. A coding repository nested under a broader second-brain hierarchy retains its application structure and scoped instructions.
4. Zettelkasten notes are not assumed agent-writable; their authority/maintenance behavior comes from the local workspace instructions.
5. CCA routing may connect these boundaries, but MUST NOT merge their schemas merely because they coexist.
6. When a selected profile declares nested classification bindings, semantic classification may compose while filesystem mutation policy remains governed by the most-specific applicable binding according to that profile's contract.

A CCA-aware consumer should be able to understand the relationship between boundaries while an upstream-specific consumer can still enter the nested native root and operate without CCA-only semantics.

## 4. Metadata discipline

CCA should infer ordinary filesystem semantics when doing so is safe. It MUST NOT require a universal manifest that merely restates obvious directory roles or duplicates native routing.

Explicit metadata is appropriate when:

- a workspace-specific semantic/binding fact cannot safely be inferred;
- authority or mutation policy would otherwise be ambiguous;
- provenance/admission/review facts cannot be safely reconstructed from the path or content;
- the active upstream/profile requires the metadata;
- a user intentionally adopts an optional CCA hardening convention.

PARA directories, Zettelkasten folders, ICM stages, wiki folders, projects, areas, resources, archives, and skill collections do not require CCA metadata solely to announce their path names.

A profile MAY require provenance metadata for evidence when the distinction is security/authority relevant. The Hybrid source contract is such a case: acquisition actor/method/origin/time and content identity are not safely inferable merely because a file lives under `collected/` or `curated/`. Hybrid v3 lets the representation fit the object (Markdown frontmatter with a body-scoped hash, file sidecars, directory/corpus manifests) without weakening those guarantees.

## 5. CCA skill package and modes

CCA is **one installable Agent Skill** named `cca`. It exposes seven lazy modes: six workspace operations (`architect`, `scaffold`, `sync`, `ingest`, `query`, `lint`) plus the separate `advise` judgment capability.

Package portability means:

1. every runtime resource referenced by path remains inside `skills/cca/` after installation;
2. no mode depends on removed sibling skill packages or repository-global implementation files;
3. installation location is not part of CCA semantics;
4. modes coordinate by semantic mode name, not filesystem package boundaries;
5. architect and advisor remain separate reference domains even though they share one package.

`architect` is the primary entry point for compound architecture/design requests. It is not a mandatory gateway for an operation whose intent already matches another mode directly.

## 6. Progressive disclosure

CCA uses Agent Skills progressive disclosure *inside the single package* rather than splitting tightly coupled operations into separately installable skills or loading all references at activation time.

- `SKILL.md` routes intent to one mode;
- a mode loads only the core/form/method/advisor references required by the task;
- detailed methodology knowledge stays behind architect references;
- advisor references stay behind `advise` or explicit architect consultation;
- focused operations do not need to load unrelated architecture or advisor material.

Creating dedicated PARA, Zettelkasten, BASB, Scrum, or similar CCA skills is not justified merely to store methodology knowledge. Those external methods remain authorities and are loaded only when the active problem crosses their boundary.

## 7. Validation

`lint` MUST NOT invent native PARA, Zettelkasten, or BASB profiles.

It may verify locally declared method-preservation constraints when a workspace explicitly defines them, but those findings MUST be distinguished from upstream-native compatibility claims.

Method composition is healthy when:

- nested native profiles remain valid;
- file authority/write behavior is clear enough for the requested operation;
- routing crosses boundaries without duplicating or flattening their rules;
- organizational shelves are not mistaken for epistemic roles;
- declared admission/provenance classifications are not mistaken for semantic roles or content authorship;
- navigation requirements come from the active upstream/profile/local contract rather than an undeclared universal skeleton;
- large collections can introduce boundary-local routing/indexing without requiring a global manifest.
