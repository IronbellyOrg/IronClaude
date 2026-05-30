"""Regression tests for the auggie-flag-clear matcher gap fix.

PR #47 — widens the PostToolUse matcher to include ``mcp__auggie-mcp__*``.
Spec: .dev/releases/current/hook-sync-and-matcher-fix/release-spec.md §4
Existing coverage: ``test_auggie_first.py`` covers the ``mcp__auggie__*``
and ``mcp__airis-mcp-gateway__auggie_*`` prefixes. This file adds the
missing third prefix plus a cross-consistency assertion that the two
prefix-list surfaces (``hooks.json`` matcher and the script's ``case``
body) stay in lockstep.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / "src" / "superclaude" / "hooks" / "scripts" / "auggie-flag-clear.sh"
HOOKS_JSON = REPO_ROOT / "src" / "superclaude" / "hooks" / "hooks.json"


def _run_hook(payload: dict, fake_home: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["HOME"] = str(fake_home)
    (fake_home / ".claude" / "state" / "auggie-first-pending").mkdir(
        parents=True, exist_ok=True
    )
    (fake_home / ".claude" / "logs").mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        ["bash", str(HOOK)],
        input=json.dumps(payload).encode(),
        capture_output=True,
        env=env,
        timeout=5,
    )


def _sticky_path(home: Path, session_id: str) -> Path:
    return home / ".claude" / "state" / "auggie-first-pending" / f"{session_id}.txt"


# ---------------------------------------------------------------------------
# Behavioral regression tests — the bug PR #47 fixes
# ---------------------------------------------------------------------------


def test_auggie_mcp_dash_prefix_ask_question_clears_sticky(tmp_path: Path) -> None:
    """``mcp__auggie-mcp__ask_question`` is the standard auggie route in this repo.

    Before PR #47 this prefix was NOT in the matcher, so calls left the
    sticky in place and downstream gates false-positive-blocked legitimate
    actionable commands. This test pins the fix.
    """
    home = tmp_path / "home"
    sid = "test-auggie-mcp-ask"
    (home / ".claude" / "state" / "auggie-first-pending").mkdir(
        parents=True, exist_ok=True
    )
    _sticky_path(home, sid).write_text("pending\n")
    payload = {
        "session_id": sid,
        "tool_name": "mcp__auggie-mcp__ask_question",
    }
    result = _run_hook(payload, fake_home=home)
    assert result.returncode == 0, result.stderr.decode()
    assert not _sticky_path(home, sid).exists(), (
        "sticky must be cleared by mcp__auggie-mcp__ask_question"
    )
    telemetry = (home / ".claude" / "logs" / "auggie-first.jsonl").read_text()
    assert '"event":"sticky_cleared"' in telemetry
    assert '"tool":"mcp__auggie-mcp__ask_question"' in telemetry


def test_auggie_mcp_dash_prefix_implement_clears_sticky(tmp_path: Path) -> None:
    """Same prefix, different suffix — confirms the glob/regex isn't suffix-coupled."""
    home = tmp_path / "home"
    sid = "test-auggie-mcp-impl"
    (home / ".claude" / "state" / "auggie-first-pending").mkdir(
        parents=True, exist_ok=True
    )
    _sticky_path(home, sid).write_text("pending\n")
    payload = {
        "session_id": sid,
        "tool_name": "mcp__auggie-mcp__implement",
    }
    result = _run_hook(payload, fake_home=home)
    assert result.returncode == 0, result.stderr.decode()
    assert not _sticky_path(home, sid).exists()
    telemetry = (home / ".claude" / "logs" / "auggie-first.jsonl").read_text()
    assert '"event":"sticky_cleared"' in telemetry
    assert '"tool":"mcp__auggie-mcp__implement"' in telemetry


# ---------------------------------------------------------------------------
# Cross-consistency assertion — structural prevention against future drift
# ---------------------------------------------------------------------------

