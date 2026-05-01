from __future__ import annotations
from nltk.corpus import stopwords
from turbo_invention.nltk_bootstrap import ensure
ensure()
EN = set(stopwords.words("english"))

def is_stopword(tok: str) -> bool:
    return tok in EN
