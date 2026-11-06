from collections import Counter
from io import BytesIO
from zipfile import BadZipFile

from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.rules import filter_rules


# Nilai ini adalah mapping eksplisit dari snapshot PPKI, bukan parser bebas teks pedoman.
PAGE_RULES = {
    "section.page-size-a4": ("PPKI-LAY-003", "A4 / 21.0 × 29.7 cm", None, (21.0, 29.7)),
    "section.margin-left-4cm": ("PPKI-LAY-008", "4 cm", "left_margin", 4.0),
    "section.margin-right-3cm": ("PPKI-LAY-009", "3 cm", "right_margin", 3.0),
    "section.margin-top-3cm": ("PPKI-LAY-010", "3 cm", "top_margin", 3.0),
    "section.margin-bottom-3cm": ("PPKI-LAY-011", "3 cm", "bottom_margin", 3.0),
}

PARAGRAPH_RULES = {
    "body.line-spacing-single": ("PPKI-LAY-017", "Single / 1.0", "line_spacing"),
    "body.first-line-indent-1cm": ("PPKI-LAY-018", "1 cm", "first_line_indent"),
    "body.justified": ("PPKI-LAY-019", "Justified", "alignment"),
}


def finding(rule, status, location, actual, message):
    return {
        "rule_code": rule["rule_code"], "severity": rule["severity"],
        "source_section": rule["source_section"], "pdf_page": rule["pdf_page"],
        "printed_page": rule["printed_page"], "status": status,
        "location": location, "actual": actual,
        "expected": rule["expected_value_pattern"], "message": message,
    }


def declared_font(run, paragraph):
    """Return declared font values, not a guarantee of Word's rendered font."""
    name, size = run.font.name, run.font.size
    for initial in (run.style, paragraph.style):
        style = initial
        visited = set()
        while style is not None and style.style_id not in visited:
            visited.add(style.style_id)
            if name is None:
                name = style.font.name
            if size is None:
                size = style.font.size
            style = style.base_style
    return name, size.pt if size is not None else None


def font_candidates(data):
    try:
        document = Document(BytesIO(data))
    except (PackageNotFoundError, BadZipFile, KeyError, ValueError, OSError) as exc:
        raise ValueError("DOCX tidak dapat dibuka; pastikan file DOCX valid dan tidak rusak.") from exc
    styles = {}
    for index, paragraph in enumerate(document.paragraphs, 1):
        if paragraph.text.strip():
            key = paragraph.style.style_id
            entry = styles.setdefault(key, {"name": paragraph.style.name, "paragraphs": []})
            entry["paragraphs"].append((index, paragraph.text))
    return styles


def certain_font(run, paragraph):
    # Hanya teks Latin sederhana; theme, karakter khusus, dan format kompleks direview.
    if not run.text.isascii():
        return None, None
    styles = []
    rpr = run._r.rPr
    if rpr is not None and rpr.rStyle is not None:
        styles.append(run.style)
    styles.append(paragraph.style)
    sources = [(run.font, rpr)]
    for style in styles:
        seen = set()
        while style is not None and style.style_id not in seen:
            seen.add(style.style_id)
            sources.append((style.font, style.element.rPr))
            style = style.base_style
    name = size = None
    name_blocked = False
    for font, properties in sources:
        if name is None and not name_blocked and properties is not None:
            fonts = properties.rFonts
            if fonts is not None:
                if any(fonts.get(qn('w:' + k)) is not None for k in ('asciiTheme', 'hAnsiTheme')):
                    name_blocked = True
                else:
                    ascii_name, ansi_name = fonts.get(qn('w:ascii')), fonts.get(qn('w:hAnsi'))
                    if ascii_name and ascii_name == ansi_name:
                        name = ascii_name
                    elif ascii_name or ansi_name:
                        name_blocked = True
        if size is None and font.size is not None:
            size = font.size.pt
    return name, size


