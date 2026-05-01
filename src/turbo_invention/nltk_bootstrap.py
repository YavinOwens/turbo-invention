"""Run once to download required NLTK corpora into ~/.nltk_data."""
from __future__ import annotations
import nltk

REQUIRED = ["punkt", "punkt_tab", "stopwords", "wordnet", "vader_lexicon"]


def ensure() -> None:
    for pkg in REQUIRED:
        try:
            nltk.data.find(f"tokenizers/{pkg}" if "punkt" in pkg
                           else f"corpora/{pkg}" if pkg in ("stopwords", "wordnet")
                           else f"sentiment/{pkg}")
        except LookupError:
            nltk.download(pkg, quiet=True)


if __name__ == "__main__":
    ensure()
    print("NLTK corpora ready.")
