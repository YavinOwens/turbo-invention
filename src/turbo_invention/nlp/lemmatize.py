from __future__ import annotations
from nltk.stem import WordNetLemmatizer
from turbo_invention.nltk_bootstrap import ensure
ensure()
_LEM = WordNetLemmatizer()

def lemma(tok: str) -> str:
    return _LEM.lemmatize(tok)
