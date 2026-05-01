"""Block accidental commit of real SAR / PII data.

Fails (exit 1) if any tracked file path matches a forbidden pattern OR if any
tracked text-like file contains a real account marker (case-insensitive).

Run via pre-push hook and CI. This is a defensive check, not a substitute for
review — it can only catch known markers.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

FORBIDDEN_PREFIXES = ("data/", "secrets/")
FORBIDDEN_SUFFIXES = (".env", ".zip", ".tar.gz", ".tgz", ".7z")
REAL_NAME_MARKERS = ("yavin michael owens", "yavinowens9", "yavinowens87")
SCANNABLE_SUFFIXES = (
    ".json", ".jsonl", ".csv", ".tsv", ".txt", ".md", ".html", ".xml",
    ".yaml", ".yml", ".py", ".ipynb", ".log", ".ndjson",
)
# Exempt: this file legitimately contains the markers as detection strings,
# and the planning docs describe the data context.
EXEMPT_PATHS = ("scripts/check_no_real_data.py",)


def tracked_files() -> list[Path]:
    out = subprocess.check_output(["git", "ls-files"], text=True)
    return [Path(p) for p in out.splitlines() if p]


def main() -> int:
    bad: list[str] = []
    for p in tracked_files():
        s = str(p)
        if any(s.startswith(pre) for pre in FORBIDDEN_PREFIXES):
            bad.append(f"forbidden path: {s}")
            continue
        if any(s.endswith(suf) for suf in FORBIDDEN_SUFFIXES):
            bad.append(f"forbidden suffix: {s}")
            continue
        if s in EXEMPT_PATHS:
            continue
        if p.suffix.lower() in SCANNABLE_SUFFIXES and p.exists():
            try:
                text = p.read_text(encoding="utf-8", errors="ignore").lower()
            except OSError:
                continue
            for marker in REAL_NAME_MARKERS:
                if marker in text:
                    bad.append(f"real-name marker '{marker}' in {s}")
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
