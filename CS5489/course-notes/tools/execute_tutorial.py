"""Execute the authored notebook from a fresh kernel; never execute source notebooks."""
from pathlib import Path
import json,os,time,argparse
import nbformat
from nbclient import NotebookClient
OUT=Path(__file__).resolve().parents[1]
cache=OUT/'.cache';cache.mkdir(exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(cache/'matplotlib'))
os.environ.setdefault('JUPYTER_RUNTIME_DIR',str(cache/'jupyter'))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--notebook',choices=['Tutorial01.ipynb','Tutorial02.ipynb','Tutorial03.ipynb','Tutorial04.ipynb'],default='Tutorial02.ipynb')
parser.add_argument('--timeout',type=int,default=180)
args=parser.parse_args()
nbpath=OUT/args.notebook
nb=nbformat.read(nbpath,as_version=4)
nbformat.validate(nb)
for cell in nb.cells:
    if cell.cell_type=='code':cell.outputs=[];cell.execution_count=None
started=time.monotonic()
client=NotebookClient(nb,timeout=args.timeout,kernel_name='python3',resources={'metadata':{'path':str(OUT)}},allow_errors=False)
client.execute()
nbformat.validate(nb)
assert all(not any(o.output_type=='error' for o in c.get('outputs',[])) for c in nb.cells)
nbformat.write(nb,nbpath)
report={'executed':True,'code_cells':sum(c.cell_type=='code' for c in nb.cells),'seconds':round(time.monotonic()-started,2),
        'counts':[c.execution_count for c in nb.cells if c.cell_type=='code'],
        'png_outputs':sum('image/png' in o.get('data',{}) for c in nb.cells for o in c.get('outputs',[])),
        'source':'authored '+args.notebook+'; original Canvas notebook unchanged'}
reports=OUT/'execution';reports.mkdir(exist_ok=True)
(reports/(nbpath.stem+'.json')).write_text(json.dumps(report,indent=2)+'\n')
if args.notebook=='Tutorial02.ipynb':
    (OUT/'execution-status.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
