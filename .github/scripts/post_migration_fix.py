#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace(path: Path, pairs: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

# Validator follows the new runtime authority/package layout.
validator = ROOT / ".github/scripts/validate_repo.py"
replace(validator, [
    ('template_dir = SKILLS / "cca-architect" / "assets" / "templates"', 'template_dir = SKILLS / "cca" / "assets" / "templates"'),
    ('error("cca-architect templates directory is missing")', 'error("cca templates directory is missing")'),
    ('ROOT / "spec" / "SPEC.md",', 'ROOT / "skills" / "cca" / "references" / "core" / "spec.md",'),
    ('ROOT / "spec" / "compatibility.md",', 'ROOT / "skills" / "cca" / "references" / "core" / "compatibility.md",'),
    ('ROOT / "spec" / "method-composition.md",', 'ROOT / "skills" / "cca" / "references" / "core" / "method-composition.md",'),
])

# Root docs had Markdown links using paths rather than backticked skill names.
for path in [ROOT / "README.md", ROOT / "CONTRIBUTING.md", ROOT / "docs/getting-started.md", ROOT / "docs/faq.md"]:
    if not path.exists():
        continue
    replace(path, [
        ('skills/cca-advisor/SKILL.md', 'skills/cca/SKILL.md'),
        ('skills/cca-advisor/', 'skills/cca/references/advisor/'),
        ('skills/cca-architect/', 'skills/cca/references/architect/'),
        ('skills/cca-scaffold/', 'skills/cca/references/operations/scaffold.md'),
        ('skills/cca-sync/', 'skills/cca/references/operations/sync.md'),
        ('skills/cca-ingest/', 'skills/cca/references/operations/ingest.md'),
        ('skills/cca-query/', 'skills/cca/references/operations/query.md'),
        ('skills/cca-lint/', 'skills/cca/references/operations/lint.md'),
    ])

# The copied compatibility file previously linked out of spec/ into docs/.
compat = ROOT / "skills/cca/references/core/compatibility.md"
replace(compat, [
    ('../docs/method-composition.md', 'method-composition.md'),
    ('../docs/standards.md', '../../../../docs/standards.md'),
])

# Add a stronger repository-structure assertion: there is exactly one first-party skill.
text = validator.read_text(encoding="utf-8")
needle = 'def validate_skills() -> None:\n'
if 'Expected exactly one first-party skill package' not in text:
    insertion = '''def validate_single_skill_package() -> None:\n    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir()) if SKILLS.is_dir() else []\n    names = [path.name for path in skill_dirs]\n    if names != ["cca"]:\n        error(f"Expected exactly one first-party skill package ['cca']; found {names}")\n\n\n'''
    text = text.replace(needle, insertion + needle)
    text = text.replace('    validate_required_docs()\n    validate_skills()\n', '    validate_required_docs()\n    validate_single_skill_package()\n    validate_skills()\n')
validator.write_text(text, encoding="utf-8")

print("Post-migration alignment applied")
