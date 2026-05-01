from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Iterator
from turbo_invention.models import Document
from turbo_invention.sar_ingest.base import SARParser

KNOWN_POST_TEXT_KEYS = ("post",)
KNOWN_KEYS_AT_TOP = {"timestamp", "attachments", "data", "title", "tags"}


def _ts(epoch: int | None) -> datetime | None:
    return datetime.fromtimestamp(epoch, tz=timezone.utc) if epoch else None


def _hash(*parts: str) -> str:
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:16]


class FacebookParser(SARParser):
    def iter_documents(self) -> Iterator[Document]:
        yield from self._iter_posts()
        yield from self._iter_comments()

    def _iter_posts(self) -> Iterator[Document]:
        posts_dir = self.root / "your_facebook_activity" / "posts"
        if not posts_dir.exists():
            return
        for jf in sorted(posts_dir.glob("your_posts*.json")):
            data = json.loads(jf.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                continue
            for i, entry in enumerate(data):
                text = self._extract_post_text(entry)
                if not text:
                    continue
                yield Document(
                    id=_hash("fb", "post", str(jf.name), str(i)),
                    platform="facebook", kind="post",
                    timestamp=_ts(entry.get("timestamp")),
                    text=text,
                    source_file=str(jf.relative_to(self.root)),
                    metadata={"title": entry.get("title", "")},
                )

    def _iter_comments(self) -> Iterator[Document]:
        cf = self.root / "your_facebook_activity" / "comments_and_reactions" / "comments.json"
        if not cf.exists():
            return
        data = json.loads(cf.read_text(encoding="utf-8"))
        items = data.get("comments_v2", []) if isinstance(data, dict) else []
        for i, entry in enumerate(items):
            for d in entry.get("data", []):
                comment = d.get("comment") or {}
                text = comment.get("comment", "")
                if not text:
                    continue
                yield Document(
                    id=_hash("fb", "comment", str(cf.name), str(i)),
                    platform="facebook", kind="comment",
                    timestamp=_ts(comment.get("timestamp") or entry.get("timestamp")),
                    text=text,
                    source_file=str(cf.relative_to(self.root)),
                    metadata={"title": entry.get("title", ""),
                              "author": comment.get("author", "")},
                )

    def _extract_post_text(self, entry: dict[str, Any]) -> str:
        for d in entry.get("data", []) or []:
            if isinstance(d, dict):
                for k in KNOWN_POST_TEXT_KEYS:
                    if isinstance(d.get(k), str) and d[k].strip():
                        return d[k]
        return ""

    def dry_run(self) -> None:
        for jf in sorted(self.root.rglob("*.json")):
            try:
                data = json.loads(jf.read_text(encoding="utf-8", errors="ignore"))
            except json.JSONDecodeError:
                print(f"[skip] {jf.relative_to(self.root)} (not JSON)")
                continue
            sample = data[0] if isinstance(data, list) and data else (
                data if isinstance(data, dict) else {})
            keys = sorted(sample.keys()) if isinstance(sample, dict) else []
            unknown = [k for k in keys if k not in KNOWN_KEYS_AT_TOP]
            print(f"{jf.relative_to(self.root)}  keys={keys}  unknown={unknown}")
