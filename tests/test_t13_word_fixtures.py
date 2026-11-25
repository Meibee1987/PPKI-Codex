from hashlib import sha256
from io import BytesIO
from zipfile import ZipFile

import pytest
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.formatter import format_margins
from core.pilot import format_pilot
from core.rules import load_rules
from scripts.t13_fixtures import (
    NAMES, build_fixtures, check_package, check_png, synthetic_png, write_fixtures,
)


@pytest.fixture(scope="module")
def fixtures():
    return build_fixtures()


def replace_part(data, name, replacement):
    stream = BytesIO()
    with ZipFile(BytesIO(data)) as source, ZipFile(stream, "w") as target:
        for item in source.infolist():
            if item.filename != name or replacement is not None:
                target.writestr(item, replacement if item.filename == name else source.read(item))
    return stream.getvalue()


@pytest.mark.parametrize("name", NAMES)
def test_fixture_package_structure(fixtures, name):
    check_package(fixtures[name])


@pytest.mark.parametrize("pair", ["font", "margin"])
def test_content_preserved_and_second_pass_is_identical(fixtures, pair):
    before = fixtures[pair + "_sebelum.docx"]
    after = fixtures[pair + "_sesudah.docx"]
    first, second = Document(BytesIO(before)), Document(BytesIO(after))
    assert [p.text for p in first.paragraphs] == [p.text for p in second.paragraphs]
    assert [t._tbl.xml for t in first.tables] == [t._tbl.xml for t in second.tables]
    assert len(first.inline_shapes) == len(second.inline_shapes) == (1 if pair == "margin" else 0)
    with ZipFile(BytesIO(before)) as old, ZipFile(BytesIO(after)) as new:
        assert old.namelist() == new.namelist()
        assert all(old.read(n) == new.read(n) for n in old.namelist() if n != "word/document.xml")
    if pair == "font":
        p = second.paragraphs[2]
        assert first.paragraphs[2].runs[0].font.name == "Arial"
        assert first.paragraphs[2].runs[0].font.size.pt == 11
        assert p.runs[0].font.name == "Times New Roman" and p.runs[0].font.size.pt == 12
        assert p.runs[0].bold and p.runs[0].italic
        assert p.paragraph_format.line_spacing == 1
        assert abs(p.paragraph_format.first_line_indent.cm - 1) < .02
        assert p.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY
        assert first.paragraphs[4]._p.xml == second.paragraphs[4]._p.xml
        again, _ = format_pilot(after, load_rules(), "S1", {3})
    else:
        for attr, expected in (("left_margin", 4), ("right_margin", 3), ("top_margin", 3), ("bottom_margin", 3)):
            assert abs(getattr(first.sections[0], attr).cm - 2) < .02
            assert abs(getattr(second.sections[0], attr).cm - expected) < .02
        assert len(second.sections) == 2
        again, report = format_margins(after, load_rules(), "S1")
        assert not any(row["status"] == "applied" for row in report)
    assert again == after


@pytest.mark.parametrize("part,old,new,match", [
    ("word/document.xml", b'w:instr=" PAGE "', b'', "fldSimple missing"),
    ("word/document.xml", b'r:id="rId9"', b'r:id="unknown"', "Unresolved XML relationship"),
    ("_rels/.rels", b'Target="word/document.xml"', b'Target="word/missing.xml"', "Missing relationship target"),
    ("word/_rels/document.xml.rels", b'Id="rId9"', b'Id="rId3"', "Invalid relationship"),
    ("[Content_Types].xml", b'wordprocessingml.document.main+xml', b'wordprocessingml.template.main+xml', "Incorrect DOCX"),
    ("word/document.xml", b'</w:document>', b'', None),
])
def test_reject_broken_xml_and_opc(fixtures, part, old, new, match):
    data = fixtures["font_sebelum.docx"]
    with ZipFile(BytesIO(data)) as source:
        original = source.read(part)
    assert old in original
    broken = replace_part(data, part, original.replace(old, new, 1))
    from xml.etree.ElementTree import ParseError
    with pytest.raises((ValueError, ParseError), match=match):
        check_package(broken)


def test_reject_missing_package_part(fixtures):
    with pytest.raises(ValueError, match="Missing required"):
        check_package(replace_part(fixtures["font_sebelum.docx"], "word/settings.xml", None))


def test_reject_png_with_bad_internal_crc_even_with_good_zip_crc(fixtures):
    png = synthetic_png()
    check_png(png)
    corrupt = bytearray(png)
    corrupt[png.index(b"IDAT") + 4] ^= 1
    with pytest.raises(ValueError, match="PNG CRC mismatch"):
        check_png(bytes(corrupt))
    data = fixtures["margin_sebelum.docx"]
    with ZipFile(BytesIO(data)) as package:
        name = next(n for n in package.namelist() if n.endswith(".png"))
    broken = replace_part(data, name, bytes(corrupt))
    with ZipFile(BytesIO(broken)) as package:
        assert package.testzip() is None
    with pytest.raises(ValueError, match="PNG CRC mismatch"):
        check_package(broken)


def test_backup_preserves_every_previous_file_before_replacement(tmp_path):
    previous = {name: ("old diagnosis " + name).encode() for name in NAMES}
    for name, data in previous.items():
        (tmp_path / name).write_bytes(data)
    backup = write_fixtures(tmp_path)
    import json
    manifest = json.loads((backup / "manifest.json").read_text())
    for name, data in previous.items():
        assert (backup / name).read_bytes() == data
        assert manifest[name]["sha256"] == sha256(data).hexdigest()
        check_package((tmp_path / name).read_bytes())
