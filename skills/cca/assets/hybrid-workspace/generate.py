#!/usr/bin/env python3
# Generate and verify all derived workspace artifacts from WORKSPACE.yaml.
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shlex
import subprocess
import sys
from typing import Any

import yaml

from schema import compact_ops, effective_agent_operations, generated_outputs, load_schema, resolves_within, semantic_role_for_slot, validate_binding_text, workspace_schema_path

PACKAGE_ROOT = Path(__file__).resolve().parent
TEMPLATE_SCHEMA = PACKAGE_ROOT / "WORKSPACE.yaml"
TEMPLATE_AGENTS = PACKAGE_ROOT / "AGENTS.md"


# One canonical form of the parsed manifest, used verbatim by the generator and
# by generated helpers at runtime: deterministic for sets and mixed-type keys,
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


def manifest_name(data: dict[str, Any]) -> str:
    return data.get("_schema_name", "WORKSPACE.yaml")


def schema(target: Path) -> dict[str, Any]:
    manifest = workspace_schema_path(target)
    data = load_schema(manifest)
    if manifest.name == "workspace.yaml" and data.get("schema_version") != 3:
        raise ValueError("lowercase workspace.yaml is a schema v3 bootstrap; schema v2 workspaces use WORKSPACE.yaml")
    if data.get("schema_version") == 3:
        # Hash parsed semantics, not raw YAML bytes or comments.
        data["_semantic_fingerprint"] = semantic_fingerprint(data)
    data["_schema_name"] = manifest.name
    return data


def resolve_target(raw: str, *, init: bool) -> Path:
    target = Path(raw).expanduser().resolve(strict=False)
    package = PACKAGE_ROOT.resolve()
    if target == package or package in target.parents:
        raise ValueError("target must be outside the installed hybrid-workspace tool package")
    if init:
        target.mkdir(parents=True, exist_ok=True)
    elif not target.is_dir():
        raise ValueError(f"target workspace does not exist: {target}")
    return target


def initialize_target(target: Path) -> list[str]:
    """Scaffold the bootstrap and declared human control file without overwrites."""
    created: list[str] = []
    existing = [p for p in target.iterdir() if p.name.casefold() == "workspace.yaml"]
    if len(existing) > 1 or (existing and existing[0].name not in {"workspace.yaml", "WORKSPACE.yaml"}):
        raise ValueError("ambiguous workspace bootstrap filename")
    if existing:
        manifest = workspace_schema_path(target)
    else:
        template = load_schema(TEMPLATE_SCHEMA)
        name = "workspace.yaml" if template.get("schema_version") == 3 else "WORKSPACE.yaml"
        manifest = target / name
        contents = TEMPLATE_SCHEMA.read_text(encoding="utf-8")
        if name == "workspace.yaml":
            contents = contents.replace("WORKSPACE.yaml", name)
        with manifest.open("x", encoding="utf-8") as output:
            output.write(contents)
        created.append(name)

    data = load_schema(manifest)
    if manifest.name == "workspace.yaml" and data.get("schema_version") != 3:
        raise ValueError("lowercase workspace.yaml is supported only for schema v3")
    if data.get("schema_version") == 3:
        # Refuse unsafe or incoherent bindings before any human-control write.
        rc, output = run_audit(target, structure_only=True)
        if rc != 0:
            raise ValueError(f"cannot initialize an invalid workspace manifest:\n{output}")

    # V2 preserves its original AGENTS.md target. V3 resolves the slot rather
    # than assuming the human-authored control file stays at the workspace root.
    instructions_binding = "AGENTS.md"
    if data.get("schema_version") == 3:
        instructions = next(
            (slot for slot in data.get("slots", [])
             if isinstance(slot, dict) and slot.get("key") == "agent.instructions"),
            None,
        )
        if not instructions or instructions.get("arity") != "file":
            raise ValueError("schema v3 requires a file binding for agent.instructions")
        instructions_binding = instructions.get("binding")
    error = validate_binding_text(instructions_binding)
    if error or not resolves_within(target, instructions_binding):
        raise ValueError(f"invalid agent.instructions binding: {error or instructions_binding!r}")
    if instructions_binding.casefold() == manifest.name.casefold():
        raise ValueError("agent.instructions must not overwrite the workspace manifest")
    instructions_path = target / instructions_binding
    if instructions_path.is_symlink():
        raise ValueError(f"agent.instructions must not be a symlink: {instructions_binding}")
    if instructions_path.exists():
        if not instructions_path.is_file():
            raise ValueError(f"agent.instructions must be a regular file: {instructions_binding}")
        return created

    text = TEMPLATE_AGENTS.read_text(encoding="utf-8")
    if manifest.name == "workspace.yaml":
        text = text.replace("WORKSPACE.yaml", manifest.name)
    instructions_path.parent.mkdir(parents=True, exist_ok=True)
    if not resolves_within(target, instructions_binding):
        raise ValueError(f"agent.instructions escapes workspace: {instructions_binding}")
    with instructions_path.open("x", encoding="utf-8") as output:
        output.write(text)
    created.append(instructions_binding)
    return created


