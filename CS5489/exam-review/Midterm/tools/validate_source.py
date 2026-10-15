"""Compatibility entry point for native TeX source and optional archive validation."""
from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parents[4]
subprocess.run([sys.executable,str(root/'scripts/validate.py'),'--source-only',*sys.argv[1:]],check=True)
