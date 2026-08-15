#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

validator = ROOT / '.github/scripts/validate_repo.py'
text = validator.read_text(encoding='utf-8')
old = '''        if assertions.is_file() and '\"assertions\": []' in read(assertions).replace(" ", ""):\n            error(f"Evaluation case has empty assertions: {path.relative_to(ROOT)}")'''
new = '''        if assertions.is_file() and re.search(r'"assertions"\\s*:\\s*\\[\\s*\\]', read(assertions)):\n            error(f"Evaluation case has empty assertions: {path.relative_to(ROOT)}")'''
if old not in text:
    raise SystemExit('validator empty-assertion anchor missing')
validator.write_text(text.replace(old, new, 1), encoding='utf-8')

readme = ROOT / 'evals/README.md'
text = readme.read_text(encoding='utf-8')
text = text.replace(
    'The 14 fixtures and harness are implemented. Real model A/B results are still unproven until actual external agent commands execute both arms under matched conditions and their artifacts are retained.',
    'The 14 core fixtures, 20 methodology/framework fixtures, and harness are implemented. Real model comparisons are still unproven for any suite until actual external agent commands execute the relevant arms under matched conditions and their artifacts are retained.',
)
text = text.replace(
    'python evals/runner.py \\\n  --case 01 \\\n  --arm A',
    'python evals/runner.py \\\n  --suite core \\\n  --case 01 \\\n  --arm A',
)
readme.write_text(text, encoding='utf-8')

for rel in (
    '.github/scripts/finalize_methodology_eval_expansion.py',
    '.github/workflows/finalize-methodology-eval-expansion.yml',
):
    path = ROOT / rel
    if path.exists():
        path.unlink()
