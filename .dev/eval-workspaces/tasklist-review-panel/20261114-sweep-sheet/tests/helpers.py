"""Minimal helpers shared by the Task 1 tests: locate SW and run a snippet with bin/common.sh sourced."""

import os
import subprocess
from pathlib import Path

SW = Path(__file__).resolve().parents[1]
REPO = SW.parents[3]
REVIEWERS = ("muse-ember-1.0", "gpt-6-luna", "claude-haiku-5-5", "claude-sonnet-5-5")


def sh(cmd, env=None):
    """Run `source bin/common.sh; <cmd>` in bash; SW_* variables of the caller are dropped first."""
    e = {k: v for k, v in os.environ.items() if not k.startswith("SW_")}
    e.update(env or {})
    return subprocess.run(
        ["bash", "-c", f"source {SW}/bin/common.sh; {cmd}"],
        capture_output=True,
        text=True,
        env=e,
    )
