#!/usr/bin/env python3
# Adversarial freeze audit for WORKSPACE.yaml.
# Exit non-zero on any contract violation; --self-test proves known corruptions fail.
from __future__ import annotations

import argparse
import copy
import itertools
from pathlib import Path
import sys
from typing import Any

import yaml

from schema import load_schema, resolves_within, validate_binding_text, validate_key

PACKAGE_ROOT = Path(__file__).resolve().parent

SLOT_FIELDS = (
    "id", "category", "key", "binding", "arity", "mutability", "indexed",
    "authority", "agent_access", "link_target", "requirement", "description",
)
VOCAB_FIELDS = (
    "category", "arity", "mutability", "indexed", "authority",
    "agent_access", "link_target", "requirement",
)

# Frozen v1 semantic/policy contract. Bindings/descriptions are intentionally not
# duplicated here because binding changes and wording clarifications are non-breaking.
FROZEN_V1: dict[str, dict[str, Any]] = {
    "workspace.schema": dict(category="bootstrap", arity="file", mutability="mutable", indexed="disabled", authority="human", agent_access="read-only", link_target="none", requirement="required"),
    "agent.instructions": dict(category="control", arity="file", mutability="mutable", indexed="disabled", authority="human", agent_access="read-only", link_target="none", requirement="required"),
    "context.router": dict(category="control", arity="file", mutability="regenerate", indexed="disabled", authority="derived", agent_access="write", link_target="none", requirement="required"),
    "state.current": dict(category="state", arity="file", mutability="replace", indexed="excluded", authority="agent", agent_access="write", link_target="none", requirement="conditional"),
    "state.tasks": dict(category="state", arity="dir", mutability="curated", indexed="excluded", authority="shared", agent_access="write", link_target="none", requirement="conditional"),
    "state.memory": dict(category="state", arity="dir", mutability="append", indexed="disabled", authority="agent", agent_access="write", link_target="none", requirement="conditional"),
    "agent.skills": dict(category="system", arity="dir", mutability="mutable", indexed="disabled", authority="human", agent_access="read-only", link_target="none", requirement="conditional"),
    "system.scripts": dict(category="system", arity="dir", mutability="mutable", indexed="disabled", authority="human", agent_access="read-only", link_target="none", requirement="optional"),
    "system.templates": dict(category="system", arity="dir", mutability="mutable", indexed="disabled", authority="human", agent_access="read-only", link_target="none", requirement="optional"),
    "system.workflows": dict(category="system", arity="dir", mutability="mutable", indexed="disabled", authority="human", agent_access="read-only", link_target="none", requirement="optional"),
    "system.assets": dict(category="system", arity="dir", mutability="mutable", indexed="excluded", authority="human", agent_access="read-only", link_target="none", requirement="optional"),
    "context.capture": dict(category="pipeline", arity="dir", mutability="mutable", indexed="excluded", authority="shared", agent_access="write", link_target="none", requirement="required"),
    "knowledge.reference": dict(category="pipeline", arity="dir", mutability="immutable", indexed="excluded", authority="human", agent_access="read-only", link_target="referenceable", requirement="required"),
    "knowledge.durable": dict(category="pipeline", arity="dir", mutability="curated", indexed="included", authority="shared", agent_access="write", link_target="graph", requirement="required"),
    "output.artifact": dict(category="pipeline", arity="dir", mutability="mutable", indexed="excluded", authority="shared", agent_access="write", link_target="none", requirement="optional"),
    "lifecycle.archive": dict(category="lifecycle", arity="dir", mutability="append", indexed="excluded", authority="shared", agent_access="write", link_target="none", requirement="optional"),
    "responsibility.area": dict(category="lens", arity="dir", mutability="mutable", indexed="included", authority="shared", agent_access="write", link_target="inward", requirement="optional"),
    "work.project": dict(category="lens", arity="dir", mutability="mutable", indexed="included", authority="shared", agent_access="write", link_target="inward", requirement="conditional"),
    "project.notes": dict(category="boundary", arity="dir", mutability="mutable", indexed="included", authority="shared", agent_access="write", link_target="inward", requirement="optional"),
    "project.local": dict(category="boundary", arity="dir", mutability="mutable", indexed="excluded", authority="human", agent_access="read-only", link_target="none", requirement="optional"),
    "project.remote": dict(category="boundary", arity="dir", mutability="mutable", indexed="excluded", authority="human", agent_access="read-only", link_target="none", requirement="optional"),
    "project.upstream": dict(category="boundary", arity="dir", mutability="replace", indexed="excluded", authority="external", agent_access="write", link_target="none", requirement="optional"),
}

