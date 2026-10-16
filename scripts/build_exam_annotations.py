"""Generate native TeX exam annotations and deduplicated counts from the public ledger."""
from pathlib import Path
import argparse
import json
import re
from latex_support import ROOT, escape

LEDGER=ROOT/'CS5489/course-notes/exam-evidence'
TEMPLATES=ROOT/'latex/exam'
ANCHORS=json.loads((TEMPLATES/'anchors.json').read_text())


def aggregate_counts(data,papers):
    result={}
    for t in data['topics']:
        rows=[o for q in data['questions'] if t['id'] in q['topics'] for o in q['occurrences']]
        c={f'{kind}_{rel}':sorted({o['paper'] for o in rows if papers[o['paper']]['countable'] and papers[o['paper']]['kind']==kind and o['relation']==rel}) for kind in ['midterm','final'] for rel in ['direct','related']}
        c.update({key:sorted({o['paper'] for o in rows if papers[o['paper']]['kind']==kind}) for key,kind in [('qe_fragments','qe'),('samples','sample')]})
        result[t['id']]=c
    return result


def ref(n,anchor,label):
    return r'\StudyRef{CS5489-Lecture'+f'{n:02}'+'}{'+anchor+'}{'+label+'}'


def table(headers,rows,weights=None):
    n=len(headers);weights=weights or [1/n]*n
    spec=''.join(r'>{\raggedright\arraybackslash}p{\dimexpr'+str(w)+r'\linewidth-'+str(2*(n-1)/n)+r'\tabcolsep\relax}' for w in weights)
    row=lambda cells:' & '.join(cells)+r' \\'
    return '\n'.join([r'\begingroup\small\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.22}',r'\begin{longtable}{@{}'+spec+'@{}}',r'\toprule',row(headers),r'\midrule\endfirsthead',row(headers),r'\midrule\endhead',r'\bottomrule\endfoot',*[row(x) for x in rows],r'\end{longtable}\endgroup'])


def targets(names):return '\n'.join(r'\StudyTarget{'+a+'}' for a in names)


def compact_review_notes(notes, known, replacement):
    """Condense reviewed clauses while retaining any later ledger additions."""
    if not known <= set(notes):
        return notes
    return replacement + [note for note in notes if note not in known]


