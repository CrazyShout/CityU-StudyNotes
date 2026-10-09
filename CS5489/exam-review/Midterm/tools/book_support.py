"""Shared, read-only helpers for the portable midterm build and validation tools."""
from pathlib import Path
import hashlib
import json
import re
import unicodedata

KINDS = ('Questions', 'Answers')


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compact(text):
    """Normalize PDF compatibility glyphs and line wrapping for printed-reference checks."""
    # Some CJK fonts expose radical codepoints in their PDF ToUnicode maps.
    # NFKC covers Kangxi radicals but not these visually identical variants.
    radicals = str.maketrans('⺟⻅⻆⻉⻋⻓⻔⻚⻛⻬', '母见角贝车长门页风齐')
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text).translate(radicals))


def reference_target(href, kind, maps):
    if href.startswith(('Questions.md#', 'Answers.md#', 'Questions.pdf#', 'Answers.pdf#')):
        target, key = href.split('#', 1)
        target = Path(target).stem
    elif re.fullmatch(r'#mt\d{3}', href):
        target, key = kind, href[1:]
    else:
        return None
    return (target, key) if key in maps.get(target, {}) else None


def expected_references(soup, kind, maps):
    for anchor in soup.select('a[href]'):
        target = reference_target(anchor['href'], kind, maps)
        if target is None:
            continue
        book, key = target
        label = '本册' if book == kind else ('题目册' if book == 'Questions' else '答案册')
        yield {'target': book, 'key': key, 'page': maps[book][key],
               'text': compact(anchor.get_text() + f'（{label}第{maps[book][key]}页）')}


def validate_catalog(root, index, source_dir=None):
    """Validate public metadata; verify original bytes only with an explicit archive directory."""
    catalog = json.loads((root / 'SourceCatalog.json').read_text())
    files = catalog['files']
    required = {'id', 'sha256', 'suffix', 'bytes', 'logical_papers', 'role', 'title'}
    allowed = required | {'pages'}
    ids = set()
    for item in files:
        assert required <= item.keys() and item.keys() <= allowed, ('source metadata fields', item['id'])
        assert re.fullmatch(r'S\d{3}', item['id']) and item['id'] not in ids, item['id']
        ids.add(item['id'])
        assert re.fullmatch(r'[a-f0-9]{64}', item['sha256']), item['id']
        assert re.fullmatch(r'\.[a-z0-9]+', item['suffix']), item['id']
        assert isinstance(item['bytes'], int) and item['bytes'] > 0, item['id']
        assert isinstance(item['logical_papers'], list), item['id']
        assert item['role'] and item['title'], item['id']
        if 'pages' in item:
            assert isinstance(item['pages'], int) and item['pages'] > 0, item['id']
    for paper in index['papers']:
        assert set(paper['source_ids'] + paper['answer_source_ids']) <= ids, paper['id']
    for question in index['questions']:
        for occurrence in question['occurrences']:
            assert occurrence['source_id'] in ids, (question['id'], occurrence['source_id'])
    verified = 0
    if source_dir is not None:
        archive = Path(source_dir).resolve()
        assert archive.is_dir(), 'External source directory does not exist'
        for item in files:
            path = archive / (item['id'] + item['suffix'])
            assert path.is_file(), f'Missing original source: {path.name}'
            assert path.stat().st_size == item['bytes'] and sha256(path) == item['sha256'], item['id']
            if item['suffix'] == '.pdf' and 'pages' in item:
                from pypdf import PdfReader
                assert len(PdfReader(path).pages) == item['pages'], item['id']
            verified += 1
    return {'source_metadata_entries_checked': len(files), 'source_hashes_verified': verified,
            'source_archive_verification': 'verified' if source_dir is not None else 'not_requested'}
