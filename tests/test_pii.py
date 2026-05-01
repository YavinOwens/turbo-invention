from turbo_invention.compliance.pii import redact

def test_redacts_email_phone_postcode():
    text = "Contact me at jane@example.com or 07712345678 or SW1A 1AA"
    out = redact(text)
    assert "jane@example.com" not in out
    assert "07712345678" not in out
    assert "SW1A 1AA" not in out
    assert "[EMAIL]" in out and "[PHONE]" in out and "[POSTCODE]" in out

def test_redacts_known_names():
    text = "Hello Alice Smith and Bob"
    out = redact(text, names=["Alice Smith", "Bob"])
    assert "Alice Smith" not in out
    assert "Bob" not in out
