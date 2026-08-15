#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"missing replacement anchor in {path}: {old[:80]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# 1. Runner suite selection.
runner = ROOT / "evals/runner.py"
text = runner.read_text(encoding="utf-8")
anchor = '''def load_case(case_dir: Path) -> dict[str, Any]:\n'''
helper = '''def suite_root(evals_root: Path, suite: str) -> Path:\n    mapping = {"core": "cases", "methodologies": "methodologies"}\n    try:\n        return evals_root / mapping[suite]\n    except KeyError as exc:\n        raise ValueError(f"unknown evaluation suite: {suite}") from exc\n\n\n'''
if "def suite_root(" not in text:
    text = text.replace(anchor, helper + anchor, 1)
text = text.replace(
    '    parser.add_argument("--case", required=True, help="Case directory or two-digit case id")\n',
    '    parser.add_argument("--suite", choices=("core", "methodologies"), default="core")\n'
    '    parser.add_argument("--case", required=True, help="Case directory or two-digit case id")\n',
    1,
)
text = text.replace(
    '    cases_root = Path(__file__).resolve().parent / "cases"\n',
    '    evals_root = Path(__file__).resolve().parent\n    cases_root = suite_root(evals_root, args.suite)\n',
    1,
)
runner.write_text(text, encoding="utf-8")

# 2. Record Library regression fix.
forms = ROOT / "skills/cca/references/architect/forms.md"
old_record = """For a fresh Record Library, treat the record template as the schema and creation source: every new record starts by copying the template, then replacing declared fields; never create a blank record and reconstruct the shape from memory. If identifiers or lifecycle status exist, declare one catalog as their authority and make record-local copies derived/readable rather than competing authorities. Keep lifecycle deliberately small (for example `draft → active → archived`) unless the domain already defines one. A record is half-created when its catalog entry exists without the required template-derived body, or the body exists without the required catalog identity; lint/sync should report that state rather than silently guessing. Detect schema drift by comparing required template fields/sections against records, while preserving an existing library's own schema and lifecycle instead of imposing these defaults."""
new_record = """For a fresh Record Library, treat the record template as the schema and creation source: every new record starts by copying the template, then replacing declared fields; never create a blank record and reconstruct the shape from memory. If identifiers or lifecycle status exist, declare one catalog as their authority and make record-local copies derived/readable rather than competing authorities. Explicit identifiers and declared catalog, template, schema, or domain rules always win. Only when no explicit identifier exists and the existing library clearly derives slug identifiers from the full display name, derive the fallback from the **full display name** rather than abbreviating or truncating it; under that evidenced convention, `Beta Corp` becomes `beta-corp`, not `beta`. Keep lifecycle deliberately small (for example `draft → active → archived`) unless the domain already defines one. A record is half-created when its catalog entry exists without the required template-derived body, or the body exists without the required catalog identity; lint/sync should report that state rather than silently guessing. Detect schema drift by comparing required template fields/sections against records, while preserving an existing library's own schema and lifecycle instead of imposing these defaults."""
replace_once(forms, old_record, new_record)

