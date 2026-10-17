"""Protect the baseline while allowing the recorded inline-radical repairs.

Reuses the existing manuscript, image, Notebook and visible-passage checks.
Does not execute experiments. Run after build.py; --candidate reads .build/latex.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import subprocess

ROOT = Path(__file__).resolve().parents[3]
REVIEW = Path(__file__).resolve().parent
BASE = '48eb1453c9e2d79c8372780802b75a45c2cba45d'


def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


def check(candidate=False):
    edits = json.loads((REVIEW / 'edits.json').read_text())
    prior = ROOT / 'docs/reviews/teaching-structure-2026-10-16/check_preservation.py'
    spec = importlib.util.spec_from_file_location('followup_protection', prior)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.BASE = BASE

    # Account for the exact migration repairs, not arbitrary math rewrites.
    old_math = module.math
    radicals = [e for e in edits if e['finding'] == 'F01']

    def normalized_math(text):
        for edit in radicals:
            text = text.replace(edit['before'], edit['after'])
        return old_math(text)

    module.math = normalized_math
    report = module.check(candidate)
    report['scope'] = 'baseline protection; exact logged edits; no new full-course reproduction'
    report['edition'] = 'candidate' if candidate else 'published'
    report['inline_radical_repairs'] = sum(e['occurrences'] for e in radicals)
    assert report['inline_radical_repairs'] == 13

    # Ensure the entire source diff is explained, including ordinary prose.
    for doc in module.DOCS:
        path = doc['source']
        expected = original(path).decode()
        for edit in edits:
            if edit['file'] == path:
                assert expected.count(edit['before']) == edit['occurrences'], edit
                expected = expected.replace(edit['before'], edit['after'])
        assert expected == (ROOT / path).read_text(), (path, 'unrecorded source edit')
    report['all_source_changes_match_log'] = True

    protected = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, '--',
        'latex/vendor/elegantbook', 'latex/preamble.tex', 'latex/exam',
        'latex/documents.json', 'latex/legacy-anchors.json'], cwd=ROOT, text=True).splitlines()
    for path in protected:
        assert original(path) == (ROOT / path).read_bytes(), path
    report['unchanged_template_registry_and_anchor_files'] = len(protected)

    local = ROOT / '.build/three-books-followup-2026-10-18/baseline.json'
    if local.exists():
        hashes = json.loads(local.read_text())['files']
        templates = {p: v for p, v in hashes.items() if p.startswith('template_ElegantbBook/')}
        for path, digest in templates.items():
            assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
        report['unchanged_user_template_files'] = len(templates)
    report['status'] = 'passed'
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = check(args.candidate)
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"Passed {len(result['documents'])} manuscripts, "
          f"{sum(n['unchanged_code_cells'] for n in result['notebooks'])} Notebook cells, "
          f"{result['inline_radical_repairs']} equivalent radical repairs and protected assets.")