EXPECTED_POLICIES = {
    "curated": {"create": "allowed", "edit": "allowed", "rename": "allowed", "relocate": "governed", "delete": "prohibited", "retire": "via-status"},
    "append": {"create": "allowed", "edit": "additive-only", "add_child": "allowed", "modify_existing": "prohibited", "delete": "prohibited"},
    "immutable": {"create": "human-only", "edit": "prohibited", "relocate": "human-only", "delete": "human-only"},
    "replace": {"reconstruct": "allowed", "delete": "allowed"},
    "mutable": {"create": "allowed", "edit": "allowed", "rename": "allowed", "relocate": "governed", "delete": "allowed"},
    "regenerate": {"create": "generator-only", "edit": "prohibited", "rename": "prohibited", "relocate": "prohibited", "delete": "allowed", "regenerate": "allowed"},
}

EXPECTED_TRUST = {
    "project.notes": "workspace-trusted",
    "project.local": "explicit-local",
    "project.remote": "explicit-local",
    "project.upstream": "external-untrusted",
}

EXPECTED_ARCHIVE_FIELDS = [
    "source_key", "semantic_role", "boundary", "boundary_class",
    "original_binding", "archived_at", "archived_by",
]

EXPECTED_EVOLUTION = {
    "binding_change": "non-breaking",
    "description_clarification": "non-breaking",
    "key_add_remove_or_rename": "schema-version-bump",
    "key_meaning_change": "schema-version-bump",
    "axis_or_vocab_change": "schema-version-bump",
    "policy_semantics_change": "schema-version-bump",
    "authority_semantics_change": "schema-version-bump",
}

EXPECTED_CROSSWALK = {
    "llm_wiki": {"raw": "knowledge.reference", "processed": "knowledge.durable", "schema": ["workspace.schema", "agent.instructions"]},
    "code": {"capture": "context.capture", "organize": "bindings + boundaries", "distill": "knowledge.durable", "express": "output.artifact"},
    "para": {"projects": "work.project", "areas": "responsibility.area", "resources": "knowledge.reference", "archives": "lifecycle.archive"},
    "icm_mwp": {"router": "context.router", "instructions": "agent.instructions", "schema": "workspace.schema"},
}

EXPECTED_GENERATION = {
    "derived": ["paths.sh", "mkdirs.sh", "obsidian-excludes.txt", "CONTEXT.md", "SPEC.md"],
    "human_authored": ["WORKSPACE.yaml", "AGENTS.md"],
    "index_policy": {"SPEC.md": "disabled"},
}

REQUIRED_INVARIANTS = {
    "relocation", "boundary_transition", "nested_instructions", "archive_identity",
    "external_boundary_trust", "binding_precedence", "generation",
}


