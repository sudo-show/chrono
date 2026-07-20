# waiter.py
import asyncio
import logging
from datetime import datetime
from typing import Literal

from .time_parser import to_datetime

logger = logging.getLogger(__name__)

_UNITS = {
    "s": (1, "seconds"),
    "m": (60, "minutes"),
    "h": (3600, "hours"),
    "d": (86400, "days"),
}


async def wait_until(date=None, time=None, day_offset: int = 0, timezone=None):
    """Sleep until the given date and time.

    Arguments match `to_datetime`. Returns immediately if the target
    is already past.
    """
    target = to_datetime(date=date, time=time, day_offset=day_offset, timezone=timezone)

    delay = (target - datetime.now(target.tzinfo)).total_seconds()
    if delay <= 0:
        target = to_datetime(date=target.date(), time=target.time(),
                             day_offset=1, timezone=str(target.tzinfo))

    logger.info(f"Waiting until {target} ({delay:.1f}s).")
    await asyncio.sleep(delay)


async def wait_for(duration: float, units: Literal["s", "m", "h", "d"] = "s"):
    """Sleep for `duration` in the given units."""
    if units not in _UNITS:
        raise ValueError(f"Unknown unit {units!r}: expected one of {sorted(_UNITS)}.")

    factor, name = _UNITS[units]
    logger.debug(f"Waiting for {duration:.2f} {name}.")
    await asyncio.sleep(duration * factor)