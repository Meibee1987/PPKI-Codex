"""Read-only image-width preflight against an explicit formatter plan.

PASS is limited to simple inline width, never Word pagination/layout acceptance.
No image, package part, rule or file is written by this module.
"""
from io import BytesIO
import re
from zipfile import ZipFile

from docx import Document
from docx.shared import Cm
from docx.oxml import parse_xml
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

from core.audit import PAGE_RULES, paragraph_value, validate_docx_input


HORIZONTAL_CODES = {"PPKI-LAY-003", "PPKI-LAY-008", "PPKI-LAY-009"}
PAGE_SPECS = {spec[0]: spec for spec in PAGE_RULES.values()}
EMU_PER_CM = 360000


def _cm(value):
    return round(value / EMU_PER_CM, 6) if value is not None else None


def _section_geometry(document, changes):
    sections = []
    for number, section in enumerate(document.sections, 1):
        current = {key: getattr(section, key) for key in
                   ("page_width", "page_height", "left_margin", "right_margin", "top_margin", "bottom_margin")}
        planned = dict(current)
        horizontal = False
        for change in changes:
            if change["location"] != f"section:{number}" or change["rule_code"] not in PAGE_SPECS:
                continue
            code = change["rule_code"]
            _, expected, attribute, target = PAGE_SPECS[code]
            if change["expected"] != expected:
                raise ValueError("Target rencana halaman tidak cocok dengan mapping yang didukung.")
            if attribute is None:
                planned.update(page_width=Cm(target[0]).twips * 635, page_height=Cm(target[1]).twips * 635)
            else:
                planned[attribute] = Cm(target).twips * 635
            horizontal |= code in HORIZONTAL_CODES
        reasons = []
        if any(planned[k] is None or planned[k] < 0 for k in planned) or not planned["page_width"] or not planned["page_height"]:
            reasons.append("Ukuran halaman/margin tidak lengkap atau tidak valid.")
        if section.gutter:
            reasons.append("Gutter: posisi bidang tulisan memerlukan review.")
        if document.settings.element.xpath('./w:mirrorMargins[not(@w:val="0" or @w:val="false" or @w:val="off")]'):
            reasons.append("Mirror margins: bidang tulisan bergantung halaman Word.")
        if section.start_type == 0:
            reasons.append("Section continuous dapat berbagi halaman.")
        cols = section._sectPr.find(qn("w:cols"))
        if cols is not None and (cols.get(qn("w:num"), "1") != "1" or len(cols) or cols.get(qn("w:equalWidth"), "1").lower() in {"0", "false", "off"}):
            reasons.append("Kolom khusus: bidang gambar tidak dapat dipastikan.")
        if section._sectPr.xpath('./w:pgBorders | ./w:textDirection | ./w:rtlGutter | ./w:sectPrChange'):
            reasons.append("Pengaturan section khusus memerlukan layout Word.")
        def width(values):
            keys = ("page_width", "left_margin", "right_margin")
            return values[keys[0]] - values[keys[1]] - values[keys[2]] if all(values[k] is not None for k in keys) else None
        text_width = width(planned)
        if text_width is not None and text_width <= 0:
            reasons.append("Bidang tulisan setelah rencana tidak positif.")
        sections.append({"section": number, "current": current, "planned": planned,
                         "current_width": width(current), "text_width": text_width,
                         "horizontal_change_planned": horizontal, "reasons": reasons})
    return sections


