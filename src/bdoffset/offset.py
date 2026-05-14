from __future__ import annotations

from datetime import date, timedelta


def offset_business_days(start: date, n: int, holidays: set[date]) -> date:
    if n == 0:
        return start
    step = 1 if n > 0 else -1
    current = start
    remaining = abs(n)
    while remaining > 0:
        current += timedelta(days=step)
        if current.weekday() < 5 and current not in holidays:
            remaining -= 1
    return current