def validate_schema(data: dict[str, Any], root: Path = PACKAGE_ROOT) -> tuple[list[str], list[str]]:
    fails: list[str] = []
    warns: list[str] = []

    def fail(cat: str, msg: str) -> None:
        fails.append(f"[{cat}] {msg}")

    def warn(cat: str, msg: str) -> None:
        warns.append(f"[{cat}] {msg}")

    # Root-level freeze contract.
    if data.get("schema_version") != 1:
        fail("version", f"schema_version must be 1 for frozen-v1 audit, got {data.get('schema_version')!r}")
    if data.get("status") != "frozen":
        fail("version", f"status must be 'frozen', got {data.get('status')!r}")
    if "version" in data:
        fail("version", "redundant top-level 'version' is forbidden; use schema_version only")
    if data.get("identifier", {}).get("id") != "ordinal/display metadata only; never a downstream reference":
        fail("identifier", "identifier.id must explicitly be ordinal/display-only")
    if data.get("policy_defaults", {}).get("unspecified") != "prohibited":
        fail("policy", "unspecified mutation operations must default to prohibited")

    vocab = data.get("vocab")
    slots = data.get("slots")
    if not isinstance(vocab, dict):
        fail("shape", "vocab must be a mapping")
        vocab = {}
    if not isinstance(slots, list):
        fail("shape", "slots must be a list")
        slots = []

    for vf in VOCAB_FIELDS:
        if not isinstance(vocab.get(vf), list) or not vocab.get(vf):
            fail("vocab", f"vocab.{vf} must be a non-empty list")

    # Slot shape + closed vocabulary.
    by_key: dict[str, dict[str, Any]] = {}
    for idx, slot in enumerate(slots, start=1):
        if not isinstance(slot, dict):
            fail("shape", f"slot #{idx} is not a mapping")
            continue
        for field in SLOT_FIELDS:
            if field not in slot:
                fail("shape", f"slot #{idx} missing field {field!r}")
        key = slot.get("key")
        if not isinstance(key, str) or not validate_key(key):
            fail("key", f"slot #{idx}: invalid semantic key {key!r}")
            continue
        by_key[key] = slot
        for field in VOCAB_FIELDS:
            value = slot.get(field)
            if isinstance(value, bool):
                fail("coercion", f"slot {key}: {field} coerced to boolean {value}")
            allowed = vocab.get(field, [])
            if value not in allowed:
                fail("vocab", f"slot {key}: {field}={value!r} not in closed vocab {allowed}")
        binding = slot.get("binding")
        err = validate_binding_text(binding) if isinstance(binding, str) else "binding must be a string"
        if err:
            fail("binding", f"slot {key}: {err}: {binding!r}")
        elif not resolves_within(root, binding):
            fail("binding", f"slot {key}: binding escapes workspace after symlink resolution: {binding!r}")
        if slot.get("arity") == "dir" and isinstance(binding, str) and not binding.endswith("/"):
            fail("arity", f"slot {key}: dir binding must end with '/': {binding!r}")
        if slot.get("arity") == "file" and isinstance(binding, str) and binding.endswith("/"):
            fail("arity", f"slot {key}: file binding must not end with '/': {binding!r}")
        if not isinstance(slot.get("description"), str) or not slot.get("description", "").strip():
            fail("description", f"slot {key}: description must be non-empty")

    # Unique id/key/binding + ordinal ids.
    for field in ("id", "key", "binding"):
        seen: dict[Any, Any] = {}
        for slot in slots:
            if not isinstance(slot, dict) or field not in slot:
                continue
            value = slot[field]
            if value in seen:
                fail("unique", f"duplicate {field}={value!r} (slots {seen[value]} and {slot.get('id')})")
            seen[value] = slot.get("id")
    ids = [s.get("id") for s in slots if isinstance(s, dict)]
    if all(isinstance(i, int) for i in ids) and sorted(ids) != list(range(1, len(ids) + 1)):
        fail("ids", f"ids must be contiguous ordinals 1..n, got {ids}")

    # Frozen v1 slot semantics. This is deliberately exhaustive.
    actual_keys = set(by_key)
    expected_keys = set(FROZEN_V1)
    if actual_keys != expected_keys:
        missing = sorted(expected_keys - actual_keys)
        extra = sorted(actual_keys - expected_keys)
        fail("freeze", f"frozen-v1 key set changed; missing={missing}, extra={extra}")
    for key, expected in FROZEN_V1.items():
        slot = by_key.get(key)
        if not slot:
            continue
        for field, value in expected.items():
            if slot.get(field) != value:
                fail("freeze", f"{key}: frozen {field}={value!r}, got {slot.get(field)!r}")

    # Mutability contracts are semantics, not mere labels.
    policies = data.get("policy_definitions")
    if policies != EXPECTED_POLICIES:
        fail("policy", f"policy_definitions differ from frozen-v1 contract: expected {EXPECTED_POLICIES}, got {policies}")

    # Permission sanity independent of the frozen map.
    for slot in slots:
        if not isinstance(slot, dict):
            continue
        key = slot.get("key", "?")
        if slot.get("authority") == "human" and slot.get("agent_access") == "write":
            fail("matrix", f"{key}: human authority cannot grant generic agent write")
        if slot.get("authority") == "derived" and slot.get("mutability") != "regenerate":
            fail("matrix", f"{key}: derived authority requires regenerate mutability")
        if slot.get("mutability") == "immutable" and slot.get("agent_access") == "write":
            fail("matrix", f"{key}: immutable content cannot be agent-writable")

    # Graph/dependency direction.
    graph = [s.get("key") for s in slots if isinstance(s, dict) and s.get("link_target") == "graph"]
    if graph != ["knowledge.durable"]:
        fail("graph", f"durable graph root must be exactly knowledge.durable, got {graph}")
    for slot in slots:
        if not isinstance(slot, dict):
            continue
        if slot.get("link_target") == "referenceable" and slot.get("mutability") not in ("immutable", "append"):
            fail("graph", f"{slot.get('key')}: referenceable targets must be immutable/append")
        if slot.get("category") in ("state", "system") and slot.get("link_target") in ("graph", "referenceable"):
            fail("graph", f"{slot.get('key')}: operational state/system cannot enter durable graph")

    # Binding topology: nested project-class bindings under work.project are the
    # only intentional slot-to-slot nesting in frozen v1.
    paths = [(s["key"], s["binding"].rstrip("/")) for s in slots if isinstance(s, dict) and isinstance(s.get("binding"), str)]
    for (k1, p1), (k2, p2) in itertools.combinations(paths, 2):
        if p1 == p2:
            fail("binding", f"identical binding {p1!r}: {k1} and {k2}")
    for k1, p1 in paths:
        for k2, p2 in paths:
            if k1 == k2 or p1 == p2:
                continue
            if (p1 + "/").startswith(p2 + "/"):
                child = by_key.get(k1, {})
                parent = by_key.get(k2, {})
                if not (parent.get("key") == "work.project" and child.get("category") == "boundary"):
                    warn("binding", f"nested binding {p1!r} under {p2!r}: {k1} under {k2}")

    # Frozen invariants and structured security contracts.
    invariants = data.get("invariants", {})
    if set(invariants) != REQUIRED_INVARIANTS:
        fail("invariant", f"required invariant set changed: expected {sorted(REQUIRED_INVARIANTS)}, got {sorted(invariants) if isinstance(invariants, dict) else invariants}")
    archive = data.get("archive_contract", {})
    if archive.get("manifest") != ".archive.yaml" or archive.get("immutable_once_written") is not True:
        fail("archive", "archive_contract must require immutable .archive.yaml manifests")
    if archive.get("required_fields") != EXPECTED_ARCHIVE_FIELDS:
        fail("archive", f"archive manifest fields changed: expected {EXPECTED_ARCHIVE_FIELDS}, got {archive.get('required_fields')}")
    if archive.get("nullable_fields") != ["boundary_class"]:
        fail("archive", "archive_contract.nullable_fields must be exactly [boundary_class]")
    field_semantics = archive.get("field_semantics", {})
    if set(field_semantics) != set(EXPECTED_ARCHIVE_FIELDS):
        fail("archive", "archive_contract.field_semantics must document every required manifest field")
    elif any(not isinstance(v, str) or not v.strip() for v in field_semantics.values()):
        fail("archive", "archive manifest field semantics must be non-empty")
    if data.get("boundary_trust") != EXPECTED_TRUST:
        fail("trust", f"boundary_trust differs from frozen-v1 contract: {data.get('boundary_trust')}")
    trust_semantics = data.get("boundary_trust_semantics", {})
    expected_trust_values = set(EXPECTED_TRUST.values())
    if set(trust_semantics) != expected_trust_values:
        fail("trust", f"boundary_trust_semantics must cover {sorted(expected_trust_values)} exactly")
    elif any(not isinstance(v, str) or not v.strip() for v in trust_semantics.values()):
        fail("trust", "boundary trust semantics must be non-empty")
    if data.get("privileged_operations", {}).get("state.memory", {}).get("compaction") != "human-authorized":
        fail("policy", "state.memory compaction must be an explicit human-authorized privileged operation")
    if data.get("evolution_contract") != EXPECTED_EVOLUTION:
        fail("evolution", f"evolution_contract differs from frozen-v1 contract: {data.get('evolution_contract')}")

    vocab_semantics = data.get("vocab_semantics", {})
    for vocab_name in VOCAB_FIELDS:
        meanings = vocab_semantics.get(vocab_name, {})
        expected_values = set(vocab.get(vocab_name, []))
        if not isinstance(meanings, dict) or set(meanings) != expected_values:
            fail("vocab-semantics", f"vocab_semantics.{vocab_name} must cover {sorted(expected_values)} exactly")
            continue
        for value, meaning in meanings.items():
            if not isinstance(meaning, str) or not meaning.strip():
                fail("vocab-semantics", f"vocab_semantics.{vocab_name}.{value} must be non-empty")

    if data.get("generation_contract") != EXPECTED_GENERATION:
        fail("generation", f"generation_contract differs from frozen-v1 contract: {data.get('generation_contract')}")
    if data.get("crosswalk") != EXPECTED_CROSSWALK:
        fail("crosswalk", f"crosswalk differs from frozen-v1 adaptation contract: {data.get('crosswalk')}")
    if data.get("promotion", {}).get("into_human_authoritative") is None:
        fail("promotion", "human-authoritative promotion policy is required")
    if not isinstance(data.get("composition"), str) or not data.get("composition", "").strip():
        fail("composition", "boundary-class/semantic-role composition rule is required")

    return fails, warns


