from __future__ import annotations
from collections import Counter
from typing import Iterable
from turbo_invention.nlp.tokenize import words
from turbo_invention.nlp.normalize import normalize_token
from turbo_invention.nlp.stopwords import is_stopword
from turbo_invention.nlp.lemmatize import lemma


def _terms(text: str) -> list[str]:
    out = []
    for tok in words(text):
        n = normalize_token(tok)
        if not n or is_stopword(n):
            continue
        out.append(lemma(n))
    return out


def top_terms(docs: Iterable[str], n: int = 50) -> list[tuple[str, int]]:
    c: Counter[str] = Counter()
    for d in docs:
        c.update(_terms(d))
    return c.most_common(n)
