from __future__ import annotations
from pathlib import Path
from typing import Iterable
from turbo_invention.models import Document
from turbo_invention.analysis.frequency import top_terms
from turbo_invention.analysis.cadence import per_weekday, per_hour
from turbo_invention.analysis.sentiment import score
from turbo_invention.compliance.pii import redact


def build_report(docs: Iterable[Document], out_path: Path,
                 redact_names: list[str] | None = None) -> None:
    docs = list(docs)
    texts = [d.text for d in docs]
    timestamps = [d.timestamp for d in docs if d.timestamp]
    terms = top_terms(texts, n=25)
    weekday = per_weekday(timestamps)
    hours = per_hour(timestamps)
    sentiments = [score(t)["compound"] for t in texts]
    avg_sent = sum(sentiments) / len(sentiments) if sentiments else 0.0

    lines = [
        "# Self-Portrait",
        "",
        f"_Total documents analysed: {len(docs)}_",
        "",
        "## Top terms",
        "",
        *[f"- {t}: {c}" for t, c in terms],
        "",
        "## Posting cadence",
        "",
        "### By weekday",
        *[f"- {d}: {n}" for d, n in weekday.items()],
        "",
        "### By hour",
        *[f"- {h:02d}:00 — {n}" for h, n in hours.items()],
        "",
        "## Sentiment",
        "",
        f"- Average VADER compound: {avg_sent:+.3f}",
        "",
        "## Compliance notes",
        "",
        "- All text below has passed PII redaction (regex + name list).",
        "- This report was generated locally; the underlying corpus is "
        "gitignored and never pushed.",
        "- Dataset metadata: see `dataset.json` (FAIR / DCAT-lite).",
        "- Five Safes gate must be asserted via the CLI to export.",
    ]
    body = "\n".join(lines)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(redact(body, names=redact_names or []))