# 3. Methodology cases.
cases = [
    ("01-cynefin-sensemaking", "Cynefin sense-making", "The work has novel dependencies, unclear cause/effect, and stakeholder feedback changes the solution after experiments.", "Assess the delivery situation before recommending a method. Identify the relevant sense-making domain and write decision.md with Scope, Recommendation, Preserve, and Avoid.", ["complex", "probe"], ["safe/", "scrum/"]),
    ("02-enterprise-scaling", "Enterprise scaling choice", "Eight teams share one product. Leadership wants either more centralized coordination, organizational simplification, or guided contextual choice; regulatory boundaries prevent pretending all teams are identical.", "Compare SAFe, LeSS, and Disciplined Agile for this situation. Write decision.md with Scope, Recommendation, Preserve, and Avoid. Do not merge the three approaches into one framework.", ["SAFe", "LeSS", "Disciplined Agile"], ["scaled-agile/"]),
    ("03-sequential-constraints", "Sequential constraints", "A medical-device release has fixed certification gates, requirement-to-test traceability, hardware milestones, and evidence that must be produced in a defined order.", "Evaluate whether sequential delivery is justified. Write decision.md with Scope, Recommendation, Preserve, and Avoid, distinguishing waterfall/stage-gate/V-model concerns from iterative discovery.", ["V-model", "traceability"], ["sprints/"]),
    ("04-scrum-kanban-conflict", "Scrum and Kanban conflict", "The team currently uses two-week Scrum sprints, but half of incoming work is interrupt-driven production support and cannot wait for sprint planning.", "Advise on the Scrum/Kanban tension without pretending they are automatically identical. Write decision.md with Scope, Recommendation, Preserve, and Avoid.", ["Scrum", "Kanban"], ["scrum-kanban/"]),
    ("05-kanban-flow", "Kanban continuous flow", "Work arrives continuously, queues are hidden, WIP is high, and cycle time is unpredictable. There is no product requirement for sprint boundaries.", "Evaluate the delivery approach. Write decision.md with Scope, Recommendation, Preserve, and Avoid. Keep flow mechanics distinct from filesystem structure.", ["WIP", "flow"], ["sprints/"]),
    ("06-dsdm-governance", "DSDM governance", "A project has a hard delivery date, fixed budget envelope, active business representatives, and formal project governance, but requirements can be prioritized and refined iteratively.", "Evaluate DSDM-style governance for this project. Write decision.md with Scope, Recommendation, Preserve, and Avoid.", ["governance", "timebox"], ["dsdm/"]),
    ("07-fdd-feature-decomposition", "FDD feature decomposition", "A large business domain has a useful domain model and can be decomposed into small client-valued features, but platform and reliability work must remain visible too.", "Evaluate Feature-Driven Development as a decomposition/planning approach. Write decision.md with Scope, Recommendation, Preserve, and Avoid.", ["feature", "domain"], ["features/"]),
    ("08-asd-uncertainty", "ASD under uncertainty", "The product direction changes rapidly, plans are hypotheses, and the team must learn from experiments while retaining explicit decision constraints.", "Evaluate Adaptive Software Development. Write decision.md with Scope, Recommendation, Preserve, and Avoid.", ["speculate", "learn"], ["asd/"]),
    ("09-xp-engineering", "XP engineering practices", "A small product team releases frequently and needs technical practices that keep code safely changeable. Pairing is optional; test-first work, CI, refactoring, and simple design are under consideration.", "Evaluate XP at the correct scope. Write decision.md with Scope, Recommendation, Preserve, and Avoid; distinguish engineering practice coherence from organizational process.", ["XP", "refactor"], ["xp/"]),
    ("10-rad-prototyping", "RAD prototyping", "Users can give rapid feedback on prototypes, time-to-validation matters, and the team is at risk of letting prototypes silently become production architecture.", "Evaluate RAD. Write decision.md with Scope, Recommendation, Preserve, and Avoid, including the prototype-to-production risk.", ["prototype", "feedback"], ["rad/"]),
    ("11-iid-strategy", "IID strategy", "The system can be built and integrated in useful increments with feedback between cycles. The team does not use Scrum and does not want Scrum ceremonies implied.", "Evaluate iterative and incremental development without equating iteration with Scrum. Write decision.md with Scope, Recommendation, Preserve, and Avoid.", ["iterative", "incremental"], ["sprints/"]),
    ("12-lean-systems", "Lean systems thinking", "The organization wants shorter queues and better value flow but has begun labeling training, resilience capacity, and exploration as waste.", "Apply Lean reasoning at the correct scope. Write decision.md with Scope, Recommendation, Preserve, and Avoid, protecting system resilience from local efficiency dogma.", ["flow", "resilience"], ["lean/"]),
    ("13-rup-up-lifecycle", "RUP/UP lifecycle", "A complex system needs explicit architecture, early risk reduction, lifecycle coverage, and tailoring; the team wants to avoid instantiating every possible role and artifact.", "Evaluate RUP/UP as a configurable lifecycle process. Write decision.md with Scope, Recommendation, Preserve, and Avoid.", ["architecture", "risk"], ["rup/"]),
    ("14-devops-operations", "DevOps lifecycle", "Development and operations share responsibility for a service. Delivery, observability, recovery, and production feedback matter; management currently equates DevOps with buying a CI/CD tool.", "Evaluate DevOps at the correct scope. Write decision.md with Scope, Recommendation, Preserve, and Avoid; do not reduce it to tooling.", ["operations", "feedback"], ["devops/"]),
    ("15-tdd-practice", "TDD engineering practice", "A team wants executable feedback and testable design for a library. Leadership asks whether adopting TDD means replacing the team's delivery framework.", "Evaluate TDD at the correct scope. Write decision.md with Scope, Recommendation, Preserve, and Avoid.", ["engineering practice", "test"], ["tdd-process/"]),
    ("16-mde-paradigm", "MDE engineering paradigm", "The domain has stable high-level models and repetitive platform-specific realizations, but generator/toolchain complexity could become a second software system.", "Evaluate Model-Driven Engineering. Write decision.md with Scope, Recommendation, Preserve, and Avoid; do not treat MDE as a team delivery framework.", ["model", "abstraction"], ["mde-sprints/"]),
    ("17-psp-tsp-discipline", "PSP and TSP discipline", "Engineers want empirical estimation and defect feedback. Management must not turn personal/team process measurements into individual performance leaderboards.", "Evaluate PSP and TSP at their respective scopes. Write decision.md with Scope, Recommendation, Preserve, and Avoid.", ["PSP", "TSP"], ["leaderboard/"]),
    ("18-semat-essence", "SEMAT Essence method engineering", "Several teams use different methods and need a common vocabulary to compare and compose practices without rewriting every method into a mandatory new methodology.", "Evaluate SEMAT/Essence as a method-engineering/common-vocabulary layer. Write decision.md with Scope, Recommendation, Preserve, and Avoid.", ["Essence", "vocabulary"], ["unified-method/"]),
    ("19-cross-scope-composition", "Cross-scope composition", "A product team uses Scrum for cadence, XP engineering practices, DevOps for delivery/operations, and Lean systems thinking. Each currently solves a different problem.", "Advise whether these approaches can coexist. Write decision.md with Scope, Recommendation, Preserve, and Avoid. Preserve their distinct scopes rather than naming the combination as a new CCA methodology.", ["Scrum", "XP", "DevOps", "Lean"], ["cca-method/"]),
    ("20-ordinary-task-nontrigger", "Ordinary implementation non-trigger", "A small Python repository has one failing function and an existing README. The task is simply to fix the function and tests; no process change is requested.", "Fix the described implementation task using the smallest relevant intervention. Do not introduce methodology/process structure merely because CCA contains advisor material. Record any necessary explanation in result.md.", ["implementation"], ["decision.md", "scrum/", "kanban/", "safe/", "stages/"]),
]

