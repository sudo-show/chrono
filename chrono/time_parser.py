# time_parser.py
"""Resolve loose date/time/timezone inputs into an aware datetime."""

import datetime as _dt
from logging import getLogger
from zoneinfo import ZoneInfo

logger = getLogger(__name__)

_KEYWORD_DATES = {"today": 0, "tomorrow": 1, "yesterday": -1}
_DATE_FORMATS = ("%Y-%m-%d", "%d.%m.%Y")


class TimeParseError(ValueError):
    """Raised when an input can't be interpreted."""


def to_datetime(date=None, time=None, day_offset: int = 0, timezone=None):
    """Return an aware datetime.

    date       -- "YYYY-MM-DD" or "DD.MM.YYYY", a date object, or one of
                  "today", "tomorrow", "yesterday". Defaults to today.
    time       -- "HH:MM:SS" (minutes and seconds optional), a tuple of
                  1-3 ints (hour, minute, second), a dict with any of
                  "hour"/"minute"/"second", a time object, or "now".
                  Defaults to midnight.
    day_offset -- days added to the resolved date. Calendar arithmetic:
                  wall-clock time survives DST.
    timezone   -- IANA name, e.g. "Europe/Berlin". Falls back to the
                  system zone with a warning.

    Raises TimeParseError on unusable input.
    """
    tz = _zone(timezone)
    now = _dt.datetime.now(tz)

    date = _parse_date(date, now)
    time = _parse_time(time, now)

    if day_offset:
        date += _dt.timedelta(days=day_offset)

    return _dt.datetime.combine(date, time, tzinfo=tz)


def _parse_date(value, now):
    """Parse into a naive `date`."""
    if value is None:
        return now.date()
    elif isinstance(value, _dt.datetime):
        logger.warning(
            f"Taking only the date from {value!r}. "
            f"Consider passing a plain date without {value.time()} or {value.tzinfo}."
        )
        return value.date()
    elif isinstance(value, _dt.date):
        return value
    elif isinstance(value, str):
        key = value.strip().lower()
        if key in _KEYWORD_DATES:
            return now.date() + _dt.timedelta(days=_KEYWORD_DATES[key])
        for fmt in _DATE_FORMATS:
            try:
                return _dt.datetime.strptime(key, fmt).date()
            except ValueError:
                continue
        raise TimeParseError(f"Unrecognized date format: {value!r}")
    else:
        raise TimeParseError(f"Can't interpret {value!r} as a date.")


def _parse_time(value, now):
    """Parse into a naive `time`."""
    # No time
    if value is None:
        return _dt.time(0, 0)
    # Time is datetime object
    elif isinstance(value, _dt.datetime):
        logger.warning(
            f"Taking only the time from {value!r}. "
            f"Consider passing a plain time without {value.date()} or {value.tzinfo}."
        )
        return value.time()
    # Time is time object
    elif isinstance(value, _dt.time):
        if value.tzinfo is not None:
            logger.warning(
                f"Ignoring tzinfo {value.tzinfo} on `time`; "
                f"use the `timezone` argument instead."
            )
        return value.replace(tzinfo=None)
    # Time is string "HH:mm", "now"
    elif isinstance(value, str):
        key = value.strip().lower()
        if key == "now":
            return now.time().replace(microsecond=0)
        parts = key.split(":")
        if len(parts) > 3:
            raise TimeParseError(f"Too many parts in time: {value!r}")
        try:
            return _build(int(p) for p in parts)
        except ValueError as e:
            raise TimeParseError(f"Unrecognized time format: {value!r}") from e
    # Time is dict {"hour", "minute", "second"}
    elif isinstance(value, dict):
        unknown = set(value) - {"hour", "minute", "second"}
        if unknown:
            raise TimeParseError(f"Unknown time keys: {sorted(unknown)}")
        return _build(
            (value.get("hour", 0), value.get("minute", 0), value.get("second", 0))
        )
    # Time is tuple (hour, minute, second)
    elif isinstance(value, (tuple, list)):
        if not 1 <= len(value) <= 3:
            raise TimeParseError("Time tuple takes 1-3 items: (hour, minute, second).")
        return _build(value)
    else:
        raise TimeParseError(f"Can't interpret {value!r} as a time.")


def _build(parts):
    hour, minute, second = (list(parts) + [0, 0, 0])[:3]
    try:
        return _dt.time(int(hour), int(minute), int(second))
    except (TypeError, ValueError) as e:
        raise TimeParseError(f"Invalid time components: {e}") from e


def _zone(timezone):
    if timezone is None:
        timezone = _dt.datetime.now().astimezone().tzinfo
        logger.warning(f"no `timezone` specified. Using default {timezone}.")
        return timezone
    try:
        return ZoneInfo(timezone)
    except Exception as e:
        raise TimeParseError(f"Unknown timezone: {timezone!r}") from e