"""Generate Lecture 2 exam notes and the end-of-book index from one public ledger.

The ledger contains metadata and topic summaries only. Full questions/answers stay local.
"""
from pathlib import Path
import argparse,json,re
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/'CS5489/course-notes/exam-evidence/Lecture02.json'

def build():
 d=json.loads(LEDGER.read_text());papers={p['id']:p for p in d['papers']};sources={s['id']:s for s in d['sources']}
 assert len(papers)==len(d['papers']) and len({q['id'] for q in d['questions']})==len(d['questions'])
 assert {p['kind'] for p in papers.values()}=={'midterm','final','sample','qe'}
 assert all(not p['countable'] for p in papers.values() if p['kind'] in {'sample','qe'})
 for q in d['questions']:
  assert set(q['topics'])<=set(t['id'] for t in d['topics'])
  assert all(o['paper'] in papers and o['relation'] in {'direct','related','fragment'} for o in q['occurrences'])
 for p in papers.values():
  assert set(p['source_ids']+p['answer_source_ids'])<=sources.keys()
  assert not p.get('duplicate_of') or not p['countable']
 def occurrences(t):return [(q,o) for q in d['questions'] if t in q['topics'] for o in q['occurrences']]
 def ids(t,kind,relation):return sorted({o['paper'] for q,o in occurrences(t) if papers[o['paper']]['countable'] and papers[o['paper']]['kind']==kind and o['relation']==relation})
 def stats(t):return {'midterm':ids(t,'midterm','direct'),'final_direct':ids(t,'final','direct'),'final_related':ids(t,'final','related'),'qe_fragments':sorted({o['paper'] for q,o in occurrences(t) if papers[o['paper']]['kind']=='qe'}),'samples':sorted({o['paper'] for q,o in occurrences(t) if papers[o['paper']]['kind']=='sample'})}
 counts={t['id']:stats(t['id']) for t in d['topics']}
 def num(seq):return str(len(seq))+'套' if seq else '未见'
 def qetext(t):return '题段；卷次待定' if counts[t]['qe_fragments'] else '现有材料未见'
 labels={'generative':'反复考查：先分清三个概率','decision':'反复考查：先验与最优性的条件','nb':'反复考查：能完整写出模型','mle':'学习思想有直接题；推导也是基础','boundary':'反复比较：共享方差是否成立','covariance':'基础与后续聚类迁移都要懂','smoothing':'能解释零概率与如何调节','text':'结合设备条件提出具体改进','limits':'用条件或反例拆掉绝对说法','parameter-posterior':'QE延伸；补齐题面后再练完整推导'}
 inventory_counts={k:sum(p['countable'] and p['kind']==k for p in papers.values()) for k in ['midterm','final']}
 def paper_order(pid):
  p=papers[pid];return ({'midterm':0,'final':1,'sample':2,'qe':3}[p['kind']],p['year'] or 9999,p['term'] or '',pid)
 def question_order(pair):
  n=re.search(r'\d+',pair[1]['question']);return int(n.group()) if n else 999
 intro=['<div class="exam-overview" markdown="1">','<a id="exam-review"></a>','## Exam focus｜这一讲怎样安排复习','','先把生成式模型、Bayes决策和Gaussian NB讲清楚，再练分布假设、边界与模型局限。下面的卷数用于安排练习顺序；它描述手头历史材料，不预测本学期考题。','','| 考点 | 本轮复习重点 | 期中 | 期末：直接／关联 | QE记录 | 回到正文 |','|---|---|---|---|---|---|']
 for t in d['topics']:
  c=counts[t['id']];intro.append(f"| {t['title']} | {labels[t['id']]} | {num(c['midterm'])} | {num(c['final_direct'])}／{num(c['final_related'])} | {qetext(t['id'])} | [讲解](#{t['anchor']}) |")
 intro += ['',f'**统计口径：** 已辨识{inventory_counts["midterm"]}套期中、{inventory_counts["final"]}套期末；同一考点同卷只计一次。同卷答案、扫描件和压缩包副本不另计；模拟题另列，2021B*保留封面年份冲突说明。“未见”只表示现有材料未找到对应题。QE年份未载、原卷身份不完整，显示卷次待定。','','**标记：** <span class="exam-mark"><span class="exam-wave wave-mid"></span>绿色＝期中</span>　<span class="exam-mark"><span class="exam-wave wave-final"></span>黄色＝期末</span>　<span class="exam-mark"><span class="exam-wave wave-qe"></span>红色＝QE</span>。多类证据分层画线，文字同时说明类别；黑白打印看文字即可。','','题号与出处见[讲末考点索引](#exam-topic-index)；按试卷查阅见[全册附录](ExamIndex.md)。期末聚类是关联选做；QE参数后验不等于本讲的类别后验。']
 intro+=['</div>']
 end=['<a id="exam-topic-index"></a>','## Historical exam map｜按考点查题源','','各行保留原题号与原材料页码。同一卷在本表不同考点下出现，不会让该考点的卷数重复增加。材料文件、配套答案与版本差异见[按卷附录](ExamIndex.md)。','']
 for t in d['topics']:
  end += ['<div class="exam-topic-unit" markdown="1">',f"### {t['title']}",'',t['skill']+'。','', '| 考试类型与学期 | 原题号 | 原材料页 | 要求 |','|---|---|---|---|']
  grouped={}
  for q,o in occurrences(t['id']):
   key=(o['paper'],o['relation']);grouped.setdefault(key,[]).append((q,o))
  for pid,relation in sorted(grouped,key=lambda key:paper_order(key[0])):
   pairs=sorted(grouped[(pid,relation)],key=question_order)
   p=papers[pid];flag='关联选做' if relation=='related' else '残题' if relation=='fragment' else '模拟' if p['kind']=='sample' else '直接'
   end.append(f"| {p['label']} · {flag} | {'、'.join(o['question'] for q,o in pairs)} | {'、'.join(dict.fromkeys(o['pages'] for q,o in pairs))} | {'、'.join(dict.fromkeys(q['skill'] for q,o in pairs))} |")
  if t['id']=='parameter-posterior':end += ['','此题问的是参数后验与MAP，缺少前页模型和先验。当前只能核对通用步骤，不能据此登记某一分布的完整MLE推导已考过。']
  end += ['</div>','']
 notice={}
 for t in d['topics']:
  if t['id']=='parameter-posterior':continue
  c=counts[t['id']];classes=[];texts=[]
  if c['midterm']:classes+=['mid'];texts += [f"期中：{len(c['midterm'])}套"]
  if c['final_direct']:classes+=['final'];texts += [f"期末直接：{len(c['final_direct'])}套"]
  if c['final_related']:classes+=['final'];texts += [f"期末关联：{len(c['final_related'])}套"]
  if c['qe_fragments']:classes+=['qe'];texts+=['QE题段，年份未载／卷次待定']
  waves=''.join(f'<span class="exam-wave wave-{s}"></span>' for s in dict.fromkeys(classes))
  detail='；'.join(texts)
  if t['id']=='mle':detail+='。QE另问参数后验和MAP，不能当作类别决策题'
  notice[t['anchor']]=f'<p class="exam-focus"><span class="exam-mark">{waves}考点：{t["title"]}</span><br>{detail}。</p>'
 lesson=ROOT/'CS5489/course-notes/Lecture02.md';text=lesson.read_text()
 def marked(key,content):return f'<!-- EXAM:{key}:START -->\n{content.strip()}\n<!-- EXAM:{key}:END -->'
 def replace_existing(key,content):
  nonlocal text
  pattern=r'<!-- EXAM:'+re.escape(key)+r':START -->[\s\S]*?<!-- EXAM:'+re.escape(key)+r':END -->'
  if re.search(pattern,text):
   text=re.sub(pattern,lambda m:marked(key,content),text,count=1);return True
  return False
 # Keep the overview on its own opening page, ahead of the teaching introduction.
 text=re.sub(r'<!-- EXAM:overview:START -->[\s\S]*?<!-- EXAM:overview:END -->\n\n','',text)
 if not replace_existing('overview','\n'.join(intro)):
  pos=text.index('<a id="_2">')
  text=text[:pos]+marked('overview','\n'.join(intro))+'\n\n'+text[pos:]
 for anchor,content in notice.items():
  if replace_existing('focus-'+anchor,content):continue
  pat=r'(<a id="'+re.escape(anchor)+r'"></a>\s*#{2,3}[^\n]*\n)'
  text,n=re.subn(pat,lambda m:m.group(1)+'\n'+marked('focus-'+anchor,content)+'\n',text,count=1)
  assert n==1,anchor
 if not replace_existing('topics','\n'.join(end)):
  pos=text.index('<a id="23">')
  text=text[:pos]+marked('topics','\n'.join(end))+'\n\n'+text[pos:]
 appendix=['# Exam appendix · Lecture 2历史题源索引','', '**本轮仅完成Lecture 2映射。** 本附录按试卷排列，位于全部Assignment之后。题目册与答案册在本地单独维护；这里公开考点、出处及核查说明，不收录完整试卷或同学作答。','','[回到Lecture 2复习表](Lecture02.md#exam-review) · [按考点查题号](Lecture02.md#exam-topic-index) · [可复算台账](exam-evidence/Lecture02.json)','','同一考点的次数按独立试卷计算。2021B*按题中指定的答案文件与配套答案登记，题纸封面写2020这一冲突保留；未知年份不猜填。','']
 for p in d['papers']:
  appendix += ['<div class="exam-paper" markdown="1">',f'<a id="paper-{p["id"].lower()}"></a>',f'## {p["label"]}','',p['description'],'','| 原题号／页 | 对应考点 | 直接或关联 | 本地题集号 |','|---|---|---|---|']
  rows=sorted([(q,o) for q in d['questions'] for o in q['occurrences'] if o['paper']==p['id']],key=question_order)
  for q,o in rows:
   flag={'direct':'直接（样题不计真题次数）' if p['kind']=='sample' else '直接','related':'关联选做','fragment':'残题；条件未齐'}[o['relation']]
   appendix += [f"| {o['question']}／p.{o['pages']} | {q['summary']} | {flag} | {q['id']} |"]
  appendix += ['','**题源与答案：**','']
  for sid in dict.fromkeys(p['source_ids'][:1]+p['answer_source_ids'][:1]):
   s=sources[sid];role='随卷答案/配套答案' if sid in p['answer_source_ids'] else '题面'
   appendix += [f"- {s['label']}（{role}；{sid}）。"]
  appendix+=['','全部同卷版本及哈希见台账：'+ '、'.join(dict.fromkeys(p['source_ids']+p['answer_source_ids']))+'。']
  appendix+=['','**答案核查：** '+'；'.join(dict.fromkeys(q['answer_basis'] for q,o in rows))+'。','']
  if p['id']=='M25A':appendix+=['2025A手写作答不作为标准答案；两道同题与2023A随卷解答对照后重新核对。','']
  appendix+=['</div>','']
 return {lesson:text,ROOT/'CS5489/course-notes/ExamIndex.md':'\n'.join(appendix).rstrip()+'\n',ROOT/'CS5489/course-notes/exam-evidence/counts.json':json.dumps(counts,ensure_ascii=False,indent=2)+'\n'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
 for path,text in build().items():
  if args.check:assert path.read_text()==text,('Regenerate exam annotations',path.relative_to(ROOT))
  else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
 print('Exam annotations match the deduplicated paper ledger.' if args.check else 'Generated Lecture 2 exam annotations and final appendix.')
