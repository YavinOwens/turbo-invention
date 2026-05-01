from __future__ import annotations
from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field

SCHEMA_VERSION = "1.0.0"

Platform = Literal["facebook", "instagram", "google", "x", "other"]
Kind = Literal["post", "comment", "message", "caption", "search", "other"]


class Document(BaseModel):
    id: str
    platform: Platform
    kind: Kind
    timestamp: datetime | None = None
    text: str
    media_refs: list[str] = Field(default_factory=list)
    source_file: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class DatasetMetadata(BaseModel):
    id: str
    title: str
    description: str
    creator: str
    created: datetime
    license: str
    schema_version: str = SCHEMA_VERSION
    record_count: int
    languages: list[str] = Field(default_factory=lambda: ["en"])
    access_notes: str = "local-only; not committed to git"
