from __future__ import annotations
import re
from typing import Iterable

EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE = re.compile(r"\b(?:\+?44|0)\d{9,10}\b")
UK_POSTCODE = re.compile(
    r"\b[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b", re.IGNORECASE)


def redact(text: str, names: Iterable[str] = ()) -> str:
    out = EMAIL.sub("[EMAIL]", text)
    out = PHONE.sub("[PHONE]", out)
    out = UK_POSTCODE.sub("[POSTCODE]", out)
    for n in sorted(set(names), key=len, reverse=True):
        if n:
            out = re.sub(re.escape(n), "[NAME]", out)
    return out
