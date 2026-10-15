from pathlib import Path
import json,re,sys,unicodedata
import markdown,pymupdf
from bs4 import BeautifulSoup
root=Path.cwd();base=root/'.build/elegantbook-migration/baseline/CS5489/exam-review/Midterm';sys.path.insert(0,str(base/'tools'))
from assemble_combined import question_blocks
qblocks=question_blocks((base/'Questions.md').read_text());ablocks=question_blocks((base/'Answers.md').read_text())
index=json.loads((root/'CS5489/exam-review/Midterm/QuestionIndex.json').read_text());maps=json.loads((root/'latex/page-maps.json').read_text())
normal=lambda s:''.join(re.findall(r'[A-Za-z0-9]',unicodedata.normalize('NFKC',s))).lower()
fail=[];checked=0
for book in ['Questions','Answers','Combined','Compact','MultipleChoice','WrittenResponse']:
 pdf=pymupdf.open(root/'CS5489/exam-review/Midterm'/(book+'.pdf'));text=[re.sub(r'\n\d+\s*\Z','',p.get_text()).replace('CityU StudyNotes','').replace(book,'') for p in pdf]
 selected=[q for q in index['questions'] if book not in ['MultipleChoice','WrittenResponse'] or q['response_type']==('multiple_select' if book=='MultipleChoice' else 'written')]
 for j,q in enumerate(selected):
  qid=q['id'];start=maps[book][book+'__'+qid.lower()];end=maps[book][book+'__'+selected[j+1]['id'].lower()] if j+1<len(selected) else len(pdf)
  window=normal(''.join(text[start-1:end]))
  fields={}
  if book!='Answers':fields['question-en']=qblocks[qid].split('### English question\n',1)[1].split('### 中文题意\n',1)[0]
  if book!='Questions':fields['answer-en']=ablocks[qid].split('### English answer\n',1)[1].split('### 中文对应答案\n',1)[0]
  for name,body in fields.items():
   soup=BeautifulSoup(markdown.markdown(body,extensions=['tables','fenced_code','md_in_html','pymdownx.arithmatex'],extension_configs={'pymdownx.arithmatex':{'generic':True}}),'html.parser')
   for tag in soup.select('.arithmatex'):tag.replace_with('¶')
   chunks=[normal(x) for x in re.split(r'¶|\n',soup.get_text()) if len(normal(x))>=18]
   for s in chunks:
    checked+=1
    if s not in window:fail.append({'book':book,'question':qid,'field':name,'fragment':s[:150]})
print('Checked prose fragments:',checked,'; extraction mismatches:',len(fail));print(json.dumps(fail[:10],ensure_ascii=False,indent=2))
(root/'docs/reviews/elegantbook-migration-2026-10-16/pdf-english-preservation.json').write_text(json.dumps({'checked_fragments':checked,'extraction_mismatches':fail,'scope':'Long English prose fragments outside math; each searched only in its own question page range, including a shared next-question page when continuous layout requires it'},ensure_ascii=False,indent=2)+'\n')
