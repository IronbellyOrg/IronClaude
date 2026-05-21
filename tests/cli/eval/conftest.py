"""Shared fixtures for tests in :mod:`tests.cli.eval`.

PR #66 follow-up: the `allowlisted_output_dir` fixture lives here so every
end-to-end eval test that passes `--output-dir` to the CLI uses a path that
satisfies the AC12 / OPS-002 scratch-root allowlist.

Pytest's stock `tmp_path` fixture lands under `/tmp/pytest-of-<user>/...`,
which is NOT in the default allowlist `[/tmp/eval-runs, <repo>/.dev/eval-runs]`.
Before the Finding #2 fix on PR #66, `eval_run` self-extended its allowlist
with the operator-supplied `--output-dir`, so `tmp_path` slipped through (the
tautology bug). After the fix the policy is correctly strict and tests must
mint their own allowlisted subtree.
"""

from __future__ import annotations

import shutil
import uuid
from pathlib import Path

import pytest


@pytest.fixture
def allowlisted_output_dir() -> Path:
    """Yield a unique writable directory under the AC12 ``/tmp/eval-runs/`` root.

    The fixture creates ``/tmp/eval-runs/pytest-<12-hex>/`` before the test
    runs and removes the subtree after the test completes (best-effort —
    `ignore_errors=True` so a still-open file descriptor or read-only
    permission does not crash the suite).
    """

    root = Path("/tmp/eval-runs") / f"pytest-{uuid.uuid4().hex[:12]}"
    root.mkdir(parents=True, exist_ok=True)
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)
