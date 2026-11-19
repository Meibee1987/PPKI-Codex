"""Regressions for evidence required before enabling automatic formatting."""
from io import BytesIO

from docx import Document

from core.pilot import format_pilot
from core.rules import load_rules


def test_unmarked_special_quote_is_not_authorized_by_body_style_alone():
    document = Document()
    document.add_heading("BAB I PENDAHULUAN", 1)
    # This is a synthetic special quotation with no quote-specific Word markup.
    # It intentionally has the same style and structure as ordinary body text.
    paragraph = document.add_paragraph(
        "Penjelasan sintetis ini merupakan kutipan khusus dan harus mempertahankan format tersendiri meskipun gaya Word menyatakannya sebagai paragraf isi.",
        style="Body Text",
    )
    paragraph.paragraph_format.line_spacing = 2.0
    stream = BytesIO()
    document.save(stream)
    data = stream.getvalue()
    rules = load_rules()
    output, plan = format_pilot(data, rules, "S1", set())
    assert output == data
    item = next((item for item in plan if item["lokasi"] == "paragraf:2" and item["rule_code"] == "PPKI-LAY-017"), None)
    assert item is None or not item["eligible_for_normalization"]
