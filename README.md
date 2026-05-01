# turbo-invention

Educational NLTK-first toolkit for turning a personal Subject Access Request (SAR)
export into a corpus and a self-portrait report. Demonstrates UK GDPR / DPA 2018,
DAMA-UK, FAIR, and the Five Safes (SAFE) in working code.

> ⚠️ **Real personal SAR data must never be committed to this repo.** All real
> data is read from a local-only path. Synthetic fixtures back the test suite.
> A safety script blocks accidental commits.

See `docs/sar-guide.md` to file a SAR. See `docs/compliance.md` for the
standards alignment. See `docs/sar-schema-2026-04-28.md` for the schema this
parser was built against (Meta changes it without notice — re-check first).

## Quickstart (local only)

```bash
pyenv local 3.12.6
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m turbo_invention.nltk_bootstrap

turbo-invention ingest --source <path-to-SAR> --out data/corpus/
turbo-invention analyze --corpus data/corpus/ --out data/reports/
turbo-invention report  --corpus data/corpus/ --out data/reports/self_portrait.md
```
