"""Local synthetic T13 fixtures; structural checks do not certify Word rendering.

Run from repository root: .venv/Scripts/python.exe -m scripts.t13_fixtures
Existing fixtures are copied and hash-verified before replacement.
"""
from datetime import datetime
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import json
import posixpath
import shutil
import struct
from urllib.parse import unquote
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import zlib

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from core.formatter import format_margins
from core.pilot import format_pilot
from core.rules import load_rules

ROOT = Path(__file__).resolve().parents[1]
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
REL = '{http://schemas.openxmlformats.org/package/2006/relationships}'
CT = '{http://schemas.openxmlformats.org/package/2006/content-types}'
NAMES = ('font_sebelum.docx', 'font_sesudah.docx',
         'margin_sebelum.docx', 'margin_sesudah.docx')


def check_png(data: bytes) -> None:
    """Check PNG chunk boundaries, CRCs and compressed raster, without Pillow."""
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('Invalid PNG signature')
    offset, kinds, compressed = 8, [], bytearray()
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError('Truncated PNG chunk')
        size = struct.unpack('>I', data[offset:offset + 4])[0]
        end = offset + 12 + size
        if end > len(data):
            raise ValueError('Truncated PNG data')
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:end - 4]
        crc = struct.unpack('>I', data[end - 4:end])[0]
        if zlib.crc32(kind + payload) & 0xffffffff != crc:
            raise ValueError(f'PNG CRC mismatch: {kind.decode("ascii")}')
        kinds.append(kind)
        if kind == b'IDAT':
            compressed.extend(payload)
        offset = end
    if not kinds or kinds[0] != b'IHDR' or kinds[-1] != b'IEND' or not compressed:
        raise ValueError('Missing required PNG chunks')
    zlib.decompress(compressed)


def check_package(data: bytes) -> None:
    """Targeted OPC/XML checks, not a full OOXML schema or Word validator."""
    with ZipFile(BytesIO(data)) as package:
        names = package.namelist()
        if len(names) != len(set(names)) or package.testzip() is not None:
            raise ValueError('Duplicate ZIP entries or invalid ZIP CRC')
        required = {'[Content_Types].xml', '_rels/.rels', 'word/document.xml',
                    'word/styles.xml', 'word/settings.xml', 'word/_rels/document.xml.rels'}
        if not required <= set(names):
            raise ValueError('Missing required fixture package parts')
        xml = {name: ET.fromstring(package.read(name)) for name in names
               if name.endswith(('.xml', '.rels'))}
        types = xml['[Content_Types].xml']
        if types.tag != CT + 'Types':
            raise ValueError('Invalid content types root')
        defaults = {e.get('Extension'): e.get('ContentType') for e in types.findall(CT + 'Default')}
        overrides = {e.get('PartName'): e.get('ContentType') for e in types.findall(CT + 'Override')}
        main_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'
        if overrides.get('/word/document.xml') != main_type:
            raise ValueError('Incorrect DOCX main content type')
        for name in names:
            if name == '[Content_Types].xml':
                continue
            if not overrides.get('/' + name, defaults.get(name.rsplit('.', 1)[-1])):
                raise ValueError(f'Missing content type: {name}')
        for name in overrides:
            if name.lstrip('/') not in names:
                raise ValueError(f'Content type target missing: {name}')
        rels = {}
        for name, tree in xml.items():
            if not name.endswith('.rels'):
                continue
            if tree.tag != REL + 'Relationships':
                raise ValueError(f'Invalid relationships root: {name}')
            base = '' if name == '_rels/.rels' else posixpath.dirname(posixpath.dirname(name))
            ids = {}
            for rel in tree:
                rid, target = rel.get('Id'), rel.get('Target')
                if not rid or rid in ids or not target or not rel.get('Type'):
                    raise ValueError(f'Invalid relationship: {name}')
                ids[rid] = rel
                if rel.get('TargetMode') == 'External':
                    raise ValueError('External relationships are not allowed in T13 fixtures')
                resolved = posixpath.normpath(posixpath.join(base, unquote(target))).lstrip('/')
                if resolved not in names:
                    raise ValueError(f'Missing relationship target: {name}: {target}')
            rels[name] = ids
        office = [r for r in rels['_rels/.rels'].values()
                  if r.get('Type') == R[1:-1] + '/officeDocument']
        if len(office) != 1 or office[0].get('Target') != 'word/document.xml':
            raise ValueError('Invalid officeDocument relationship')
        for name, tree in xml.items():
            if name.endswith('.rels'):
                continue
            rel_name = posixpath.join(posixpath.dirname(name), '_rels', posixpath.basename(name) + '.rels')
            for element in tree.iter():
                if element.tag == W + 'fldSimple' and not element.get(W + 'instr', '').strip():
                    raise ValueError(f'fldSimple missing w:instr: {name}')
                for attr, value in element.attrib.items():
                    if attr in {R + 'id', R + 'embed', R + 'link'} and value not in rels.get(rel_name, {}):
                        raise ValueError(f'Unresolved XML relationship: {name}: {value}')
        main = xml['word/document.xml']
        body = main.find(W + 'body')
        if main.tag != W + 'document' or body is None or not len(body) or body[-1].tag != W + 'sectPr':
            raise ValueError('Invalid document/body/final sectPr')
        for name in names:
            if name.endswith('.png'):
                check_png(package.read(name))


