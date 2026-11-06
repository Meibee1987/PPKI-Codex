import subprocess
import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest


PROJECT = Path(__file__).resolve().parent.parent


def test_app_import_in_fresh_process():
    result = subprocess.run(
        [sys.executable, "-c", "import app; from core.formatter import skipped_changes; assert callable(skipped_changes)"],
        cwd=PROJECT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stderr


def test_app_starts_without_import_error():
    app = AppTest.from_file(PROJECT / "app.py", default_timeout=15).run()
    assert not app.exception
    assert app.title[0].value == "PPKI Academic Formatter"
