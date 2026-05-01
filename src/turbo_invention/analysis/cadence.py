from __future__ import annotations
from collections import Counter
from datetime import datetime
from typing import Iterable

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"]


def per_weekday(timestamps: Iterable[datetime]) -> dict[str, int]:
    c = Counter(WEEKDAYS[t.weekday()] for t in timestamps if t)
    return {d: c.get(d, 0) for d in WEEKDAYS}


def per_hour(timestamps: Iterable[datetime]) -> dict[int, int]:
    c = Counter(t.hour for t in timestamps if t)
    return {h: c.get(h, 0) for h in range(24)}