def run_self_test(good: dict[str, Any], root: Path) -> tuple[list[str], int]:
    """Mutation-test the frozen contract; every intentional corruption must fail."""
    failures: list[str] = []
    exhaustive_count = 0

    def must_fail(label: str, mutate) -> None:
        nonlocal exhaustive_count
        candidate = copy.deepcopy(good)
        mutate(candidate)
        exhaustive_count += 1
        found, _ = validate_schema(candidate, root)
        if not found:
            failures.append(f"self-test corruption passed: {label}")

    def slot(data: dict[str, Any], key: str) -> dict[str, Any]:
        return next(s for s in data["slots"] if s["key"] == key)

    # Exhaust every frozen semantic field by changing it to another valid vocab value.
    field_to_vocab = {
        "category": "category", "arity": "arity", "mutability": "mutability",
        "indexed": "indexed", "authority": "authority", "agent_access": "agent_access",
        "link_target": "link_target", "requirement": "requirement",
    }
    for key, expected in FROZEN_V1.items():
        for field, current in expected.items():
            alternatives = [v for v in good["vocab"][field_to_vocab[field]] if v != current]
            if not alternatives:
                continue
            alternative = alternatives[0]
            must_fail(
                f"{key}.{field}: {current!r} -> {alternative!r}",
                lambda d, k=key, f=field, v=alternative: slot(d, k).__setitem__(f, v),
            )

    # Policy semantics: every declared verb is part of the frozen meaning.
    for policy_name, policy in EXPECTED_POLICIES.items():
        for verb, current in policy.items():
            alternative = "prohibited" if current != "prohibited" else "allowed"
            must_fail(
                f"policy {policy_name}.{verb}: {current!r} -> {alternative!r}",
                lambda d, p=policy_name, v=verb, a=alternative: d["policy_definitions"][p].__setitem__(v, a),
            )

    # Structural security contracts.
    for invariant in sorted(REQUIRED_INVARIANTS):
        must_fail(f"remove invariant {invariant}", lambda d, i=invariant: d["invariants"].pop(i, None))
    for field in EXPECTED_ARCHIVE_FIELDS:
        must_fail(f"archive drops {field}", lambda d, f=field: d["archive_contract"]["required_fields"].remove(f))
    must_fail("archive boundary_class no longer nullable", lambda d: d["archive_contract"].__setitem__("nullable_fields", []))
    for vocab_name, values in good["vocab"].items():
        must_fail(f"remove vocab semantics {vocab_name}.{values[0]}", lambda d, n=vocab_name, v=values[0]: d["vocab_semantics"][n].pop(v, None))
    for key, trust in EXPECTED_TRUST.items():
        alternative = "external-untrusted" if trust != "external-untrusted" else "explicit-local"
        must_fail(f"trust {key}: {trust} -> {alternative}", lambda d, k=key, a=alternative: d["boundary_trust"].__setitem__(k, a))
    for change, treatment in EXPECTED_EVOLUTION.items():
        alternative = "non-breaking" if treatment != "non-breaking" else "schema-version-bump"
        must_fail(f"evolution {change}: {treatment} -> {alternative}", lambda d, c=change, a=alternative: d["evolution_contract"].__setitem__(c, a))
    for source, concepts in EXPECTED_CROSSWALK.items():
        for concept in concepts:
            must_fail(f"remove crosswalk {source}.{concept}", lambda d, s=source, c=concept: d["crosswalk"][s].pop(c, None))

    # Key-set and privileged/default policy protections.
    must_fail("remove frozen key", lambda d: d["slots"].pop())
    must_fail("add unknown key", lambda d: d["slots"].append({**copy.deepcopy(d["slots"][-1]), "id": 23, "key": "project.unknown", "binding": "40-projects/unknown/"}))
    must_fail("allow unspecified operations", lambda d: d["policy_defaults"].__setitem__("unspecified", "allowed"))
    must_fail("remove memory compaction gate", lambda d: d["privileged_operations"].pop("state.memory", None))
    must_fail("drop SPEC from generation contract", lambda d: d["generation_contract"]["derived"].remove("SPEC.md"))
    must_fail("index generated SPEC", lambda d: d["generation_contract"]["index_policy"].__setitem__("SPEC.md", "included"))

    return failures, exhaustive_count


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit a CCA Hybrid Workspace Profile target against the frozen-v1 contract."
    )
    parser.add_argument("--target", help="Target workspace root. Required for workspace audits; never defaults to the installed tool directory.")
    parser.add_argument("--self-test", action="store_true", help="Mutation-test the frozen contract. Without --target, self-tests the bundled template only.")
    args = parser.parse_args(argv)
    if not args.target and not args.self_test:
        parser.error("--target is required for workspace audit (or use --self-test for package contract tests)")
    return args


