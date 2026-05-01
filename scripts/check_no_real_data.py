"""Block accidental commit of real SAR / PII data.

Fails (exit 1) if any tracked file path matches a forbidden pattern OR if any
tracked text-like file contains a real account marker (case-insensitive).

Markers themselves are NOT stored in this file — they live in a local-only
config so the public source code carries no PII. Configure via either:

  - env var:  TURBO_REAL_NAME_MARKERS="alice smith,acmehandle,acme123"
  - file:     a gitignored `.real-name-markers` at repo root, one marker per
              line, blanks and `#` comments allowed.

If neither is provided the script still enforces the path / suffix rules but
emits a notice that no name markers are configured.

Run via pre-commit / pre-push and CI.
"""
from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path

FORBIDDEN_PREFIXES = ("data/", "secrets/")
FORBIDDEN_SUFFIXES = (".env", ".zip", ".tar.gz", ".tgz", ".7z")
SCANNABLE_SUFFIXES = (
    ".json", ".jsonl", ".csv", ".tsv", ".txt", ".md", ".html", ".xml",
    ".yaml", ".yml", ".py", ".ipynb", ".log", ".ndjson",
)
ROOT = Path(__file__).resolve().parents[1]
MARKER_FILE = ROOT / ".real-name-markers"
ENV_VAR = "TURBO_REAL_NAME_MARKERS"


def load_markers() -> list[str]:
    raw: list[str] = []
    env = os.environ.get(ENV_VAR, "").strip()
    if env:
        raw.extend(env.split(","))
    if MARKER_FILE.exists():
        for line in MARKER_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                raw.append(line)
    return [m.strip().lower() for m in raw if m.strip()]


def tracked_files() -> list[Path]:
    out = subprocess.check_output(["git", "ls-files"], text=True)
    return [Path(p) for p in out.splitlines() if p]


def main() -> int:
    markers = load_markers()
    if not markers:
        print(
            f"notice: no name markers configured "
            f"({ENV_VAR} env var or {MARKER_FILE.name} file); "
            "path/suffix checks only.",
            file=sys.stderr,
        )

    bad: list[str] = []
    for p in tracked_files():
        s = str(p)
        if any(s.startswith(pre) for pre in FORBIDDEN_PREFIXES):
            bad.append(f"forbidden path: {s}")
            continue
        if any(s.endswith(suf) for suf in FORBIDDEN_SUFFIXES):
            bad.append(f"forbidden suffix: {s}")
            continue
        if not markers:
            continue
        if p.suffix.lower() in SCANNABLE_SUFFIXES and p.exists():
            try:
                text = p.read_text(encoding="utf-8", errors="ignore").lower()
            except OSError:
                continue
            for marker in markers:
                if marker in text:
                    bad.append(f"real-name marker matched in {s}")
                    break

    if bad:
        print("REAL-DATA SAFETY CHECK FAILED:", file=sys.stderr)
        for b in bad:
            print(f"  - {b}", file=sys.stderr)
        return 1
    print("safety check OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
