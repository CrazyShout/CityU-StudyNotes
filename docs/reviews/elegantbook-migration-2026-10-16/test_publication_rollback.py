from pathlib import Path
import sys,json,hashlib,importlib.util
from unittest.mock import patch
root=Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/'scripts'))
sys.argv=['build_latex.py','--book','CS5489','--book','CS5222']
spec=importlib.util.spec_from_file_location('publication_under_test',root/'scripts/build_latex.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
from latex_project import output,ALL_BOOKS,stubs,DOCS,MANIFEST,PAGE_MAP,MID
paths=set(stubs(module.MAPS))|{root/d['notebook'] for d in DOCS if 'notebook' in d}|{output(b) for b in ALL_BOOKS}|{MANIFEST,PAGE_MAP,root/'pdf/manifest.json',root/'pdf/README.md',MID/'PaperIndex.md'}|set(MID.glob('*PageIndex.json'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={str(p):sha(p) for p in paths};real_replace=module.os.replace;count=0
module.SOURCE_REF='simulated-interrupted-publication'
def interrupt(src,dst):
 global count
 count+=1
 if count==2:raise OSError('Simulated interruption after replacing one PDF')
 return real_replace(src,dst)
try:
 with patch.object(module.os,'replace',interrupt):module.publish()
except OSError as e:assert 'Simulated interruption' in str(e)
else:raise AssertionError('The simulated publication failure was not triggered')
assert count==2
assert before=={str(p):sha(p) for p in paths}
print(json.dumps({'partial_publication_rollback':'passed','verified_files':len(paths),'replacements_before_interruption':1}))
