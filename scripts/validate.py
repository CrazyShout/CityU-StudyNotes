"""Validate collaborative sources, local references and committed A4 files."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import hashlib,json,re
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
manifest=json.loads((ROOT/'pdf/manifest.json').read_text())
for book in manifest['books']:
    p=ROOT/'pdf'/book['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==book['sha256'],p
    reader=PdfReader(p,strict=True);assert len(reader.pages)==book['pages']
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
