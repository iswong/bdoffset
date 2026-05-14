from __future__ import annotations

import re
import urllib.error
import urllib.request
from datetime import date

EXCHANGE_ICS: dict[str, str] = {
    "HK": "https://calendar.google.com/calendar/ical/en.hong_kong%23holiday%40group.v.calendar.google.com/public/basic.ics",
    "US": "https://calendar.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics",
    "LON": "https://www.gov.uk/bank-holidays/england-and-wales.ics",
    "TYO": "https://calendar.google.com/calendar/ical/en.japanese%23holiday%40group.v.calendar.google.com/public/basic.ics",
}

# Matches both DTSTART:yyyyMMdd and DTSTART;VALUE=DATE:yyyyMMdd
_DTSTART_RE = re.compile(r"^DTSTART(?:;[^:]+)?:(\d{8})")


def fetch_holidays(exch: str, years: set[int]) -> set[date]:
    url = EXCHANGE_ICS[exch]
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:  # noqa: S310
            data = resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, OSError) as exc:
        raise SystemExit(f"Error fetching holiday calendar for {exch}: {exc}") from exc
    return parse_ics(data, years)


def parse_ics(data: str, years: set[int]) -> set[date]:
    holidays: set[date] = set()
    for line in data.splitlines():
        m = _DTSTART_RE.match(line)
        if not m:
            continue
        raw = m.group(1)
        try:
            d = date(int(raw[:4]), int(raw[4:6]), int(raw[6:8]))
        except ValueError:
            continue
        if d.year in years:
            holidays.add(d)
    return holidays
