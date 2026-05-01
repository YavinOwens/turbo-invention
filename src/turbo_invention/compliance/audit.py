from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuditLog:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, step: str, **fields: Any) -> None:
        record = {"ts": datetime.now(timezone.utc).isoformat(),
                  "step": step, **fields}
        with self.path.open("a") as f:
            f.write(json.dumps(record, default=str) + "\n")
