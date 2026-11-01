#!/usr/bin/env python3
# Reference provenance primitives for the Hybrid Workspace Profile (schema v3):
# provenance representations, content identity, container walking, and an
# admission-time stamping helper. Pure functions are shared with audit.py.
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
from pathlib import Path
import re
import sys
from typing import Any, Callable, Iterator

import yaml

from schema import StrictSafeLoader, load_schema

HASH_RE = re.compile(r"^sha256:([0-9a-fA-F]{64})$")
TREE_RE = re.compile(r"^sha256-tree:([0-9a-fA-F]{64})$")
FRONTMATTER_CLOSE = {b"---", b"..."}


# ── content identity ──────────────────────────────────────────────────────────

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_frontmatter(data: bytes) -> tuple[bytes, bytes] | None:
    """Split a Markdown document into (frontmatter YAML bytes, body bytes).

    The frontmatter starts with a first line that is exactly ``---`` and ends at
    the next line that is exactly ``---`` or ``...`` (an optional trailing CR is
    tolerated). The body is every byte after that closing line's terminator.
    Returns None when the document has no well-formed frontmatter.
    """
    lines = data.splitlines(keepends=True)
    if not lines or lines[0].rstrip(b"\r\n") != b"---":
        return None
    offset = len(lines[0])
    for line in lines[1:]:
        if line.rstrip(b"\r\n") in FRONTMATTER_CLOSE:
            front = data[len(lines[0]):offset]
            return front, data[offset + len(line):]
        offset += len(line)
    return None


def markdown_body_hash(data: bytes) -> str | None:
    """sha256 of the body bytes after frontmatter (hash_scope: body)."""
    parts = split_frontmatter(data)
    if parts is None:
        return None
    return sha256_bytes(parts[1])


def tree_files(directory: Path, manifest_name: str) -> list[str]:
    """Regular files beneath directory (POSIX relative paths), excluding the manifest at its root."""
    files: list[str] = []
    for path in directory.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"symlink inside provenance-bearing directory: {path}")
        if path.is_file():
            rel = path.relative_to(directory).as_posix()
            if rel != manifest_name:
                files.append(rel)
    return sorted(files, key=lambda item: item.encode("utf-8"))


def tree_identity(directory: Path, manifest_name: str = ".source.yaml") -> str:
    """sha256-tree identity, reproducible with coreutils:

        find . -type f ! -path ./.source.yaml -printf '%P\\0' | LC_ALL=C sort -z \\
          | xargs -0 sha256sum | sha256sum
    """
    lines = []
    for rel in tree_files(directory, manifest_name):
        lines.append(f"{sha256_bytes((directory / rel).read_bytes())}  {rel}\n")
    return "sha256-tree:" + sha256_bytes("".join(lines).encode("utf-8"))


# ── provenance objects ────────────────────────────────────────────────────────

@dataclass
class SourceObject:
    path: Path
    representation: str  # markdown_frontmatter | file_sidecar | directory_manifest | missing
    metadata_path: Path | None = None
    problems: list[str] = field(default_factory=list)


def _load_yaml_mapping(text: str) -> Any:
    return yaml.load(text, Loader=StrictSafeLoader)


def read_frontmatter(path: Path) -> dict[str, Any] | None:
    parts = split_frontmatter(path.read_bytes())
    if parts is None:
        return None
    data = _load_yaml_mapping(parts[0].decode("utf-8"))
    return data if isinstance(data, dict) else None


