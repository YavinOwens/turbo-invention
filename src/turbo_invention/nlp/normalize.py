from __future__ import annotations
import string

def normalize_token(tok: str) -> str:
    cleaned = tok.strip().lower().strip(string.punctuation)
    if not cleaned or all(c in string.punctuation for c in cleaned):
        return ""
    return cleaned
