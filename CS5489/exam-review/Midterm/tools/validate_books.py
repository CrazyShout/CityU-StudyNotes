"""Validate committed A4 PDFs without caches; optionally require fresh render evidence."""
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from urllib.parse import urlsplit
from collections import Counter
import argparse
import json
import re
import markdown
from pypdf import PdfReader
from bs4 import BeautifulSoup
from book_support import KINDS, compact, expected_references, sha256, validate_catalog

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true', help='Validate without writing any files')
parser.add_argument('--require-render', action='store_true', help='Also verify fresh render report and HTML printed page references')
parser.add_argument('--source-dir', type=Path, help='Optionally verify original archive files named Sxxx.ext')
args = parser.parse_args()
index = json.loads((ROOT / 'QuestionIndex.json').read_text())
maps = json.loads((ROOT / 'PageIndex.json').read_text())
ids = [question['id'].lower() for question in index['questions']]
assert len(ids) == len(set(ids)) == index['unique_questions'] == 67
positions = [(item['paper'], item['question']) for q in index['questions'] for item in q['occurrences']]
assert len(positions) == len(set(positions)) == index['original_question_positions'] == 78
assert len(index['papers']) == 6
assert sum(len(question['legacy_ids']) for question in index['questions']) == 15
assert set(maps) == set(KINDS)
assert all(set(maps[kind]) == set(ids) for kind in KINDS)
catalog_checks = validate_catalog(ROOT, index, args.source_dir)
books, soups = [], {}
printed_refs = 0


def walk(items):
    for item in items:
        if isinstance(item, list):
            yield from walk(item)
        else:
            yield item


for kind in KINDS:
    source = (ROOT / f'{kind}.md').read_text()
    assert re.findall(r'^## (MT\d{3})', source, re.M) == [item.upper() for item in ids], (kind, 'Source order')
    soup = BeautifulSoup(markdown.markdown(source, extensions=['tables', 'toc', 'md_in_html', 'pymdownx.arithmatex'],
                         extension_configs={'pymdownx.arithmatex': {'generic': True}}), 'html.parser')
    soups[kind] = soup
    refs = list(expected_references(soup, kind, maps))
    expected_targets = Counter((item['target'], item['key']) for item in refs)
    file = ROOT / f'{kind}.pdf'
    reader = PdfReader(file, strict=True)
    metadata = reader.metadata or {}
    for key, path in [('/MidtermSourceSHA256', ROOT / f'{kind}.md'),
                      ('/MidtermIndexSHA256', ROOT / 'QuestionIndex.json'),
                      ('/MidtermPageIndexSHA256', ROOT / 'PageIndex.json')]:
        assert metadata.get(key) == sha256(path), (kind, 'PDF is not bound to current source/index; run tools/build_all.py', key)
    outline = {re.match(r'MT\d{3}', dest['/Title'])[0].lower(): reader.get_destination_page_number(dest) + 1
               for dest in walk(reader.outline) if re.match(r'MT\d{3}', dest['/Title'])}
    assert outline == maps[kind], (kind, 'Outline/page-index mismatch')
    texts = [page.extract_text() for page in reader.pages]
    for question in index['questions']:
        qid = question['id'].lower()
        page_number = maps[kind][qid]
        assert isinstance(page_number, int) and 1 <= page_number <= len(reader.pages)
        assert question['id'] in texts[page_number - 1], (kind, qid, page_number)
        for key in [qid] + [alias.lower() for alias in question['legacy_ids']]:
            destination = reader.named_destinations.get('/' + key) or reader.named_destinations.get(key)
            assert destination and reader.get_destination_page_number(destination) + 1 == page_number, (kind, key, page_number)
    full_text = compact('\n'.join(texts))
    expected_text = Counter(item['text'] for item in refs)
    for text, count in expected_text.items():
        assert full_text.count(text) >= count, (kind, 'Missing or incorrect printed page reference', text, count)
    printed_refs += len(refs)
    link_count = 0
    actual_targets = Counter()
    for page, text in zip(reader.pages, texts):
        assert abs(float(page.mediabox.width) - 595.28) < 2 and abs(float(page.mediabox.height) - 841.89) < 2
        assert not re.search(r'Student (?:EID|ID)|Seat Number|/Users/|/home/|file://', text), (kind, 'Private data in PDF')
        for ref in page.get('/Annots', []):
            annotation = ref.get_object()
            action = annotation.get('/A', {})
            uri = str(action.get('/URI', ''))
            identity = str(annotation.get('/NM', ''))
            if identity.startswith('midterm:'):
                _, target, key = identity.split(':')
                assert target in maps and key in maps[target], identity
                actual_targets[(target, key)] += 1
                if target == kind:
                    destination = annotation.get('/Dest', action.get('/D', ''))
                    assert str(destination).lstrip('/') == key, (identity, destination)
                else:
                    assert uri == f'{target}.pdf#page={maps[target][key]}', (identity, uri)
            if uri:
                parsed = urlsplit(uri)
                assert not parsed.scheme and parsed.path in ['Questions.pdf', 'Answers.pdf'], uri
                assert parsed.fragment.startswith('page='), uri
                assert int(parsed.fragment[5:]) in maps[Path(parsed.path).stem].values(), uri
                assert identity.startswith('midterm:'), ('Untracked cross-book link', uri)
                link_count += 1
    # One wrapped link can produce several PDF annotations; every source link still needs a matching target.
    for target, count in expected_targets.items():
        assert actual_targets[target] >= count, (kind, 'Missing PDF link target', target, count)
    assert set(actual_targets) == set(expected_targets), (kind, 'Unexpected PDF link targets')
    books.append({'file': file.name, 'pages': len(reader.pages), 'sha256': sha256(file),
                  'source_sha256': sha256(ROOT / f'{kind}.md'), 'portable_cross_book_links': link_count})

