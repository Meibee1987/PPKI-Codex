from io import BytesIO
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

from core.audit import audit_docx, PAGE_RULES, certain_font, is_chapter_candidate
from core.rules import filter_rules


VALUES = {"PPKI-LAY-017": ("line_spacing", 1.0),
          "PPKI-LAY-018": ("first_line_indent", Cm(1)),
          "PPKI-LAY-019": ("alignment", WD_ALIGN_PARAGRAPH.JUSTIFY)}
NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
PAGE_CODES = {spec[0]: (spec[2], spec[3]) for spec in PAGE_RULES.values()}
FONT_CODE = "PPKI-LAY-005"
SYMBOL_FONTS = ("symbol", "wingdings", "webdings", "dingbats")
HEADING_CODES = {"PPKI-HDG-003", "PPKI-HDG-004", "PPKI-HDG-006"}


def heading_targets(paragraph):
    """Return title offsets per plain text node; reject ambiguous or expanding case mappings."""
    import re
    from docx.oxml.ns import qn
    if not is_chapter_candidate(paragraph):
        return None
    match = re.fullmatch(r"\s*BAB\s+[IVXLCDM]+\s+(.+?)\s*", paragraph.text, flags=re.IGNORECASE | re.DOTALL)
    if not match or any(not c.isascii() for c in match.group(1)):
        return None
    if any(c.tag not in (qn("w:pPr"), qn("w:r"), qn("w:bookmarkStart"), qn("w:bookmarkEnd")) for c in paragraph._p):
        return None
    targets, offset = [], 0
    for run_index, run in enumerate(paragraph.runs):
        if any(c.tag not in (qn("w:rPr"), qn("w:t")) for c in run._r):
            return None
        nodes = run._r.findall(qn("w:t"))
        for text_index, node in enumerate(nodes):
            text = node.text or ""
            start, end = max(0, match.start(1) - offset), min(len(text), match.end(1) - offset)
            if start < end:
                targets.append((run_index, text_index, start, end))
            offset += len(text)
    return targets if targets and offset == len(paragraph.text) else None


def font_targets(paragraph, expected):
    """Return changed run indexes and properties, or None for ambiguous paragraphs."""
    from docx.oxml.ns import qn
    if any(child.tag not in (qn("w:pPr"), qn("w:r")) for child in paragraph._p):
        return None
    expected_name, amount, unit = expected.rsplit(" ", 2)
    if unit != "pt":
        return None
    size = float(amount)
    targets = []
    for index, run in enumerate(paragraph.runs):
        if any(child.tag not in (qn("w:rPr"), qn("w:t")) for child in run._r):
            return None
        if not run.text.strip():
            continue
        name, actual_size = certain_font(run, paragraph)
        if name is None or actual_size is None or any(token in name.casefold() for token in SYMBOL_FONTS):
            return None
        fields = set()
        if name.casefold() != expected_name.casefold():
            fields.add("name")
        if actual_size != size:
            fields.add("size")
        if fields:
            targets.append((index, fields))
    return targets


def section_skip_reason(section):
    from docx.enum.section import WD_ORIENT
    from docx.oxml.ns import qn
    if section.orientation == WD_ORIENT.LANDSCAPE:
        return "Section berorientasi landscape."
    if section.page_width is not None and section.page_height is not None and section.page_width > section.page_height:
        return "Ukuran halaman lebih lebar daripada tinggi; orientasi perlu review."
    columns = section._sectPr.find(qn("w:cols"))
    if columns is not None:
        try:
            count = int(columns.get(qn("w:num"), "1"))
            children = list(columns)
            if any(child.tag != qn("w:col") for child in children) or (children and len(children) != count) or count < 1:
                return "Definisi kolom tidak konsisten; jumlah kolom perlu review."
            equal = columns.get(qn("w:equalWidth"), "true").lower()
            if equal not in ("true", "1", "on", "false", "0", "off"):
                return "Pengaturan lebar kolom tidak dikenal; perlu review."
            if equal in ("false", "0", "off") and not children:
                return "Lebar kolom khusus tidak didefinisikan; perlu review."
            if count > 1:
                return f"Section memiliki {count} kolom dan memerlukan review."
        except ValueError:
            return "Jumlah kolom tidak valid; perlu review."
    return None


