#!/usr/bin/env python3
# Shared schema primitives: strict YAML loading, path validation, and effective permissions.
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
    if any(part in (".", "..") for part in p.parts):
        return "binding may not contain . or .. path segments"
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

    destinations: list[str] = []
    for entry in data.get("generation_contract", {}).get("derived", []):
        # `CONTEXT.md` is the frozen-v1 legacy/default declaration. Newer
        # contracts may name the semantic role directly. In both cases the
        # current context.router binding is the actual output destination.
        if entry in {"CONTEXT.md", "context.router"} and isinstance(router_binding, str):
            destinations.append(router_binding)
        elif isinstance(entry, str):
            destinations.append(entry)
    return destinations


def _validate_generated_destinations(data: Mapping[str, Any], root: Path) -> None:
    """Reject generated outputs whose text or existing symlinks escape the target."""
    for destination in _generated_destinations(data):
        error = validate_binding_text(destination)
        if error:
            raise ValueError(f"generated artifact binding {destination!r}: {error}")
        if not resolves_within(root, destination):
            raise ValueError(f"generated artifact {destination!r} escapes workspace via symlink/path resolution")


def load_schema(path: str | Path) -> dict[str, Any]:
    """Load WORKSPACE.yaml safely and reject duplicate keys/path escapes."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as fh:
        data = yaml.load(fh, Loader=StrictSafeLoader)
    if not isinstance(data, dict):
        raise ValueError("schema root must be a mapping")
    _validate_generated_destinations(data, p.parent.resolve())
    return data


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

    # Derived artifacts are generator-controlled even though an agent/tool may
    # perform regeneration. Never flatten them to generic write.
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
