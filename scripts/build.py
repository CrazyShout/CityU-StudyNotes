"""Build three A4 books from authored Markdown and saved Notebook outputs."""
from pathlib import Path
import argparse,json,subprocess,sys,os,hashlib
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--node',default='node');p.add_argument('--finalize-python',default=sys.executable);args=p.parse_args()
run=ROOT/'.build/reports';run.mkdir(parents=True,exist_ok=True)
def call(*cmd):subprocess.run([str(x) for x in cmd],cwd=ROOT,check=True)
call(sys.executable,ROOT/'CS5489/course-notes/tools/build_previews.py')
for iteration in range(5):
    paths=[ROOT/'.build/print'/f for f in ['page-map.json','anchor-map.json']]
    old=[p.read_bytes() if p.exists() else b'' for p in paths]
    call(sys.executable,ROOT/'scripts/build_course_print.py')
    call(args.node,ROOT/'scripts/render_course_print.cjs',run)
    call(sys.executable,ROOT/'scripts/index_course_print.py')
    if old==[p.read_bytes() for p in paths]:break
else:raise RuntimeError('Pagination did not stabilize')
call(args.finalize_python,ROOT/'scripts/index_course_print.py','--finalize')
page_map=json.loads((ROOT/'.build/print/page-map.json').read_text())
manifest={'updated':json.loads((ROOT/'learning/course-notes-documents.json').read_text())['updated'],'books':[]}
lines=['# A4 PDFs','','A4、100%实际大小、每张一页；双面建议长边翻转。答案已展开。颜色区分权重/类别的图建议彩印。','','[项目首页](../README.md) · [源稿与贡献方法](../CONTRIBUTING.md)','']
for group in ['CS5489','CS5222','Foundations']:
    file=ROOT/'pdf'/(group+'-A4.pdf');n=len(PdfReader(file,strict=True).pages)
    docs=[{'id':k,**v} for k,v in page_map.items() if v['group']==group]
    manifest['books'].append({'file':file.name,'pages':n,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'documents':docs})
    lines += [f'## {group}', '', f'[下载PDF]({file.name}) · {n}页','','| 文档 | PDF页码 |','|---|---|']
    for d in docs:lines.append(f"| [{d['id'].split('-',1)[1]}](../{d['source']}) | {d['start']}–{d['end']} |")
    lines.append('')
(ROOT/'pdf/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(ROOT/'pdf/README.md').write_text('\n'.join(lines).rstrip()+'\n')
print('PDFs and page index rebuilt without executing course experiments.')
