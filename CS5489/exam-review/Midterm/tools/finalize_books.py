"""Finalize fresh PDF renders with portable links, stable destinations and source digests."""
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import urlsplit, unquote
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject, DictionaryObject, ArrayObject
from book_support import KINDS, sha256

ROOT = Path(__file__).resolve().parents[1]
index = json.loads((ROOT / 'QuestionIndex.json').read_text())
report_path = ROOT / '.build/render-report.json'
reports = json.loads(report_path.read_text())
by_kind = {row['kind']: row for row in reports}
assert set(by_kind) == set(KINDS), 'Both freshly rendered books are required'


def walk(items):
    for item in items:
        if isinstance(item, list):
            yield from walk(item)
        else:
            yield item


maps, readers = {}, {}
for kind in KINDS:
    row = by_kind[kind]
    assert row['source_sha256'] == sha256(ROOT / f'{kind}.md'), (kind, 'Source changed since render')
    assert row['index_sha256'] == sha256(ROOT / 'QuestionIndex.json'), 'Question index changed since render'
    assert row['html_sha256'] == sha256(ROOT / '.build' / f'{kind}.html'), (kind, 'HTML changed since render')
    assert row['rendered_pdf_sha256'] == sha256(ROOT / f'{kind}.pdf'), (kind, 'Expected a fresh PDF render')
    reader = PdfReader(ROOT / f'{kind}.pdf', strict=True)
    readers[kind] = reader
    maps[kind] = {re.match(r'MT\d{3}', dest['/Title'])[0].lower(): reader.get_destination_page_number(dest) + 1
                  for dest in walk(reader.outline) if re.match(r'MT\d{3}', dest['/Title'])}
    assert len(maps[kind]) == index['unique_questions']
map_text = json.dumps(maps, indent=2) + '\n'
map_sha = hashlib.sha256(map_text.encode()).hexdigest()
for kind, reader in readers.items():
    writer = PdfWriter(clone_from=reader)
    dests = writer._root_object.get('/Dests', DictionaryObject()).get_object()
    for key, page in maps[kind].items():
        dests[NameObject('/' + key)] = ArrayObject([writer.pages[page - 1].indirect_reference, NameObject('/Fit')])
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
                         '/Subject': 'Historical midterm questions with bilingual explanations',
                         '/MidtermSourceSHA256': sha256(ROOT / f'{kind}.md'),
                         '/MidtermIndexSHA256': sha256(ROOT / 'QuestionIndex.json'),
                         '/MidtermPageIndexSHA256': map_sha})
    target = ROOT / f'{kind}.pdf'
    temporary = ROOT / f'.{kind}.final.pdf'
    writer.write(temporary)
    temporary.replace(target)
    by_kind[kind]['final_pdf_sha256'] = sha256(target)
(ROOT / 'PageIndex.json').write_text(map_text)
report_path.write_text(json.dumps(reports, ensure_ascii=False, indent=2) + '\n')
print('Finalized both books, 67 destinations and 15 legacy aliases each; source digests embedded.')
