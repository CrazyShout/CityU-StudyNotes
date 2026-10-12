"""Build and validate the separate, combined and concise midterm books in isolation.

Uses the current Python interpreter and --node (default: node). PLAYWRIGHT_MODULE
and CHROME_PATH are passed through unchanged. Original exam archives are optional;
committed figure assets suffice for routine builds.
"""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from book_support import sha256
from book_editions import CONCISE_KINDS, EDITION_FLAGS, SPLIT_TYPES

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SEPARATE_OUTPUTS = ('Questions.pdf', 'Answers.pdf', 'PageIndex.json', 'PaperIndex.md',
                    'CalculationChecks.json', 'SourceValidation.json', 'Validation.json')
COMBINED_OUTPUTS = ('Combined.md', 'Combined.pdf', 'CombinedPageIndex.json', 'CombinedValidation.json')
COMPACT_OUTPUTS = ('Compact.md', 'Compact.pdf', 'CompactPageIndex.json', 'CompactValidation.json')
SPLIT_OUTPUTS = tuple(kind + suffix for kind in SPLIT_TYPES
                      for suffix in ('.md', '.pdf', 'PageIndex.json', 'Validation.json'))
OUTPUTS = SEPARATE_OUTPUTS + COMBINED_OUTPUTS + COMPACT_OUTPUTS + SPLIT_OUTPUTS + ('.build',)
# PaperIndex is both an input (paper/question mapping) and a generated page-column output.
GENERATED_ONLY = set(OUTPUTS) - {'PaperIndex.md'}


def source_snapshot(root):
    result = {}
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if any(part.startswith('.') or part == '__pycache__' for part in relative.parts):
            continue
        if path.is_file() and str(relative) not in GENERATED_ONLY:
            result[relative.as_posix()] = sha256(path)
    return result


def output_snapshot(root):
    return {name: sha256(root / name) if (root / name).is_file() else None
            for name in OUTPUTS if name != '.build'}


def remove(path):
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def publish(stage, destination, outputs=OUTPUTS):
    """Rollback all previous outputs on an ordinary failure or interruption."""
    for name in outputs:
        assert (stage / name).exists(), ('Missing staged output', name)
    backup = Path(tempfile.mkdtemp(prefix='.midterm-publish-backup-', dir=destination.parent))
    touched = []
    try:
        for name in outputs:
            target = destination / name
            had_old = target.exists()
            touched.append((name, had_old))
            if had_old:
                os.replace(target, backup / name)
            os.replace(stage / name, target)
    except BaseException:
        failures = []
        for name, had_old in reversed(touched):
            target, old = destination / name, backup / name
            try:
                if old.exists():
                    remove(target)
                    os.replace(old, target)
                elif not had_old:
                    remove(target)
            except OSError as error:
                failures.append(f'{name}: {error}')
        if failures:
            raise RuntimeError(f'Rollback needs manual recovery from {backup}: ' + '; '.join(failures))
        shutil.rmtree(backup)
        raise
    else:
        shutil.rmtree(backup)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--node', default='node', help='Node.js executable used for Playwright')
    parser.add_argument('--source-dir', type=Path, help='Optionally verify externally held Sxxx.ext original archives')
    edition = parser.add_mutually_exclusive_group()
    edition.add_argument('--combined-only', action='store_true', help='Build the combined copy while preserving other editions')
    edition.add_argument('--compact-only', action='store_true', help='Build the concise bilingual copy while preserving other editions')
    edition.add_argument('--split-only', action='store_true', help='Build both question-type copies while preserving other editions')
    args = parser.parse_args()
    assert (REPO / 'vendor/katex/katex.min.js').is_file(), 'Missing repository vendor/katex'
    node = shutil.which(args.node)
    assert node, f'Node executable not found: {args.node}'
    node = str(Path(node).resolve())
    source_args = ['--source-dir', str(args.source_dir.resolve())] if args.source_dir else []
    original_sources = source_snapshot(ROOT)
    original_outputs = output_snapshot(ROOT)
    with tempfile.TemporaryDirectory(prefix='.midterm-build-', dir=ROOT.parent) as temporary:
        stage = Path(temporary) / 'CS5489/exam-review/Midterm'
        shutil.copytree(ROOT, stage, ignore=shutil.ignore_patterns('.build', '__pycache__', '.DS_Store'))
        partial_build = args.combined_only or args.compact_only or args.split_only
        if partial_build and (ROOT / '.build').is_dir():
            shutil.copytree(ROOT / '.build', stage / '.build')
        assert source_snapshot(stage) == original_sources == source_snapshot(ROOT), 'Sources changed during staging; rerun the build'
        tools = stage / 'tools'

        def python(script, *arguments):
            subprocess.run([sys.executable, str(tools / script), *map(str, arguments)], check=True, cwd=stage)

        check_only = ['--check'] if partial_build else []
        python('verify_calculations.py', *check_only)
        python('validate_source.py', *check_only, *source_args)
        editions = (list(SPLIT_TYPES) if args.split_only else ['Compact'] if args.compact_only
                    else ['Combined'] if args.combined_only else [None, *EDITION_FLAGS])
        for derived in editions:
            flags = [EDITION_FLAGS[derived]] if derived else []
            if derived in CONCISE_KINDS:
                python('assemble_compact.py', '--kind', derived)
            elif derived:
                python('assemble_combined.py')
            stable = False
            for round_number in range(1, 6):
                page_index = stage / (f'{derived}PageIndex.json' if derived else 'PageIndex.json')
                before = json.loads(page_index.read_text()) if page_index.exists() else {}
                print(f'Midterm {derived or "separate"} pagination round {round_number}/5', flush=True)
                python('build_books.py', '--notes-root', REPO, *flags)
                subprocess.run([node, str(tools / 'render_books.cjs'), *flags], check=True, cwd=stage)
                python('finalize_books.py', *flags)
                if json.loads(page_index.read_text()) == before:
                    stable = True
                    break
            assert stable, 'Pagination did not stabilize within five rounds; original outputs were preserved'
            if not derived:
                python('update_paper_index.py')
            python('validate_books.py', '--require-render', *flags, *source_args)
        assert source_snapshot(ROOT) == original_sources, 'Sources changed during build; original outputs were preserved'
        assert output_snapshot(ROOT) == original_outputs, 'Another build changed outputs; nothing was published'
        selected = (SPLIT_OUTPUTS if args.split_only else COMPACT_OUTPUTS if args.compact_only
                    else COMBINED_OUTPUTS if args.combined_only else None)
        publish(stage, ROOT, selected + ('.build',) if selected else OUTPUTS)
    print('Published validated midterm PDFs, stable page maps, paper index and build reports.', flush=True)


if __name__ == '__main__':
    main()
