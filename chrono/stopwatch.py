#stopwatch.py
import time
import logging

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.logger = logging.getLogger(__name__)

    # Start the stopwatch.
    def start(self):
        if self.start_time is not None:
            raise RuntimeError("Can't start the stopwatch: Another stopwatch is already running in this Stopwatch instance. Stop it first.")
        self.start_time = time.time()
        self.logger.debug("Stopwatch started")

    # Stop the stopwatch and return time.
    def stop(self):
        if self.start_time is None:
            raise RuntimeError("Can't stop the stopwatch: Stopwatch has not been started yet.")

        end_time = time.time()
        time_interval = end_time - self.start_time
        self.start_time = None

        self.logger.debug(f"Stopwatch stopped after {time_interval}s")
        return time_interval

    # Return how much time has gone.
    def status(self):
        if self.start_time is None:
            raise RuntimeError("There is no active stopwatch.")

        end_time = time.time()
        time_interval = end_time - self.start_time
        return time_interval