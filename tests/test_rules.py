import json
import pytest

from core.rules import RULES_PATH, filter_rules, load_rules


@pytest.fixture
def sample_rule():
    return load_rules(RULES_PATH)[0].copy()


def write_rules(path, rules):
    path.write_text(json.dumps(rules), encoding="utf-8")
    return path


def test_load_real_snapshot():
    rules = load_rules()
    assert len(rules) == 317
    assert sum(rule["is_implemented"] for rule in rules) == 25


@pytest.mark.parametrize("degree,expected", [("S1", {"Semua", "Skripsi"}), ("S2", {"Semua", "Tesis", "Tesis/Disertasi"}), ("S3", {"Semua", "Disertasi", "Tesis/Disertasi"})])
def test_filter_explicit_applicability(sample_rule, degree, expected):
    labels = ["Semua", "Skripsi", "Tesis", "Disertasi", "Tesis/Disertasi", "Skripsi FKH", "Semua terkait"]
    rules = [dict(sample_rule, applies_to=label) for label in labels]
    applicable, review = filter_rules(rules, degree)
    assert {rule["applies_to"] for rule in applicable} == expected
    assert {rule["applies_to"] for rule in review} == {"Skripsi FKH", "Semua terkait"}


def test_duplicate_rule_code_rejected(tmp_path, sample_rule):
    duplicate = dict(sample_rule, id="00000000-0000-0000-0000-000000000001")
    with pytest.raises(ValueError, match="rule_code duplikat"):
        load_rules(write_rules(tmp_path / "rules.json", [sample_rule, duplicate]))


def test_invalid_json_and_missing_file(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text("[broken", encoding="utf-8")
    for candidate in (path, tmp_path / "missing.json"):
        with pytest.raises(ValueError, match="Gagal membaca JSON"):
            load_rules(candidate)


@pytest.mark.parametrize("field,value", [("domain", None), ("is_implemented", 1), ("pdf_page", True), ("id", "invalid"), ("created_at", "invalid")])
def test_invalid_schema_rejected(tmp_path, sample_rule, field, value):
    sample_rule[field] = value
    with pytest.raises(ValueError):
        load_rules(write_rules(tmp_path / "rules.json", [sample_rule]))


def test_missing_nullable_field_rejected(tmp_path, sample_rule):
    del sample_rule["subdomain"]
    with pytest.raises(ValueError, match="subdomain"):
        load_rules(write_rules(tmp_path / "rules.json", [sample_rule]))


def test_invalid_root_rejected(tmp_path):
    with pytest.raises(ValueError, match="array"):
        load_rules(write_rules(tmp_path / "rules.json", {}))
