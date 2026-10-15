"""Build all nine ElegantBook editions from canonical TeX and saved notebook outputs."""
from __future__ import annotations
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import nbformat
from pypdf import PdfReader, PdfWriter
from latex_support import Renderer, escape, ROOT

BUILD = ROOT/'.build/latex'
CONFIG = ROOT/'latex/documents.json'
MID = ROOT/'CS5489/exam-review/Midterm'
KINDS = ['Questions','Answers','Combined','Compact','MultipleChoice','WrittenResponse']
COURSES = ['CS5489','CS5222','Foundations']
TITLES = {'CS5489':('CS5489 · 机器学习','课程讲义与练习'),
          'CS5222':('CS5222 · 计算机网络','课程讲义与练习'),
          'Foundations':('基础补课','数学、网络与来源说明')}
PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument('--book', action='append', choices=COURSES+KINDS+['Sample'])
PARSER.add_argument('--engine', default='xelatex')
PARSER.add_argument('--jobs',type=int,default=2)
PARSER.add_argument('--rounds',type=int,default=5)
PARSER.add_argument('--prepare-only',action='store_true')
PARSER.add_argument('--sample', action='store_true')
PARSER.add_argument('--no-publish', action='store_true', help='Compile candidates without replacing published files')
ARGS = PARSER.parse_args()
CONFIG_DATA=json.loads(CONFIG.read_text())
DOCS=CONFIG_DATA['documents']
INDEX=json.loads((MID/'QuestionIndex.json').read_text())
GROUPS={g['id']:g['title'] for g in INDEX['groups']}
BOOKS = ARGS.book or (['Sample'] if ARGS.sample else COURSES+KINDS)
MAP_FILE=BUILD/'page-maps.json'
MAPS=json.loads(MAP_FILE.read_text()) if MAP_FILE.exists() else json.loads((ROOT/'latex/page-maps.json').read_text()) if (ROOT/'latex/page-maps.json').exists() else {}
SOURCE_REF=os.environ.get('STUDY_NOTES_SOURCE_REF','main')
SOURCE_DATE=json.loads((ROOT/'learning/course-notes-documents.json').read_text())['updated']
BUILD.mkdir(parents=True,exist_ok=True)


def output(book):
    return ROOT/'pdf'/f'{book}-A4.pdf' if book in COURSES else MID/f'{book}.pdf'


def selected(book):
    if book=='MultipleChoice':
        return [q for q in INDEX['questions'] if q['response_type']=='multiple_select']
    if book=='WrittenResponse':
        return [q for q in INDEX['questions'] if q['response_type']=='written']
    return INDEX['questions']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def notebook_assets():
    definitions=[]
    for d in DOCS:
        if 'notebook' not in d: continue
        nb=nbformat.read(ROOT/d['notebook'],as_version=4)
        for i,c in enumerate(nb.cells):
            if c.cell_type!='code':continue
            cid=c.get('id') or f'cell-{i+1:03}'
            name=Path(d['notebook']).stem+'-'+cid
            folder=BUILD/'notebooks';folder.mkdir(exist_ok=True)
            lines=[r'\Needspace{3\baselineskip}',r'\textsf{\small In ['+str(c.execution_count)+']}',r'\begin{StudyCode}',c.source,r'\end{StudyCode}','']
            for j,o in enumerate(c.get('outputs',[])):
                if o.output_type=='error':raise RuntimeError((d['notebook'],cid,'saved error'))
                if o.output_type=='stream':
                    lines += [r'\begin{StudyCode}',o.text.rstrip(),r'\end{StudyCode}','']
                    continue
                data=o.get('data',{})
                if 'image/png' in data:
                    asset=folder/(name+f'-output-{j}.png')
                    asset.write_bytes(base64.b64decode(data['image/png']))
                    lines += [r'\StudyImage{'+asset.relative_to(ROOT).as_posix()+'}','']
                elif 'text/html' in data:
                    renderer=Renderer(ROOT/d['notebook'],d['id']+'-'+cid+'-'+str(j),CONFIG_DATA['legacy_ids'])
                    content,_=renderer.convert(data['text/html'])
                    lines += [content]
                elif 'text/plain' in data:
                    lines += [r'\begin{StudyCode}',data['text/plain'].rstrip(),r'\end{StudyCode}','']
                elif 'text/markdown' in data:
                    import markdown
                    renderer=Renderer(ROOT/d['notebook'],d['id']+'-'+cid+'-'+str(j),CONFIG_DATA['legacy_ids'])
                    content,_=renderer.convert(markdown.markdown(data['text/markdown'],extensions=['tables']))
                    lines += [content]
                elif data:
                    raise RuntimeError(('Unsupported saved MIME output',d['notebook'],cid,list(data)))
            target=folder/(name+'.tex');target.write_text('\n'.join(lines)+'\n')
            definitions.append(r'\expandafter\def\csname studynb@'+d['notebook']+'@'+cid+r'\endcsname{../../'+target.relative_to(ROOT).as_posix()+'}')
    return definitions


