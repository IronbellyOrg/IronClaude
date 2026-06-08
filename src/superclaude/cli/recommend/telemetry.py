"""sc-recommend telemetry JSONL appender.

Writes one line per ``/sc:recommend`` invocation to the gitignored, high-churn
``.claude/cache/sc-recommend-events.jsonl``. Each line is a JSON object with
EXACTLY five fields -- ``ts``, ``mode``, ``cache_result``, ``classification_key``,
``duration_ms`` -- and the ``cache_result`` value is validated against the closed
six-value enum before the write.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

# The closed cache_result enum (research/04 section 2.8). No other value is valid.
CACHE_RESULTS = frozenset(
    {
        "hit",
        "miss_no_key",
        "miss_low_confidence",
        "miss_validation_stale",
        "miss_budget_exceeded",
        "cold_inserted",
    }
)

# The exact, ordered field set written per event line. Exactly these five.
EVENT_FIELDS = ("ts", "mode", "cache_result", "classification_key", "duration_ms")


def append_event(
    events_path: Path,
    *,
    mode: str,
    cache_result: str,
    classification_key: str,
    duration_ms: int,
) -> None:
    """Append exactly one telemetry event line to ``events_path``.

    Validates ``cache_result`` against the closed six-value enum (raising
    ``ValueError`` on an out-of-set value) and writes a single newline-terminated
    JSON object carrying ONLY the five ``EVENT_FIELDS``. ``ts`` is stamped here as
    a UTC ISO-8601 timestamp.
    """
    if cache_result not in CACHE_RESULTS:
        raise ValueError(
            f"Invalid cache_result {cache_result!r}; must be one of {sorted(CACHE_RESULTS)}"
        )

    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "cache_result": cache_result,
        "classification_key": classification_key,
        "duration_ms": duration_ms,
    }

    events_path.parent.mkdir(parents=True, exist_ok=True)
    with events_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
