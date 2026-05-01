import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_no_real_data.py"

# Synthetic markers used to exercise the scanner. They are never written
# anywhere except a tmp_path repo, and passed via env var so the production
# safety check (which loads from .real-name-markers locally) is unaffected.
_TEST_MARKERS = "test-name-alpha,test-handle-beta"


def _env_with_markers(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = os.environ.copy()
    env["TURBO_REAL_NAME_MARKERS"] = _TEST_MARKERS
    if extra:
        env.update(extra)
    return env


def _run_in(repo: Path, with_markers: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=repo, capture_output=True, text=True,
        env=_env_with_markers() if with_markers else os.environ.copy(),
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


def test_blocks_real_name_via_env_marker(tmp_path: Path):
    _init_repo(tmp_path)
    _add(tmp_path, "notes.csv", "id,name\n1,test-name-alpha\n")
    r = _run_in(tmp_path, with_markers=True)
    assert r.returncode == 1
    assert "real-name marker" in r.stderr


def test_blocks_real_name_case_insensitive(tmp_path: Path):
    _init_repo(tmp_path)
    _add(tmp_path, "notes.md", "see TEST-HANDLE-BETA for details")
    r = _run_in(tmp_path, with_markers=True)
    assert r.returncode == 1


def test_blocks_zip_suffix(tmp_path: Path):
    _init_repo(tmp_path)
    _add(tmp_path, "export.zip", "binary-ish")
    r = _run_in(tmp_path)
    assert r.returncode == 1
    assert "forbidden suffix" in r.stderr


def test_marker_file_loaded_from_local_file(tmp_path: Path):
    _init_repo(tmp_path)
    (tmp_path / ".real-name-markers").write_text("# comment\nfile-marker\n")
    _add(tmp_path, "x.md", "some text with file-marker in it")
    # Run with PWD different so MARKER_FILE resolution uses script root,
    # not the tmp repo. We instead directly invoke against the tmp repo
    # by supplying env. But here we want to prove the file-loading path
    # works — copy the script into tmp_path so MARKER_FILE resolves there.
    import shutil
    (tmp_path / "scripts").mkdir()
    shutil.copy(SCRIPT, tmp_path / "scripts" / "check_no_real_data.py")
    r = subprocess.run(
        [sys.executable, "scripts/check_no_real_data.py"],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert r.returncode == 1
    assert "real-name marker" in r.stderr