method_root = ROOT / "evals/methodologies"
method_root.mkdir(parents=True, exist_ok=True)

readme = """# Methodology and framework evaluation suite

This suite is separate from the 14-case core interoperability benchmark. It tests whether CCA routes process/methodology judgment at the correct scope, preserves independent authorities, composes different-scope approaches without assimilation, surfaces same-scope tensions, and avoids loading process ceremony into an ordinary implementation task.

Directories `01-` through `20-` use the same executable contract as `evals/cases/`: `case.json`, `prompt.md`, `fixture/`, and `assertions.json`.

These fixtures are benchmark contracts, not behavioral results. CI validates their mechanics only. Real matched external-agent runs are required before claiming methodology parity or improvement.
"""
write(method_root / "README.md", readme)

for idx, (dirname, name, evidence, prompt, must_contain, absent_paths) in enumerate(cases, start=1):
    case_dir = method_root / dirname
    case_id = f"{idx:02d}"
    manifest = {
        "id": case_id,
        "name": name,
        "baseline": "none",
        "profiles": ["advisor", "methodology"],
        "expected_behavior": "Use the relevant method at its own scope, preserve independent authorities, and avoid unnecessary structural implementation of process guidance.",
    }
    write(case_dir / "case.json", json.dumps(manifest, indent=2))
    write(case_dir / "prompt.md", prompt)
    if idx == 20:
        write(case_dir / "fixture/README.md", "# Tiny library\n\nKeep changes limited to the implementation and tests.")
        write(case_dir / "fixture/app.py", "def add(a, b):\n    return a - b")
        write(case_dir / "fixture/test_app.py", "from app import add\n\nassert add(2, 3) == 5")
        assertions = [
            {"type": "file_contains", "path": "app.py", "text": "return a + b"},
            {"type": "path_absent", "path": "decision.md"},
            {"type": "path_absent", "path": "scrum"},
            {"type": "path_absent", "path": "kanban"},
            {"type": "path_absent", "path": "safe"},
            {"type": "path_absent", "path": "stages"},
        ]
    else:
        write(case_dir / "fixture/situation.md", f"# Situation\n\n{evidence}")
        assertions = [
            {"type": "path_exists", "path": "decision.md"},
            {"type": "file_contains", "path": "decision.md", "text": "Scope:"},
            {"type": "file_contains", "path": "decision.md", "text": "Recommendation:"},
            {"type": "file_contains", "path": "decision.md", "text": "Preserve:"},
            {"type": "file_contains", "path": "decision.md", "text": "Avoid:"},
        ]
        assertions.extend({"type": "file_contains", "path": "decision.md", "text": item} for item in must_contain)
        assertions.extend({"type": "path_absent", "path": item} for item in absent_paths)
    write(case_dir / "assertions.json", json.dumps({"assertions": assertions}, indent=2))

