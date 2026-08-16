# Schema -- the rules of this workspace

The closed set of note types, the labels they carry, and the naming they follow. When practice and this file disagree, reconcile the same day -- schema drift is how structures rot.

## Node types

| `type:` | Lives at | Carries |
|---|---|---|
| [type] | [path pattern] | [frontmatter + sections] |
| [type] | [path pattern] | [frontmatter + sections] |
| [type] | [path pattern] | [frontmatter + sections] |

## Labels that make it queryable

`type`, `owner`, `ai-level` (L0-L3), `value` (1-5), `pain` (1-5), `governance` (internal / sensitive / external). `consumes:` and `produces:` are wikilinks to assets -- the links draw the map on their own. value + pain >= 8 flags a pilot candidate.

## Naming

- Slugs: kebab-case. Data assets always `data-[thing].md`.
- Human-browsed cards may use Title Case filenames -- but declare that choice here and hold it everywhere.
- [Workspace-specific] metadata holds the rules (this file). Generated indexes are rebuilt by script, never hand-edited.

## Maintenance

- [Who reconciles drift and how often]
- [When a new node type is introduced vs. folded into an existing one]