def image_assets():
    definitions=[]
    sources=[ROOT/d['source'] for d in DOCS]+list((MID/'items').rglob('*.tex'))
    images=set()
    for p in sources:
        images.update(re.findall(r'\\Study(?:Cell)?Image\{([^}]+)\}',p.read_text()))
    for name in sorted(images):
        p=ROOT/name
        if not p.is_file():raise FileNotFoundError(p)
        if p.suffix.lower()=='.svg':
            if sys.platform=='darwin' and Path('/opt/homebrew/lib/libcairo.2.dylib').exists():
                os.environ.setdefault('DYLD_FALLBACK_LIBRARY_PATH','/opt/homebrew/lib')
            import cairosvg
            folder=BUILD/'assets';folder.mkdir(exist_ok=True)
            target=folder/(p.stem+'-'+sha(p)[:12]+'.pdf')
            if not target.exists():
                cairosvg.svg2pdf(url=str(p),write_to=str(target))
            definitions.append(r'\expandafter\def\csname studyimage@'+name+r'\endcsname{../../'+target.relative_to(ROOT).as_posix()+'}')
    return definitions


def legacy_aliases():
    path=ROOT/'latex/legacy-anchors.json'
    return json.loads(path.read_text()) if path.exists() else {}


ALIASES=legacy_aliases()


def field_targets(book,qid,field):
    names=[a for a,v in ALIASES.get(book,{}).items() if v.get('qid')==qid and v.get('field')==field]
    excluded={qid.lower(),qid} if qid else set()
    if qid:excluded.update(a.lower() for q in INDEX['questions'] if q['id']==qid for a in q['legacy_ids'])
    return [r'\StudyTarget{'+book+'__'+a+'}' for a in names if a not in excluded]


def field(book,qid,name,title=None):
    lines=[]
    if title: lines += [r'\subsection*{'+title+'}']
    lines += field_targets(book,qid,name)
    lines += [r'\input{\StudyRoot/CS5489/exam-review/Midterm/items/'+qid+'/'+name+'.tex}']
    return lines


