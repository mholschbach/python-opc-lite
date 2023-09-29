from datetime import datetime, timezone, timedelta
from opc.datetime import Dt


def test_dt_to_w3cdtf_from_timezone_aware_dt_object():
    tz = timezone(timedelta(hours=5, minutes=30))
    dt_obj = datetime(year=2023, month=9, day=26,
                      hour=20, minute=31, second=32, tzinfo=tz)
    assert "2023-09-26T15:01:32Z" == Dt.to_w3cdtf(dt_obj)

    tz = timezone(timedelta(hours=-4))
    dt_obj = datetime(year=2023, month=9, day=26,
                      hour=20, minute=31, second=32, tzinfo=tz)
    assert "2023-09-27T00:31:32Z" == Dt.to_w3cdtf(dt_obj)


def test_dt_from_w3cdtf_from_string():
    dt_stamp = Dt.from_w3cdtf("2023-09-26T15:01:32Z").timestamp()
    assert dt_stamp == datetime(year=2023, month=9, day=26,
                                hour=20, minute=31, second=32).timestamp()
