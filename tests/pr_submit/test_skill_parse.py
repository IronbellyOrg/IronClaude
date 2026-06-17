"""Skill flag/parse tests (spec FR-1.1/FR-1.2/FR-1.6/FR-1.7).

T-101 `--monitor` choices {0,1,2,3} (argparse); T-102 `--max-rounds` default=2,
hard cap=5, reject >5; T-103 no `--monitor` → armed at default L1; T-111 `--poll-interval 10`
→ reject "minimum is 30 seconds"; T-112 `--timeout 60` honored; T-113 `--resume`
captured (full JSONL state rebuild is exercised by test_crash_recovery).
"""

from __future__ import annotations

import pytest

from superclaude.pr_submit.fsm import (
    DEFAULT_MAX_ROUNDS,
    DEFAULT_MONITOR,
    DEFAULT_TIMEOUT,
    POLL_INTERVAL_ERROR,
    parse_args,
)


@pytest.mark.parametrize("ordinal", [0, 1, 2, 3])
def test_t101_monitor_choices_valid(ordinal):
    """T-101: `--monitor` accepts each of {0,1,2,3}."""
    args = parse_args(["--monitor", str(ordinal)])
    assert args.monitor == ordinal


def test_t101_monitor_choice_invalid_rejected():
    """T-101: `--monitor 4` is rejected by argparse (choices validation)."""
    with pytest.raises(SystemExit):
        parse_args(["--monitor", "4"])


def test_t102_max_rounds_default_and_cap():
    """T-102: `--max-rounds` default=2, cap=5 accepted, >5 rejected."""
    assert parse_args([]).max_rounds == DEFAULT_MAX_ROUNDS == 2
    assert parse_args(["--max-rounds", "5"]).max_rounds == 5
    with pytest.raises(ValueError):
        parse_args(["--max-rounds", "6"])


def test_t_max_rounds_zero_allowed():
    """EC-8: `--max-rounds 0` is a VALID 'monitor but never remediate' config via the CLI.

    The core (`run_skill` with `RunConfig(max_rounds=0)`) already honors EC-8 (gate
    `0 >= 0` True → HALT before any fix, zero rounds; see
    test_ec8_max_rounds_zero_never_remediates). This guards that the documented CLI
    surface ALSO accepts 0 — only NEGATIVE values are rejected.
    """
    assert parse_args(["--max-rounds", "0"]).max_rounds == 0
    # A negative value is still rejected.
    with pytest.raises(ValueError):
        parse_args(["--max-rounds", "-1"])


def test_t103_default_monitor_one_armed():
    """T-103: with no `--monitor`, the default is 1 and the monitor IS armed."""
    args = parse_args([])
    assert args.monitor == DEFAULT_MONITOR == 1
    assert args.armed is True


def test_explicit_monitor_zero_not_armed():
    """Explicit `--monitor 0` still preserves the open-only, not-armed path."""
    args = parse_args(["--monitor", "0"])
    assert args.monitor == 0
    assert args.armed is False


def test_t111_poll_interval_below_30_rejected():
    """T-111: `--poll-interval 10` is rejected with the exact 'minimum is 30 seconds' message."""
    with pytest.raises(ValueError) as exc:
        parse_args(["--poll-interval", "10"])
    assert POLL_INTERVAL_ERROR in str(exc.value)
    assert "minimum is 30 seconds" in str(exc.value)
    # The boundary value 30 is accepted.
    assert parse_args(["--poll-interval", "30"]).poll_interval == 30


def test_t112_timeout_honored():
    """T-112: `--timeout 60` is honored; the default is 600s."""
    assert parse_args(["--timeout", "60"]).timeout == 60
    assert parse_args([]).timeout == DEFAULT_TIMEOUT == 600


def test_t113_resume_path_captured():
    """T-113: `--resume <path>` is captured (state rebuild covered by test_crash_recovery)."""
    args = parse_args(["--resume", "/abs/monitor-run-42.jsonl"])
    assert args.resume == "/abs/monitor-run-42.jsonl"
    assert parse_args([]).resume is None
