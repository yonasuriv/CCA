#!/usr/bin/env python3
# Shared schema primitives: strict YAML loading, path validation, semantic composition,
# most-specific binding resolution, and effective permissions.
from __future__ import annotations

from collections.abc import Mapping
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any

import yaml
from yaml.constructor import ConstructorError

KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)+$")
BINDING_RE = re.compile(r"^[A-Za-z0-9._/-]+$")
FINGERPRINT_RE = re.compile(r"^[0-9a-f]{64}$")
PACKAGE_ROOT = Path(__file__).resolve().parent

# One canonical form of a parsed manifest, shared by the generator, generated
# helpers, and contract pinning: deterministic for sets and mixed-type keys,
# independent of comments, whitespace, key order, and YAML spelling.
CANONICAL_SOURCE = (
    "def _c(o):\n"
    " if isinstance(o,bool) or o is None or isinstance(o,(int,float,str)): return o\n"
    " if isinstance(o,dict): return ['m',sorted([[_c(k),_c(v)] for k,v in o.items()],key=lambda kv: json.dumps(kv[0],sort_keys=True))]\n"
    " if isinstance(o,(list,tuple)): return ['l',[_c(x) for x in o]]\n"
    " if isinstance(o,(set,frozenset)): return ['s',sorted([_c(x) for x in o],key=lambda x: json.dumps(x,sort_keys=True))]\n"
    " return ['o',type(o).__name__,str(o)]\n"
    "def fingerprint(d): return hashlib.sha256(json.dumps(_c(d),separators=(',',':'),ensure_ascii=True).encode('utf-8')).hexdigest()\n"
)
_canonical_ns: dict[str, Any] = {"json": json, "hashlib": hashlib}
exec(CANONICAL_SOURCE, _canonical_ns)  # noqa: S102 - fixed, package-owned source
semantic_fingerprint = _canonical_ns["fingerprint"]

# Minimal manifests (`extends`) compose with a profile contract shipped inside
# this package. Only these top-level keys are accepted; anything else fails
# closed so a manifest cannot smuggle in policy, vocab, or slot changes.
EXTENDS_PROFILES = {("hybrid-workspace", 3): PACKAGE_ROOT / "contracts" / "hybrid-workspace-v3.yaml"}
EXTENDS_KEYS = {"extends", "cca", "identity", "bindings", "provenance_aliases", "narrow"}
# Ordered from widest to narrowest; a manifest may only move a slot rightwards.
AGENT_ACCESS_ORDER = ("write", "read-only", "none")
MINIMAL_MANIFEST_SINCE = (1, 4, 0)


class StrictSafeLoader(yaml.SafeLoader):
    """SafeLoader variant that rejects duplicate mapping keys."""