def driver(book):
    if book=='Sample':return ROOT/'latex/books/Sample.tex'
    lines=['% !TEX program = xelatex',r'\def\StudyRoot{../..}',r'\def\StudyBook{'+book+'}',
           r'\input{../preamble.tex}',r'\begin{document}']
    if book in COURSES:
        title,subtitle=TITLES[book]
        lines += [r'\StudyCover{'+title+'}{'+subtitle+'}',r'\tableofcontents']
        for d in DOCS:
            if (d['course'] or 'Foundations')==book:
                lines += [r'\input{\StudyRoot/'+d['source']+'}']
    else:
        lines += [r'\setlength{\parskip}{.25\baselineskip}',r'\titlespacing*{\subsection}{0pt}{.7\baselineskip}{.2\baselineskip}']
        title=CONFIG_DATA['midterm_titles'][book]
        halves=title.split(' / ',1)
        lines += [r'\renewcommand{\StudyCoverExtra}{'+''.join(field_targets(book,None,'cover'))+'}']
        lines += [r'\StudyCover{'+escape(halves[0])+'}{'+escape(halves[1] if len(halves)>1 else '')+'}',
                  r'\input{\StudyRoot/CS5489/exam-review/Midterm/frontmatter/'+book+'.tex}',
                  r'\begingroup\small\setlength{\cftbeforechapskip}{.45\baselineskip}\tableofcontents\endgroup']
        lines += field_targets(book,None,'front')
        sys.path.insert(0,str(MID/'tools'))
        from question_types import type_label
        previous_group=None
        for q in selected(book):
            qid=q['id']
            if book in ['Questions','Answers','Combined']:lines += [r'\clearpage']
            if q['group']!=previous_group:
                lines += [r'\Needspace{7\baselineskip}\phantomsection\addcontentsline{toc}{chapter}{'+escape(GROUPS[q['group']])+'}']
                previous_group=q['group']
            anchors=[r'\StudyTarget{'+book+'__'+qid.lower()+'}']
            anchors += [r'\StudyTarget{'+book+'__'+a.lower()+'}' for a in q['legacy_ids']]
            anchors += field_targets(book,qid,'title')
            lines += [r'\renewcommand{\StudyQuestionExtra}{'+''.join(anchors)+'}',r'\StudyQuestion{'+qid+'}{'+escape(q['title'])+'}{'+escape(type_label(q))+'}']
            if book=='Answers':
                lines += field(book,qid,'answer-provenance')
                lines += field(book,qid,'answer-prompt','中文题意')
            else:
                lines += field(book,qid,'answer-provenance' if book=='Combined' else 'provenance')
                lines += field(book,qid,'question-en','English question')
                lines += field(book,qid,'question-zh','中文题意')
            if book!='Questions':
                lines += field(book,qid,'answer-en','English answer')
                lines += field(book,qid,'answer-zh','中文对应答案')
                if book in ['Answers','Combined']:
                    lines += field(book,qid,'explanation','中文讲解')
                else:
                    lines += field(book,qid,'concise-extra')
        if book in ['Answers','Combined']:
            lines += [r'\clearpage']
            if book!='Answers':lines += field_targets(book,None,'source-differences')
            lines += [r'\input{\StudyRoot/CS5489/exam-review/Midterm/frontmatter/source-differences.tex}']
        lines += [r'\clearpage\StudyHeading{1}{原卷索引 / Original-paper index}',
                  r'按原卷题号查找本册位置；不同年份的重复题指向同一MT编号。2021B*保留题纸与配套答案的年份冲突。']
        lines += field_targets(book,None,'paper-index-start')
        for paper in INDEX['papers']:
            lines += [r'\subsection*{'+escape(paper['label'])+'}']
            lines += [r'\StudyTarget{'+book+'__'+alias+'}' for alias,v in ALIASES.get(book,{}).items() if v.get('paper')==paper['id']]
            lines += [
                      r'\begin{longtable}{@{}p{.2\linewidth}p{.56\linewidth}p{.18\linewidth}@{}}',
                      r'\toprule 原题 & 本册题号与页码 & 分值 \\ \midrule\endhead']
            entries=[(o,q) for q in selected(book) for o in q['occurrences'] if o['paper']==paper['id']]
            for o,q in sorted(entries,key=lambda v:int(v[0]['question'][1:])):
                lines += [escape(o['question'])+' & '+r'\StudyRef{'+book+'}{'+q['id'].lower()+'}{'+q['id']+'} & '+str(o['marks'])+r' \\']
            lines += [r'\bottomrule\end{longtable}']
    lines += [r'\end{document}','']
    path=ROOT/'latex/books'/f'{book}.tex'
    path.write_text('\n'.join(lines))
    return path


def all_refs():
    refs=set()
    for p in [ROOT/d['source'] for d in DOCS]+list((MID/'items').rglob('*.tex'))+list((MID/'frontmatter').glob('*.tex')):
        refs.update(re.findall(r'\\StudyRef\{([^}]+)\}\{([^}]+)\}',p.read_text()))
    for kind in KINDS:
        refs.update((kind,q['id'].lower()) for q in INDEX['questions'])
    return refs


