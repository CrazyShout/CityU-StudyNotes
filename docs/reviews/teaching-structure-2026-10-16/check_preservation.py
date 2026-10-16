"""Check this revision against its baseline and inspect visible teaching passages.

Run with the repository build environment. --candidate reads .build/latex;
the default reads the published PDFs. This does not execute any notebook.
"""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import pymupdf

ROOT = Path(__file__).resolve().parents[3]
BASE = 'b34d9888a56e2e56568716ca4dd9fb5a740e9e36'
DOCS = json.loads((ROOT / 'latex/documents.json').read_text())['documents']


def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


def math(s):
    return Counter(re.sub(r'\s', '', a or b) for a, b in
                   re.findall(r'\\\[(.*?)\\\]|\\\((.*?)\\\)', s, re.S))


def caption_bodies(s):
    for m in re.finditer(r'\\StudyCaption\{', s):
        start = m.end()
        depth = 1
        for i in range(start, len(s)):
            if s[i] in '{}' and s[i - 1] != '\\':
                depth += 1 if s[i] == '{' else -1
                if depth == 0:
                    yield s[start:i]
                    break
        else:
            raise AssertionError('Unclosed caption')


def cjk(text):
    return re.sub(r'[^\u4e00-\u9fff]', '', text)


def check(candidate):
    report = {'baseline': BASE, 'documents': [], 'notebooks': [], 'visible_passages': []}
    images = set()
    page_text = {}
    for book in ['CS5489', 'CS5222', 'Foundations']:
        path = (ROOT / f'.build/latex/{book}/{book}.pdf' if candidate else
                ROOT / f'pdf/{book}-A4.pdf')
        with pymupdf.open(path) as pdf:
            pages = []
            for page in pdf:
                text = page.get_text(clip=pymupdf.Rect(0, 50, page.rect.width, page.rect.height - 35))
                text = re.sub(r'（(?:本册|基础册|CS\d+册|题目册|解析册)\s*p\.\s*\d+）', '', text)
                pages.append(cjk(text))
            page_text[book] = pages
    for d in DOCS:
        path = d['source']
        before = original(path).decode()
        after = (ROOT / path).read_text()
        matches = lambda pattern, text: re.findall(pattern, text, re.S)
        checks = {
            'math_multiset_equal': math(before) == math(after),
            'equation_numbers_equal': matches(r'\\tag\{([^}]+)\}', before) == matches(r'\\tag\{([^}]+)\}', after),
            'image_references_equal': matches(r'\\Study(?:Cell)?Image\{([^}]+)\}', before) == matches(r'\\Study(?:Cell)?Image\{([^}]+)\}', after),
            'old_anchors_preserved': set(matches(r'\\StudyTarget\{([^}]+)\}', before)) <= set(matches(r'\\StudyTarget\{([^}]+)\}', after)),
            'code_blocks_equal': matches(r'\\begin\{StudyCode\}(.*?)\\end\{StudyCode\}', before) == matches(r'\\begin\{StudyCode\}(.*?)\\end\{StudyCode\}', after),
            'notebook_cell_calls_equal': matches(r'\\StudyNotebookCell[^\n]*', before) == matches(r'\\StudyNotebookCell[^\n]*', after),
        }
        assert all(checks.values()), (path, checks)
        images.update(matches(r'\\Study(?:Cell)?Image\{([^}]+)\}', after))
        report['documents'].append({'source': path, **checks,
                                    'sha256': hashlib.sha256(after.encode()).hexdigest()})
        book = d['course'] or 'Foundations'
        text = ''.join(page_text[book])
        passages = [(title, body) for _, title, body in matches(
            r'\\begin\{StudyBlock\}\{([^{}]*)\}\{([^{}]*)\}(.*?)\\end\{StudyBlock\}', after)]
        assert len(passages) == after.count(r'\begin{StudyBlock}') == after.count(r'\end{StudyBlock}'), path
        for title, body in passages:
            snippets = [cjk(title), cjk(body)[:20], cjk(body)[-20:]]
            assert all(not v or v in text for v in snippets), (path, title, 'missing visible passage')
            report['visible_passages'].append({'source': path, 'title': title,
                'pages': [i + 1 for i, p in enumerate(page_text[book]) if cjk(title) in p]})
        captions = list(caption_bodies(after))
        for body in captions:
            snippets = [cjk(body)[:20], cjk(body)[-20:]]
            assert all(not v or v in text for v in snippets), (path, body, 'missing visible caption')
        report['documents'][-1].update(named_passages=len(passages), visible_captions=len(captions))
        if 'notebook' in d:
            path = d['notebook']
            before = json.loads(original(path)); after = json.loads((ROOT / path).read_text())
            cells = lambda nb: [c for c in nb['cells'] if c['cell_type'] == 'code']
            identity = lambda nb: [(c.get('id'), c['cell_type'], c.get('metadata')) for c in nb['cells']]
            assert cells(before) == cells(after), (path, 'changed executable cell/output')
            assert identity(before) == identity(after) and before['metadata'] == after['metadata'], (path, 'changed notebook metadata')
            report['notebooks'].append({'source': path, 'unchanged_code_cells': len(cells(after))})
    protected = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, '--',
        'CS5489/exam-review/Midterm/items', 'CS5489/course-notes/exam-evidence'], cwd=ROOT, text=True).splitlines()
    for path in protected:
        assert original(path) == (ROOT / path).read_bytes(), (path, 'changed protected question or ledger')
    for path in images:
        assert original(path) == (ROOT / path).read_bytes(), (path, 'changed original figure')
    report['unchanged_original_images'] = len(images)
    report['unchanged_question_and_evidence_files'] = len(protected)
    report['status'] = 'passed'
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = check(args.candidate)
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(f"Passed {len(result['documents'])} source checks, {len(result['visible_passages'])} visible passages, "
          f"{sum(d['visible_captions'] for d in result['documents'])} visible captions and protected notebook/question/evidence checks.")
