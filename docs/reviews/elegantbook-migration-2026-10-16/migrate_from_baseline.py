"""One-time, explicit migration of the recorded Markdown/Notebook baseline.

Not part of normal builds. Never run this over edited TeX manuscripts.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re
import sys
import subprocess
import tarfile
import io
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'scripts'))
import nbformat
import markdown
from bs4 import BeautifulSoup
from latex_support import Renderer, escape, ROOT

BASE = ROOT / '.build/elegantbook-migration/baseline'
if not BASE.exists():
    BASE.mkdir(parents=True)
    data=subprocess.check_output(['git','archive','9ad4a45ff757732342aaef2e536fae7c5a5332c1'],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:archive.extractall(BASE,filter='data')
REVIEW = ROOT / 'docs/reviews/elegantbook-migration-2026-10-16'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--write', action='store_true')
args = parser.parse_args()
assert args.write, 'Explicit --write required; this is not a build step'
registry = json.loads((BASE / 'learning/course-notes-documents.json').read_text())
records = [r for r in registry['documents']
           if r['major'] or r.get('print_appendix') or r['course'] is None]
ids = {}
for r in records:
    group = r['course'] or 'Foundations'
    r['id'] = group + '-' + Path(r['source']).stem
    for suffix in [Path(r['source']).suffix, '.html', '.tex']:
        ids[str(Path(r['source']).with_suffix(suffix))] = r['id']
for kind in ['Questions', 'Answers', 'Combined', 'Compact', 'MultipleChoice', 'WrittenResponse']:
    for suffix in ['.md', '.html', '.tex']:
        ids[f'CS5489/exam-review/Midterm/{kind}{suffix}'] = kind
spec = importlib.util.spec_from_file_location('legacy_preview', BASE/'CS5489/course-notes/tools/build_previews.py')
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
legacy.OUT=ROOT/'CS5489/course-notes'
legacy.CODEXING=ROOT
legacy.DOCUMENTS={(ROOT/r['source']).resolve():r for r in registry['documents']}
legacy.PREVIEWS={p:p.with_suffix('.html') for p in legacy.DOCUMENTS}
reports = []
notebooks = {}


def md_html(text, source):
    if source not in legacy.PREVIEWS:
        return legacy.md(text)
    return legacy.wrap('Migration baseline', legacy.md(text), source)


def convert(text, source, docid, first_heading=True):
    renderer = Renderer(source, docid, ids, first_heading=first_heading)
    tex, report = renderer.convert(md_html(text, source))
    return tex, report


def save(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text() == text:
            return
        raise FileExistsError(f'Refusing to overwrite edited TeX: {path}')
    path.write_text(text)


for record in records:
    relative = record['source']
    source = ROOT / relative
    target = source.with_suffix('.tex')
    data = (BASE / relative).read_bytes()
    if source.suffix == '.md':
        tex, report = convert(data.decode(), source, record['id'])
    else:
        notebook = nbformat.reads(data.decode(), as_version=4)
        parts = []
        original = []
        for i, cell in enumerate(notebook.cells):
            cid = cell.get('id') or f'cell-{i+1:03}'
            anchor = 'notebook-' + cid
            original.append({
                'id': cid, 'index': i, 'type': cell.cell_type,
                'sha256': hashlib.sha256(json.dumps(dict(cell), sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
                'code_sha256': hashlib.sha256(cell.source.encode()).hexdigest() if cell.cell_type == 'code' else None,
                'outputs_sha256': hashlib.sha256(json.dumps(cell.get('outputs',[]),sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
            })
            parts.append(f'<section id="cell-{i+1}"><a id="{anchor}"></a>')
            if cell.cell_type == 'markdown':
                parts.append(legacy.md(cell.source))
            elif cell.cell_type == 'code':
                parts.append(f'<div class="notebook-code-reference" data-notebook="{relative}" data-cell="{cid}"></div>')
            else:
                raise ValueError((relative, cid, 'unsupported raw cell'))
            parts.append('</section>')
        renderer = Renderer(source, record['id'], ids)
        tex, report = renderer.convert(legacy.wrap('Migration baseline','\n'.join(parts),source))
        notebooks[relative] = {'cells':original, 'metadata':notebook.metadata}
        record['notebook'] = relative
    header = '% Teaching manuscript. Edit this TeX source; Markdown is compatibility navigation only.\n'
    save(target, header + tex)
    report['baseline_sha256'] = hashlib.sha256(data).hexdigest()
    report['target'] = target.relative_to(ROOT).as_posix()
    reports.append(report)
    record['legacy_source'] = relative
    record['source'] = target.relative_to(ROOT).as_posix()

# Preserve each question and each answer section as native TeX components.
mid = ROOT/'CS5489/exam-review/Midterm'
index = json.loads((BASE/'CS5489/exam-review/Midterm/QuestionIndex.json').read_text())
sys.path.insert(0,str(BASE/'CS5489/exam-review/Midterm/tools'))
from assemble_combined import question_blocks
from assemble_compact import concise_answer, ANSWER_FIGURES
qb = question_blocks((BASE/'CS5489/exam-review/Midterm/Questions.md').read_text())
ab = question_blocks((BASE/'CS5489/exam-review/Midterm/Answers.md').read_text())
questions = []
for q in index['questions']:
    qid = q['id']
    question = qb[qid].rsplit('\n[题目](',1)[0].strip()
    answer = ab[qid].rsplit('\n[题目](',1)[0].strip()
    # Fields retain whole original blocks, including their subheadings and figures.
    qhead, qbody = question.split('### English question\n',1)
    en, zh = qbody.split('### 中文题意\n',1)
    ahead, rest = answer.split('### English answer\n',1)
    aen, rest = rest.split('### 中文对应答案\n',1)
    azh, explanation = rest.split('### 中文讲解\n',1)
    zh_answer = ahead.split('### 中文题意\n',1)[1]
    fields = {'question-en':en, 'question-zh':zh, 'answer-prompt':zh_answer,
              'answer-en':aen, 'answer-zh':azh, 'explanation':explanation}
    fields['answer-provenance'] = ahead.split('### 中文题意\n',1)[0].split('\n',1)[1].strip()
    # Additional question-header provenance notes remain outside the body fields.
    qmeta = qhead.split('\n',1)[1].strip()
    fields['provenance'] = qmeta
    figure_text = ''
    if qid in ANSWER_FIGURES:
        name, caption = ANSWER_FIGURES[qid]
        match = next(m[0] for m in re.finditer(r'!\[[^\]]*\]\(assets/[^)]+\)', answer) if f'assets/{name})' in m[0])
        figure_text = match + '\n\n*' + caption + '*\n'
    if '题头差异：' not in question:
        figure_text += '\n\n'.join(re.findall(r'^\*\*原题差异 / Source note：\*\*[^\n]*', answer,re.M))
    fields['concise-extra'] = figure_text
    qreports = {}
    for field, body in fields.items():
        original = mid/('Questions.md' if field.startswith('question') or field=='provenance' else 'Answers.md')
        tex, report = convert(body.strip(), original,
                              qid + '-' + field, first_heading=False)
        dest = mid/'items'/qid/(field+'.tex')
        save(dest, '% '+qid+' / '+field+' — canonical editable content.\n'+tex)
        report['target'] = dest.relative_to(ROOT).as_posix()
        qreports[field] = report
    questions.append({'id':qid,'fields':qreports})

book_titles = {}
for kind in ['Questions','Answers','Combined','Compact','MultipleChoice','WrittenResponse']:
    text = (BASE/f'CS5489/exam-review/Midterm/{kind}.md').read_text()
    # Keep introductory and final material, replacing only the generated manual contents.
    start = text.split('## 目录\n',1)[0]
    title = next(line[2:] for line in start.splitlines() if line.startswith('# '))
    book_titles[kind] = title
    start = '\n'.join(line for line in start.splitlines() if not line.startswith('# '))
    intro, rep = convert(start, mid/(kind+'.md'), kind, first_heading=False)
    save(mid/'frontmatter'/(kind+'.tex'), intro)
tail = '<h2 id="source-differences">' + (BASE/'CS5489/exam-review/Midterm/Answers.md').read_text().split('<h2 id="source-differences">',1)[1]
tex, report = convert(tail, mid/'Answers.md', 'Answers', first_heading=False)
save(mid/'frontmatter/source-differences.tex', tex)

data = {'baseline_ref':'9ad4a45ff757732342aaef2e536fae7c5a5332c1',
        'course_documents':reports,'questions':questions,'notebooks':notebooks}
(REVIEW/'migration-manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(ROOT/'latex/documents.json').write_text(json.dumps({'documents':records,'legacy_ids':ids,'midterm_titles':book_titles},ensure_ascii=False,indent=2)+'\n')
print(f'Converted {len(records)} course manuscripts and {len(questions)} complete bilingual question/answer sets.')
