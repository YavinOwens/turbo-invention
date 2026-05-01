from turbo_invention.nlp.ngrams import ngrams

def test_bigrams():
    assert ngrams(["a","b","c"], 2) == [("a","b"), ("b","c")]
