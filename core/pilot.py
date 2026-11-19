"""Opt-in, per-paragraph formatting pilot. Never consumes AI classifications."""
from collections import Counter
from copy import deepcopy
from io import BytesIO
from types import SimpleNamespace
from zipfile import ZipFile

from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

from core.audit import PARAGRAPH_RULES, font_findings, paragraph_findings, validate_docx_input
from core.formatter import FONT_CODE, VALUES, _document_structure, font_targets
from core.rules import filter_rules
from core.structure import safe_format_scope

PILOT_CODES = (FONT_CODE, *VALUES)


def _analysis_paragraph(paragraph):
    """Ignore known non-format markers on an analysis clone only."""
    clone = Paragraph(deepcopy(paragraph._p), paragraph._parent)
    markers = {qn("w:bookmarkStart"), qn("w:bookmarkEnd"), qn("w:proofErr")}
    for child in list(clone._p):
        if child.tag in markers:
            clone._p.remove(child)
    return clone


def pilot_plan(data: bytes, rules: list[dict], degree: str, confirmed: set[int]) -> list[dict]:
    """Build independent per-rule decisions; IDs need explicit operator confirmation."""
    validate_docx_input(data, "input.docx")
    document = Document(BytesIO(data))
    if any(type(index) is not int or index < 1 or index > len(document.paragraphs) for index in confirmed):
        raise ValueError("Lokasi konfirmasi tidak valid untuk dokumen ini.")
    applicable, _ = filter_rules(rules, degree)
    available = {r["rule_code"]: r for r in applicable if r["rule_code"] in PILOT_CODES}
    scope = safe_format_scope(data, rules, degree, include_document_defaults=True, use_structure_map=True)
    output = []
    for row in scope:
        if row["jenis"] != "teks_isi" or not row["lokasi"].startswith("paragraf:"):
            continue
        index = int(row["lokasi"].split(":")[1])
        paragraph = document.paragraphs[index - 1]
        for check in row["rule_decisions"]:
            code = check["rule_code"]
            rule = available.get(code)
            state = "known_compliant" if check["needs_change"] is False else "known_noncompliant" if check["needs_change"] is True else "unknown_value"
            reasons = []
            if index not in confirmed:
                reasons.append("Paragraf belum dikonfirmasi operator sebagai teks isi.")
            if not row.get("ai_section_safe", False):
                reasons.append("Section atau batas section tidak aman atau belum dipetakan.")
            if not check["eligible"]:
                reasons.append("Struktur paragraf, aturan, atau penerapan belum dapat dipastikan: " + check["alasan"])
            if rule is None:
                reasons.append("Aturan tidak tersedia atau tidak berlaku untuk jenjang.")
            elif rule["fix_mode"] != "Auto":
                reasons.append("Aturan bukan Auto; tidak ada izin otomatis.")
            # A known compliant value is never written; still record scope ambiguity.
            if rule is not None and code == FONT_CODE and state != "known_compliant" and font_targets(paragraph, rule["expected_value_pattern"]) is None:
                reasons.append("Font, theme, simbol, atau struktur run tidak dapat dipastikan aman.")
            if state == "known_noncompliant" and not check["technical_safe"]:
                reasons.append("Perubahan belum dapat dipastikan aman secara teknis.")
            if state == "unknown_value" and code in VALUES and rule is not None and check["eligible"]:
                spec = PARAGRAPH_RULES.get(rule["validation_key"])
                clone = _analysis_paragraph(paragraph)
                finding = paragraph_findings(SimpleNamespace(paragraphs=[clone]), rule, spec[2], clone.style.style_id, True, include_defaults=True)[0] if spec else None
                if not finding or finding["message"] != "Properti eksplisit tidak ditemukan; default dokumen perlu review.":
                    reasons.append("Nilai tidak diketahui karena format atau struktur kompleks; normalisasi tidak aman.")
            elif state == "unknown_value" and code == FONT_CODE:
                reasons.append("Nilai font tidak diketahui; normalisasi font belum didukung secara aman.")
            eligible = not reasons and state != "known_compliant"
            output.append({"lokasi": row["lokasi"], "rule_code": code, "nilai_awal": state,
                           "eligible_for_normalization": eligible, "unsafe_or_ambiguous": bool(reasons),
                           "target": rule["expected_value_pattern"] if rule else "Tidak tersedia",
                           "alasan": " ".join(reasons) if reasons else "Sudah sesuai; tidak perlu perubahan." if state == "known_compliant" else "Konfirmasi dan pemeriksaan lokal terpenuhi."})
    represented = {int(row["lokasi"].split(":")[1]) for row in output}
    for index in sorted(confirmed - represented):
        for code in PILOT_CODES:
            rule = available.get(code)
            output.append({"lokasi": f"paragraf:{index}", "rule_code": code, "nilai_awal": "unknown_value",
                           "eligible_for_normalization": False, "unsafe_or_ambiguous": True,
                           "target": rule["expected_value_pattern"] if rule else "Tidak tersedia",
                           "alasan": "Paragraf terpilih bukan kandidat teks isi yang aman untuk diperiksa."})
    return output