# 4. Validator: both suites, corpus anchors, regression semantics, docs surface.
validator = ROOT / ".github/scripts/validate_repo.py"
vtext = validator.read_text(encoding="utf-8")
old_eval = re.search(r"def validate_evaluation_cases\(\) -> None:\n.*?\n(?=def validate_icm_derived_example)", vtext, flags=re.S)
if not old_eval:
    raise SystemExit("could not locate validate_evaluation_cases")
new_eval = '''def _validate_case_suite(directory: str, expected_count: int) -> None:\n    cases = ROOT / "evals" / directory\n    dirs = sorted(path for path in cases.iterdir() if path.is_dir() and re.match(r"^\\d{2}-", path.name)) if cases.is_dir() else []\n    expected = [f"{i:02d}" for i in range(1, expected_count + 1)]\n    found = [path.name[:2] for path in dirs]\n    if found != expected:\n        error(f"Expected {directory} evaluation cases 01..{expected_count:02d}; found {found}")\n        return\n    for path in dirs:\n        for required in ("case.json", "prompt.md", "assertions.json"):\n            if not (path / required).is_file():\n                error(f"Evaluation case missing {required}: {path.relative_to(ROOT)}")\n        fixture = path / "fixture"\n        if not fixture.is_dir() or not any(p.is_file() for p in fixture.rglob("*")):\n            error(f"Evaluation case missing non-empty fixture: {path.relative_to(ROOT)}")\n        assertions = path / "assertions.json"\n        if assertions.is_file() and '"assertions": []' in read(assertions).replace(" ", ""):\n            error(f"Evaluation case has empty assertions: {path.relative_to(ROOT)}")\n\n\ndef validate_evaluation_cases() -> None:\n    _validate_case_suite("cases", 14)\n    _validate_case_suite("methodologies", 20)\n\n\ndef validate_methodology_corpus() -> None:\n    path = CCA / "references/advisor/frameworks-and-methodologies.md"\n    text = read(path)\n    anchors = [\n        "Cynefin", "SAFe", "LeSS", "Disciplined Agile", "waterfall", "stage-gate", "V-model",\n        "Scrum", "Kanban", "DSDM", "FDD", "ASD", "XP", "RAD", "IID", "Lean",\n        "RUP / UP", "DevOps", "TDD", "MDE", "PSP", "TSP", "SEMAT", "Essence",\n    ]\n    for anchor in anchors:\n        if anchor not in text:\n            error(f"Methodology corpus lost coverage anchor: {anchor!r}")\n\n'''
vtext = vtext[:old_eval.start()] + new_eval + vtext[old_eval.end():]
vtext = vtext.replace(
    '        CCA / "references/architect/forms.md": ["Record Library defaults", "half-created", "frequency", "System Map"],',
    '        CCA / "references/architect/forms.md": ["Record Library defaults", "half-created", "frequency", "System Map", "full display name", "beta-corp"],',
    1,
)
vtext = vtext.replace(
    '        ROOT / "evals/cases/README.md",\n',
    '        ROOT / "evals/cases/README.md",\n        ROOT / "evals/methodologies/README.md",\n',
    1,
)
vtext = vtext.replace(
    '    validate_evaluation_cases()\n',
    '    validate_evaluation_cases()\n    validate_methodology_corpus()\n',
    1,
)
validator.write_text(vtext, encoding="utf-8")

