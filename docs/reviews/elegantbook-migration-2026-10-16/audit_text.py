from pathlib import Path
import json,re,hashlib
import markdown,nbformat
from bs4 import BeautifulSoup
root=Path.cwd();base=root/'.build/elegantbook-migration/baseline';config=json.loads((root/'latex/documents.json').read_text())
reports=[];fail=[]
for d in config['documents']:
 original=base/d['legacy_source']
 if original.suffix=='.ipynb':old='\n\n'.join(c.source for c in nbformat.read(original,as_version=4).cells if c.cell_type=='markdown')
 else:old=original.read_text()
 html=BeautifulSoup(markdown.markdown(old,extensions=['tables','fenced_code','toc','md_in_html','pymdownx.arithmatex'],extension_configs={'pymdownx.arithmatex':{'generic':True}}),'html.parser')
 for tag in html.select('.toc,.arithmatex'):tag.decompose()
 codes=[p.get_text().rstrip('\n') for p in html.find_all('pre')]
 for tag in html.find_all('pre'):tag.decompose()
 text=(root/d['source']).read_text()
 actual_codes=re.findall(r'\\begin\{StudyCode\}\n(.*?)\n\\end\{StudyCode\}',text,re.S)
 assert actual_codes==codes,(d['id'],'authored code blocks changed')
 text=re.sub(r'\\begin\{StudyCode\}.*?\\end\{StudyCode\}','',text,flags=re.S)
 text=re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)','',text,flags=re.S)
 text=re.sub(r'\\StudyTarget\{[^}]*\}','',text)
 text=re.sub(r'\\midrule\\endfirsthead.*?\\midrule\\endhead','',text,flags=re.S)
 old_chinese=''.join(re.findall(r'[\u3400-\u9fff]',html.get_text()))
 new_chinese=''.join(re.findall(r'[\u3400-\u9fff]',text))
 ok=old_chinese==new_chinese
 report={'document':d['id'],'chinese_characters':len(old_chinese),'chinese_sequence_preserved':ok,'authored_code_blocks':len(codes),'code_blocks_exact':True}
 reports.append(report)
 if not ok:
  import difflib
  diffs=[(op,old_chinese[a:b],new_chinese[c:e]) for op,a,b,c,e in difflib.SequenceMatcher(None,old_chinese,new_chinese,autojunk=False).get_opcodes() if op!='equal']
  fail.append((d['id'],diffs[:5]))
print(json.dumps(fail,ensure_ascii=False,indent=2))
(root/'docs/reviews/elegantbook-migration-2026-10-16/full-text-preservation.json').write_text(json.dumps({'scope':'All teaching prose including generated exam blocks; mathematical expressions checked separately; saved Notebook code/output guarded independently','documents':reports,'failures':fail},ensure_ascii=False,indent=2)+'\n')
