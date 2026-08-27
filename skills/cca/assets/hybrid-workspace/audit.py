#!/usr/bin/env python3
# Adversarial freeze audit for the CCA Hybrid Workspace Profile.
# v2 preserves the complete frozen-v1 slot/policy baseline and adds only the
# reference admission classification extension declared by the v1 evolution rule.
from __future__ import annotations

import argparse
import copy
from datetime import datetime
import hashlib
import itertools
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any

import yaml

from schema import load_schema, resolves_within, validate_binding_text, validate_key

PACKAGE_ROOT = Path(__file__).resolve().parent
INSTALLED_SKILL_MD = PACKAGE_ROOT.parent.parent / "SKILL.md"

CCA_SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
CCA_SKILL_VERSION_RE = re.compile(r'(?ms)^metadata:\s*$.*?^\s+version:\s*["\']([^"\']+)["\']\s*$')


def cca_semver_tuple(version: str) -> tuple[int, int, int]:
    return tuple(int(part) for part in version.split("."))  # type: ignore[return-value]


def resolve_installed_cca_version() -> str:
    """Read the installed CCA contract version from the sibling skill's SKILL.md.

    This never reads a repository commit/tree/blob identity: per
    references/core/versioning.md, CCA conformance identity is the SemVer
    contract version, not a source-control revision.
    """
    text = INSTALLED_SKILL_MD.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{INSTALLED_SKILL_MD}: SKILL.md is missing YAML frontmatter")
    frontmatter = text.split("---", 2)[1]
    match = CCA_SKILL_VERSION_RE.search(frontmatter)
    if not match:
        raise ValueError(f"{INSTALLED_SKILL_MD}: metadata.version is required")
    version = match.group(1)
    if not CCA_SEMVER_RE.fullmatch(version):
        raise ValueError(f"{INSTALLED_SKILL_MD}: metadata.version must be stable SemVer x.y.z, got {version!r}")
    return version

SLOT_FIELDS = (
    "id", "category", "key", "binding", "arity", "mutability", "indexed",
    "authority", "agent_access", "link_target", "requirement", "description",
)
VOCAB_FIELDS = (
    "category", "arity", "mutability", "indexed", "authority",
    "agent_access", "link_target", "requirement",
)

# Frozen v1 semantic/policy baseline. These 22 slots remain byte-for-meaning
# unchanged by v2 except for binding/description fields, which v1 already declared
# non-breaking/customizable.
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

# Minimal v2 key-set extension required to make source admission provenance visible
# in the filesystem without creating new knowledge roles or vocabulary axes.
FROZEN_V2_EXTENSION: dict[str, dict[str, Any]] = {
    "reference.curated": dict(category="pipeline", arity="dir", mutability="immutable", indexed="excluded", authority="human", agent_access="read-only", link_target="referenceable", requirement="required"),
    "reference.collected": dict(category="pipeline", arity="dir", mutability="append", indexed="excluded", authority="shared", agent_access="write", link_target="referenceable", requirement="required"),
}

EXPECTED_CURRENT = {**FROZEN_V1, **FROZEN_V2_EXTENSION}

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

EXPECTED_CLASSIFICATION_ROLES = {
    "project.notes": "work.project",
    "project.local": "work.project",
    "project.remote": "work.project",
    "project.upstream": "work.project",
    "reference.curated": "knowledge.reference",
    "reference.collected": "knowledge.reference",
}

