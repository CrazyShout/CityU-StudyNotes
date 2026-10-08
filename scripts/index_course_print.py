"""Derive printed document page ranges and portable cross-book links from rendered PDFs."""
from pathlib import Path
import json,re,sys,unicodedata
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject,TextStringObject,ArrayObject,DictionaryObject
from urllib.parse import unquote,urlsplit,quote
C=Path(__file__).resolve().parents[1];P=C/'.build/print';F=C/'pdf'
manifest=json.loads((P/'manifest.json').read_text());old=json.loads((P/'page-map.json').read_text()) if (P/'page-map.json').exists() else {}
old_anchors=json.loads((P/'anchor-map.json').read_text()) if (P/'anchor-map.json').exists() else {}
result={};pdfs={};anchors={};heading_destinations={};destination_repairs=[]
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
 outlines=list(walk(r.outline))
 headings=[(norm(o.title),r.get_destination_page_number(o)+1) for o in outlines]
 heading_destinations[group]={}
 for doc in book['documents']:
  start,end=result[doc['id']]['start'],result[doc['id']]['end']
  anchors[doc['id']]=start
  for t in doc.get('targets',[]):
   candidates=[p for title,p in headings if start<=p<=end and title==norm(t['title'])]
   if candidates:anchors[t['id']]=candidates[0]
  for key,dest in r.named_destinations.items():
   if key.lstrip('/').startswith(doc['id']+'__'):anchors[key.lstrip('/')]=r.get_destination_page_number(dest)+1
  # Chromium occasionally leaves a named destination at its pre-pagination
  # position even when it wraps real heading text. The outline has the actual
  # printed heading position; use it for the page map and final PDF destination.
  for target in doc.get('targets',[]):
   if not target.get('attached_to_heading'):continue
   key='/'+target['id'] if '/'+target['id'] in r.named_destinations else target['id']
   actual=r.named_destinations.get(key)
   if actual is None:continue
   matches=[o for o in outlines if start<=r.get_destination_page_number(o)+1<=end and norm(o.title)==norm(target['title'])]
   if len(matches)!=1:raise RuntimeError(('Ambiguous heading destination',target['id'],len(matches)))
   heading=matches[0];page=r.get_destination_page_number(heading)+1
   heading_destinations[group][key]=(page,heading.dest_array)
   anchors[target['id']]=page
   if r.get_destination_page_number(actual)+1!=page:
    destination_repairs.append({'group':group,'id':target['id'],'from':r.get_destination_page_number(actual)+1,'to':page})
(P/'heading-destination-repairs.json').write_text(json.dumps(destination_repairs,ensure_ascii=False,indent=2)+'\n')
(P/'page-map.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(P/'anchor-map.json').write_text(json.dumps(anchors,ensure_ascii=False,indent=2)+'\n')
print('Page map stable:',result==old,'Anchor map stable:',anchors==old_anchors)
for group,r in pdfs.items():print(group,len(r.pages),'pages',[(d['id'],result[d['id']]['start'],result[d['id']]['end']) for d in manifest[group]['documents']])
if '--finalize' in sys.argv:
 if result!=old or anchors!=old_anchors:raise RuntimeError('Page map changed; rebuild and render before finalizing')
 for group,r in pdfs.items():
  w=PdfWriter();w.clone_document_from_reader(r)
  destinations=w.get_named_dest_root()
  repaired=set()
  # Chromium uses the legacy /Dests dictionary; other producers use /Names.
  direct=w.root_object.get('/Dests')
  if direct:
   direct=direct.get_object()
   for key in list(direct):
    if str(key) in heading_destinations[group]:
     page,array=heading_destinations[group][str(key)]
     direct[key]=ArrayObject([w.pages[page-1].indirect_reference,*array[1:]])
     repaired.add(str(key))
  for index in range(0,len(destinations),2):
   key=str(destinations[index])
   if key not in heading_destinations[group]:continue
   page,array=heading_destinations[group][key]
   corrected=ArrayObject([w.pages[page-1].indirect_reference,*array[1:]])
   item=destinations[index+1].get_object()
   if isinstance(item,DictionaryObject):item[NameObject('/D')]=corrected
   else:destinations[index+1]=corrected
   repaired.add(key)
  if repaired!=set(heading_destinations[group]):raise RuntimeError(('Unrepaired heading destinations',group,set(heading_destinations[group])-repaired))

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
  verified=PdfReader(F/(group+'-A4.pdf'),strict=True)
  for key,(page,_) in heading_destinations[group].items():
   if verified.get_destination_page_number(verified.named_destinations[key])+1!=page:
    raise RuntimeError(('Final PDF destination mismatch',group,key,page))

 print('Final metadata, named document destinations and relative cross-book links written.')
