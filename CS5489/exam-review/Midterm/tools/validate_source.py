"""Validate the editable midterm manuscripts and their complete six-paper mapping."""
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from urllib.parse import urlsplit,unquote
import argparse,json,re
from book_support import validate_catalog
import markdown
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check',action='store_true',help='Validate without writing any files')
parser.add_argument('--source-dir',type=Path,help='Optionally verify original archive files named Sxxx.ext')
args=parser.parse_args()
idx=json.loads((ROOT/'QuestionIndex.json').read_text())
ids=[q['id'] for q in idx['questions']]
assert len(ids)==len(set(ids))==idx['unique_questions']==67
assert len(idx['papers'])==6 and len({p['id'] for p in idx['papers']})==6
assert sum(len(q['legacy_ids']) for q in idx['questions'])==15
positions=[(o['paper'],o['question']) for q in idx['questions'] for o in q['occurrences']]
assert len(positions)==len(set(positions))==78
for paper in idx['papers']:
    assert {n for p,n in positions if p==paper['id']}=={f'Q{i}' for i in range(1,14)}
assert all(o['paper'].startswith('M') and o['paper']!='MOCK' for q in idx['questions'] for o in q['occurrences'])
soups={};formulae=[];reports=[]
for kind in ['Questions','Answers']:
    p=ROOT/f'{kind}.md';s=p.read_text()
    found=re.findall(r'^## (MT\d{3})',s,re.M);assert found==ids
    assert not re.search(r'SYMBOL TO VERIFY|ANSWER HERE|TODO|Student ID|Seat Number',s)
    for qid in ids:
        block=re.search(r'^## '+qid+r' .*?(?=\n<a id="mt|\Z)',s,re.M|re.S)[0]
        labels=['### English question','### 中文题意'] if kind=='Questions' else ['### 中文题意','### English answer','### 中文对应答案','### 中文讲解','**答案依据：**']
        assert all(block.count(v)==1 for v in labels),(kind,qid,'Missing or repeated section')
        assert [block.index(v) for v in labels]==sorted(block.index(v) for v in labels),(kind,qid,'Section order')
        if kind=='Answers':
            counterpart=block.split('### 中文对应答案\n')[1].split('### 中文讲解\n')[0].strip()
            assert re.search(r'[\u4e00-\u9fff]',counterpart),(qid,'Missing Chinese answer text')
        assert re.search(r'[\u4e00-\u9fff]',block)
    soup=BeautifulSoup(markdown.markdown(s,extensions=['tables','toc','md_in_html','pymdownx.arithmatex'],extension_configs={'pymdownx.arithmatex':{'generic':True}}),'html.parser')
    soups[kind]=soup
    for el in soup.select('.arithmatex'):
        t=el.get_text()
        display=el.name=='div'
        t=t.removeprefix('\\[' if display else '\\(').removesuffix('\\]' if display else '\\)')
        formulae.append({'kind':kind,'display':display,'tex':t})
    reports.append({'kind':kind,'questions':len(found),'math_expressions':len(soup.select('.arithmatex'))})
qtext=(ROOT/'Questions.md').read_text();atext=(ROOT/'Answers.md').read_text()
for qid in ids:
    qb=re.search(r'^## '+qid+r' .*?(?=\n<a id="mt|\Z)',qtext,re.M|re.S)[0]
    ab=re.search(r'^## '+qid+r' .*?(?=\n<a id="mt|\Z)',atext,re.M|re.S)[0]
    qprompt=qb.split('### 中文题意\n')[1].split('[题目](')[0].strip()
    aprompt=ab.split('### 中文题意\n')[1].split('### English answer')[0].strip()
    assert aprompt.startswith(qprompt),(qid,'Chinese prompt differs')
    # Some source figures sit before the Chinese prompt in Questions. Answers repeats
    # those exact figures/captions after the prompt so each answer remains standalone.
    extra=aprompt[len(qprompt):].strip()
    for paragraph in re.split(r'\n\s*\n',extra) if extra else []:
        assert (paragraph.startswith('![') or (paragraph.startswith('*') and paragraph.endswith('*'))) and paragraph in qb, (qid,'Unexpected text after repeated Chinese prompt')
    qimages=set(re.findall(r'!\[[^\]]*\]\(([^)]+)\)',qb))
    aimages=set(re.findall(r'!\[[^\]]*\]\(([^)]+)\)',aprompt))
    assert qimages==aimages,(qid,'Prompt figures differ')
for kind,soup in soups.items():
    for e in soup.select('a[href],img[src]'):
        link=e.get('href',e.get('src'));u=urlsplit(link)
        if u.scheme:continue
        target=ROOT/unquote(u.path) if u.path else ROOT/f'{kind}.md'
        assert target.exists(),(kind,link)
        if u.fragment and target.stem in soups:assert soups[target.stem].find(id=u.fragment),(kind,link)
catalog_checks=validate_catalog(ROOT,idx,args.source_dir)
for kind,soup in soups.items():
    for question in idx['questions']:
        for alias in question['legacy_ids']:
            assert soup.find(id=alias.lower()), (kind,'Missing legacy alias',alias)
assert json.loads((ROOT/'CalculationChecks.json').read_text())['status']=='passed'
result={'status':'source_checks_passed','unique_question_answer_pairs':67,'original_positions':78,'independent_midterms':6,'legacy_aliases':15,**catalog_checks,'documents':reports,'pdf_status':'requires separate render and visual verification'}
if not args.check:
    build=ROOT/'.build';build.mkdir(exist_ok=True)
    (build/'formulae.json').write_text(json.dumps(formulae,ensure_ascii=False)+'\n')
    (ROOT/'SourceValidation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