def section_is_safe(section):
    return section_skip_reason(section) is None


def skipped_changes(data, rules, degree, findings, plan, style, confirmed, heading_only=False):
    document = Document(BytesIO(data))
    applicable, _ = filter_rules(rules, degree)
    applicable_codes = {rule["rule_code"] for rule in applicable}
    rule_by_code = {rule["rule_code"]: rule for rule in rules}
    planned = {(item["rule_code"], item["location"]) for item in plan}
    skipped = []
    for item in findings:
        code, location, status = item["rule_code"], item["location"], item["status"]
        if code not in PAGE_CODES and code not in VALUES and code != FONT_CODE and code not in HEADING_CODES:
            continue
        if status not in {"fail", "needs_review", "not_supported"} or (code, location) in planned:
            continue
        rule = rule_by_code[code]
        if heading_only and code not in HEADING_CODES:
            reason = "Di luar cakupan perbaikan heading yang dipilih."
        elif code not in applicable_codes:
            reason = f"Konteks applies_to '{rule['applies_to']}' belum dipastikan untuk {degree}."
        elif status == "not_supported":
            reason = "Validator atau mapping aturan belum didukung."
        elif status == "needs_review":
            reason = item["message"]
        elif rule["fix_mode"] != "Auto":
            reason = f"fix_mode={rule['fix_mode']}; perbaikan Auto tidak diizinkan."
        elif code in PAGE_CODES and location.startswith("section:"):
            reason = section_skip_reason(document.sections[int(location.split(":")[1]) - 1]) or "Section memerlukan review."
        elif code in HEADING_CODES:
            reason = "Judul BAB mengandung karakter non-ASCII, struktur run kompleks, atau bold yang belum pasti; perlu review."
        elif not style or not confirmed:
            reason = "Style teks isi belum dipilih dan dikonfirmasi."
        elif code == FONT_CODE and location.startswith("paragraf:"):
            reason = "Font simbol, theme, properti tidak diketahui, atau struktur run kompleks memerlukan review."
        else:
            reason = "Temuan tidak memenuhi syarat perbaikan aman."
        skipped.append({**item, "alasan_dilewati": reason})
    return skipped


def plan_changes(data, rules, degree, style, confirmed, heading_confirmed=None, heading_only=False):
    findings = audit_docx(data, rules, degree, style, confirmed, heading_confirmed)
    applicable, _ = filter_rules(rules, degree)
    allowed = {rule["rule_code"] for rule in applicable if rule["fix_mode"] == "Auto"}
    document = Document(BytesIO(data))
    result = []
    for item in findings:
        code, location = item["rule_code"], item["location"]
        if code not in allowed or item["status"] != "fail":
            continue
        if code in HEADING_CODES and location.startswith("paragraf:") and int(location.split(":")[1]) in (heading_confirmed or set()):
            paragraph = document.paragraphs[int(location.split(":")[1]) - 1]
            targets = heading_targets(paragraph)
            if not targets:
                continue
            if code == "PPKI-HDG-004" and any(paragraph.runs[r].bold is None for r, _, _, _ in targets):
                continue
            result.append(item)
            continue
        if heading_only:
            continue
        if code in VALUES and confirmed and style and location.startswith("paragraf:"):
            result.append(item)
        elif code == FONT_CODE and confirmed and style and location.startswith("paragraf:"):
            paragraph = document.paragraphs[int(location.split(":")[1]) - 1]
            if paragraph.style.style_id == style and font_targets(paragraph, item["expected"]):
                result.append(item)
        elif code in PAGE_CODES and location.startswith("section:") and section_is_safe(document.sections[int(location.split(":")[1]) - 1]):
            result.append(item)
    return result


