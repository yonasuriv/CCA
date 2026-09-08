# System Map form

Use a System Map when the subject is a mutable repository, vault, or mixed tree and the user needs reliable **change-impact reasoning** rather than only an organizational/process graph.

A System Map is distinct from a Context Map:

- **Context Map**: people, teams, workflows, systems, ownership, information movement.
- **System Map**: concrete mutable objects, processes, effects, source-backed change impact.

Do not create either form when ordinary code navigation, search, or existing architecture documentation already answers the question cheaply.

## Smallest justified shape

Start with inventory and a proposed map. Create shelves only when verified material needs them:

```text
map/
├── CONTEXT.md
├── schema.md
├── templates/
├── objects/
├── processes/          # only when verified recurring movements exist
└── effects/
    └── CONTEXT.md      # only when a useful impact index exists
```

The subject tree remains source of truth. Cards cite it; they do not copy it into a second specification.

## Universes

Classify evidence-backed material when the distinction is useful:

- **live**: currently wired/in force;
- **leftover**: still present but no longer the primary path;
- **ghost**: named, documented, or stubbed but not actually wired/implemented.

Do not promote aspiration or a stale document to live merely because it has a confident name.

## Human/cold-walk slices

System-map construction can be expensive. Work in slices and stop for human review **or a cold-agent verification gate** before the next expensive slice:

0. **Inventory**: inspect the real tree, infer candidate nouns/verbs, classify universes, propose the smallest useful map; do not write speculative cards.
1. **Catalog**: establish `CONTEXT.md`, schema/templates and a route from the subject's existing orientation surface when needed.
2. **Objects**: create source-cited noun cards. Mark verified only when citations/revision evidence support the claim.
3. **Processes**: add only recurring movements that can be evidenced. State input → movement → output and link affected objects.
4. **Effects**: create the change-impact index. `Hits` and `Does not hit` should capture first-order boundaries, not invented waterfalls.
5. **Inbound/reverse walk**: for important mapped objects, determine what known consumers **outside** the subject tree point into them. Ask the owner and inspect bounded known integration surfaces such as configs, sibling/parent repositories, issue/project automation, agents, harnesses, CI/deploy definitions, and scheduled jobs. Record each external consumer on the card it lands on; absence from the subject tree is not evidence that no inbound dependency exists.
6. **Re-verify**: re-open source for load-bearing claims, especially impact boundaries and inbound dependencies, after the initial fill or material subject changes.

A person does not have to approve every trivial file; the gate exists before costly/speculative expansion. Linear verification may continue when evidence is deterministic.

`effects/CONTEXT.md` answers the outward question: “if I change X, what inside the mapped subject moves?” The inbound/reverse walk answers the complementary question: “what outside this tree points into X?” Keep those directions distinct so a useful internal impact index does not create false confidence about external consumers.

## Card requirements

A useful object/process card identifies:

- what the thing is, including product/file/type names when they differ;
- why its shape matters;
- source-of-truth path(s) and revision/verification context when available;
- connected objects/processes;
- **Hits** and **Does not hit** for useful first-order change boundaries;
- who/what reads or writes it, including verified inbound external consumers where material;
- inference versus observed fact.

Do not mark a card verified without source evidence. Do not cite another explanatory card as the final source when the real code/file is available.

## Cold-agent walk

A fresh agent with no chat memory should be able to:

1. reach the map from the subject's normal entry/orientation surface;
2. distinguish live, leftover, and ghost names that matter;
3. open one card and land on the real source it cites;
4. answer one stated change-impact question from `effects/CONTEXT.md` plus the minimum relevant cards;
5. state both what the change hits and an obvious nearby thing it does **not** hit;
6. identify known material inbound consumers from outside the subject tree, or state explicitly that the bounded reverse walk did not verify any;
7. identify which claims are inferred or stale and need re-verification.

If the agent must load the whole map or the map merely duplicates source files, split/shrink it rather than adding a longer reading guide.

## Failure modes

- collapsing Context Map and System Map into one vague graph;
- generating empty `processes/`/`effects/` shelves for symmetry;
- copying source behavior into cards instead of citing source;
- treating ghost/leftover material as live;
- verified labels without evidence;
- unlimited transitive impact claims;
- an outward-only effects index that ignores what points into the tree from outside;
- claiming there are no external consumers merely because no internal file names them;
- a map that becomes more expensive to maintain than direct navigation.
