from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from turbo_invention.models import DatasetMetadata


def emit_dataset_metadata(path: Path, *, title: str, description: str,
                          creator: str, record_count: int,
                          license: str = "personal-data, not for redistribution",
                          languages: list[str] | None = None) -> DatasetMetadata:
    meta = DatasetMetadata(
        id=str(uuid.uuid4()),
        title=title, description=description, creator=creator,
        created=datetime.now(timezone.utc), license=license,
        record_count=record_count,
        languages=languages or ["en"],
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(meta.model_dump(mode="json"), indent=2))
    return meta
