"""Deterministic, read-only document structure candidates; not a formatter."""
from io import BytesIO
import re
from zipfile import BadZipFile

from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

from core.audit import paragraph_value


def recognize_structure(data: bytes) -> list[dict]:
    try:
        document = Document(BytesIO(data))
    except (PackageNotFoundError, BadZipFile, KeyError, ValueError, OSError) as exc:
        raise ValueError("Struktur DOCX tidak dapat dibaca.") from exc

    labels = {
        "PERNYATAAN": "pernyataan", "ABSTRAK": "abstrak", "ABSTRACT": "abstract",
        "RINGKASAN": "ringkasan", "SUMMARY": "summary", "PRAKATA": "prakata",
        "DAFTAR ISI": "daftar_isi", "DAFTAR TABEL": "daftar_tabel",
        "DAFTAR GAMBAR": "daftar_gambar", "DAFTAR PUSTAKA": "daftar_pustaka",
        "PENGESAHAN": "pengesahan", "LAMPIRAN": "lampiran",
    }
    rows = []
    context = "awal"
    paragraph_index = 0
    table_index = 0
    previous_page_break = False

    def add(location, p, kind, evidence, status="needs_review"):
        rows.append({"lokasi": location, "jenis": kind, "style": p.style.style_id,
                     "teks": p.text, "alasan": evidence,
                     "keyakinan": "terbatas" if status == "detected" else "perlu konfirmasi",
                     "status": status})

    def numbered(p):
        properties = [p._p.pPr]
        style, seen = p.style, set()
        while style is not None and style.style_id not in seen:
            seen.add(style.style_id)
            properties.append(style.element.pPr)
            style = style.base_style
        return any(item is not None and item.find(qn("w:numPr")) is not None for item in properties)

    for block in document.iter_inner_content():
        if isinstance(block, Table):
            table_index += 1
            seen = set()
            for row_index, row in enumerate(block.rows, 1):
                for column_index, cell in enumerate(row.cells, 1):
                    if cell._tc in seen:
                        continue
                    seen.add(cell._tc)
                    for cell_index, p in enumerate(cell.paragraphs, 1):
                        add(f"tabel:{table_index}/baris:{row_index}/kolom:{column_index}/paragraf:{cell_index}", p, "paragraf_tabel", "Paragraf berada pada sel tabel body.", "detected")
            continue
        if not isinstance(block, Paragraph):
            continue
        paragraph_index += 1
        p = block
        location = f"paragraf:{paragraph_index}"
        text = p.text.strip()
        if not text:
            previous_page_break = previous_page_break or bool(p._p.xpath('.//w:br[@w:type="page"] | .//w:lastRenderedPageBreak | ./w:pPr/w:sectPr'))
            continue
        style = p.style.style_id
        style_lower = style.casefold()
        compact = " ".join(text.split())
        upper = compact.upper()
        complex_xml = bool(p._p.xpath('.//w:hyperlink | .//w:fldChar | .//w:fldSimple | .//w:drawing | .//w:object | .//m:oMath'))
        toc_style = style_lower.startswith("toc") or style_lower.startswith("daftarisi")
        caption = re.match(r"^(tabel|gambar)\s+\d", text, re.IGNORECASE)
        heading_level = {"Heading1": 1, "Heading2": 2, "Heading3": 3}.get(style)
        label = labels.get(upper)
        if upper.startswith("PERNYATAAN "):
            label = "pernyataan"
        if re.match(r"^LAMPIRAN(?:\s|$)", upper):
            label = "lampiran"
        chapter = re.match(r"^(?:BAB\s+)?[IVXLCDM]+\s+\S", compact, re.IGNORECASE)
        sub = re.match(r"^\d+\.\d+(?:\.\d+)?(?:\s|$)", compact)
        section_break = bool(p._p.xpath('.//w:br[@w:type="page"] | .//w:lastRenderedPageBreak | ./w:pPr/w:sectPr')) or bool(paragraph_value(p, "page_break_before"))
        boundary_before = previous_page_break
        previous_page_break = False
        if toc_style:
            add(location, p, "entri_daftar_isi", "Style daftar isi; bukan heading isi.", "detected")
        elif chapter and heading_level == 1 and boundary_before and "\t" not in text and not p._p.xpath('.//w:hyperlink | .//w:fldChar | .//w:fldSimple'):
            add(location, p, "bab", "Heading 1 berpola Romawi setelah pemisah halaman; elemen atau konteks perlu konfirmasi.")
            context = "isi_ambigu"
        elif context == "daftar_isi" and not section_break and (heading_level != 1 or complex_xml or "\t" in text):
            add(location, p, "entri_daftar", "Dalam daftar isi tanpa batas bagian yang jelas; identitas perlu review.")
        elif caption:
            kind = "caption_tabel" if caption.group(1).casefold() == "tabel" else "caption_gambar"
            add(location, p, kind, "Teks bernomor caption; hubungan dengan objek belum dipastikan.")
        elif label and (heading_level == 1 or style_lower in {"normal", "heading"}):
            add(location, p, label, "Label bagian eksplisit; identitas dan cakupan perlu konfirmasi.")
            context = label
        elif style == "Title" and context == "awal":
            add(location, p, "sampul_atau_halaman_judul", "Style Title pada bagian awal; sampul atau halaman judul belum pasti.")
        elif chapter and heading_level == 1 and not complex_xml and "\t" not in text and (context != "daftar_isi" or section_break):
            add(location, p, "bab", "Style Heading 1 dan pola angka Romawi; kepatuhan PPKI belum diperiksa.", "detected")
            context = "isi"
        elif chapter and heading_level == 1 and context == "daftar_isi":
            add(location, p, "khusus", "Mirip BAB dalam konteks daftar isi; pemisahan bagian belum pasti.")
        elif chapter and style_lower in {"normal", "bodytext"} and text.isupper() and (context == "awal" or (context in {"isi", "isi_ambigu"} and section_break)):
            add(location, p, "bab", "Pola angka Romawi tanpa style Heading 1; perlu konfirmasi BAB.")
            context = "isi_ambigu"
        elif sub and heading_level in (2, 3) and context in {"isi", "isi_ambigu"} and not complex_xml:
            kind = "sub_subbab" if compact.split()[0].count(".") == 2 else "subbab"
            add(location, p, kind, "Style heading dan pola nomor dalam konteks BAB.", "detected" if context == "isi" else "needs_review")
        elif sub and style_lower == "normal" and context in {"isi", "isi_ambigu"} and len(text) <= 150 and not numbered(p) and not complex_xml:
            kind = "sub_subbab" if compact.split()[0].count(".") == 2 else "subbab"
            add(location, p, kind, "Pola nomor tanpa style heading; kandidat perlu konfirmasi.")
        elif numbered(p) or style_lower.startswith("list"):
            add(location, p, "daftar", "Penomoran Word atau style daftar; makna daftar perlu review.")
        elif context in {"daftar_isi", "daftar_tabel", "daftar_gambar"}:
            add(location, p, "entri_daftar", "Berada dalam bagian daftar; konteks perlu review.")
        elif context == "daftar_pustaka":
            add(location, p, "entri_referensi", "Berada setelah kandidat daftar pustaka; identitas entri perlu review.")
        elif context == "lampiran":
            add(location, p, "lampiran", "Berada dalam kandidat lampiran; struktur perlu review.")
        elif context in {"isi", "isi_ambigu"} and not complex_xml and style_lower in {"normal", "bodytext", "firstparagraph"}:
            add(location, p, "teks_isi", "Style paragraf dan posisi dalam BAB; bagian khusus belum dapat dikecualikan sepenuhnya.")
        else:
            add(location, p, "khusus", "Posisi, style atau struktur belum cukup memastikan fungsi paragraf.")
    return rows


