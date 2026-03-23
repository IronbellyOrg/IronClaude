"""Benchmark test for wiring analysis performance.

Validates that run_wiring_analysis completes within acceptable latency
on a synthetic codebase, ensuring P95 stays under the 5-second threshold.
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from superclaude.cli.audit.wiring_config import WiringConfig
from superclaude.cli.audit.wiring_gate import run_wiring_analysis

# Synthetic Python file templates with realistic class/function definitions.
_SYNTHETIC_MODULES: list[tuple[str, str]] = [
    (
        "models.py",
        """\
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def validate(self) -> bool:
        return bool(self.name and self.email)

class Organisation:
    def __init__(self, title: str):
        self.title = title

    def member_count(self) -> int:
        return 0
""",
    ),
    (
        "service.py",
        """\
from typing import Any

class UserService:
    def create_user(self, data: dict[str, Any]) -> dict:
        return {"id": 1, **data}

    def delete_user(self, user_id: int) -> bool:
        return True

def fetch_remote_config(endpoint: str) -> dict:
    return {"endpoint": endpoint, "timeout": 30}
""",
    ),
    (
        "repository.py",
        """\
class BaseRepository:
    def find_by_id(self, record_id: int):
        raise NotImplementedError

    def find_all(self):
        raise NotImplementedError

class UserRepository(BaseRepository):
    def find_by_id(self, record_id: int):
        return {"id": record_id}

    def find_all(self):
        return []
""",
    ),
    (
        "validators.py",
        """\
import re

def validate_email(email: str) -> bool:
    pattern = r"^[\\w.+-]+@[\\w-]+\\.[\\w.]+$"
    return bool(re.match(pattern, email))

def validate_name(name: str) -> bool:
    return len(name) >= 2

class FieldValidator:
    def __init__(self, field_name: str):
        self.field_name = field_name

    def check(self, value: str) -> bool:
        return bool(value)
""",
    ),
    (
        "utils.py",
        """\
import hashlib
from pathlib import Path

def hash_content(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()

def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
""",
    ),
    (
        "config.py",
        """\
from dataclasses import dataclass, field

@dataclass
class AppConfig:
    debug: bool = False
    log_level: str = "INFO"
    max_retries: int = 3

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    pool_size: int = 10

def merge_configs(*configs: dict) -> dict:
    merged: dict = {}
    for cfg in configs:
        merged.update(cfg)
    return merged
""",
    ),
    (
        "middleware.py",
        """\
from typing import Callable, Any

class Middleware:
    def __init__(self, handler: Callable):
        self.handler = handler

    def process(self, request: dict) -> Any:
        return self.handler(request)

class LoggingMiddleware(Middleware):
    def process(self, request: dict) -> Any:
        return super().process(request)

def chain_middleware(*layers: Middleware) -> Middleware:
    return layers[0] if layers else Middleware(lambda r: r)
""",
    ),
    (
        "events.py",
        """\
from typing import Callable

class EventBus:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def subscribe(self, event: str, callback: Callable) -> None:
        self._listeners.setdefault(event, []).append(callback)

    def publish(self, event: str, data: dict) -> None:
        for cb in self._listeners.get(event, []):
            cb(data)

def create_event(name: str, payload: dict) -> dict:
    return {"name": name, "payload": payload}
""",
    ),
    (
        "transformers.py",
        """\
from typing import Any

class DataTransformer:
    def transform(self, data: Any) -> Any:
        raise NotImplementedError

class UpperCaseTransformer(DataTransformer):
    def transform(self, data: str) -> str:
        return data.upper()

class TrimTransformer(DataTransformer):
    def transform(self, data: str) -> str:
        return data.strip()

def apply_pipeline(data: Any, *transformers: DataTransformer) -> Any:
    for t in transformers:
        data = t.transform(data)
    return data
""",
    ),
    (
        "cache.py",
        """\
from typing import Any

class SimpleCache:
    def __init__(self, max_size: int = 128):
        self._store: dict[str, Any] = {}
        self._max_size = max_size

    def get(self, key: str) -> Any | None:
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        if len(self._store) >= self._max_size:
            oldest = next(iter(self._store))
            del self._store[oldest]
        self._store[key] = value

    def invalidate(self, key: str) -> bool:
        return self._store.pop(key, None) is not None
""",
    ),
    (
        "scheduler.py",
        """\
from typing import Callable

class Task:
    def __init__(self, name: str, fn: Callable):
        self.name = name
        self.fn = fn

    def execute(self) -> None:
        self.fn()

class Scheduler:
    def __init__(self):
        self._queue: list[Task] = []

    def enqueue(self, task: Task) -> None:
        self._queue.append(task)

    def run_all(self) -> int:
        count = len(self._queue)
        for task in self._queue:
            task.execute()
        self._queue.clear()
        return count
""",
    ),
    (
        "serializers.py",
        """\
import json
from typing import Any

class Serializer:
    def serialize(self, obj: Any) -> str:
        raise NotImplementedError

    def deserialize(self, data: str) -> Any:
        raise NotImplementedError

class JsonSerializer(Serializer):
    def serialize(self, obj: Any) -> str:
        return json.dumps(obj)

    def deserialize(self, data: str) -> Any:
        return json.loads(data)

def round_trip(serializer: Serializer, obj: Any) -> Any:
    return serializer.deserialize(serializer.serialize(obj))
""",
    ),
]

_NUM_ITERATIONS = 20
_P95_INDEX = 18  # 0-indexed: 19th value out of 20 sorted = 95th percentile
_P95_THRESHOLD_SECONDS = 5.0


@pytest.mark.slow
@pytest.mark.performance
def test_performance_p95_under_5s(tmp_path: Path) -> None:
    """Run wiring analysis 20 times on a synthetic codebase, assert P95 < 5s."""
    # Build synthetic codebase
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    for filename, content in _SYNTHETIC_MODULES:
        (src_dir / filename).write_text(content, encoding="utf-8")

    config = WiringConfig(rollout_mode="soft")

    # Collect timings
    timings: list[float] = []
    for _ in range(_NUM_ITERATIONS):
        start = time.monotonic()
        run_wiring_analysis(config, src_dir)
        elapsed = time.monotonic() - start
        timings.append(elapsed)

    timings.sort()
    p95 = timings[_P95_INDEX]

    assert p95 < _P95_THRESHOLD_SECONDS, (
        f"P95 latency {p95:.3f}s exceeds {_P95_THRESHOLD_SECONDS}s threshold. "
        f"All timings (sorted): {[f'{t:.3f}' for t in timings]}"
    )
