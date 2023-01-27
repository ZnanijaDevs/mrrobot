import pytest
from mrrobot.util import ts_to_date


def test_ts_to_date():
    test_cases = {
        "1674730929.142549": "26.01.2023 14:02:09",
        "1674570159.338679": "24.01.2023 17:22:39",
        1674570159.338679: "24.01.2023 17:22:39",
        1: "01.01.1970 03:00:01",
        1671545427.043229: "20.12.2022 17:10:27"
    }

    for ts, value in test_cases.items():
        assert ts_to_date(ts) == value


def test_ts_to_date_with_invalid_arg():
    with pytest.raises(ValueError):
        ts_to_date("")
