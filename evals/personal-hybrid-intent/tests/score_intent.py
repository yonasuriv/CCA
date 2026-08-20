#!/usr/bin/env python3
"""Score a personal-hybrid workspace against user intent and CCA invariants.

The scorer is deliberately path-flexible. It rewards usable separation of
projects, human notes, preserved evidence, maintained knowledge, capture, and
bounded navigation. It does not require an ICM-shaped skeleton unless the target
independently claims one.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PASS_SCORE = 85.0


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def all_files(root: Path) -> list[Path]:
    skip = {".git", "__pycache__", ".pytest_cache", "node_modules", ".agents", ".claude"}
    out: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file() and not any(part in skip for part in path.parts):
            out.append(path)
    return out


def corpus(root: Path) -> str:
    chunks: list[str] = []
    for path in all_files(root):
        if path.suffix.lower() in {".md", ".txt", ""} or path.name in {"AGENTS.md", "CLAUDE.md", "README.md"}:
            chunks.append(f"\n# FILE {path.relative_to(root)}\n{read_text(path)}")
    return "\n".join(chunks).lower()


def find_readme(root: Path) -> Path | None:
    for name in ("README.md", "readme.md"):
        path = root / name
        if path.is_file():
            return path
    return None


def find_agent_entries(root: Path) -> list[Path]:
    return [root / name for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md") if (root / name).is_file()]


def dirs_matching(root: Path, patterns: list[str]) -> list[Path]:
    hits: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_dir():
            continue
        rel = path.relative_to(root)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if any(re.search(pattern, path.name.lower()) for pattern in patterns):
            hits.append(path)
    return hits


def score_workspace(root: Path) -> dict:
    root = root.resolve()
    text = corpus(root)
    checks: list[dict] = []

    def add(id_: str, weight: float, ok: bool, detail: str) -> None:
        checks.append({"id": id_, "weight": weight, "ok": ok, "detail": detail})

    projects = dirs_matching(root, [r"^projects?$", r"^code$", r"^repos?$"])
    notes = dirs_matching(root, [r"^notes?$", r"^zettel", r"^journal$"])
    sources = dirs_matching(root, [r"^raw$", r"^sources?$", r"^corpus$", r"^evidence$", r"^references?$"])
    knowledge = dirs_matching(root, [r"^wiki$", r"^knowledge$", r"^synthesis$"])

    add("projects_home", 10, bool(projects), f"found={[str(p.relative_to(root)) for p in projects[:5]]}")
    add("human_notes_home", 10, bool(notes), f"found={[str(p.relative_to(root)) for p in notes[:5]]}")
    add("source_reference_home", 10, bool(sources), f"found={[str(p.relative_to(root)) for p in sources[:8]]}")
    add("maintained_knowledge_home", 10, bool(knowledge), f"found={[str(p.relative_to(root)) for p in knowledge[:8]]}")

    preserved = any(
        phrase in text
        for phrase in (
            "immutable",
            "write-once",
            "write once",
            "do not rewrite",
            "never rewrite",
            "must not overwrite",
            "preserved evidence",
        )
    )
    supersede = any(phrase in text for phrase in ("supersede", "supersession", "keep the old", "preserve the old"))
    add("source_preservation", 8, preserved, "preservation language present")
    add("source_correction_path", 6, preserved and supersede, "preserved material has supersession/correction path")

    separate = bool(sources and knowledge) and not ({p.resolve() for p in sources} & {p.resolve() for p in knowledge})
    add("sources_vs_synthesis_separation", 8, separate, "source and maintained-knowledge homes are distinct")

    notes_distinct = bool(notes) and not ({p.resolve() for p in notes} & {p.resolve() for p in sources})
    human_note_signal = "human" in text and any(word in text for word in ("note", "zettel", "thinking"))
    add("notes_distinct_from_evidence", 8, notes_distinct and human_note_signal, "human thinking is not raw evidence")

    inbox = dirs_matching(root, [r"^inbox$", r"^capture$"])
    capture_tool = any(path.name == "capture" for path in all_files(root))
    add("capture_affordance", 5, bool(inbox) or capture_tool, f"inbox={bool(inbox)} capture_tool={capture_tool}")

    entries = find_agent_entries(root)
    entry_text = "\n".join(read_text(path).lower() for path in entries)
    nav_signal = bool(entries) and any(word in entry_text for word in ("route", "directory", "where", "index", "catalog", "load"))
    add("durable_navigation_entry", 8, nav_signal, f"entries={[p.name for p in entries]}")

    bounded_route = (
        any(term in text for term in ("route before search", "targeted search", "local index", "local catalog", "scoped search", "bounded search"))
        and any(term in text for term in ("fallback", "broad search", "grep", "search only", "search within"))
    )
    add("bounded_route_before_search", 9, bounded_route, "navigation narrows scope before broad search")

    global_manifest_required = bool(
        re.search(r"(?i)(must|required|always).{0,50}(root|global).{0,30}(manifest|index).{0,40}(every|all).{0,20}(file|document)", text)
    )
    add("no_global_manifest_dependency", 5, not global_manifest_required, f"global_manifest_required={global_manifest_required}")

    readme = find_readme(root)
    readme_text = read_text(readme).lower() if readme else ""
    day_to_day = bool(readme) and any(term in readme_text for term in ("day to day", "day-to-day", "daily", "how to", "capture", "when you"))
    add("readme_day_to_day", 6, day_to_day, f"readme={readme.name if readme else None}")

    researchish = any(term in text for term in ("research", "second brain", "knowledge", "source index", "maintained synthesis"))
    add("research_second_brain_structure", 5, researchish, "knowledge/research affordance is described")

    has_hash_manifest = any(
        path.name in {".manifest.sha256", "manifest.sha256", ".hashes", "SHA256SUMS"} or path.name.endswith(".sha256")
        for path in all_files(root)
    )
    has_verify_tool = any(
        path.name in {"verify", "lint-knowledge", "check-sources"}
        or (path.parent.name in {"bin", "scripts"} and "verif" in path.name.lower())
        for path in all_files(root)
    )
    add(
        "checkable_or_supersession_preservation",
        5,
        has_hash_manifest or has_verify_tool or (preserved and supersede),
        f"manifest={has_hash_manifest} verify_tool={has_verify_tool} supersede={supersede}",
    )

    source_bodies: list[Path] = []
    for directory in sources:
        for path in directory.rglob("*"):
            if path.is_file() and path.name not in {"README.md", ".gitkeep"} and not path.name.startswith("."):
                try:
                    if path.stat().st_size > 40:
                        source_bodies.append(path)
                except OSError:
                    pass

    knowledge_pages: list[Path] = []
    for directory in knowledge:
        for path in directory.rglob("*.md"):
            if path.name.lower() not in {"index.md", "overview.md", "readme.md"}:
                try:
                    if path.stat().st_size > 80:
                        knowledge_pages.append(path)
                except OSError:
                    pass

    citation = False
    if source_bodies and knowledge_pages:
        names = {p.name for p in source_bodies} | {p.stem for p in source_bodies}
        for page in knowledge_pages:
            body = read_text(page)
            if "sources:" in body.lower() or any(name in body for name in names):
                citation = True
                break
    add("worked_source_to_knowledge_chain", 5, bool(source_bodies) and bool(knowledge_pages) and citation, f"sources={len(source_bodies)} knowledge_pages={len(knowledge_pages)} citation={citation}")

    contradiction_policy = any(term in text for term in ("contradict", "disagreement", "preserve both", "do not silently overwrite"))
    add("contradiction_policy", 4, contradiction_policy, "contradiction/preservation language present")

    skill_lock_in = bool(
        re.search(r"(?i)(must|required|need to).{0,40}(cca|icm).{0,40}(skill|mode|ingest)", text)
    ) or bool(re.search(r"(?i)use cca (in )?ingest mode", text))
    add("self_describing_without_mandatory_skill", 4, not skill_lock_in, f"mandatory_skill_language={skill_lock_in}")

    # A generic personal hybrid must not earn points for claiming native ICM or
    # requiring ICM-shaped contracts. If it does claim native ICM, the native
    # boundary should at least expose its real bootstrap rather than a CCA alias.
    claims_native_icm = "upstream-native icm" in text or "native icm" in text
    native_bootstrap = (root / "CLAUDE.md").is_file() and (root / "CONTEXT.md").is_file()
    add("profile_claim_honesty", 4, (not claims_native_icm) or native_bootstrap, f"claims_native_icm={claims_native_icm} native_bootstrap={native_bootstrap}")

    earned = sum(check["weight"] for check in checks if check["ok"])
    total = sum(check["weight"] for check in checks)
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
    for path in skill_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".py", ".json"}:
            continue
        body = read_text(path)
        for needle in needles:
            if needle.lower() in body.lower():
                hits.append({"file": str(path), "needle": needle})
    return {"ok": not hits, "hits": hits}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    parser.add_argument("--skill", default="")
    parser.add_argument("--json-out", default="")
    args = parser.parse_args()

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