def safe_format_scope(data: bytes, rules: list[dict], degree: str) -> list[dict]:
    """Per-rule experimental assessment; never authorizes the live formatter."""
    from copy import deepcopy
    from types import SimpleNamespace
    from core.audit import font_findings, paragraph_findings, PARAGRAPH_RULES
    from core.formatter import font_targets
    from core.rules import filter_rules

    document = Document(BytesIO(data))
    recognized = recognize_structure(data)
    by_location = {item["lokasi"]: item for item in recognized}
    applicable, review = filter_rules(rules, degree)
    applicable_codes = {r["rule_code"] for r in applicable}
    review_codes = {r["rule_code"] for r in review}
    by_code = {r["rule_code"]: r for r in rules}
    body_codes = ("PPKI-LAY-005", "PPKI-LAY-017", "PPKI-LAY-018", "PPKI-LAY-019")
    protected = {"bab", "subbab", "sub_subbab", "paragraf_tabel", "sampul_atau_halaman_judul", "pernyataan", "pengesahan", "abstrak", "abstract", "ringkasan", "summary", "prakata", "daftar_isi", "daftar_tabel", "daftar_gambar", "entri_daftar", "entri_daftar_isi", "caption_tabel", "caption_gambar", "daftar_pustaka", "entri_referensi", "lampiran", "daftar"}
    reason_labels = {
        "empty_paragraph": "Paragraf kosong.", "section_separator": "Pemisah section.",
        "special_part": "Bagian khusus dilindungi.", "field_or_object": "Field, objek atau revisi kompleks dilindungi.",
        "special_paragraph_format": "Daftar atau format paragraf khusus dilindungi.",
        "unknown_xml_structure": "Struktur XML belum dapat diperiksa dengan aman.",
        "structure_unrecognized": "Jenis paragraf belum dikenali sebagai teks isi.",
        "chapter_context_unknown": "Konteks BAB belum dipastikan.",
        "heading_like_text": "Teks menyerupai heading, bukan isi yang dipastikan.",
        "applicability_unknown": "Penerapan aturan memerlukan review.",
        "rule_not_applicable": "Aturan tidak berlaku atau tidak tersedia.",
        "handler_not_supported": "Mapping validator tidak didukung.",
        "property_unknown": "Nilai format belum dapat dipastikan.",
        "fix_mode_not_auto": "Aturan tidak mengizinkan perbaikan Auto.",
        "body_identity_unconfirmed": "Identitas teks isi masih memerlukan konfirmasi operator.",
        "chapter_context_unconfirmed": "Identitas atau batas BAB masih memerlukan konfirmasi.",
        "style_identity_ambiguous": "Style juga dapat dipakai bagian khusus; identitas isi belum dikonfirmasi.",
        "already_compliant": "Nilai format sudah sesuai, tidak perlu perubahan.",
        "experimental_scope": "Cakupan teknis eksperimental, dry-run saja.",
        "operator_review_required": "Periksa keputusan tiap aturan bersama operator.",
    }
    output = []
    chapter_context = None
    for index, p in enumerate(document.paragraphs, 1):
        location = f"paragraf:{index}"
        item = by_location.get(location)
        kind = item["jenis"] if item else "kosong"
        section = p._p.pPr is not None and p._p.pPr.find(qn("w:sectPr")) is not None
        if kind == "bab":
            chapter_context = item["status"]
        elif kind in {"sampul_atau_halaman_judul", "pernyataan", "pengesahan", "abstrak", "abstract", "ringkasan", "summary", "prakata", "daftar_isi", "daftar_tabel", "daftar_gambar", "daftar_pustaka", "entri_referensi", "lampiran"} or (p.style.style_id == "Heading1" and kind == "khusus"):
            chapter_context = None
        if section:
            chapter_context = None

        # Only the analysis clone loses non-content markers. The original is untouched.
        clone = Paragraph(deepcopy(p._p), p._parent)
        marker_tags = {qn("w:bookmarkStart"), qn("w:bookmarkEnd"), qn("w:proofErr")}
        for child in list(clone._p):
            if child.tag in marker_tags:
                clone._p.remove(child)
        simple = all(child.tag in (qn("w:pPr"), qn("w:r")) for child in clone._p) and all(all(child.tag in (qn("w:rPr"), qn("w:t")) for child in run._r) for run in clone.runs)
        risky = bool(p._p.xpath('.//w:hyperlink | .//w:fldChar | .//w:instrText | .//w:fldSimple | .//w:drawing | .//w:pict | .//w:object | .//w:footnoteReference | .//w:endnoteReference | .//w:commentReference | .//w:commentRangeStart | .//w:sdt | .//w:ins | .//w:del | .//w:rPrChange | .//w:pPrChange | .//m:oMath'))
        properties = [p._p.pPr]
        style, seen = p.style, set()
        while style is not None and style.style_id not in seen:
            seen.add(style.style_id)
            properties.append(style.element.pPr)
            style = style.base_style
        special_format = any(pr is not None and any(pr.find(qn("w:" + tag)) is not None for tag in ("numPr", "framePr", "textDirection", "bidi")) for pr in properties)
        if not p.text.strip():
            reason = "empty_paragraph"
        elif section:
            reason = "section_separator"
        elif kind in protected:
            reason = "special_part"
        elif risky:
            reason = "field_or_object"
        elif special_format:
            reason = "special_paragraph_format"
        elif not simple:
            reason = "unknown_xml_structure"
        elif kind != "teks_isi":
            reason = "structure_unrecognized"
        elif chapter_context is None:
            reason = "chapter_context_unknown"
        elif re.match(r"^(?:BAB\s+)?[IVXLCDM]+\s+\S|^\d+(?:\.\d+)*\s+\S", p.text.strip()) or p.text.strip().isupper():
            reason = "heading_like_text"
        else:
            reason = None
        hard_protection = reason in {"empty_paragraph", "section_separator", "special_part", "field_or_object", "special_paragraph_format"}
        identity_certain = chapter_context == "detected" and p.style.style_id == "BodyText"
        checks = []
        for code in body_codes:
            rule = by_code.get(code)
            check = {"rule_code": code, "eligible": False, "needs_change": None, "technical_safe": False, "safe_to_apply": False, "status": "needs_review", "reason_codes": []}
            codes = check["reason_codes"]
            if reason:
                codes.append(reason)
            if code not in applicable_codes:
                codes.append("applicability_unknown" if code in review_codes else "rule_not_applicable")
            spec = PARAGRAPH_RULES.get(rule["validation_key"]) if rule else None
            supported_font = rule and code == "PPKI-LAY-005" and rule["validation_key"] == "body.font-times-new-roman-12" and rule["expected_value_pattern"] == "Times New Roman 12 pt"
            supported_paragraph = spec and (code, rule["expected_value_pattern"]) == spec[:2]
            if not (supported_font or supported_paragraph):
                codes.append("handler_not_supported")
            if not codes:
                check["eligible"] = True
                analysis = SimpleNamespace(paragraphs=[clone])
                finding = (font_findings(analysis, rule, clone.style.style_id, True) if supported_font else paragraph_findings(analysis, rule, spec[2], clone.style.style_id, True))[0]
                check["status"] = finding["status"]
                if finding["status"] in {"pass", "fail"}:
                    check["needs_change"] = finding["status"] == "fail"
                    check["technical_safe"] = not supported_font or font_targets(clone, rule["expected_value_pattern"]) is not None
                else:
                    codes.append("property_unknown")
                if rule["fix_mode"] != "Auto":
                    codes.append("fix_mode_not_auto")
                if not identity_certain:
                    codes.append("body_identity_unconfirmed")
                    if chapter_context != "detected":
                        codes.append("chapter_context_unconfirmed")
                    if p.style.style_id != "BodyText":
                        codes.append("style_identity_ambiguous")
                check["safe_to_apply"] = check["technical_safe"] and rule["fix_mode"] == "Auto" and identity_certain
                if check["status"] == "pass":
                    codes.append("already_compliant")
            check["alasan"] = " ".join(reason_labels[code] for code in codes) or reason_labels["experimental_scope"]
            checks.append(check)
        safe_codes = [c["rule_code"] for c in checks if c["safe_to_apply"]]
        changes = [c["rule_code"] for c in checks if c["safe_to_apply"] and c["needs_change"]]
        decision = "protected" if hard_protection else "auto_safe" if safe_codes else "needs_review"
        reason_code = reason or ("experimental_scope" if safe_codes else "operator_review_required")
        output.append({"lokasi": location, "jenis": kind, "keputusan": decision, "aturan_diizinkan": safe_codes, "aturan_berubah": changes, "reason_code": reason_code, "alasan": reason_labels[reason_code], "rule_decisions": checks})
    for item in recognized:
        if item["jenis"] == "paragraf_tabel":
            output.append({"lokasi": item["lokasi"], "jenis": item["jenis"], "keputusan": "protected", "aturan_diizinkan": [], "aturan_berubah": [], "reason_code": "table_cell", "alasan": "Paragraf sel tabel dilindungi.", "rule_decisions": [{"rule_code": code, "eligible": False, "needs_change": None, "technical_safe": False, "safe_to_apply": False, "status": "needs_review", "reason_codes": ["table_cell"], "alasan": "Paragraf sel tabel dilindungi."} for code in body_codes]})
    return output
