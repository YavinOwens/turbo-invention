from turbo_invention.nlp.normalize import normalize_token

def test_lowercase_strip_punct():
    assert normalize_token("Hello,") == "hello"

def test_drops_pure_punct():
    assert normalize_token("!!!") == ""