REFS=all_refs()
DOC_BOOK={d['id']:d['course'] or 'Foundations' for d in DOCS}
DOC_BOOK.update({k:k for k in KINDS})


def refs_file(book,resources):
    lines=[r'\renewcommand{\StudySourceRef}{'+SOURCE_REF+'}',r'\renewcommand{\StudyDate}{'+SOURCE_DATE+'}']+resources
    for d in DOCS:
        stem=Path(d['source']).stem
        label=re.sub(r'(Lecture|Chapter|Tutorial|Assignment)0?(\d+)',r'\1 \2',stem)
        lines.append(r'\expandafter\def\csname studytitle@'+d['id']+r'\endcsname{'+(d['course'] or '基础')+' · '+escape(label)+'}')
    chosen={q['id'].lower() for q in selected(book)}
    for doc,anchor in sorted(REFS):
        effective=book if book in KINDS[2:] and doc in ['Questions','Answers'] and anchor in chosen else doc
        target_book=DOC_BOOK[effective]
        key=effective+'__'+anchor
        page=MAPS.get(target_book,{}).get(key)
        own=target_book==book or book=='Sample' and effective in ['CS5222-Chapter03','CS5489-Lecture02']
        if own:
            body=r'\hyperlink{'+key+r'}{#1}{\scriptsize（本册 p.\pageref*{'+key+'}）}'
        else:
            rel=os.path.relpath(output(target_book),output(book).parent).replace(os.sep,'/')
            label={'CS5489':'CS5489册','CS5222':'CS5222册','Foundations':'基础册','Questions':'题目册','Answers':'解析册'}.get(target_book,target_book)
            n=str(page) if page is not None else '??'
            body=r'\href{'+rel+r'\#page='+n+r'}{#1}{\scriptsize（'+label+' p.'+n+'）}'
        lines.append(r'\expandafter\def\csname studyref@'+doc+'@'+anchor+r'\endcsname#1{'+body+'}')
    folder=BUILD/book;folder.mkdir(exist_ok=True)
    (folder/'refs.tex').write_text('\n'.join(lines)+'\n')