def _document_structure(xml, changes):
    root = ET.fromstring(xml)
    body = root.find(NS + "body")
    if body is None:
        raise ValueError("Struktur badan DOCX tidak ditemukan.")
    paragraphs = body.findall(NS + "p")
    sections = []
    for child in body:
        if child.tag == NS + "p":
            ppr = child.find(NS + "pPr")
            section = ppr.find(NS + "sectPr") if ppr is not None else None
            if section is not None:
                sections.append(section)
        elif child.tag == NS + "sectPr":
            sections.append(child)
    for index, codes in changes.items():
        if isinstance(index, tuple) and index[0] == "heading_text":
            _, paragraph_index, run_index, text_index, start, end = index
            run = paragraphs[paragraph_index - 1].findall(NS + "r")[run_index]
            text = run.findall(NS + "t")[text_index]
            value = text.text or ""
            text.text = value[:start] + value[start:end].upper() + value[end:]
            continue
        if isinstance(index, tuple) and index[0] == "heading_bold":
            _, paragraph_index, run_index = index
            run = paragraphs[paragraph_index - 1].findall(NS + "r")[run_index]
            rpr = run.find(NS + "rPr")
            if rpr is not None:
                bold = rpr.find(NS + "b")
                if bold is not None:
                    rpr.remove(bold)
                if not rpr.attrib and not list(rpr):
                    run.remove(rpr)
            continue
        if isinstance(index, tuple):
            _, paragraph_index, run_index = index
            run = paragraphs[paragraph_index - 1].findall(NS + "r")[run_index]
            rpr = run.find(NS + "rPr")
            if rpr is None:
                continue
            if "name" in codes:
                fonts = rpr.find(NS + "rFonts")
                if fonts is not None:
                    for key in ("ascii", "hAnsi"):
                        fonts.attrib.pop(NS + key, None)
                    if not fonts.attrib and not list(fonts):
                        rpr.remove(fonts)
            if "size" in codes:
                size = rpr.find(NS + "sz")
                if size is not None:
                    rpr.remove(size)
            if not rpr.attrib and not list(rpr):
                run.remove(rpr)
            continue
        if isinstance(index, str):
            section = sections[int(index.split(":")[1]) - 1]
            for code in codes:
                element = section.find(NS + ("pgSz" if code == "PPKI-LAY-003" else "pgMar"))
                if element is None:
                    continue
                keys = {"PPKI-LAY-003": ("w", "h"), "PPKI-LAY-008": ("left",), "PPKI-LAY-009": ("right",), "PPKI-LAY-010": ("top",), "PPKI-LAY-011": ("bottom",)}[code]
                for key in keys:
                    element.attrib.pop(NS + key, None)
                if not element.attrib and not list(element):
                    section.remove(element)
            continue
        ppr = paragraphs[index - 1].find(NS + "pPr")
        if ppr is None:
            continue
        if "PPKI-LAY-017" in codes:
            spacing = ppr.find(NS + "spacing")
            if spacing is not None:
                for key in ("line", "lineRule"):
                    spacing.attrib.pop(NS + key, None)
                if not spacing.attrib and not list(spacing):
                    ppr.remove(spacing)
        if "PPKI-LAY-018" in codes:
            indent = ppr.find(NS + "ind")
            if indent is not None:
                for key in ("firstLine", "hanging"):
                    indent.attrib.pop(NS + key, None)
                if not indent.attrib and not list(indent):
                    ppr.remove(indent)
        if "PPKI-LAY-019" in codes or "PPKI-HDG-006" in codes:
            alignment = ppr.find(NS + "jc")
            if alignment is not None:
                ppr.remove(alignment)
        if not ppr.attrib and not list(ppr):
            paragraphs[index - 1].remove(ppr)
    def canonical(element):
        return (element.tag, tuple(sorted(element.attrib.items())), element.text, element.tail, tuple(canonical(child) for child in element))
    return canonical(root)


