from turbo_invention.nlp.tokenize import sentences, words

def test_sentences():
    assert sentences("Hello world. How are you?") == ["Hello world.", "How are you?"]

def test_words():
    assert words("Hello, world!") == ["Hello", ",", "world", "!"]
