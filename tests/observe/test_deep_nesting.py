"""Deeply nested Orca replies fail safely (PR review findings on the adapter and the snapshot)."""

from __future__ import annotations

import json

from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector
from superclaude.cli.observe.export import snapshot_json
from superclaude.cli.observe.view import Session, build_view
from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows

DEPTH = 8  # parse keeps nested containers to depth 6 and maps deeper values to UNKNOWN


def _nested(depth):
    value = 1
    for _ in range(depth):
        value = {"a": value}
    return value


def test_a_reply_nested_beyond_the_recursion_limit_is_a_json_failure(fake_clock):
    runner = FakeRunner([], [(0, "[" * 100_000)])
    source = LiveSource(runner, FakeDiscover([], "/usr/bin/orca"))
    result = source.read_pages(fake_clock, fake_clock.monotonic() + 15.0, None)
    assert (result.state, result.code, result.pages) == ("FAILED", "json", ())


def test_the_snapshot_survives_a_deeply_nested_scope_and_counts(fake_clock):
    envelope = make_envelope(make_rows(2, 1), total=2)
    envelope["result"]["scope"] = _nested(DEPTH)
    envelope["result"]["counts"] = _nested(DEPTH)
    runner = FakeRunner([], [(0, json.dumps(envelope))])
    source = LiveSource(runner, FakeDiscover([], "/usr/bin/orca"))
    result = Collector(source, fake_clock).run_once()
    text = snapshot_json(build_view(result, Session(), fake_clock))
    assert json.loads(text)["schemaVersion"]
