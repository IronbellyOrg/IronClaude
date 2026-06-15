"""Hook-update tests (spec FR-7.1).

T-701 a successful `gh pr create` → hook stdout contains BOTH `/sc:auggie-review`
AND `/sc:pr-submit --monitor`; T-702 a non-matching command → exit 0; T-703 a failed
`gh pr create` (tool_response.error non-empty) → exit 0. The hook is resolved under
the `src/` source-of-truth (NEVER `.claude/`).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / "src" / "superclaude" / "hooks" / "scripts" / "offer-pr-review.sh"


def _run_hook(payload: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(HOOK)],
        input=json.dumps(payload).encode(),
        capture_output=True,
        timeout=5,
    )


def test_hook_points_at_src_source():
    """The test resolves the hook at the src/ source of truth, not the .claude/ mirror."""
    assert HOOK.exists()
    assert ".claude" not in str(HOOK)


def test_t701_offer_mentions_both_commands():
    """T-701: a successful `gh pr create` → stdout mentions BOTH /sc:auggie-review and /sc:pr-submit --monitor.

    Uses an unrelated third-party repo (``acme/widgets``) to prove the hook is
    repo-agnostic: it fires on any ``gh pr create`` and extracts the PR URL generically,
    never keyed to one fork slug.
    """
    payload = {
        "tool_name": "Bash",
        "tool_input": {
            "command": "gh pr create --repo acme/widgets --base main --head feature/x --title t --body b"
        },
        "tool_response": {
            "stdout": "https://github.com/acme/widgets/pull/42",
            "error": "",
        },
    }
    result = _run_hook(payload)
    out = result.stdout.decode()
    assert result.returncode == 0
    assert "/sc:auggie-review" in out, f"missing auggie-review mention; stdout={out!r}"
    assert "/sc:pr-submit --monitor" in out, (
        f"missing pr-submit mention; stdout={out!r}"
    )


def test_t702_non_matching_command_exits_zero():
    """T-702: a non-matching command → exit 0 (fail-open, no offer)."""
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": "ls -la"},
        "tool_response": {"stdout": "", "error": ""},
    }
    result = _run_hook(payload)
    assert result.returncode == 0
    assert "/sc:pr-submit" not in result.stdout.decode()


def test_t703_failed_pr_create_exits_zero():
    """T-703: a failed `gh pr create` (error non-empty) → exit 0, no offer."""
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": "gh pr create --repo acme/widgets --head feature/x"},
        "tool_response": {
            "stdout": "",
            "error": "pull request create failed: a pull request already exists",
        },
    }
    result = _run_hook(payload)
    assert result.returncode == 0
    assert "/sc:pr-submit" not in result.stdout.decode()
