#!/usr/bin/env python3
"""Score a workspace against the human prompt's intent — not a hardcoded tree.

Properties are derived only from Prompt A/C in HUMAN_PROMPTS.md:
- coding projects
- notes
- research / second brain structure
- human + agent navigation
- immutable sources vs growing wiki
- README day-to-day guide

Path names are flexible; content/contracts matter.
Exit 0 if pass_threshold met, else 1.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PASS_SCORE = 85.0  # out of 100


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def all_files(root: Path) -> list[Path]:
    skip = {".git", "__pycache__", ".pytest_cache", "node_modules", ".agents", ".claude"}
    out: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in skip for part in p.parts):
            continue
        out.append(p)
    return out


def corpus(root: Path) -> str:
    chunks: list[str] = []
    for p in all_files(root):
        if p.suffix.lower() in {".md", ".txt", ""} or p.name in {"AGENTS.md", "CLAUDE.md", "README.md"}:
            chunks.append(f"\n# FILE {p.relative_to(root)}\n{read_text(p)}")
    return "\n".join(chunks).lower()


def find_readme(root: Path) -> Path | None:
    for name in ("README.md", "readme.md"):
        p = root / name
        if p.is_file():
            return p
    return None


def find_agent_entry(root: Path) -> list[Path]:
    found = []
    for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        p = root / name
        if p.is_file():
            found.append(p)
    return found


def dir_named_like(root: Path, patterns: list[str]) -> list[Path]:
    hits = []
    for p in root.rglob("*"):
        if not p.is_dir():
            continue
        if any(part.startswith(".") for part in p.relative_to(root).parts):
            continue
        name = p.name.lower()
        if any(re.search(pat, name) for pat in patterns):
            hits.append(p)
    return hits


def score_workspace(root: Path) -> dict:
    root = root.resolve()
    text = corpus(root)
    checks: list[dict] = []

    def add(id_: str, weight: float, ok: bool, detail: str) -> None:
        checks.append({"id": id_, "weight": weight, "ok": ok, "detail": detail})

    # --- From Prompt A ---
    projects = dir_named_like(root, [r"^projects?$", r"^code$", r"^repos?$"])
    add(
        "projects_shelf",
        12,
        bool(projects),
        f"found={ [str(p.relative_to(root)) for p in projects[:5]] }",
    )

    notes = dir_named_like(root, [r"^notes?$", r"^zettel", r"^journal$"])
    # notes must not be only inside an 'immutable' raw/sources-only story without a notes path
    add(
        "notes_shelf",
        12,
        bool(notes),
        f"found={ [str(p.relative_to(root)) for p in notes[:5]] }",
    )

    sources = dir_named_like(root, [r"^raw$", r"^sources?$", r"^corpus$", r"^evidence$"])
    add(
        "immutable_sources_area",
        14,
        bool(sources),
        f"found={ [str(p.relative_to(root)) for p in sources[:8]] }",
    )

    wiki = dir_named_like(root, [r"^wiki$", r"^brain$", r"^knowledge$"])
    # Prefer an explicit wiki dir; knowledge alone is weaker but counts if wiki language present
    wiki_ok = any(p.name.lower() == "wiki" for p in wiki) or (
        bool(wiki) and ("wiki" in text and "immutable" in text)
    )
    add(
        "growing_wiki_area",
        14,
        wiki_ok,
        f"found={ [str(p.relative_to(root)) for p in wiki[:8]] }",
    )

    immut = any(
        phrase in text
        for phrase in (
            "immutable",
            "write-once",
            "write once",
            "do not rewrite",
            "never rewrite",
            "must not edit",
            "must not overwrite",
        )
    )
    add("immutability_contract", 10, immut, "contract language present in durable files")

    separate = False
    if sources and wiki_ok:
        # sources path and wiki path should not be the same directory
        source_set = {p.resolve() for p in sources}
        wiki_dirs = [p for p in dir_named_like(root, [r"^wiki$"])] or wiki
        separate = all(w.resolve() not in source_set for w in wiki_dirs) if wiki_dirs else False
        # also raw nested under knowledge with wiki sibling is fine
        if not separate and wiki_dirs and sources:
            separate = True  # distinct matched dirs exist
    add("sources_wiki_separation", 10, separate and immut, "distinct source vs wiki areas + immutability")

    agent_files = find_agent_entry(root)
    agent_nav = bool(agent_files) and any(
        k in read_text(agent_files[0]).lower()
        for k in ("rout", "load only", "directory", "where", "do not", "map")
    )
    add("agent_navigation", 10, agent_nav, f"entry={[p.name for p in agent_files]}")

    readme = find_readme(root)
    readme_text = read_text(readme).lower() if readme else ""
    day = bool(readme) and any(
        k in readme_text for k in ("day to day", "day-to-day", "daily", "how to", "capture", "when you")
    )
    add("readme_day_to_day", 10, day, f"readme={readme.name if readme else None}")

    # research / second brain signal: indexes or knowledge routing
    researchish = any(
        k in text for k in ("research", "second brain", "knowledge", "ingest", "source index", "wiki/index")
    ) or bool(dir_named_like(root, [r"^research$", r"^resources?$", r"^areas?$"]))
    add("research_second_brain_structure", 8, researchish, "structured knowledge/research affordance")

    # Notes must be epistemically distinct from immutable sources when both exist
    notes_not_raw = True
    if notes and sources:
        for n in notes:
            # fail if the only notes dir is inside raw/ and marked immutable without human-owned language
            rel = str(n.relative_to(root)).lower()
            if "/raw/" in f"/{rel}/" or rel.endswith("/raw") or "/raw/" in rel + "/":
                if "human" not in text and "do not rewrite" in text:
                    notes_not_raw = False
    human_notes = ("human" in text and "note" in text) or ("notes/" in text and "immutable" in text)
    add(
        "notes_distinct_from_sources",
        10,
        bool(notes) and notes_not_raw and (human_notes or "note" in text),
        "notes shelf distinct; human-owned signal preferred",
    )

    # --- Intent consequences (still not a hardcoded tree) ---
    # "immutable" is a boundary claim: require a checkable mechanism OR
    # an explicit supersession protocol (keep old + add new), not prose alone.
    has_hash_manifest = any(
        p.name in {".manifest.sha256", "manifest.sha256", ".hashes", "SHA256SUMS"}
        or p.name.endswith(".sha256")
        for p in all_files(root)
    )
    has_verify_tool = any(
        p.name in {"verify", "lint-knowledge", "check-sources"}
        or (p.parent.name in {"bin", "scripts"} and "verif" in p.name.lower())
        for p in all_files(root)
    )
    supersede = any(
        k in text
        for k in ("supersede", "supersession", "do not overwrite", "keep the old", "new source")
    )
    add(
        "checkable_or_supersession_immutability",
        12,
        has_hash_manifest or has_verify_tool or (immut and supersede),
        f"manifest={has_hash_manifest} verify_tool={has_verify_tool} supersede={supersede}",
    )

    # Fresh-session survival: prove the loop with at least one real source body
    # and one synthesis page that cites it — empty scaffolds fail "structured so
    # it's easy … for agents" because agents cannot pattern-match an empty recipe.
    source_bodies = []
    for sdir in sources:
        if sdir.is_dir():
            for p in sdir.rglob("*"):
                if p.is_file() and p.suffix.lower() in {".md", ".txt", ".pdf", ".html"} and p.stat().st_size > 40:
                    if p.name not in {"README.md", ".gitkeep"} and not p.name.startswith("."):
                        source_bodies.append(p)
    wiki_pages = []
    for wdir in dir_named_like(root, [r"^wiki$"]):
        for p in wdir.rglob("*.md"):
            if p.name.lower() in {"index.md", "overview.md", "readme.md"}:
                continue
            if p.stat().st_size > 80:
                wiki_pages.append(p)
    citation = False
    if source_bodies and wiki_pages:
        names = {p.name for p in source_bodies} | {p.stem for p in source_bodies}
        for page in wiki_pages:
            body = read_text(page)
            if "sources:" in body.lower() or any(n in body for n in names):
                citation = True
                break
    add(
        "worked_example_chain",
        12,
        bool(source_bodies) and bool(wiki_pages) and citation,
        f"sources={len(source_bodies)} wiki_pages={len(wiki_pages)} citation={citation}",
    )

    # Operable without inventing mandatory external skill modes for daily use
    skill_lock_in = bool(
        re.search(
            r"(?i)(must|required|need to).{0,40}(cca|icm).{0,40}(skill|mode|ingest)",
            text,
        )
    ) or bool(re.search(r"(?i)use cca (in )?ingest mode", text))
    add(
        "self_describing_no_mandatory_skill",
        8,
        not skill_lock_in,
        f"mandatory_skill_language={skill_lock_in}",
    )

    # Capture affordance: inbox and/or capture tool (BASB capture implied by second brain)
    inbox = dir_named_like(root, [r"^inbox$", r"^capture$"])
    capture_tool = any(p.name == "capture" for p in all_files(root))
    add(
        "capture_affordance",
        6,
        bool(inbox) or capture_tool,
        f"inbox={bool(inbox)} capture_tool={capture_tool}",
    )

    # Contradictions survive (needed once wiki grows from multiple sources)
    contra = any(k in text for k in ("contradict", "disagreement", "do not silently", "preserve both"))
    add("contradiction_policy", 6, contra, "contradiction/preservation language present")

    # --- ICM skeleton / cold-agent isomorphism (path-flexible) ---
    agent_blob = "\n".join(read_text(p) for p in agent_files).lower()
    skeleton_map = (
        "skeleton map" in agent_blob
        or "l1 workspace router" in agent_blob
        or ("l2 folder contract" in agent_blob and "context.md" in agent_blob)
    )
    add(
        "skeleton_map_in_entry",
        10,
        skeleton_map,
        "L0 declares role→path map (or equivalent) so agents do not assume filenames",
    )

    contract_files = [
        p
        for p in all_files(root)
        if p.name.lower() in {"context.md", "purpose.md", "router.md"}
        or (p.name.upper() == "AGENTS.MD" and p.parent != root)
    ]
    shaped = 0
    for p in contract_files:
        body = read_text(p).lower()
        if (
            "inputs" in body
            and "process" in body
            and "outputs" in body
            and ("human check" in body or "human gate" in body)
        ):
            shaped += 1
    # Root L1 router may omit Human check; require several working-folder contracts
    add(
        "folder_contracts_icm_shape",
        12,
        shaped >= 4,
        f"contracts_with_inputs_process_outputs_human_check={shaped}",
    )

    templates = dir_named_like(root, [r"^_templates$", r"^templates$"])
    stamp_files = []
    for tdir in templates:
        for p in tdir.rglob("*"):
            if p.is_file() and p.stat().st_size > 20 and p.name not in {".gitkeep"}:
                stamp_files.append(p)
    add(
        "live_factory_stamps",
        8,
        len(stamp_files) >= 2,
        f"template_dirs={len(templates)} stamp_files={len(stamp_files)}",
    )

    status_scan = any(
        k in text
        for k in (
            "status scan",
            "without memory",
            "status without",
            "scan surfaces",
            "current state",
        )
    ) or ("log.md" in text and "index.md" in text and "status" in text)
    add(
        "status_without_memory",
        6,
        status_scan,
        "declared status scan surface for cold agents",
    )

    earned = sum(c["weight"] for c in checks if c["ok"])
    total = sum(c["weight"] for c in checks)
    score = round(100.0 * earned / total, 2) if total else 0.0

    return {
        "root": str(root),
        "score": score,
        "pass": score >= PASS_SCORE,
        "pass_threshold": PASS_SCORE,
        "earned": earned,
        "total_weight": total,
        "checks": checks,
    }


def assert_prompt_not_in_skill(skill_root: Path) -> dict:
    needles = [
        "immutable and the wiki that grows",
        "idk, do what you consider whats best",
        "ill continue on a new session",
    ]
    hits = []
    for p in skill_root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".txt", ".py", ".json"}:
            continue
        body = read_text(p)
        for n in needles:
            if n.lower() in body.lower():
                hits.append({"file": str(p), "needle": n})
    return {"ok": not hits, "hits": hits}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--skill", default="")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()
    result = score_workspace(Path(args.workspace))
    if args.skill:
        result["prompt_not_in_skill"] = assert_prompt_not_in_skill(Path(args.skill))
        if not result["prompt_not_in_skill"]["ok"]:
            result["pass"] = False
    print(json.dumps(result, indent=2))
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