def iter_source_objects(root_dir: Path, contract: dict[str, Any]) -> Iterator[SourceObject]:
    """Walk a reference-class binding and yield every provenance-bearing object.

    Directories carrying a directory manifest are acquisition objects (batches or
    corpora). Directories without one are organizational containers: their
    descendants are walked and must each carry their own provenance.
    """
    reps = contract["representations"]
    suffix = reps["file_sidecar"]["suffix"]
    manifest = reps["directory_manifest"]["name"]
    md_suffix = reps["markdown_frontmatter"]["applies_to"]
    ignored = set(contract.get("ignored_names", []))

    def walk(directory: Path) -> Iterator[SourceObject]:
        entries = sorted(directory.iterdir(), key=lambda p: p.name)
        names = {entry.name for entry in entries}
        for entry in entries:
            if entry.name in ignored or entry.name == manifest:
                continue
            if entry.is_symlink():
                yield SourceObject(entry, "missing", problems=["symlinked source objects are not admissible"])
                continue
            if entry.is_file() and entry.name.endswith(suffix):
                if entry.name[: -len(suffix)] not in names:
                    yield SourceObject(entry, "missing", problems=[f"orphan provenance sidecar has no source object"])
                continue
            if entry.is_dir():
                if (entry / manifest).is_file():
                    yield SourceObject(entry, "directory_manifest", entry / manifest)
                else:
                    yield from walk(entry)
                continue
            sidecar = entry.with_name(entry.name + suffix)
            if sidecar.is_file():
                yield SourceObject(entry, "file_sidecar", sidecar)
            elif entry.name.endswith(md_suffix):
                yield SourceObject(entry, "markdown_frontmatter", entry)
            else:
                yield SourceObject(entry, "missing", problems=[f"source file has no provenance (expected {entry.name + suffix})"])

    if (root_dir / manifest).is_file():
        yield SourceObject(root_dir, "directory_manifest", root_dir / manifest)
        return
    yield from walk(root_dir)


def _valid_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def validate_object(obj: SourceObject, contract: dict[str, Any], *, curated: bool, record_fields: list[str]) -> list[str]:
    """Return problems for one source object under the v3 provenance contract."""
    problems = list(obj.problems)
    if obj.representation == "missing":
        return problems
    reps = contract["representations"]
    try:
        if obj.representation == "markdown_frontmatter":
            data = obj.path.read_bytes()
            parts = split_frontmatter(data)
            front = _load_yaml_mapping(parts[0].decode("utf-8")) if parts else None
            if not isinstance(front, dict):
                return problems + ["Markdown source has no frontmatter provenance and no sidecar"]
            prov = front.get(reps["markdown_frontmatter"]["key"])
            if not isinstance(prov, dict):
                return problems + ["frontmatter lacks a provenance mapping"]
            prov = dict(prov)
            for canonical, alias in (reps["markdown_frontmatter"].get("field_aliases") or {}).items():
                if not prov.get(canonical) and isinstance(front.get(alias), str):
                    prov[canonical] = front[alias]
        else:
            loaded = _load_yaml_mapping(obj.metadata_path.read_text(encoding="utf-8"))  # type: ignore[union-attr]
            if not isinstance(loaded, dict) or not isinstance(loaded.get("provenance"), dict):
                return problems + ["provenance metadata must contain a provenance mapping"]
            prov = dict(loaded["provenance"])
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return problems + [f"invalid provenance metadata: {exc}"]
    for name, value in list(prov.items()):
        # Unquoted YAML timestamps load as datetime; keep their exact meaning.
        if isinstance(value, datetime):
            prov[name] = value.isoformat()

    for name in contract["required_fields"]:
        if not isinstance(prov.get(name), str) or not prov[name].strip():
            problems.append(f"missing/non-empty provenance field {name!r}")
    if prov.get("acquired_at") is not None and isinstance(prov.get("acquired_at"), str) and not _valid_timestamp(prov["acquired_at"]):
        problems.append("acquired_at must be RFC3339/ISO-8601 with timezone")
    basis = prov.get("acquired_at_basis")
    if basis is not None and basis not in contract.get("acquired_at_basis", []):
        problems.append(f"acquired_at_basis must be one of {contract.get('acquired_at_basis')}, got {basis!r}")
    original = prov.get("original_acquisition_time")
    if original is not None and original != "unknown" and not _valid_timestamp(original):
        problems.append("original_acquisition_time must be RFC3339 with timezone or 'unknown'")
    if curated:
        for name in record_fields:
            if not isinstance(prov.get(name), str) or not prov[name].strip():
                problems.append(f"curated source requires curation record field {name!r}")
        if isinstance(prov.get("curated_at"), str) and not _valid_timestamp(prov["curated_at"]):
            problems.append("curated_at must be RFC3339/ISO-8601 with timezone")

    if obj.representation == "markdown_frontmatter":
        problems.extend(_check_hash(prov, markdown_body_hash(obj.path.read_bytes()), "body"))
    elif obj.representation == "file_sidecar":
        problems.extend(_check_hash(prov, sha256_bytes(obj.path.read_bytes()), "bytes"))
    else:
        problems.extend(_check_directory_identity(obj, prov, reps["directory_manifest"]["name"]))
    return problems


