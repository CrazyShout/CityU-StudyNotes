"""Regression for a failed PDF driver leaving an unreadable auxiliary file."""
from pathlib import Path
import importlib.util
import subprocess
import sys
import tempfile
from unittest.mock import patch
import pymupdf

root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root / 'scripts'))
sys.argv = ['build_latex.py', '--book', 'Foundations']
spec = importlib.util.spec_from_file_location('build_recovery_test', root / 'scripts/build_latex.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with tempfile.TemporaryDirectory(dir=root / '.build') as temp:
    module.ROOT = Path(temp)
    module.BUILD = module.ROOT / '.build/latex'
    (module.ROOT / '.build/texmf').mkdir(parents=True)
    folder = module.BUILD / 'Foundations'
    folder.mkdir(parents=True)
    source = folder / 'Foundations.tex'
    source.write_text('% test fixture\n')
    for suffix in ['.aux', '.out', '.toc']:
        (folder / ('Foundations' + suffix)).write_text('truncated auxiliary data {')
    candidate = folder / 'Foundations.pdf'
    candidate.write_bytes(b'previous candidate fixture')

    def fail(command, **kwargs):
        assert kwargs['env']['TEXMFHOME'] == str(module.ROOT / '.build/texmf')
        assert kwargs['env']['TEXMFVAR'] == str(module.ROOT / '.build/texmf-var')
        return subprocess.CompletedProcess(command, 1, 'Simulated font driver failure')

    with patch.object(module, 'driver', return_value=source), patch.object(module.subprocess, 'run', side_effect=fail):
        try:
            module.compile_book('Foundations')
        except RuntimeError as error:
            assert 'XeLaTeX failed' in str(error)
        else:
            raise AssertionError('The failed build was accepted')
    assert candidate.read_bytes() == b'previous candidate fixture'
    assert (folder / 'compile-output.log').read_text() == 'Simulated font driver failure'
    assert all(not (folder / ('Foundations' + ext)).exists() for ext in ['.aux', '.out', '.toc'])

    def repaired(command, **kwargs):
        assert not (folder / 'Foundations.aux').exists()
        (folder / 'Foundations.pages').write_text('Foundations__root|1\n')
        with pymupdf.open() as pdf:
            pdf.new_page()
            pdf.save(candidate)
        return subprocess.CompletedProcess(command, 0, 'Simulated repaired compilation')

    with patch.object(module, 'driver', return_value=source), patch.object(module.subprocess, 'run', side_effect=repaired):
        assert module.compile_book('Foundations') == ('Foundations', {'Foundations__root': 1})

print('Passed: project font-map isolation, failed-build diagnostics/cache cleanup, and retry after repair.')
