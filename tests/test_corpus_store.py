from datetime import datetime, timezone
from pathlib import Path
from turbo_invention.models import Document
from turbo_invention.corpus.store import write_corpus, read_corpus


def test_write_and_read_roundtrip(tmp_path: Path):
    docs = [
        Document(
            id="abc", platform="facebook", kind="post",
            timestamp=datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc),
            text="hello world", source_file="posts/x.json",
        ),
        Document(
            id="def", platform="facebook", kind="comment",
            timestamp=datetime(2026, 1, 2, 12, 0, tzinfo=timezone.utc),
            text="another", source_file="comments/x.json",
        ),
    ]
    out = tmp_path / "corpus.parquet"
    write_corpus(docs, out)
    back = list(read_corpus(out))
    assert len(back) == 2
    assert back[0].text == "hello world"
    assert back[1].kind == "comment"
