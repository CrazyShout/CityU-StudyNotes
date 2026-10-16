from pathlib import Path
import json,re,sys,unicodedata,difflib
import markdown
from bs4 import BeautifulSoup
root=Path.cwd();base=root/'.build/elegantbook-migration/baseline/CS5489/exam-review/Midterm';sys.path.insert(0,str(base/'tools'))
from assemble_combined import question_blocks
qs=question_blocks((base/'Questions.md').read_text());ans=question_blocks((base/'Answers.md').read_text());reports=[];fail=[]
for qid in qs:
 fields={'question-en':qs[qid].split('### English question\n',1)[1].split('### 中文题意\n',1)[0], 'answer-en':ans[qid].split('### English answer\n',1)[1].split('### 中文对应答案\n',1)[0]}
 for field,old in fields.items():
  soup=BeautifulSoup(markdown.markdown(old,extensions=['tables','fenced_code','toc','md_in_html','pymdownx.arithmatex'],extension_configs={'pymdownx.arithmatex':{'generic':True}}),'html.parser')
  for t in soup.select('.arithmatex'):t.decompose()
  original=soup.get_text()
  text=(root/'CS5489/exam-review/Midterm/items'/qid/(field+'.tex')).read_text()
  text=re.sub(r'^%[^\n]*','',text,flags=re.M)
  text=re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)','',text,flags=re.S)
  text=re.sub(r'\\Study(?:Target|Image|CellImage)\{[^}]*\}','',text)
  text=re.sub(r'\\begin\{[^}]*\}(?:\[[^\]]*\])?|\\end\{[^}]*\}','',text)
  text=re.sub(r'\\(?:StudyRef|StudyRepoRef)\{[^}]*\}\{[^}]*\}','',text)
  text=re.sub(r'\\vphantom\{[^}]*\}','',text)
  text=re.sub(r'\\[a-zA-Z@]+\*?','',text)
  normal=lambda s:''.join(re.findall(r'[A-Za-z0-9]',unicodedata.normalize('NFKC',s)))
  a,b=normal(original),normal(text)
  ok=a==b;reports.append({'question':qid,'field':field,'alphanumeric_sequence_preserved':ok,'characters':len(a)})
  if not ok:fail.append((qid,field,[(op,a[x:y],b[z:w]) for op,x,y,z,w in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes() if op!='equal'][:5]))
print(json.dumps(fail,ensure_ascii=False,indent=2))
(root/'docs/reviews/elegantbook-migration-2026-10-16/english-preservation.json').write_text(json.dumps({'scope':'All English question and core-answer prose, including options; exact alphanumeric sequence after math removal; all removed mathematical expressions independently checked','fields':reports,'failures':fail},ensure_ascii=False,indent=2)+'\n')
