"""Validate collaborative sources, local references and committed A4 files."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import hashlib,json,re,subprocess,sys,importlib.util
import markdown,nbformat
from bs4 import BeautifulSoup
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
registry=json.loads((ROOT/'learning/course-notes-documents.json').read_text());docs=registry['documents'];soups={};issues=[]
paths={ROOT/d['source'] for d in docs}|{ROOT/'README.md',ROOT/'CONTRIBUTING.md',ROOT/'AGENTS.md'}|set((ROOT/'docs').glob('*.md'))|{ROOT/'pdf/README.md'}
for p in paths:
    assert p.is_file(),p
    if p.suffix=='.ipynb':
        nb=nbformat.read(p,as_version=4);nbformat.validate(nb)
        for c in nb.cells:
            if c.cell_type=='code':
                assert c.execution_count is not None,(p,'missing output count')
                assert not any(o.output_type=='error' for o in c.outputs),(p,'saved error')
                compile(c.source,str(p),'exec')
        text='\n\n'.join(c.source for c in nb.cells if c.cell_type=='markdown')
    else:text=p.read_text()
    assert '/Users/' not in text and 'file://' not in text,(p,'machine-local path')
    soup=BeautifulSoup(markdown.markdown(text,extensions=['tables','fenced_code','toc','md_in_html','pymdownx.arithmatex']), 'html.parser');soups[p.resolve()]=soup
for p,soup in soups.items():
    for tag in soup.select('a[href],img[src]'):
        href=tag.get('href',tag.get('src'));u=urlsplit(href)
        if u.scheme or u.netloc:continue
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        if not target.is_relative_to(ROOT) or not target.exists():issues.append((str(p.relative_to(ROOT)),href));continue
        if u.fragment and target in soups and not soups[target].find(id=unquote(u.fragment)):
            issues.append((str(p.relative_to(ROOT)),href,'missing anchor'))
assert not issues,issues
# Registered order must keep theory before tutorials and assignments in each course.
for course in ['CS5489','CS5222']:
    stems=[Path(d['source']).stem for d in docs if d['major'] and d['course']==course]
    ranks=[0 if s.startswith(('Lecture','Chapter')) else 1 if s.startswith('Tutorial') else 2 for s in stems]
    assert ranks==sorted(ranks),(course,'document ordering')
# Lecture 2 display equations are numbered once, in reading order.
lecture=(ROOT/'CS5489/course-notes/Lecture02.md').read_text()
blocks=re.findall(r'\$\$(.*?)\$\$',lecture,re.S)
# Keep later references stable when one numbered calculation gains subparts.
supplements={14:['2.14a','2.14b','2.14c'],16:['2.16a','2.16b','2.16c'],35:['2.35a','2.35b']}
expected_tags=[tag for i in range(1,37) for tag in ((['2.21a','2.21b'] if i==21 else [f'2.{i}'])+supplements.get(i,[]))]
assert len(blocks)==len(expected_tags),('Lecture02 displayed equation count',len(blocks))
equation_numbers=[]
for block,expected in zip(blocks,expected_tags):
    tags=re.findall(r'\\tag\{([^}]+)\}',block)
    assert tags==[expected],('Lecture02 equation numbering',expected,tags)
    equation_numbers.append(f'({expected})')
# Exam links must lead to the ability they name, not merely to a valid anchor.
for anchor in ['decision-boundaries','gaussian-nb-boundary','model-limits','qe-parameter-posterior-note']:
    assert lecture.count(f'id="{anchor}"')==1,('Lecture02 teaching anchor',anchor)
for anchor in ['decision-boundaries','model-limits']:
    assert lecture.count(f'<!-- EXAM:focus-{anchor}:START -->')==1
for stale in ['log-scores','comparison']:
    assert f'<!-- EXAM:focus-{stale}:START -->' not in lecture
assert '[相关MLE基础](#prior-mle) · [QE残题说明](#qe-parameter-posterior-note)' in lecture
# Regression check: source-index links must not be stolen by new Chinese headings.
spec=importlib.util.spec_from_file_location('notes_previews',ROOT/'CS5489/course-notes/tools/build_previews.py')
previews=importlib.util.module_from_spec(spec);spec.loader.exec_module(previews)
for n in [1,5]:
    source=ROOT/f'CS5489/course-notes/Lecture{n:02}.md'
    rendered=BeautifulSoup(previews.wrap('anchor check',previews.md(source.read_text()),source),'html.parser')
    target=rendered.find(id='_2')
    heading=target if target and target.name=='h2' else target.find_next('h2') if target else None
    assert heading and '覆盖索引' in heading.get_text(),(source.name,'legacy source-index target')

subprocess.run([sys.executable,str(ROOT/'scripts/build_exam_annotations.py'),'--check'],check=True)
# Other authored display formulas are numbered by document, not by experiment cell.
numbered_documents={}
for record in docs:
    path=ROOT/record['source']
    if path.name=='Lecture02.md':continue
    if path.suffix=='.ipynb':
        source='\n\n'.join(c.source for c in nbformat.read(path,as_version=4).cells if c.cell_type=='markdown')
    else:source=path.read_text()
    displayed=re.findall(r'\$\$(.*?)\$\$',source,re.S)
    if not displayed:continue
    stem=path.stem
    if stem.startswith(('Lecture','Chapter')):prefix=str(int(stem[-2:]))
    elif stem.startswith('Tutorial'):prefix='T'+str(int(stem[-2:]))
    elif stem.startswith('Assignment'):prefix='A'+str(int(stem[-2:]))
    else:prefix={'MathForML':'M','NetworkBasics':'N'}[stem]
    inserted={
        'CS5489/course-notes/Lecture03.md':{1:['3.1a'],6:['3.6a'],11:['3.11a','3.11b'],13:['3.13a']},
        'CS5489/course-notes/Lecture04.md':{3:['4.3a','4.3b'],7:['4.7a'],15:['4.15a'],16:['4.16a']},
        'CS5489/course-notes/Lecture05.md':{8:['5.8a'],9:['5.9a'],11:['5.11a']},
    }.get(record['source'],{})
    main_count=len(displayed)-sum(len(v) for v in inserted.values())
    expected=[tag for i in range(1,main_count+1) for tag in [f'{prefix}.{i}']+inserted.get(i,[])]
    actual=[]
    for formula in displayed:
        tags=re.findall(r'\\tag\{([^}]+)\}',formula)
        assert len(tags)==1,(record['source'],'missing/duplicate formula tag')
        actual+=tags
    assert actual==expected,(record['source'],actual,expected)
    numbered_documents[record['source']]=(prefix,expected)

printed_cs=[x for x in docs if x['course']=='CS5489' and (x['major'] or x.get('print_appendix'))]
assert printed_cs[-1]['source']=='CS5489/course-notes/ExamIndex.md'
manifest=json.loads((ROOT/'pdf/manifest.json').read_text())
for book in manifest['books']:
    p=ROOT/'pdf'/book['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==book['sha256'],p
    reader=PdfReader(p,strict=True);assert len(reader.pages)==book['pages']
    if book['file']=='CS5489-A4.pdf':
        document=next(d for d in book['documents'] if d['id']=='CS5489-Lecture02')
        text='\n'.join(reader.pages[i-1].extract_text() or '' for i in range(document['start'],document['end']+1))
        assert not re.search(r'EXAM:(overview|focus|topics)',text),'Source markers must not appear in the PDF'
        printed=re.findall(r'\(2\.\d+[a-z]?\)',text)
        assert printed==equation_numbers,('Printed Lecture02 equation tags',printed)

    for document in book['documents']:
        if document['source'] not in numbered_documents:continue
        prefix,expected=numbered_documents[document['source']]
        text='\n'.join(reader.pages[i-1].extract_text() or '' for i in range(document['start'],document['end']+1))
        printed=[n for n in re.findall(r'\(('+re.escape(prefix)+r'\.\d+[a-z]?)\)',text) if n in expected]
        assert printed==expected,(document['source'],'printed equation numbers',printed,expected)

    for page in reader.pages:
        assert abs(float(page.mediabox.width)-595.28)<2 and abs(float(page.mediabox.height)-841.89)<2
        for ref in page.get('/Annots',[]):
            uri=str(ref.get_object().get('/A',{}).get('/URI',''))
            assert not uri.startswith('file:') and '/Users/' not in uri,(p,uri)
            if 'github.com/CrazyShout/CityU-StudyNotes/blob/' in uri:
                assert not urlsplit(uri).path.endswith('.html'),(p,'PDF points to an ignored HTML intermediate',uri)
            if uri.endswith('.pdf') or '.pdf#page=' in uri:
                parsed=urlsplit(uri)
                if not parsed.scheme:assert (p.parent/parsed.path).is_file(),uri
print(json.dumps({'status':'passed','major_documents':sum(d['major'] for d in docs),'sources':len(docs),'pdf_pages':sum(b['pages'] for b in manifest['books']),'links':'all local links and anchors resolve'},ensure_ascii=False))