paper_rows = re.findall(r'^\| Q\d+ \|.*$', (ROOT / 'PaperIndex.md').read_text(), re.M)
assert len(paper_rows) == 78
for line in paper_rows:
    qid = re.search(r'\bMT\d{3}\b', line)[0].lower()
    for kind in KINDS:
        assert f'[{maps[kind][qid]}]({kind}.pdf#page={maps[kind][qid]})' in line, (qid, kind)
html_refs = 0
if args.require_render:
    reports = json.loads((ROOT / '.build/render-report.json').read_text())
    assert {row['kind'] for row in reports} == set(KINDS) and len(reports) == 2
    for row in reports:
        kind = row['kind']
        assert not row['mathErrors'] and not row['brokenImages'] and not row['overflow'] and not row['errors'], kind
        assert row['questions'] == ids, (kind, 'Rendered question order')
        assert row['source_sha256'] == sha256(ROOT / f'{kind}.md'), (kind, 'Stale source render')
        assert row['index_sha256'] == sha256(ROOT / 'QuestionIndex.json'), (kind, 'Stale index render')
        assert row['html_sha256'] == sha256(ROOT / '.build' / f'{kind}.html'), (kind, 'Stale HTML render')
        assert row['final_pdf_sha256'] == sha256(ROOT / f'{kind}.pdf'), (kind, 'Stale PDF render')
        assert row['page_maps_used'] == maps, (kind, 'Printed page references were not rebuilt after pagination')
        soup = BeautifulSoup((ROOT / '.build' / f'{kind}.html').read_text(), 'html.parser')
        rendered_refs = soup.select('.page-ref')
        assert len(rendered_refs) == len(list(expected_references(soups[kind], kind, maps))), kind
        for ref in rendered_refs:
            anchor = ref.find_previous_sibling('a')
            assert anchor
            href = anchor['href']
            key = href.split('#')[-1]
            target = kind if href.startswith('#') else Path(href.split('#')[0]).stem
            assert f'第{maps[target][key]}页' in ref.get_text(), (kind, href, ref.get_text())
            html_refs += 1
numeric = json.loads((ROOT / 'CalculationChecks.json').read_text())
assert numeric['status'] == 'passed' and numeric['checks']
result = {'status': 'passed', 'books': books, 'unique_question_answer_pairs': 67, 'original_question_positions': 78,
          'independent_midterms': 6, 'independent_page_maps': True, 'verified_printed_page_references': printed_refs,
          'verified_html_page_references': html_refs, 'paper_index_rows': len(paper_rows), 'legacy_aliases_per_book': 15,
          **catalog_checks, 'numeric_checks': len(numeric['checks']),
          'render_evidence': 'verified_current' if args.require_render else 'not_requested',
          'visual_review': 'Recorded separately after examining rendered pages; not inferred from automated checks.'}
if not args.check:
    (ROOT / 'Validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False))
