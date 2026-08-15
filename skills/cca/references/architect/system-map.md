# System Map form

Use a System Map when the subject is a mutable repository, vault, or mixed tree
and the user needs reliable change-impact reasoning rather than only an
organizational/process graph.

A System Map is distinct from a Context Map:

- **Context Map**: people, teams, workflows, systems, information movement.
- **System Map**: concrete mutable objects, processes, effects, and change impact.

## Minimal shape

```text
map/
├── CONTEXT.md
├── schema.md
├── templates/
├── objects/
├── processes/
└── effects/
```

Use the existing workspace paths as evidence; do not copy the whole repository
into the map. Object/process/effect cards must cite their source of truth.

## Required semantics

- classify discovered material as **live**, **leftover**, or **ghost** when that distinction can be evidenced;
- record `Hits` and `Does not hit` for impact boundaries where useful;
- maintain a change-impact index from mapped object/process relationships;
- distinguish observed fact from inference;
- re-verify affected cards after material changes;
- support a cold-agent walk: a fresh agent can identify what changes, what is affected, and which source files prove it.

Do not use System Map when ordinary code navigation, existing architecture docs,
or search already answer the question cheaply. The form must earn its maintenance cost.
