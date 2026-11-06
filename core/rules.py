import json
from datetime import datetime
from pathlib import Path
from uuid import UUID


RULES_PATH = Path(__file__).resolve().parent.parent / "rules" / "ppki_rules_all.json"
TEXT_FIELDS = (
    "id", "rule_code", "domain", "applies_to", "element",
    "official_requirement", "expected_value_pattern", "severity", "fix_mode",
    "validation_key", "created_at",
)
NULLABLE_TEXT_FIELDS = ("subdomain", "printed_page", "source_section")
APPLICABILITY = {
    "Semua": {"S1", "S2", "S3"},
    "Skripsi": {"S1"},
    "Tesis": {"S2"},
    "Disertasi": {"S3"},
    "Tesis/Disertasi": {"S2", "S3"},
}


def load_rules(path: Path = RULES_PATH) -> list[dict]:
    """Load the local public.rules snapshot, rejecting invalid records."""
    try:
        with path.open(encoding="utf-8") as source:
            rules = json.load(source)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Gagal membaca JSON aturan: {exc}") from exc
    if not isinstance(rules, list):
        raise ValueError("JSON aturan harus berupa array.")

    codes, ids = set(), set()
    for index, rule in enumerate(rules, start=1):
        if not isinstance(rule, dict):
            raise ValueError(f"Aturan ke-{index} harus berupa objek.")
        for field in TEXT_FIELDS:
            if not isinstance(rule.get(field), str) or not rule[field].strip():
                raise ValueError(f"Aturan ke-{index}: {field} harus berupa teks yang tidak kosong.")
        for field in NULLABLE_TEXT_FIELDS:
            if field not in rule or (rule[field] is not None and not isinstance(rule[field], str)):
                raise ValueError(f"Aturan ke-{index}: {field} harus berupa teks atau null.")
        if type(rule.get("is_implemented")) is not bool:
            raise ValueError(f"Aturan ke-{index}: is_implemented harus boolean.")
        if "pdf_page" not in rule or (rule["pdf_page"] is not None and type(rule["pdf_page"]) is not int):
            raise ValueError(f"Aturan ke-{index}: pdf_page harus berupa integer atau null.")
        try:
            rule_id = UUID(rule["id"])
            timestamp = datetime.fromisoformat(rule["created_at"])
            if timestamp.utcoffset() is None:
                raise ValueError("timestamp tanpa zona waktu")
        except ValueError as exc:
            raise ValueError(f"Aturan ke-{index}: id UUID atau created_at tidak valid: {exc}") from exc
        if rule["rule_code"] in codes:
            raise ValueError(f"rule_code duplikat: {rule['rule_code']}")
        if rule_id in ids:
            raise ValueError(f"id duplikat: {rule['id']}")
        codes.add(rule["rule_code"])
        ids.add(rule_id)
    return rules


def filter_rules(rules: list[dict], degree: str) -> tuple[list[dict], list[dict]]:
    """Return applicable rules and rules whose applicability needs review."""
    if degree not in {"S1", "S2", "S3"}:
        raise ValueError(f"Jenjang tidak dikenal: {degree}")
    applicable, review = [], []
    for rule in rules:
        degrees = APPLICABILITY.get(rule["applies_to"])
        if degrees is None:
            review.append(rule)
        elif degree in degrees:
            applicable.append(rule)
    return applicable, review
