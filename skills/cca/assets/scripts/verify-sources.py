#!/usr/bin/env python3
"""Copy into a workspace as bin/verify (or similar).

Checks: raw hashes vs .manifest.sha256, raw files appear in a source index,
wiki pages (if any) have sources: or unsourced: true in frontmatter/body.

Usage: verify [--update]
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


def find_raw(root: Path) -> Path | None:
    for c in (
        root / "resources" / "knowledge" / "sources" / "raw",
        root / "resources" / "knowledge" / "raw",
        root / "Resources" / "knowledge" / "llm-wiki" / "raw",
        root / "Resources" / "knowledge" / "raw",
        root / "brain" / "raw",
        root / "raw",
    ):
        if c.is_dir():
            return c
    return None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: list[str]) -> int:
    root = Path.cwd()
    if Path(argv[0]).resolve().parent.name in {"bin", "scripts"}:
        root = Path(argv[0]).resolve().parents[1]
    update = "--update" in argv
    raw = find_raw(root)
    if raw is None:
        print("VERIFY FAIL\n- no raw/ directory found")
        return 1
    manifest = raw.parent / ".manifest.sha256"
    if not manifest.exists():
        manifest = raw / ".manifest.sha256"
    index = raw.parent / "index.md"
    if not index.exists():
        index = raw / "_index.md"
    errors: list[str] = []
    files = sorted(p for p in raw.iterdir() if p.is_file() and not p.name.startswith(".") and p.name != ".gitkeep")

    entries: dict[str, str] = {}
    if update:
        entries = {p.name: sha256_file(p) for p in files}
        manifest.write_text("".join(f"{d}  {n}\n" for n, d in sorted(entries.items())), encoding="utf-8")
    elif manifest.exists():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            d, n = line.split(None, 1)
            entries[n] = d
    else:
        errors.append("missing .manifest.sha256 (run verify --update after seeding raw/)")

    for name, digest in sorted(entries.items()):
        path = raw / name
        if not path.is_file():
            errors.append(f"manifest lists missing file: {name}")
            continue
        actual = sha256_file(path)
        if actual != digest:
            errors.append(f"hash mismatch: {name}")
    for p in files:
        if p.name not in entries:
            errors.append(f"raw file not in manifest: {p.name}")

    if index.is_file():
        idx = index.read_text(encoding="utf-8")
        for p in files:
            if f"`{p.name}`" not in idx and p.name not in idx:
                errors.append(f"raw file not indexed: {p.name}")
    else:
        errors.append("missing source index.md")

    wiki = None
    for c in (raw.parent / "wiki", raw.parent.parent / "wiki", root / "wiki"):
        if c.is_dir():
            wiki = c
            break
    if wiki:
        for page in wiki.rglob("*.md"):
            if page.name.lower() in {"index.md", "overview.md", "readme.md"}:
                continue
            body = page.read_text(encoding="utf-8")
            low = body.lower()
            if "sources:" not in low and "unsourced:" not in low:
                errors.append(f"wiki page missing sources:/unsourced: {page.relative_to(root)}")

    if errors:
        print("VERIFY FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print(f"VERIFY OK ({len(files)} raw files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
