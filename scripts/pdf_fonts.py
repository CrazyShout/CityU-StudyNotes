"""Make native TeX PDFs independent of a reader's optional CJK language packs."""
from pathlib import Path
import hashlib
import json

from pypdf.generic import DecodedStreamObject, NameObject

RESOURCE = Path(__file__).resolve().parents[1] / 'latex/vendor/adobe-mapping'


def fonts(pdf):
    """Yield shared fonts once, including fonts inside imported figure forms."""
    seen_resources, seen_fonts = set(), set()

    def walk(resources):
        resources = resources.get_object()
        if id(resources) in seen_resources:
            return
        seen_resources.add(id(resources))
        font_dict = resources['/Font'] if '/Font' in resources else {}
        for ref in font_dict.values():
            font = ref.get_object()
            if id(font) not in seen_fonts:
                seen_fonts.add(id(font))
                yield font
        xobjects = resources['/XObject'] if '/XObject' in resources else {}
        for ref in xobjects.values():
            obj = ref.get_object()
            if '/Resources' in obj:
                yield from walk(obj['/Resources'])

    for page in pdf.pages:
        yield from walk(page['/Resources'])


def embed_cjk_unicode(writer):
    """Embed Adobe's exact CID-to-Unicode map without altering text or outlines.

    XeTeX omits ToUnicode for registered Adobe-GB1 fonts such as Fandol.
    Some readers then discard these fonts when their external CMap data is
    absent. The embedded map works with the existing Identity-H/CID encoding.
    """
    data = (RESOURCE / 'Adobe-GB1-UCS2').read_bytes()
    expected = json.loads((RESOURCE / 'UPSTREAM.json').read_text())['sha256']
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('Adobe mapping resource differs from its pinned source')
    mapping = None
    count = 0
    for font in fonts(writer):
        if font.get('/Subtype') != '/Type0' or '/ToUnicode' in font:
            continue
        descendant = font['/DescendantFonts'][0].get_object()
        cid = descendant['/CIDSystemInfo']
        if (cid.get('/Registry'), cid.get('/Ordering')) != ('Adobe', 'GB1') or cid.get('/Supplement', 0) > 5 or font.get('/Encoding') != '/Identity-H':
            raise ValueError(f"No pinned Unicode mapping for {font.get('/BaseFont')}")
        if mapping is None:
            stream = DecodedStreamObject()
            stream.set_data(data)
            mapping = writer._add_object(stream.flate_encode())
        font[NameObject('/ToUnicode')] = mapping
        count += 1
    check_unicode_fonts(writer)
    return count


def check_unicode_fonts(pdf):
    """Reject composite fonts that depend on the viewer's fonts or CMaps."""
    count = 0
    for font in fonts(pdf):
        if font.get('/Subtype') != '/Type0':
            continue
        name = font.get('/BaseFont')
        if '/ToUnicode' not in font or b'beginbf' not in font['/ToUnicode'].get_data():
            raise ValueError(f'Missing embedded Unicode mapping: {name}')
        for ref in font['/DescendantFonts']:
            descendant = ref.get_object()
            descriptor = descendant['/FontDescriptor'] if '/FontDescriptor' in descendant else {}
            if not any(k in descriptor for k in ['/FontFile', '/FontFile2', '/FontFile3']):
                raise ValueError(f'Font is not embedded: {name}')
        count += 1
    return count
