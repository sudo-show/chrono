# chrono

Small async timing helpers and date/time resolution.

## `to_datetime(date=None, time=None, day_offset=0, timezone=None)`

Resolves loose date and time inputs into a single aware datetime. Each half accepts several formats; a missing `date` defaults to today, a missing `time` to midnight.

```python
from chrono import to_datetime

to_datetime(time="10:00", timezone="Europe/Berlin")                    # today at 10:00
to_datetime(date="tomorrow", time=(9, 30), timezone="Europe/Berlin")
to_datetime(date="19.07.2026", time="now", timezone="Europe/Berlin")
to_datetime(day_offset=4, time={"hour": 9}, timezone="Europe/Berlin")
```

`date` accepts `"YYYY-MM-DD"`, `"DD.MM.YYYY"`, a `date` object, or one of `"today"`, `"tomorrow"`, `"yesterday"`.

`time` accepts `"HH:MM:SS"` (minutes and seconds optional), `"now"`, a tuple or list of 1–3 ints as `(hour, minute, second)`, a dict with any of `"hour"`/`"minute"`/`"second"`, or a `time` object.

`day_offset` shifts the resolved date by whole days, negatives included. Calendar arithmetic — wall-clock time survives DST.

`timezone` is an IANA name. Omitting it falls back to the system zone and logs a warning.

Passing a `datetime` to either `date` or `time` takes the relevant half and logs a warning. An aware `time` has its zone stripped, also with a warning — use `timezone` instead.

Raises `TimeParseError` (a `ValueError`) on unusable input.

## `to_timezone(value, timezone)`

Re-expresses an aware datetime in another zone, preserving the instant.

```python
from chrono import to_datetime, to_timezone

berlin = to_datetime(time="14:00", timezone="Europe/Berlin")
tokyo = to_timezone(berlin, "Asia/Tokyo")   # same moment, 21:00 Tokyo
```

Naive input is rejected — there's no way to know which zone it's already in. Attach one with `to_datetime` first.

## `wait_until(date=None, time=None, day_offset=0, timezone=None)`

Sleeps until a wall-clock target. Arguments match `to_datetime`. If the target is already past, it rolls forward one day.

```python
from chrono import wait_until

await wait_until(time="09:00", timezone="Europe/Berlin")
await wait_until(date="tomorrow", time="09:00", timezone="Europe/Berlin")
await wait_until(day_offset=4, time="08:55", timezone="Europe/Berlin")
```

The rollover is unconditional, so an explicitly past date jumps forward a day rather than returning immediately.

## `wait_for(duration, units="s")`

Sleeps for a fixed duration. `units` is one of `"s"`, `"m"`, `"h"`, `"d"` — defaults to seconds.

```python
from chrono import wait_for

await wait_for(30)          # 30 seconds
await wait_for(5, "m")      # 5 minutes
await wait_for(2, "h")      # 2 hours
```

Raises `ValueError` on an unknown unit.

## `Stopwatch`

Measures elapsed time between `start()` and `stop()`.

```python
from chrono import Stopwatch

sw = Stopwatch()
sw.start()
...
elapsed = sw.stop()   # float, seconds

sw.start()
...
elapsed_so_far = sw.status()   # peek without stopping
```

- `start()` raises `RuntimeError` if already running.
- `stop()` / `status()` raise `RuntimeError` if not started.
- One stopwatch instance tracks one run at a time — call `stop()` before `start()`ing again.
- Return values are raw floats (unrounded) — round at the point you display them, not before.