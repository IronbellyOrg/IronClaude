"""Registration of the launch-level guard in both hooks.json files (issue #394, Task 12).

The guard is registered once on UserPromptSubmit and once on PreToolUse, each with a
5 second timeout, and no onFailure key. The PreToolUse matcher is the string printed in
design section 13. The launch-job-identity.sh registration stays the last PreToolUse entry.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FILES = {
    "src": ROOT / "src/superclaude/hooks/hooks.json",
    "plugin": ROOT / "plugins/superclaude/hooks/hooks.json",
}
GUARD = "~/.claude/hooks/launch-level-guard.sh"
DESIGN = ROOT / "docs/designs/sc-issue-launch-level-hook.md"


def _hooks(name: str) -> dict:
    return json.loads(FILES[name].read_text(encoding="utf-8"))["hooks"]


def _guard_entries(hooks: dict, event: str) -> list[dict]:
    return [
        registration
        for registration in hooks[event]
        if any(h["command"] == GUARD for h in registration["hooks"])
    ]


def _design_matcher() -> str:
    section = DESIGN.read_text(encoding="utf-8").split(
        "## 13. Registration, install and claim-feature interface requests"
    )[1]
    return re.search(r'"matcher": "([^"]+)"', section).group(1)


@pytest.mark.parametrize("name", sorted(FILES))
def test_guard_registered_once_on_each_event_with_timeout_5(name):
    hooks = _hooks(name)
    for event in ("UserPromptSubmit", "PreToolUse"):
        entries = _guard_entries(hooks, event)
        assert len(entries) == 1, (name, event)
        assert [h["timeout"] for h in entries[0]["hooks"]] == [5]
    assert "matcher" not in _guard_entries(hooks, "UserPromptSubmit")[0]


@pytest.mark.parametrize("name", sorted(FILES))
def test_guard_is_not_registered_on_other_events(name):
    hooks = _hooks(name)
    for event, registrations in hooks.items():
        if event in ("UserPromptSubmit", "PreToolUse"):
            continue
        assert not _guard_entries(hooks, event), (name, event)


@pytest.mark.parametrize("name", sorted(FILES))
def test_no_on_failure_key_anywhere(name):
    assert "onFailure" not in FILES[name].read_text(encoding="utf-8")


def test_pretooluse_matcher_equals_the_design_string():
    expected = _design_matcher()
    for name in FILES:
        assert _guard_entries(_hooks(name), "PreToolUse")[0]["matcher"] == expected


@pytest.mark.parametrize("name", sorted(FILES))
def test_matcher_matches_the_guarded_tools_and_not_the_others(name):
    matcher = re.compile(_guard_entries(_hooks(name), "PreToolUse")[0]["matcher"])
    for tool in (
        "Bash",
        "Skill",
        "Agent",
        "Task",
        "Edit",
        "Write",
        "NotebookEdit",
        "Monitor",
        "Workflow",
        "RemoteTrigger",
        "SendMessage",
        "CronCreate",
        "ScheduleWakeup",
        "mcp__x__merge_pull_request",
    ):
        assert matcher.search(tool), tool
    for tool in ("Read", "Grep", "Glob", "TaskCreate"):
        assert not matcher.search(tool), tool


@pytest.mark.parametrize("name", sorted(FILES))
def test_existing_bash_registrations_stay_and_identity_hook_stays_last(name):
    pre_tool = _hooks(name)["PreToolUse"]
    commands = {
        hook["command"]
        for registration in pre_tool
        if registration.get("matcher") == "Bash"
        for hook in registration["hooks"]
    }
    assert commands == {
        "~/.claude/hooks/block-bare-python.sh",
        "~/.claude/hooks/launch-job-identity.sh",
    }
    assert (
        pre_tool[-1]["hooks"][0]["command"] == "~/.claude/hooks/launch-job-identity.sh"
    )
    assert (
        pre_tool.index(_guard_entries(_hooks(name), "PreToolUse")[0])
        == len(pre_tool) - 2
    )


def test_guard_registrations_are_the_same_in_both_trees():
    # The two files differ in other, older entries (the plugin copy is a subset);
    # only the guard entries must be identical.
    for event in ("UserPromptSubmit", "PreToolUse"):
        assert _guard_entries(_hooks("src"), event) == _guard_entries(
            _hooks("plugin"), event
        )
