"""Configurable profile: validate shape and compose owner-defined bindings."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

PACKAGE = Path(__file__).resolve().parent


def compose(raw, root, manifest_name):
    from schema import load_manifest, validate_binding_text, resolves_within

    validator = Draft202012Validator(json.loads((PACKAGE / "workspace.schema.json").read_text(encoding="utf-8")))
    errors = sorted(validator.iter_errors(raw), key=lambda e: str(list(e.absolute_path)))
    if errors:
        raise ValueError("; ".join(f"{'.'.join(map(str, e.absolute_path)) or 'manifest'}: {e.message}" for e in errors))
    if manifest_name != "workspace.yaml":
        raise ValueError("schema v5 requires lowercase workspace.yaml")
    base = load_manifest(PACKAGE / "contracts" / "hybrid-workspace-v4.yaml")
    data = copy.deepcopy(base)
    defaults = {s["key"]: s for s in base["slots"]}
    roles = {}
    slots = []
    seen = {manifest_name.casefold()}
    # The bootstrap is implicit; all other bindings are owner-selected.
    slots.append(dict(defaults["workspace.schema"], id=1, binding=manifest_name))
    for key, spec in raw["bindings"].items():
        role, path = spec["role"], spec["path"]
        if key == "workspace.schema" or role == "workspace.schema":
            raise ValueError("workspace.schema is an implicit reserved binding")
        if role in roles and role in defaults:
            raise ValueError(f"duplicate built-in role {role}")
        if key in defaults and key != role:
            raise ValueError(f"binding key {key} is reserved for role {key}")
        roles[role] = key
        err = validate_binding_text(path)
        if err or not resolves_within(root, path):
            raise ValueError(f"bindings.{key}.path: {err or 'escapes workspace'}")
        folded = path.rstrip("/").casefold()
        if folded in seen:
            raise ValueError(f"bindings.{key}.path: duplicate destination")
        seen.add(folded)
        policy = {k: v for k, v in spec.items() if k not in {"role", "path"}}
        if role in defaults:
            slot = dict(defaults[role])
            for field, value in policy.items():
                if field in {"description", "requirement"}:
                    slot[field] = value
                elif field == "agent_access" and ("write", "read-only", "none").index(value) >= ("write", "read-only", "none").index(slot[field]):
                    slot[field] = value
                elif value != slot[field]:
                    raise ValueError(f"bindings.{key}.{field}: cannot change built-in role policy")
        else:
            required = {"category", "arity", "mutability", "indexed", "authority", "agent_access", "link_target", "requirement", "description"}
            if required - policy.keys():
                raise ValueError(f"bindings.{key}: custom role needs {sorted(required - policy.keys())}")
            slot = policy
        slot.update(key=key, binding=path, id=len(slots)+1, role=role)
        if (slot["arity"] == "dir") != path.endswith("/"):
            raise ValueError(f"bindings.{key}.path: arity does not match trailing slash")
        if slot["authority"] == "human" and slot["agent_access"] == "write" or slot["mutability"] == "immutable" and slot["agent_access"] == "write":
            raise ValueError(f"bindings.{key}: prohibited write policy")
        if slot["authority"] == "derived" and slot["mutability"] != "regenerate":
            raise ValueError(f"bindings.{key}: derived authority requires regenerate")
        if slot["link_target"] == "referenceable" and slot["mutability"] not in {"immutable", "append"}:
            raise ValueError(f"bindings.{key}: referenceable content must be preserved")
        if slot["category"] in {"state", "system", "asset"} and slot["link_target"] in {"graph", "referenceable"}:
            raise ValueError(f"bindings.{key}: operational content cannot enter durable graph")
        slots.append(slot)
    by_role = {s.get("role", s["key"]): s for s in slots}
    refs = {"knowledge.reference", "reference.curated", "reference.collected"}
    if refs & by_role.keys() and not refs <= by_role.keys():
        raise ValueError("reference capability requires knowledge.reference, reference.curated and reference.collected together")
    for role in ("reference.curated", "reference.collected"):
        if role in by_role:
            parent = Path(by_role["knowledge.reference"]["binding"])
            if Path(by_role[role]["binding"]).parent != parent:
                raise ValueError(f"{role} must be a direct child of knowledge.reference")
    for child in slots:
        for parent in slots:
            if child is parent:
                continue
            a, b = Path(child["binding"].casefold()), Path(parent["binding"].casefold())
            if b in a.parents and (parent["arity"] == "file" or (parent["mutability"] in {"immutable", "append"} and child.get("role") not in {"reference.curated", "reference.collected"})):
                raise ValueError(f"binding {child['key']} cannot nest beneath protected {parent['key']}")
    data.update(schema_version=5, status="configurable", cca=raw["cca"], slots=slots)
    if "identity" in raw:
        data["identity"] = raw["identity"]
    data["classification_roles"] = {s["key"]: base["classification_roles"].get(s.get("role"), s.get("role", s["key"])) for s in slots}
    data["privileged_operations"] = {roles[k]: v for k, v in base["privileged_operations"].items() if k in roles}
    data["boundary_trust"] = {roles[k]: v for k, v in base["boundary_trust"].items() if k in roles}
    data["evolution_contract"]["key_add_remove_or_rename"] = "workspace-local"
    outputs = raw.get("generation", {}).get("outputs", {})
    by_key = {s["key"]: s for s in slots}
    destinations = set()
    for name, spec in outputs.items():
        owner = by_key.get(spec["slot"])
        if not owner or owner["category"] not in {"system", "control"} or owner["authority"] not in {"derived", "shared"} or owner["agent_access"] != "write":
            raise ValueError(f"generation.outputs.{name}: requires writable derived/shared tooling binding")
        file = spec.get("file")
        if owner["arity"] == "dir":
            if not file or validate_binding_text(file) or "/" in file:
                raise ValueError(f"generation.outputs.{name}: requires a safe filename")
            dest = owner["binding"] + file
        else:
            if file is not None or owner["mutability"] != "regenerate":
                raise ValueError(f"generation.outputs.{name}: requires generated file binding")
            dest = owner["binding"]
        if not resolves_within(root, dest) or (root / dest).is_symlink():
            raise ValueError(f"generation.outputs.{name}: unsafe destination")
        if dest.casefold() in destinations or any(s is not owner and (dest.casefold() == s["binding"].rstrip("/").casefold() or s["arity"] == "dir" and Path(s["binding"].casefold()) in Path(dest.casefold()).parents and Path(owner["binding"].casefold()) in Path(s["binding"].casefold()).parents) for s in slots):
            raise ValueError(f"generation.outputs.{name}: destination collision")
        if spec["renderer"] in {"paths", "mkdirs"} and Path(dest).suffix.lower() not in {".py", ".sh"}:
            raise ValueError(f"generation.outputs.{name}: helper must end in .py or .sh")
        destinations.add(dest.casefold())
    data["generation_contract"] = {"outputs": outputs, "human_authored": ["workspace.schema"] + [s["key"] for s in slots if s.get("role") == "agent.instructions"], "index_policy": {k: v.get("indexed", "disabled") for k,v in outputs.items()}}
    aliases = raw.get("provenance_aliases", {})
    prov = data["reference_contract"]["provenance"]
    if set(aliases) - set(prov["required_fields"]):
        raise ValueError("unknown provenance alias")
    prov["representations"]["markdown_frontmatter"]["field_aliases"] = aliases
    return data


def migrate(data):
    """Convert legacy effective data without moving any content."""
    bindings = {}
    for slot in data["slots"]:
        key = slot["key"]
        if key == "workspace.schema":
            continue
        bindings[key] = {"role": key, "path": slot["binding"], **{k: v for k,v in slot.items() if k not in {"id","key","binding"}}}
    outputs = {}
    for name, spec in data["generation_contract"]["outputs"].items():
        outputs[name] = dict(spec, renderer="context" if name == "context.router" else name)
    result = {"schema_version": 5, "cca": {"specification": "1.6.0"}, "bindings": bindings, "generation": {"outputs": outputs}}
    if "identity" in data:
        result["identity"] = data["identity"]
    aliases = data["reference_contract"]["provenance"]["representations"]["markdown_frontmatter"].get("field_aliases")
    if aliases:
        result["provenance_aliases"] = aliases
    return result
