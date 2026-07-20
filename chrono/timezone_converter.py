# timezone_converter.py
import datetime as _dt
from zoneinfo import ZoneInfo
from logging import getLogger
logger = getLogger(__name__)

class TimezoneConverterError(ValueError):
    """Raised when an input can't be interpreted."""

def to_timezone(value, timezone):
    """Return `value` expressed in `timezone`.

    value    -- an aware datetime. Naive input is rejected: there's no way
                to know what zone it's already in.
    timezone -- IANA name, e.g. "Europe/Berlin".
    """
    if not isinstance(value, _dt.datetime):
        raise TimezoneConverterError(f"Can't convert {value!r}: expected a datetime.")
    if value.tzinfo is None:
        raise TimezoneConverterError("Can't convert a naive datetime — its zone is unknown.")
    return value.astimezone(_zone(timezone))

def _zone(timezone):
    if timezone is None:
        timezone = _dt.datetime.now().astimezone().tzinfo
        logger.warning(f"no `timezone` specified. Using default {timezone}.")
        return timezone
    try:
        return ZoneInfo(timezone)
    except Exception as e:
        raise TimezoneConverterError(f"Unknown timezone: {timezone!r}") from e