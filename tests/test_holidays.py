from datetime import date

from bdoffset.holidays import parse_ics

SAMPLE_ICS = """\
BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTART;VALUE=DATE:20250101
SUMMARY:New Year's Day
END:VEVENT
BEGIN:VEVENT
DTSTART:20250425
SUMMARY:Other Holiday
END:VEVENT
BEGIN:VEVENT
DTSTART;VALUE=DATE:20241225
SUMMARY:Christmas 2024
END:VEVENT
END:VCALENDAR
"""


def test_parses_value_date_form() -> None:
    result = parse_ics(SAMPLE_ICS, {2025})
    assert date(2025, 1, 1) in result


def test_parses_plain_dtstart() -> None:
    result = parse_ics(SAMPLE_ICS, {2025})
    assert date(2025, 4, 25) in result


def test_filters_by_year() -> None:
    result = parse_ics(SAMPLE_ICS, {2025})
    assert date(2024, 12, 25) not in result


def test_includes_all_requested_years() -> None:
    result = parse_ics(SAMPLE_ICS, {2024, 2025})
    assert date(2024, 12, 25) in result
    assert date(2025, 1, 1) in result


def test_empty_data_returns_empty_set() -> None:
    assert parse_ics("", {2025}) == set()


def test_ignores_malformed_dtstart() -> None:
    bad_ics = "DTSTART;VALUE=DATE:not-a-date\n"
    assert parse_ics(bad_ics, {2025}) == set()