def resolve_audit_root(args: argparse.Namespace) -> Path:
    if not args.target:
        return PACKAGE_ROOT
    root = Path(args.target).expanduser().resolve(strict=False)
    package = PACKAGE_ROOT.resolve()
    if root == package or package in root.parents:
        raise ValueError("target must be outside the installed hybrid-workspace tool package")
    if not root.is_dir():
        raise ValueError(f"target workspace does not exist: {root}")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        root = resolve_audit_root(args)
        data = load_schema(root / "WORKSPACE.yaml")
    except (yaml.YAMLError, ValueError, OSError) as exc:
        print("=" * 72)
        print("FREEZE AUDIT — SCHEMA LOAD FAILURE")
        print("=" * 72)
        print(f"✗ {exc}")
        return 1

    fails, warns = validate_schema(data, root)
    self_test_count = 0
    if args.self_test:
        self_test_failures, self_test_count = run_self_test(data, root)
        fails.extend(f"[self-test] {msg}" for msg in self_test_failures)

    print("=" * 72)
    print(f"FREEZE AUDIT — {len(data.get('slots', []))} slots — schema v{data.get('schema_version', '?')}")
    print("=" * 72)
    if fails:
        print(f"\nFAIL ({len(fails)}):")
        for item in fails:
            print("  ✗", item)
    else:
        print("\n✓ all frozen-v1 contract checks passed")
    if warns:
        print(f"\nWARN ({len(warns)}):")
        for item in warns:
            print("  ⚠", item)
    if args.self_test and not any("[self-test]" in f for f in fails):
        print(f"✓ exhaustive frozen-field mutations rejected ({self_test_count} corruptions)")
    print()
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
