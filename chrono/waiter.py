#waiter.py
import logging
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Literal


logger = logging.getLogger(__name__)


async def wait_until(hour: int, minute: int, offset_minutes: int = 0, timezone: str = None):
    if timezone is None:
        raise ValueError("No timezone provided")

    now = datetime.now(ZoneInfo(timezone))

    target = now.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    ) + timedelta(minutes=offset_minutes)

    # Always schedule for the next occurrence
    if target <= now:
        target += timedelta(days=1)

    logger.info(f"Waiting until {target}")
    await asyncio.sleep((target - now).total_seconds())

async def wait_for(self, wait_time: int, units: Literal["s", "m", "h", "d"] = "s"):
    if units == "m":
        wait_seconds = wait_time * 60
        units = "minutes"
    elif units == "h":
        wait_seconds = wait_time * 3600
        units = "hours"
    elif units == "d":
        wait_seconds = wait_time * 86400
        units = "days"

    logger.info(f"Waiting {wait_time} {units}")
    await asyncio.sleep(wait_seconds)