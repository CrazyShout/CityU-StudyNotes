"""Build and verify standalone ElegantBook A4 Final Exam Q&A PDFs with full CJK Unicode checks."""
from collections import Counter
from pathlib import Path
import argparse
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from pdf_fonts import check_unicode_fonts, embed_cjk_unicode
from pypdf import PdfReader, PdfWriter
import pymupdf


def build_tex(tex_path: Path, out_pdf: Path):
    tex_path = tex_path.resolve()
    out_pdf = out_pdf.resolve()
    build_dir = ROOT / '.build' / 'final-qa' / tex_path.stem
    build_dir.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    local = ROOT / '.build/texmf'
    if local.is_dir():
        env['TEXMFHOME'] = str(local)
        env['TEXMFVAR'] = str(ROOT / '.build/texmf-var')
    env['TEXINPUTS'] = str(ROOT / 'latex/vendor/elegantbook') + '//:' + env.get('TEXINPUTS', '')

    cmd = [
        'xelatex', '-no-shell-escape', '-interaction=nonstopmode',
        '-halt-on-error', '-file-line-error',
        '-output-directory=' + str(build_dir), tex_path.name,
    ]
    for pass_no in range(1, 3):
        res = subprocess.run(cmd, cwd=tex_path.parent, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        (build_dir / f'pass-{pass_no}.log').write_text(res.stdout)
        if res.returncode != 0:
            print(res.stdout[-2500:], file=sys.stderr)
            raise RuntimeError(f'XeLaTeX failed on pass {pass_no} for {tex_path}')

    log = (build_dir / (tex_path.stem + '.log')).read_text(errors='replace')
    missing = re.findall(r'Missing character:.*', log)
    undef = re.findall(r'undefined references|Reference .* undefined', log)
    overfull = [float(x) for x in re.findall(r'Overfull \\[hv]box \(([\d.]+)pt', log) if float(x) > 1.0]
    if missing or undef or overfull:
        raise RuntimeError(f'Diagnostics failed: missing={missing[:3]} undef={undef[:3]} overfull={overfull}')

    raw_pdf = build_dir / (tex_path.stem + '.pdf')
    reader = PdfReader(raw_pdf)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    embed_cjk_unicode(writer)
    check_unicode_fonts(writer)
    tmp_pdf = build_dir / (tex_path.stem + '.unicode.pdf')
    with tmp_pdf.open('wb') as f:
        writer.write(f)
    os.replace(tmp_pdf, out_pdf)

    # Dual-parser CJK verification
    r_check = PdfReader(out_pdf, strict=True)
    with pymupdf.open(out_pdf) as doc:
        cjk = lambda s: Counter(c for c in s if '\u3400' <= c <= '\u9fff')
        for page in doc:
            assert cjk(r_check.pages[page.number].extract_text()) == cjk(page.get_text()), f'CJK mismatch on p.{page.number+1}'
            assert abs(page.rect.width - 595.28) < 2 and abs(page.rect.height - 841.89) < 2
        pages = len(doc)
    print(f'Built and verified {out_pdf.relative_to(ROOT)}: {pages} pages, 0 missing glyphs, 0 overfull > 1pt, CJK dual-parser OK.')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('tex', type=Path)
    p.add_argument('--out', type=Path, default=None)
    args = p.parse_args()
    out = args.out or args.tex.with_suffix('.pdf')
    build_tex(args.tex, out)


if __name__ == '__main__':
    main()