def format_pilot(data: bytes, rules: list[dict], degree: str, confirmed: set[int]) -> tuple[bytes, list[dict]]:
    """Apply only operator-confirmed pilot decisions, then verify every change."""
    plan = pilot_plan(data, rules, degree, confirmed)
    changes = [row for row in plan if row["eligible_for_normalization"]]
    if not changes:
        return data, plan
    document = Document(BytesIO(data))
    changed = {}
    for item in changes:
        index = int(item["lokasi"].split(":")[1])
        paragraph = document.paragraphs[index - 1]
        code = item["rule_code"]
        if code == FONT_CODE:
            targets = font_targets(paragraph, item["target"])
            if not targets:
                raise ValueError("Validasi font pilot gagal; hasil dibatalkan.")
            name, amount, unit = item["target"].rsplit(" ", 2)
            if unit != "pt":
                raise ValueError("Target font tidak didukung.")
            for run_index, fields in targets:
                run = paragraph.runs[run_index]
                if "name" in fields:
                    run.font.name = name
                if "size" in fields:
                    run.font.size = Pt(float(amount))
                changed[("font", index, run_index)] = fields
        else:
            attribute, value = VALUES[code]
            setattr(paragraph.paragraph_format, attribute, value)
            changed.setdefault(index, set()).add(code)
    output = BytesIO(); document.save(output)
    with ZipFile(BytesIO(data)) as original, ZipFile(BytesIO(output.getvalue())) as generated:
        replacement = generated.read("word/document.xml")
        rebuilt = BytesIO()
        with ZipFile(rebuilt, "w") as target:
            for info in original.infolist():
                target.writestr(info, replacement if info.filename == "word/document.xml" else original.read(info))
    result = rebuilt.getvalue()
    validate_docx_input(result, "pilot.docx")
    with ZipFile(BytesIO(data)) as original, ZipFile(BytesIO(result)) as formatted:
        if set(original.namelist()) != set(formatted.namelist()):
            raise ValueError("Struktur paket pilot berubah; hasil dibatalkan.")
        if any(original.read(name) != formatted.read(name) for name in original.namelist() if name != "word/document.xml"):
            raise ValueError("Bagian paket pilot di luar cakupan berubah; hasil dibatalkan.")
        if _document_structure(original.read("word/document.xml"), changed) != _document_structure(formatted.read("word/document.xml"), changed):
            raise ValueError("Isi atau struktur pilot di luar cakupan berubah; hasil dibatalkan.")
    after = Document(BytesIO(result))
    rules_by_code = {rule["rule_code"]: rule for rule in rules}
    for item in changes:
        paragraph = _analysis_paragraph(after.paragraphs[int(item["lokasi"].split(":")[1]) - 1])
        rule = rules_by_code[item["rule_code"]]
        view = SimpleNamespace(paragraphs=[paragraph])
        if item["rule_code"] == FONT_CODE:
            finding = font_findings(view, rule, paragraph.style.style_id, True)[0]
        else:
            spec = PARAGRAPH_RULES[rule["validation_key"]]
            finding = paragraph_findings(view, rule, spec[2], paragraph.style.style_id, True, include_defaults=True)[0]
        if finding["status"] != "pass":
            raise ValueError(f"Audit ulang pilot gagal untuk {item['rule_code']} di {item['lokasi']}; hasil dibatalkan.")
    return result, plan


def pilot_summary(plan: list[dict]) -> dict:
    counts = Counter(row["nilai_awal"] for row in plan)
    return {"known_compliant": counts["known_compliant"], "known_noncompliant": counts["known_noncompliant"],
            "unknown_value": counts["unknown_value"], "planned": sum(row["eligible_for_normalization"] for row in plan),
            "unknown_to_normalize": sum(row["eligible_for_normalization"] and row["nilai_awal"] == "unknown_value" for row in plan),
            "rejected": sum(row["unsafe_or_ambiguous"] for row in plan)}
