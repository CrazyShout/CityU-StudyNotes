"""Derive printed document page ranges and portable cross-book links from rendered PDFs."""
from pathlib import Path
import json,re,sys,unicodedata
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject,TextStringObject
from urllib.parse import unquote,urlsplit,quote
C=Path(__file__).resolve().parents[1];P=C/'.build/print';F=C/'pdf'
manifest=json.loads((P/'manifest.json').read_text());old=json.loads((P/'page-map.json').read_text()) if (P/'page-map.json').exists() else {}
old_anchors=json.loads((P/'anchor-map.json').read_text()) if (P/'anchor-map.json').exists() else {}
result={};pdfs={};anchors={}
for group,book in manifest.items():
 r=PdfReader(F/(group+'-A4.pdf'));pdfs[group]=r
 texts=None
 for doc in book['documents']:
  destination=r.named_destinations.get('/'+doc['id']) or r.named_destinations.get(doc['id'])
  if destination is not None:pages=[r.get_destination_page_number(destination)+1]
  else:
   if texts is None:texts=[p.extract_text() or '' for p in r.pages]
   pages=[i+1 for i,t in enumerate(texts) if re.search(r'(?m)^'+re.escape(doc['id'])+r'\s*$',t)]
  if len(pages)!=1:raise RuntimeError((doc['id'],pages))
  result[doc['id']]={'start':pages[0],'group':group,'source':doc['source']}
 for i,doc in enumerate(book['documents']):
  result[doc['id']]['end']=result[book['documents'][i+1]['id']]['start']-1 if i+1<len(book['documents']) else len(r.pages)
 def walk(items):
  for item in items:
   if isinstance(item,list):yield from walk(item)
   else:yield item
 def norm(s):return re.sub(r'\s+','',unicodedata.normalize('NFKC',s))
 headings=[(norm(o.title),r.get_destination_page_number(o)+1) for o in walk(r.outline)]
 for doc in book['documents']:
  start,end=result[doc['id']]['start'],result[doc['id']]['end']
  anchors[doc['id']]=start
  for t in doc.get('targets',[]):
   candidates=[p for title,p in headings if start<=p<=end and title==norm(t['title'])]
   if candidates:anchors[t['id']]=candidates[0]
  for key,dest in r.named_destinations.items():
   if key.lstrip('/').startswith(doc['id']+'__'):anchors[key.lstrip('/')]=r.get_destination_page_number(dest)+1
(P/'page-map.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(P/'anchor-map.json').write_text(json.dumps(anchors,ensure_ascii=False,indent=2)+'\n')
print('Page map stable:',result==old,'Anchor map stable:',anchors==old_anchors)
for group,r in pdfs.items():print(group,len(r.pages),'pages',[(d['id'],result[d['id']]['start'],result[d['id']]['end']) for d in manifest[group]['documents']])
if '--finalize' in sys.argv:
 if result!=old or anchors!=old_anchors:raise RuntimeError('Page map changed; rebuild and render before finalizing')
 for group,r in pdfs.items():
  w=PdfWriter();w.clone_document_from_reader(r)
  w.add_metadata({'/Title':group+' | A4 study notes','/Author':'Local course learning notes','/Subject':'Instructor-aligned bilingual study notes; current downloaded Canvas; collaborative study notes'})
  for doc in manifest[group]['documents']:w.add_named_destination(doc['id'],result[doc['id']]['start']-1)
  from io import BytesIO
  from reportlab.pdfgen import canvas
  from reportlab.pdfbase import pdfmetrics
  from reportlab.pdfbase.ttfonts import TTFont
  import reportlab
  pdfmetrics.registerFont(TTFont('CoursePrintHeader',str(Path(reportlab.__file__).parent/'fonts/Vera.ttf')))
  for i,page in enumerate(w.pages,1):
   # Small running document label; it occupies the existing top margin and
   # never covers course text or changes pagination.
   label=next((key for key,v in result.items() if v['group']==group and v['start']<=i<=v['end']),group+' - Contents')
   buffer=BytesIO();width,height=float(page.mediabox.width),float(page.mediabox.height)
   cv=canvas.Canvas(buffer,pagesize=(width,height));cv.setFont('CoursePrintHeader',7);cv.setFillGray(.35)
   cv.drawRightString(width-48.2,height-20,label);cv.save();buffer.seek(0)
   page.merge_page(PdfReader(buffer).pages[0])
   for ref in page.get('/Annots',[]):
    a=ref.get_object().get('/A')
    if a and '/URI' in a:
     uri=str(a['/URI'])
     hit=re.search(r'/(CS5489|CS5222|Foundations)-A4\.pdf#([^/]+)$',uri)
     if hit:
      target_anchor=unquote(hit.group(2));target_id=target_anchor.split('__')[0]; target=result.get(target_id)
      if target:a[NameObject('/URI')]=TextStringObject(hit.group(1)+'-A4.pdf#page='+str(anchors.get(target_anchor,target['start'])))
     elif uri.startswith('file:'):
      target=Path(unquote(urlsplit(uri).path)).resolve()
      if target.is_relative_to(C):a[NameObject('/URI')]=TextStringObject('https://github.com/CrazyShout/CityU-StudyNotes/blob/main/'+quote(target.relative_to(C).as_posix(),safe='/'))
      else:raise RuntimeError('Unexpected non-portable file link in PDF')
  temp=F/(group+'-A4.tmp.pdf')
  with temp.open('wb') as f:w.write(f)
  temp.replace(F/(group+'-A4.pdf'))
 print('Final metadata, named document destinations and relative cross-book links written.')
