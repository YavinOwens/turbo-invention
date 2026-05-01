import json
from pathlib import Path
from turbo_invention.compliance.audit import AuditLog


def test_audit_appends_jsonl(tmp_path: Path):
    log = AuditLog(tmp_path / "audit.jsonl")
    log.write("ingest", inputs=["a"], outputs=["b"], n=1)
    log.write("nlp", inputs=["b"], outputs=["c"], n=1)
    lines = (tmp_path / "audit.jsonl").read_text().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["step"] == "ingest"
