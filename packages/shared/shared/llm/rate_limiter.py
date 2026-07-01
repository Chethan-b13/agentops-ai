"""
GeminiRateLimiter — thread-safe free-tier quota enforcer.

Free-tier limits (Gemini 2.0 Flash Lite):
  - 15 Requests Per Minute  → minimum 4 s between calls
  - 500 Requests Per Day    → hard stop after 500 calls
"""

import threading
import time
from datetime import date


class GeminiRateLimiter:
    """Singleton rate limiter for the Gemini free tier.

    Call ``wait()`` before every Gemini API request.  It returns the
    number of seconds it actually slept so callers can log the overhead.
    """

    # Free-tier hard limits
    MAX_RPM: int = 15
    MAX_RPD: int = 500

    # Minimum gap between consecutive calls (seconds)
    _MIN_INTERVAL: float = 60.0 / MAX_RPM  # 4.0 s

    # --- Singleton boilerplate ---
    _instance: "GeminiRateLimiter | None" = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> "GeminiRateLimiter":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._init()
                    cls._instance = instance
        return cls._instance

    def _init(self) -> None:
        self._call_lock = threading.Lock()
        self._last_call_time: float = 0.0
        self._daily_count: int = 0
        self._count_date: date = date.today()

    # ------------------------------------------------------------------

    def wait(self) -> float:
        """Block until it is safe to make the next Gemini call.

        Returns:
            wait_seconds (float): how long this call slept.
                                  0.0 means no throttling was needed.
        Raises:
            RuntimeError: when the daily request quota is exhausted.
        """
        with self._call_lock:
            today = date.today()

            # Reset daily counter on a new calendar day
            if today != self._count_date:
                self._daily_count = 0
                self._count_date = today

            if self._daily_count >= self.MAX_RPD:
                raise RuntimeError(
                    f"Gemini daily quota exhausted: {self.MAX_RPD} requests "
                    f"already made today ({today})."
                )

            now = time.monotonic()
            elapsed = now - self._last_call_time
            sleep_for = max(0.0, self._MIN_INTERVAL - elapsed)

            if sleep_for > 0:
                time.sleep(sleep_for)

            self._last_call_time = time.monotonic()
            self._daily_count += 1

            return sleep_for

    @property
    def daily_count(self) -> int:
        """How many Gemini calls have been made today."""
        return self._daily_count

    @property
    def remaining_today(self) -> int:
        """How many Gemini calls remain in today's quota."""
        return max(0, self.MAX_RPD - self._daily_count)
