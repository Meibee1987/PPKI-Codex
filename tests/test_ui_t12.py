from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from core.audit import audit_docx, summarize
from core.rules import load_rules


ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "tests/fixtures/PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx"


def test_summary_and_heading_only_workflow():
    data = MASTER.read_bytes()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name=MASTER.name, getvalue=lambda: data)):
        app = AppTest.from_file(ROOT / "app.py", default_timeout=20).run()
        assert not app.exception
        assert app.selectbox[1].value is None
        app.checkbox[2].check()  # BAB II
        app.checkbox[4].check()  # Heading saja
        app.button[0].click().run()
        assert not app.exception
        assert [h.value for h in app.header] == ["1. Upload dokumen dan pilih jenjang", "2. Audit dan ringkasan", "3. Detail temuan dan diagnostik", "4. Rencana perbaikan dan download"]
        snapshot = app.session_state["audit_t4a"]
        expected = summarize(audit_docx(data, load_rules(), "S1", None, False, {60}))
        assert snapshot["before"] == expected
        summary = next(x.value for x in app.markdown if x.value.startswith("Diperiksa:"))
        for status, key in (("pass", "sesuai"), ("fail", "tidak_sesuai"), ("needs_review", "perlu_review"), ("not_supported", "tidak_didukung")):
            assert f"{status}: {expected[key]}" in summary
        assert any("Dilewati beserta alasan" in exp.label for exp in app.expander)
        assert {item["rule_code"] for item in snapshot["plan"]} == {"PPKI-HDG-003", "PPKI-HDG-004", "PPKI-HDG-006"}
        assert MASTER.read_bytes() == data
        next(button for button in app.button if button.label == "Terapkan Perbaikan Otomatis").click().run()
        assert not app.exception
        assert len(app.get("download_button")) == 2
        assert app.session_state["output_t4a"]["report"] and all(row["status"] == "pass" for row in app.session_state["output_t4a"]["report"])
        assert any(x.value == summary for x in app.markdown)
        assert MASTER.read_bytes() == data
