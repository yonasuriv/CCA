#!/usr/bin/env python3
# Reference provenance primitives for the Hybrid Workspace Profile (schema v3):
# provenance representations, content identity, container walking, and an
# admission-time stamping helper. Pure functions are shared with audit.py.
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import date, datetime
import hashlib
from pathlib import Path
import re
import sys
from typing import Any, Iterator

import yaml

from schema import StrictSafeLoader, load_schema, resolves_within

HASH_RE = re.compile(r"^sha256:([0-9a-fA-F]{64})$")
TREE_RE = re.compile(r"^sha256-tree:([0-9a-fA-F]{64})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FRONTMATTER_CLOSE = {b"---", b"..."}
CHUNK = 1 << 20


# ── content identity ──────────────────────────────────────────────────────────

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_frontmatter(data: bytes) -> tuple[bytes, bytes] | None:
    """Split a Markdown document into (frontmatter YAML bytes, body bytes).

    The frontmatter starts with a first line that is exactly ``---`` and ends at
    the next line that is exactly ``---`` or ``...`` (an optional trailing CR is
    tolerated). The body is every byte after that closing line's terminator,
    hashed exactly as stored (no newline normalisation). Returns None when the
    document has no well-formed frontmatter.
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
            raise ValueError(f"symlink inside provenance-bearing directory: {path.relative_to(directory)}")
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
    digest = hashlib.sha256()
    for rel in tree_files(directory, manifest_name):
        digest.update(f"{sha256_file(directory / rel)}  {rel}\n".encode("utf-8"))
    return "sha256-tree:" + digest.hexdigest()


# ── provenance objects ────────────────────────────────────────────────────────

@dataclass
class SourceObject:
    path: Path
    representation: str  # markdown_frontmatter | file_sidecar | directory_manifest | missing
    metadata_path: Path | None = None
    problems: list[str] = field(default_factory=list)


def _load_yaml_mapping(text: str) -> Any:
    return yaml.load(text, Loader=StrictSafeLoader)


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
            if entry.is_symlink():
                yield SourceObject(entry, "missing", problems=["symlinked source objects are not admissible"])
                continue
            if entry.name in ignored and entry.is_file():
                continue
            if entry.name == manifest:
                if not entry.is_file():
                    yield SourceObject(entry, "missing", problems=[f"{manifest} must be a regular file, not a directory"])
                continue
            if entry.is_file() and entry.name.endswith(suffix):
                if entry.name[: -len(suffix)] not in names:
                    yield SourceObject(entry, "missing", problems=["orphan provenance sidecar has no source object"])
                continue
            if entry.is_dir():
                marker = entry / manifest
                if marker.is_symlink() or marker.is_dir():
                    yield SourceObject(entry, "missing", problems=[f"{manifest} must be a regular file, not a directory or symlink"])
                elif marker.is_file():
                    yield SourceObject(entry, "directory_manifest", marker)
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

    marker = root_dir / manifest
    if marker.is_file() and not marker.is_symlink():
        yield SourceObject(root_dir, "directory_manifest", marker)
        return
    yield from walk(root_dir)


CANONICAL_FIELDS = (
    "origin", "acquired_by", "acquisition_method", "acquired_at", "acquired_at_basis", "original_acquisition_time",
    "content_hash", "content_hash_scope", "curated_by", "curated_at", "curated_at_basis",
)


def _normalise(value: Any) -> Any:
    # Unquoted YAML timestamps/dates load as datetime/date; keep their meaning.
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def _valid_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip() or DATE_RE.fullmatch(value.strip()):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _valid_date(value: Any) -> bool:
    if not isinstance(value, str) or not DATE_RE.fullmatch(value.strip()):
        return False
    try:
        date.fromisoformat(value.strip())
    except ValueError:
        return False
    return True


def markdown_provenance(front: dict[str, Any], rep: dict[str, Any]) -> dict[str, Any] | None:
    """Collect canonical provenance fields from a capture's frontmatter.

    Fields come from the nested provenance mapping first, then (when the contract
    allows top-level fields, as capture tools that cannot write nested YAML need)
    from same-named top-level keys, then from declared aliases. Returns None when
    no provenance is present at all.
    """
    nested = front.get(rep["key"])
    if nested is not None and not isinstance(nested, dict):
        return None
    prov: dict[str, Any] = dict(nested or {})
    if rep.get("top_level_fields") == "allowed":
        for name in CANONICAL_FIELDS:
            if name not in prov and name in front:
                prov[name] = front[name]
    for name, alias in (rep.get("field_aliases") or {}).items():
        if not prov.get(name) and alias in front:
            prov[name] = front[alias]
    if nested is None and not any(name in prov for name in CANONICAL_FIELDS if name != "origin"):
        return None
    return {name: _normalise(value) for name, value in prov.items()}


def validate_object(obj: SourceObject, contract: dict[str, Any], *, curated: bool, curation: dict[str, Any]) -> list[str]:
    """Return problems for one source object under the v3 provenance contract."""
    problems = list(obj.problems)
    if obj.representation == "missing":
        return problems
    reps = contract["representations"]
    try:
        if obj.representation == "markdown_frontmatter":
            parts = split_frontmatter(obj.path.read_bytes())
            front = _load_yaml_mapping(parts[0].decode("utf-8")) if parts else None
            if not isinstance(front, dict):
                return problems + ["Markdown source has no frontmatter provenance and no sidecar"]
            prov = markdown_provenance(front, reps["markdown_frontmatter"])
            if prov is None:
                return problems + ["frontmatter carries no provenance fields"]
        else:
            loaded = _load_yaml_mapping(obj.metadata_path.read_text(encoding="utf-8"))  # type: ignore[union-attr]
            if not isinstance(loaded, dict) or not isinstance(loaded.get("provenance"), dict):
                return problems + ["provenance metadata must contain a provenance mapping"]
            prov = {name: _normalise(value) for name, value in loaded["provenance"].items()}
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        # ValueError: YAML resolves an unquoted impossible date (2026-02-30) and fails while constructing it.
        return problems + [f"invalid provenance metadata: {exc}"]

    for name in contract["required_fields"]:
        if not isinstance(prov.get(name), str) or not prov[name].strip():
            problems.append(f"missing/non-empty provenance field {name!r}")
    if isinstance(prov.get("acquired_at"), str) and prov["acquired_at"].strip() and not _valid_timestamp(prov["acquired_at"]):
        problems.append("acquired_at must be an RFC3339/ISO-8601 timestamp with timezone (a bare date is not a timestamp)")
    basis = prov.get("acquired_at_basis")
    if basis is not None and basis not in contract.get("acquired_at_basis", []):
        problems.append(f"acquired_at_basis must be one of {contract.get('acquired_at_basis')}, got {basis!r}")
    original = prov.get("original_acquisition_time")
    if original is not None and original != "unknown" and not _valid_timestamp(original) and not _valid_date(original):
        problems.append("original_acquisition_time must be an RFC3339 timestamp with timezone, an ISO calendar date, or 'unknown'")
    if curated:
        for name in curation.get("record_fields", []):
            if not isinstance(prov.get(name), str) or not prov[name].strip():
                problems.append(f"curated source requires curation record field {name!r}")
        if isinstance(prov.get("curated_at"), str) and prov["curated_at"].strip() and not _valid_timestamp(prov["curated_at"]):
            problems.append("curated_at must be RFC3339/ISO-8601 with timezone")
        record_basis = prov.get("curated_at_basis")
        if record_basis is not None and record_basis not in curation.get("record_basis", []):
            problems.append(f"curated_at_basis must be one of {curation.get('record_basis')}, got {record_basis!r}")

    if obj.representation == "markdown_frontmatter":
        problems.extend(_check_hash(prov, markdown_body_hash(obj.path.read_bytes()), "body"))
    elif obj.representation == "file_sidecar":
        problems.extend(_check_hash(prov, sha256_file(obj.path), "bytes"))
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
            elif rel in present and sha256_file(obj.path / rel) != match.group(1).lower():
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

class StampError(RuntimeError):
    pass


def stamp_markdown(path: Path, rep: dict[str, Any]) -> str:
    """Complete a new Markdown capture's identity by adding a body-scoped content_hash.

    Admission-time only: an existing content_hash is never replaced (that would
    launder a mutation) and no other provenance field is ever invented; the
    capture template must already have supplied them. The insertion is verified
    by re-parsing; on any mismatch the original bytes are restored.
    Returns: stamped | already-stamped. Raises StampError when the capture cannot
    be stamped safely.
    """
    raw = path.read_bytes()
    parts = split_frontmatter(raw)
    if parts is None:
        raise StampError("no frontmatter")
    front_text = parts[0].decode("utf-8")
    front = _load_yaml_mapping(front_text)
    if not isinstance(front, dict):
        raise StampError("frontmatter is not a mapping")
    prov = markdown_provenance(front, rep)
    if prov is None:
        raise StampError("no provenance fields (the capture template must supply them)")
    missing = [name for name in ("origin", "acquired_by", "acquisition_method", "acquired_at") if not prov.get(name)]
    if missing:
        raise StampError(f"provenance incomplete, refusing to stamp: missing {missing}")
    if "content_hash" in prov:
        return "already-stamped"
    key = rep["key"]
    lines = front_text.splitlines(keepends=True)
    newline = "\r\n" if lines and lines[0].endswith("\r\n") else "\n"
    digest = sha256_bytes(parts[1])
    if isinstance(front.get(key), dict):
        header = [i for i, line in enumerate(lines) if re.fullmatch(rf"{re.escape(key)}:[ \t]*", line.rstrip("\r\n"))]
        if len(header) != 1:
            raise StampError(f"unsupported `{key}:` layout (use a block mapping without inline comments)")
        start = header[0]
        child = next((line for line in lines[start + 1:] if line.strip()), "")
        indent = child[: len(child) - len(child.lstrip())] if child[:1] in (" ", "\t") else "  "
        insert_at = start + 1
        insert = [f"{indent}content_hash: sha256:{digest}{newline}", f"{indent}content_hash_scope: body{newline}"]
    else:
        insert_at = len(lines)
        insert = [f"content_hash: sha256:{digest}{newline}", f"content_hash_scope: body{newline}"]
        if lines and not lines[-1].endswith(("\n", "\r")):
            insert[0] = newline + insert[0]
    new_front = "".join(lines[:insert_at] + insert + lines[insert_at:])
    head = raw[: raw.index(b"\n") + 1]
    updated = head + new_front.encode("utf-8") + raw[len(head) + len(parts[0]):]
    path.write_bytes(updated)
    try:
        check = split_frontmatter(updated)
        reparsed = _load_yaml_mapping(check[0].decode("utf-8")) if check else None
        got = markdown_provenance(reparsed, rep) if isinstance(reparsed, dict) else None
        if not got or got.get("content_hash") != f"sha256:{digest}" or got.get("content_hash_scope") != "body" or check is None or check[1] != parts[1]:
            raise StampError("verification after insertion failed")
    except (StampError, yaml.YAMLError) as exc:
        path.write_bytes(raw)
        raise StampError(f"{exc}; original restored") from None
    return "stamped"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Hybrid Workspace v3 provenance helper (identity + admission stamping).")
    parser.add_argument("--target", required=True, help="Target workspace root containing WORKSPACE.yaml.")
    sub = parser.add_subparsers(dest="command", required=True)
    stamp = sub.add_parser(
        "stamp",
        help="At deposit time, add the body-scoped content_hash to new Markdown captures in reference.collected. "
             "Explicit paths only; never touches reference.curated; never overwrites an existing hash.",
    )
    stamp.add_argument("paths", nargs="+", help="Workspace-relative files/dirs under reference.collected that are being admitted now.")
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
    slots = {slot["key"]: slot for slot in data["slots"]}

    if args.command == "identity":
        target = (root / args.path).resolve()
        if root not in target.parents and target != root:
            print("path escapes the workspace", file=sys.stderr)
            return 2
        if target.is_dir():
            print(tree_identity(target, contract["representations"]["directory_manifest"]["name"]))
        else:
            print("sha256:" + sha256_file(target))
        return 0

    collected_binding = slots["reference.collected"]["binding"]
    if not resolves_within(root, collected_binding):
        print("refusing: reference.collected escapes the workspace after symlink resolution", file=sys.stderr)
        return 2
    collected = (root / collected_binding.rstrip("/")).resolve()
    rep = contract["representations"]["markdown_frontmatter"]
    counts: dict[str, int] = {}
    failed = False
    for raw_path in args.paths:
        base = (root / raw_path).resolve()
        if base != collected and collected not in base.parents:
            print(f"refusing {raw_path}: stamping is limited to reference.collected (curated sources are never stamped)", file=sys.stderr)
            return 2
        if base == collected:
            print(f"refusing {raw_path}: name the new deposit (a file or its batch folder), not the whole reference.collected class", file=sys.stderr)
            return 2
        if not base.exists():
            print(f"refusing {raw_path}: does not exist", file=sys.stderr)
            return 2
        objects = [SourceObject(base, "markdown_frontmatter", base)] if base.is_file() else list(iter_source_objects(base, contract))
        for obj in objects:
            if obj.representation != "markdown_frontmatter" or not obj.path.name.endswith(rep["applies_to"]):
                continue
            rel = obj.path.relative_to(root)
            try:
                if args.dry_run:
                    parts = split_frontmatter(obj.path.read_bytes())
                    front = _load_yaml_mapping(parts[0].decode("utf-8")) if parts else None
                    prov = markdown_provenance(front, rep) if isinstance(front, dict) else None
                    status = "already-stamped" if prov and "content_hash" in prov else "would-stamp" if prov else "no-provenance"
                else:
                    status = stamp_markdown(obj.path, rep)
                    if status == "stamped":
                        print(f"  stamped {rel}")
            except (StampError, yaml.YAMLError, UnicodeError, ValueError) as exc:
                status = "refused"
                failed = True
                print(f"  ! {rel}: {exc}", file=sys.stderr)
            counts[status] = counts.get(status, 0) + 1
    for status, count in sorted(counts.items()):
        print(f"{status}: {count}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
