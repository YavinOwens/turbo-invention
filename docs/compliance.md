# Compliance alignment

## UK GDPR / DPA 2018
- Lawful basis = data subject's own data, processed locally.
- Article 5 minimisation: only fields used by the analysis are retained in the corpus.
- No data leaves the local machine. `.gitignore` and `scripts/check_no_real_data.py` enforce this; CI re-runs the check.

## ICO Anonymisation guidance
- `compliance/pii.py` redacts emails, UK phones, UK postcodes, and a configurable name list before any text is written to a report.

## DAMA-UK / data engineering
- `Document` and `DatasetMetadata` carry an explicit `schema_version`.
- `compliance/audit.py` writes a JSONL lineage entry per pipeline step.

## FAIR
- **Findable:** `dataset.json` carries a UUID and descriptive title.
- **Accessible:** local-only access notes documented in metadata.
- **Interoperable:** parquet corpus + JSON metadata.
- **Reusable:** schema versioned; license stated.

## SAFE / Five Safes
- **Safe People** — only the data subject runs this on their machine.
- **Safe Projects** — purpose stated in the report header.
- **Safe Settings** — local environment, no cloud upload.
- **Safe Data** — PII redacted before output.
- **Safe Outputs** — the report is gitignored; sharing it requires a deliberate copy.
- All five must be asserted at the CLI (`--safe-*` flags) or the export refuses.