def build_font_before() -> bytes:
    doc = Document()
    defaults = doc.styles.element.find(qn('w:docDefaults'))
    ppr = defaults.find(qn('w:pPrDefault'))
    if ppr is not None:
        defaults.remove(ppr)
    doc.add_paragraph('Sampul sintetis')
    doc.add_heading('BAB I PENDAHULUAN', 1)
    p = doc.add_paragraph('Paragraf sintetis untuk pilot yang telah dikonfirmasi operator dan memiliki format yang perlu diperiksa.', style='Body Text')
    run = p.runs[0]
    run.font.name, run.font.size = 'Arial', Pt(11)
    run.bold, run.italic = True, True
    p.paragraph_format.line_spacing = 2.0
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    other = doc.add_paragraph('Paragraf sintetis lain yang tidak dikonfirmasi dan tidak boleh diubah oleh pilot ini.', style='Body Text')
    other.paragraph_format.line_spacing = 2.0
    complex_p = doc.add_paragraph('Paragraf sintetis dengan field Word.', style='Body Text')
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'), ' PAGE ')
    field.set(qn('w:fldLock'), 'true')
    result_run = OxmlElement('w:r')
    result_text = OxmlElement('w:t')
    result_text.text = '1'
    result_run.append(result_text)
    field.append(result_run)
    complex_p._p.append(field)
    doc.add_paragraph('Tabel 1 Caption sintetis', style='Caption')
    doc.add_table(rows=1, cols=1).cell(0, 0).text = 'Isi tabel sintetis'
    doc.sections[0].header.paragraphs[0].add_run('Header sintetis')
    output = BytesIO()
    doc.save(output)
    return output.getvalue()


def synthetic_png() -> bytes:
    def chunk(kind, payload):
        return struct.pack('>I', len(payload)) + kind + payload + struct.pack('>I', zlib.crc32(kind + payload) & 0xffffffff)
    # Visible 32x32 RGB square with valid per-chunk CRCs.
    raster = (b'\0' + bytes((30, 100, 180)) * 32) * 32
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 32, 32, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raster)) + chunk(b'IEND', b''))


def build_margin_before() -> bytes:
    doc = Document()
    first = doc.sections[0]
    first.page_width, first.page_height = Cm(20), Cm(28)
    first.left_margin = first.right_margin = first.top_margin = first.bottom_margin = Cm(2)
    first.header.paragraphs[0].add_run('Header sintetis')
    first.footer.paragraphs[0].add_run('Footer sintetis')
    doc.add_paragraph('Teks utama')
    table = doc.add_table(rows=1, cols=1)
    table.autofit = False
    table.columns[0].width = Cm(10)
    table.cell(0, 0).width = Cm(10)
    table.cell(0, 0).text = 'Tabel'
    doc.add_picture(BytesIO(synthetic_png()), width=Cm(1))
    second = doc.add_section(WD_SECTION_START.NEW_PAGE)
    second.page_width, second.page_height = Cm(21), Cm(29.7)
    second.left_margin = Cm(4)
    second.right_margin = second.top_margin = second.bottom_margin = Cm(3)
    output = BytesIO()
    doc.save(output)
    return output.getvalue()


def build_fixtures() -> dict[str, bytes]:
    rules = load_rules()
    font, margin = build_font_before(), build_margin_before()
    font_after, _ = format_pilot(font, rules, 'S1', {3})
    margin_after, _ = format_margins(margin, rules, 'S1')
    files = dict(zip(NAMES, (font, font_after, margin, margin_after)))
    for data in files.values():
        check_package(data)
    return files


def write_fixtures(directory: Path) -> Path:
    files = build_fixtures()  # Validate every new package before touching existing files.
    directory.mkdir(parents=True, exist_ok=True)
    backup = directory / ('backup_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    backup.mkdir()
    manifest = {}
    for name in NAMES:
        source = directory / name
        if source.exists():
            shutil.copy2(source, backup / name)
            digest = sha256(source.read_bytes()).hexdigest()
            if sha256((backup / name).read_bytes()).hexdigest() != digest:
                raise ValueError(f'Backup hash mismatch: {name}')
            manifest[name] = {'bytes': source.stat().st_size, 'sha256': digest}
    (backup / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    for name, data in files.items():
        temporary = directory / (name + '.new')
        temporary.write_bytes(data)
        check_package(temporary.read_bytes())
        temporary.replace(directory / name)
    return backup


if __name__ == '__main__':
    backup = write_fixtures(ROOT / 'private_tests' / 't13_word_validation')
    print(f'Backup: {backup}')
    for name in NAMES:
        path = backup.parent / name
        print(f'{name}: {path.stat().st_size} bytes; SHA256 {sha256(path.read_bytes()).hexdigest()}')
    print('Package checks completed; Microsoft Word opening and visual review: PENDING MANUAL REVIEW')