def compile_book(book):
    env=dict(os.environ)
    local=ROOT/'.build/texmf'
    if local.is_dir():env['TEXMFHOME']=str(local)
    env['TEXINPUTS']=str(ROOT/'latex/vendor/elegantbook')+'//:'+env.get('TEXINPUTS','')
    path=driver(book)
    folder=BUILD/book
    command=[ARGS.engine,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error',
             '-file-line-error','-output-directory='+str(folder),path.name]
    result=subprocess.run(command,cwd=path.parent,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (folder/'compile-output.log').write_text(result.stdout)
    if result.returncode:
        print(result.stdout[-2800:],file=sys.stderr)
        raise RuntimeError(f'{book}: XeLaTeX failed; see {folder}/compile-output.log')
    mapping={}
    for line in (folder/(book+'.pages')).read_text().splitlines():
        if '|' not in line:continue
        key,page=line.rsplit('|',1)
        if not page.isdigit():raise RuntimeError((book,line))
        if key in mapping:raise RuntimeError(('Duplicate TeX destination',book,key))
        mapping[key]=int(page)
    print(book,len(PdfReader(folder/(book+'.pdf')).pages),'pages',flush=True)
    return book,mapping


def main():
    global MAPS
    resources=notebook_assets()+image_assets()
    for book in BOOKS:
        driver(book);refs_file(book,resources)
    if ARGS.prepare_only:return
    for round_ in range(ARGS.rounds):
        before=json.dumps(MAPS,sort_keys=True)
        for book in BOOKS:refs_file(book,resources)
        with ThreadPoolExecutor(max_workers=max(1,ARGS.jobs)) as pool:
            futures=[pool.submit(compile_book,b) for b in BOOKS]
            for f in as_completed(futures):
                book,mapping=f.result();MAPS[book]=mapping
        MAP_FILE.write_text(json.dumps(MAPS,ensure_ascii=False,indent=2)+'\n')
        stable=before==json.dumps(MAPS,sort_keys=True)
        print('Cross-book page map stable:',stable,flush=True)
        if stable and round_>=1:break
    else:raise RuntimeError('Page maps did not stabilize; existing published PDFs retained')
    if BOOKS==['Sample']:return
    if ARGS.no_publish:
        print('Candidate editions compiled; published files retained.',flush=True)
        return
    publish()


def publish():
    from latex_project import stubs, MANIFEST, PAGE_MAP
    targets=set(stubs(MAPS))|{ROOT/d['notebook'] for d in DOCS if 'notebook' in d}
    targets|={output(b) for b in BOOKS}|{MANIFEST,PAGE_MAP,ROOT/'pdf/manifest.json',ROOT/'pdf/README.md',MID/'PaperIndex.md',MID/'PageIndex.json'}
    targets|={MID/(b+'PageIndex.json') for b in KINDS[2:]}
    before={p:p.read_bytes() if p.exists() else None for p in targets}
    try:_publish()
    except BaseException:
        for path,data in before.items():
            if data is None:path.unlink(missing_ok=True)
            elif not path.exists() or path.read_bytes()!=data:path.write_bytes(data)
        raise


def _publish():
    from latex_project import binding, stubs, notebook_markdown, MANIFEST, PAGE_MAP
    if not all(b in MAPS for b in COURSES+KINDS):
        raise RuntimeError('First publication requires all nine editions; use the default full build')
    # Reject unresolved destinations and layout failures before touching published PDFs.
    import pymupdf
    for book in BOOKS:
        folder=BUILD/book
        log=(folder/(book+'.log')).read_text(errors='replace')
        if re.search(r'Missing character:|undefined references|Reference .* undefined',log):
            raise RuntimeError((book,'Unresolved reference or missing glyph; see TeX log'))
        overfull=[float(x) for x in re.findall(r'Overfull \\[hv]box \(([\d.]+)pt',log)]
        if any(x>1 for x in overfull):raise RuntimeError((book,'Content exceeds its typesetting area',overfull))
        with pymupdf.open(folder/(book+'.pdf')) as pdf:
            for page in pdf:
                if '待定页' in page.get_text() or 'p.??' in page.get_text():
                    raise RuntimeError((book,page.number+1,'Unresolved printed page reference'))
                for link in page.get_links():
                    if '??' in link.get('uri',''):raise RuntimeError((book,'Unresolved link',link))
    # The only Notebook mutation is generated navigation in Markdown cells.
    for d in DOCS:
        if 'notebook' not in d:continue
        path=ROOT/d['notebook'];nb=nbformat.read(path,as_version=4)
        before=[dict(c) for c in nb.cells if c.cell_type=='code']
        for i,c in enumerate(nb.cells):
            if c.cell_type=='markdown':c.source=notebook_markdown(d,i,c,MAPS)
        assert before==[dict(c) for c in nb.cells if c.cell_type=='code']
        nbformat.write(nb,path)
    for path,text in stubs(MAPS).items():path.write_text(text)
    stage=BUILD/'publication';stage.mkdir(exist_ok=True)
    manifest=json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {'schema':1,'template':'ElegantBook 4.7','books':{}}
    for book in BOOKS:
        digest,files=binding(book)
        reader=PdfReader(BUILD/book/(book+'.pdf'));writer=PdfWriter();writer.clone_document_from_reader(reader)
        writer.add_metadata({'/StudyNotesEdition':book,'/StudyNotesSourceSHA256':digest,'/StudyNotesSourceRef':SOURCE_REF,'/StudyNotesTemplate':'ElegantBook 4.7'})
        path=stage/(book+'.pdf')
        with path.open('wb') as f:writer.write(f)
        manifest['books'][book]={'file':output(book).relative_to(ROOT).as_posix(),'pages':len(reader.pages),'sha256':sha(path),'source_sha256':digest,'source_ref':SOURCE_REF,'inputs':files,'diagnostics':{'missing_glyphs':0,'unresolved_references':0,'overfull_boxes':[float(x) for x in re.findall(r'Overfull \\[hv]box \(([\d.]+)pt', (BUILD/book/(book+'.log')).read_text(errors='replace'))]}}
    # All compilation and source checks finish before the publication transaction.
    replacements={output(book):stage/(book+'.pdf') for book in BOOKS}
    backups={p:p.read_bytes() if p.exists() else None for p in replacements}
    try:
        for target,path in replacements.items():os.replace(path,target)
    except BaseException:
        for p,contents in backups.items():
            if contents is None:p.unlink(missing_ok=True)
            else:p.write_bytes(contents)
        raise
    PAGE_MAP.write_text(json.dumps({b:MAPS[b] for b in COURSES+KINDS},ensure_ascii=False,indent=2)+'\n')
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    course_manifest={'updated':SOURCE_DATE,'books':[]}
    readme=['# A4 学习讲义','', 'A4、100%实际大小、双面长边翻转；各册独立分页。正文在同名 `.tex` 主稿维护。','']
    for book in COURSES:
        meta=manifest['books'][book];documents=[];records=[d for d in DOCS if (d['course'] or 'Foundations')==book]
        readme += ['## '+book,'','| 文档 | 页码 |','|---|---|']
        for i,d in enumerate(records):
            start=MAPS[book][d['id']+'__root'];end=MAPS[book][records[i+1]['id']+'__root']-1 if i+1<len(records) else meta['pages']
            documents.append({'id':d['id'],'start':start,'end':end,'group':book,'source':d['source']})
            readme.append('| ['+d['id']+'](../'+d['source']+') | ['+str(start)+'–'+str(end)+']('+book+'-A4.pdf#page='+str(start)+') |')
        course_manifest['books'].append({**{k:meta[k] for k in ['pages','sha256','source_sha256']},'file':book+'-A4.pdf','documents':documents});readme.append('')
    (ROOT/'pdf/manifest.json').write_text(json.dumps(course_manifest,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'pdf/README.md').write_text('\n'.join(readme).rstrip()+'\n')
    bankmaps={b:{q['id'].lower():MAPS[b][b+'__'+q['id'].lower()] for q in selected(b)} for b in KINDS}
    (MID/'PageIndex.json').write_text(json.dumps({b:bankmaps[b] for b in KINDS[:2]},ensure_ascii=False,indent=2)+'\n')
    for book in KINDS[2:]:(MID/(book+'PageIndex.json')).write_text(json.dumps({book:bankmaps[book]},ensure_ascii=False,indent=2)+'\n')
    lines=['# 原卷索引','', '按各册最终 PDF 的独立页码回查。2021B*保留封面年份冲突；完整原卷和个人批注不随题库发布。','']
    for paper in INDEX['papers']:
        lines+=['## '+paper['label'],'','| 原题 | 题库 | 题目 | 答案 | 合订 | 精简 | 题型分册 |','|---|---|---|---|---|---|---|']
        rows=[(o,q) for q in INDEX['questions'] for o in q['occurrences'] if o['paper']==paper['id']]
        for o,q in sorted(rows,key=lambda v:int(v[0]['question'][1:])):
            edition='MultipleChoice' if q['response_type']=='multiple_select' else 'WrittenResponse'
            links=['[p.'+str(bankmaps[b][q['id'].lower()])+']('+b+'.pdf#page='+str(bankmaps[b][q['id'].lower()])+')' for b in KINDS[:4]+[edition]]
            lines+=['| '+o['question']+' | '+q['id']+' | '+' | '.join(links)+' |']
        lines.append('')
    (MID/'PaperIndex.md').write_text('\n'.join(lines).rstrip()+'\n')
    print('Published '+str(len(BOOKS))+' verified compilations with independent page maps.',flush=True)


if __name__=='__main__':main()
