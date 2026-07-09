# waiter / stopwatch

Small async timing helpers.

## `wait_until(hour, minute, offset_minutes=0, timezone=None)`

Sleeps until the next occurrence of a specific wall-clock time. Timezone-aware — handles DST correctly. If the target time has already passed today, it rolls to tomorrow automatically.

```python
from waiter import wait_until

await wait_until(9, 0, timezone="Europe/Berlin")          # sleep until next 9:00 Berlin time
await wait_until(9, 0, offset_minutes=-5, timezone="Europe/Berlin")  # 8:55 Berlin time
```

Raises `ValueError` if `timezone` isn't provided.

## `wait_for(wait_time, units="s")`

Sleeps for a fixed duration. `units` is one of `"s"`, `"m"`, `"h"`, `"d"` — defaults to seconds.

```python
from waiter import wait_for

await wait_for(30)          # 30 seconds
await wait_for(5, "m")      # 5 minutes
await wait_for(2, "h")      # 2 hours
```

## `Stopwatch`

Measures elapsed time between `start()` and `stop()`.

```python
from stopwatch import Stopwatch

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