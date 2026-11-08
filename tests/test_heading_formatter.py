from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from zipfile import ZipFile

import pytest
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from streamlit.testing.v1 import AppTest

from core.audit import audit_docx
from core.formatter import format_docx, plan_changes, skipped_changes
from core.rules import load_rules


FIXTURE = Path(__file__).parent / "fixtures" / "PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx"
CODES = {"PPKI-HDG-003", "PPKI-HDG-004", "PPKI-HDG-006"}


def test_master_heading_only_preserves_everything_else_and_is_idempotent():
    data, rules, selected = FIXTURE.read_bytes(), load_rules(), {40, 60, 75}
    before = audit_docx(data, rules, "S1", heading_confirmed=selected)
    plan = plan_changes(data, rules, "S1", None, False, selected, True)
    assert len(plan) == 3 and {i["rule_code"] for i in plan} == CODES
    assert all(i["location"] == "paragraf:60" for i in plan)
    output, after, applied = format_docx(data, rules, "S1", None, False, selected, True)
    original, result = Document(BytesIO(data)), Document(BytesIO(output))
    assert FIXTURE.read_bytes() == data
    assert len(applied) == 3
    assert original.paragraphs[59].text == "BAB II Metode Penelitian."
    assert result.paragraphs[59].text == "BAB II METODE PENELITIAN."
    assert result.paragraphs[59].alignment == WD_ALIGN_PARAGRAPH.CENTER
    assert all(run.bold is True for run in result.paragraphs[59].runs if run.text.strip())
    for index in range(len(original.paragraphs)):
        if index != 59:
            assert original.paragraphs[index]._p.xml == result.paragraphs[index]._p.xml
    assert len(original.sections) == len(result.sections)
    for first, second in zip(original.sections, result.sections):
        assert first._sectPr.xml == second._sectPr.xml
    assert [table._tbl.xml for table in original.tables] == [table._tbl.xml for table in result.tables]
    assert len(original.inline_shapes) == len(result.inline_shapes)
    with ZipFile(BytesIO(data)) as old, ZipFile(BytesIO(output)) as new:
        assert all(old.read(name) == new.read(name) for name in old.namelist() if name != "word/document.xml")
    after_map = {(i["rule_code"], i["location"]): i for i in after}
    before_map = {(i["rule_code"], i["location"]): i for i in before}
    assert all(before_map[(i["rule_code"], i["location"])]["status"] == "fail" and after_map[(i["rule_code"], i["location"])]["status"] == "pass" for i in applied)
    second, _, remaining = format_docx(output, rules, "S1", None, False, selected, True)
    assert second == output and not remaining


def test_unconfirmed_chapter_and_restricted_fix_modes_are_skipped():
    data, rules = FIXTURE.read_bytes(), load_rules()
    assert not plan_changes(data, rules, "S1", None, False, {40, 75}, True)
    for rule in rules:
        if rule["rule_code"] == "PPKI-HDG-003": rule["fix_mode"] = "Manual"
        if rule["rule_code"] == "PPKI-HDG-004": rule["fix_mode"] = "Confirm"
    plan = plan_changes(data, rules, "S1", None, False, {60}, True)
    assert [i["rule_code"] for i in plan] == ["PPKI-HDG-006"]
    findings = audit_docx(data, rules, "S1", heading_confirmed={60})
    skipped = skipped_changes(data, rules, "S1", findings, plan, None, False, True)
    assert "Manual" in next(i for i in skipped if i["rule_code"] == "PPKI-HDG-003" and i["location"] == "paragraf:60")["alasan_dilewati"]
    assert "Confirm" in next(i for i in skipped if i["rule_code"] == "PPKI-HDG-004" and i["location"] == "paragraf:60")["alasan_dilewati"]


def test_ambiguous_heading_is_skipped():
    doc = Document(); p = doc.add_paragraph(style="Heading 1")
    p.add_run("BAB II Metode").bold = False; p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p._p.append(OxmlElement("w:hyperlink"))
    buffer = BytesIO(); doc.save(buffer); data = buffer.getvalue(); rules = load_rules()
    findings = audit_docx(data, rules, "S1", heading_confirmed={1})
    assert all(i["status"] == "needs_review" for i in findings if i["rule_code"] in CODES)
    assert not plan_changes(data, rules, "S1", None, False, {1}, True)


def test_split_runs_keep_number_and_formatting():
    doc = Document(); p = doc.add_paragraph(style="Heading 1")
    prefix = p.add_run("BAB II "); prefix.bold = False
    first = p.add_run("Metode "); first.bold = False; first.italic = True
    second = p.add_run("Penelitian."); second.bold = False; second.underline = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    data = BytesIO(); doc.save(data)
    output, after, changes = format_docx(data.getvalue(), load_rules(), "S1", None, False, {1}, True)
    p2 = Document(BytesIO(output)).paragraphs[0]
    assert [run.text for run in p2.runs] == ["BAB II ", "METODE ", "PENELITIAN."]
    assert p2.runs[0].bold is False and p2.runs[1].italic and p2.runs[2].underline
    assert len(changes) == 3
    assert all(next(i for i in after if i["rule_code"] == c["rule_code"] and i["location"] == c["location"])["status"] == "pass" for c in changes)


def test_non_ascii_heading_is_skipped_with_reason():
    doc = Document(); para = doc.add_paragraph("BAB II Kajian ékonomi", style="Heading 1")
    para.runs[0].bold = False; para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    data = BytesIO(); doc.save(data); rules = load_rules()
    findings = audit_docx(data.getvalue(), rules, "S1", heading_confirmed={1})
    plan = plan_changes(data.getvalue(), rules, "S1", None, False, {1}, True)
    skipped = skipped_changes(data.getvalue(), rules, "S1", findings, plan, None, False, True)
    assert not plan
    assert len([i for i in skipped if i["rule_code"] in CODES]) == 3
    assert all("non-ASCII" in i["alasan_dilewati"] for i in skipped if i["rule_code"] in CODES)


def test_streamlit_heading_plan_reaudit_and_downloads():
    data = FIXTURE.read_bytes()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name=FIXTURE.name, getvalue=lambda: data)):
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=20).run()
        app.checkbox[2].check()  # BAB II
        app.checkbox[4].check()  # heading-only
        app.button[0].click().run()
        assert not app.exception
        assert len(app.session_state["audit_t4a"]["plan"]) == 3
        next(button for button in app.button if button.label == "Terapkan Perbaikan Otomatis").click().run()
        assert not app.exception
        output = app.session_state["output_t4a"]
        assert len(output["report"]) == 3 and all(i["status"] == "pass" for i in output["report"])
        assert len(app.get("download_button")) == 2
