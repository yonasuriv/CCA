#!/usr/bin/env python3
"""Copy into a workspace as bin/capture (or similar).

Deposit a file into the knowledge raw/ directory, append the source index,
and update .manifest.sha256. Refuses to overwrite an existing raw file.

Environment (optional):
  CCA_RAW_DIR   default: resources/knowledge/raw  or  raw  (auto-detect)
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
from datetime import date
from pathlib import Path


def find_raw(root: Path) -> Path:
    env = os.environ.get("CCA_RAW_DIR")
    if env:
        return (root / env).resolve()
    candidates = [
        root / "resources" / "knowledge" / "sources" / "raw",
        root / "resources" / "knowledge" / "raw",
        root / "Resources" / "knowledge" / "llm-wiki" / "raw",
        root / "Resources" / "knowledge" / "raw",
        root / "brain" / "raw",
        root / "raw",
    ]
    for c in candidates:
        if c.is_dir() or c.parent.is_dir():
            return c
    return candidates[0]


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "source"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: capture <path> [slug]", file=sys.stderr)
        return 2
    root = Path.cwd()
    # if invoked from bin/, workspace root is parent
    if (Path(argv[0]).resolve().parent.name in {"bin", "scripts"}):
        root = Path(argv[0]).resolve().parents[1]
    src = Path(argv[1]).expanduser().resolve()
    if not src.is_file():
        print(f"not a file: {src}", file=sys.stderr)
        return 1
    raw = find_raw(root)
    raw.mkdir(parents=True, exist_ok=True)
    index = raw.parent / "index.md"
    if not index.exists():
        index = raw / "_index.md"
    manifest = raw.parent / ".manifest.sha256"
    if not manifest.parent.exists():
        manifest = raw / ".manifest.sha256"
    log = raw.parent.parent / "log.md"
    if not log.exists():
        log = raw.parent / "log.md"

    slug = slugify(argv[2] if len(argv) > 2 else src.stem)
    today = date.today().isoformat()
    dest_name = f"{today}-{slug}{src.suffix.lower() or '.md'}"
    dest = raw / dest_name
    if dest.exists():
        print(f"refusing overwrite: {dest}", file=sys.stderr)
        return 1
    dest.write_bytes(src.read_bytes())
    digest = sha256_file(dest)

    entries: dict[str, str] = {}
    if manifest.exists():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            d, n = line.split(None, 1)
            entries[n] = d
    entries[dest_name] = digest
    manifest.write_text(
        "".join(f"{d}  {n}\n" for n, d in sorted(entries.items())),
        encoding="utf-8",
    )

    if not index.exists():
        index.write_text(
            "# Source index\n\n| Date | File | Note | Supersedes |\n|---|---|---|---|\n",
            encoding="utf-8",
        )
    idx = index.read_text(encoding="utf-8")
    if dest_name not in idx:
        index.write_text(idx + ("" if idx.endswith("\n") else "\n") + f"| {today} | `{dest_name}` | {slug} | |\n", encoding="utf-8")

    if log.exists():
        lt = log.read_text(encoding="utf-8")
        line = f"- {today}: capture `{dest_name}`\n"
        if dest_name not in lt:
            log.write_text(lt + ("" if lt.endswith("\n") else "\n") + line, encoding="utf-8")

    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
