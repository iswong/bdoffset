from __future__ import annotations

import argparse
import math
from datetime import date

from bdoffset.holidays import fetch_holidays
from bdoffset.offset import offset_business_days


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}': expected yyyy-MM-dd") from None


def _years_needed(start: date, n: int) -> set[int]:
    # Each year has ~200–250 business days; n/200 gives a safe upper bound on extra years.
    span = math.ceil(abs(n) / 200) + 1
    if n >= 0:
        return set(range(start.year, start.year + span + 1))
    return set(range(start.year - span, start.year + 1))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="bdoffset",
        description="Offset a date by N business days for a given exchange.",
    )
    parser.add_argument("--date", required=True, type=_parse_date, metavar="YYYY-MM-DD")
    parser.add_argument("--n", required=True, type=int, metavar="N")
    parser.add_argument("--exch", required=True, choices=["HK", "US", "LON", "TYO"])
    args = parser.parse_args()

    years = _years_needed(args.date, args.n)
    holidays = fetch_holidays(args.exch, years)
    result = offset_business_days(args.date, args.n, holidays)
    print(result.isoformat())
