"""Quitting never leaves an Orca call running (PR review finding on ``Collector.stop``)."""

from __future__ import annotations

import os
import sys
import threading
import time

import pytest

from superclaude.cli.observe import adapter
from superclaude.cli.observe.adapter import LiveSource, cancel_active, production_runner
from superclaude.cli.observe.collector import Collector


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


@pytest.mark.observe_real_process
def test_cancel_active_kills_and_reaps_a_hung_call():
    argv = [sys.executable, "-c", "import time; time.sleep(60)"]
    outcome: dict = {}

    def run():
        try:
            outcome["reply"] = production_runner(argv, 30.0)
        except Exception as exc:  # noqa: BLE001 - recorded for the assertion below
            outcome["error"] = exc

    worker = threading.Thread(target=run, daemon=True)
    worker.start()
    deadline = time.monotonic() + 5
    while not adapter._ACTIVE and time.monotonic() < deadline:
        time.sleep(0.01)
    (proc,) = list(adapter._ACTIVE)
    started = time.monotonic()
    cancel_active()
    worker.join(timeout=5)
    assert not worker.is_alive()
    assert time.monotonic() - started < 5  # not the 30 s call timeout
    assert not _alive(proc.pid)
    assert not adapter._ACTIVE  # unregistered once the call returned


class _CancelSource:
    mode = "live"
    variant = None
    available = False
    namespace = ""

    def __init__(self):
        self.cancelled = False

    def cancel(self):
        self.cancelled = True


def test_collector_stop_cancels_the_source(fake_clock):
    source = _CancelSource()
    Collector(source, fake_clock).stop()
    assert source.cancelled


def test_a_cancelled_live_source_starts_no_further_call(fake_clock):
    calls = []

    def runner(argv, timeout):
        calls.append(argv)
        return 0, "{}"

    source = LiveSource(runner, lambda: "/opt/fake/orca")
    source.cancel()
    result = source.read_pages(fake_clock, fake_clock.monotonic() + 15.0)
    assert calls == [] and result.state == "FAILED"
