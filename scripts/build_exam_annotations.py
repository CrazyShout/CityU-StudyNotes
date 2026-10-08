"""Generate lecture exam notes and the course index from shared paper identities.

The ledger contains metadata and topic summaries only. Full questions/answers stay local.
"""
from pathlib import Path
import argparse,json,re
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/'CS5489/course-notes/exam-evidence/Lecture02.json'

def build_lecture2():
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
 labels={'generative':'反复考查：先分清三个概率','decision':'反复考查：先验与最优性的条件','nb':'反复考查：能完整写出模型','mle':'学习思想有直接题；推导也是基础','boundary':'反复比较：共享方差是否成立','covariance':'基础与后续聚类迁移都要懂','smoothing':'能解释零概率与如何调节','text':'结合设备条件提出具体改进','limits':'用假设与反例判断模型局限','parameter-posterior':'QE延伸；补齐题面后再练完整推导'}
 inventory_counts={k:sum(p['countable'] and p['kind']==k for p in papers.values()) for k in ['midterm','final']}
 def paper_order(pid):
  p=papers[pid];return ({'midterm':0,'final':1,'sample':2,'qe':3}[p['kind']],p['year'] or 9999,p['term'] or '',pid)
 def question_order(pair):
  n=re.search(r'\d+',pair[1]['question']);return int(n.group()) if n else 999
 intro=['<div class="exam-overview" markdown="1">','<a id="exam-review"></a>','## Exam focus｜这一讲怎样安排复习','','先把生成式模型、Bayes决策和Gaussian NB讲清楚，再练分布假设、边界与模型局限。下面的卷数用于安排练习顺序；它描述手头历史材料，不预测本学期考题。','','| 考点 | 本轮复习重点 | 期中 | 期末：直接／关联 | QE记录 | 学习入口 |','|---|---|---|---|---|---|']
 for t in d['topics']:
  c=counts[t['id']]
  entry=f"[讲解](#{t['anchor']})" if t['id']!='parameter-posterior' else '[相关MLE基础](#prior-mle) · [QE残题说明](#qe-parameter-posterior-note)'
  intro.append(f"| {t['title']} | {labels[t['id']]} | {num(c['midterm'])} | {num(c['final_direct'])}／{num(c['final_related'])} | {qetext(t['id'])} | {entry} |")
 intro += ['',f'**统计口径：** 已辨识{inventory_counts["midterm"]}套期中、{inventory_counts["final"]}套期末；同一考点同卷只计一次。同卷答案、扫描件和压缩包副本不另计；模拟题另列，2021B*保留封面年份冲突说明。“未见”只表示现有材料未找到对应题。QE年份未载、原卷身份不完整，显示卷次待定。','','**标记：** <span class="exam-mark"><span class="exam-wave wave-mid"></span>绿色＝期中</span>　<span class="exam-mark"><span class="exam-wave wave-final"></span>黄色＝期末</span>　<span class="exam-mark"><span class="exam-wave wave-qe"></span>红色＝QE</span>。多类证据分层画线，文字同时说明类别；黑白打印看文字即可。','','题号与出处见[讲末考点索引](#exam-topic-index)；按试卷查阅见[全册附录](ExamIndex.md)。期末聚类是关联选做；QE参数后验不等于本讲的类别后验。']
 intro+=['</div>']
 end=['<a id="exam-topic-index"></a>','## Historical exam map｜按考点查题源','','各行保留原题号与原材料页码。同一卷在本表不同考点下出现，不会让该考点的卷数重复增加。材料文件、配套答案与版本差异见[按卷附录](ExamIndex.md)。','']
 for t in d['topics']:
  end += ['<div class="exam-topic-unit" markdown="1">',*(['<a id="qe-parameter-posterior-note"></a>'] if t['id']=='parameter-posterior' else []),f"### {t['title']}",'',t['skill']+'。','', '| 考试类型与学期 | 原题号 | 原材料页 | 要求 |','|---|---|---|---|']
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
 # A moved topic must leave no obsolete focus block at its former location.
 text=re.sub(r'<!-- EXAM:focus-([^:\n]+):START -->[\s\S]*?<!-- EXAM:focus-\1:END -->',lambda m:m.group(0) if m.group(1) in notice else '',text)
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


def marked(key, content):
 return f'<!-- EXAM:{key}:START -->\n{content.strip()}\n<!-- EXAM:{key}:END -->'

def replace_block(text, key, content, insert_at):
 pattern=r'<!-- EXAM:'+re.escape(key)+r':START -->[\s\S]*?<!-- EXAM:'+re.escape(key)+r':END -->'
 block=marked(key,content)
 if re.search(pattern,text):return re.sub(pattern,lambda m:block,text,count=1)
 pos=insert_at(text)
 return text[:pos]+block+'\n\n'+text[pos:]

