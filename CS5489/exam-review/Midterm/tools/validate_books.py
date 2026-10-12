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
from book_editions import CONCISE_KINDS, add_edition_arguments, selected_questions

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true', help='Validate without writing any files')
parser.add_argument('--require-render', action='store_true', help='Also verify fresh render report and HTML printed page references')
parser.add_argument('--source-dir', type=Path, help='Optionally verify original archive files named Sxxx.ext')
add_edition_arguments(parser)
args = parser.parse_args()
derived = args.edition
kinds = (derived,) if derived else KINDS
map_file = ROOT / (f'{derived}PageIndex.json' if derived else 'PageIndex.json')
if derived == 'Combined':
    from assemble_combined import combined_source
    assert (ROOT / 'Combined.md').read_text() == combined_source(ROOT), 'Combined manuscript is stale'
if derived in CONCISE_KINDS:
    from assemble_compact import compact_source
    from question_types import type_label, toc_marker
    assert (ROOT / f'{derived}.md').read_text() == compact_source(ROOT, derived), f'{derived} manuscript is stale'
index = json.loads((ROOT / 'QuestionIndex.json').read_text())
maps = json.loads(map_file.read_text())
all_ids = [question['id'].lower() for question in index['questions']]
assert len(all_ids) == len(set(all_ids)) == index['unique_questions'] == 67
questions = selected_questions(index, derived)
ids = [question['id'].lower() for question in questions]
selected_positions = {(item['paper'], item['question'], q['id'])
                      for q in questions for item in q['occurrences']}
alias_count = sum(len(question['legacy_ids']) for question in questions)
positions = [(item['paper'], item['question']) for q in index['questions'] for item in q['occurrences']]
assert len(positions) == len(set(positions)) == index['original_question_positions'] == 78
assert len(index['papers']) == 6
assert sum(len(question['legacy_ids']) for question in index['questions']) == 15
assert set(maps) == set(kinds)
assert all(set(maps[kind]) == set(ids) for kind in kinds)
catalog_checks = validate_catalog(ROOT, index, args.source_dir)
books, soups = [], {}
printed_refs = 0


def walk(items):
    for item in items:
        if isinstance(item, list):
            yield from walk(item)
        else:
            yield item


for kind in kinds:
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
                      ('/MidtermPageIndexSHA256', map_file)]:
        assert metadata.get(key) == sha256(path), (kind, 'PDF is not bound to current source/index; run tools/build_all.py', key)
    if kind in ('Combined', *CONCISE_KINDS):
        for name in ['Questions', 'Answers']:
            assert metadata.get(f'/Midterm{name}SourceSHA256') == sha256(ROOT / f'{name}.md'), (kind, 'Input changed', name)
    heading_dests = {re.match(r'MT\d{3}', dest['/Title'])[0].lower(): dest
                     for dest in walk(reader.outline) if re.match(r'MT\d{3}', dest['/Title'])}
    outline = {key: reader.get_destination_page_number(dest) + 1 for key, dest in heading_dests.items()}
    assert outline == maps[kind], (kind, 'Outline/page-index mismatch')
    texts = [page.extract_text() for page in reader.pages]
    for question in questions:
        qid = question['id'].lower()
        page_number = maps[kind][qid]
        assert isinstance(page_number, int) and 1 <= page_number <= len(reader.pages)
        assert question['id'] in texts[page_number - 1], (kind, qid, page_number)
        for key in [qid] + [alias.lower() for alias in question['legacy_ids']]:
            destination = reader.named_destinations.get('/' + key) or reader.named_destinations.get(key)
            assert destination and reader.get_destination_page_number(destination) + 1 == page_number, (kind, key, page_number)
            if kind in CONCISE_KINDS:
                assert destination.get('/Type') == '/XYZ' and abs(float(destination.top) - float(heading_dests[qid].top)) < 0.001, (kind, key, 'Heading position differs')
    if kind in ('Answers', 'Combined'):
        for i, qid in enumerate(ids):
            start = maps[kind][qid] - 1
            end = maps[kind][ids[i + 1]] - 1 if i + 1 < len(ids) else len(texts)
            question_text = compact('\n'.join(texts[start:end]))
            assert question_text.count('中文对应答案') == 1, (qid, 'Missing or repeated Chinese answer in PDF')
            assert question_text.index('Englishanswer') < question_text.index('中文对应答案') < question_text.index('中文讲解'), (qid, 'PDF answer section order')
            if kind == 'Combined':
                labels = ['Englishquestion', '中文题意', 'Englishanswer', '中文对应答案', '中文讲解']
                assert all(question_text.count(label) == 1 for label in labels), (qid, 'Missing or repeated combined section')
                assert [question_text.index(label) for label in labels] == sorted(question_text.index(label) for label in labels), (qid, 'Combined section order')
    if kind in CONCISE_KINDS:
        # Continuous layout may place multiple questions on one page. Split at
        # unique heading text, not at the next question's page number.
        body = compact('\n'.join(texts[min(maps[kind].values()) - 1:]))
        starts = [body.find(compact(heading_dests[qid]['/Title'])) for qid in ids]
        assert min(starts) >= 0 and starts == sorted(set(starts)), 'Compact PDF question headings missing or out of order'
        labels = ['Englishquestion', '中文题意', 'Englishanswer', '中文对应答案']
        for i, qid in enumerate(ids):
            block = body[starts[i]:starts[i + 1] if i + 1 < len(starts) else len(body)]
            question = questions[i]
            assert compact(type_label(question)) in block, (qid, 'Printed question-type label missing or incorrect')
            assert all(block.count(label) == 1 for label in labels), (qid, 'Missing or repeated concise section')
            assert [block.index(label) for label in labels] == sorted(block.index(label) for label in labels), (qid, 'Concise section order')
            assert '中文讲解' not in block, (qid, 'Explanatory section leaked into concise edition')
        contents = compact('\n'.join(texts[:min(maps[kind].values()) - 1]))
        for question in questions:
            assert compact(question['id'] + ' · ' + question['title'] + '〔' + toc_marker(question) + '〕') in contents, (question['id'], 'Contents type label missing')
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
            assert annotation.get('/Subtype') == '/Link', (kind, 'Personal or non-link annotation in generated PDF')
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

