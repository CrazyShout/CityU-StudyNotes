"""Refresh both PDF page columns from the stable final page maps."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
maps=json.loads((ROOT/'PageIndex.json').read_text())
p=ROOT/'PaperIndex.md';text=p.read_text()
text=text.replace('两册同一页码对应同一题。','两册按MT题号对应，分别查下表的题目页与答案页。')
text=text.replace('| 题答PDF页 |','| 题目PDF页 | 答案PDF页 |')
text=text.replace('|---|---|---|---:|---:|','|---|---|---|---:|---:|---:|')
rows=0
def update(m):
    global rows
    line=m[0];qid=re.search(r'\bMT\d{3}\b',line)[0].lower()
    cells=line.split('|');cells=cells[:5]
    rows+=1
    return '|'.join(cells)+f'| [{maps["Questions"][qid]}](Questions.pdf#page={maps["Questions"][qid]}) | [{maps["Answers"][qid]}](Answers.pdf#page={maps["Answers"][qid]}) |'
text=re.sub(r'^\| Q\d+ \|.*$',update,text,flags=re.M)
assert rows==78
p.write_text(text.rstrip()+'\n')
print('Updated',rows,'original-paper rows with independent question/answer pages.')