def aggregate_counts(data,papers):
 counts={}
 for topic in data['topics']:
  rows=[o for q in data['questions'] if topic['id'] in q['topics'] for o in q['occurrences']]
  result={}
  for kind in ['midterm','final']:
   for relation in ['direct','related']:
    result[f'{kind}_{relation}']=sorted({o['paper'] for o in rows if papers[o['paper']]['countable'] and papers[o['paper']]['kind']==kind and o['relation']==relation})
  result['qe_fragments']=sorted({o['paper'] for o in rows if papers[o['paper']]['kind']=='qe'})
  result['samples']=sorted({o['paper'] for o in rows if papers[o['paper']]['kind']=='sample'})
  counts[topic['id']]=result
 return counts

def generate_lecture(n,data,papers):
 path=ROOT/f'CS5489/course-notes/Lecture{n:02}.md';text=path.read_text()
 topics={t['id']:t for t in data['topics']}
 assert len(topics)==len(data['topics'])
 assert len({q['id'] for q in data['questions']})==len(data['questions'])
 for q in data['questions']:
  assert set(q['topics'])<=topics.keys()
  for o in q['occurrences']:
   assert o['paper'] in papers and o['relation'] in {'direct','related','fragment'}
   assert o['source_id'] in papers[o['paper']]['source_ids']
 counts=aggregate_counts(data,papers)
 def num(items):return f'{len(items)}套' if items else '未见'
 overview=['<div class="exam-overview exam-overview-compact" markdown="1">','<a id="exam-review"></a>',
  '## Exam focus｜这一讲怎样安排复习','',data['intro'],'',
  '| 考点 | 复习动作 | 期中：直接／关联 | 期末：直接／关联 | QE记录 | 入口 |',
  '|---|---|---|---|---|---|']
 for t in data['topics']:
  c=counts[t['id']];qe='关联题段；卷次待定' if c['qe_fragments'] else '未见'
  overview.append(f"| {t['title']} | {t['priority']} | {num(c['midterm_direct'])}／{num(c['midterm_related'])} | {num(c['final_direct'])}／{num(c['final_related'])} | {qe} | [讲解](#{t['anchor']}) |")
 overview += ['', '**口径：** 同一考点在同一独立试卷只计一次；题纸、答案和扫描副本不重复计。已辨识6套期中、3套期末；模拟题另列，2021B*保留封面年份冲突。同卷可同时有直接题和关联题，两列不相加。未见不等于不考，QE题段不换算为已确认卷数。', '',data['boundaries'],'',
  '绿色波浪＝期中，黄色＝期末，红色＝QE；文字同时标明类别，黑白打印可直接读。题号见[讲末索引](#exam-topic-index)，材料身份见[全册附录](ExamIndex.md)。','</div>']
 text=replace_block(text,'overview','\n'.join(overview),lambda s:s.index('[TOC]') if '[TOC]' in s else s.index('| 主题 |'))
 for t in data['topics']:
  c=counts[t['id']];classes=[];phrases=[]
  for kind,label,cls in [('midterm','期中','mid'),('final','期末','final')]:
   for relation,suffix in [('direct','直接'),('related','关联')]:
    ids=c[f'{kind}_{relation}']
    if ids:classes.append(cls);phrases.append(f'{label}{suffix}：{len(ids)}套')
  if c['qe_fragments']:classes.append('qe');phrases.append('QE关联题段，年份未载／卷次待定')
  if not classes:continue
  waves=''.join(f'<span class="exam-wave wave-{v}"></span>' for v in dict.fromkeys(classes))
  notice=f'<p class="exam-focus"><span class="exam-mark">{waves}考点：{t["title"]}</span><br>'+ '；'.join(phrases)+'。</p>'
  def position(s,anchor=t['anchor']):
   match=re.search(r'<a id="'+re.escape(anchor)+r'"></a>\s*(?:<a [^>]+></a>\s*)?#{2,3}[^\n]*\n',s)
   assert match,anchor
   return match.end()
  text=replace_block(text,'focus-'+t['anchor'],notice,position)
 end=['<a id="exam-topic-index"></a>','## Historical exam map｜按考点查题源','',
  '题号和页码指向原题纸；多题出现只增加定位，不重复增加同一卷的次数。需要整题作答时，请按题号回查原卷；当前独立题答册只整理Lecture 2。','']
 for t in data['topics']:
  end += ['<div class="exam-topic-unit" markdown="1">',f"### {t['title']}",'',t['skill']+'。','',
          '| 试卷 | 原题号／页码 | 关系与要求 |','|---|---|---|']
  found=False
  for q in data['questions']:
   if t['id'] not in q['topics']:continue
   for o in q['occurrences']:
    found=True;p=papers[o['paper']];rel={'direct':'直接','related':'关联','fragment':'残题'}[o['relation']]
    if p['kind']=='sample':rel+='（样题）'
    end.append(f"| {p['label']} | {o['question']}／{o['pages']} | {rel}：{q['summary']} |")
  if not found:end.append('| 现有材料未见 | — | 本讲仍按当前课件与配套任务学习 |')
  notes=list(dict.fromkeys(q['review_note'] for q in data['questions'] if t['id'] in q['topics'] and q.get('review_note')))
  if notes:end+=['','**题源条件：** '+'；'.join(notes)+'。']
  end+=['</div>','']
 def before_sources(s):
  match=re.search(r'^## (?:\d+\. )?(?:原材料覆盖索引|来源覆盖索引|原课疑点与覆盖索引|Source coverage[^\n]*)',s,re.M)
  assert match,path
  return match.start()
 text=replace_block(text,'topics','\n'.join(end),before_sources)
 return {path:text,LEDGER.parent/f'counts-Lecture{n:02}.json':json.dumps(counts,ensure_ascii=False,indent=2)+'\n'}

