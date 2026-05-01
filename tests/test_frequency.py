from turbo_invention.analysis.frequency import top_terms

def test_top_terms():
    docs = ["machine learning is fun", "machine learning rules", "python is fun"]
    out = top_terms(docs, n=3)
    terms = [t for t, _ in out]
    assert "machine" in terms and "learning" in terms
