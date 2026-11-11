"""Shared support for tests/observe: fake clock, fake runner and discovery, console factory.

Every test in this package runs with ``subprocess.Popen`` and ``subprocess.run`` replaced by a
function that raises, unless the test carries the marker ``observe_real_process`` (AD-16, T36).
"""

from __future__ import annotations

import io
import subprocess
from datetime import datetime, timedelta, timezone

import pytest

from superclaude.cli.observe.terminal import make_console, resolve_policy

BASE_TIME = datetime(2026, 11, 8, 12, 0, 0, tzinfo=timezone.utc)
WORKER_LIST_BASE = ["orchestration", "worker-list", "--json", "--limit", "100"]
DISCOVERY_TAIL = ["skills", "list", "--json"]


# -- subprocess guard -------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _subprocess_guard(request, monkeypatch):
    if request.node.get_closest_marker("observe_real_process"):
        return

    def refuse(*args, **kwargs):
        raise AssertionError(
            "subprocess is blocked in tests/observe; mark the test observe_real_process to lift the guard"
        )

    monkeypatch.setattr(subprocess, "Popen", refuse)
    monkeypatch.setattr(subprocess, "run", refuse)


# -- fake clock ---------------------------------------------------------------------------


class FakeClock:
    """Monotonic time, wall time and the local time zone, all under the test's control."""

    def __init__(
        self,
        monotonic: float = 1000.0,
        wall: float | None = None,
        tz: timezone = timezone.utc,
    ):
        self._mono = monotonic
        self._wall = BASE_TIME.timestamp() if wall is None else wall
        self.tz = tz

    def monotonic(self) -> float:
        return self._mono

    def wall(self) -> float:
        return self._wall

    def local_tz(self) -> timezone:
        return self.tz

    def advance(self, seconds: float) -> None:
        self._mono += seconds
        self._wall += seconds

    def jump_wall(self, seconds: float) -> None:
        """A wall-clock jump that leaves monotonic time alone."""
        self._wall += seconds


@pytest.fixture
def fake_clock() -> FakeClock:
    return FakeClock()


# -- fake runner and discovery (one shared argv log) ---------------------------------------


def argv_allowed(argv) -> bool:
    """The only argv the observer may ever run: worker-list (with optional pairs) or discovery."""
    argv = list(argv)
    if len(argv) < 2 or not all(isinstance(a, str) for a in argv):
        return False
    tail = argv[1:]
    if tail == DISCOVERY_TAIL:
        return True
    if tail[:5] != WORKER_LIST_BASE:
        return False
    rest = tail[5:]
    if rest[:1] == ["--run"] and len(rest) >= 2 and not rest[1].startswith("-"):
        rest = rest[2:]
    if rest[:1] == ["--cursor"] and len(rest) >= 2 and not rest[1].startswith("-"):
        rest = rest[2:]
    return rest == []


class FakeRunner:
    """``Runner`` stand-in: logs every argv, raises on one outside the allow-list.

    ``responses`` holds ``(returncode, stdout)`` pairs, exceptions, or callables
    ``f(argv, timeout) -> (returncode, stdout)``; the last one repeats when they run out.
    """

    def __init__(self, log: list, responses: list | None = None):
        self.log = log
        self.responses = responses if responses is not None else [(0, "{}")]
        self.timeouts: list[float] = []
        self.calls = 0

    def __call__(self, argv, timeout):
        self.log.append(list(argv))
        self.timeouts.append(timeout)
        if not argv_allowed(argv):
            raise AssertionError(f"argv outside the allow-list: {list(argv)!r}")
        response = self.responses[min(self.calls, len(self.responses) - 1)]
        self.calls += 1
        if isinstance(response, BaseException):
            raise response
        if callable(response):
            return response(argv, timeout)
        return response


class FakeDiscover:
    """``Discover`` stand-in: logs the discovery argv the real helper would run."""

    def __init__(self, log: list, path: str | None = "/opt/fake/orca"):
        self.log = log
        self.path = path
        self.calls = 0

    def __call__(self):
        self.calls += 1
        self.log.append([self.path or "orca", *DISCOVERY_TAIL])
        return self.path


@pytest.fixture
def argv_log() -> list:
    return []


@pytest.fixture
def fake_runner(argv_log) -> FakeRunner:
    return FakeRunner(argv_log)


@pytest.fixture
def fake_discover(argv_log) -> FakeDiscover:
    return FakeDiscover(argv_log)


# -- data and console helpers ----------------------------------------------------------------


def make_rows(n_rows: int, n_runs: int) -> list[dict]:
    """``n_rows`` valid worker rows spread over ``n_runs`` distinct runs (T16 matrix)."""
    rows = []
    for i in range(1, n_rows + 1):
        observed = (BASE_TIME - timedelta(seconds=3 * i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows.append(
            {
                "dispatchId": f"w-{i:03d}",
                "taskId": f"t-{i:03d}",
                "runId": f"run-{(i - 1) % n_runs}",
                "workerState": "running" if i % 2 else "idle",
                "dispatchStatus": "active",
                "terminalState": "active",
                "projection": {
                    "outcome": "none",
                    "nextAction": {"kind": "wait" if i % 3 else "none"},
                    "liveness": {
                        "verdict": "alive",
                        "source": "terminal",
                        "observedAt": observed,
                    },
                    "evidence": {"lastObservedAt": observed},
                },
            }
        )
    return rows


def make_envelope(
    rows: list[dict], total: int | None = None, has_more: bool = False
) -> dict:
    page = {"hasMore": has_more, "limit": 100}
    if total is not None:
        page["total"] = total
    return {"result": {"workers": rows, "page": page, "scope": {"source": "all"}}}


@pytest.fixture(name="make_rows")
def make_rows_fixture():
    return make_rows


@pytest.fixture
def console_factory():
    """``console_factory(width=160, height=40, ascii=False, no_color=False) -> (console, policy)``."""

    def factory(
        width: int = 160, height: int = 40, ascii: bool = False, no_color: bool = False
    ):
        env = {"NO_COLOR": "1"} if no_color else {}
        policy = resolve_policy(env, "utf-8", {"ascii": ascii}, width, height)
        return make_console(policy, file=io.StringIO(), record=True), policy

    return factory
