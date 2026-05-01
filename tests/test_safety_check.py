import subprocess
import sys
from pathlib import Path

# Marker is split so this test file itself doesn't trip the safety scanner.
_FIRST = "Yavin"
_LAST = "Michael" + " " + "Owens"
_FULL = _FIRST + " " + _LAST
_HANDLE = "yavin" + "owens" + "87"

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_no_real_data.py"


def _run_in(repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=repo, capture_output=True, text=True,
    )


def test_safety_script_passes_on_clean_tree():
    result = _run_in(ROOT)
    assert result.returncode == 0, result.stderr


def _init_repo(path: Path) -> None:
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=path, check=True)


def _add(repo: Path, rel: str, body: str) -> None:
    f = repo / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(body)
    subprocess.run(["git", "add", rel], cwd=repo, check=True)


def test_blocks_forbidden_path(tmp_path: Path):
    _init_repo(tmp_path)
    _add(tmp_path, "data/foo.txt", "harmless")
    r = _run_in(tmp_path)
    assert r.returncode == 1
    assert "forbidden path" in r.stderr


def test_blocks_real_name_in_csv(tmp_path: Path):
    _init_repo(tmp_path)
    _add(tmp_path, "notes.csv", f"id,name\n1,{_FULL}\n")
    r = _run_in(tmp_path)
    assert r.returncode == 1
    assert "real-name marker" in r.stderr


def test_blocks_real_name_case_insensitive(tmp_path: Path):
    _init_repo(tmp_path)
    _add(tmp_path, "notes.md", f"see {_HANDLE.upper()} for details")
    r = _run_in(tmp_path)
    assert r.returncode == 1


def test_blocks_zip_suffix(tmp_path: Path):
    _init_repo(tmp_path)
    _add(tmp_path, "export.zip", "binary-ish")
    r = _run_in(tmp_path)
    assert r.returncode == 1
    assert "forbidden suffix" in r.stderr
