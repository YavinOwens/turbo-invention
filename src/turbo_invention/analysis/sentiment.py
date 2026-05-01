from __future__ import annotations
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from turbo_invention.nltk_bootstrap import ensure
ensure()
_SIA = SentimentIntensityAnalyzer()

def score(text: str) -> dict[str, float]:
    return _SIA.polarity_scores(text)
