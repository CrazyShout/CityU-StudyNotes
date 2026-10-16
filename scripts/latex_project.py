"""Shared paths, source bindings and compatibility navigation for native TeX editions."""
from pathlib import Path
import hashlib
import json
import os
import re
import nbformat
from functools import lru_cache
from html import escape as html_escape

ROOT=Path(__file__).resolve().parents[1]
MID=ROOT/'CS5489/exam-review/Midterm'
COURSES=['CS5489','CS5222','Foundations']
KINDS=['Questions','Answers','Combined','Compact','MultipleChoice','WrittenResponse']
ALL_BOOKS=COURSES+KINDS
CONFIG=json.loads((ROOT/'latex/documents.json').read_text())
DOCS=CONFIG['documents']
INDEX=json.loads((MID/'QuestionIndex.json').read_text())
ALIASES=json.loads((ROOT/'latex/legacy-anchors.json').read_text())
FIELDS=['question-en','question-zh','answer-prompt','answer-en','answer-zh','explanation','provenance','answer-provenance','concise-extra']
PAGE_MAP=ROOT/'latex/page-maps.json'
MANIFEST=ROOT/'latex/manifest.json'
STUB_MARKER='<!-- Generated compatibility navigation; edit the linked TeX source. -->'


def output(book):return ROOT/'pdf'/f'{book}-A4.pdf' if book in COURSES else MID/(book+'.pdf')

def selected(book):
    kind={'MultipleChoice':'multiple_select','WrittenResponse':'written'}.get(book)
    return [q for q in INDEX['questions'] if not kind or q['response_type']==kind]

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def inputs(book):
    paths={ROOT/'latex/preamble.tex',ROOT/'latex/vendor/elegantbook/elegantbook.cls',ROOT/'latex/vendor/elegantbook/UPSTREAM.json',ROOT/'latex/books'/f'{book}.tex',ROOT/'scripts/build_latex.py',ROOT/'scripts/latex_support.py',ROOT/'scripts/latex_project.py'}
    paths.update({ROOT/'scripts/pdf_fonts.py',ROOT/'latex/vendor/adobe-mapping/Adobe-GB1-UCS2',ROOT/'latex/vendor/adobe-mapping/UPSTREAM.json'})
    def add(path):
        if path in paths:return
        assert path.is_file(),path
        paths.add(path)
        if path.suffix!='.tex':return
        text=path.read_text()
        for name in re.findall(r'\\input\{\\StudyRoot/([^}]+)\}',text):add(ROOT/name)
        for name in re.findall(r'\\Study(?:Cell)?Image\{([^}]+)\}',text):add(ROOT/name)
        for name in re.findall(r'\\StudyNotebookCell\{([^}]+)\}',text):add(ROOT/name)
    if book in COURSES:
        for d in DOCS:
            if (d['course'] or 'Foundations')==book:add(ROOT/d['source'])
    else:
        paths.add(MID/'QuestionIndex.json');paths.add(MID/'SourceCatalog.json')
        add(MID/'frontmatter'/(book+'.tex'))
        for q in selected(book):
            fields=['answer-provenance','answer-prompt','answer-en','answer-zh','explanation'] if book=='Answers' else ['answer-provenance' if book=='Combined' else 'provenance','question-en','question-zh']
            if book!='Questions' and book!='Answers':fields+=['answer-en','answer-zh','explanation' if book=='Combined' else 'concise-extra']
            for f in fields:add(MID/'items'/q['id']/(f+'.tex'))
        if book in ['Answers','Combined']:add(MID/'frontmatter/source-differences.tex')
    return sorted(paths)

def binding(book):
    files={p.relative_to(ROOT).as_posix():sha(p) for p in inputs(book)}
    digest=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return digest,files

def compatibility_markdown(source,docid,book,maps,title):
    pdf=os.path.relpath(output(book),source.parent).replace(os.sep,'/')
    main=Path(CONFIG['documents'][next(i for i,d in enumerate(DOCS) if d['id']==docid)]['source']) if docid not in KINDS else Path('latex/books')/(book+'.tex')
    main_rel=os.path.relpath(ROOT/main,source.parent).replace(os.sep,'/')
    lines=[STUB_MARKER,'# '+title,'',f'正文已迁入 [LaTeX 主稿]({main_rel})；阅读与打印请用 [A4 PDF]({pdf})。本页仅保留旧链接入口，由构建脚本生成。','']
    if docid in KINDS:
        lines+=['题答只维护在 [`items/`](items/)；各版本共用相同题干和答案。','']
    for key,page in maps[book].items():
        prefix=docid+'__'
        if not key.startswith(prefix):continue
        anchor=key[len(prefix):]
        lines += ['<a id="'+anchor+'"></a>',f'- `{anchor}` → [第 {page} 页]({pdf}#page={page})']
    return '\n'.join(lines)+'\n'

def stubs(maps):
    result={}
    for d in DOCS:
        old=ROOT/d['legacy_source']
        if old.suffix=='.md':
            result[old]=compatibility_markdown(old,d['id'],d['course'] or 'Foundations',maps,d['id'])
    for book in KINDS:
        old=MID/(book+'.md');result[old]=compatibility_markdown(old,book,book,maps,CONFIG['midterm_titles'][book])
    return result

@lru_cache(maxsize=None)
def notebook_aliases(source,notebook,docid):
    cells=nbformat.read(ROOT/notebook,as_version=4).cells
    markdown_cells=[i for i,c in enumerate(cells) if c.cell_type=='markdown']
    owner=markdown_cells[0]
    result={i:[] for i in markdown_cells}
    result[owner].append('root')
    for anchor in re.findall(r'\\StudyTarget\{'+re.escape(docid)+r'__([^}]+)\}',(ROOT/source).read_text()):
        match=re.fullmatch(r'cell-(\d+)',anchor)
        if match:
            position=int(match[1])-1
            owner=max((n for n in markdown_cells if n<=position),default=markdown_cells[0])
        result[owner].append(anchor)
    return result


def notebook_markdown(d,i,c,maps):
    book=d['course'] or 'Foundations';key=d['id']+'__notebook-'+c['id'];page=maps[book][key]
    source=ROOT/d['notebook'];pdf=os.path.relpath(output(book),source.parent).replace(os.sep,'/')
    lines=[STUB_MARKER,'本单元教学说明见 [LaTeX 主稿]('+Path(d['source']).name+')；[A4 PDF 第 '+str(page)+' 页]('+pdf+'#page='+str(page)+')。代码及原有执行输出保留在此 Notebook。','']
    for anchor in notebook_aliases(d['source'],d['notebook'],d['id'])[i]:
        n=maps[book][d['id']+'__'+anchor]
        lines += ['<a id="'+html_escape(anchor,quote=True)+'"></a>',f'- `{anchor}` → [第 {n} 页]({pdf}#page={n})']
    return '\n'.join(lines)+'\n'