def font_findings(document, rule, body_style=None, confirmed=False):
    """Inspect declared values for candidate body styles; context remains uncertain."""
    results = []
    if body_style is not None:
        for index, paragraph in enumerate(document.paragraphs, 1):
            if paragraph.style.style_id != body_style or not paragraph.text.strip():
                continue
            location = f"paragraf:{index}"
            simple = all(child.tag in (qn('w:pPr'), qn('w:r')) for child in paragraph._p)
            simple = simple and all(all(child.tag in (qn('w:rPr'), qn('w:t')) for child in run._r) for run in paragraph.runs)
            if not confirmed or not simple or not paragraph.runs:
                results.append(finding(rule, "needs_review", location, "Tidak dapat diverifikasi", "Konfirmasi cakupan atau pemeriksaan struktur manual diperlukan."))
                continue
            values = [certain_font(run, paragraph) for run in paragraph.runs if run.text.strip()]
            actual = "; ".join(f"{name or 'tidak diketahui'} / {f'{size:g} pt' if size is not None else 'ukuran tidak diketahui'}" for name, size in values)
            expected_name, expected_size = rule["expected_value_pattern"].rsplit(" ", 2)[0], float(rule["expected_value_pattern"].rsplit(" ", 2)[1])
            wrong = any((name is not None and name.casefold() != expected_name.casefold()) or (size is not None and size != expected_size) for name, size in values)
            unknown = not values or any(name is None or size is None or any(token in name.casefold() for token in ("symbol", "wingdings", "webdings", "dingbats")) for name, size in values)
            status = "needs_review" if unknown else "fail" if wrong else "pass"
            results.append(finding(rule, status, location, actual or "Tidak dapat diverifikasi", "Pemeriksaan terbatas pada kandidat yang dikonfirmasi; font simbol, theme, atau nilai tidak diketahui memerlukan review."))
        if not results:
            results.append(finding(rule, "needs_review", "dokumen", "Tidak dapat diverifikasi", "Tidak ada paragraf kandidat untuk style yang dipilih."))
        return results
    for index, paragraph in enumerate(document.paragraphs, 1):
        if not paragraph.text.strip():
            continue
        location = f"paragraf:{index}"
        if paragraph.style.style_id != "BodyText":
            results.append(finding(rule, "needs_review", location, "Tidak diperiksa", "Konteks paragraf belum dapat dipastikan sebagai teks isi utama."))
            continue
        if not paragraph.runs or "".join(run.text for run in paragraph.runs) != paragraph.text:
            results.append(finding(rule, "needs_review", location, "Tidak dapat diverifikasi", "Struktur paragraf kompleks; periksa manual."))
            continue
        declarations = []
        for run in paragraph.runs:
            if not run.text.strip():
                continue
            name, size = declared_font(run, paragraph)
            declarations.append(f"{name or 'tidak diketahui'} / {f'{size:g} pt' if size is not None else 'ukuran tidak diketahui'}")
        actual = "; ".join(declarations) if declarations else "Tidak dapat diverifikasi"
        results.append(finding(rule, "needs_review", location, actual, "Deklarasi font kandidat Body Text; konteks isi dan font efektif Word belum dapat dipastikan. Periksa manual."))
    if not results:
        results.append(finding(rule, "needs_review", "dokumen", "Tidak dapat diverifikasi", "Tidak ditemukan paragraf yang dapat diperiksa."))
    return results


def paragraph_value(paragraph, attribute):
    """Resolve explicit paragraph and paragraph-style properties, not document defaults."""
    value = getattr(paragraph.paragraph_format, attribute)
    if value is not None:
        return value
    style = paragraph.style
    seen = set()
    while style is not None and style.style_id not in seen:
        seen.add(style.style_id)
        value = getattr(style.paragraph_format, attribute)
        if value is not None:
            return value
        style = style.base_style
    return None


def paragraph_findings(document, rule, attribute, body_style, confirmed):
    results = []
    if not body_style or not confirmed:
        return [finding(rule, "needs_review", "dokumen", "Tidak diperiksa", "Pilih dan konfirmasi cakupan teks isi terlebih dahulu.")]
    for index, paragraph in enumerate(document.paragraphs, 1):
        if paragraph.style.style_id != body_style or not paragraph.text.strip():
            continue
        location = f"paragraf:{index}"
        simple = all(child.tag in (qn("w:pPr"), qn("w:r")) for child in paragraph._p)
        simple = simple and all(all(child.tag in (qn("w:rPr"), qn("w:t")) for child in run._r) for run in paragraph.runs)
        # Daftar dan format paragraf karakter-unit dapat mengubah arti indentasi.
        properties = [paragraph._p.pPr]
        style, seen = paragraph.style, set()
        while style is not None and style.style_id not in seen:
            seen.add(style.style_id)
            properties.append(style.element.pPr)
            style = style.base_style
        uncertain = False
        for ppr in properties:
            if ppr is None:
                continue
            indent = ppr.find(qn("w:ind"))
            if ppr.find(qn("w:numPr")) is not None or (indent is not None and any(indent.get(qn("w:" + key)) is not None for key in ("firstLineChars", "hangingChars"))):
                uncertain = True
            spacing = ppr.find(qn("w:spacing"))
            if attribute == "line_spacing" and spacing is not None and spacing.get(qn("w:lineRule")) is not None and spacing.get(qn("w:line")) is None:
                uncertain = True
        if not simple or uncertain:
            results.append(finding(rule, "needs_review", location, "Tidak dapat diverifikasi", "Struktur kompleks atau daftar perlu review manual."))
            continue
        value = paragraph_value(paragraph, attribute)
        if value is None:
            results.append(finding(rule, "needs_review", location, "Tidak diketahui", "Properti eksplisit tidak ditemukan; default dokumen perlu review."))
            continue
        if attribute == "line_spacing":
            if not isinstance(value, float):
                results.append(finding(rule, "needs_review", location, f"{value.pt:g} pt", "Spasi tinggi tetap atau minimum perlu review manual."))
                continue
            actual, matches = f"{value:g}", abs(value - 1.0) < 0.001
        elif attribute == "first_line_indent":
            actual, matches = f"{value.cm:.2f} cm", abs(value.cm - 1.0) <= 0.02
        else:
            actual, matches = str(value), value == WD_ALIGN_PARAGRAPH.JUSTIFY
        item = finding(rule, "pass" if matches else "fail", location, actual, "Properti sesuai." if matches else "Properti tidak sesuai.")
        if not matches and rule["fix_mode"] == "Auto":
            item["proposed_change"] = f"Usulan saja: {rule['expected_value_pattern']} (belum diterapkan)"
        results.append(item)
    if not results:
        results.append(finding(rule, "needs_review", "dokumen", "Tidak diperiksa", "Tidak ada paragraf kandidat pada style yang dipilih."))
    return results


