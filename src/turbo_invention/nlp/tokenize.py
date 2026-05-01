from __future__ import annotations
from nltk.tokenize import sent_tokenize, word_tokenize
from turbo_invention.nltk_bootstrap import ensure
ensure()

def sentences(text: str) -> list[str]:
    return sent_tokenize(text)

def words(text: str) -> list[str]:
    return word_tokenize(text)
