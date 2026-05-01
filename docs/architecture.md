# Architecture

See `docs/superpowers/specs/2026-05-01-turbo-invention-design.md` for the full spec.

```
SAR export ──► sar_ingest ──► corpus (parquet) ──► nlp ──► analysis ──► report
                  │              │                                          ▲
                  ▼              ▼                                          │
              audit log     FAIR metadata ──────► SAFE gate ────────────────┘
```