def format_docx(data, rules, degree, style, confirmed, heading_confirmed=None, heading_only=False):
    """Return validated copy, re-audit and applied changes; never write input."""
    changes = plan_changes(data, rules, degree, style, confirmed, heading_confirmed, heading_only)
    if not changes:
        return data, audit_docx(data, rules, degree, style, confirmed, heading_confirmed), []
    document = Document(BytesIO(data))
    changed = {}
    for item in changes:
        if item["location"].startswith("section:"):
            index = int(item["location"].split(":", 1)[1])
            section = document.sections[index - 1]
            if not section_is_safe(section):
                raise ValueError("Section tidak aman; audit ulang diperlukan.")
            attr, value = PAGE_CODES[item["rule_code"]]
            if attr is None:
                section.page_width, section.page_height = Cm(value[0]), Cm(value[1])
            else:
                setattr(section, attr, Cm(value))
            changed.setdefault(f"section:{index}", set()).add(item["rule_code"])
            continue
        index = int(item["location"].split(":", 1)[1])
        paragraph = document.paragraphs[index - 1]
        if item["rule_code"] in HEADING_CODES:
            targets = heading_targets(paragraph)
            if index not in (heading_confirmed or set()) or not targets:
                raise ValueError("Kandidat BAB tidak aman atau belum dikonfirmasi.")
            if item["rule_code"] == "PPKI-HDG-003":
                from docx.oxml.ns import qn
                for run_index, text_index, start, end in targets:
                    node = paragraph.runs[run_index]._r.findall(qn("w:t"))[text_index]
                    text = node.text or ""
                    node.text = text[:start] + text[start:end].upper() + text[end:]
                    changed[("heading_text", index, run_index, text_index, start, end)] = {"uppercase"}
            elif item["rule_code"] == "PPKI-HDG-004":
                for run_index in {target[0] for target in targets}:
                    run = paragraph.runs[run_index]
                    if run.bold is False:
                        run.bold = True
                        changed[("heading_bold", index, run_index)] = {"bold"}
            else:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                changed.setdefault(index, set()).add("PPKI-HDG-006")
            continue
        if paragraph.style.style_id != style:
            raise ValueError("Cakupan paragraf berubah; audit ulang diperlukan.")
        if item["rule_code"] == FONT_CODE:
            targets = font_targets(paragraph, item["expected"])
            if not targets:
                raise ValueError("Font tidak aman untuk diperbaiki; audit ulang diperlukan.")
            expected_name, amount, _ = item["expected"].rsplit(" ", 2)
            for run_index, fields in targets:
                run = paragraph.runs[run_index]
                if "name" in fields:
                    run.font.name = expected_name
                if "size" in fields:
                    run.font.size = Pt(float(amount))
                changed[("font", index, run_index)] = fields
            continue
        attribute, value = VALUES[item["rule_code"]]
        setattr(paragraph.paragraph_format, attribute, value)
        changed.setdefault(index, set()).add(item["rule_code"])
    output = BytesIO()
    document.save(output)
    result = output.getvalue()
    try:
        # Keep every original package part byte-for-byte; only the audited main XML changes.
        if any(item["rule_code"] in HEADING_CODES for item in changes):
            with ZipFile(BytesIO(data)) as original, ZipFile(BytesIO(result)) as generated:
                replacement = generated.read("word/document.xml")
                rebuilt = BytesIO()
                with ZipFile(rebuilt, "w") as target:
                    for info in original.infolist():
                        target.writestr(info, replacement if info.filename == "word/document.xml" else original.read(info))
                result = rebuilt.getvalue()
        with ZipFile(BytesIO(data)) as original, ZipFile(BytesIO(result)) as formatted:
            if len(original.namelist()) != len(set(original.namelist())) or set(original.namelist()) != set(formatted.namelist()):
                raise ValueError("Struktur paket DOCX berubah.")
            for name in original.namelist():
                if name != "word/document.xml" and original.read(name) != formatted.read(name):
                    raise ValueError(f"Bagian DOCX berubah di luar cakupan: {name}")
            if _document_structure(original.read("word/document.xml"), changed) != _document_structure(formatted.read("word/document.xml"), changed):
                raise ValueError("Isi atau struktur dokumen berubah di luar format yang dipilih.")
        after = audit_docx(result, rules, degree, style, confirmed, heading_confirmed)
        statuses = {(item["rule_code"], item["location"]): item["status"] for item in after}
        if any(statuses.get((item["rule_code"], item["location"])) != "pass" for item in changes):
            raise ValueError("Audit ulang tidak membuktikan semua perubahan berhasil.")
    except (ET.ParseError, KeyError, IndexError) as exc:
        raise ValueError("Validasi integritas DOCX gagal.") from exc
    return result, after, changes