def _construct_unique_mapping(loader: StrictSafeLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found unhashable key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


StrictSafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def validate_key(key: str) -> bool:
    return bool(KEY_RE.fullmatch(key))


def validate_binding_text(binding: str) -> str | None:
    """Return an error string for unsafe/non-portable binding text, else None."""
    if not isinstance(binding, str) or not binding:
        return "binding must be a non-empty string"
    if "\x00" in binding or "\n" in binding or "\r" in binding:
        return "binding contains control characters"
    if not BINDING_RE.fullmatch(binding):
        return "binding contains unsupported characters"
    p = PurePosixPath(binding.rstrip("/"))
    if p.is_absolute():
        return "binding must be workspace-relative"
    # Inspect the raw segments: PurePosixPath silently drops "." segments, which
    # would let "./" or "a/./b" alias the workspace root or another binding.
    raw_segments = binding.rstrip("/").split("/")
    if any(part in ("", ".", "..") for part in raw_segments):
        return "binding may not contain empty, . or .. path segments"
    return None


def resolves_within(root: str | Path, binding: str) -> bool:
    """Resolve existing symlink parents and ensure the binding stays inside root."""
    root_path = Path(root).resolve()
    target = (root_path / binding.rstrip("/")).resolve(strict=False)
    try:
        target.relative_to(root_path)
    except ValueError:
        return False
    return True


def _generated_destinations(data: Mapping[str, Any]) -> list[str]:
    """Resolve declared generated outputs to concrete target-local destinations."""
    slots = {
        slot.get("key"): slot
        for slot in data.get("slots", [])
        if isinstance(slot, Mapping) and isinstance(slot.get("key"), str)
    }
    router = slots.get("context.router", {})
    router_binding = router.get("binding") if isinstance(router, Mapping) else None

    outputs = data.get("generation_contract", {}).get("outputs")
    if isinstance(outputs, Mapping):
        # Schema v3: every output resolves through a declared slot binding.
        return list(generated_outputs(data).values())

    destinations: list[str] = []
    for entry in data.get("generation_contract", {}).get("derived", []):
        # `CONTEXT.md` is the historical/default declaration. Newer contracts
        # may name the semantic role directly. In both cases the current
        # context.router binding is the actual output destination.
        if entry in {"CONTEXT.md", "context.router"} and isinstance(router_binding, str):
            destinations.append(router_binding)
        elif isinstance(entry, str):
            destinations.append(entry)
    return destinations


def generated_outputs(data: Mapping[str, Any]) -> dict[str, str]:
    """Resolve schema-v3 generation_contract.outputs to target-relative files.

    `{slot: <file key>}` uses that file binding; `{slot: <dir key>, file: <name>}`
    places a single filename segment inside that directory binding. Unknown
    slots or unsafe names raise ValueError; nothing defaults to the target root.
    """
    slots = {
        slot.get("key"): slot
        for slot in data.get("slots", [])
        if isinstance(slot, Mapping) and isinstance(slot.get("key"), str)
    }
    resolved: dict[str, str] = {}
    outputs = data.get("generation_contract", {}).get("outputs", {})
    if not isinstance(outputs, Mapping):
        raise ValueError("generation_contract.outputs must be a mapping")
    for name, spec in outputs.items():
        if not isinstance(spec, Mapping) or not isinstance(spec.get("slot"), str):
            raise ValueError(f"generated output {name!r} must name a slot")
        slot = slots.get(spec["slot"])
        if not isinstance(slot, Mapping) or not isinstance(slot.get("binding"), str):
            raise ValueError(f"generated output {name!r} references undeclared slot {spec['slot']!r}")
        binding = slot["binding"]
        file_name = spec.get("file")
        if file_name is None:
            if slot.get("arity") != "file":
                raise ValueError(f"generated output {name!r} needs a file name inside directory slot {spec['slot']!r}")
            resolved[str(name)] = binding
            continue
        if not isinstance(file_name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", file_name):
            raise ValueError(f"generated output {name!r} file must be one safe filename segment, got {file_name!r}")
        if slot.get("arity") != "dir":
            raise ValueError(f"generated output {name!r} file requires a directory slot")
        resolved[str(name)] = binding.rstrip("/") + "/" + file_name
    return resolved


def _validate_generated_destinations(data: Mapping[str, Any], root: Path) -> None:
    """Reject generated outputs whose text or existing symlinks escape the target."""
    for destination in _generated_destinations(data):
        error = validate_binding_text(destination)
        if error:
            raise ValueError(f"generated artifact binding {destination!r}: {error}")
        if not resolves_within(root, destination):
            raise ValueError(f"generated artifact {destination!r} escapes workspace via symlink/path resolution")


def workspace_schema_path(root: str | Path) -> Path:
    """Discover the single bootstrap manifest without guessing its capitalization.

    New v3 workspaces use workspace.yaml; existing uppercase workspaces remain
    supported. Reject duplicate case variants, including on case-insensitive
    filesystems where listing exposes one spelling.
    """
    directory = Path(root)
    if not directory.is_dir():
        raise ValueError(f"workspace root does not exist: {directory}")
    entries = [entry for entry in directory.iterdir() if entry.name.casefold() == "workspace.yaml"]
    if len(entries) != 1 or entries[0].name not in {"workspace.yaml", "WORKSPACE.yaml"}:
        raise ValueError(
            f"expected exactly one workspace.yaml or WORKSPACE.yaml in {directory}; "
            f"found {[entry.name for entry in entries]}"
        )
    path = entries[0]
    if not path.is_file() or path.is_symlink() or not resolves_within(directory, path.name):
        raise ValueError(f"workspace manifest must be a regular file inside {directory}: {path}")
    return path


def load_manifest(path: str | Path) -> dict[str, Any]:
    """Load the raw bootstrap manifest strictly, without composing a profile."""
    with Path(path).open("r", encoding="utf-8") as fh:
        data = yaml.load(fh, Loader=StrictSafeLoader)
    if not isinstance(data, dict):
        raise ValueError("schema root must be a mapping")
    return data


def load_schema(path: str | Path) -> dict[str, Any]:
    """Load the effective workspace schema safely and reject duplicate keys/path escapes.

    A full manifest is returned as written. A minimal manifest (`extends`) is
    composed with its pinned profile contract into the same full shape, so every
    consumer sees one schema regardless of how the workspace serialized it.
    """
    p = Path(path)
    data = load_manifest(p)
    if "extends" in data:
        data = compose_manifest(data, p.name)
    _validate_generated_destinations(data, p.parent.resolve())
    return data


def contract_path(profile: str, schema_version: int) -> Path:
    """Locate a bundled profile contract by name and schema version."""
    try:
        return EXTENDS_PROFILES[(profile, schema_version)]
    except KeyError:
        known = ", ".join(f"{name}@{version}" for name, version in sorted(EXTENDS_PROFILES))
        raise ValueError(f"unknown profile contract {profile}@{schema_version!r}; this CCA ships: {known}") from None


def _pinned_fingerprint(contract: Mapping[str, Any]) -> str:
    """Semantic fingerprint of a contract file as parsed."""
    return semantic_fingerprint(contract)


def normalize_prose(value: Any) -> Any:
    """Collapse whitespace in every string, so folded and single-line prose compare equal."""
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, Mapping):
        return {key: normalize_prose(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_prose(item) for item in value]
    return value


def contract_fingerprint(profile: str, schema_version: int) -> str:
    """Semantic fingerprint a minimal manifest pins in extends.fingerprint."""
    return _pinned_fingerprint(load_manifest(contract_path(profile, schema_version)))


def compose_manifest(manifest: Mapping[str, Any], manifest_name: str) -> dict[str, Any]:
    """Compose a minimal manifest with its pinned contract into a full schema.

    The contract supplies every semantic: vocab, slots, policies and invariants,
    but no paths. The manifest binds every slot, declares identity and the
    targeted CCA version, aliases provenance fields, and may narrow agent access.
    It can never widen authority or add, remove, or redefine keys. Slot ids are
    display ordinals assigned in contract order.
    """
    unknown = set(manifest) - EXTENDS_KEYS
    if unknown:
        raise ValueError(f"minimal manifest keys not allowed: {sorted(unknown)}; allowed: {sorted(EXTENDS_KEYS)}")

    extends = manifest.get("extends")
    if not isinstance(extends, Mapping) or set(extends) != {"profile", "schema_version", "fingerprint"}:
        raise ValueError("extends must declare exactly profile, schema_version and fingerprint")
    profile, version, pinned = extends["profile"], extends["schema_version"], extends["fingerprint"]
    if not isinstance(profile, str) or not isinstance(version, int) or isinstance(version, bool):
        raise ValueError("extends.profile must be a string and extends.schema_version an integer")
    if not isinstance(pinned, str) or not FINGERPRINT_RE.fullmatch(pinned):
        raise ValueError("extends.fingerprint must be a lowercase 64-character SHA-256 hex digest")

    contract = load_manifest(contract_path(profile, version))
    actual = _pinned_fingerprint(contract)
    if actual != pinned:
        # Fail closed: a contract change is reviewed by the owner, never adopted silently.
        raise ValueError(
            f"pinned {profile}@{version} contract fingerprint {pinned} does not match the installed contract {actual}; "
            "review the contract change, then update extends.fingerprint"
        )
    data = copy.deepcopy(contract)
    for ordinal, slot in enumerate(data["slots"], start=1):
        slot["id"] = ordinal
    slots = {slot["key"]: slot for slot in data["slots"]}

    # Minimal manifests first exist in CCA 1.4.0; an older declared target could not read this file.
    cca = manifest.get("cca")
    declared = cca.get("specification") if isinstance(cca, Mapping) else None
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", declared) if isinstance(declared, str) else None
    if not match or tuple(int(part) for part in match.groups()) < MINIMAL_MANIFEST_SINCE:
        raise ValueError(f"a minimal manifest must declare cca.specification >= {'.'.join(map(str, MINIMAL_MANIFEST_SINCE))}, got {declared!r}")
    data["cca"] = copy.deepcopy(dict(cca))
    data.pop("identity", None)
    if "identity" in manifest:
        data["identity"] = copy.deepcopy(manifest["identity"])

    bindings = manifest.get("bindings", {})
    if not isinstance(bindings, Mapping):
        raise ValueError("bindings must map semantic keys to workspace-relative paths")
    for key, binding in bindings.items():
        if key not in slots:
            raise ValueError(f"bindings.{key}: not a key of {profile}@{version}")
        if key == "workspace.schema" and binding != manifest_name:
            raise ValueError(f"bindings.workspace.schema must be the manifest itself ({manifest_name}), got {binding!r}")
        error = validate_binding_text(binding) if isinstance(binding, str) else "binding must be a string"
        if error:
            raise ValueError(f"bindings.{key}: {error}: {binding!r}")
        slots[key]["binding"] = binding
    # The bootstrap slot always names the file that was actually loaded.
    slots["workspace.schema"]["binding"] = manifest_name
    unbound = [key for key, slot in slots.items() if "binding" not in slot]
    if unbound:
        raise ValueError(f"bindings missing for {unbound}; a minimal manifest binds every slot of {profile}@{version}")

    aliases = manifest.get("provenance_aliases", {})
    if not isinstance(aliases, Mapping):
        raise ValueError("provenance_aliases must map canonical provenance fields to frontmatter names")
    provenance = data["reference_contract"]["provenance"]
    canonical = set(provenance.get("required_fields", [])) | set(provenance.get("optional_fields", []))
    for field, alias in aliases.items():
        if field not in canonical:
            raise ValueError(f"provenance_aliases.{field}: not a canonical provenance field")
        if not isinstance(alias, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", alias):
            raise ValueError(f"provenance_aliases.{field}: alias must be a plain frontmatter field name")
    if aliases:
        markdown = provenance["representations"]["markdown_frontmatter"]
        markdown["field_aliases"] = {**(markdown.get("field_aliases") or {}), **dict(aliases)}

    narrow = manifest.get("narrow", {})
    if not isinstance(narrow, Mapping) or set(narrow) - {"agent_access"}:
        raise ValueError("narrow may only contain agent_access")
    access = narrow.get("agent_access", {})
    if not isinstance(access, Mapping):
        raise ValueError("narrow.agent_access must map semantic keys to an access level")
    for key, level in access.items():
        if key not in slots:
            raise ValueError(f"narrow.agent_access.{key}: not a key of {profile}@{version}")
        if level not in AGENT_ACCESS_ORDER:
            raise ValueError(f"narrow.agent_access.{key}: {level!r} not in {list(AGENT_ACCESS_ORDER)}")
        current = slots[key]["agent_access"]
        if AGENT_ACCESS_ORDER.index(level) < AGENT_ACCESS_ORDER.index(current):
            raise ValueError(f"narrow.agent_access.{key}: {level!r} would widen the contract's {current!r}")
        slots[key]["agent_access"] = level
    # Re-insert binding after key so the composed slot reads like a full manifest slot.
    data["slots"] = [
        {"id": slot["id"], "key": slot["key"], "binding": slot["binding"],
         **{field: value for field, value in slot.items() if field not in ("id", "key", "binding")}}
        for slot in data["slots"]
    ]
    return data


def semantic_role_for_slot(slot: Mapping[str, Any], schema: Mapping[str, Any]) -> str:
    """Return the semantic role after composing any classification key."""
    key = slot.get("key")
    if not isinstance(key, str):
        raise ValueError("slot key must be a string")
    mapping = schema.get("classification_roles", {})
    if isinstance(mapping, Mapping):
        role = mapping.get(key)
        if isinstance(role, str):
            return role
    return key


def resolve_slot_for_path(path: str, schema: Mapping[str, Any]) -> Mapping[str, Any]:
    """Resolve filesystem policy from the most-specific matching binding.

    Semantic composition is separate: callers use semantic_role_for_slot() to
    recover the role when the winning slot is a classification such as
    reference.collected or project.remote.
    """
    error = validate_binding_text(path)
    if error:
        raise ValueError(f"invalid workspace-relative path {path!r}: {error}")
    target = PurePosixPath(path.rstrip("/"))
    matches: list[tuple[int, Mapping[str, Any]]] = []
    for slot in schema.get("slots", []):
        if not isinstance(slot, Mapping):
            continue
        binding = slot.get("binding")
        arity = slot.get("arity")
        if not isinstance(binding, str):
            continue
        bound = PurePosixPath(binding.rstrip("/"))
        if arity == "file":
            matched = target == bound
        else:
            matched = target == bound or bound in target.parents
        if matched:
            matches.append((len(bound.parts), slot))
    if not matches:
        raise KeyError(f"no declared binding matches {path!r}")
    matches.sort(key=lambda item: item[0], reverse=True)
    return matches[0][1]


def effective_agent_operations(slot: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    """Resolve user-facing agent operations from policy intersection.

    This is descriptive, not an authorization primitive. Runtime tools must still
    enforce boundary/relocation checks at operation time.
    """
    access = slot["agent_access"]
    if access == "none":
        return []
    if access == "read-only" or slot["authority"] == "human":
        return ["read"]

    policy = schema["policy_definitions"][slot["mutability"]]
    ops: list[str] = ["read"]

    if slot["authority"] == "derived":
        if policy.get("regenerate") == "allowed":
            ops.append("regenerate")
        return ops

    if policy.get("create") == "allowed":
        ops.append("create")
    if policy.get("edit") == "allowed":
        ops.append("edit")
    elif policy.get("edit") == "additive-only":
        ops.append("append")
    if policy.get("add_child") == "allowed":
        ops.append("add-child")
    if policy.get("rename") == "allowed":
        ops.append("rename")
    if policy.get("relocate") in ("allowed", "governed"):
        ops.append("relocate")
    if policy.get("reconstruct") == "allowed":
        ops.append("reconstruct")
    if policy.get("delete") == "allowed":
        ops.append("delete")
    if isinstance(policy.get("retire"), str) and policy["retire"].startswith("via-"):
        ops.append("retire")
    if policy.get("regenerate") == "allowed":
        ops.append("regenerate")

    privileged = schema.get("privileged_operations", {}).get(slot["key"], {})
    for op, gate in privileged.items():
        if gate == "human-authorized":
            ops.append(f"{op} (human-authorized)")

    return ops


def compact_ops(ops: list[str]) -> str:
    return ", ".join(ops) if ops else "—"


def minimize_manifest(full: Mapping[str, Any], manifest_name: str, profile: str = "hybrid-workspace") -> dict[str, Any]:
    """Express a full manifest as a minimal one, or explain why it cannot be.

    The result keeps only bindings that differ from the contract defaults, plus
    identity, cca, provenance aliases and access narrowing. It is accepted only
    if composing it reproduces the full manifest exactly, so no semantic is lost.
    """
    version = full.get("schema_version")
    contract = load_manifest(contract_path(profile, version))
    contract_slots = {slot["key"]: slot for slot in contract["slots"]}
    minimal: dict[str, Any] = {
        "extends": {"profile": profile, "schema_version": version, "fingerprint": _pinned_fingerprint(contract)},
    }
    declared = (full.get("cca") or {}).get("specification")
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", declared) if isinstance(declared, str) else None
    floor = ".".join(map(str, MINIMAL_MANIFEST_SINCE))
    keep = match and tuple(int(part) for part in match.groups()) >= MINIMAL_MANIFEST_SINCE
    minimal["cca"] = {"specification": declared if keep else floor}
    if full.get("identity") is not None:
        minimal["identity"] = copy.deepcopy(full["identity"])
    bindings: dict[str, str] = {}
    access: dict[str, str] = {}
    for slot in full.get("slots", []):
        declared = contract_slots.get(slot.get("key"))
        if declared is None:
            raise ValueError(f"slot {slot.get('key')!r} is not part of {profile}@{version}; it cannot be expressed minimally")
        if slot["key"] != "workspace.schema":
            bindings[slot["key"]] = slot["binding"]
        if slot.get("agent_access") != declared.get("agent_access"):
            access[slot["key"]] = slot["agent_access"]
    if bindings:
        minimal["bindings"] = bindings
    aliases = (full.get("reference_contract", {}).get("provenance", {}).get("representations", {})
               .get("markdown_frontmatter", {}).get("field_aliases")) or {}
    contract_aliases = (contract["reference_contract"]["provenance"]["representations"]
                        ["markdown_frontmatter"].get("field_aliases")) or {}
    extra_aliases = {k: v for k, v in aliases.items() if contract_aliases.get(k) != v}
    if extra_aliases:
        minimal["provenance_aliases"] = extra_aliases
    if access:
        minimal["narrow"] = {"agent_access": access}
    composed = normalize_prose(compose_manifest(minimal, manifest_name))
    expected = normalize_prose(copy.deepcopy(dict(full)))
    expected["cca"] = composed["cca"]  # the only intended difference: the version that can read the result
    if expected != composed:
        differing = sorted(k for k in set(expected) | set(composed) if expected.get(k) != composed.get(k))
        raise ValueError(f"manifest diverges from {profile}@{version} beyond what a minimal manifest can express: {differing}")
    return minimal
