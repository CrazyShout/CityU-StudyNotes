"""Build print HTML from the registered, already executed local notes. Never reruns notebooks."""
from pathlib import Path
from urllib.parse import urlsplit,unquote,quote
import importlib.util,json,re,html,copy
from bs4 import BeautifulSoup
from PIL import Image,ImageChops
C=Path(__file__).resolve().parents[1]; OUT=C/'.build/print';OUT.mkdir(parents=True,exist_ok=True)
REG=json.loads((C/'learning/course-notes-documents.json').read_text())['documents']
GROUPS={'CS5489':[r for r in REG if r['major'] and r['course']=='CS5489'],
        'CS5222':[r for r in REG if r['major'] and r['course']=='CS5222'],
        'Foundations':[r for r in REG if r['course'] is None]}
# Registry order is shared with local directories and public notes.
LOOKUP={}
for group,records in GROUPS.items():
 for r in records:
  src=(C/r['source']).resolve();docid=group+'-'+src.stem
  LOOKUP[src]=LOOKUP[src.with_suffix('.html')]={'group':group,'docid':docid,'source':src}
PAGE_MAP=json.loads((OUT/'page-map.json').read_text()) if (OUT/'page-map.json').exists() else {}
ANCHOR_MAP=json.loads((OUT/'anchor-map.json').read_text()) if (OUT/'anchor-map.json').exists() else {}
CSS=(C/'scripts/course_print.css').read_text()
manifest={}
for group,records in GROUPS.items():
 blocks=[];docs=[]
 for r in records:
  src=C/r['source'];preview=src.with_suffix('.html');docid=LOOKUP[src.resolve()]['docid']
  soup=BeautifulSoup(preview.read_text(),'html.parser');body=soup.main
  for x in body.select('nav,.source-note'):x.decompose()
  title=body.find('h1').get_text(' ',strip=True)
  # Preserve source headings and prefix anchors to make the combined book unambiguous.
  for e in body.select('[id]'):e['id']=docid+'__'+e['id']
  for a in body.select('a[href]'):
   u=urlsplit(a['href'])
   if u.scheme or u.netloc:continue
   dest=(preview.parent/unquote(u.path)).resolve() if u.path else preview.resolve()
   target=LOOKUP.get(dest)
   if target:
    anchor=target['docid']+('__'+unquote(u.fragment) if u.fragment else '')
    a['href']=('#' if target['group']==group else target['group']+'-A4.pdf#')+anchor
    if target['docid']!=docid or u.fragment:
     label='本册' if target['group']==group else {'CS5489':'CS5489册','CS5222':'CS5222册','Foundations':'基础册'}[target['group']]
     pagen=ANCHOR_MAP.get(anchor,PAGE_MAP.get(target['docid'],{}).get('start','000'))
     note=soup.new_tag('span',attrs={'class':'print-ref'})
     note.string=f'〔{label} p.{pagen}〕';a.insert_after(note)
   elif u.path:
    if dest.is_relative_to(C):
     a['href']='https://github.com/CrazyShout/CityU-StudyNotes/blob/main/'+quote(dest.relative_to(C).as_posix(),safe='/')+('#'+u.fragment if u.fragment else '')
    else:
     a.replace_with(a.get_text())
  for im in body.select('img[src]'):
   if not urlsplit(im['src']).scheme:im['src']=(preview.parent/unquote(im['src'])).resolve().as_uri()
   im.attrs.pop('width',None);im.attrs.pop('height',None)
  # CSS alone cannot reliably print closed details. Replace the actual element.
  for d in body.select('details'):
   d.name='div';d.attrs={'class':'answer-block'}
   summary=d.find('summary')
   if summary:summary.name='p';summary.attrs={'class':'answer-title'}
  # One figure per image; a paragraph containing 4 source pages must not become one giant keep-together box.
  for im in list(body.select('img')):
   parent=im.parent
   if parent.name=='p' and not parent.get_text(strip=True) and len(parent.find_all('img'))>=1:
    f=soup.new_tag('figure');im.extract();f.append(im);parent.insert_before(f)
    if not parent.find('img'):parent.decompose()
   elif parent.name not in ['td','th','figure']:
    f=soup.new_tag('figure');im.wrap(f)
  # Clip only blank margins of full-page question images through layout.
  # Pixels in the original file are never rewritten; all nonwhite content stays.
  for image in list(body.select('figure img')):
   image_path=Path(unquote(urlsplit(image.get('src','')).path))
   if not re.fullmatch(r'(tutorial0[12345]|assignment01)-\d+\.png',image_path.name):continue
   with Image.open(image_path) as original:
    rgb=original.convert('RGB');mask=ImageChops.difference(rgb,Image.new('RGB',rgb.size,'white')).convert('L').point(lambda value:255 if value>12 else 0)
    bbox=mask.getbbox()
    if not bbox:continue
    x0,y0,x1,y1=bbox;pad=20
    x0=max(0,x0-pad);y0=max(0,y0-pad);x1=min(rgb.width,x1+pad);y1=min(rgb.height,y1+pad)
    bw,bh=x1-x0,y1-y0;nw,nh=rgb.size
   viewport=soup.new_tag('div',attrs={'class':'source-viewport','style':f'width:min(100%,{215*bw/bh:.3f}mm);aspect-ratio:{bw}/{bh};','data-original-size':f'{nw},{nh}','data-ink-viewport':f'{x0},{y0},{x1},{y1}'})
   image.wrap(viewport)
   image['style']=f'left:{-100*x0/bw:.6f}%;top:{-100*y0/bh:.6f}%;width:{100*nw/bw:.6f}%;height:{100*nh/bh:.6f}%;'
  # Captions stay with images when the next paragraph is explicitly italic.
  for f in list(body.select('figure')):
   nxt=f.find_next_sibling()
   if nxt and nxt.name=='p' and nxt.find('em') and len(nxt.get_text())<500:
    nxt.name='figcaption';f.append(nxt.extract())
   image=f.find('img')
   if image and 'svm-supplement-' in image.get('src',''):
    # Preserve the teacher's wide handwritten page at a readable size. The
    # paper remains portrait A4; only this full-page original is rotated.
    f['class']='source-spread'
    caption=soup.new_tag('figcaption');caption.string='SVM 手写补充原页 · 将纸张横向阅读；符号与勘误见前文 §7–10。'
    f.append(caption)
  # Keep numeric output readable on A4: repeat the row index across column panels.
  # The saved Notebook output remains untouched; only simple, rectangular tables qualify.
  for table in list(body.select('table.dataframe')):
   rows=table.find_all('tr');cells=[row.find_all(['th','td'],recursive=False) for row in rows]
   n=len(cells[0]) if cells else 0
   if n<12 or any(len(row)!=n for row in cells) or table.select('[rowspan],[colspan]'):continue
   wrapper=soup.new_tag('div',attrs={'class':'print-column-panels','data-columns':str(n)})
   for start in range(1,n,6):
    end=min(start+6,n);panel=copy.deepcopy(table)
    panel['class']=list(panel.get('class',[]))+['print-column-panel']
    panel['data-column-start']=str(start);panel['data-column-end']=str(end)
    for row in panel.find_all('tr'):
     for i,cell in enumerate(list(row.find_all(['th','td'],recursive=False))):
      if i!=0 and not start<=i<end:cell.decompose()
    caption=soup.new_tag('caption');caption.string=f'同一张数据表 · 字段 {start}–{end-1} / {n-1}（行号对应）'
    panel.insert(0,caption);wrapper.append(panel)
   table.replace_with(wrapper)
  for table in body.find_all('table'):
   heading=table.find_previous(['h2','h3'])
   if heading and any(key in heading.get_text().lower() for key in ['覆盖索引','来源索引','source coverage','从哪里来，学到哪里为止']):
    table['class']=list(table.get('class',[]))+['source-index']
  h1s=body.find_all('h1')
  for i,h in enumerate(h1s):
   h['class']='doc-title' if i==0 else 'doc-subtitle'
   if i:h.name='p'
  tag=soup.new_tag('p',attrs={'class':'doc-code'});tag.string=docid
  body.insert(0,tag)
  sections=[{'id':h.get('id'),'title':h.get_text(' ',strip=True)} for h in body.select('h2,h3') if h.get('id')]
  targets=[]
  for e in body.select('[id]'):
   if e.name in ['h1','h2','h3','h4']:heading=e
   elif e.name=='a':heading=e.find_next(['h1','h2','h3','h4'])
   else:continue
   if heading:targets.append({'id':e['id'],'title':heading.get_text(' ',strip=True)})
  blocks.append('<article class="doc" id="'+docid+'">'+''.join(str(x) for x in body.contents)+'</article>')
  docs.append({'id':docid,'source':r['source'],'title':title,'sections':sections,'targets':targets})
 label={'CS5489':'机器学习 · 课堂讲义与练习','CS5222':'计算机网络 · 课堂讲义与练习','Foundations':'按需基础补课与来源说明'}[group]
 rows=''.join('<tr><td><a href="#'+d['id']+'">'+html.escape(d['id'].replace(group+'-',''))+'</a></td><td>'+html.escape(d['title'].split('｜')[0].replace(' · ',' / '))+'</td><td class="page-ref">'+(str(PAGE_MAP[d['id']]['start'])+'–'+str(PAGE_MAP[d['id']]['end']) if d['id'] in PAGE_MAP else '—')+'</td></tr>' for d in docs)
 cover=f'''<section class="cover"><p class="cover-kicker">CITYU STUDY NOTES · A4 PRINT EDITION</p><h1 class="cover-title">{group if group!='Foundations' else '基础补课'}<br>{label}</h1><p class="cover-summary">沿老师课程学习，按需补基础，再做题与复习。<br>中文串讲 · English terminology · 双语题答 · 原课定位</p><table><thead><tr><th>文档</th><th>内容</th><th>页码</th></tr></thead><tbody>{rows}</tbody></table><div class="cover-notes"><p><strong>打印：</strong>A4，实际大小 / 100%，每张一页。建议双面、长边翻转；正文与表格可黑白打印；颜色编码的权重图、分类图建议彩印。左侧20 mm、右侧17 mm供装订和批注。页码就是PDF页序，可按本表选择页码范围。</p><p><strong>使用：</strong>每份Lecture/Chapter、Tutorial、Assignment保持独立起页；答案与原图已经全部展开。先遮住答案自己做，再核对过程。基础册独立保存，避免每讲重复打印。讲义中的电子链接仍保留；打印标注给出相应分册的专题页码；若链接指向整篇，则给文档起页。</p><p><strong>范围：</strong>{json.loads((C/'learning/course-notes-documents.json').read_text())['updated']}修订；当前已下载材料。优先级为有依据的学习建议，非教师公布的考试清单。原题、原结果、补充推导及本轮实测依正文标注区分；没有用历史材料替代未下载内容。</p></div></section>'''
 if len(docs)>10:cover=cover.replace('class="cover"','class="cover cover-long"',1)
 vendor=(C/'vendor/katex').as_uri()
 js='''renderMathInElement(document.querySelector('main'),{delimiters:[{left:"\\\\[",right:"\\\\]",display:true},{left:"\\\\(",right:"\\\\)",display:false}],throwOnError:false});window.printReady=true;'''
 page=f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{group} · A4学习讲义</title><link rel="stylesheet" href="{vendor}/katex.min.css"><style>{CSS}</style></head><body><main>{cover}{"".join(blocks)}</main><script src="{vendor}/katex.min.js"></script><script src="{vendor}/contrib/auto-render.min.js"></script><script>{js}</script></body></html>'
 (OUT/(group+'.html')).write_text(page)
 manifest[group]={'html':str((OUT/(group+'.html')).relative_to(C)),'pdf':'pdf/'+group+'-A4.pdf','documents':docs}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Built 3 print books from registered sources; notes and saved outputs are unchanged.')