EXPECTED_REFERENCE_ROUTING = {
    "unclassified_incoming": "context.capture",
    "preserved_evidence": "knowledge.reference",
    "derived_synthesis": "knowledge.durable",
    "external_deliverable": "output.artifact",
    "finite_research_effort": "work.project",
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

HASH_RE = re.compile(r"^sha256:([0-9a-fA-F]{64})$")


def _is_direct_child(parent_binding: str, child_binding: str) -> bool:
    parent = PurePosixPath(parent_binding.rstrip("/"))
    child = PurePosixPath(child_binding.rstrip("/"))
    return child.parent == parent


def _validate_reference_contract(data: dict[str, Any], by_key: dict[str, dict[str, Any]], fail) -> None:
    roles = data.get("classification_roles")
    if roles != EXPECTED_CLASSIFICATION_ROLES:
        fail("composition", f"classification_roles differ from v2 contract: {roles}")

    contract = data.get("reference_contract")
    if not isinstance(contract, dict):
        fail("reference", "reference_contract must be a mapping")
        return
    if contract.get("semantic_role") != "knowledge.reference":
        fail("reference", "reference_contract.semantic_role must be knowledge.reference")
    if contract.get("parent_key") != "knowledge.reference":
        fail("reference", "reference_contract.parent_key must be knowledge.reference")
    if contract.get("direct_parent_objects") != "prohibited":
        fail("reference", "direct objects under knowledge.reference parent must be prohibited")

    classes = contract.get("classes")
    if not isinstance(classes, dict) or set(classes) != {"reference.curated", "reference.collected"}:
        fail("reference", "reference_contract.classes must be exactly reference.curated/reference.collected")
    else:
        curated = classes["reference.curated"]
        collected = classes["reference.collected"]
        if curated.get("admission") != "human" or curated.get("agent_deposit") != "prohibited" or curated.get("existing_objects") != "immutable":
            fail("reference", "reference.curated admission policy changed")
        if collected.get("admission") != "automated" or collected.get("agent_deposit") != "add-child-only" or collected.get("existing_objects") != "immutable":
            fail("reference", "reference.collected deposit policy changed")
        if collected.get("review_changes_classification") is not False:
            fail("reference", "human review must not reclassify collected evidence")

    provenance = contract.get("collected_provenance")
    if not isinstance(provenance, dict):
        fail("reference", "collected_provenance must be a mapping")
    else:
        if provenance.get("file_sidecar_suffix") != ".source.yaml":
            fail("reference", "collected file sidecar suffix must be .source.yaml")
        if provenance.get("directory_manifest") != ".source.yaml":
            fail("reference", "collected directory manifest must be .source.yaml")
        required = provenance.get("required_fields")
        if required != ["acquired_by", "acquisition_method", "origin", "acquired_at"]:
            fail("reference", f"collected provenance required_fields changed: {required}")
        if provenance.get("identity_fields") != ["content_hash", "content_identity"]:
            fail("reference", "collected provenance identity_fields must preserve hash/identity options")
        if provenance.get("file_hash_required") is not True or provenance.get("hash_algorithm") != "sha256":
            fail("reference", "collected file identity must require SHA-256")

    if contract.get("routing") != EXPECTED_REFERENCE_ROUTING:
        fail("reference", f"reference routing differs from contract: {contract.get('routing')}")
    statement = contract.get("epistemic_statement")
    if not isinstance(statement, str) or not statement.strip():
        fail("reference", "reference epistemic statement must be non-empty")

    parent = by_key.get("knowledge.reference")
    curated_slot = by_key.get("reference.curated")
    collected_slot = by_key.get("reference.collected")
    if parent and curated_slot and collected_slot:
        for child in (curated_slot, collected_slot):
            if not _is_direct_child(parent["binding"], child["binding"]):
                fail("binding", f"{child['key']} must be a direct child binding of knowledge.reference")


def _load_provenance(path: Path, fail, label: str) -> dict[str, Any] | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        fail("provenance", f"{label}: invalid provenance metadata: {exc}")
        return None
    if not isinstance(data, dict) or not isinstance(data.get("provenance"), dict):
        fail("provenance", f"{label}: provenance metadata must contain a provenance mapping")
        return None
    return data["provenance"]


def _validate_provenance_fields(provenance: dict[str, Any], contract: dict[str, Any], fail, label: str) -> None:
    for field in contract["required_fields"]:
        value = provenance.get(field)
        if not isinstance(value, str) or not value.strip():
            fail("provenance", f"{label}: missing/non-empty provenance field {field!r}")
    timestamp = provenance.get("acquired_at")
    if isinstance(timestamp, str) and timestamp.strip():
        try:
            parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                raise ValueError("timezone required")
        except ValueError:
            fail("provenance", f"{label}: acquired_at must be RFC3339/ISO-8601 with timezone")


def _validate_reference_filesystem(data: dict[str, Any], by_key: dict[str, dict[str, Any]], root: Path, fail) -> None:
    parent_slot = by_key.get("knowledge.reference")
    curated_slot = by_key.get("reference.curated")
    collected_slot = by_key.get("reference.collected")
    if not parent_slot or not curated_slot or not collected_slot:
        return

    parent_path = root / parent_slot["binding"].rstrip("/")
    curated_path = root / curated_slot["binding"].rstrip("/")
    collected_path = root / collected_slot["binding"].rstrip("/")

    if parent_path.exists():
        allowed = {curated_path.name, collected_path.name}
        for child in parent_path.iterdir():
            if child.name not in allowed:
                fail(
                    "reference",
                    f"loose/unknown source entry {child.relative_to(root)} is prohibited; raw/reference objects must resolve through reference.curated or reference.collected",
                )
            elif not child.is_dir():
                fail("reference", f"reference admission binding {child.relative_to(root)} must be a directory")

    if not collected_path.exists():
        return
    if not collected_path.is_dir():
        fail("reference", f"reference.collected binding is not a directory: {collected_path.relative_to(root)}")
        return

    provenance_contract = data["reference_contract"]["collected_provenance"]
    suffix = provenance_contract["file_sidecar_suffix"]
    manifest_name = provenance_contract["directory_manifest"]

    entries = list(collected_path.iterdir())
    objects = [entry for entry in entries if not (entry.is_file() and entry.name.endswith(suffix))]
    object_sidecars = {
        entry.name + suffix
        for entry in objects
        if entry.is_file()
    }
    for entry in entries:
        if entry.is_file() and entry.name.endswith(suffix) and entry.name not in object_sidecars:
            fail("provenance", f"orphan provenance sidecar {entry.relative_to(root)} has no source object")

    for source in objects:
        label = str(source.relative_to(root))
        if source.is_file():
            metadata_path = source.with_name(source.name + suffix)
            if not metadata_path.is_file():
                fail("provenance", f"{label}: collected source is missing provenance sidecar {metadata_path.name}")
                continue
            provenance = _load_provenance(metadata_path, fail, label)
            if provenance is None:
                continue
            _validate_provenance_fields(provenance, provenance_contract, fail, label)
            content_hash = provenance.get("content_hash")
            if not isinstance(content_hash, str):
                fail("provenance", f"{label}: collected file requires content_hash")
                continue
            match = HASH_RE.fullmatch(content_hash)
            if not match:
                fail("provenance", f"{label}: content_hash must be sha256:<64 hex characters>")
                continue
            actual = hashlib.sha256(source.read_bytes()).hexdigest()
            if actual.lower() != match.group(1).lower():
                fail("provenance", f"{label}: content hash mismatch; existing collected source was modified or metadata is incorrect")
        elif source.is_dir():
            metadata_path = source / manifest_name
            if not metadata_path.is_file():
                fail("provenance", f"{label}: collected directory requires {manifest_name}")
                continue
            provenance = _load_provenance(metadata_path, fail, label)
            if provenance is None:
                continue
            _validate_provenance_fields(provenance, provenance_contract, fail, label)
            if not any(isinstance(provenance.get(field), str) and provenance[field].strip() for field in provenance_contract["identity_fields"]):
                fail("provenance", f"{label}: collected directory requires content_hash or content_identity")
        else:
            fail("reference", f"{label}: unsupported collected source object type")


def validate_schema(data: dict[str, Any], root: Path = PACKAGE_ROOT) -> tuple[list[str], list[str]]:
    fails: list[str] = []
    warns: list[str] = []

    def fail(cat: str, msg: str) -> None:
        fails.append(f"[{cat}] {msg}")

    def warn(cat: str, msg: str) -> None:
        warns.append(f"[{cat}] {msg}")

    if data.get("schema_version") != 2:
        fail("version", f"schema_version must be 2 for current profile audit, got {data.get('schema_version')!r}")
    if data.get("status") != "frozen":
        fail("version", f"status must be 'frozen', got {data.get('status')!r}")
    if "version" in data:
        fail("version", "redundant top-level 'version' is forbidden; use schema_version only")

    cca_contract = data.get("cca")
    if cca_contract is None:
        warn("cca-version", "workspace does not declare cca.specification; CCA contract-version compatibility cannot be checked (see references/core/versioning.md). Add `cca: {specification: \"<installed version>\"}` to WORKSPACE.yaml.")
    elif not isinstance(cca_contract, dict) or "specification" not in cca_contract:
        fail("cca-version", "cca.specification is required when a 'cca' block is present")
    else:
        declared = cca_contract["specification"]
        if not isinstance(declared, str) or not CCA_SEMVER_RE.fullmatch(declared):
            fail("cca-version", f"cca.specification must be a stable SemVer string, got {declared!r}")
        else:
            try:
                installed = resolve_installed_cca_version()
            except (OSError, ValueError) as exc:
                warn("cca-version", f"could not resolve installed CCA contract version to check against: {exc}")
            else:
                declared_t, installed_t = cca_semver_tuple(declared), cca_semver_tuple(installed)
                if declared_t[0] != installed_t[0]:
                    fail("cca-version", f"workspace targets CCA {declared} (major {declared_t[0]}) but installed CCA is {installed} (major {installed_t[0]}); a major version difference is a breaking incompatibility, not something this audit can wave through")
                elif installed_t < declared_t:
                    fail("cca-version", f"workspace targets CCA {declared} but the installed CCA is older ({installed}); upgrade the installed cca skill before this workspace can be validated against what it declares")
                # installed_t >= declared_t with the same major: compatible, no fail/warn.

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
            fail("key", f"slot #{idx}: invalid semantic/classification key {key!r}")
            continue
        by_key[key] = slot
        for field in VOCAB_FIELDS:
            value = slot.get(field)
            if isinstance(value, bool):
                fail("coercion", f"slot {key}: {field} coerced to boolean {value}")
            if value not in vocab.get(field, []):
                fail("vocab", f"slot {key}: {field}={value!r} not in closed vocab {vocab.get(field, [])}")
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

    actual_keys = set(by_key)
    expected_keys = set(EXPECTED_CURRENT)
    if actual_keys != expected_keys:
        fail("freeze", f"current key set changed; missing={sorted(expected_keys-actual_keys)}, extra={sorted(actual_keys-expected_keys)}")
    for key, expected in EXPECTED_CURRENT.items():
        slot = by_key.get(key)
        if not slot:
            continue
        for field, value in expected.items():
            if slot.get(field) != value:
                origin = "frozen-v1" if key in FROZEN_V1 else "v2-extension"
                fail("freeze", f"{key}: {origin} {field}={value!r}, got {slot.get(field)!r}")

    if data.get("policy_definitions") != EXPECTED_POLICIES:
        fail("policy", f"policy_definitions differ from frozen-v1 contract: expected {EXPECTED_POLICIES}, got {data.get('policy_definitions')}")

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

    paths = [(s["key"], s["binding"].rstrip("/")) for s in slots if isinstance(s, dict) and isinstance(s.get("binding"), str)]
    for (k1, p1), (k2, p2) in itertools.combinations(paths, 2):
        if p1 == p2:
            fail("binding", f"identical binding {p1!r}: {k1} and {k2}")
    allowed_nested = {
        ("work.project", "project.notes"),
        ("work.project", "project.local"),
        ("work.project", "project.remote"),
        ("work.project", "project.upstream"),
        ("knowledge.reference", "reference.curated"),
        ("knowledge.reference", "reference.collected"),
    }
    for child_key, child_path in paths:
        for parent_key, parent_path in paths:
            if child_key == parent_key or child_path == parent_path:
                continue
            if (child_path + "/").startswith(parent_path + "/") and (parent_key, child_key) not in allowed_nested:
                warn("binding", f"nested binding {child_path!r} under {parent_path!r}: {child_key} under {parent_key}")

    invariants = data.get("invariants", {})
    if set(invariants) != REQUIRED_INVARIANTS:
        fail("invariant", f"required invariant set changed: expected {sorted(REQUIRED_INVARIANTS)}, got {sorted(invariants) if isinstance(invariants, dict) else invariants}")
    precedence = invariants.get("binding_precedence", "") if isinstance(invariants, dict) else ""
    if "most-specific" not in precedence or "reference.curated" not in precedence or "reference.collected" not in precedence:
        fail("invariant", "binding_precedence must explicitly protect most-specific reference classification policy")

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
    if set(trust_semantics) != set(EXPECTED_TRUST.values()):
        fail("trust", f"boundary_trust_semantics must cover {sorted(set(EXPECTED_TRUST.values()))} exactly")
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
    if data.get("promotion", {}).get("into_human_authoritative") is None or data.get("promotion", {}).get("collected_deposit") is None:
        fail("promotion", "curated admission and collected deposit policies are both required")
    if not isinstance(data.get("composition"), str) or not data.get("composition", "").strip():
        fail("composition", "classification/semantic-role composition rule is required")

    _validate_reference_contract(data, by_key, fail)
    _validate_reference_filesystem(data, by_key, root, fail)

    return fails, warns


def run_self_test(good: dict[str, Any], root: Path) -> tuple[list[str], int]:
    """Mutation-test the frozen-v1 baseline plus the v2 admission extension."""
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

    field_to_vocab = {
        "category": "category", "arity": "arity", "mutability": "mutability",
        "indexed": "indexed", "authority": "authority", "agent_access": "agent_access",
        "link_target": "link_target", "requirement": "requirement",
    }
    for key, expected in EXPECTED_CURRENT.items():
        for field, current in expected.items():
            alternatives = [v for v in good["vocab"][field_to_vocab[field]] if v != current]
            if alternatives:
                must_fail(
                    f"{key}.{field}: {current!r} -> {alternatives[0]!r}",
                    lambda d, k=key, f=field, v=alternatives[0]: slot(d, k).__setitem__(f, v),
                )

    for policy_name, policy in EXPECTED_POLICIES.items():
        for verb, current in policy.items():
            alternative = "prohibited" if current != "prohibited" else "allowed"
            must_fail(
                f"policy {policy_name}.{verb}: {current!r} -> {alternative!r}",
                lambda d, p=policy_name, v=verb, a=alternative: d["policy_definitions"][p].__setitem__(v, a),
            )

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
    for classification in EXPECTED_CLASSIFICATION_ROLES:
        must_fail(f"remove classification role {classification}", lambda d, c=classification: d["classification_roles"].pop(c, None))

    must_fail("remove frozen-v1 key", lambda d: d["slots"].__delitem__(0))
    must_fail("remove v2 reference key", lambda d: d["slots"].pop())
    must_fail("add unknown key", lambda d: d["slots"].append({**copy.deepcopy(d["slots"][-1]), "id": 25, "key": "reference.unknown", "binding": "20-sources/unknown/"}))
    must_fail("allow unspecified operations", lambda d: d["policy_defaults"].__setitem__("unspecified", "allowed"))
    must_fail("remove memory compaction gate", lambda d: d["privileged_operations"].pop("state.memory", None))
    must_fail("drop SPEC from generation contract", lambda d: d["generation_contract"]["derived"].remove("SPEC.md"))
    must_fail("index generated SPEC", lambda d: d["generation_contract"]["index_policy"].__setitem__("SPEC.md", "included"))
    must_fail("allow loose parent reference objects", lambda d: d["reference_contract"].__setitem__("direct_parent_objects", "allowed"))
    must_fail("curated agent deposit", lambda d: d["reference_contract"]["classes"]["reference.curated"].__setitem__("agent_deposit", "add-child-only"))
    must_fail("collected mutable after deposit", lambda d: d["reference_contract"]["classes"]["reference.collected"].__setitem__("existing_objects", "mutable"))
    must_fail("review reclassifies collected", lambda d: d["reference_contract"]["classes"]["reference.collected"].__setitem__("review_changes_classification", True))
    must_fail("drop collected hash requirement", lambda d: d["reference_contract"]["collected_provenance"].__setitem__("file_hash_required", False))
    must_fail("route synthesis into collected", lambda d: d["reference_contract"]["routing"].__setitem__("derived_synthesis", "reference.collected"))

    return failures, exhaustive_count


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit a CCA Hybrid Workspace Profile target against the frozen-v1 baseline plus current v2 admission extension."
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
        print("PROFILE AUDIT — SCHEMA LOAD FAILURE")
        print("=" * 72)
        print(f"✗ {exc}")
        return 1

    fails, warns = validate_schema(data, root)
    self_test_count = 0
    if args.self_test:
        self_test_failures, self_test_count = run_self_test(data, root)
        fails.extend(f"[self-test] {msg}" for msg in self_test_failures)

    print("=" * 72)
    print(f"PROFILE AUDIT — {len(data.get('slots', []))} slots — schema v{data.get('schema_version', '?')}")
    print("=" * 72)
    if fails:
        print(f"\nFAIL ({len(fails)}):")
        for item in fails:
            print("  ✗", item)
    else:
        print("\n✓ frozen-v1 baseline + v2 reference-admission extension checks passed")
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
