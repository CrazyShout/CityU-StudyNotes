"""Validate the sole TeX teaching source, saved experiments, nine PDFs and old links."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from collections import Counter
import argparse
import hashlib
import json
import re
import subprocess
import sys
import markdown
import nbformat
import pymupdf
from bs4 import BeautifulSoup
from pypdf import PdfReader
from latex_project import (ROOT,MID,COURSES,KINDS,ALL_BOOKS,DOCS,INDEX,CONFIG,ALIASES,FIELDS,
                           PAGE_MAP,MANIFEST,binding,output,selected,stubs,notebook_markdown,sha)
sys.path.insert(0,str(MID/'tools'))
from book_support import validate_catalog
from question_types import TASK_LABELS


def source_checks(source_dir=None):
    registry=json.loads((ROOT/'learning/course-notes-documents.json').read_text())['documents']
    formal=[x for x in registry if x['major'] or x.get('print_appendix') or x['course'] is None]
    assert [x['source'] for x in formal]==[d['source'] for d in DOCS]
    assert sum(x['major'] for x in registry)==21 and len(DOCS)==25
    for course in COURSES[:2]:
        stems=[Path(d['source']).stem for d in DOCS if d['course']==course and d['major']]
        order=[0 if s.startswith(('Lecture','Chapter')) else 1 if s.startswith('Tutorial') else 2 for s in stems]
        assert order==sorted(order),(course,'teaching order')
    paths=[ROOT/d['source'] for d in DOCS]+list((MID/'items').rglob('*.tex'))+list((MID/'frontmatter').glob('*.tex'))
    document_text={d['id']:(ROOT/d['source']).read_text() for d in DOCS}
    anchors={d:set(re.findall(r'\\StudyTarget\{'+re.escape(d)+r'__([^}]+)\}',t))|{'root'} for d,t in document_text.items()}
    anchors.update({k:set(v)|{q['id'] for q in selected(k)} for k,v in ALIASES.items()})
    for path in paths:
        assert path.is_file(),path
        text=path.read_text()
        assert not re.search(r'/Users/|file://|Student ID|Seat Number|ANSWER HERE|SYMBOL TO VERIFY',text),(path,'private path or placeholder')
        for doc,anchor in re.findall(r'\\StudyRef\{([^}]+)\}\{([^}]+)\}',text):
            assert doc in anchors and anchor in anchors[doc],(path,doc,anchor,'missing target')
        for name in re.findall(r'\\Study(?:Cell)?Image\{([^}]+)\}',text):assert (ROOT/name).is_file(),(path,name)
        for name in re.findall(r'\\StudyRepoRef\{([^}]+)\}',text):assert (ROOT/name).exists() and not name.endswith('.html'),(path,name)
    migration=json.loads((ROOT/'docs/reviews/elegantbook-migration-2026-10-16/migration-manifest.json').read_text())
    # Every previous course anchor, image, explicit equation number and math expression survives.
    math_count=0
    for rec in migration['course_documents']:
        text=(ROOT/rec['target']).read_text();doc=rec['docid']
        assert set(rec['anchors'])<=anchors[doc],(doc,'lost legacy anchors',set(rec['anchors'])-anchors[doc])
        assert set(rec['images'])<=set(re.findall(r'\\Study(?:Cell)?Image\{([^}]+)\}',text)),(doc,'lost image')
        original=[m['tex'] for m in rec['math']]
        actual=re.findall(r'\\\[(.*?)\\\]|\\\((.*?)\\\)',text,re.S)
        actual=[a or b for a,b in actual]
        norm=lambda s:re.sub(r'\s+','',s).replace(r'\lt','<').replace(r'\gt','>')
        available=Counter(norm(m) for m in actual)
        for m in original:
            value=norm(m);assert available[value]>0,(doc,'lost mathematical expression',m);available[value]-=1
        math_count+=len(original)
        oldtags=[tag for m in original for tag in re.findall(r'\\tag\{([^}]+)\}',m)]
        newtags=re.findall(r'\\tag\{([^}]+)\}',text)
        assert newtags==oldtags,(doc,'equation tags/order changed')
    protected=0
    for d in DOCS:
        if 'notebook' not in d:continue
        nb=nbformat.read(ROOT/d['notebook'],as_version=4);nbformat.validate(nb)
        baseline=migration['notebooks'][d['notebook']]
        assert nb.metadata==baseline['metadata']
        assert len(nb.cells)==len(baseline['cells'])
        for c,original in zip(nb.cells,baseline['cells']):
            assert c['id']==original['id'] and c.cell_type==original['type']
            assert c.metadata==original['metadata'],(d['notebook'],c['id'],'cell metadata changed')
            if c.cell_type=='code':
                digest=hashlib.sha256(json.dumps(dict(c),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
                assert digest==original['sha256'],(d['notebook'],c['id'],'code/output/metadata changed')
                assert c.execution_count is not None and not any(o.output_type=='error' for o in c.outputs)
                compile(c.source,d['notebook'],'exec');protected+=1
    ids=[q['id'] for q in INDEX['questions']]
    assert len(ids)==len(set(ids))==INDEX['unique_questions']==67
    positions=[(o['paper'],o['question']) for q in INDEX['questions'] for o in q['occurrences']]
    assert len(positions)==len(set(positions))==78
    assert len(INDEX['papers'])==6 and sum(len(q['legacy_ids']) for q in INDEX['questions'])==15
    for p in INDEX['papers']:assert {q for paper,q in positions if paper==p['id']}=={f'Q{i}' for i in range(1,14)}
    types=Counter()
    original_questions={q['id']:q['fields'] for q in migration['questions']}
    def expanded(path,stack=()):
        assert path not in stack,('Cyclic TeX input',path)
        def include(match):
            target=(ROOT/match[1]).resolve();assert target.is_relative_to(ROOT)
            return expanded(target,stack+(path,))
        return re.sub(r'\\input\{\\StudyRoot/([^}]+)\}',include,path.read_text())
    for q in INDEX['questions']:
        files={f:expanded(MID/'items'/q['id']/(f+'.tex')) for f in FIELDS}
        for field,record in original_questions[q['id']].items():
            source=files[field]
            formulas=[a or b for a,b in re.findall(r'\\\[(.*?)\\\]|\\\((.*?)\\\)',source,re.S)]
            normal=lambda s:re.sub(r'\s+','',s).replace(r'\lt','<').replace(r'\gt','>')
            actual=Counter(normal(s) for s in formulas)
            for m in record['math']:
                key=normal(m['tex']);assert actual[key]>0,(q['id'],field,'lost mathematical expression',m);actual[key]-=1
            assert set(record['images'])<=set(re.findall(r'\\Study(?:Cell)?Image\{([^}]+)\}',source)),(q['id'],field,'lost figure')
        english=files['question-en'];chinese=files['question-zh']
        expected='multiple_select' if 'select all that apply' in english.lower() else 'written'
        assert q['response_type']==expected;types[expected]+=1
        options=re.findall(r'^([A-E])\)',english,re.M)
        if expected=='multiple_select':
            assert options==list('ABCDE'[:len(options)]) and len(options) in [4,5],q['id']
            assert re.findall(r'(?<![A-Za-z])([A-E])）',chinese)==options,(q['id'],'Chinese options')
            direction='incorrect' if re.search(r'\bnot\s+(?:true|correct)\b',english,re.I) else 'correct'
            assert q['select']==direction
        else:assert not options and set(q['tasks'])<=set(TASK_LABELS) and q['tasks']
        assert re.search(r'[\u4e00-\u9fff]',files['answer-zh'])
        assert '答案依据' in files['explanation'],q['id']
        plain=lambda s:re.sub(r'^%[^\n]*\n','',s,flags=re.M).strip()
        assert plain(files['answer-prompt']).startswith(plain(chinese)),(q['id'],'Chinese prompt differs')
        qimages=set(re.findall(r'\\StudyImage\{([^}]+)\}',english+chinese))
        assert qimages==set(re.findall(r'\\StudyImage\{([^}]+)\}',files['answer-prompt'])),(q['id'],'answer prompt images')
    assert types=={'multiple_select':30,'written':37}
    assert set(q['id'] for q in selected('MultipleChoice')).isdisjoint(q['id'] for q in selected('WrittenResponse'))
    catalog=validate_catalog(MID,INDEX,source_dir)
    subprocess.run([sys.executable,str(ROOT/'scripts/build_exam_annotations.py'),'--check'],check=True)
    for script in [ROOT/'CS5222/course-notes/tools/depth_examples.py',MID/'tools/verify_calculations.py']:
        subprocess.run([sys.executable,str(script),'--check'] if script.name=='verify_calculations.py' else [sys.executable,str(script)],check=True)
    return {'major_documents':21,'formal_tex_documents':25,'protected_notebook_code_cells':protected,'preserved_course_math_expressions':math_count,'question_pairs':67,'original_positions':78,'question_types':dict(types),**catalog}


def publication_checks():
    maps=json.loads(PAGE_MAP.read_text());manifest=json.loads(MANIFEST.read_text());reports={}
    for path,expected in stubs(maps).items():assert path.read_text()==expected,('Regenerate compatibility navigation',path)
    for d in DOCS:
        if 'notebook' not in d:continue
        for i,c in enumerate(nbformat.read(ROOT/d['notebook'],as_version=4).cells):
            if c.cell_type=='markdown':assert c.source==notebook_markdown(d,i,c,maps),(d['notebook'],i,'generated Markdown differs')
    for book in ALL_BOOKS:
        path=output(book);meta=manifest['books'][book]
        assert meta['sha256']==sha(path),(book,'PDF hash differs')
        digest,files=binding(book)
        assert meta['source_sha256']==digest and meta['inputs']==files,(book,'PDF is stale for current TeX sources')
        reader=PdfReader(path,strict=True)
        assert reader.metadata['/StudyNotesSourceSHA256']==digest and reader.metadata['/StudyNotesEdition']==book
        destinations=reader.named_destinations
        for key,page in maps[book].items():
            assert key in destinations,(book,key,'PDF named destination missing')
            assert reader.get_destination_page_number(destinations[key])+1==page,(book,key,'page map differs')
        if book in KINDS:
            for a in ALIASES[book]:assert book+'__'+a in maps[book],(book,a,'legacy alias missing')
        with pymupdf.open(path) as pdf:
            assert len(pdf)==meta['pages']
            text='\n'.join(p.get_text() for p in pdf)
            assert not re.search(r'待定页|p\.\?\?|EXAM:(overview|topics|focus)|/Users/|file://',text),(book,'unexpected printed content')
            links=0
            for page in pdf:
                assert abs(page.rect.width-595.28)<2 and abs(page.rect.height-841.89)<2
                assert not list(page.annots() or []),(book,page.number+1,'non-link annotation')
                for link in page.get_links():
                    links+=1;uri=link.get('uri','')
                    assert not uri.startswith('file:') and '/Users/' not in uri
                    if link['kind']==1:assert 0<=link['page']<len(pdf),(book,'internal link invalid',link)
                    if '.pdf#page=' in uri:
                        u=urlsplit(uri);target=(path.parent/unquote(u.path)).resolve();page_no=int(u.fragment.split('=',1)[1])
                        target_book=next((b for b in ALL_BOOKS if output(b)==target),None)
                        assert target_book and 1<=page_no<=manifest['books'][target_book]['pages'],(book,uri)
                    if 'github.com/CrazyShout/CityU-StudyNotes/blob/' in uri:assert not urlsplit(uri).path.endswith('.html')
            toc=pdf.get_toc()
            assert toc,(book,'missing bookmarks')
            if book in KINDS:
                qtoc=[x for x in toc if re.match(r'MT\d{3} · ',x[1])]
                assert [x[1][:5] for x in qtoc]==[q['id'] for q in selected(book)],(book,'question order/bookmarks')
                for _,title,page in qtoc:assert page==maps[book][book+'__'+title[:5].lower()],(book,title,'bookmark destination differs')
            else:
                documents=[d for d in DOCS if (d['course'] or 'Foundations')==book]
                for i,d in enumerate(documents):
                    if (d['course'] or 'Foundations')!=book:continue
                    assert any(x[2]==maps[book][d['id']+'__root'] for x in toc),(d['id'],'missing chapter bookmark')
                    begin=maps[book][d['id']+'__root']
                    end=maps[book][documents[i+1]['id']+'__root']-1 if i+1<len(documents) else len(pdf)
                    expected=re.findall(r'\\tag\{([^}]+)\}',(ROOT/d['source']).read_text())
                    section='\n'.join(pdf[p-1].get_text() for p in range(begin,end+1))
                    actual=[x for x in re.findall(r'\(([A-ZTAMN0-9]+\.\d+[a-z]?)\)',section) if x in expected]
                    assert actual==expected,(d['id'],'printed equation labels/order',actual,expected)
            assert meta['diagnostics']['missing_glyphs']==0 and meta['diagnostics']['unresolved_references']==0
            assert not [x for x in meta['diagnostics']['overfull_boxes'] if x>1],(book,'overfull boxes',meta['diagnostics'])
            reports[book]={'pages':len(pdf),'links':links,'destinations':len(maps[book]),'sha256':meta['sha256']}
    # Engineering documents and generated legacy links resolve independently of ignored HTML.
    paths={ROOT/'README.md',ROOT/'CONTRIBUTING.md',ROOT/'AGENTS.md',ROOT/'pdf/README.md'}|set((ROOT/'docs').glob('*.md'))
    paths|={ROOT/d['legacy_source'] for d in DOCS if d['legacy_source'].endswith('.md')}|set(MID.glob('*.md'))
    soups={p:BeautifulSoup(markdown.markdown(p.read_text(),extensions=['tables','toc','fenced_code','md_in_html']),'html.parser') for p in paths}
    for p,soup in soups.items():
        assert '/Users/' not in p.read_text() and 'file://' not in p.read_text(),p
        for a in soup.select('a[href],img[src]'):
            uri=a.get('href',a.get('src'));u=urlsplit(uri)
            if u.scheme or u.netloc:continue
            dest=(p.parent/unquote(u.path)).resolve() if u.path else p
            assert dest.is_relative_to(ROOT) and dest.exists(),(p,uri)
            if u.fragment and dest in soups:assert soups[dest].find(id=unquote(u.fragment)),(p,uri,'missing anchor')
    return reports


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--source-only',action='store_true');parser.add_argument('--source-dir',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    report={'status':'source_checks_passed' if args.source_only else 'passed',**source_checks(args.source_dir)}
    if not args.source_only:report['books']=publication_checks()
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
