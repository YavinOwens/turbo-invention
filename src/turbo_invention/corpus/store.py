from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable, Iterator
import pandas as pd
from turbo_invention.models import Document

_COLUMNS = ["id", "platform", "kind", "timestamp",
            "text", "media_refs", "source_file", "metadata"]


def write_corpus(docs: Iterable[Document], path: Path) -> int:
    rows = [d.model_dump() for d in docs]  # native types (datetime preserved)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        pd.DataFrame(columns=_COLUMNS).to_parquet(path)
        return 0
    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["media_refs"] = df["media_refs"].apply(json.dumps)
    df["metadata"] = df["metadata"].apply(json.dumps)
    df.to_parquet(path, index=False)
    return len(rows)


def read_corpus(path: Path) -> Iterator[Document]:
    df = pd.read_parquet(path)
    for _, row in df.iterrows():
        ts = row["timestamp"]
        ts_out = ts.to_pydatetime() if isinstance(ts, pd.Timestamp) and not pd.isna(ts) else None
        media = row["media_refs"]
        meta = row["metadata"]
        yield Document(
            id=row["id"],
            platform=row["platform"],
            kind=row["kind"],
            timestamp=ts_out,
            text=row["text"],
            media_refs=json.loads(media) if isinstance(media, str) and media else [],
            source_file=row["source_file"],
            metadata=json.loads(meta) if isinstance(meta, str) and meta else {},
        )