paper_text = (ROOT / (f'{derived}.md' if derived else 'PaperIndex.md')).read_text()
if not derived:
    paper_soup = BeautifulSoup(markdown.markdown(paper_text, extensions=['tables']), 'html.parser')
    tables = paper_soup.select('table')
    assert len(tables) == len(index['papers']), 'Original-paper index must render as six tables'
    for table in tables:
        assert len(table.select('thead th')) == 6, 'Original-paper index must have six columns'
        rows = table.select('tbody tr')
        assert len(rows) == 13 and all(len(row.find_all('td', recursive=False)) == 6 for row in rows), 'Original-paper index has malformed rows'
paper_rows = re.findall(r'^\| Q\d+ \|.*$', paper_text, re.M)
assert len(paper_rows) == len(selected_positions)
if derived:
    # Verify each selected original position, not just a row count.
    expected_rows = []
    for paper in index['papers']:
        entries = [(o, q) for q in questions for o in q['occurrences'] if o['paper'] == paper['id']]
        for occurrence, question in sorted(entries, key=lambda item: int(item[0]['question'][1:])):
            qid = question['id']
            expected_rows.append(f"| {occurrence['question']} | [{qid}]({derived}.md#{qid.lower()}) | {occurrence['marks']} |")
    assert paper_rows == expected_rows, (derived, 'Original-paper mapping differs from selected questions')
for line in paper_rows:
    qid = re.search(r'\bMT\d{3}\b', line)[0].lower()
    if derived:
        assert f']({derived}.md#{qid})' in line, (derived, 'Paper index', qid)
    else:
        for kind in kinds:
            assert f'[{maps[kind][qid]}]({kind}.pdf#page={maps[kind][qid]})' in line, (qid, kind)
html_refs = 0
if args.require_render:
    reports = json.loads((ROOT / '.build' / (f'{derived.lower()}-render-report.json' if derived else 'render-report.json')).read_text())
    assert {row['kind'] for row in reports} == set(kinds) and len(reports) == len(kinds)
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
result = {'status': 'passed', 'books': books, 'unique_question_answer_pairs': len(ids), 'original_question_positions': len(selected_positions),
          'printed_chinese_answer_counterparts': len(ids),
          'non_link_annotations': 0,
          'independent_midterms': 6, 'independent_page_maps': True, 'verified_printed_page_references': printed_refs,
          'verified_html_page_references': html_refs, 'paper_index_rows': len(paper_rows), 'legacy_aliases_per_book': alias_count,
          **catalog_checks, 'numeric_checks': len(numeric['checks']),
          'render_evidence': 'verified_current' if args.require_render else 'not_requested',
          'visual_review': 'Recorded separately after examining rendered pages; not inferred from automated checks.'}
if not args.check:
    (ROOT / (f'{derived}Validation.json' if derived else 'Validation.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False))
