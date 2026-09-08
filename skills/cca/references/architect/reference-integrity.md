# Reference integrity for restructures

Read this only when Architect is restructuring, migrating, moving, renaming, merging, archiving, or deleting existing workspace content. It is a move-safety gate, not a new semantic profile.

For an **upstream-native ICM** boundary, current upstream ICM remains the authority. This reference preserves the current inherited restructure floor while making the same safety mechanics available to CCA-owned/custom restructures where they fit.

A clean post-change walk proves the result is navigable. It does not prove the migration itself was safe. Apparent disuse is not evidence that a path can move.

## Pre-move reference integrity

Before proposing any destructive or path-changing action, enumerate what points at each affected path:

1. **In-boundary references** — direct path/name references from files inside the target boundary.
2. **Sibling/escaping relative references** — especially `../` paths whose meaning changes when folders are regrouped.
3. **Symlinks** — both links being moved and links whose targets are being moved.
4. **Known external consumers** — parent/sibling repositories, configs, scripts, CI, scheduled jobs, issue/project automation, agents, harnesses, deployment definitions, or other systems that hardcode or otherwise depend on the current path.

External discovery must stay bounded. Search known adjacent/declared consumers and ask the owner when only human knowledge can resolve the dependency; do not turn the gate into an unbounded filesystem or network crawl.

Record referrers on the migration map. A path with a live referrer is **held** unless every affected referrer is updated in the same approved change or an explicit compatibility pointer/bridge preserves the contract.

A file is not Dead, stale-safe, or archive-safe until this dependency check supports that classification.

## Destination collision gate

Before any copy or rename, compare the intended destination against existing paths **case-folded** within the relevant parent scope.

Case-only or case-colliding names such as `CONTEXT.md` and `context.md` can alias on case-insensitive filesystems even when an inventory lists them separately. Surface every collision before approval; do not rely on a post-copy parity check to discover an overwrite after the source has already replaced the destination.

This check supplements existing path/symlink containment rules. Containment answers whether a destination escapes a boundary; case-fold checking answers whether a supposedly new destination aliases an existing one.

## Copy, verify, then remove

For moves/renames of substantive existing content, prefer a recoverable sequence:

1. copy to the approved destination;
2. verify source/destination parity before removal;
3. remove the original only after parity passes and required referrers are updated/preserved.

Parity should be appropriate to the artifact:

- text/ordinary files: byte/content hash;
- directory moves: file count plus per-file/content verification sufficient to detect omissions or substitutions;
- archive/container formats with incidental metadata: compare meaningful unpacked content when outer hashes are not stable evidence of semantic parity.

If parity cannot be established safely, stop before removing the original and report the unresolved condition.

## Durability gate

Before reorganizing important content, verify the source is durably recoverable: tracked by version control, backed up, or otherwise recoverable according to the owning boundary's contract.

Do not make an irreversible tidy-up inside temporary, ignored, ephemeral, or otherwise unrecoverable storage merely because the target tree looks cleaner afterward.

## Post-move verification

After the approved migration:

1. re-run every pre-move reference that was expected to survive;
2. verify updated referrers resolve to the intended semantic owner;
3. verify compatibility pointers/bridges when intentionally retained;
4. verify no case-fold collision or stale source path remains hidden by filesystem behavior;
5. run the applicable upstream/profile/CCA validation and fresh-consumer walk.

A restructure is not successful merely because the destination exists. If a reference that resolved before the move is expected to remain valid and no longer resolves, the migration is broken.

## Migration-map evidence

For path-changing work, the migration map should carry enough evidence to review the move before execution:

```text
current path -> function/authority -> destination -> action -> referrers -> compatibility impact
```

The approval gate reviews this evidence, not a guess based on directory appearance.