def _paragraph_width(paragraph, document, field_width):
    """Only a single picture on its own line with ordinary nonnegative indents."""
    reasons = []
    if paragraph is None:
        return None, ["Konteks paragraf gambar tidak diketahui."]
    if paragraph.text.strip() or paragraph._p.xpath('.//w:tab | .//w:br | .//w:fldChar | .//w:fldSimple | .//w:instrText | .//w:numPr'):
        reasons.append("Gambar bercampur teks/tab/field/daftar; posisi memerlukan Word.")
    if len(list(paragraph._p.iter(qn("wp:inline")))) != 1:
        reasons.append("Beberapa objek dalam paragraf; posisi baris belum pasti.")
    sources = [paragraph._p.pPr]
    style, seen = paragraph.style, set()
    while style is not None and style.style_id not in seen:
        seen.add(style.style_id)
        sources.append(style.element.pPr)
        style = style.base_style
    sources.extend(document.styles.element.xpath('./w:docDefaults/w:pPrDefault/w:pPr'))
    for source in sources:
        if source is None:
            continue
        if source.xpath('./w:numPr | ./w:tabs | ./w:bidi | ./w:mirrorIndents | ./w:framePr | ./w:textDirection | ./w:pPrChange'):
            reasons.append("Properti paragraf/style memerlukan layout Word.")
        ind = source.find(qn("w:ind"))
        if ind is not None and any(key not in {qn("w:left"), qn("w:right"), qn("w:firstLine"), qn("w:hanging")} for key in ind.attrib):
            reasons.append("Indentasi karakter/logis tidak dapat diukur pasti.")
    values = [paragraph_value(paragraph, name, include_defaults=True) or 0
              for name in ("left_indent", "right_indent", "first_line_indent")]
    left, right, first = values
    if left < 0 or right < 0 or first != 0:
        reasons.append("Indentasi negatif/baris pertama memerlukan review posisi.")
    alignment = paragraph_value(paragraph, "alignment", include_defaults=True)
    if alignment not in (None, 0, 1, 2):
        reasons.append("Alignment khusus memerlukan layout Word.")
    available = field_width - left - right if field_width is not None else None
    if available is not None and available <= 0:
        reasons.append("Bidang paragraf tidak positif.")
    return available, reasons


