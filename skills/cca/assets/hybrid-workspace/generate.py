#!/usr/bin/env python3
# Generate and verify all derived workspace artifacts from WORKSPACE.yaml.
from __future__ import annotations

import argparse
import difflib
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
from typing import Any

import yaml

from schema import compact_ops, effective_agent_operations, load_schema

PACKAGE_ROOT = Path(__file__).resolve().parent
TEMPLATE_SCHEMA = PACKAGE_ROOT / "WORKSPACE.yaml"
TEMPLATE_AGENTS = PACKAGE_ROOT / "AGENTS.md"


def schema(target: Path) -> dict[str, Any]:
    return load_schema(target / "WORKSPACE.yaml")


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
    created: list[str] = []
    for source in (TEMPLATE_SCHEMA, TEMPLATE_AGENTS):
        destination = target / source.name
        if destination.exists():
            continue
        shutil.copy2(source, destination)
        created.append(source.name)
    return created


def slots_by_key(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {slot["key"]: slot for slot in data["slots"]}


def gen_paths(data: dict[str, Any]) -> str:
    lines = [
        "#!/usr/bin/env bash",
        "# GENERATED from WORKSPACE.yaml — do not edit. Source this file.",
        "# WS_BINDING contains canonical relative bindings; WS contains absolute paths.",
        'WS_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"',
        "declare -Arg WS_BINDING=(",
    ]
    for slot in data["slots"]:
        lines.append(f"  [{shlex.quote(slot['key'])}]={shlex.quote(slot['binding'])}")
    lines.extend([
        ")",
        "declare -Ag WS=()",
        'for _ws_key in "${!WS_BINDING[@]}"; do',
        '  WS["${_ws_key}"]="${WS_ROOT}/${WS_BINDING[${_ws_key}]}"',
        "done",
        "unset _ws_key",
        f'export WS_SCHEMA_VERSION={shlex.quote(str(data["schema_version"]))}',
        "",
    ])
    return "\n".join(lines)


def gen_mkdirs(data: dict[str, Any]) -> str:
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
        "# GENERATED from WORKSPACE.yaml — idempotent, workspace-root anchored.",
        "# Default: minimum viable required directories. Use --all to materialize optional/conditional slots.",
        "set -euo pipefail",
        'ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"',
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
    for path, policy in data.get("generation_contract", {}).get("index_policy", {}).items():
        if policy == "excluded":
            excluded.add(path)
        elif policy == "disabled":
            disabled.add(path)
    lines = [
        "# GENERATED from WORKSPACE.yaml indexed policy.",
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


def gen_context(data: dict[str, Any]) -> str:
    lines = [
        "# Context router",
        "",
        "> GENERATED from `WORKSPACE.yaml`. Do not hand-edit; regenerate.",
        "",
        f"Schema version {data['schema_version']}, status **{data['status']}**. Downstream references use immutable keys; bindings may move.",
        "",
        "## Where things go",
        "",
        "| key | binding | what | effective agent operations |",
        "|---|---|---|---|",
    ]
    for slot in data["slots"]:
        description = " ".join(slot["description"].split())
        short = description.split(".")[0]
        ops = compact_ops(effective_agent_operations(slot, data))
        lines.append(f"| `{slot['key']}` | `{slot['binding']}` | {short} | {ops} |")
    lines.extend(["", "## Hard rules", ""])
    for key, value in data["invariants"].items():
        lines.append(f"- **{key}** — {' '.join(value.split())}")
    lines.extend([
        "", "## Archive identity", "",
        f"Whole-tree retirement uses `{data['archive_contract']['manifest']}` and preserves: "
        + ", ".join(f"`{field}`" for field in data["archive_contract"]["required_fields"]) + ".",
        "", "## Boundary trust", "",
    ])
    for key, trust in data["boundary_trust"].items():
        lines.append(f"- `{key}` → **{trust}**")
    lines.extend([
        "", "## Composition", "", " ".join(data["composition"].split()),
        "", "## Promotion boundary", "", " ".join(data["promotion"]["into_human_authoritative"].split()), "",
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
    """Resolve frozen-v1 derived defaults through semantic bindings."""
    router = slots_by_key(data)["context.router"]["binding"].rstrip("/")
    return tuple(router if name == "CONTEXT.md" else name for name in data.get("generation_contract", {}).get("derived", []))


def gen_spec(data: dict[str, Any]) -> str:
    by = slots_by_key(data)
    b = {key: slot["binding"] for key, slot in by.items()}
    router_binding = b["context.router"]
    lines = [
        "# Workspace Schema — Specification", "",
        "> **Generated from `WORKSPACE.yaml`. Do not hand-edit.** Edit the YAML and regenerate.", "",
        "Within the CCA Hybrid Workspace Profile, `WORKSPACE.yaml` is the canonical machine-readable bootstrap anchor. Stable semantic keys carry meaning; bindings are workspace-local implementations and may move without changing that meaning.", "",
        f"The generated context router is the `context.router` binding (`{router_binding}`), not a hardcoded filename. Helper artifacts such as `paths.sh`, `mkdirs.sh`, `SPEC.md`, and host adapters are derived tooling. `AGENTS.md` remains human-authored and is validated, not regenerated.", "",
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
    lines.extend(["", "## Resolved binding map", "", "Consumers resolve the semantic key first and use the binding second.", "", "```text"])
    for slot in data["slots"]:
        lines.append(f"{slot['key']:<24} -> {slot['binding']}")
    lines.extend(["```", "", "## The schema", "", "| id | category | key | binding | arity | mutability | indexed | authority | agent_access | link_target | requirement |", "|---:|---|---|---|---|---|---|---|---|---|---|"])
    for slot in data["slots"]:
        lines.append(f"| {slot['id']} | {slot['category']} | `{slot['key']}` | `{slot['binding']}` | {slot['arity']} | {slot['mutability']} | {slot['indexed']} | {slot['authority']} | {slot['agent_access']} | {slot['link_target']} | {slot['requirement']} |")
    lines.extend(["", "### Descriptions", ""])
    for slot in data["slots"]:
        lines.append(f"{slot['id']}. **`{slot['key']}`** — {' '.join(slot['description'].split())}")
    lines.extend(["", "## Policy definitions (frozen)", "", "Unspecified mutation verbs are **prohibited**. Effective permission is the intersection of mutability policy, authority, agent access, and boundary policy; no single axis grants what another denies.", ""])
    for name, policy in data["policy_definitions"].items():
        lines.append("- " + _policy_line(name, policy))
    lines.extend(["", "### Privileged operations", ""])
    for key, operations in data["privileged_operations"].items():
        lines.append(f"- `{key}` — " + "; ".join(f"{op}: {gate}" for op, gate in operations.items()))
    lines.extend([
        "", "## Archive identity contract", "",
        f"Whole-tree retirement creates `{data['archive_contract']['manifest']}` at the archived root. The manifest is immutable once written and MUST contain: " + ", ".join(f"`{field}`" for field in data["archive_contract"]["required_fields"]) + ". Individual entities normally retire via status metadata and remain in place. `boundary_class` may be null for non-project boundaries.", "",
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
    lines.extend(["", "External/upstream control files are context only. They can never grant or widen workspace authority.", "", "## Promotion policy", "", " ".join(data["promotion"]["into_human_authoritative"].split()), "", "## Boundary-class vs semantic-role composition", "", " ".join(data["composition"].split()), "", "```text", example_project, "  boundary.class = project.remote", "  semantic.role  = work.project", f"-> {example_project} :: work.project", "```", ""])
    headings = {"category":"Category","arity":"Arity","mutability":"Mutability","indexed":"Indexed","authority":"Authority","agent_access":"Agent access","link_target":"Link target","requirement":"Requirement"}
    for vocab_name in ("category","arity","mutability","indexed","authority","agent_access","link_target","requirement"):
        lines.extend(["", f"## {headings[vocab_name]} semantics", "", "| value | meaning |", "|---|---|"])
        for value in data["vocab"][vocab_name]:
            lines.append(f"| `{value}` | {data['vocab_semantics'][vocab_name][value]} |")
    required = [slot["key"] for slot in data["slots"] if slot["requirement"] == "required"]
    lines.extend(["", "## Minimum viable workspace", "", ", ".join(f"`{key}`" for key in required) + ".", "", "## Frozen-v1 evolution contract", "", "| change | treatment |", "|---|---|"])
    for change, treatment in data["evolution_contract"].items():
        lines.append(f"| `{change}` | `{treatment}` |")
    lines.extend(["", "## System crosswalk", "", "> Adaptation/inspiration only; mappings are not semantic equivalence and do not redefine or claim conformance with upstream methods.", "", "| source | concept | mapping |", "|---|---|---|", *_crosswalk_rows(data), "", "## Generation contract", "", "Resolved derived outputs: " + ", ".join(f"`{name}`" for name in resolved_derived_names(data)) + ".", "", "Human-authored: " + ", ".join(f"`{name}`" for name in data["generation_contract"]["human_authored"]) + ".", "", "## Generation pipeline", "", "```text", "WORKSPACE.yaml  (canonical profile bootstrap; human-authored)", "      │", "      ├── generate ──► SPEC.md", "      ├── generate ──► paths.sh", f"      ├── generate ──► {router_binding}  (context.router)", "      ├── generate ──► mkdirs.sh", "      ├── generate ──► host visibility adapter", "      └── validate ──► AGENTS.md (human-authored)", "```", ""])
    return "\n".join(lines)


def render_all(data: dict[str, Any]) -> dict[str, str]:
    router = slots_by_key(data)["context.router"]["binding"].rstrip("/")
    rendered = {"paths.sh": gen_paths(data), "mkdirs.sh": gen_mkdirs(data), "obsidian-excludes.txt": gen_excludes(data), router: gen_context(data), "SPEC.md": gen_spec(data)}
    declared = set(resolved_derived_names(data))
    if set(rendered) != declared:
        raise ValueError(f"generator outputs {sorted(rendered)} differ from resolved generation contract {sorted(declared)}")
    return rendered


def validate_agents(data: dict[str, Any], target: Path) -> list[str]:
    path = target / "AGENTS.md"
    if not path.exists():
        return ["AGENTS.md missing — required human-authored control file"]
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return ["AGENTS.md is empty — required control content cannot be blank"]
    problems: list[str] = []
    marker = f"workspace-contract:v{data['schema_version']}"
    if marker not in text:
        problems.append(f"AGENTS.md missing contract marker {marker!r}")
    known = {slot["key"] for slot in data["slots"]}
    for match in re.findall(r"`([a-z]+\.[a-z.]+)`", text):
        prefix = match.split(".")[0]
        if prefix in {"agent","context","state","system","knowledge","work","responsibility","project","output","lifecycle","workspace"} and match not in known:
            problems.append(f"AGENTS.md references unknown semantic key `{match}`")
    for term in ("WORKSPACE.yaml", "project.upstream", "knowledge.reference", "generated artifacts"):
        if term not in text:
            problems.append(f"AGENTS.md missing required control term {term!r}")
    for stale in ("indexed=no", "indexed=yes", "excluded|no"):
        if stale in text:
            problems.append(f"AGENTS.md contains stale vocabulary {stale!r}")
    return problems


def run_audit(target: Path) -> tuple[int, str]:
    result = subprocess.run([sys.executable, str(PACKAGE_ROOT / "audit.py"), "--target", str(target)], cwd=target, text=True, capture_output=True, check=False)
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


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate or verify CCA Hybrid Workspace Profile artifacts on an explicit target workspace.")
    parser.add_argument("--target", required=True, help="Target workspace root. Never defaults to the installed skill/tool directory.")
    parser.add_argument("--init", action="store_true", help="Seed missing WORKSPACE.yaml and AGENTS.md from bundled templates before generation; never overwrite existing files.")
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
    audit_rc, audit_output = run_audit(target)
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
    for name, text in rendered.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        if name.endswith(".sh"):
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