def audit_docx(data: bytes, rules: list[dict], degree: str, body_style: str | None = None, confirmed: bool = False) -> list[dict]:
    """Audit in memory; never save or modify the uploaded DOCX."""
    try:
        document = Document(BytesIO(data))
    except (PackageNotFoundError, BadZipFile, KeyError, ValueError, OSError) as exc:
        raise ValueError("DOCX tidak dapat dibuka; pastikan file DOCX valid dan tidak rusak.") from exc

    applicable, review = filter_rules(rules, degree)
    findings = []
    for rule in applicable:
        spec = PAGE_RULES.get(rule["validation_key"])
        if spec and rule["rule_code"] == spec[0] and rule["expected_value_pattern"] == spec[1]:
            for index, section in enumerate(document.sections, 1):
                values = (section.page_width, section.page_height) if spec[2] is None else (getattr(section, spec[2]),)
                expected = spec[3] if isinstance(spec[3], tuple) else (spec[3],)
                if any(value is None for value in values):
                    findings.append(finding(rule, "needs_review", f"section:{index}", "Tidak tersedia", "Ukuran tidak dapat diverifikasi."))
                    continue
                actual = tuple(value.cm for value in values)
                matches = all(abs(a - b) <= 0.02 for a, b in zip(actual, expected))
                findings.append(finding(rule, "pass" if matches else "fail", f"section:{index}", " × ".join(f"{value:.2f}" for value in actual) + " cm", "Nilai section sesuai." if matches else "Nilai section tidak sesuai."))
        elif rule["validation_key"] == "body.font-times-new-roman-12" and rule["rule_code"] == "PPKI-LAY-005" and rule["expected_value_pattern"] == "Times New Roman 12 pt":
            findings.extend(font_findings(document, rule, body_style, confirmed))
        elif rule["validation_key"] in PARAGRAPH_RULES and (rule["rule_code"], rule["expected_value_pattern"]) == PARAGRAPH_RULES[rule["validation_key"]][:2]:
            findings.extend(paragraph_findings(document, rule, PARAGRAPH_RULES[rule["validation_key"]][2], body_style, confirmed))
        else:
            findings.append(finding(rule, "not_supported", "dokumen", "—", "Validator belum tersedia atau aturan tidak cocok dengan mapping yang diuji."))
    for rule in review:
        findings.append(finding(rule, "needs_review", "dokumen", rule["applies_to"], "Konteks penerapan belum dipetakan."))
    return findings


def summarize(findings: list[dict]) -> dict[str, int]:
    # Satu status per rule, dengan ketidakpastian mengalahkan hasil parsial.
    priority = {"pass": 0, "needs_review": 1, "fail": 2, "not_supported": 3}
    statuses = {}
    for item in findings:
        code, status = item["rule_code"], item["status"]
        if code not in statuses or priority[status] > priority[statuses[code]]:
            statuses[code] = status
    counts = Counter(statuses.values())
    checked = {item["rule_code"] for item in findings if item["location"].startswith(("section:", "paragraf:")) and item["actual"] != "Tidak diperiksa"}
    return {"diperiksa": len(checked),
            "sesuai": counts["pass"], "tidak_sesuai": counts["fail"],
            "tidak_didukung": counts["not_supported"], "perlu_review": counts["needs_review"]}
