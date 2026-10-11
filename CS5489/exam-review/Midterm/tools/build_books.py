"""Generate offline A4 intermediates from the editable Markdown, without modifying prose."""
from pathlib import Path
import argparse,json,re,os
import markdown
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]
p=argparse.ArgumentParser();p.add_argument('--notes-root',type=Path,default=REPO);args=p.parse_args()
assert (args.notes_root/'vendor/katex/katex.min.js').is_file(), 'Missing vendor/katex in notes repository'
build=ROOT/'.build';build.mkdir(exist_ok=True)
index=json.loads((ROOT/'QuestionIndex.json').read_text())
page_maps=json.loads((ROOT/'PageIndex.json').read_text()) if (ROOT/'PageIndex.json').exists() else {}
css='''@page{size:A4;margin:19mm 18mm 18mm 20mm}*{box-sizing:border-box}
body{font-family:"PingFang SC","Noto Sans CJK SC",Arial,sans-serif;color:#111;font-size:11pt;line-height:1.58;margin:0}
h1{font-size:22pt;line-height:1.4;margin:0 0 7mm}
h2{font-size:14pt;line-height:1.35;break-before:page;break-after:avoid;margin:0 0 4mm;border-bottom:.6pt solid #aaa;padding-bottom:2.5mm}
h3{font-size:11.5pt;margin:4mm 0 2mm;break-after:avoid}
p{margin:0 0 3mm;orphans:3;widows:3}li{margin:1.4mm 0}a{color:#111;text-decoration:none}
img{display:block;max-width:140mm;max-height:72mm;width:auto;height:auto;object-fit:contain;margin:3mm auto}
figure{margin:3mm 0;break-inside:avoid}figcaption{font-size:9pt;line-height:1.4}
ul,ol{padding-left:6mm}.toc{font-size:9.5pt;line-height:1.4;columns:2;column-gap:8mm}
.toc h2{column-span:all}.toc p{break-after:avoid;margin:3mm 0 1mm}.toc li{margin:.5mm 0}
.katex{font-size:1.02em}.katex-display{margin:3.5mm 0;break-inside:avoid}.arithmatex{overflow:visible}
.katex-display>.katex{white-space:nowrap}.exam-source{font-size:9pt;color:#444}
.notes-space{border-top:.3pt solid #ccc;padding-top:2mm;margin-top:5mm;font-size:9pt;color:#555}
.equation-lead{break-after:avoid}.topic{font-size:9.5pt;color:#333}
table{border-collapse:collapse;width:100%;font-size:9pt}td,th{padding:1.5mm;border-bottom:.4pt solid #aaa}
tr{break-inside:avoid}.crosslinks{font-size:9pt}
.source-discrepancy{font-size:9.5pt;line-height:1.45;color:#444;border-top:.3pt solid #ddd;padding-top:2mm;break-inside:avoid}
.page-ref{font-size:9pt;color:#444;white-space:nowrap}
.optional-reading{border-left:1pt solid #bbb;padding-left:3mm}
.equation-number{display:block;text-align:right;font-size:8.5pt;color:#555;margin-top:-1mm}
thead{display:table-header-group}td,th{vertical-align:top}strong{font-weight:600}
.references{font-size:8.5pt;line-height:1.32;color:#444;margin-top:2mm;break-inside:avoid}
.references p{font-size:inherit;line-height:inherit;margin:0 0 1mm;orphans:1;widows:1}
.references .page-ref{font-size:8.5pt}.answers p{margin-bottom:2.5mm}
.answers li{break-inside:avoid}
.answers img[src$="answer-kernel-map.png"],.answers img[src$="answer-asymmetric-loss.png"],.answers img[src$="answer-huber.png"]{max-height:54mm;max-width:115mm}
.answers img[src$="answer-l1-l2-geometry.png"]{max-height:70mm;max-width:155mm}
.answers div.arithmatex{break-inside:avoid;position:relative}
'''
for kind in ['Questions','Answers']:
    source=ROOT/f'{kind}.md'
    soup=BeautifulSoup(markdown.markdown(source.read_text(),extensions=['tables','toc','md_in_html','fenced_code','pymdownx.arithmatex'],extension_configs={'pymdownx.arithmatex':{'generic':True}}),'html.parser')
    for h in soup.select('h2'):
        prev=h.find_previous_sibling()
        if prev and prev.name=='p' and (a:=prev.find('a',id=re.compile('^mt\\d{3}$'))):
            h['id']=a['id'];prev.decompose()
    for im in list(soup.select('img')):
        im['src']=Path(os.path.relpath((source.parent/im['src']).resolve(),build)).as_posix()
        parent=im.parent;f=soup.new_tag('figure');im.extract();f.append(im);parent.insert_before(f)
        if not parent.get_text(strip=True):parent.decompose()
        if im['src'].endswith('answer-l1-l2-geometry.png'):
            lead=f.find_previous_sibling()
            if lead and lead.name=='p':lead['style']='break-after:avoid'
        nxt=f.find_next_sibling()
        if nxt and nxt.name=='p' and nxt.find('em'):nxt.name='figcaption';f.append(nxt.extract())
    for a in list(soup.select('a[href]')):
        href=a['href'];target_kind=kind;key=None
        if href.startswith(('Questions.md#','Answers.md#')):
            target_kind=href.split('.md#')[0];key=href.split('#')[1]
        elif re.fullmatch(r'#mt\d{3}',href):key=href[1:]
        if key and key in page_maps.get(target_kind,{}):
            ref=soup.new_tag('span',attrs={'class':'page-ref'})
            label='本册' if target_kind==kind else ('题目册' if target_kind=='Questions' else '答案册')
            ref.string=f'（{label}第{page_maps[target_kind][key]}页）'
            a.insert_after(ref)
        if href.startswith(('Questions.md#','Answers.md#')):a['href']=href.replace('.md#','.pdf#')
        elif '.md' in a['href']:a.replace_with(a.get_text()+'（见同目录文件）')
    for para in soup.find_all('p'):
        if para.get_text().startswith('出处：'):para['class']='exam-source'
        if para.get_text().startswith('考点：'):para['class']='topic'
        if para.get_text().startswith('原题差异 / Source note：'):para['class']='source-discrepancy'
        if para.get_text().startswith('题目（') or para.get_text().strip()=='题目 · 答案':para['class']='crosslinks'
        if para.get_text().startswith('选读：'):para['class']='optional-reading'
    if kind=='Answers':
        for para in list(soup.find_all('p')):
            if not para.get_text().startswith('出处：'):continue
            refs=soup.new_tag('div',attrs={'class':'references'});para.insert_before(refs)
            refs.append(para.extract())
            while (nxt:=refs.find_next_sibling()) and nxt.name=='p' and (nxt.get_text().startswith('答案依据：') or 'crosslinks' in nxt.get('class',[])):
                refs.append(nxt.extract())
            before=refs.find_previous_sibling()
            if before and before.name in ('p','ul','ol'):
                before['style']='break-after:avoid'
                # Keep a short closing sentence with its preceding explanation,
                # rather than leaving only that sentence and sources on a page.
                if before.name=='p' and len(before.get_text())<60:
                    previous=before.find_previous_sibling()
                    if previous and previous.name in ('p','ul','ol'):
                        previous['style']='break-after:avoid'
    for eq in soup.select('div.arithmatex'):
        before=eq.find_previous_sibling()
        if before and before.name=='p' and len(before.get_text())<180:before['class']=list(before.get('class',[]))+['equation-lead']
    if kind=='Answers':
        eq_counts={}
        for eq in soup.select('div.arithmatex'):
            heading=eq.find_previous('h2');qid=heading.get('id','') if heading else ''
            if not re.fullmatch(r'mt\d{3}',qid):continue
            eq_counts[qid]=eq_counts.get(qid,0)+1
            label=soup.new_tag('span',attrs={'class':'equation-number'})
            label.string=f'({qid.upper()}.{eq_counts[qid]})';eq.append(label)
    toc=next(h for h in soup.find_all('h2') if h.get_text()=='目录');toc['id']='contents';toc['style']='break-before:avoid'
    wrap=soup.new_tag('div',attrs={'class':'toc'});toc.insert_before(wrap);wrap.append(toc.extract())
    while (nxt:=wrap.find_next_sibling()) and nxt.name!='h2':wrap.append(nxt.extract())
    if kind=='Questions':
        for h in soup.find_all('h2'):
            if not re.fullmatch(r'mt\d{3}',h.get('id','')):continue
            last=h
            while last.find_next_sibling() and last.find_next_sibling().name!='h2':last=last.find_next_sibling()
            space=soup.new_tag('p',attrs={'class':'notes-space'});space.string='作答与草稿 / Your answer and working';last.insert_after(space)
    vendor=(args.notes_root/'vendor/katex').resolve().as_uri()
    js=r'''renderMathInElement(document.body,{delimiters:[{left:"\\[",right:"\\]",display:true},{left:"\\(",right:"\\)",display:false}],throwOnError:false});document.fonts.ready.then(()=>{window.printReady=true;});'''
    (build/f'{kind}.html').write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>CS5489 Midterm {kind}</title><link rel="stylesheet" href="{vendor}/katex.min.css"><style>{css}</style></head><body class="{kind.lower()}">{soup}<script src="{vendor}/katex.min.js"></script><script src="{vendor}/contrib/auto-render.min.js"></script><script>{js}</script></body></html>')
print('Built both offline A4 intermediates from Markdown.')