def build():
    catalog=json.loads((LEDGER/'Lecture02.json').read_text());papers={p['id']:p for p in catalog['papers']};sources={s['id']:s for s in catalog['sources']}
    data={n:json.loads((LEDGER/f'Lecture{n:02}.json').read_text()) for n in range(1,6)}
    output={}
    for n,d in data.items():
        topic_ids={t['id'] for t in d['topics']}
        assert len(topic_ids)==len(d['topics'])
        assert len({q['id'] for q in d['questions']})==len(d['questions'])
        for q in d['questions']:
            assert set(q['topics'])<=topic_ids
            assert all(o['paper'] in papers and o['relation'] in ['direct','related','fragment'] for o in q['occurrences'])
        counts=aggregate_counts(d,papers)
        saved={t:{'midterm':v['midterm_direct'],**{k:x for k,x in v.items() if k not in ['midterm_direct','midterm_related']}} for t,v in counts.items()} if n==2 else counts
        output[LEDGER/('counts.json' if n==2 else f'counts-Lecture{n:02}.json')]=json.dumps(saved,ensure_ascii=False,indent=2)+'\n'
        num=lambda seq:str(len(seq))+'套' if seq else '未见'
        # The Lecture 2 review actions are authored TeX; all counts come from the ledger.
        priorities=['反复考查：先分清三个概率','反复考查：先验与最优性的条件','反复考查：能完整写出模型','学习思想有直接题；推导也是基础','反复比较：共享方差是否成立','基础与后续聚类迁移都要懂','能解释零概率与如何调节','结合设备条件提出具体改进','用假设与反例判断模型局限','QE延伸；补齐题面后再练完整推导']
        overview=[];notices={};topic_parts=[]
        for i,t in enumerate(d['topics']):
            c=counts[t['id']]
            entry=ref(n,t['anchor'],'讲解') if t['id']!='parameter-posterior' else ref(n,'prior-mle','相关MLE基础')+' · '+ref(n,'qe-parameter-posterior-note','QE残题说明')
            overview.append([escape(t['title']),escape(priorities[i] if n==2 else t['priority']),num(c['midterm_direct']) if n==2 else num(c['midterm_direct'])+'／'+num(c['midterm_related']),num(c['final_direct'])+'／'+num(c['final_related']),('题段；卷次待定' if n==2 else '关联题段；卷次待定') if c['qe_fragments'] else ('现有材料未见' if n==2 else '未见'),entry])
            badges=[]
            for kind,label,style in [('midterm','期中','mid'),('final','期末','final')]:
                for relation,suffix in [('direct','直接'),('related','关联')]:
                    seq=c[kind+'_'+relation]
                    if seq:badges.append(r'\StudyBadge{'+style+'}{'+label+('' if n==2 and kind=='midterm' else suffix)+' · '+str(len(seq))+' 套}')
            if c['qe_fragments']:badges.append(r'\StudyBadge{qe}{'+('QE题段' if n==2 else 'QE关联题段')+' · 年份未载／卷次待定}')
            if badges and t['id']!='parameter-posterior':
                notices['focus-'+t['anchor']]='考点：'+escape(t['title'])+'\n'+' '.join(badges)+'\n'+('QE另问参数后验和MAP，不能当作类别决策题。\n' if n==2 and t['id']=='mle' else '')
            heading=r'\StudyHeading{2}{'+escape(t['title'])+'}'
            topic_parts += [heading,targets(ANCHORS[str(n)]['topic_titles'].get(heading,[])),escape(t['skill'])+'。']
            pairs=[(q,o) for q in d['questions'] if t['id'] in q['topics'] for o in q['occurrences']]
            if n==2:
                grouped={}
                for q,o in pairs:grouped.setdefault((o['paper'],o['relation']),[]).append((q,o))
                rows=[]
                for pid,relation in sorted(grouped,key=lambda k:({'midterm':0,'final':1,'sample':2,'qe':3}[papers[k[0]]['kind']],papers[k[0]]['year'] or 9999,papers[k[0]]['term'] or '',k[0])):
                    ps=sorted(grouped[pid,relation],key=lambda v:int(re.search(r'\d+',v[1]['question'])[0]) if re.search(r'\d+',v[1]['question']) else 999)
                    flag='关联选做' if relation=='related' else '残题' if relation=='fragment' else '模拟' if papers[pid]['kind']=='sample' else '直接'
                    rows.append([escape(papers[pid]['label']+' · '+flag),escape('、'.join(o['question'] for q,o in ps)),escape('、'.join(dict.fromkeys(o['pages'] for q,o in ps))),escape('、'.join(dict.fromkeys(q['skill'] for q,o in ps)))])
                topic_parts += [table(['考试类型与学期','原题号','原材料页','要求'],rows,[.25,.13,.13,.49])]
                if t['id']=='parameter-posterior':topic_parts+=['此题问的是参数后验与MAP，缺少前页模型和先验。当前只能核对通用步骤，不能据此登记某一分布的完整MLE推导已考过。']
            else:
                rows=[]
                for q,o in pairs:
                    p=papers[o['paper']];flag={'direct':'直接','related':'关联','fragment':'残题'}[o['relation']]+('（样题）' if p['kind']=='sample' else '')
                    rows.append([escape(p['label']),escape(o['question']+'／'+o['pages']),escape(flag+'：'+q['summary'])])
                if not rows:rows=[['现有材料未见','—','本讲仍按当前课件与配套任务学习']]
                topic_parts += [table(['试卷','原题号／页码','关系与要求'],rows,[.22,.22,.56])]
                # A ledger note may contain several clauses repeated by other questions.
                notes=list(dict.fromkeys(clause.strip().rstrip('。') for q in d['questions']
                    if t['id'] in q['topics'] and q.get('review_note')
                    for clause in q['review_note'].split('；') if clause.strip().rstrip('。')))
                if n==1 and t['id']=='diagnosis':
                    notes=compact_review_notes(notes, {
                        '完整处理还需Lecture5的优化与早停', 'CNN结构不在当前Lecture1–5范围',
                        '缺年份与独立原卷身份', 'CNN设计另需后续课', '缺年份',
                        '不把片段数量计为卷数', '只映射一般诊断能力'}, [
                        '完整处理还需Lecture5的优化与早停',
                        '当前只映射通用训练/验证诊断，CNN结构设计属于后续内容',
                        'QE题段缺年份与独立原卷身份，不按片段数计卷数'])
                if notes:topic_parts+=[r'\textbf{题源条件：}'+escape('；'.join(notes)+'。')]
        headers=['考点','复习重点' if n==2 else '复习动作','期中' if n==2 else '期中：直接／关联','期末：直接／关联','QE记录','学习入口' if n==2 else '入口']
        notices['overview']=(TEMPLATES/f'Lecture{n:02}-overview.tex.in').read_text().replace('@@OVERVIEW_TABLE@@',table(headers,overview,[.17,.23,.13,.15,.16,.16]))
        notices['topics']=(TEMPLATES/f'Lecture{n:02}-topics.tex.in').read_text().replace('@@TOPICS@@','\n\n'.join(topic_parts))
        path=ROOT/f'CS5489/course-notes/Lecture{n:02}.tex';text=path.read_text()
        def replace(m):
            key=m[1]
            if key not in notices:return ''
            return '% EXAM:'+key+':START\n'+notices[key].strip()+'\n% EXAM:'+key+':END'
        text=re.sub(r'% EXAM:([^:\n]+):START(.*?)% EXAM:\1:END',replace,text,flags=re.S)
        # New topics with evidence must be inserted next to their declared teaching anchor.
        for key,body in notices.items():
            if '% EXAM:'+key+':START' in text:continue
            assert key.startswith('focus-'),key
            needle=r'\StudyTarget{CS5489-Lecture'+f'{n:02}'+'__'+key[6:]+'}'
            assert needle in text,(n,key)
            text=text.replace(needle,needle+'\n% EXAM:'+key+':START\n'+body.strip()+'\n% EXAM:'+key+':END',1)
        output[path]=text
    parts=[]
    for p in catalog['papers']:
        heading=r'\StudyHeading{1}{'+escape(p['label'])+'}'
        parts += [heading,targets(ANCHORS['appendix'].get(heading,[]))]
        description=p['description']
        if p['kind']=='final':description='题纸共'+{'F20B':'4','F21A':'4','F21B':'5'}[p['id']]+'页；本表汇总与Lecture1–5有关的部分，其余题不计入当前讲义覆盖。'
        if p['kind']=='qe':description='使用者提供的CS5489 QE整理片段，夹有同学笔记；仅按印刷题面映射。年份与独立卷身份未载，参数后验残题还缺前页模型和先验。'
        parts.append(escape(description));rows=[];pairs=[]
        for n,d in data.items():
            for q in d['questions']:
                for o in q['occurrences']:
                    if o['paper']!=p['id']:continue
                    pairs.append((n,q,o));flag={'direct':'直接','related':'关联','fragment':'残题'}[o['relation']]+('（样题）' if p['kind']=='sample' else '')
                    rows.append([ref(n,'exam-topic-index','L'+str(n)),escape(o['question']+'／'+o['pages']),escape(q['summary']),flag])
        parts += [table(['Lecture','原题号／原页','考查内容','关系'],rows,[.14,.20,.53,.13]),r'\textbf{题源与答案：}',r'\begin{itemize}']
        for sid in dict.fromkeys(p['source_ids'][:1]+p['answer_source_ids'][:1]):
            role='题面及配套／随卷答案' if sid in p['answer_source_ids'] and sid in p['source_ids'] else '配套答案' if sid in p['answer_source_ids'] else '题面'
            parts += [r'\item '+escape(sources[sid]['label']+'（'+role+'；'+sid+'）。')]
        parts += [r'\end{itemize}',r'全部版本及SHA-256见\StudyRepoRef{CS5489/course-notes/exam-evidence/Lecture02.json}{}{共享材料台账}：'+escape('、'.join(dict.fromkeys(p['source_ids']+p['answer_source_ids']))+'。')]
        notes=list(dict.fromkeys(clause.strip().rstrip('。') for n,q,o in pairs
            if q.get('review_note') for clause in q['review_note'].split('；')
            if clause.strip().rstrip('。')))
        if p['id']=='QE-U':
            # Year, coverage and independent-paper identity are stated before/after the table.
            notes=compact_review_notes(notes, {
                '缺年份与独立原卷身份', 'CNN设计另需后续课', '缺年份',
                '不把片段数量计为卷数', '只映射一般诊断能力', 'CNN架构未在当前讲义覆盖',
                '题段年份与卷次待定', '仅映射通用训练诊断', '图与问题跨两个原页',
                '不使用扫描手写解答', '缺年份和独立原卷身份'}, [
                '部分图与问题跨两个原页，须一起读取；手写解答不作为标准答案'])
        if notes:parts += [r'\textbf{核对说明：}'+escape('；'.join(notes)+'。')]
        if p['id']=='QE-U':parts+=['Apple、Bottles、CWD用来区分题段主题，不是已确认的三套独立卷。CNN架构、增强和压缩部分留待后续课件，未登记为当前已讲。']
    output[ROOT/'CS5489/course-notes/ExamIndex.tex']=(TEMPLATES/'appendix.tex.in').read_text().replace('@@PAPERS@@','\n\n'.join(parts))
    return {path:text.rstrip()+'\n' for path,text in output.items()}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for path,text in build().items():
        if args.check:assert path.read_text()==text,('Regenerate exam annotations',path.relative_to(ROOT))
        else:path.write_text(text)
    print('Native TeX exam annotations match the deduplicated paper ledger.')
