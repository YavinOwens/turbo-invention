from turbo_invention.analysis.sentiment import score

def test_positive_higher_than_negative():
    assert score("I love this so much!")["compound"] > score("I hate this awful thing")["compound"]
