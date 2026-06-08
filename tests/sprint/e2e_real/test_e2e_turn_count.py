"""Stage-0 acceptance — exact per-task turn count (real-subprocess e2e).

The Stage-0 criterion is a CORRECT turn count, not merely ``!= 0``. Only the
real-spawn path exercises the formerly-hard-coded ``turns_consumed = 0`` line in
``_run_task_subprocess``. This test makes the ``claude`` shim emit a transcript
whose terminal stream-json ``result`` event carries a KNOWN ``num_turns`` value
N (via ``FAKE_CLAUDE_NUM_TURNS``), runs the real per-task spawn, and asserts the
persisted ``TaskResult.turns_consumed == N`` EXACTLY. It would FAIL against the
pre-change hard-coded ``0`` (0 != N).
"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from superclaude.cli.sprint.executor import execute_sprint


@pytest.mark.integration
class TestE2ETurnCount:
    def test_turns_consumed_equals_reported_num_turns(
        self, claude_shim, real_release, monkeypatch
    ):
        config, _index = real_release
        claude_shim.set_failures()  # all tasks pass

        known_n = 7
        monkeypatch.setenv("FAKE_CLAUDE_NUM_TURNS", str(known_n))

        with patch("superclaude.cli.sprint.notify._notify"):
            try:
                execute_sprint(config)
            except SystemExit as exc:  # all-pass sprint may exit(0)
                assert exc.code in (0, None), f"unexpected non-zero exit: {exc.code}"

        result = json.loads(
            (config.results_dir / "phase-1-result.json").read_text(encoding="utf-8")
        )
        by_id = {
            tr.get("task", {}).get("task_id"): tr
            for tr in result.get("task_results", [])
        }
        assert by_id, "no task_results persisted — real per-task path did not run"

        for tid, tr in by_id.items():
            assert tr["turns_consumed"] == known_n, (
                f"{tid}: turns_consumed={tr['turns_consumed']!r} != {known_n} "
                "(the real stream-json num_turns was not parsed exactly)"
            )