def _check_hash(prov: dict[str, Any], actual: str | None, scope: str) -> list[str]:
    declared = prov.get("content_hash")
    if not isinstance(declared, str):
        return [f"content_hash (sha256, scope {scope}) is required"]
    match = HASH_RE.fullmatch(declared)
    if not match:
        return ["content_hash must be sha256:<64 hex characters>"]
    declared_scope = prov.get("content_hash_scope", scope)
    if declared_scope != scope:
        return [f"content_hash_scope must be {scope!r} for this representation, got {declared_scope!r}"]
    if actual is None or actual.lower() != match.group(1).lower():
        return [f"content hash mismatch ({scope}); existing source was modified or metadata is incorrect"]
    return []


def _check_directory_identity(obj: SourceObject, prov: dict[str, Any], manifest_name: str) -> list[str]:
    files = prov.get("files")
    identity = prov.get("content_identity")
    try:
        present = tree_files(obj.path, manifest_name)
    except ValueError as exc:
        return [str(exc)]
    if files is not None:
        if not isinstance(files, dict) or not files:
            return ["files must be a non-empty mapping of relative path -> sha256:<hex>"]
        problems: list[str] = []
        if sorted(files) != present:
            missing = sorted(set(present) - set(files))[:5]
            extra = sorted(set(files) - set(present))[:5]
            problems.append(f"manifest file list differs from directory contents (unlisted={missing}, absent={extra})")
        for rel, declared in files.items():
            match = HASH_RE.fullmatch(declared) if isinstance(declared, str) else None
            if not match:
                problems.append(f"{rel}: per-file hash must be sha256:<64 hex characters>")
            elif rel in present and sha256_bytes((obj.path / rel).read_bytes()) != match.group(1).lower():
                problems.append(f"{rel}: content hash mismatch")
        return problems
    if not isinstance(identity, str):
        return ["directory manifest requires `files` (per-file sha256) or `content_identity` (sha256-tree:<hex>)"]
    if not TREE_RE.fullmatch(identity):
        return ["content_identity must use the verifiable sha256-tree:<hex> scheme"]
    if tree_identity(obj.path, manifest_name).lower() != identity.lower():
        return ["content_identity mismatch; directory contents changed or metadata is incorrect"]
    return []


# ── admission-time stamping ───────────────────────────────────────────────────

