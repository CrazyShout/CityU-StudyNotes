"""Check protected content against the review baseline and visible PDF passages.

Use --candidate before publication. No Notebook or original experiment is executed.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import pymupdf

ROOT = Path(__file__).resolve().parents[3]
BASE = 'c805d278d66afda0d72566bc702aff04b32186a5'
REVIEW = Path(__file__).resolve().parent


def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


def exam_rows(text):
    return [line.replace('本轮复习重点', '复习重点') for line in text.splitlines()
            if '&' in line and line.rstrip().endswith(r'\\')]


def check(candidate=False):
    prior = ROOT / 'docs/reviews/teaching-structure-2026-10-16/check_preservation.py'
    spec = importlib.util.spec_from_file_location('protected_content_review', prior)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.BASE = BASE
    report = module.check(candidate)
    report['scope'] = 'protected content and visible revised passages; no experiment execution'
    report['edition'] = 'candidate' if candidate else 'published'
    assert original('latex/documents.json') == (ROOT / 'latex/documents.json').read_bytes()
    for n in range(1, 6):
        path = f'CS5489/course-notes/Lecture{n:02}.tex'
        blocks = lambda s: '\n'.join(re.findall(r'% EXAM:[^\n]*:START(.*?)% EXAM:[^\n]*:END', s, re.S))
        assert exam_rows(blocks(original(path).decode())) == exam_rows(blocks((ROOT / path).read_text())), path
    path = 'CS5489/course-notes/ExamIndex.tex'
    assert exam_rows(original(path).decode()) == exam_rows((ROOT / path).read_text()), path
    report['exam_table_rows_and_counts_preserved'] = True
    sys.path.insert(0, str(ROOT / 'scripts'))
    from build_exam_annotations import compact_review_notes
    assert compact_review_notes(['known A', 'new condition', 'known B'],
                                {'known A', 'known B'}, ['compact']) == ['compact', 'new condition']
    assert compact_review_notes(['known A', 'changed B'],
                                {'known A', 'known B'}, ['compact']) == ['known A', 'changed B']
    report['future_ledger_conditions_preserved'] = True
    template_files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, '--',
        'latex/vendor/elegantbook', 'latex/preamble.tex'], cwd=ROOT, text=True).splitlines()
    for path in template_files:
        assert original(path) == (ROOT / path).read_bytes(), path
    report['unchanged_public_template_files'] = len(template_files)
    local = ROOT / '.build/prose-audit/baseline.json'
    if local.exists():
        baseline = json.loads(local.read_text())
        for path, digest in baseline['template'].items():
            assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
        report['unchanged_user_template_files'] = len(baseline['template'])
    coverage = json.loads((REVIEW / 'coverage.json').read_text())
    assert len(coverage['documents']) == 25
    assert all(s['keep_reason'] and s['status'] != '待审'
               for d in coverage['documents'] for s in d['sections'])
    report['recorded_review_sections'] = sum(len(d['sections']) for d in coverage['documents'])
    report['review_record_note'] = 'Coverage rows record human reading; this script checks their presence, not prose quality.'
    visible = {
        'CS5489': ['本指南在何处计入批量平均', '共享指数为什么收到多个位置的梯度之和',
                   '怎样避免缩放时使用测试信息', '额外设计受控优化器比较时', '由新模型预测旧模型尚未解释的差值'],
        'CS5222': ['不同客户端为什么可以共享服务器', '序号解决了什么歧义', '为什么还需要定时器',
                   '长时间延迟的旧副本为什么可能破坏交替比特协议的可靠性', '本章的包与字节有何区别'],
        'Foundations': ['内积把对应分量的乘积相加', '外积保留各分量配对的乘积',
                        '将它乘以目标向量就得到最小范数的最小二乘解', '上条为发送时延下条为传播时延'],
    }
    report['specific_visible_checks'] = []
    for book, snippets in visible.items():
        path = ROOT / (f'.build/latex/{book}/{book}.pdf' if candidate else f'pdf/{book}-A4.pdf')
        with pymupdf.open(path) as pdf:
            raw = '\n'.join(page.get_text() for page in pdf)
            cjk = re.sub(r'[^\u4e00-\u9fff]', '', raw)
            for snippet in snippets:
                needle = re.sub(r'[^\u4e00-\u9fff]', '', snippet)
                assert needle in cjk, (book, snippet)
                report['specific_visible_checks'].append({'book': book, 'text': snippet})
            if book == 'CS5489':
                assert 'x*=2' in re.sub(r'\s', '', raw), 'Lost multiplication assignment in printed question'
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
    print(f"Passed {len(result['documents'])} manuscripts, {result['recorded_review_sections']} recorded sections, "
          f"{sum(x['unchanged_code_cells'] for x in result['notebooks'])} protected Notebook cells and visible passages.")
