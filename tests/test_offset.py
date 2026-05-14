from datetime import date

import pytest

from bdoffset.offset import offset_business_days

HOLIDAYS = {date(2025, 1, 1), date(2025, 12, 25), date(2025, 12, 26)}


def test_zero_offset() -> None:
    d = date(2025, 6, 10)  # Tuesday
    assert offset_business_days(d, 0, set()) == d


def test_positive_offset_simple() -> None:
    # Monday + 1 = Tuesday
    assert offset_business_days(date(2025, 6, 9), 1, set()) == date(2025, 6, 10)


def test_positive_offset_crosses_weekend() -> None:
    # Friday + 1 = Monday
    assert offset_business_days(date(2025, 6, 6), 1, set()) == date(2025, 6, 9)


def test_negative_offset_simple() -> None:
    # Tuesday - 1 = Monday
    assert offset_business_days(date(2025, 6, 10), -1, set()) == date(2025, 6, 9)


def test_negative_offset_crosses_weekend() -> None:
    # Monday - 1 = Friday
    assert offset_business_days(date(2025, 6, 9), -1, set()) == date(2025, 6, 6)


def test_skips_holiday() -> None:
    # 2025-12-19 (Fri) + 5 business days, skipping Dec 25 (Thu) and Dec 26 (Fri):
    # Mon Dec 22 (+1), Tue Dec 23 (+2), Wed Dec 24 (+3),
    # Thu Dec 25 skipped (holiday), Fri Dec 26 skipped (holiday),
    # Mon Dec 29 (+4), Tue Dec 30 (+5)
    assert offset_business_days(date(2025, 12, 19), 5, HOLIDAYS) == date(2025, 12, 30)


def test_skips_new_years() -> None:
    # 2024-12-31 (Tue) + 1, skipping Jan 1 holiday → Wed 2025-01-02
    assert offset_business_days(date(2024, 12, 31), 1, HOLIDAYS) == date(2025, 1, 2)


def test_crosses_year_boundary_no_holidays() -> None:
    # 2025-12-31 (Wed) + 2, no holidays in our set → Thu Jan 1 + Fri Jan 2
    assert offset_business_days(date(2025, 12, 31), 2, set()) == date(2026, 1, 2)


def test_negative_large_offset() -> None:
    # 2025-01-10 (Fri) - 5 = Mon Jan 3 (skips weekend between Jan 4-5)
    # Fri Jan 10 → Thu Jan 9 → Wed Jan 8 → Tue Jan 7 → Mon Jan 6 → Fri Jan 3
    assert offset_business_days(date(2025, 1, 10), -5, set()) == date(2025, 1, 3)


@pytest.mark.parametrize("n", [1, 5, 10, 50])
def test_roundtrip(n: int) -> None:
    start = date(2025, 6, 10)  # Tuesday
    forward = offset_business_days(start, n, set())
    back = offset_business_days(forward, -n, set())
    assert back == start