def stamp_markdown(path: Path, frontmatter_key: str = "provenance") -> str:
    """Add a body-scoped content_hash to a Markdown capture's provenance mapping.

    Admission-time only: an existing content_hash is never replaced (replacing
    it would launder a mutation). Required provenance fields are never invented;
    the caller must supply them via the capture template.
    Returns one of: stamped, already-stamped, no-frontmatter, no-provenance.
    """
    raw = path.read_bytes()
    parts = split_frontmatter(raw)
    if parts is None:
        return "no-frontmatter"
    front_text = parts[0].decode("utf-8")
    front = _load_yaml_mapping(front_text)
    if not isinstance(front, dict) or not isinstance(front.get(frontmatter_key), dict):
        return "no-provenance"
    if "content_hash" in front[frontmatter_key]:
        return "already-stamped"
    lines = front_text.splitlines(keepends=True)
    newline = "\r\n" if lines and lines[0].endswith("\r\n") else "\n"
    start = next(i for i, line in enumerate(lines) if re.match(rf"^{re.escape(frontmatter_key)}:\s*$", line.rstrip("\r\n")))
    end = start + 1
    indent = "  "
    while end < len(lines) and (lines[end].startswith((" ", "\t")) or not lines[end].strip()):
        if lines[end].strip():
            indent = lines[end][: len(lines[end]) - len(lines[end].lstrip())]
        end += 1
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    digest = sha256_bytes(parts[1])
    insert = [f"{indent}content_hash: sha256:{digest}{newline}", f"{indent}content_hash_scope: body{newline}"]
    new_front = "".join(lines[:end] + insert + lines[end:])
    head = raw[: raw.index(b"\n") + 1]
    path.write_bytes(head + new_front.encode("utf-8") + raw[len(head) + len(parts[0]):])
    if markdown_body_hash(path.read_bytes()) != digest:
        raise RuntimeError(f"{path}: stamping changed the body; refusing")
    return "stamped"


def _reference_roots(root: Path, data: dict[str, Any]) -> list[Path]:
    slots = {slot["key"]: slot for slot in data["slots"]}
    return [root / slots[key]["binding"].rstrip("/") for key in ("reference.collected", "reference.curated")]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Hybrid Workspace v3 provenance helper (identity + admission stamping).")
    parser.add_argument("--target", required=True, help="Target workspace root containing WORKSPACE.yaml.")
    sub = parser.add_subparsers(dest="command", required=True)
    stamp = sub.add_parser("stamp", help="Add body-scoped content_hash to Markdown captures that lack one (never overwrites).")
    stamp.add_argument("paths", nargs="*", help="Workspace-relative files/dirs under a reference class (default: both classes).")
    stamp.add_argument("--dry-run", action="store_true")
    ident = sub.add_parser("identity", help="Print the sha256-tree identity of a directory, or sha256 of a file.")
    ident.add_argument("path")
    args = parser.parse_args(argv)

    root = Path(args.target).expanduser().resolve()
    data = load_schema(root / "WORKSPACE.yaml")
    if data.get("schema_version") != 3:
        print("provenance.py requires a schema v3 workspace", file=sys.stderr)
        return 2
    contract = data["reference_contract"]["provenance"]
    if args.command == "identity":
        target = (root / args.path).resolve()
        if root not in target.parents and target != root:
            print("path escapes the workspace", file=sys.stderr)
            return 2
        if target.is_dir():
            print(tree_identity(target, contract["representations"]["directory_manifest"]["name"]))
        else:
            print("sha256:" + sha256_bytes(target.read_bytes()))
        return 0

    class_roots = [p.resolve() for p in _reference_roots(root, data)]
    requested = [(root / p).resolve() for p in args.paths] or class_roots
    counts: dict[str, int] = {}
    for base in requested:
        if not base.exists():
            continue
        if not any(base == c or c in base.parents for c in class_roots):
            print(f"refusing {base}: not under a reference class binding", file=sys.stderr)
            return 2
        candidates = [base] if base.is_file() else list(iter_source_objects(base, contract))
        for item in candidates:
            path = item if isinstance(item, Path) else item.path
            rep = "markdown_frontmatter" if isinstance(item, Path) else item.representation
            if rep != "markdown_frontmatter":
                continue
            if args.dry_run:
                front = read_frontmatter(path) or {}
                status = "would-stamp" if isinstance(front.get("provenance"), dict) and "content_hash" not in front["provenance"] else "skip"
            else:
                status = stamp_markdown(path)
            counts[status] = counts.get(status, 0) + 1
            if status in {"no-frontmatter", "no-provenance"}:
                print(f"  ! {path.relative_to(root)}: {status} (capture template must supply provenance)")
    for status, count in sorted(counts.items()):
        print(f"{status}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
