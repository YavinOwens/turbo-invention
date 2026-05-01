import json
from pathlib import Path
from turbo_invention.compliance.fair import emit_dataset_metadata


def test_emit_dataset_json(tmp_path: Path):
    out = tmp_path / "dataset.json"
    emit_dataset_metadata(out, title="t", description="d", creator="c",
                          record_count=42)
    data = json.loads(out.read_text())
    for key in ("id","title","description","creator","created","license",
                "schema_version","record_count","languages","access_notes"):
        assert key in data
    assert data["record_count"] == 42