def image_preflight(data: bytes, planned_changes: list[dict] | None = None,
                    *, max_bytes: int = 20 * 1024 * 1024) -> dict:
    """Return deterministic dimensions/risks, without text excerpts or package changes.

    planned_changes uses the existing formatter's location/rule_code/expected rows.
    Omitting the plan checks current dimensions; it never invents margin targets.
    """
    validate_docx_input(data, "input.docx", max_bytes)
    document = Document(BytesIO(data))
    sections = _section_geometry(document, planned_changes or [])
    body = document.element.body
    direct_sections = body.xpath('./w:p/w:pPr/w:sectPr | ./w:sectPr')
    known = len(direct_sections) == len(document.sections) == len(list(body.iter(qn("w:sectPr")))) and len(body.findall(qn("w:sectPr"))) == 1
    block_sections, number = {}, 1
    for block in body:
        block_sections[block] = number if known else None
        if block.tag == qn("w:p") and block.find('./' + qn("w:pPr") + '/' + qn("w:sectPr")) is not None:
            number += 1
    direct_paragraphs = {p._p: i for i, p in enumerate(document.paragraphs, 1)}
    rows = []

    def inspect(root, part_name, body_story=False):
        parents = {child: parent for parent in root.iter() for child in parent}
        objects = [node for node in root.iter() if node.tag in {qn("wp:inline"), qn("wp:anchor"), qn("w:pict")}]
        for index, obj in enumerate(objects, 1):
            ancestors, node = [], obj
            while node in parents:
                node = parents[node]
                ancestors.append(node)
            paragraph_node = next((a for a in ancestors if a.tag == qn("w:p")), None)
            block = next((a for a in ancestors if a in block_sections), None) if body_story else None
            section_number = block_sections.get(block) if block is not None else None
            section = sections[section_number - 1] if section_number is not None else None
            location = (f"paragraf:{direct_paragraphs[paragraph_node]}" if paragraph_node in direct_paragraphs else f"{part_name}/gambar:{index}")
            if any(a.tag == qn("w:tc") for a in ancestors):
                location += "/tabel"
            kind = obj.tag.split("}")[-1]
            reasons = list(section["reasons"]) if section else ["Section gambar tidak dapat dipetakan pasti; periksa story/section di Word."]
            if not body_story:
                reasons.append("Gambar di header/footer/catatan: posisi terhadap bidang isi perlu review Word.")
            if any(a.tag in {qn("w:tc"), qn("w:txbxContent")} for a in ancestors):
                reasons.append("Gambar dalam tabel/textbox; lebar sel/konteks tidak dipastikan.")
            if kind == "inline" and len(list(obj.iter(qn("pic:pic")))) != 1:
                reasons.append("Drawing bukan satu gambar inline biasa; perlu review.")
            if kind != "inline":
                reasons.append("Gambar floating/anchored atau VML; posisi/wrapping memerlukan Word.")
            if body_story and block is not None and block.tag not in {qn("w:p"), qn("w:tbl")}:
                reasons.append("Gambar dalam kontainer body khusus memerlukan review.")
            extent = obj.find(qn("wp:extent"))
            try:
                image_width = int(extent.get("cx")) if extent is not None else None
                if image_width is not None and image_width <= 0:
                    image_width = None
            except (ValueError, TypeError):
                image_width = None
            if image_width is None:
                reasons.append("Lebar gambar tidak tersedia/valid pada extent DOCX.")
            transforms = list(obj.iter(qn("a:xfrm")))
            if any(any(k in transform.attrib and transform.get(k) not in {"0", "false", "off"} for k in ("rot", "flipH", "flipV")) for transform in transforms):
                reasons.append("Transformasi/rotasi gambar memerlukan review batas tampilan.")
            effect = obj.find(qn("wp:effectExtent"))
            if (effect is not None and any(value != "0" for value in effect.attrib.values())) or any(obj.get(k, "0") != "0" for k in ("distL", "distR")):
                reasons.append("Efek/jarak gambar dapat memperlebar batas tampilan.")
            field_width = section["text_width"] if section else None
            paragraph = Paragraph(paragraph_node, document._body) if paragraph_node is not None and body_story else None
            available, paragraph_reasons = _paragraph_width(paragraph, document, field_width)
            reasons.extend(paragraph_reasons)
            if reasons:
                # Do not report a page-width calculation as a known table-cell/anchor position.
                available = None
            delta = image_width - available if image_width is not None and available is not None else None
            # One twip (635 EMU) accounts only for stored page-margin rounding, not layout uncertainty.
            if delta is not None and delta > 635:
                reasons.append("Lebar gambar melebihi bidang paragraf setelah rencana margin; potensi overflow.")
            reasons = list(dict.fromkeys(reasons))
            rows.append({"image": len(rows) + 1, "location": location, "section": section_number,
                         "part": part_name, "kind": kind,
                         "image_width_cm": _cm(image_width), "text_width_before_cm": _cm(section["current_width"]) if section else None,
                         "text_width_after_cm": _cm(field_width), "available_width_cm": _cm(available),
                         "difference_cm": _cm(delta), "potential_width_overflow": None if delta is None else delta > 635,
                         "status": "NEEDS_REVIEW" if reasons else "PASS",
                         "reason": " ".join(reasons) if reasons else "Tidak ditemukan pelanggaran lebar pada gambar inline sederhana; bukan validasi seluruh layout Word."})
    inspect(body, "word/document.xml", True)
    with ZipFile(BytesIO(data)) as archive:
        for name in sorted(archive.namelist()):
            if re.fullmatch(r"word/(?:header[^/]*|footer[^/]*|footnotes|endnotes)\.xml", name):
                inspect(parse_xml(archive.read(name)), name)
    review = [row for row in rows if row["status"] == "NEEDS_REVIEW"]
    unknown_section = any(row["section"] is None for row in review)
    risky_sections = {row["section"] for row in review if row["section"] is not None}
    if unknown_section:
        risky_sections.update(range(1, len(sections) + 1))
    return {"status": "NOT_APPLICABLE" if not rows else "NEEDS_REVIEW" if review else "PASS",
            "images_checked": len(rows), "images_needing_review": len(review), "images": rows,
            "sections": [{"section": s["section"], "current_cm": {k: _cm(v) for k, v in s["current"].items()},
                          "planned_cm": {k: _cm(v) for k, v in s["planned"].items()},
                          "text_width_before_cm": _cm(s["current_width"]), "text_width_after_cm": _cm(s["text_width"]),
                          "horizontal_change_planned": s["horizontal_change_planned"], "reasons": s["reasons"]} for s in sections],
            "review_sections": sorted(s for s in risky_sections if sections[s - 1]["horizontal_change_planned"]),
            "measurement": "DOCX structural width only; no Word layout engine used",
            "advice": "Periksa posisi gambar, bidang tulisan, caption dan clipping di Microsoft Word sebelum menerima hasil."}


def reviewed_changes(changes: list[dict], report: dict, reviewed_sections=()) -> list[dict]:
    """Hold only horizontal page operations in risky sections lacking explicit review."""
    held = set(report["review_sections"]) - set(reviewed_sections)
    return [row for row in changes if not (row["rule_code"] in HORIZONTAL_CODES
            and row["location"] in {f"section:{n}" for n in held})]
