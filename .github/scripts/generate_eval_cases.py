#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "evals" / "cases"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def write_case(slug: str, manifest: dict, prompt: str, fixture: dict[str, str], assertions: list[dict]) -> None:
    case = CASES / slug
    if case.exists():
        shutil.rmtree(case)
    (case / "fixture").mkdir(parents=True)
    (case / "case.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (case / "prompt.md").write_text(prompt.strip() + "\n", encoding="utf-8")
    for rel, content in fixture.items():
        path = case / "fixture" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    (case / "assertions.json").write_text(json.dumps({"assertions": assertions}, indent=2) + "\n", encoding="utf-8")


def m(i: int, name: str, baseline: str, profiles: list[str], behavior: str) -> dict:
    return {"id": f"{i:02d}", "name": name, "baseline": baseline, "profiles": profiles, "expected_behavior": behavior}


write_case(
    "01-native-icm",
    m(1, "Native ICM repair", "icm", ["native-icm"], "Repair native contract drift while preserving native Layer-0 authority."),
    "Repair this native ICM workspace. Preserve its native entry semantics and change only what is required for native compatibility. Do not replace the native CLAUDE.md with a CCA preference.",
    {
        "CLAUDE.md": "# Native ICM Entry\n\nNATIVE-OWNER: keep-this-rule\n",
        "CONTEXT.md": "# Router\n\nRoute work to stages/01-research/.\n",
        "stages/01-research/CONTEXT.md": "## Inputs\n\n| File | Section to Load | Why |\n|---|---|---|\n| ../../sources.md | Full file | Evidence |\n\n## Process\n\n1. Research.\n\n## Outputs\n\n| Artifact | Location | Format |\n|---|---|---|\n| Notes | output/notes.md | Markdown |\n",
        "stages/01-research/output/.gitkeep": "",
        "sources.md": "Evidence.\n",
    },
    [
        {"type": "file_contains", "path": "CLAUDE.md", "text": "NATIVE-OWNER: keep-this-rule"},
        {"type": "file_contains", "path": "stages/01-research/CONTEXT.md", "text": "| Source | File/Location | Section/Scope | Why |"},
        {"type": "path_exists", "path": "CONTEXT.md"},
    ],
)

write_case(
    "02-icm-derived-pipeline",
    m(2, "ICM-derived pipeline repair", "icm", ["icm-derived", "ordinary-project"], "Repair borrowed stage mechanics without promoting the host project to native ICM."),
    "Fix the ICM-derived stage contract in this ordinary project. Keep it explicitly derived; do not add native-Icm-only scaffolding merely to make it look complete.",
    {
        "README.md": "# Data tool\n\nThis project borrows ICM stage contracts; it is not a native ICM workspace.\n",
        "src/app.py": "print('app')\n",
        "stages/01-plan/CONTEXT.md": "## Inputs\n\n| File | Section to Load | Why |\n|---|---|---|\n| ../../README.md | Full file | Scope |\n\n## Process\n\n1. Plan.\n\n## Outputs\n\n| Artifact | Location | Format |\n|---|---|---|\n| Plan | output/plan.md | Markdown |\n",
        "stages/01-plan/output/.gitkeep": "",
    },
    [
        {"type": "file_contains", "path": "stages/01-plan/CONTEXT.md", "text": "| Source | File/Location | Section/Scope | Why |"},
        {"type": "path_absent", "path": "CLAUDE.md"},
        {"type": "file_contains", "path": "README.md", "text": "not a native ICM workspace"},
    ],
)

app3 = "def add(a, b):\n    return a + b\n"
write_case(
    "03-existing-code-repo",
    m(3, "Existing healthy code repository", "none", ["ordinary-project"], "Preserve healthy code structure; add only routing that solves a demonstrated need."),
    "Make this repository easier for agents to work in without restructuring application code. If its current structure is already sufficient, prefer a no-op or minimal portable guidance over new methodology folders.",
    {"README.md": "# Small library\n\nRun tests with python -m unittest.\n", "src/app.py": app3, "tests/test_app.py": "# existing tests\n"},
    [
        {"type": "sha256_equals", "path": "src/app.py", "sha256": digest(app3)},
        {"type": "path_absent", "path": "stages"},
        {"type": "path_absent", "path": "wiki"},
    ],
)

app4 = "def total(items):\n    return sum(items)\n"
write_case(
    "04-code-repo-scrum",
    m(4, "Code repository with Scrum authority", "none", ["ordinary-project", "scrum"], "Keep Scrum as process authority and code as code; route between artifacts without filesystem-implementing Scrum."),
    "Improve agent orientation in this software repository. The team uses Scrum and its backlog/process file is authoritative. Do not turn Scrum ceremonies or roles into a CCA folder schema.",
    {"src/service.py": app4, "PROCESS.md": "# Scrum\n\nProduct backlog: backlog.md\nSprint work is selected by the team.\n", "backlog.md": "# Product Backlog\n\n- Improve totals\n"},
    [
        {"type": "sha256_equals", "path": "src/service.py", "sha256": digest(app4)},
        {"type": "path_exists", "path": "backlog.md"},
        {"type": "path_absent", "path": "Scrum"},
        {"type": "path_absent", "path": "stages"},
    ],
)

write_case(
    "05-para-second-brain",
    m(5, "PARA second brain", "none", ["para"], "Preserve PARA actionability categories and add only useful routing."),
    "Make this PARA second brain easier for an agent to navigate. Preserve Projects, Areas, Resources, and Archives as the human organization; do not duplicate those obvious paths into a new manifest.",
    {"Projects/site-redesign.md": "Outcome: launch redesign.\n", "Areas/health.md": "Ongoing responsibility.\n", "Resources/css.md": "Reference.\n", "Archives/old-project.md": "Inactive.\n"},
    [
        {"type": "path_exists", "path": "Projects/site-redesign.md"},
        {"type": "path_exists", "path": "Areas/health.md"},
        {"type": "path_exists", "path": "Resources/css.md"},
        {"type": "path_exists", "path": "Archives/old-project.md"},
        {"type": "path_absent", "path": "cca.yaml"},
    ],
)

zettel = "# Context routing\n\nHuman-authored note. Links: [[progressive-disclosure]].\n"
write_case(
    "06-para-zettelkasten",
    m(6, "PARA plus Zettelkasten", "none", ["para", "zettelkasten"], "Preserve outer actionability and inner linked-note/write-authority semantics."),
    "Add agent orientation without converting the Zettelkasten into an agent-written wiki. Treat the note as human-authored source unless local instructions say otherwise.",
    {"Projects/research.md": "Outcome: publish note.\n", "Areas/.gitkeep": "", "Resources/zettelkasten/context-routing.md": zettel, "Resources/zettelkasten/progressive-disclosure.md": "# Progressive disclosure\n", "Archives/.gitkeep": ""},
    [
        {"type": "sha256_equals", "path": "Resources/zettelkasten/context-routing.md", "sha256": digest(zettel)},
        {"type": "path_absent", "path": "Resources/zettelkasten/wiki"},
    ],
)

wiki_index = "# Wiki\n\n- [Routing](routing.md)\n"
write_case(
    "07-llm-wiki",
    m(7, "Existing LLM Wiki", "none", ["llm-wiki"], "Preserve implementation-defined maintained-synthesis behavior before optional CCA hardening."),
    "Inspect this maintained LLM Wiki and improve only what is necessary for reliable use. Preserve its existing schema; do not force a CCA raw/wiki taxonomy or metadata just because CCA has optional hardened forms.",
    {"SOURCES/source-a.md": "Raw evidence A.\n", "KNOWLEDGE/index.md": wiki_index, "KNOWLEDGE/routing.md": "# Routing\n\nMaintained synthesis.\n", "INSTRUCTIONS.md": "Update KNOWLEDGE from SOURCES; keep synthesis persistent across sessions.\n"},
    [
        {"type": "sha256_equals", "path": "KNOWLEDGE/index.md", "sha256": digest(wiki_index)},
        {"type": "path_exists", "path": "SOURCES/source-a.md"},
        {"type": "path_absent", "path": "raw"},
    ],
)

write_case(
    "08-llm-wiki-icm",
    m(8, "LLM Wiki plus native ICM", "icm", ["llm-wiki", "native-icm", "hybrid"], "Keep synthesis and staged workflow as distinct nested authorities with explicit routing between them."),
    "Orient this hybrid workspace. The knowledge base is maintained synthesis; workflow/ is a native ICM root. Preserve both schemas and make cross-boundary consumption clear without merging them.",
    {"knowledge/SOURCES/a.md": "Evidence.\n", "knowledge/KNOWLEDGE/index.md": "# Maintained synthesis\n", "workflow/CLAUDE.md": "# Native workflow entry\n", "workflow/CONTEXT.md": "# Workflow router\n", "workflow/stages/01-use-knowledge/CONTEXT.md": "## Inputs\n\n| Source | File/Location | Section/Scope | Why |\n|---|---|---|---|\n| Knowledge | ../../../knowledge/KNOWLEDGE/index.md | Full file | Maintained synthesis |\n\n## Process\n\n1. Use routed knowledge.\n\n## Outputs\n\n| Artifact | Location | Format |\n|---|---|---|\n| Result | output/result.md | Markdown |\n", "workflow/stages/01-use-knowledge/output/.gitkeep": ""},
    [
        {"type": "path_exists", "path": "knowledge/KNOWLEDGE/index.md"},
        {"type": "path_exists", "path": "workflow/CLAUDE.md"},
        {"type": "path_exists", "path": "workflow/stages/01-use-knowledge/CONTEXT.md"},
        {"type": "path_absent", "path": "knowledge/stages"},
    ],
)

write_case(
    "09-record-library",
    m(9, "Record Library", "icm-architect", ["record-library"], "Create a record from the declared template/schema, update one catalog authority, and avoid half-created records."),
    "Add a new client record for Beta Corp using this library's template. Keep id/status authority in index.md. Do not start a blank record or invent a second lifecycle source.",
    {"index.md": "# Clients\n\n| id | name | status |\n|---|---|---|\n| acme | Acme | active |\n", "record-template/profile.md": "# {{name}}\n\nid: {{id}}\nstatus: {{status}}\nowner: {{owner}}\n", "acme/profile.md": "# Acme\n\nid: acme\nstatus: active\nowner: team-a\n"},
    [
        {"type": "path_exists", "path": "beta-corp/profile.md"},
        {"type": "file_contains", "path": "beta-corp/profile.md", "text": "id: beta-corp"},
        {"type": "file_contains", "path": "beta-corp/profile.md", "text": "status:"},
        {"type": "file_contains", "path": "index.md", "text": "beta-corp"},
    ],
)

write_case(
    "10-context-map",
    m(10, "Context Map", "icm-architect", ["context-map"], "Represent organizational/process/information relationships with operational fields and evidence discipline."),
    "Extend this context map with a recurring intake workflow observed three times per week. Record frequency and evidence without turning the map into a source-code impact map.",
    {"map/schema.md": "# Schema\n\nnode types: team, workflow, system, decision\n", "map/workflows/intake.md": "# Intake\n\nowner: ops\n\n## Inputs\nrequests\n\n## Outputs\ntriaged requests\n", "observations.md": "Mon: intake observed\nWed: intake observed\nFri: intake observed\n"},
    [
        {"type": "file_contains", "path": "map/workflows/intake.md", "text": "frequency"},
        {"type": "file_contains", "path": "map/workflows/intake.md", "text": "observations.md"},
        {"type": "path_absent", "path": "map/effects"},
    ],
)

write_case(
    "11-system-map",
    m(11, "System Map", "icm-architect", ["system-map"], "Build a source-backed change-impact map for a mutable code tree without duplicating source."),
    "Map this codebase for change-impact reasoning. Distinguish live/leftover/ghost material, cite source paths, record Hits/Does not hit, and create only shelves justified by verified content.",
    {"src/models.py": "class User:\n    pass\n", "src/auth.py": "from .models import User\n\ndef login(user: User):\n    return True\n", "legacy/old_auth.py": "# leftover legacy path\n", "docs/future.md": "Ghost: planned Billing model does not exist yet.\n"},
    [
        {"type": "path_exists", "path": "map/CONTEXT.md"},
        {"type": "path_exists", "path": "map/objects"},
        {"type": "path_exists", "path": "map/effects/CONTEXT.md"},
        {"type": "file_contains", "path": "map/CONTEXT.md", "text": "live"},
        {"type": "file_contains", "path": "map/CONTEXT.md", "text": "ghost"},
    ],
)

write_case(
    "12-hybrid-workspace",
    m(12, "Hybrid nested authorities", "icm", ["para", "native-icm", "ordinary-project", "llm-wiki", "hybrid"], "Route across nested authorities while leaving each independently interpretable."),
    "Add the smallest useful top-level orientation for this hybrid workspace. Do not flatten the native ICM assessment, code repository, PARA organization, or maintained wiki into one schema.",
    {"Projects/client/assessment/CLAUDE.md": "# Native assessment\n", "Projects/client/assessment/CONTEXT.md": "# Router\n", "Projects/client/code/src/app.py": "print('client')\n", "Areas/.gitkeep": "", "Resources/wiki/INSTRUCTIONS.md": "Maintain synthesis here.\n", "Resources/wiki/index.md": "# Wiki\n", "Archives/.gitkeep": ""},
    [
        {"type": "path_exists", "path": "Projects/client/assessment/CLAUDE.md"},
        {"type": "path_exists", "path": "Projects/client/code/src/app.py"},
        {"type": "path_exists", "path": "Resources/wiki/index.md"},
        {"type": "path_absent", "path": "Projects/client/code/stages"},
    ],
)

write_case(
    "13-approved-restructure",
    m(13, "Explicit approved restructure", "none", ["ordinary-project", "restructure"], "Apply only the explicitly approved move and repair navigation without opportunistic redesign."),
    "The user explicitly approved moving legacy/guide.md to docs/guide.md. Apply that move, preserve the content byte-for-byte, update README's pointer, and make no other structural changes.",
    {"README.md": "# Project\n\nGuide: legacy/guide.md\n", "legacy/guide.md": "# Guide\n\nCanonical content.\n", "src/app.py": "print('stable')\n"},
    [
        {"type": "path_exists", "path": "docs/guide.md"},
        {"type": "path_absent", "path": "legacy/guide.md"},
        {"type": "file_contains", "path": "README.md", "text": "docs/guide.md"},
        {"type": "file_contains", "path": "docs/guide.md", "text": "Canonical content."},
    ],
)

healthy = "print('healthy')\n"
ag = "# Agent guidance\n\nRead README.md, then relevant source/tests. No additional context structure is required.\n"
write_case(
    "14-no-op",
    m(14, "Already healthy no-op", "none", ["ordinary-project"], "Recognize that no structural change is required and avoid cosmetic CCA artifacts."),
    "Audit this repository for CCA usefulness. It is already small and explicitly routed. If no change materially improves navigation or maintenance, leave the filesystem unchanged and report a no-op.",
    {"AGENTS.md": ag, "README.md": "# Healthy tiny project\n", "src/app.py": healthy},
    [
        {"type": "sha256_equals", "path": "AGENTS.md", "sha256": digest(ag)},
        {"type": "sha256_equals", "path": "src/app.py", "sha256": digest(healthy)},
        {"type": "path_absent", "path": "CONTEXT.md"},
        {"type": "path_absent", "path": "stages"},
        {"type": "path_absent", "path": "wiki"},
        {"type": "glob_count", "pattern": "*", "count": 3},
    ],
)

print("generated 14 evaluation cases")