# The auggie-flag-clear hook has TWO surfaces that must reference the same
# auggie-prefix set:
#   1. hooks.json:60 "matcher" field (regex, used by Claude Code's matcher engine)
#   2. auggie-flag-clear.sh "case" body (glob, used by the script itself)
# If these drift, the matcher could fire the script for a tool name the
# script's case body then rejects (or vice versa). The fix in PR #47 lands
# the third prefix in BOTH files; this test pins that they keep agreeing.
# This is a mini Part 3 of .dev/releases/current/hook-sync-and-matcher-fix/release-spec.md
# (the full Part 3 lives in the bundled release as a Makefile assertion;
# this Python version covers the same invariant at pytest time).

_AUGGIE_PREFIX_RE = re.compile(
    r"mcp__[A-Za-z0-9_-]+(?:__|_)auggie[A-Za-z0-9_-]*|mcp__auggie[A-Za-z0-9_-]*"
)


def _normalize_prefixes(raw: list[str]) -> set[str]:
    """Strip trailing ``.*`` (regex) and ``*`` (glob) so both forms compare equal."""
    out: set[str] = set()
    for p in raw:
        p = p.rstrip("*").rstrip(".")
        out.add(p)
    return out


def _extract_matcher_prefixes() -> set[str]:
    """Pull auggie-related prefixes from hooks.json PostToolUse matcher."""
    data = json.loads(HOOKS_JSON.read_text())
    for entry in data["hooks"]["PostToolUse"]:
        matcher = entry.get("matcher", "")
        if "auggie" not in matcher:
            continue
        parts = matcher.split("|")
        return _normalize_prefixes([p for p in parts if "auggie" in p])
    return set()


def _extract_case_prefixes() -> set[str]:
    """Pull auggie-related prefixes from auggie-flag-clear.sh case body."""
    body = HOOK.read_text()
    # Find the case ... in line and capture its patterns
    match = re.search(r"case\s+\"\$TOOL_NAME\"\s+in\s*\n\s*([^\n)]+)\)", body)
    assert match, "could not locate case body in auggie-flag-clear.sh"
    parts = match.group(1).split("|")
    return _normalize_prefixes([p.strip() for p in parts if "auggie" in p])


def test_matcher_and_case_body_reference_same_auggie_prefixes() -> None:
    """hooks.json matcher and auggie-flag-clear.sh case body must agree.

    If a future change widens one but not the other (e.g. adds a new MCP
    deployment prefix to hooks.json but forgets the script body), the
    matcher would fire the hook for tool names the script then ignores
    — a silent no-op gap. This test catches that drift at PR time.
    """
    matcher_prefixes = _extract_matcher_prefixes()
    case_prefixes = _extract_case_prefixes()
    assert matcher_prefixes == case_prefixes, (
        f"prefix-set drift between hooks.json matcher and auggie-flag-clear.sh case body:\n"
        f"  matcher prefixes:    {sorted(matcher_prefixes)}\n"
        f"  case body prefixes:  {sorted(case_prefixes)}\n"
        f"  in matcher only:     {sorted(matcher_prefixes - case_prefixes)}\n"
        f"  in case body only:   {sorted(case_prefixes - matcher_prefixes)}"
    )


def test_pr47_widened_prefixes_present_in_both_surfaces() -> None:
    """PR #47 specifically lands ``mcp__auggie-mcp__`` in both files. Pin it."""
    matcher_prefixes = _extract_matcher_prefixes()
    case_prefixes = _extract_case_prefixes()
    assert "mcp__auggie-mcp__" in matcher_prefixes, (
        f"hooks.json matcher missing mcp__auggie-mcp__ prefix; got {sorted(matcher_prefixes)}"
    )
    assert "mcp__auggie-mcp__" in case_prefixes, (
        f"auggie-flag-clear.sh case body missing mcp__auggie-mcp__ prefix; "
        f"got {sorted(case_prefixes)}"
    )
