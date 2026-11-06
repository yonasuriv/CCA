#!/usr/bin/env python3
# Resolve CCA workspace bindings and generated outputs from one canonical manifest.
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml

from schema import V3_FAMILY, contract_fingerprint, generated_outputs, load_manifest, load_schema, minimize_manifest, resolves_within, validate_binding_text, workspace_schema_path


def resolve(root: str | Path, *, key: str | None = None, output: str | None = None) -> tuple[str, Path]:
    """Return (workspace-relative binding, absolute target) without scanning content.

    Consumers use stable semantic keys. A schema change is loaded on each call,
    so there is no cache, hardcoded binding table, or expected file hash.
    """
    if (key is None) == (output is None):
        raise ValueError("provide exactly one semantic --key or generated --output")
    workspace = Path(root).expanduser().resolve()
    manifest = workspace_schema_path(workspace)
    data = load_schema(manifest)
    version = data.get("schema_version")
    if version not in (2, 3, 4) or isinstance(version, bool):
        raise ValueError(f"unsupported workspace schema version: {version!r}")
    if manifest.name == "workspace.yaml" and version not in V3_FAMILY:
        raise ValueError("lowercase workspace.yaml is supported for schema v3 and v4; v2 uses WORKSPACE.yaml")
    slots = data.get("slots")
    if not isinstance(slots, list):
        raise ValueError("slots must be a list")
    bindings: dict[str, dict] = {}
    for slot in slots:
        if not isinstance(slot, dict) or not isinstance(slot.get("key"), str):
            raise ValueError("every slot must declare a string key")
        name = slot["key"]
        if name in bindings:
            raise ValueError(f"duplicate semantic slot: {name}")
        bindings[name] = slot
    schema_slot = bindings.get("workspace.schema")
    if not schema_slot or schema_slot.get("binding") != manifest.name:
        raise ValueError(f"workspace.schema must point to {manifest.name}")

    if key is not None:
        if key not in bindings:
            raise KeyError(f"unknown workspace semantic key: {key}")
        binding = bindings[key].get("binding")
    else:
        if version not in V3_FAMILY:
            raise ValueError("generated output lookup requires schema v3 or v4")
        outputs = generated_outputs(data)
        if output not in outputs:
            raise KeyError(f"unknown generated output: {output}")
        binding = outputs[output]

    error = validate_binding_text(binding)
    if error or not resolves_within(workspace, binding):
        raise ValueError(f"invalid or escaping binding for {key or output}: {error or binding!r}")
    return binding, workspace / binding.rstrip("/")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resolve a semantic CCA binding without duplicating paths.")
    parser.add_argument("--target", help="Workspace root containing the sole bootstrap manifest")
    name = parser.add_mutually_exclusive_group(required=True)
    name.add_argument("--key", help="Semantic slot key, e.g. knowledge.durable")
    name.add_argument("--output", help="Generated output key, e.g. paths")
    name.add_argument("--contract-fingerprint", metavar="PROFILE@VERSION",
                      help="print the fingerprint a minimal manifest pins, e.g. hybrid-workspace@3")
    name.add_argument("--minimize", action="store_true",
                      help="print the target's full manifest as an equivalent minimal (extends) manifest")
    parser.add_argument("--format", choices=("absolute", "relative", "json"), default="absolute")
    args = parser.parse_args(argv)
    if args.contract_fingerprint:
        profile, _, version = args.contract_fingerprint.partition("@")
        try:
            print(contract_fingerprint(profile, int(version)))
        except ValueError as exc:
            print(f"CCA contract lookup failed: {exc}", file=sys.stderr)
            return 1
        return 0
    if not args.target:
        parser.error("--target is required")
    if args.minimize:
        try:
            manifest = workspace_schema_path(Path(args.target).expanduser().resolve())
            full = load_manifest(manifest)
            if "extends" in full:
                raise ValueError("manifest is already minimal")
            print(yaml.safe_dump(minimize_manifest(full, manifest.name), sort_keys=False, allow_unicode=True, width=1000), end="")
        except (OSError, ValueError, KeyError) as exc:
            print(f"CCA manifest minimization failed: {exc}", file=sys.stderr)
            return 1
        return 0
    try:
        relative, absolute = resolve(args.target, key=args.key, output=args.output)
    except (OSError, ValueError, KeyError) as exc:
        print(f"CCA binding resolution failed: {exc}", file=sys.stderr)
        return 1
    if args.format == "json":
        print(json.dumps({"key": args.key or args.output, "relative": relative, "absolute": str(absolute)}))
    else:
        print(relative if args.format == "relative" else absolute)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