def combined_appendix(all_data,catalogue):
 papers=catalogue['papers'];sources={s['id']:s for s in catalogue['sources']}
 lines=['<a id="exam-appendix-lecture-2"></a>','# Exam appendix · Lecture 1–5历史题源索引','',
 '**映射范围：当前Lecture 1–5。** 本附录按独立试卷整理本轮已核对的对应题目，放在Assignment之后。CNN、PCA、聚类等后续主题仅在与当前基础有直接联系时列为关联，不表示完整教学已覆盖。','',
 '题目册与答案册目前只单独维护Lecture 2。下面公开考点、题号和材料身份，不附完整原卷或同学作答。','',
 ' · '.join(f'[Lecture {n}复习表](Lecture{n:02}.md#exam-review)' for n in sorted(all_data)),'',
 '按独立试卷计数，样题另列。2021B*题纸封面写2020，但题内答案文件名及配套解答指向2021B，保留此冲突。QE年份和独立原卷身份待补，片段数量不当作考试次数。','']
 for p in papers:
  lines+=['<div class="exam-paper" markdown="1">',f'<a id="paper-{p["id"].lower()}"></a>',f'## {p["label"]}','']
  description=p['description']
  if p['kind']=='final':description=f'题纸共'+{'F20B':'4','F21A':'4','F21B':'5'}[p['id']]+'页；本表汇总与Lecture1–5有关的部分，其余题不计入当前讲义覆盖。'
  if p['kind']=='qe':description='使用者提供的CS5489 QE整理片段，夹有同学笔记；仅按印刷题面映射。年份与独立卷身份未载，参数后验残题还缺前页模型和先验。'
  lines += [description,'','| Lecture | 原题号／原页 | 考查内容 | 关系 |','|---|---|---|---|']
  rows=[]
  for n,data in all_data.items():
   for q in data['questions']:
    for o in q['occurrences']:
     if o['paper']==p['id']:rows.append((n,q,o))
  for n,q,o in rows:
   flag={'direct':'直接','related':'关联','fragment':'残题'}[o['relation']]
   if p['kind']=='sample':flag+='（样题）'
   lines.append(f"| [L{n}](Lecture{n:02}.md#exam-topic-index) | {o['question']}／{o['pages']} | {q['summary']} | {flag} |")
  lines+=['','**题源与答案：**']
  for sid in dict.fromkeys(p['source_ids'][:1]+p['answer_source_ids'][:1]):
   src=sources[sid];role='题面及配套／随卷答案' if sid in p['answer_source_ids'] and sid in p['source_ids'] else '配套答案' if sid in p['answer_source_ids'] else '题面'
   lines += [f'- {src["label"]}（{role}；{sid}）。']
  lines+=['','全部版本及SHA-256见[共享材料台账](exam-evidence/Lecture02.json)：'+'、'.join(dict.fromkeys(p['source_ids']+p['answer_source_ids']))+'。']
  notes=list(dict.fromkeys(q.get('review_note','') for n,q,o in rows if q.get('review_note')))
  if p['id']=='M25A':notes.insert(0,'扫描手写作答不作为标准答案；本轮只记录印刷题面要求')
  if notes:lines+=['','**核对说明：** '+'；'.join(notes)+'。']
  if p['id']=='QE-U':lines+=['','Apple、Bottles、CWD用来区分题段主题，不是已确认的三套独立卷。CNN架构、增强和压缩部分留待后续课件，未登记为当前已讲。']
  lines+=['</div>','']
 return '\n'.join(lines).rstrip()+'\n'

def build():
 output=build_lecture2()
 catalogue=json.loads(LEDGER.read_text());papers={p['id']:p for p in catalogue['papers']}
 data={2:catalogue}
 for n in [1,3,4,5]:
  path=LEDGER.parent/f'Lecture{n:02}.json'
  if not path.exists():continue
  d=json.loads(path.read_text());assert d['catalogue']=='Lecture02.json'
  data[n]=d;output.update(generate_lecture(n,d,papers))
 if len(data)>1:output[ROOT/'CS5489/course-notes/ExamIndex.md']=combined_appendix(dict(sorted(data.items())),catalogue)
 return output

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
 for path,text in build().items():
  if args.check:assert path.read_text()==text,('Regenerate exam annotations',path.relative_to(ROOT))
  else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
 print('Exam annotations match the deduplicated paper ledger.' if args.check else 'Generated Lecture 1–5 annotations and final appendix.')
