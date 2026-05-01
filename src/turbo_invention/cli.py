from __future__ import annotations
from pathlib import Path
import typer
from rich import print
from turbo_invention.sar_ingest.facebook import FacebookParser
from turbo_invention.corpus.store import write_corpus, read_corpus
from turbo_invention.analysis.report import build_report
from turbo_invention.compliance.fair import emit_dataset_metadata
from turbo_invention.compliance.audit import AuditLog
from turbo_invention.compliance.safe import five_safes_gate

app = typer.Typer(add_completion=False, help="turbo-invention SAR corpus toolkit")


@app.command()
def ingest(source: Path = typer.Option(..., exists=True, file_okay=False),
           out: Path = typer.Option(..., file_okay=False),
           dry_run: bool = typer.Option(False, "--dry-run")):
    parser = FacebookParser(source)
    if dry_run:
        parser.dry_run()
        return
    out.mkdir(parents=True, exist_ok=True)
    audit = AuditLog(out / "audit.jsonl")
    docs = list(parser.iter_documents())
    n = write_corpus(docs, out / "corpus.parquet")
    audit.write("ingest", source=str(source), records=n)
    print(f"[green]Wrote[/] {n} documents to {out/'corpus.parquet'}")


@app.command()
def report(corpus: Path = typer.Option(..., exists=True, file_okay=False),
           out: Path = typer.Option(..., file_okay=True),
           redact_name: list[str] = typer.Option([], "--redact-name"),
           safe_people: bool = False, safe_project: bool = False,
           safe_setting: bool = False, safe_data: bool = False,
           safe_outputs: bool = False):
    five_safes_gate(people=safe_people, project=safe_project,
                    setting=safe_setting, data=safe_data, outputs=safe_outputs)
    docs = list(read_corpus(corpus / "corpus.parquet"))
    build_report(docs, out, redact_names=redact_name)
    print(f"[green]Wrote report to[/] {out}")


@app.command()
def fair(corpus: Path = typer.Option(..., exists=True, file_okay=False),
         out: Path = typer.Option(...),
         title: str = "Personal SAR corpus",
         creator: str = "data subject"):
    docs = list(read_corpus(corpus / "corpus.parquet"))
    emit_dataset_metadata(out, title=title, description="Personal SAR corpus",
                          creator=creator, record_count=len(docs))
    print(f"[green]Wrote FAIR metadata to[/] {out}")
