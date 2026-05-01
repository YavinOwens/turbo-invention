import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_safety_script_passes_on_clean_tree():
    result = subprocess.run(
        [sys.executable, "scripts/check_no_real_data.py"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
