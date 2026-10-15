"""Build the shared native TeX midterm editions, retaining the existing selection flags."""
from pathlib import Path
import argparse
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[4]
p=argparse.ArgumentParser(description=__doc__)
g=p.add_mutually_exclusive_group()
for flag in ['combined-only','compact-only','split-only']:g.add_argument('--'+flag,action='store_true')
p.add_argument('--jobs',type=int,default=2)
a=p.parse_args()
books=['Combined'] if a.combined_only else ['Compact'] if a.compact_only else ['MultipleChoice','WrittenResponse'] if a.split_only else ['Questions','Answers','Combined','Compact','MultipleChoice','WrittenResponse']
cmd=[sys.executable,str(ROOT/'scripts/build.py'),'--jobs',str(a.jobs)]
for book in books:cmd+=['--book',book]
subprocess.run(cmd,cwd=ROOT,check=True)