# 5. Evaluation documentation.
evals_readme = ROOT / "evals/README.md"
etext = evals_readme.read_text(encoding="utf-8")netext = etext.replace(
    "The evaluation **protocol and case contract are defined**, but the 14 scenario fixtures have not yet all been implemented or executed. No repository claim of behavioral superiority over ICM should be inferred from this directory until real isolated runs and their results are committed.",
    "The evaluation protocol, 14-case core interoperability suite, and 20-case methodology/framework suite are implemented. Repository CI validates mechanics and deterministic contracts only; real isolated external-agent runs are still required for behavioral claims. The 2026-08-15 three-way report covers only the 14 frozen core cases and must not be generalized to the methodology suite until those cases are executed.",
)
if "## Evaluation suites" not in etext:
    insert = '''\n## Evaluation suites\n\n- `cases/` — 14 core interoperability and workspace-behavior cases. Existing three-way results apply only to this suite.\n- `methodologies/` — 20 advisor/process cases covering sense-making, enterprise scaling, sequential constraints, team delivery, engineering practices/paradigms, lifecycle/operations, method engineering, composition/conflict, and an ordinary-task non-trigger.\n\nUse `--suite core` (default) or `--suite methodologies` when invoking the runner. Suite existence and CI success are not behavioral evidence.\n'''
    etext = etext.replace("\n## Runner usage\n", insert + "\n## Runner usage\n", 1)
etext = etext.replace(
    "python evals/runner.py \\\n  --case 03 \\",
    "python evals/runner.py \\\n  --suite core \\\n  --case 03 \\",
)
if "--suite methodologies" not in etext:
    etext += '''\n### Methodology suite example\n\n```bash\npython evals/runner.py \\\n  --suite methodologies \\\n  --case 04 \\\n  --arm B \\\n  --runs /tmp/cca-evals \\\n  --cca-skill skills/cca \\\n  --command <agent-command> <agent-args>\n```\n\nThis executes the Scrum/Kanban conflict case using the same isolated runner contract.\n'''
evals_readme.write_text(etext, encoding="utf-8")

cases_readme = ROOT / "evals/cases/README.md"
ctext = cases_readme.read_text(encoding="utf-8")
if "methodology/framework" not in ctext:
    ctext += "\nThis is the **core interoperability suite**. Broader process/methodology reasoning is tested separately under [`../methodologies/`](../methodologies/); do not infer that the 14 core cases cover the full advisor corpus.\n"
cases_readme.write_text(ctext, encoding="utf-8")

# 6. Remove temporary generator surfaces before committing generated result.
for rel in (
    ".github/scripts/apply_methodology_eval_expansion.py",
    ".github/workflows/apply-methodology-eval-expansion.yml",
):
    target = ROOT / rel
    if target.exists():
        target.unlink()
