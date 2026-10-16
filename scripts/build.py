"""Build all nine native ElegantBook PDFs without executing notebooks."""
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'scripts/build_exam_annotations.py'),'--check'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/build_latex.py'),*sys.argv[1:]],cwd=ROOT,check=True)