def slots_by_key(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {slot["key"]: slot for slot in data["slots"]}


def is_v3(data: dict[str, Any]) -> bool:
    return data.get("schema_version") == 3


def _root_hops(destination: str) -> str:
    """Relative hop from a generated helper's directory back to the workspace root."""
    depth = len(PurePosixPath(destination).parent.parts)
    return "/".join([".."] * depth)


def _root_resolution(helper: str, destination: str, self_var: str, root_var: str, *, sourced: bool, schema_name: str, fingerprint: str) -> list[str]:
    """Check the helper destination and parsed workspace semantics, not YAML bytes.

    Comments and YAML formatting cannot invalidate the generated helper.
    Material changes must be regenerated; copied helpers fail on changed identity.
    """
    hops = _root_hops(destination)
    suffix = f"/{hops}" if hops else ""
    failure = f"unset {root_var} _ws_link _ws_here; return 1 2>/dev/null || exit 1" if sourced else "exit 1"
    quoted_dest = shlex.quote(destination)
    canonicalize = (
        "import hashlib,json,sys\n"
        "try:\n import yaml\nexcept ImportError:\n sys.exit(3)\n"
        + CANONICAL_SOURCE
        + "try:\n d=yaml.safe_load(open(sys.argv[1],encoding='utf-8'))\nexcept Exception:\n sys.exit(4)\n"
        "print(fingerprint(d))\n"
    )
    return [
        f"# Workspace root = generated helper location, {destination}",
        f"# Verify its exact destination and the root bootstrap manifest ({schema_name}).",
        f'_ws_here="{self_var}"',
        'while [ -L "$_ws_here" ]; do',
        '  _ws_link="$(readlink -- "$_ws_here")"',
        '  case "$_ws_link" in /*) _ws_here="$_ws_link" ;; *) _ws_here="$(dirname -- "$_ws_here")/$_ws_link" ;; esac',
        "done",
        f'{root_var}="$(cd -P -- "$(dirname -- "$_ws_here"){suffix}" 2>/dev/null && pwd -P)"',
        f'if [ -z "${{{root_var}}}" ] || [ ! -f "${{{root_var}}}/{schema_name}" ] || [ ! "${{{root_var}}}/"{quoted_dest} -ef "$_ws_here" ]; then',
        f'  echo "{helper}: workspace root not found; expected <workspace>/{destination} and {schema_name}. Regenerate if relocated." >&2',
        f"  {failure}",
        "fi",
        "# A semantic fingerprint detects changed bindings without treating YAML whitespace as drift.",
        f'if [ "$(ls -A "${{{root_var}}}" | grep -ci \'^workspace\\.yaml$\')" != 1 ]; then',
        f'  echo "{helper}: expected exactly one workspace.yaml/WORKSPACE.yaml in ${{{root_var}}}" >&2',
        f"  {failure}",
        "fi",
        f'_ws_fingerprint="$(python3 -c {shlex.quote(canonicalize)} "${{{root_var}}}/{schema_name}" 2>/dev/null)"',
        'case $? in',
        '  0) ;;',
        f'  3) echo "{helper}: verifying {schema_name} needs python3 with PyYAML" >&2; {failure} ;;',
        f'  *) echo "{helper}: cannot read or parse {schema_name}" >&2; {failure} ;;',
        "esac",
        f'if [ "$_ws_fingerprint" != "{fingerprint}" ]; then',
        f'  echo "{helper}: workspace semantics changed; regenerate derived artifacts" >&2',
        f"  unset _ws_fingerprint; {failure}",
        "fi",
        "unset _ws_link _ws_here _ws_fingerprint",
    ]


def gen_paths(data: dict[str, Any], destination: str | None = None) -> str:
    lines = [
        f"# GENERATED from {manifest_name(data)} — do not edit. Source this file (bash or zsh).",
        "# WS_BINDING contains canonical relative bindings; WS contains absolute paths.",
        'if [ -n "${BASH_SOURCE:-}" ]; then',
        '  _ws_self="${BASH_SOURCE[0]}"',
        'elif [ -n "${ZSH_VERSION:-}" ]; then',
        '  _ws_self="${(%):-%x}"',
        "else",
        '  _ws_self="$0"',
        "fi",
    ]
    if destination is None:
        lines.append('WS_ROOT="$(cd -- "$(dirname -- "$_ws_self")" && pwd)"')
    else:
        lines.extend(_root_resolution("paths.sh", destination, "$_ws_self", "WS_ROOT", sourced=True, schema_name=data["_schema_name"], fingerprint=data["_semantic_fingerprint"]))
    lines.extend([
        "unset _ws_self",
        "declare -Ar WS_BINDING=(",
    ])
    for slot in data["slots"]:
        lines.append(f"  [{shlex.quote(slot['key'])}]={shlex.quote(slot['binding'])}")
    lines.append(")")
    lines.append("declare -Ar WS=(")
    for slot in data["slots"]:
        lines.append(f'  [{shlex.quote(slot["key"])}]="${{WS_ROOT}}/{slot["binding"]}"')
    lines.extend([
        ")",
        f'export WS_SCHEMA_VERSION={shlex.quote(str(data["schema_version"]))}',
        "",
    ])
    return "\n".join(lines)


def gen_mkdirs(data: dict[str, Any], destination: str | None = None) -> str:
    required_dirs = sorted({
        slot["binding"].rstrip("/")
        for slot in data["slots"]
        if slot["arity"] == "dir" and slot["requirement"] == "required"
    })
    all_dirs = sorted({slot["binding"].rstrip("/") for slot in data["slots"] if slot["arity"] == "dir"})
    extra_dirs = [path for path in all_dirs if path not in required_dirs]
    optional_state_files = [
        slot["binding"]
        for slot in data["slots"]
        if slot["arity"] == "file"
        and slot["category"] == "state"
        and slot["authority"] == "agent"
        and slot["agent_access"] == "write"
    ]
    lines = [
        "#!/usr/bin/env bash",
        f"# GENERATED from {manifest_name(data)} — idempotent, workspace-root anchored.",
        "# Default: minimum viable required directories. Use --all to materialize optional/conditional slots.",
        "set -euo pipefail",
        *(['ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"'] if destination is None
          else _root_resolution("mkdirs.sh", destination, "${BASH_SOURCE[0]}", "ROOT", sourced=False, schema_name=data["_schema_name"], fingerprint=data["_semantic_fingerprint"])),
        'case "${1:-}" in',
        '  ""|--required) MODE=required ;;',
        '  --all) MODE=all ;;',
        '  -h|--help) echo "usage: mkdirs.sh [--required|--all]"; exit 0 ;;',
        '  *) echo "unknown option: $1" >&2; exit 2 ;;',
        'esac',
    ]
    for rel in required_dirs:
        lines.append(f'mkdir -p -- "${{ROOT}}/{rel}"')
    lines.append('if [[ "${MODE}" == all ]]; then')
    for rel in extra_dirs:
        lines.append(f'  mkdir -p -- "${{ROOT}}/{rel}"')
    for rel in optional_state_files:
        lines.append(f'  [[ -e "${{ROOT}}/{rel}" ]] || : > "${{ROOT}}/{rel}"')
    lines.extend(["fi", ""])
    return "\n".join(lines)


def gen_excludes(data: dict[str, Any]) -> str:
    excluded = {s["binding"] for s in data["slots"] if s["indexed"] == "excluded"}
    disabled = {s["binding"] for s in data["slots"] if s["indexed"] == "disabled"}
    index_policy = dict(data.get("generation_contract", {}).get("index_policy", {}))
    if is_v3(data):
        outputs = generated_outputs(data)
        index_policy = {outputs[name]: policy for name, policy in index_policy.items()}
    for path, policy in index_policy.items():
        if policy == "excluded":
            excluded.add(path)
        elif policy == "disabled":
            disabled.add(path)
    lines = [
        f"# GENERATED from {manifest_name(data)} indexed policy.",
        "# Obsidian adapter: both excluded and disabled are placed in Excluded Files.",
        "# This deliberately degrades disabled to exclusion because the host cannot",
        "# represent runtime-only disabled as a stronger semantic state.",
        "#",
        "# indexed=excluded",
        *sorted(excluded),
        "",
        "# indexed=disabled",
        *sorted(disabled),
        "",
    ]
    return "\n".join(lines)


def _reference_curation_lines_v3(data: dict[str, Any]) -> list[str]:
    by = slots_by_key(data)
    curated = by["reference.curated"]
    collected = by["reference.collected"]
    prov = data["reference_contract"]["provenance"]
    reps = prov["representations"]
    return [
        "## Reference curation", "",
        "`knowledge.reference` defines **what** the material is: preserved source/evidence. The two classifications record its **curation state** — whether it was explicitly curated — not what it is and not who acquired it.", "",
        "```text",
        f"{collected['binding']}clip.md",
        "  classification = reference.collected   (not explicitly curated; any acquirer)",
        "  semantic.role = knowledge.reference",
        "",
        f"{curated['binding']}paper.pdf",
        "  classification = reference.curated     (explicitly human-curated)",
        "  semantic.role = knowledge.reference",
        "```", "",
        f"- `reference.collected` (`{collected['binding']}`): preserved raw/reference material not explicitly promoted. Any actor (human, agent, crawler, tool, integration, workflow) may deposit new objects; existing objects remain unchanged. Collected is a legitimate permanent home.",
        f"- `reference.curated` (`{curated['binding']}`): deliberately human-admitted, maintained reference, entered by explicit human-authorized promotion or direct human admission; agents read only.",
        "- Acquisition (who/how/when/origin/identity) and curation state are orthogonal. Review alone never promotes; promotion adds a curation record (" + ", ".join(f"`{f}`" for f in data["reference_contract"]["curation"]["record_fields"]) + ").",
        "- Presence in either class means preserved evidence, not truth, correctness, quality, or endorsement.",
        "- Every object answers " + ", ".join(f"`{f}`" for f in prov["required_fields"]) + " and a verifiable content identity:",
        f"  - Markdown capture: frontmatter `{reps['markdown_frontmatter']['key']}:` mapping" + (" or top-level fields" if reps["markdown_frontmatter"].get("top_level_fields") == "allowed" else "") + "; `content_hash` = sha256 of the body after the frontmatter (`content_hash_scope: body`).",
        f"  - Other file: `<file>{reps['file_sidecar']['suffix']}` sidecar; `content_hash` = sha256 of the file bytes.",
        f"  - Acquisition batch or corpus: directory `{reps['directory_manifest']['name']}`; per-file `files:` hashes or `content_identity: sha256-tree:<hex>`.",
        "  - A directory without a manifest is an organizational container; its descendants carry their own provenance.",
        "- `acquired_at` is never invented: when the original time is unknown, record custody time with `acquired_at_basis: import` and `original_acquisition_time: unknown`.",
        "- Agent-authored conclusions/synthesis route to `knowledge.durable`; deliberate external deliverables route to `output.artifact`.",
        "- Research is an activity/workflow. A finite research effort routes to `work.project`, not a new semantic role.",
        "",
    ]


def _identity_lines(data: dict[str, Any]) -> list[str]:
    identity = data.get("identity")
    if not isinstance(identity, dict):
        return ["## Workspace identity", "", f"No external identity is declared (`identity` is absent from `{manifest_name(data)}`).", ""]
    lines = ["## Workspace identity", "", f"Canonical source: the `identity` block of `{manifest_name(data)}`. It is system identity, not durable knowledge.", ""]
    lines.append(f"- endpoint: `{identity['endpoint']}`")
    lines.append(f"- owner authority: `{identity['owner']}`")
    if identity.get("description"):
        lines.append(f"- {' '.join(str(identity['description']).split())}")
    lines.append("")
    return lines


def _archive_lines_v3(data: dict[str, Any]) -> list[str]:
    archive = data["archive_contract"]
    return [
        f"Ordinary human cold storage in the archive binding needs no manifest. Formal semantic retirement of an existing canonical tree/boundary writes an immutable `{archive['manifest']}` at the retired root preserving: "
        + ", ".join(f"`{field}`" for field in archive["required_fields"]) + ". Never manufacture a manifest for cold storage.",
    ]


def _reference_admission_lines(data: dict[str, Any]) -> list[str]:
    if is_v3(data):
        return _reference_curation_lines_v3(data)
    by = slots_by_key(data)
    contract = data["reference_contract"]
    curated = by["reference.curated"]
    collected = by["reference.collected"]
    provenance = contract["collected_provenance"]
    return [
        "## Reference admission", "",
        "`knowledge.reference` defines **what** the material is: preserved source/evidence. Admission classification defines **how** that evidence entered the workspace; it does not create another knowledge role.", "",
        "```text",
        f"{curated['binding']}paper.pdf",
        "  classification = reference.curated",
        "  semantic.role = knowledge.reference",
        "",
        f"{collected['binding']}paper.pdf",
        "  classification = reference.collected",
        "  semantic.role = knowledge.reference",
        "```", "",
        f"- `reference.curated` (`{curated['binding']}`): human-admitted evidence; agents read only.",
        f"- `reference.collected` (`{collected['binding']}`): automatically acquired evidence; agents may deposit new children only. Existing children remain unchanged.",
        "- Human review of collected evidence does not change its admission classification; review is metadata.",
        "- Presence in either class means preserved evidence, not truth, correctness, quality, or endorsement.",
        f"- Collected file provenance uses `{provenance['file_sidecar_suffix']}` sidecars and requires " + ", ".join(f"`{field}`" for field in provenance["required_fields"]) + "; files also require SHA-256 `content_hash`.",
        "- Agent-authored conclusions/synthesis route to `knowledge.durable`; deliberate external deliverables route to `output.artifact`.",
        "- Research is an activity/workflow. A finite research effort routes to `work.project`, not a new semantic role.",
        "",
    ]


def gen_context(data: dict[str, Any]) -> str:
    lines = [
        "# Context router",
        "",
        f"> GENERATED from `{manifest_name(data)}`. Do not hand-edit; regenerate.",
        "",
        f"Schema version {data['schema_version']}, status **{data['status']}**. Downstream references use immutable keys; bindings may move.",
        "",
        "## Where things go",
        "",
        "| key | binding | semantic role | what | effective agent operations |",
        "|---|---|---|---|---|",
    ]
    for slot in data["slots"]:
        description = " ".join(slot["description"].split())
        short = description.split(".")[0]
        ops = compact_ops(effective_agent_operations(slot, data))
        role = semantic_role_for_slot(slot, data)
        lines.append(f"| `{slot['key']}` | `{slot['binding']}` | `{role}` | {short} | {ops} |")
    if is_v3(data):
        lines.extend(["", *_identity_lines(data)[:-1]])
    lines.extend(["", *_reference_admission_lines(data), "## Hard rules", ""])
    for key, value in data["invariants"].items():
        lines.append(f"- **{key}** — {' '.join(value.split())}")
    archive_text = _archive_lines_v3(data) if is_v3(data) else [
        f"Whole-tree retirement uses `{data['archive_contract']['manifest']}` and preserves: "
        + ", ".join(f"`{field}`" for field in data["archive_contract"]["required_fields"]) + "."
    ]
    lines.extend([
        "", "## Archive identity", "",
        *archive_text,
        "", "## Boundary trust", "",
    ])
    for key, trust in data["boundary_trust"].items():
        lines.append(f"- `{key}` → **{trust}**")
    lines.extend([
        "", "## Composition", "", " ".join(data["composition"].split()),
        "", "## Admission / promotion boundary", "", " ".join(data["promotion"]["into_human_authoritative"].split()), "",
        " ".join(data["promotion"]["collected_deposit"].split()), "",
    ])
    return "\n".join(lines)


def _policy_line(name: str, policy: dict[str, Any]) -> str:
    return f"**`{name}`** — " + "; ".join(f"{verb}: {value}" for verb, value in policy.items())


def _crosswalk_rows(data: dict[str, Any]) -> list[str]:
    labels = {"llm_wiki": "LLM Wiki", "code": "CODE", "para": "PARA", "icm_mwp": "ICM/MWP"}
    rows: list[str] = []
    for source, concepts in data["crosswalk"].items():
        for concept, target in concepts.items():
            if isinstance(target, list):
                rendered = " + ".join(f"`{item}`" for item in target)
            else:
                rendered = f"`{target}`" if "." in str(target) and " " not in str(target) else str(target)
            rows.append(f"| {labels.get(source, source)} | {concept.replace('_', ' ').title()} | {rendered} |")
    return rows


def resolved_derived_names(data: dict[str, Any]) -> tuple[str, ...]:
    """Resolve historical/default generated names through semantic bindings."""
    if is_v3(data):
        return tuple(generated_outputs(data).values())
    router = slots_by_key(data)["context.router"]["binding"].rstrip("/")
    return tuple(router if name == "CONTEXT.md" else name for name in data.get("generation_contract", {}).get("derived", []))


def _spec_intro_v3(data: dict[str, Any]) -> list[str]:
    outputs = generated_outputs(data)
    return [
        f"`{manifest_name(data)}` at the target root is the **only** fixed bootstrap path. Every generated artifact resolves its destination through a declared slot binding in `generation_contract.outputs`: " + ", ".join(f"`{name}` → `{path}`" for name, path in outputs.items()) + ". Generated helpers locate the workspace root from that encoded relationship and verify it by finding `" + manifest_name(data) + "`; they never assume their own directory is the root.", "",
        "Schema v3 preserves the complete frozen-v1 semantic/policy baseline and the v2 reference classification keys, and adds: relocatable generated outputs, an optional machine-readable workspace `identity`, the `state.hotset` operational hotset, `system.operations` and `system.documentation`, the human/editor-facing `asset.*` bindings with the `asset` category, actor-independent curation semantics with representation-aware provenance, and scoped archive manifests. Schema v2 workspaces continue to validate under the unchanged v2 rules.", "",
        *_identity_lines(data),
    ]


def gen_spec(data: dict[str, Any]) -> str:
    by = slots_by_key(data)
    b = {key: slot["binding"] for key, slot in by.items()}
    router_binding = b["context.router"]
    lines = [
        "# Workspace Schema — Specification", "",
        f"> **Generated from `{manifest_name(data)}`. Do not hand-edit.** Edit the YAML and regenerate.", "",
        f"Within the CCA Hybrid Workspace Profile, `{manifest_name(data)}` is the canonical machine-readable bootstrap anchor. Stable keys carry declared meaning; bindings are workspace-local implementations and may move without changing that meaning.", "",
        *(_spec_intro_v3(data) if is_v3(data) else [
        f"The generated context router is the `context.router` binding (`{router_binding}`), not a hardcoded filename. Helper artifacts such as `paths.sh`, `mkdirs.sh`, `SPEC.md`, and host adapters are derived tooling. `AGENTS.md` remains human-authored and is validated, not regenerated.", "",
        "Schema v2 preserves the complete frozen-v1 semantic/policy baseline and adds only the two reference-admission classification keys required by the v1 evolution contract. No new knowledge role, axis, authority vocabulary, or mutability vocabulary was introduced.", ""]),
        "Upstream crosswalks are non-owning mappings. Native ICM, LLM Wiki, PARA, CODE/BASB, and other upstream methods remain governed by their own authority; this profile composes useful semantics without claiming to redefine them.", "",
        "## Identifier and the five axes", "",
        f"`id` is **{data['identifier']['id']}**. `key` is the **{data['identifier']['key']}**.", "",
        "Every resolved entity is interpreted across five independent axes. **No axis implicitly overrides another.**", "",
    ]
    for axis, meaning in data["axes"].items():
        lines.append(f"- **{axis}** — {meaning}")
    lines.extend(["", "## Invariants (frozen)", ""])
    for name, text in data["invariants"].items():
        lines.append(f"**{name.replace('_', ' ').title()}.** {' '.join(text.split())}")
    lines.extend(["", "## Resolved binding map", "", "Consumers resolve the key first and use the binding second.", "", "```text"])
    for slot in data["slots"]:
        lines.append(f"{slot['key']:<24} -> {slot['binding']}")
    lines.extend(["```", "", "## The schema", "", "| id | category | key | binding | semantic role | arity | mutability | indexed | authority | agent_access | link_target | requirement |", "|---:|---|---|---|---|---|---|---|---|---|---|---|"])
    for slot in data["slots"]:
        role = semantic_role_for_slot(slot, data)
        lines.append(f"| {slot['id']} | {slot['category']} | `{slot['key']}` | `{slot['binding']}` | `{role}` | {slot['arity']} | {slot['mutability']} | {slot['indexed']} | {slot['authority']} | {slot['agent_access']} | {slot['link_target']} | {slot['requirement']} |")
    lines.extend(["", "### Descriptions", ""])
    for slot in data["slots"]:
        lines.append(f"{slot['id']}. **`{slot['key']}`** — {' '.join(slot['description'].split())}")

    lines.extend(["", *_reference_admission_lines(data), "## Classification vs semantic role", "", "Classification keys compose with semantic roles; they do not replace them.", "", "| classification | semantic role |", "|---|---|"])
    for classification, role in data["classification_roles"].items():
        lines.append(f"| `{classification}` | `{role}` |")
    lines.extend(["", " ".join(data["composition"].split()), ""])

    lines.extend(["", "## Policy definitions (frozen)", "", "Unspecified mutation verbs are **prohibited**. Effective permission is resolved from the most-specific applicable binding and its declared mutability/authority/agent-access policy; a parent permission never widens a more-specific child policy.", ""])
    for name, policy in data["policy_definitions"].items():
        lines.append("- " + _policy_line(name, policy))
    lines.extend(["", "### Privileged operations", ""])
    for key, operations in data["privileged_operations"].items():
        lines.append(f"- `{key}` — " + "; ".join(f"{op}: {gate}" for op, gate in operations.items()))

    lines.extend([
        "", "## Archive identity contract", "",
        *((_archive_lines_v3(data) + [" ".join(f"`{scope}` — {meaning}." for scope, meaning in data["archive_contract"]["scope_semantics"].items()), "The manifest is immutable once written. Individual entities normally retire via status metadata and remain in place. `boundary_class` may be null for non-project boundaries.", ""]) if is_v3(data) else [
        f"Whole-tree retirement creates `{data['archive_contract']['manifest']}` at the archived root. The manifest is immutable once written and MUST contain: " + ", ".join(f"`{field}`" for field in data["archive_contract"]["required_fields"]) + ". Individual entities normally retire via status metadata and remain in place. `boundary_class` may be null for non-project boundaries.", ""]),
        "| manifest field | meaning |", "|---|---|",
        *[f"| `{field}` | {meaning} |" for field, meaning in data["archive_contract"]["field_semantics"].items()],
        "", "## Boundary trust", "", "| boundary class | trust |", "|---|---|",
    ])
    for key, trust in data["boundary_trust"].items():
        lines.append(f"| `{key}` | `{trust}` |")
    lines.extend(["", "### Trust meanings", "", "| trust | meaning |", "|---|---|"])
    for trust, meaning in data["boundary_trust_semantics"].items():
        lines.append(f"| `{trust}` | {meaning} |")

    example_project = f"{b['project.remote']}cca/"
    lines.extend([
        "", "External/upstream control files are context only. They can never grant or widen workspace authority.",
        "", "## Admission and promotion policy", "", " ".join(data["promotion"]["into_human_authoritative"].split()), "", " ".join(data["promotion"]["collected_deposit"].split()),
        "", "## Composition examples", "", "```text", example_project, "  classification = project.remote", "  semantic.role = work.project", "", f"{b['reference.curated']}paper.pdf", "  classification = reference.curated", "  semantic.role = knowledge.reference", "", f"{b['reference.collected']}paper.pdf", "  classification = reference.collected", "  semantic.role = knowledge.reference", "```", "",
    ])

    headings = {"category":"Category","arity":"Arity","mutability":"Mutability","indexed":"Indexed","authority":"Authority","agent_access":"Agent access","link_target":"Link target","requirement":"Requirement"}
    for vocab_name in ("category","arity","mutability","indexed","authority","agent_access","link_target","requirement"):
        lines.extend(["", f"## {headings[vocab_name]} semantics", "", "| value | meaning |", "|---|---|"])
        for value in data["vocab"][vocab_name]:
            lines.append(f"| `{value}` | {data['vocab_semantics'][vocab_name][value]} |")

    required = [slot["key"] for slot in data["slots"] if slot["requirement"] == "required"]
    lines.extend(["", "## Minimum viable workspace", "", ", ".join(f"`{key}`" for key in required) + ".", "", "## Evolution contract", "", "| change | treatment |", "|---|---|"])
    for change, treatment in data["evolution_contract"].items():
        lines.append(f"| `{change}` | `{treatment}` |")
    lines.extend(["", "## System crosswalk", "", "> Adaptation/inspiration only; mappings are not semantic equivalence and do not redefine or claim conformance with upstream methods.", "", "| source | concept | mapping |", "|---|---|---|", *_crosswalk_rows(data), "", "## Generation contract", "", "Resolved derived outputs: " + ", ".join(f"`{name}`" for name in resolved_derived_names(data)) + ".", "", "Human-authored: " + ", ".join(f"`{name}`" for name in data["generation_contract"]["human_authored"]) + ".", "", "## Generation pipeline", "", "```text", f"{manifest_name(data)}  (canonical profile bootstrap; human-authored)", "      │"])
    if is_v3(data):
        outputs = generated_outputs(data)
        lines.extend(f"      ├── generate ──► {path}  ({name})" for name, path in outputs.items())
        lines.extend([f"      └── validate ──► {b['agent.instructions']} (agent.instructions; human-authored)", "```", ""])
    else:
        lines.extend(["      ├── generate ──► SPEC.md", "      ├── generate ──► paths.sh", f"      ├── generate ──► {router_binding}  (context.router)", "      ├── generate ──► mkdirs.sh", "      ├── generate ──► host visibility adapter", "      └── validate ──► AGENTS.md (human-authored)", "```", ""])
    return "\n".join(lines)


# ── Python helpers (cross-platform; default for v3) ──────────────────────────
PYTHON_HELPER_EXTENSIONS = {".py"}
SHELL_HELPER_EXTENSIONS = {".sh"}


def _py_root_resolution(data: dict[str, Any], destination: str) -> list[str]:
    """Python twin of _root_resolution: same verification, no shell required."""
    depth = len(PurePosixPath(destination).parent.parts)
    return [
        "import hashlib",
        "import json",
        "import os",
        "from pathlib import Path",
        "import sys",
        "",
        f"MANIFEST = {manifest_name(data)!r}",
        f"DESTINATION = {destination!r}",
        f"FINGERPRINT = {data['_semantic_fingerprint']!r}",
        "",
        "",
        "class WorkspaceRootError(RuntimeError):",
        '    """The helper is not at its generated location, or the workspace changed."""',
        "",
        "",
        *CANONICAL_SOURCE.rstrip("\n").split("\n"),
        "",
        "",
        "def workspace_root() -> Path:",
        '    """Resolve and verify the workspace root; never assumes this file\'s folder is the root."""',
        "    here = Path(os.path.realpath(__file__))",
        f"    root = here.parents[{depth}] if len(here.parents) > {depth} else here.parent",
        "    manifests = [p for p in root.iterdir() if p.name.casefold() == 'workspace.yaml']",
        "    if len(manifests) != 1:",
        "        raise WorkspaceRootError(f'expected exactly one workspace.yaml/WORKSPACE.yaml in {root}')",
        "    try:",
        "        same = os.path.samefile(root / DESTINATION, here) and (root / MANIFEST).is_file()",
        "    except OSError:",
        "        same = False",
        "    if not same:",
        "        raise WorkspaceRootError(f'workspace root not found; expected <workspace>/{DESTINATION} and {MANIFEST}. Regenerate if relocated.')",
        "    try:",
        "        import yaml",
        "    except ImportError as exc:",
        "        raise WorkspaceRootError(f'verifying {MANIFEST} needs PyYAML') from exc",
        "    try:",
        "        data = yaml.safe_load((root / MANIFEST).read_text(encoding='utf-8'))",
        "    except Exception as exc:",
        "        raise WorkspaceRootError(f'cannot read or parse {MANIFEST}') from exc",
        "    if fingerprint(data) != FINGERPRINT:",
        "        raise WorkspaceRootError('workspace semantics changed; regenerate derived artifacts')",
        "    return root",
    ]


def gen_paths_py(data: dict[str, Any], destination: str) -> str:
    bindings = {slot["key"]: slot["binding"] for slot in data["slots"]}
    lines = [
        "#!/usr/bin/env python3",
        f"# GENERATED from {manifest_name(data)} — do not edit. Cross-platform semantic binding map.",
        "# Import WS_ROOT / WS_BINDING / WS, or run: python paths.py KEY | --json | --list",
        "from __future__ import annotations",
        "",
        *_py_root_resolution(data, destination),
        "",
        "",
        "WS_BINDING = {",
        *(f"    {key!r}: {binding!r}," for key, binding in bindings.items()),
        "}",
        f"WS_SCHEMA_VERSION = {data['schema_version']!r}",
        "",
        "",
        "def ws() -> dict[str, Path]:",
        "    root = workspace_root()",
        "    return {key: root / binding.rstrip('/') for key, binding in WS_BINDING.items()}",
        "",
        "",
        "def main(argv: list[str]) -> int:",
        "    try:",
        "        paths = ws()",
        "    except WorkspaceRootError as exc:",
        "        print(f'paths: {exc}', file=sys.stderr)",
        "        return 1",
        "    if argv and argv[0] in ('-h', '--help'):",
        "        print('usage: paths.py [KEY | --json | --list]   (import: ws(), WS_BINDING, workspace_root())')",
        "        return 0",
        "    if not argv or argv[0] == '--list':",
        "        for key, path in paths.items():",
        "            print(f'{key}\\t{path}')",
        "        return 0",
        "    if argv[0] == '--json':",
        "        print(json.dumps({key: str(path) for key, path in paths.items()}, indent=2))",
        "        return 0",
        "    if argv[0] not in paths:",
        "        print(f'paths: unknown semantic key {argv[0]!r}', file=sys.stderr)",
        "        return 2",
        "    print(paths[argv[0]])",
        "    return 0",
        "",
        "",
        "if __name__ == '__main__':",
        "    raise SystemExit(main(sys.argv[1:]))",
        "",
    ]
    return "\n".join(lines)


def gen_mkdirs_py(data: dict[str, Any], destination: str) -> str:
    required = sorted({s["binding"].rstrip("/") for s in data["slots"] if s["arity"] == "dir" and s["requirement"] == "required"})
    every = sorted({s["binding"].rstrip("/") for s in data["slots"] if s["arity"] == "dir"})
    state_files = [s["binding"] for s in data["slots"] if s["arity"] == "file" and s["category"] == "state" and s["authority"] == "agent" and s["agent_access"] == "write"]
    lines = [
        "#!/usr/bin/env python3",
        f"# GENERATED from {manifest_name(data)} — idempotent, workspace-root anchored.",
        "# Default: minimum viable required directories. Use --all to materialize optional/conditional slots.",
        "from __future__ import annotations",
        "",
        *_py_root_resolution(data, destination),
        "",
        "",
        f"REQUIRED_DIRS = {required!r}",
        f"OPTIONAL_DIRS = {[d for d in every if d not in required]!r}",
        f"STATE_FILES = {state_files!r}",
        "",
        "",
        "def main(argv: list[str]) -> int:",
        "    mode = argv[0] if argv else '--required'",
        "    if mode in ('-h', '--help'):",
        "        print('usage: mkdirs.py [--required|--all]')",
        "        return 0",
        "    if mode not in ('--required', '--all'):",
        "        print(f'unknown option: {mode}', file=sys.stderr)",
        "        return 2",
        "    try:",
        "        root = workspace_root()",
        "    except WorkspaceRootError as exc:",
        "        print(f'mkdirs: {exc}', file=sys.stderr)",
        "        return 1",
        "    for rel in REQUIRED_DIRS + (OPTIONAL_DIRS if mode == '--all' else []):",
        "        (root / rel).mkdir(parents=True, exist_ok=True)",
        "    if mode == '--all':",
        "        for rel in STATE_FILES:",
        "            path = root / rel",
        "            if not path.exists():",
        "                path.touch()",
        "    return 0",
        "",
        "",
        "if __name__ == '__main__':",
        "    raise SystemExit(main(sys.argv[1:]))",
        "",
    ]
    return "\n".join(lines)


def render_helper(kind: str, data: dict[str, Any], destination: str) -> str:
    suffix = PurePosixPath(destination).suffix.lower()
    if suffix in PYTHON_HELPER_EXTENSIONS:
        return gen_paths_py(data, destination) if kind == "paths" else gen_mkdirs_py(data, destination)
    if suffix in SHELL_HELPER_EXTENSIONS:
        return gen_paths(data, destination) if kind == "paths" else gen_mkdirs(data, destination)
    raise ValueError(f"generated {kind} helper {destination!r} must end in .py or .sh")


def render_all(data: dict[str, Any]) -> dict[str, str]:
    if is_v3(data):
        outputs = generated_outputs(data)
        rendered = {
            outputs["paths"]: render_helper("paths", data, outputs["paths"]),
            outputs["mkdirs"]: render_helper("mkdirs", data, outputs["mkdirs"]),
            outputs["host_index_adapter"]: gen_excludes(data),
            outputs["context.router"]: gen_context(data),
            outputs["spec"]: gen_spec(data),
        }
        return rendered
    router = slots_by_key(data)["context.router"]["binding"].rstrip("/")
    rendered = {
        "paths.sh": gen_paths(data),
        "mkdirs.sh": gen_mkdirs(data),
        "obsidian-excludes.txt": gen_excludes(data),
        router: gen_context(data),
        "SPEC.md": gen_spec(data),
    }
    declared = set(resolved_derived_names(data))
    if set(rendered) != declared:
        raise ValueError(f"generator outputs {sorted(rendered)} differ from resolved generation contract {sorted(declared)}")
    return rendered


FILE_EXTENSIONS = {"yaml", "yml", "md", "json", "sh", "txt", "py", "toml"}


def validate_agents(data: dict[str, Any], target: Path) -> list[str]:
    name = slots_by_key(data)["agent.instructions"]["binding"] if is_v3(data) else "AGENTS.md"
    path = target / name
    if not path.exists():
        return [f"{name} missing — required human-authored control file"]
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return ["AGENTS.md is empty — required control content cannot be blank"]
    problems: list[str] = []
    marker = f"workspace-contract:v{data['schema_version']}"
    if marker not in text:
        problems.append(f"AGENTS.md missing contract marker {marker!r}")
    known = {slot["key"] for slot in data["slots"]}
    for match in re.findall(r"`([a-z]+\.[a-z.]+)`", text):
        if match.rsplit(".", 1)[-1] in FILE_EXTENSIONS:
            continue  # a file name such as `workspace.yaml`, not a semantic key
        prefix = match.split(".")[0]
        prefixes = {"agent","context","state","system","knowledge","work","responsibility","project","output","lifecycle","workspace","reference"}
        if is_v3(data):
            prefixes = prefixes | {"asset"}
        if prefix in prefixes and match not in known:
            problems.append(f"AGENTS.md references unknown semantic/classification key `{match}`")
    manifest_name = data.get("_schema_name", "WORKSPACE.yaml")
    for term in (manifest_name, "project.upstream", "knowledge.reference", "reference.curated", "reference.collected", "generated artifacts"):
        if term not in text:
            problems.append(f"AGENTS.md missing required control term {term!r}")
    for stale in ("indexed=no", "indexed=yes", "excluded|no"):
        if stale in text:
            problems.append(f"AGENTS.md contains stale vocabulary {stale!r}")
    return problems


def run_audit(target: Path, *, structure_only: bool = False) -> tuple[int, str]:
    command = [sys.executable, str(PACKAGE_ROOT / "audit.py"), "--target", str(target)]
    if structure_only:
        command.append("--structure-only")
    result = subprocess.run(
        command,
        cwd=target,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode, result.stdout + result.stderr


def artifact_drift(rendered: dict[str, str], target: Path) -> list[str]:
    problems: list[str] = []
    for name, expected in rendered.items():
        path = target / name
        if not path.exists():
            problems.append(f"{name}: missing generated artifact")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            diff = "".join(difflib.unified_diff(actual.splitlines(True), expected.splitlines(True), fromfile=f"{name} (disk)", tofile=f"{name} (rendered)", n=2))
            problems.append(f"{name}: generated artifact drift\n" + "\n".join(diff.splitlines()[:12]))
    return problems


def _header(text: str, lines: int = 3) -> str:
    return "".join(text.splitlines(keepends=True)[:lines])


def foreign_destinations(rendered: dict[str, str], target: Path) -> list[str]:
    """Existing destinations that are not this generator's artifact.

    An existing file may be replaced only when it already starts with the exact
    header this generator writes for that artifact (its first three lines).
    """
    foreign: list[str] = []
    for name, expected in rendered.items():
        path = target / name
        if path.is_dir():
            foreign.append(name)
        elif path.is_file():
            current = path.read_text(encoding="utf-8", errors="replace")
            if current != expected and _header(current) != _header(expected):
                foreign.append(name)
    return foreign


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate or verify CCA Hybrid Workspace Profile artifacts on an explicit target workspace.")
    parser.add_argument("--target", required=True, help="Target workspace root. Never defaults to the installed skill/tool directory.")
    parser.add_argument("--init", action="store_true", help="Seed a missing workspace manifest and AGENTS.md; never overwrite existing files.")
    parser.add_argument("--check", action="store_true", help="Verify target artifacts without rewriting them.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        target = resolve_target(args.target, init=args.init)
        initialized = initialize_target(target) if args.init else []
        data = schema(target)
    except (yaml.YAMLError, ValueError, OSError) as exc:
        print(f"workspace load failed: {exc}", file=sys.stderr)
        return 1
    # Generating v3 projections must not rehash the entire source corpus.
    audit_rc, audit_output = run_audit(target, structure_only=is_v3(data))
    if audit_rc != 0:
        print(audit_output, end="")
        print("SCHEMA INVALID — generation aborted.", file=sys.stderr)
        return 1
    rendered = render_all(data)
    agent_problems = validate_agents(data, target)
    if args.check:
        problems = artifact_drift(rendered, target) + agent_problems
        if problems:
            print("freeze check failed:")
            for problem in problems:
                print(f"  ✗ {problem}")
            return 1
        print("✓ target schema audit passed")
        print("✓ all generated artifacts match canonical render")
        print("✓ AGENTS.md structural control contract passed")
        return 0
    if is_v3(data):
        foreign = foreign_destinations(rendered, target)
        if foreign:
            for name in foreign:
                print(f"refusing to overwrite {name}: existing file is not a generated artifact", file=sys.stderr)
            return 1
    for name, text in rendered.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        helpers = {generated_outputs(data)[k] for k in ("paths", "mkdirs")} if is_v3(data) else set()
        if name.endswith(".sh") or name in helpers:
            path.chmod(0o755)
    if initialized:
        print("initialized:")
        for name in initialized:
            print(f"  • {name}")
    print("generated on target:")
    for name in resolved_derived_names(data):
        print(f"  • {name}")
    if agent_problems:
        print("AGENTS.md validation notes:")
        for problem in agent_problems:
            print(f"  ⚠ {problem}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
