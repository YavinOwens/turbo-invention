from datetime import datetime, timezone
from turbo_invention.analysis.cadence import per_weekday

def test_per_weekday():
    ts = [datetime(2026, 5, 4, 12, tzinfo=timezone.utc),  # Mon
          datetime(2026, 5, 4, 13, tzinfo=timezone.utc),
          datetime(2026, 5, 6, 10, tzinfo=timezone.utc)]  # Wed
    out = per_weekday(ts)
    assert out["Monday"] == 2
    assert out["Wednesday"] == 1
