"""Bind visual review to delivered PDFs by comparing text and rendered pixels.

The reference directory is a local snapshot of the visually reviewed candidates.
It is deliberately ignored by Git; the output records both input hashes.
"""
from pathlib import Path
import argparse
import hashlib
import json
import pymupdf

ROOT = Path(__file__).resolve().parents[3]


def compare(reference, candidate=False):
    manifest = json.loads((ROOT / 'latex/manifest.json').read_text())
    report = {'status': 'passed', 'renderer': 'PyMuPDF', 'dpi': 100, 'books': {}}
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    for book, meta in manifest['books'].items():
        previous = reference / (book + '.pdf')
        current = ROOT / (f'.build/latex/{book}/{book}.pdf' if candidate else meta['file'])
        with pymupdf.open(previous) as old, pymupdf.open(current) as new:
            text_changed, pixels_changed = [], []
            for i in range(max(len(old), len(new))):
                if i >= min(len(old), len(new)):
                    text_changed.append(i+1)
                    pixels_changed.append(i+1)
                    continue
                if old[i].get_text() != new[i].get_text():
                    text_changed.append(i+1)
                if old[i].get_pixmap(dpi=100, alpha=False).digest != new[i].get_pixmap(dpi=100, alpha=False).digest:
                    pixels_changed.append(i+1)
            report['books'][book] = {'reference_sha256': digest(previous), 'delivery_sha256': digest(current),
                'pages': len(new), 'reference_pages': len(old),
                'text_changed_pages': text_changed, 'pixel_changed_pages': pixels_changed}
            if text_changed or pixels_changed:
                report['status'] = 'differences_require_review'
    current_map = ROOT / ('.build/latex/page-maps.json' if candidate else 'latex/page-maps.json')
    report['page_maps_equal'] = json.loads((reference/'page-maps.json').read_text()) == json.loads(current_map.read_text())
    if not report['page_maps_equal']:
        report['status'] = 'differences_require_review'
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--candidate', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = compare(args.reference, args.candidate)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(report['status'])
    for book, data in report['books'].items():
        if data['pixel_changed_pages']:
            print(book, 'changed pages:', data['pixel_changed_pages'])
