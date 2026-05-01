from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable, Iterator
import pandas as pd
from turbo_invention.models import Document


def write_corpus(docs: Iterable[Document], path: Path) -> int:
    rows = [d.model_dump(mode="json") for d in docs]
    if not rows:
        path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(columns=["id", "platform", "kind", "timestamp",
                              "text", "media_refs", "source_file", "metadata"]
                     ).to_parquet(path)
        return 0
    df = pd.DataFrame(rows)
    df["media_refs"] = df["media_refs"].apply(json.dumps)
    df["metadata"] = df["metadata"].apply(json.dumps)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    return len(rows)


def read_corpus(path: Path) -> Iterator[Document]:
    df = pd.read_parquet(path)
    for _, row in df.iterrows():
        yield Document(
            id=row["id"],
            platform=row["platform"],
            kind=row["kind"],
            timestamp=row["timestamp"] if pd.notna(row["timestamp"]) else None,
            text=row["text"],
            media_refs=json.loads(row["media_refs"]) if row["media_refs"] else [],
            source_file=row["source_file"],
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
        )
