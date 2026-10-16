"""Compatibility entry point; native validation always checks all nine bound editions."""
from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parents[4]
args=[x for x in sys.argv[1:] if x not in ['--combined','--compact','--multiple-choice','--written-response']]
subprocess.run([sys.executable,str(root/'scripts/validate.py'),*args],check=True)
