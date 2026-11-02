#!/usr/bin/env python3
# Shared schema primitives: strict YAML loading, path validation, semantic composition,
# most-specific binding resolution, and effective permissions.
from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path, PurePosixPath
import re
from typing import Any

import yaml
from yaml.constructor import ConstructorError

KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)+$")
BINDING_RE = re.compile(r"^[A-Za-z0-9._/-]+$")


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


def load_schema(path: str | Path) -> dict[str, Any]:
    """Load WORKSPACE.yaml safely and reject duplicate keys/path escapes."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as fh:
        data = yaml.load(fh, Loader=StrictSafeLoader)
    if not isinstance(data, dict):
        raise ValueError("schema root must be a mapping")
    _validate_generated_destinations(data, p.parent.resolve())
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
