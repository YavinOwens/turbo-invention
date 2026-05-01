from datetime import datetime, timezone
from pathlib import Path
from turbo_invention.models import Document
from turbo_invention.analysis.report import build_report


def test_report_contains_sections(tmp_path: Path):
    docs = [
        Document(id="a", platform="facebook", kind="post",
                 timestamp=datetime(2026, 1, 1, 12, tzinfo=timezone.utc),
                 text="machine learning python is fun",
                 source_file="x.json"),
        Document(id="b", platform="facebook", kind="comment",
                 timestamp=datetime(2026, 1, 2, 13, tzinfo=timezone.utc),
                 text="data data data analysis", source_file="x.json"),
    ]
    out = tmp_path / "report.md"
    build_report(docs, out, redact_names=["Test User"])
    text = out.read_text()
    for header in ("# Self-Portrait", "## Top terms", "## Posting cadence",
                   "## Sentiment", "## Compliance notes"):
        assert header in text
