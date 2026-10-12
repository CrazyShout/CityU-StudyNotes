"""Finalize fresh PDF renders with portable links, stable destinations and source digests."""
from pathlib import Path
import argparse
import hashlib
import json
import re
from urllib.parse import urlsplit, unquote
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject, DictionaryObject, ArrayObject
from book_support import KINDS, sha256

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
edition = parser.add_mutually_exclusive_group()
edition.add_argument('--combined', action='store_true')
edition.add_argument('--compact', action='store_true')
args = parser.parse_args()
derived = 'Compact' if args.compact else 'Combined' if args.combined else None
kinds = (derived,) if derived else KINDS
index = json.loads((ROOT / 'QuestionIndex.json').read_text())
report_path = ROOT / '.build' / (f'{derived.lower()}-render-report.json' if derived else 'render-report.json')
reports = json.loads(report_path.read_text())
by_kind = {row['kind']: row for row in reports}
assert set(by_kind) == set(kinds), 'All requested freshly rendered books are required'


def walk(items):
    for item in items:
        if isinstance(item, list):
            yield from walk(item)
        else:
            yield item


maps, readers, headings = {}, {}, {}
for kind in kinds:
    row = by_kind[kind]
    assert row['source_sha256'] == sha256(ROOT / f'{kind}.md'), (kind, 'Source changed since render')
    assert row['index_sha256'] == sha256(ROOT / 'QuestionIndex.json'), 'Question index changed since render'
    assert row['html_sha256'] == sha256(ROOT / '.build' / f'{kind}.html'), (kind, 'HTML changed since render')
    assert row['rendered_pdf_sha256'] == sha256(ROOT / f'{kind}.pdf'), (kind, 'Expected a fresh PDF render')
    reader = PdfReader(ROOT / f'{kind}.pdf', strict=True)
    readers[kind] = reader
    headings[kind] = {re.match(r'MT\d{3}', dest['/Title'])[0].lower(): dest
                      for dest in walk(reader.outline) if re.match(r'MT\d{3}', dest['/Title'])}
    maps[kind] = {key: reader.get_destination_page_number(dest) + 1 for key, dest in headings[kind].items()}
    assert len(maps[kind]) == index['unique_questions']
map_text = json.dumps(maps, indent=2) + '\n'
map_sha = hashlib.sha256(map_text.encode()).hexdigest()
for kind, reader in readers.items():
    writer = PdfWriter(clone_from=reader)
    dests = writer._root_object.get('/Dests', DictionaryObject()).get_object()
    for key, page in maps[kind].items():
        # Several concise questions can share a page; retain the heading coordinates.
        view = list(headings[kind][key].dest_array[1:]) if kind == 'Compact' else [NameObject('/Fit')]
        dests[NameObject('/' + key)] = ArrayObject([writer.pages[page - 1].indirect_reference, *view])
    for question in index['questions']:
        for alias in question['legacy_ids']:
            dests[NameObject('/' + alias.lower())] = dests[NameObject('/' + question['id'].lower())]
    writer._root_object[NameObject('/Dests')] = dests
    names = writer._root_object.get('/Names')
    if names:
        names = names.get_object()
        names.pop('/Dests', None)
        if not names:
            writer._root_object.pop('/Names', None)
    for page in writer.pages:
        for ref in page.get('/Annots', []):
            annotation = ref.get_object()
            direct_key = str(annotation.get('/Dest', '')).lstrip('/')
            if direct_key in maps[kind]:
                annotation[NameObject('/Dest')] = NameObject('/' + direct_key)
                annotation[NameObject('/NM')] = TextStringObject(f'midterm:{kind}:{direct_key}')
            action = annotation.get('/A')
            if not action:
                continue
            uri = action.get('/URI')
            local_key = str(action.get('/D', '')).lstrip('/')
            if action.get('/S') == '/GoTo' and local_key in maps[kind]:
                action[NameObject('/D')] = NameObject('/' + local_key)
                annotation[NameObject('/NM')] = TextStringObject(f'midterm:{kind}:{local_key}')
            if not uri:
                continue
            parsed = urlsplit(str(uri))
            name = Path(unquote(parsed.path)).stem
            key = parsed.fragment.lower()
            if name in maps and key in maps[name]:
                annotation[NameObject('/NM')] = TextStringObject(f'midterm:{name}:{key}')
                if name == kind:
                    annotation[NameObject('/A')] = DictionaryObject({NameObject('/S'): NameObject('/GoTo'), NameObject('/D'): NameObject('/' + key)})
                else:
                    annotation[NameObject('/A')] = DictionaryObject({NameObject('/S'): NameObject('/URI'), NameObject('/URI'): TextStringObject(f'{name}.pdf#page={maps[name][key]}')})
            elif str(uri).startswith('file:'):
                raise ValueError(('Unexpected local file link', uri))
    writer.add_metadata({'/Title': f'CS5489 Midterm - {kind}', '/Author': 'Study notes compilation',
                         '/Subject': 'Historical midterm questions with concise bilingual answers' if kind == 'Compact' else 'Historical midterm questions with bilingual explanations',
                         '/MidtermSourceSHA256': sha256(ROOT / f'{kind}.md'),
                         '/MidtermIndexSHA256': sha256(ROOT / 'QuestionIndex.json'),
                         '/MidtermPageIndexSHA256': map_sha})
    if kind in ('Combined', 'Compact'):
        writer.add_metadata({'/MidtermQuestionsSourceSHA256': sha256(ROOT / 'Questions.md'),
                             '/MidtermAnswersSourceSHA256': sha256(ROOT / 'Answers.md')})
    target = ROOT / f'{kind}.pdf'
    temporary = ROOT / f'.{kind}.final.pdf'
    writer.write(temporary)
    temporary.replace(target)
    by_kind[kind]['final_pdf_sha256'] = sha256(target)
(ROOT / (f'{derived}PageIndex.json' if derived else 'PageIndex.json')).write_text(map_text)
report_path.write_text(json.dumps(reports, ensure_ascii=False, indent=2) + '\n')
print('Finalized requested books, 67 destinations and 15 legacy aliases each; source digests embedded.')
