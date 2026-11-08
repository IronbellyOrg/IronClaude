"""Behavioral tests for launch-level-guard.sh (issue #394, plan Tasks 3 to 11).

Each case runs the real script with a JSON payload on stdin, HOME inside
tmp_path, CLAUDE_CONFIG_DIR unset and a PATH holding only a temporary bin
directory, so the result does not depend on the developer's machine. Expected
message texts are read from section 9 of the design, not copied here.

Two test-only routes reach paths the Task 3 skeleton cannot reach through a
real payload; neither adds behaviour to the shipped script:
- the printer block (between the ">>> printer" and "<<< printer" comments) is
  run on its own in bash, to check all eighteen message texts; the normalise
  block (">>> normalise" to "<<< normalise") is run the same way, to check
  the T, G and W texts that the Task 7 to 9 classifiers read;
- a copy of the script with one known line changed to "exit 7" drives the
  real EXIT trap through a real payload.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "src" / "superclaude" / "hooks" / "scripts" / "launch-level-guard.sh"
DESIGN = ROOT / "docs" / "designs" / "sc-issue-launch-level-hook.md"
BASH = shutil.which("bash") or "/bin/bash"
SID = "sess-abc_123"
HEADER = "Launch-level guard: this session was started by /sc:issue --claim at level {level}."
LEVELS = {
    "W": "worktree",
    "WA": "worktree (approved)",
    "F": "full",
    "FS": "full --submit",
}
STATE_NOTE = (
    "Note: the launch record was invalid or unreadable, so the strictest level "
    "(worktree) applies."
)
IDS = [
    "LL-IMPL",
    "LL-COMMIT",
    "LL-PUSH",
    "LL-PUSH-FORM",
    "LL-PROTECTED",
    "LL-MERGE",
    "LL-GH-WRITE",
    "LL-SUBMIT",
    "LL-REPO",
    "LL-UNKNOWN",
    "LL-MCP",
    "LL-ESCAPE",
    "LL-TURN",
    "LL-TAMPER",
    "LL-SKILL",
    "LL-BIG",
    "LL-BROKEN",
    "LL-NOBIND",
]


def _design_section_9() -> str:
    text = DESIGN.read_text()
    return text.split("## 9. Block messages", 1)[1].split("## 10.", 1)[0]


def _design_table() -> dict[str, tuple[str, str, str]]:
    rows = {}
    for line in _design_section_9().splitlines():
        m = re.match(r"^\| (LL-[A-Z-]+) \| (.*) \| (.*) \| (.*) \|$", line)
        if m:
            # Amendment marks such as [B-7] are not printed (DD-3).
            cells = [re.sub(r" ?\[B-\d+\]", "", c) for c in m.groups()[1:]]
            rows[m.group(1)] = tuple(cells)
    return rows


def _design_note(name: str) -> str:
    m = re.search(rf"\*\*{name}\*\*[^`]*`(Note: [^`]*)`", _design_section_9())
    assert m, name
    return m.group(1)


def _store(home: Path) -> Path:
    return home / ".claude" / "state" / "launch-level"


def _bin(tmp_path: Path, with_jq: bool = True) -> Path:
    bindir = tmp_path / "bin"
    bindir.mkdir(exist_ok=True)
    tools = ["cat", "sed", "tr", "mkdir", "mv", "ln", "rm"] + (
        ["jq"] if with_jq else []
    )
    for tool in tools:
        found = shutil.which(tool)
        assert found, tool
        (bindir / tool).symlink_to(found)
    return bindir


def _env(home: Path, bindir: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"}
    env["HOME"] = str(home)
    env["PATH"] = str(bindir)
    return env


def _run(payload, tmp_path: Path, script: Path = HOOK, with_jq: bool = True):
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    stdin = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
    bindir = tmp_path / "bin"
    if not bindir.exists():
        _bin(tmp_path, with_jq)
    return subprocess.run(
        [BASH, str(script)],
        input=stdin,
        capture_output=True,
        env=_env(home, bindir),
        timeout=10,
    )


def _bind(tmp_path: Path, word: str = "full", ok: bool = False) -> Path:
    sessions = _store(tmp_path / "home") / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    (sessions / SID).write_text(word)
    if ok:
        (sessions / f"{SID}.ok").write_text("")
    return sessions


NONCE = "0123456789abcdef0123456789abcdef"
NONCE2 = "fedcba9876543210fedcba9876543210"


def _marker(nonce: str = NONCE) -> str:
    return f"[sc-launch:v1:{nonce}]"


def _pending(tmp_path: Path, word: str = "full", nonce: str = NONCE) -> Path:
    """Write a launch record the way publish_pending does (one word, no newline)."""
    pending = _store(tmp_path / "home") / "pending"
    pending.mkdir(parents=True, exist_ok=True, mode=0o700)
    (pending / nonce).write_text(word)
    return pending / nonce


def _prompt(text: str, sid=SID, **extra) -> dict:
    payload = {"hook_event_name": "UserPromptSubmit", "prompt": text, **extra}
    if sid is not None:
        payload["session_id"] = sid
    return payload


def _assert_bound(tmp_path: Path, sid: str, word: str) -> None:
    """sessions/<sid> holds exactly the word, and no temporary file is left."""
    sessions = _store(tmp_path / "home") / "sessions"
    path = sessions / sid
    assert path.is_file() and not path.is_symlink()
    assert path.read_text() == word
    assert [p.name for p in sessions.iterdir() if p.name.startswith(".")] == []


def _session_files(tmp_path: Path) -> list[str]:
    sessions = _store(tmp_path / "home") / "sessions"
    return sorted(p.name for p in sessions.iterdir()) if sessions.exists() else []


def _governed_level(tmp_path: Path, sid: str = SID, **extra):
    """A PostToolUse call on sid: the skeleton answers a bound id with LL-BROKEN
    and the level header, so the result shows the level the guard reads."""
    payload = {"hook_event_name": "PostToolUse", "session_id": sid, **extra}
    return _run(payload, tmp_path)


def _expected_level(tmp_path: Path, word: str, sid: str = SID) -> str:
    store = str(_store(tmp_path / "home"))
    level = {"worktree": "worktree", "full": "full", "full-submit": "full --submit"}
    if word in level:
        return _expected("LL-BROKEN", level[word], sid, store)
    return _expected("LL-BROKEN", "worktree", sid, store) + STATE_NOTE + "\n"


def _expected(msg_id: str, level: str | None, sid: str, store: str) -> str:
    blocked, why, you_can = _design_table()[msg_id]
    subst = {"{store}": store, "{sid}": sid}
    lines = []
    for text in (blocked, why, you_can):
        for key, value in subst.items():
            text = text.replace(key, value)
        lines.append(text)
    first = HEADER.format(level=level) if level else "Launch-level guard:"
    return f"{first}\nBlocked: {lines[0]}\nWhy: {lines[1]}\nYou can: {lines[2]}\n"


def _printer(
    tmp_path: Path, msg_id: str, level: str, sid: str = SID, notes: str = "00"
):
    """Run only the printer block of the script (test-only route)."""
    driver = (
        'eval "$(sed -n \'/^# >>> printer/,/^# <<< printer/p\' "$1")"\n'
        "LL_LEVEL=$2 LL_SID=$3 LL_NOTE_STATE=${5:0:1} LL_NOTE_TEXT=${5:1:1}\n"
        'll_say "$4"\n'
    )
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    return subprocess.run(
        [BASH, "-c", driver, "_", str(HOOK), level, sid, msg_id, notes],
        capture_output=True,
        env=_env(home, _bin(tmp_path)),
        timeout=10,
    )


FAULT_LINES = {
    # First line of each branch; "marker" is the first write after a marker.
    "tool": '[ "$LL_GOVERNED" = 1 ] || exit 0 # unbound or identity loss',
    "prompt": '[ "$LL_AGENT" = 1 ] && exit 0 # B5: a subagent prompt never binds or approves',
    "marker": 'mkdir -p -- "$LL_SESS" 2>/dev/null',
}


def _faulty_copy(tmp_path: Path, stub: str) -> Path:
    """Copy of the script with one line made "exit 7", to drive the EXIT trap."""
    text = HOOK.read_text()
    marker = FAULT_LINES[stub]
    assert text.count(marker) == 1
    copy = tmp_path / "guard-fault.sh"
    copy.write_text(text.replace(marker, "exit 7"))
    return copy


# --- script text -----------------------------------------------------------


def test_script_is_executable_with_version_line():
    assert os.access(HOOK, os.X_OK)
    lines = HOOK.read_text().splitlines()
    assert lines[0] == "#!/bin/bash"
    assert "# launch-level-guard-version: 1" in lines[:10]


def test_script_text_never_names_the_joined_store_path():
    assert ".claude/state" not in HOOK.read_text()


def test_script_passes_bash_syntax_check():
    assert subprocess.run([BASH, "-n", str(HOOK)]).returncode == 0


def test_script_prints_no_amendment_marks():
    assert not re.search(r"\[B-\d+\]", HOOK.read_text())


# --- ordinary sessions -----------------------------------------------------

VALID_PAYLOADS = {
    "pretooluse-bash": {
        "hook_event_name": "PreToolUse",
        "session_id": SID,
        "tool_name": "Bash",
        "tool_input": {"command": "git push origin main"},
    },
    "pretooluse-skill": {
        "hook_event_name": "PreToolUse",
        "session_id": SID,
        "tool_name": "Skill",
        "tool_input": {"skill": "sc:implement"},
    },
    "prompt": {
        "hook_event_name": "UserPromptSubmit",
        "session_id": SID,
        "prompt": "hello",
    },
    "marker-prompt": {
        "hook_event_name": "UserPromptSubmit",
        "session_id": SID,
        "prompt": "[sc-launch:v1:" + "a" * 32 + "] plan issue 1",
    },
    "other-event": {"hook_event_name": "PostToolUse", "session_id": SID},
}


@pytest.mark.parametrize("name", sorted(VALID_PAYLOADS))
def test_empty_home_allows_silently(tmp_path, name):
    result = _run(VALID_PAYLOADS[name], tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    if name == "marker-prompt":
        # A launch marker with no record binds degraded (FR-L-09 B12).
        _assert_bound(tmp_path, SID, "degraded")
    else:
        assert not (tmp_path / "home" / ".claude").exists()


def test_empty_home_without_jq_allows_silently(tmp_path):
    _bin(tmp_path, with_jq=False)
    result = _run(VALID_PAYLOADS["pretooluse-bash"], tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


@pytest.mark.parametrize("name", sorted(VALID_PAYLOADS))
def test_unbound_session_with_nonempty_store_allows_silently(tmp_path, name):
    sessions = _store(tmp_path / "home") / "sessions"
    sessions.mkdir(parents=True)
    (sessions / "someone-else").write_text("worktree")
    result = _run(VALID_PAYLOADS[name], tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


# --- event dispatch and the identity-loss rule -----------------------------

OTHER_EVENTS = {
    "post-tool-use": {"hook_event_name": "PostToolUse", "session_id": SID},
    "missing-event": {"session_id": SID, "tool_name": "Bash"},
    "numeric-event": {"hook_event_name": 7, "session_id": SID},
    "nested-forged-event": {
        "hook_event_name": "Stop",
        "session_id": SID,
        "tool_input": {"hook_event_name": "PreToolUse"},
    },
}


@pytest.mark.parametrize("name", sorted(OTHER_EVENTS))
def test_other_event_unbound_allows_silently(tmp_path, name):
    # Identity loss (design section 3): a nonempty store alone never proves
    # this caller is governed; allow without claiming enforcement.
    sessions = _store(tmp_path / "home") / "sessions"
    sessions.mkdir(parents=True)
    (sessions / "someone-else").write_text("full")
    result = _run(OTHER_EVENTS[name], tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_unparseable_envelope_allows_silently(tmp_path):
    _bind(tmp_path)
    result = _run(b'{"hook_event_name": "PreToolUse", "session_id": ', tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


@pytest.mark.parametrize(
    "word, ok, level, note",
    [
        ("full", False, "full", False),
        ("full-submit\n", False, "full --submit", False),
        ("worktree", True, "worktree (approved)", False),
        ("garbage", False, "worktree", True),
    ],
)
def test_other_event_bound_session_blocks_broken(tmp_path, word, ok, level, note):
    _bind(tmp_path, word, ok)
    result = _run(OTHER_EVENTS["post-tool-use"], tmp_path)
    store = str(_store(tmp_path / "home"))
    expected = _expected("LL-BROKEN", level, SID, store)
    if note:
        expected += STATE_NOTE + "\n"
    assert result.returncode == 2
    assert result.stdout == b""
    assert result.stderr.decode() == expected


# --- EXIT trap through a real payload (fault-injected copy) ----------------


def test_trap_in_tool_branch_gives_broken(tmp_path):
    _bind(tmp_path, "full")
    result = _run(
        VALID_PAYLOADS["pretooluse-bash"], tmp_path, _faulty_copy(tmp_path, "tool")
    )
    store = str(_store(tmp_path / "home"))
    assert result.returncode == 2
    assert result.stderr.decode() == _expected("LL-BROKEN", "full", SID, store)


def test_trap_in_prompt_branch_gives_nobind(tmp_path):
    _bind(tmp_path, "worktree")
    result = _run(VALID_PAYLOADS["prompt"], tmp_path, _faulty_copy(tmp_path, "prompt"))
    store = str(_store(tmp_path / "home"))
    assert result.returncode == 2
    assert result.stderr.decode() == _expected("LL-NOBIND", "worktree", SID, store)


@pytest.mark.parametrize(
    "stub, payload", [("tool", "pretooluse-bash"), ("prompt", "prompt")]
)
def test_trap_never_blocks_an_ordinary_session(tmp_path, stub, payload):
    # FR-L-53: an internal failure in an unbound session allows silently.
    sessions = _store(tmp_path / "home") / "sessions"
    sessions.mkdir(parents=True)
    result = _run(VALID_PAYLOADS[payload], tmp_path, _faulty_copy(tmp_path, stub))
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_trap_after_marker_gives_nobind_bare_header(tmp_path):
    # FR-L-09 B6: once a marker is seen, any internal failure blocks the prompt.
    _pending(tmp_path)
    result = _run(
        _prompt(_marker() + " plan"), tmp_path, _faulty_copy(tmp_path, "marker")
    )
    store = str(_store(tmp_path / "home"))
    assert result.returncode == 2
    assert result.stderr.decode() == _expected("LL-NOBIND", None, SID, store)


# --- binding on UserPromptSubmit (FR-L-09, T-BIND-*) -----------------------

WORDS = ["worktree", "full", "full-submit"]


def _nobind(tmp_path: Path) -> str:
    return _expected("LL-NOBIND", None, SID, str(_store(tmp_path / "home")))


@pytest.mark.parametrize("word", WORDS)
def test_bind_marker_with_record_binds_level(tmp_path, word):
    # T-BIND-1
    record = _pending(tmp_path, word)
    result = _run(_prompt(_marker() + " plan issue 7"), tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    _assert_bound(tmp_path, SID, word)
    assert not record.exists()
    assert _governed_level(tmp_path).stderr.decode() == _expected_level(tmp_path, word)


def test_bind_marker_at_start_without_record_binds_degraded(tmp_path):
    # T-BIND-2
    result = _run(_prompt(_marker() + " plan"), tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    _assert_bound(tmp_path, SID, "degraded")
    later = _governed_level(tmp_path)
    assert later.returncode == 2
    assert later.stderr.decode() == _expected_level(tmp_path, "degraded")


@pytest.mark.parametrize(
    "marker",
    [
        "[sc-launch:v1:" + "ABCDEF0123456789" * 2 + "]",
        "[sc-launch:v1:01234567-89ab-cdef-0123-456789abcdef]",
        "[sc-launch:v1:" + "a" * 33 + "]",
        "[sc-launch:v2:" + NONCE + "]",
        "[sc-launch:v1:<nonce>]",
    ],
)
def test_bind_malformed_marker_at_start_binds_degraded(tmp_path, marker):
    # T-BIND-3: a record exists, but a malformed marker never names it.
    record = _pending(tmp_path, "full-submit")
    result = _run(_prompt(marker + " plan"), tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    _assert_bound(tmp_path, SID, "degraded")
    assert record.read_text() == "full-submit"


LEADS = ["   ", "\n\n", "\t\r\n ", "﻿", " ﻿\n﻿\t"]


@pytest.mark.parametrize("lead", LEADS)
def test_bind_marker_after_whitespace_or_bom_binds(tmp_path, lead):
    # T-BIND-4: with a record the strict marker binds its level ...
    _pending(tmp_path, "full")
    result = _run(_prompt(lead + _marker() + " plan"), tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    _assert_bound(tmp_path, SID, "full")


@pytest.mark.parametrize("lead", LEADS)
def test_bind_loose_marker_after_whitespace_or_bom_binds_degraded(tmp_path, lead):
    # ... and a loose marker after the same lead binds degraded.
    result = _run(_prompt(lead + "[sc-launch:v1:<nonce>] plan"), tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    _assert_bound(tmp_path, SID, "degraded")


def test_bind_strict_marker_mid_prompt_with_record_binds(tmp_path):
    # T-BIND-5
    record = _pending(tmp_path, "full-submit")
    result = _run(_prompt("Please start. " + _marker() + " plan"), tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    _assert_bound(tmp_path, SID, "full-submit")
    assert not record.exists()


def test_bind_strict_marker_mid_prompt_without_record_blocks_prompt(tmp_path):
    # T-BIND-6 (owner decision O-20)
    result = _run(_prompt("Example: " + _marker() + " plan"), tmp_path)
    assert result.returncode == 2
    assert result.stdout == b""
    assert result.stderr.decode() == _nobind(tmp_path)
    assert _session_files(tmp_path) == []


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory modes")
def test_bind_failure_blocks_prompt(tmp_path):
    # T-BIND-7: read-only sessions/; the record is left for a retry.
    record = _pending(tmp_path, "full")
    sessions = _store(tmp_path / "home") / "sessions"
    sessions.mkdir(mode=0o700)
    sessions.chmod(0o500)
    try:
        result = _run(_prompt(_marker() + " plan"), tmp_path)
    finally:
        sessions.chmod(0o700)
    assert result.returncode == 2
    assert result.stderr.decode() == _nobind(tmp_path)
    assert _session_files(tmp_path) == []
    assert record.read_text() == "full"


def test_bind_sessions_dir_created(tmp_path):
    # T-BIND-8
    _pending(tmp_path, "worktree")
    sessions = _store(tmp_path / "home") / "sessions"
    assert not sessions.exists()
    result = _run(_prompt(_marker() + " plan"), tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    _assert_bound(tmp_path, SID, "worktree")
    assert sessions.stat().st_mode & 0o777 == 0o700


def test_bind_nonce_single_use(tmp_path):
    # T-BIND-9
    _pending(tmp_path, "full-submit")
    assert _run(_prompt(_marker() + " plan"), tmp_path).returncode == 0
    result = _run(_prompt(_marker() + " plan", sid="second-session"), tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    _assert_bound(tmp_path, SID, "full-submit")
    _assert_bound(tmp_path, "second-session", "degraded")


@pytest.mark.parametrize("old", ["worktree", "garbage", ""])
def test_bind_later_marker_consumes_record_keeps_level(tmp_path, old):
    # T-BIND-10, and a pre-created file with another word stays unchanged.
    sessions = _bind(tmp_path, old)
    record = _pending(tmp_path, "full-submit")
    result = _run(_prompt(_marker() + " plan"), tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    assert (sessions / SID).read_text() == old
    assert not record.exists()
    assert _session_files(tmp_path) == [SID]


def test_bind_resume_same_id_governed(tmp_path):
    # T-BIND-11: a later ordinary prompt keeps the binding; a later call reads it.
    _pending(tmp_path, "full")
    _run(_prompt(_marker() + " plan"), tmp_path)
    result = _run(_prompt("continue"), tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    _assert_bound(tmp_path, SID, "full")
    assert _governed_level(tmp_path).stderr.decode() == _expected_level(
        tmp_path, "full"
    )


def test_bind_rename_still_governed(tmp_path):
    # T-BIND-12: identity is the session id, never the cwd.
    _pending(tmp_path, "worktree")
    _run(_prompt(_marker() + " plan", cwd="/work/a"), tmp_path)
    later = _governed_level(tmp_path, cwd="/work/renamed")
    assert later.stderr.decode() == _expected_level(tmp_path, "worktree")


def test_bind_reclaim_new_session_new_level(tmp_path):
    # T-BIND-13
    _pending(tmp_path, "worktree")
    _run(_prompt(_marker() + " plan", sid="old-session"), tmp_path)
    _pending(tmp_path, "full", NONCE2)
    result = _run(_prompt(_marker(NONCE2) + " plan", sid="new-session"), tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    _assert_bound(tmp_path, "old-session", "worktree")
    _assert_bound(tmp_path, "new-session", "full")


@pytest.mark.parametrize(
    "sid", [".", "..", "x.ok", "a/b", "", "a" * 129, 7, {"id": SID}, None]
)
def test_bind_invalid_session_ids(tmp_path, sid):
    # T-BIND-14 (prompt half; the PreToolUse half is Task 5).
    record = _pending(tmp_path, "full")
    result = _run(_prompt(_marker() + " plan", sid=sid), tmp_path)
    assert result.returncode == 2
    assert result.stderr.decode() == _nobind(tmp_path)
    assert _session_files(tmp_path) == []
    assert record.read_text() == "full"


@pytest.mark.parametrize("agent_id", ["agent-1", "x"])
def test_bind_marker_prompt_with_agent_id_ignored(tmp_path, agent_id):
    # T-BIND-15
    record = _pending(tmp_path, "full")
    result = _run(_prompt(_marker() + " plan", agent_id=agent_id), tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert _session_files(tmp_path) == []
    assert record.read_text() == "full"


def test_bind_jq_missing_marker_prompt_blocked(tmp_path):
    # T-BIND-16
    _bin(tmp_path, with_jq=False)
    record = _pending(tmp_path, "full")
    result = _run(_prompt(_marker() + " plan"), tmp_path)
    assert result.returncode == 2
    assert result.stderr.decode() == _nobind(tmp_path)
    assert _session_files(tmp_path) == []
    assert record.read_text() == "full"


def test_bind_unparseable_marker_prompt_blocked(tmp_path):
    # FR-L-09 B4: a jq failure on a marker prompt acts as B3.
    raw = b'{"hook_event_name": "UserPromptSubmit", "prompt": "[sc-launch:v1:'
    result = _run(raw, tmp_path)
    assert result.returncode == 2
    assert result.stderr.decode() == _nobind(tmp_path)


@pytest.mark.parametrize("store", [False, True])
def test_bind_loose_marker_mid_prompt_ignored(tmp_path, store):
    # T-BIND-17
    if store:
        sessions = _store(tmp_path / "home") / "sessions"
        sessions.mkdir(parents=True)
        (sessions / "someone-else").write_text("full")
    result = _run(_prompt("see [sc-launch:v2:x] in the docs"), tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert SID not in _session_files(tmp_path)


# --- isolation and fail-closed cases that concern binding ------------------


def test_bind_two_sessions_isolated(tmp_path):
    # T-ISO-2
    _pending(tmp_path, "worktree")
    _pending(tmp_path, "full-submit", NONCE2)
    _run(_prompt(_marker() + " a", sid="session-a"), tmp_path)
    _run(_prompt(_marker(NONCE2) + " b", sid="session-b"), tmp_path)
    for sid, word in [("session-a", "worktree"), ("session-b", "full-submit")]:
        got = _governed_level(tmp_path, sid).stderr.decode()
        assert got == _expected_level(tmp_path, word, sid)


def test_bind_same_worktree_other_session_ordinary(tmp_path):
    # T-ISO-3
    _pending(tmp_path, "worktree")
    _run(_prompt(_marker() + " plan", cwd="/work/wt"), tmp_path)
    result = _run(_prompt("hello", sid="other-session", cwd="/work/wt"), tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert _session_files(tmp_path) == [SID]


def test_bind_person_subagent_not_governed(tmp_path):
    # T-ISO-4 (X-004): unbound id, agent_id, the bound worktree's cwd.
    _bind(tmp_path, "worktree")
    _pending(tmp_path, "full")
    payload = _prompt(
        _marker() + " plan", sid="person-session", agent_id="a1", cwd="/work/wt"
    )
    result = _run(payload, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert _session_files(tmp_path) == [SID]


def test_bind_forged_nested_session_id(tmp_path):
    # T-ISO-6: only the top-level session_id counts.
    _bind(tmp_path, "worktree")
    ordinary = _prompt(_marker() + " plan", sid="unbound-one", meta={"session_id": SID})
    record = _pending(tmp_path, "full")
    result = _run(ordinary, tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    _assert_bound(tmp_path, "unbound-one", "full")
    governed = _prompt(_marker(NONCE2) + " plan", meta={"session_id": "unbound-two"})
    record = _pending(tmp_path, "full-submit", NONCE2)
    result = _run(governed, tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    assert not record.exists()
    _assert_bound(tmp_path, SID, "worktree")
    assert "unbound-two" not in _session_files(tmp_path)


def test_bind_jq_missing_ordinary_prompt_allows(tmp_path):
    # T-FC-1 (prompt half): no jq and no marker never blocks a prompt.
    _bin(tmp_path, with_jq=False)
    _bind(tmp_path, "full")
    result = _run(_prompt("continue"), tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


# --- concurrency (FR-L-09 B11: one nonce binds at most one session) --------


def _race(tmp_path: Path, sids: list[str]) -> list[subprocess.CompletedProcess]:
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    env = _env(home, _bin(tmp_path))
    procs = [
        subprocess.Popen(
            [BASH, str(HOOK)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )
        for _ in sids
    ]
    # Every guard is started and blocked on stdin; release them together.
    payloads = [json.dumps(_prompt(_marker() + " plan", sid=s)).encode() for s in sids]
    for proc, data in zip(procs, payloads):
        proc.stdin.write(data)
    for proc in procs:
        proc.stdin.close()
    results = []
    for proc in procs:
        out, err = proc.stdout.read(), proc.stderr.read()
        rc = proc.wait(timeout=20)
        results.append(subprocess.CompletedProcess(proc.args, rc, out, err))
    return results


def test_bind_concurrent_same_session_same_nonce(tmp_path):
    record = _pending(tmp_path, "full-submit")
    results = _race(tmp_path, [SID] * 12)
    assert [(r.returncode, r.stderr) for r in results] == [(0, b"")] * 12
    _assert_bound(tmp_path, SID, "full-submit")
    assert _session_files(tmp_path) == [SID]
    assert not record.exists()


def test_bind_concurrent_other_sessions_same_nonce(tmp_path):
    record = _pending(tmp_path, "full")
    sids = [f"racer-{i}" for i in range(12)]
    results = _race(tmp_path, sids)
    assert [(r.returncode, r.stderr) for r in results] == [(0, b"")] * 12
    words = sorted(
        (_store(tmp_path / "home") / "sessions" / s).read_text() for s in sids
    )
    assert words == ["degraded"] * 11 + ["full"]
    assert _session_files(tmp_path) == sorted(sids)
    assert not record.exists()


def test_bind_race_winner_level_governs_tool_calls(tmp_path):
    # After the race, a PreToolUse call for the same id resolves the winner's level.
    _pending(tmp_path, "worktree")
    results = _race(tmp_path, [SID] * 8)
    assert [r.returncode for r in results] == [0] * 8
    result = _run(_skill("sc:implement"), tmp_path)
    store = str(_store(tmp_path / "home"))
    assert result.returncode == 2
    assert result.stderr.decode() == _expected("LL-IMPL", "worktree", SID, store)


# --- PreToolUse: Skill classifier and the policy grid (Task 5) -------------

# Launch level -> (record word, .ok present).
LEVEL_FILES = {
    "W": ("worktree", False),
    "WA": ("worktree", True),
    "F": ("full", False),
    "FS": ("full-submit", False),
}

# Hand-written oracle of the policy grid (design section 4), one row per class,
# typed from the design table and never derived from the script: None allows,
# otherwise the message id a call of that class alone is blocked with.
GRID_CLASSES = (
    "IMPL",
    "TURN",
    "SUBMIT",
    "COMMIT",
    "PUSH",
    "PUSHFORM",
    "PROTECTED",
    "MERGE",
    "GHWRITE",
    "UNKNOWN",
    "MCP",
    "ESCAPE",
    "TAMPER",
    "SKILL",
    "BIG",
    "REPO",
)
EXPECTED = {
    "NONE": {"W": None, "WA": None, "F": None, "FS": None},
    "IMPL": {"W": "LL-IMPL", "WA": None, "F": None, "FS": None},
    "TURN": {"W": "LL-TURN", "WA": None, "F": None, "FS": None},
    "SUBMIT": {"W": "LL-SUBMIT", "WA": "LL-SUBMIT", "F": "LL-SUBMIT", "FS": None},
    "COMMIT": {"W": "LL-COMMIT", "WA": "LL-COMMIT", "F": "LL-COMMIT", "FS": None},
    "PUSH": {"W": "LL-PUSH", "WA": "LL-PUSH", "F": "LL-PUSH", "FS": None},
    "SKILL": {"W": "LL-SKILL", "WA": "LL-SKILL", "F": "LL-SKILL", "FS": None},
    "REPO": {"W": "LL-REPO", "WA": "LL-REPO", "F": "LL-REPO", "FS": "LL-REPO"},
    "PUSHFORM": {
        "W": "LL-PUSH-FORM",
        "WA": "LL-PUSH-FORM",
        "F": "LL-PUSH-FORM",
        "FS": "LL-PUSH-FORM",
    },
    "PROTECTED": {
        "W": "LL-PROTECTED",
        "WA": "LL-PROTECTED",
        "F": "LL-PROTECTED",
        "FS": "LL-PROTECTED",
    },
    "MERGE": {"W": "LL-MERGE", "WA": "LL-MERGE", "F": "LL-MERGE", "FS": "LL-MERGE"},
    "GHWRITE": {
        "W": "LL-GH-WRITE",
        "WA": "LL-GH-WRITE",
        "F": "LL-GH-WRITE",
        "FS": "LL-GH-WRITE",
    },
    "UNKNOWN": {
        "W": "LL-UNKNOWN",
        "WA": "LL-UNKNOWN",
        "F": "LL-UNKNOWN",
        "FS": "LL-UNKNOWN",
    },
    "MCP": {"W": "LL-MCP", "WA": "LL-MCP", "F": "LL-MCP", "FS": "LL-MCP"},
    "ESCAPE": {
        "W": "LL-ESCAPE",
        "WA": "LL-ESCAPE",
        "F": "LL-ESCAPE",
        "FS": "LL-ESCAPE",
    },
    "TAMPER": {
        "W": "LL-TAMPER",
        "WA": "LL-TAMPER",
        "F": "LL-TAMPER",
        "FS": "LL-TAMPER",
    },
    "BIG": {"W": "LL-BIG", "WA": "LL-BIG", "F": "LL-BIG", "FS": "LL-BIG"},
}
# T-GRID-2 at import time too: a class without an oracle row fails the module.
assert set(GRID_CLASSES) | {"NONE"} == set(EXPECTED), "grid class without oracle row"

# Hand-written oracle for the Skill rows of the grid (design section 8):
# None allows, otherwise the message id the call is blocked with.
SKILL_EXPECTED = {
    "sc:implement": {"W": "LL-IMPL", "WA": None, "F": None, "FS": None},
    "sc:pr-submit": {"W": "LL-SUBMIT", "WA": "LL-SUBMIT", "F": "LL-SUBMIT", "FS": None},
    "sc:issue": {
        "W": "LL-ESCAPE",
        "WA": "LL-ESCAPE",
        "F": "LL-ESCAPE",
        "FS": "LL-ESCAPE",
    },
    "": {"W": "LL-SKILL", "WA": "LL-SKILL", "F": "LL-SKILL", "FS": None},
    "sc:workflow": {"W": None, "WA": None, "F": None, "FS": None},
}

_ABSENT = object()


def _skill(name=_ABSENT, sid=SID, tool_input=None, **extra) -> dict:
    """A Skill PreToolUse payload; name goes under tool_input.skill."""
    tool_input = dict(tool_input or {})
    if name is not _ABSENT:
        tool_input["skill"] = name
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Skill", **extra}
    payload["tool_input"] = tool_input
    if sid is not None:
        payload["session_id"] = sid
    return payload


def _assert_decision(result, tmp_path, msg_id, level, note=False, text=False):
    if msg_id is None:
        assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
        return
    store = str(_store(tmp_path / "home"))
    expected = _expected(msg_id, LEVELS[level], SID, store)
    if note:
        expected += STATE_NOTE + "\n"
    if text:
        expected += _design_note("LL-TEXT") + "\n"
    assert result.returncode == 2
    assert result.stdout == b""
    assert result.stderr.decode() == expected


@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
@pytest.mark.parametrize("name", sorted(SKILL_EXPECTED))
def test_skill_grid_matches_oracle(tmp_path, name, level):
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(_skill(name), tmp_path)
    _assert_decision(result, tmp_path, SKILL_EXPECTED[name][level], level)


IMPL_SPELLINGS = [
    "sc:implement",
    "sc:implement-protocol",
    "sc-implement-protocol",
    "task",
    "sc:task",
    "sc:task-protocol",
    "sc:improve",
    "sc:cleanup",
    "sc:spawn",
    "sc:build",
    "SC:IMPLEMENT",
    "/sc:implement args",
    "superclaude:sc-implement-protocol",
    " \t\nsc:implement",
]


@pytest.mark.parametrize("name", IMPL_SPELLINGS)
def test_impl_name_spellings(tmp_path, name):
    # T-SKL-1
    _bind(tmp_path, "worktree")
    _assert_decision(_run(_skill(name), tmp_path), tmp_path, "LL-IMPL", "W")


@pytest.mark.parametrize(
    "name", ["sc:cleanup-audit-protocol", "task-builder", "sc:tasklist-protocol"]
)
def test_lookalike_skill_names_stay_none(tmp_path, name):
    # T-SKL-1: names that only resemble an IMPL skill are NONE.
    _bind(tmp_path, "worktree")
    _assert_decision(_run(_skill(name), tmp_path), tmp_path, None, "W")


@pytest.mark.parametrize("name", ["sc:pr-submit", "sc:pr-submit-protocol"])
@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
def test_submit_name_spellings(tmp_path, name, level):
    # T-SKL-2
    _bind(tmp_path, *LEVEL_FILES[level])
    msg_id = None if level == "FS" else "LL-SUBMIT"
    _assert_decision(_run(_skill(name), tmp_path), tmp_path, msg_id, level)


@pytest.mark.parametrize(
    "tool_input",
    [
        {"skill": "sc:implement"},
        {"name": "sc:implement"},
        {"skill": None, "name": "sc:implement"},
        {"skill": "sc:implement", "name": "sc:workflow"},
    ],
)
def test_skill_name_keys(tmp_path, tool_input):
    # T-SKL-3: skill, else name (a null skill counts as missing).
    _bind(tmp_path, "worktree")
    result = _run(_skill(tool_input=tool_input), tmp_path)
    _assert_decision(result, tmp_path, "LL-IMPL", "W")


def test_explicit_empty_skill_does_not_fall_back_to_name(tmp_path):
    _bind(tmp_path, "full")
    result = _run(_skill(tool_input={"skill": "", "name": "sc:workflow"}), tmp_path)
    _assert_decision(result, tmp_path, "LL-SKILL", "F")


@pytest.mark.parametrize(
    "name", [_ABSENT, "", "   ", "\t\n", "/", "sc:", "sc:sc--protocol"]
)
@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
def test_skill_without_name(tmp_path, name, level):
    # T-SKL-4: no readable name is SKILL; allowed only at full --submit.
    _bind(tmp_path, *LEVEL_FILES[level])
    msg_id = None if level == "FS" else "LL-SKILL"
    _assert_decision(_run(_skill(name), tmp_path), tmp_path, msg_id, level)


@pytest.mark.parametrize("name", ["sc:issue", "sc:issue-protocol"])
@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
def test_issue_skill_escape(tmp_path, name, level):
    # T-SKL-5
    _bind(tmp_path, *LEVEL_FILES[level])
    _assert_decision(_run(_skill(name), tmp_path), tmp_path, "LL-ESCAPE", level)


def test_skill_name_newline_does_not_shift_fields(tmp_path):
    # T-FC-8 (Skill variant): a newline in the name decides as the first word.
    _bind(tmp_path, "worktree")
    result = _run(_skill("sc:implement\nsc:workflow"), tmp_path)
    _assert_decision(result, tmp_path, "LL-IMPL", "W")
    result = _run(_skill("sc:workflow\nsc:implement"), tmp_path)
    _assert_decision(result, tmp_path, None, "W")


# ===========================================================================
# Task 15: speed (T-SPD-1 to T-SPD-5, design section 8, MR NFR-L-01; F2).
#
# Real subprocess runs timed with time.monotonic() around subprocess.run, after
# one untimed warm-up run; 100 runs per case unless the row says otherwise.
# Only T-SPD-3 (ratio) and T-SPD-5 (LARGE_LIMIT_S each) assert; the millisecond
# targets are printed and reported, not asserted, because they are flaky on a
# loaded host. T-SPD-5's limit (3.5 s) is asserted everywhere, xdist workers
# included; the 1 s design target stays a reported figure (#440). Run with -s
# to see the numbers. With LL_SPEED_RESULTS=<path> set, the
# module writes the table of this run to that path after its last test.
# ===========================================================================

SPD_RUNS = 100
# Design section 8 / Task 15: 100 runs per case. A 64 KB run takes 0.5 to 0.9 s,
# so the four T-SPD-5 cases add about 4 minutes to a run of this section.
LARGE_RUNS = SPD_RUNS
# T-SPD-5 per-run limit, asserted on every run including xdist workers (#440).
# Chosen 2026-11-08 from measurements in the #440 plan package
# (.dev/tasks, artifacts/limit-selection.md; slowest 64 KB max per condition):
# idle serial 893.9 ms, full suite under -n auto 998.6 ms, CI's own pre-skip
# failing worst 1166.0 ms; 56 busy loops (2x CPU oversubscription, not a CI
# condition) reached 5536.1 ms, which is why no limit can also cover that arm.
# Coordinator decision on the owner's "diminishing returns" rule: 3.5 s gives
# 3.0x margin over CI's worst observed failing max and stays 1.5 s under the
# 5 s hook timeout where the governed call fails open; a 10x-slower guard
# (10 runs in a row) takes 5.2-7.6 s and still fails this limit, and one more
# doubling would reach the fail-open timeout without clearing the
# oversubscription arm, so loosening stops here. Design target remains 1 s,
# reported (not asserted) per row. Revisit if any CI run exceeds 2 s.
LARGE_LIMIT_S = 3.5
BLOCK_BARE_PYTHON = HOOK.parent / "block-bare-python.sh"
IDENTITY = HOOK.parent / "launch-job-identity.sh"
SPD_COMMAND = "git status && ls -la src"
ENVELOPE_BYTES = 32 * 1024 * 1024
ENVELOPE_RUNS = 5
ENVELOPE_TIMEOUT = 30
GUARD_FOLLOW_UP = (
    "profile the ordinary path of launch-level-guard.sh in a follow-up issue"
)
IDENTITY_FOLLOW_UP = (
    "a follow-up change to launch-job-identity.sh that checks sessions/<session_id> "
    "in bash before starting uv (this plan does not modify that script)"
)
_SPD_ROWS: list[dict] = []


@pytest.fixture(scope="module")
def speed_report():
    yield _SPD_ROWS
    target = os.environ.get("LL_SPEED_RESULTS")
    if target and _SPD_ROWS:
        Path(target).write_text(_spd_markdown())


def _spd_env(tmp_path: Path, home: Path, extra: tuple[str, ...] = ()) -> dict:
    bindir = tmp_path / "bin"
    if not bindir.exists():
        _bin(tmp_path)
        for tool in extra:
            (bindir / tool).symlink_to(shutil.which(tool))
    home.mkdir(exist_ok=True)
    return _env(home, bindir)


def _spd_once(script: Path, stdin: bytes, env: dict, timeout: float = 10):
    started = time.monotonic()
    result = subprocess.run(
        [BASH, str(script)], input=stdin, capture_output=True, env=env, timeout=timeout
    )
    return time.monotonic() - started, result


def _spd_time(script: Path, stdin: bytes, env: dict, runs: int = SPD_RUNS):
    _spd_once(script, stdin, env)  # warm-up, not counted
    times, codes = [], set()
    for _ in range(runs):
        seconds, result = _spd_once(script, stdin, env)
        times.append(seconds)
        codes.add(result.returncode)
    return times, codes


def _ms(times: list[float]) -> tuple[float, float]:
    """Median and 95th percentile in milliseconds."""
    p95 = statistics.quantiles(times, n=20, method="inclusive")[18]
    return statistics.median(times) * 1000, p95 * 1000


def _spd_row(case, runs, times, target, result, follow_up="", note=""):
    median, p95 = _ms(times)
    if result == "reported":
        limits = [float(x) for x in re.findall(r"(\d+) ms", target)]
        values = [median, p95] if len(limits) == 2 else [p95]
        exceeded = any(v > lim for v, lim in zip(values, limits))
        result = "EXCEEDED (reported only)" if exceeded else "within (reported only)"
    row = {
        "case": case,
        "runs": runs,
        "median": f"{median:.1f} ms",
        "p95": f"{p95:.1f} ms",
        "target": target,
        "result": result + (f"; {note}" if note else ""),
        "follow_up": follow_up,
    }
    _SPD_ROWS.append(row)
    print(" | ".join(str(v) for k, v in row.items() if k != "follow_up"))
    return row


def _spd_markdown() -> str:
    bash_version = subprocess.run(
        [BASH, "--version"], capture_output=True, text=True
    ).stdout.splitlines()[0]
    load = " ".join(f"{x:.2f}" for x in os.getloadavg())
    lines = [
        "# Task 15: hook speed results",
        "",
        "Written by the test module tests/hooks/test_launch_level_guard.py (section",
        '"Task 15: speed") at the end of the run below; no number is edited by hand.',
        "",
        f"- Run: {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC, "
        "`LL_SPEED_RESULTS=<this file> uv run pytest "
        'tests/hooks/test_launch_level_guard.py -k "SPD or speed"`.',
        f"- Host: {bash_version}; {os.cpu_count()} CPUs; load average {load} "
        f"when the file was written; Python {sys.version.split()[0]}.",
        "- Method: each run is one real subprocess (bash and the hook script), "
        "timed with time.monotonic() around subprocess.run after one untimed "
        "warm-up run. p95 is the inclusive 95th percentile. PATH holds only a "
        "temporary bin directory; HOME is a temporary directory. T-SPD-5 uses "
        f"{LARGE_RUNS} runs per command (each run takes 0.5 to 0.9 s); the "
        f"envelope stress case uses {ENVELOPE_RUNS} runs, with p95 taken from "
        "those runs.",
        "- Asserted (design section 8): T-SPD-3 (guard median at most 1.5 times "
        "block-bare-python.sh) and T-SPD-5 (every run under LARGE_LIMIT_S, "
        "asserted on every run including xdist workers; the 1 s design target "
        "is reported). Every other row is reported only.",
        "",
        "| Case | Runs | Median | p95 | Target | Result |",
        "|---|---|---|---|---|---|",
    ]
    for row in _SPD_ROWS:
        cells = [row[k] for k in ("case", "runs", "median", "p95", "target", "result")]
        lines.append("| " + " | ".join(str(c) for c in cells) + " |")
    exceeded = [r for r in _SPD_ROWS if r["result"].startswith("EXCEEDED")]
    failed = [r for r in _SPD_ROWS if r["result"].startswith("FAIL")]
    lines += ["", "## Reported targets exceeded", ""]
    lines += [
        f"- {r['case']} exceeded its reported target ({r['target']}); "
        f"follow-up: {r['follow_up']}."
        for r in exceeded
    ] or ["None."]
    lines += ["", "## Asserted targets failed", ""]
    lines += [
        f"- {r['case']} FAILED its asserted target ({r['target']}): {r['result']}."
        for r in failed
    ] or ["None."]
    return "\n".join(lines) + "\n"


def _spd_stale_store(home: Path) -> None:
    """1,000 session files of other sessions and 50 pending records."""
    store = _store(home)
    for name, count, stem in (("sessions", 1000, "other-"), ("pending", 50, "")):
        part = store / name
        part.mkdir(parents=True, mode=0o700)
        for i in range(count):
            (part / (f"{stem}{i:04d}" if stem else f"{i:032x}")).write_text("full")


def _spd_ordinary(tmp_path: Path, stale: bool):
    home = tmp_path / "home"
    env = _spd_env(tmp_path, home, ("awk",))
    if stale:
        _spd_stale_store(home)
    return env, json.dumps(_bash(SPD_COMMAND)).encode()


ORDINARY_TARGET = "median 20 ms, p95 50 ms"


def test_speed_empty_store(tmp_path, speed_report):
    # T-SPD-1: ordinary session, no store at all (the empty-store fast exit).
    env, stdin = _spd_ordinary(tmp_path, stale=False)
    times, codes = _spd_time(HOOK, stdin, env)
    assert codes == {0}
    _spd_row(
        "T-SPD-1 guard, ordinary, empty store",
        SPD_RUNS,
        times,
        ORDINARY_TARGET,
        "reported",
        GUARD_FOLLOW_UP,
    )


def test_speed_stale_store(tmp_path, speed_report):
    # T-SPD-2: ordinary session, store with 1,000 session files and 50 pending.
    env, stdin = _spd_ordinary(tmp_path, stale=True)
    times, codes = _spd_time(HOOK, stdin, env)
    assert codes == {0}
    _spd_row(
        "T-SPD-2 guard, ordinary, store of 1,050 files",
        SPD_RUNS,
        times,
        ORDINARY_TARGET,
        "reported",
        GUARD_FOLLOW_UP,
    )


@pytest.mark.parametrize("stale", [False, True], ids=["empty-store", "stale-store"])
def test_speed_ratio_to_block_bare_python(tmp_path, speed_report, stale):
    # T-SPD-3: the same Bash payload through both hooks, runs interleaved.
    env, stdin = _spd_ordinary(tmp_path, stale)
    store = "store of 1,050 files" if stale else "empty store"
    _spd_once(HOOK, stdin, env)
    _spd_once(BLOCK_BARE_PYTHON, stdin, env)
    guard, other = [], []
    for _ in range(SPD_RUNS):
        for script, times in ((HOOK, guard), (BLOCK_BARE_PYTHON, other)):
            seconds, result = _spd_once(script, stdin, env)
            assert result.returncode == 0, (script.name, result.stderr)
            times.append(seconds)
    ratio = statistics.median(guard) / statistics.median(other)
    verdict = "PASS" if ratio <= 1.5 else "FAIL"
    _spd_row(
        f"T-SPD-3 block-bare-python.sh, ordinary, {store} (same run)",
        SPD_RUNS,
        other,
        "baseline for T-SPD-3",
        "baseline",
    )
    _spd_row(
        f"T-SPD-3 guard, ordinary, {store} (same run)",
        SPD_RUNS,
        guard,
        "median at most 1.5 times block-bare-python.sh (asserted)",
        f"{verdict}: ratio {ratio:.2f}",
    )
    assert ratio <= 1.5, f"T-SPD-3 {store}: guard/block-bare-python ratio {ratio:.2f}"


@pytest.mark.parametrize(
    "command, code",
    [("git status", 0), ("git commit -m x", 2)],
    ids=["allow", "block"],
)
def test_speed_governed(tmp_path, speed_report, command, code):
    # T-SPD-4: governed session at level F (full).
    env = _spd_env(tmp_path, tmp_path / "home")
    _bind(tmp_path, "full")
    times, codes = _spd_time(HOOK, json.dumps(_bash(command)).encode(), env)
    assert codes == {code}
    _spd_row(
        f"T-SPD-4 guard, governed F, {'allow' if code == 0 else 'block'} `{command}`",
        SPD_RUNS,
        times,
        "p95 60 ms",
        "reported",
        GUARD_FOLLOW_UP,
    )


def _spd_fill(head: str, unit: str, tail: str, size: int = 65_536) -> str:
    count, rest = divmod(size - len((head + tail).encode()), len(unit.encode()))
    text = head + " " * rest + unit * count + tail
    assert len(text.encode()) == size
    return text


LARGE_COMMANDS = {
    "heredoc-git-words-64KB": _spd_fill(
        "git commit -m \"$(cat <<'EOF'\nfeat: speed fixture\n\n",
        "Run git status, then git push origin feature and gh pr create --repo o/r.\n",
        'EOF\n)"',
    ),
    "backslash-lines-64KB": _spd_fill("", "git status --short \\\n", "true"),
    "git-status-lines-64KB": _spd_fill("", "git status\n", ""),
    "1MB-big": _spd_fill("", "git status\n", "", 1 << 20),
}


@pytest.mark.parametrize("name", list(LARGE_COMMANDS))
def test_speed_large_commands(tmp_path, speed_report, name):
    # T-SPD-5: governed full-submit session, each run under LARGE_LIMIT_S
    # (3.5 s, asserted; 1 s design target reported).
    env = _spd_env(tmp_path, tmp_path / "home")
    _bind(tmp_path, "full-submit")
    stdin = json.dumps(_bash(LARGE_COMMANDS[name])).encode()
    times, codes = _spd_time(HOOK, stdin, env, LARGE_RUNS)
    if name == "1MB-big":
        assert codes == {2}  # LL-BIG at once
    worst = max(times)
    verdict = "PASS" if worst < LARGE_LIMIT_S else "FAIL"
    if worst >= 1.0:
        verdict += " (over 1 s design target)"
    _spd_row(
        f"T-SPD-5 guard, governed FS, {name}",
        LARGE_RUNS,
        times,
        f"every run under {LARGE_LIMIT_S:g} s (asserted; design target 1 s, reported)",
        f"{verdict}: max {worst * 1000:.1f} ms",
        note=f"exit {sorted(codes)}",
    )
    assert worst < LARGE_LIMIT_S, (
        f"T-SPD-5 {name}: slowest run {worst:.3f} s, limit {LARGE_LIMIT_S:g} s"
    )


@pytest.mark.parametrize("name", list(LARGE_COMMANDS))
def test_speed_large_limit_catches_10x_slower_guard(tmp_path, name):
    # Negative control for LARGE_LIMIT_S (#440): a guard about 10x slower must
    # fail the limit, so the assert above is live on every runner (xdist
    # included). Ten runs of the slowest 64 KB case (~0.9 s each) take well
    # over LARGE_LIMIT_S; 10x is not a sensitivity bound (measured margins:
    # 1.3x to 2.2x over the limit at 3.5 s).
    env = _spd_env(tmp_path, tmp_path / "home")
    _bind(tmp_path, "full-submit")
    payload = tmp_path / "in.json"
    payload.write_bytes(json.dumps(_bash(LARGE_COMMANDS[name])).encode())
    run = " ".join(shlex.quote(str(p)) for p in (BASH, HOOK))
    slow = tmp_path / "slow-guard.sh"
    slow.write_text(
        f"for _ in 1 2 3 4 5 6 7 8 9 10; do {run} "
        f"< {shlex.quote(str(payload))} >/dev/null 2>&1; done\n"
    )
    seconds, _ = _spd_once(slow, b"", env, timeout=120)
    assert seconds > LARGE_LIMIT_S, (
        f"{name}: 10 guard runs took {seconds:.3f} s, limit {LARGE_LIMIT_S:g} s"
    )


def _spd_wait4(script: Path, stdin_path: Path, env: dict, timeout: float):
    """Seconds, exit code and peak RSS (KiB) of the hook and its children."""
    started = time.monotonic()
    with stdin_path.open("rb") as stdin:
        proc = subprocess.Popen(
            [BASH, str(script)],
            stdin=stdin,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
        )
    while True:
        pid, status, usage = os.wait4(proc.pid, os.WNOHANG)
        if pid:
            proc.returncode = os.waitstatus_to_exitcode(status)
            return time.monotonic() - started, proc.returncode, usage.ru_maxrss
        if time.monotonic() - started > timeout:
            proc.kill()
            _, status, _ = os.wait4(proc.pid, 0)
            proc.returncode = os.waitstatus_to_exitcode(status)
            return None, None, None
        time.sleep(0.002)


@pytest.mark.parametrize("governed", [False, True], ids=["ordinary", "governed"])
def test_speed_large_envelope(tmp_path, speed_report, governed):
    # Design section 8: a very large non-command field; time and memory, or a
    # timeout, are the result. No size limit is implied or asserted.
    home = tmp_path / "home"
    env = _spd_env(tmp_path, home)
    if governed:
        _bind(tmp_path, "full")
    else:
        _spd_stale_store(home)  # a store is present, so the guard parses the input
    payload = _bash("git status", description="x" * ENVELOPE_BYTES)
    stdin_path = tmp_path / "envelope.json"
    stdin_path.write_bytes(json.dumps(payload).encode())
    size_mib = stdin_path.stat().st_size / (1 << 20)
    times, codes, peak = [], set(), 0
    for _ in range(ENVELOPE_RUNS):
        seconds, code, rss = _spd_wait4(HOOK, stdin_path, env, ENVELOPE_TIMEOUT)
        if seconds is None:
            break
        times.append(seconds)
        codes.add(code)
        peak = max(peak, rss)
    case = (
        f"Envelope stress, guard, {'governed F' if governed else 'ordinary'}, "
        f"{size_mib:.0f} MiB description field"
    )
    target = "none; report time and memory, or a timeout"
    if len(times) < ENVELOPE_RUNS:
        row = {
            "case": case,
            "runs": f"{len(times) + 1} (stopped)",
            "median": "-",
            "p95": "-",
            "target": target,
            "result": f"TIMEOUT after {ENVELOPE_TIMEOUT} s",
            "follow_up": "",
        }
        _SPD_ROWS.append(row)
        print(row)
        return
    _spd_row(
        case,
        ENVELOPE_RUNS,
        times,
        target,
        f"completed, exit {sorted(codes)}, peak RSS {peak / 1024:.0f} MiB "
        "(largest process of the hook tree)",
    )


def test_speed_identity_hook_with_pending_only_store(tmp_path, speed_report):
    # F2: an ordinary Bash call through launch-job-identity.sh (not modified
    # here) with a store that holds only pending/, as a claim leaves it, against
    # the same call with no store. UV environment of test_launch_job_identity.py.
    none_home, pending_home = tmp_path / "home-none", tmp_path / "home-pending"
    env_none = _spd_env(tmp_path, none_home, ("awk", "uv"))
    env_none.update(UV_PYTHON=sys.executable, UV_PYTHON_DOWNLOADS="never")
    env_pending = {**env_none, "HOME": str(pending_home)}
    pending_home.mkdir()
    pending = _store(pending_home) / "pending"
    pending.mkdir(parents=True, mode=0o700)
    (pending / NONCE).write_text("full")
    stdin = json.dumps({**_bash(SPD_COMMAND), "tool_use_id": "toolu_01"}).encode()
    cases = (("no store", env_none, []), ("store with only pending/", env_pending, []))
    for _, env, _ in cases:
        _spd_once(IDENTITY, stdin, env, timeout=30)
    for _ in range(SPD_RUNS):
        for _, env, times in cases:
            seconds, result = _spd_once(IDENTITY, stdin, env, timeout=30)
            assert (result.returncode, result.stdout) == (0, b""), result.stderr
            times.append(seconds)
    for label, _, times in cases:
        _spd_row(
            f"F2 launch-job-identity.sh, ordinary Bash, {label}",
            SPD_RUNS,
            times,
            "median 20 ms, p95 50 ms (ordinary budget, reported only)",
            "reported",
            IDENTITY_FOLLOW_UP,
        )


def test_huge_fields_are_quick(tmp_path):
    # Line splitting must stay linear: _run's 10 s timeout fails a quadratic split.
    _bind(tmp_path, "worktree")
    result = _run(_skill("sc:implement " + "x" * 200_000), tmp_path)
    _assert_decision(result, tmp_path, "LL-IMPL", "W")
    bash = {**VALID_PAYLOADS["pretooluse-bash"], "session_id": SID}
    # Just under the 65,536-byte cap the whole text is normalised, many lines.
    bash["tool_input"] = {"command": "echo " + "y\n" * 32_000}
    _assert_decision(_run(bash, tmp_path), tmp_path, None, "W")
    bash["tool_input"] = {"command": "echo " + "y\n" * 100_000}
    _assert_decision(_run(bash, tmp_path), tmp_path, "LL-BIG", "W", text=True)
    # Not JSON (closing brace cut), the bound id after the long field: LL-BROKEN.
    raw = json.dumps(_skill("sc:workflow", tool_input=bash["tool_input"])).encode()
    _assert_decision(_run(raw[:-1], tmp_path), tmp_path, "LL-BROKEN", "W")


@pytest.mark.parametrize(
    "tool_name, tool_input",
    [
        ("Edit", {"file_path": "/x/settings.json"}),
        ("Read", {"file_path": "/etc/passwd"}),
    ],
)
def test_other_tools_are_none(tmp_path, tool_name, tool_input):
    # FR-L-66: a tool no classifier names is NONE (Agent and MCP: Task 10 tests).
    _bind(tmp_path, "worktree")
    payload = {
        "hook_event_name": "PreToolUse",
        "session_id": SID,
        "tool_name": tool_name,
        "tool_input": tool_input,
    }
    _assert_decision(_run(payload, tmp_path), tmp_path, None, "W")


BAD_FIELDS = {
    "numeric-skill": {"tool_name": "Skill", "tool_input": {"skill": 7}},
    "object-name": {"tool_name": "Skill", "tool_input": {"name": {"a": 1}}},
    "nul-skill": {"tool_name": "Skill", "tool_input": {"skill": "sc:work\u0000flow"}},
    "numeric-tool-name": {"tool_name": 5, "tool_input": {}},
    "list-tool-input": {"tool_name": "Skill", "tool_input": ["sc:implement"]},
    "numeric-command": {"tool_name": "Bash", "tool_input": {"command": 1}},
    "nul-command": {"tool_name": "Bash", "tool_input": {"command": "ls\u0000"}},
    "list-path": {"tool_name": "Write", "tool_input": {"file_path": ["a"]}},
    "bool-isolation": {"tool_name": "Task", "tool_input": {"isolation": True}},
}


@pytest.mark.parametrize("name", sorted(BAD_FIELDS))
def test_input_error_blocks_governed_broken(tmp_path, name):
    _bind(tmp_path, "full-submit")
    payload = {"hook_event_name": "PreToolUse", "session_id": SID, **BAD_FIELDS[name]}
    _assert_decision(_run(payload, tmp_path), tmp_path, "LL-BROKEN", "FS")


@pytest.mark.parametrize("name", sorted(BAD_FIELDS))
def test_input_error_allows_ordinary(tmp_path, name):
    _bind(tmp_path, "worktree")
    payload = {
        "hook_event_name": "PreToolUse",
        "session_id": "other",
        **BAD_FIELDS[name],
    }
    _assert_decision(_run(payload, tmp_path), tmp_path, None, "W")


# --- PreToolUse resolution: isolation and fail-closed (Task 5) -------------


@pytest.mark.parametrize("store", ["empty", "other-sessions"])
@pytest.mark.parametrize("name", sorted(SKILL_EXPECTED))
def test_ordinary_session_never_blocked(tmp_path, store, name):
    # T-ISO-1
    if store == "other-sessions":
        sessions = _store(tmp_path / "home") / "sessions"
        sessions.mkdir(parents=True)
        (sessions / "someone-else").write_text("worktree")
    result = _run(_skill(name, sid="unbound-session"), tmp_path)
    _assert_decision(result, tmp_path, None, "W")


def test_two_sessions_isolated(tmp_path):
    # T-ISO-2
    sessions = _store(tmp_path / "home") / "sessions"
    sessions.mkdir(parents=True)
    (sessions / "session-a").write_text("worktree")
    (sessions / "session-b").write_text("full-submit")
    a = _run(_skill("sc:pr-submit", sid="session-a"), tmp_path)
    b = _run(_skill("sc:pr-submit", sid="session-b"), tmp_path)
    store = str(_store(tmp_path / "home"))
    assert a.returncode == 2
    assert a.stderr.decode() == _expected("LL-SUBMIT", "worktree", "session-a", store)
    assert (b.returncode, b.stderr) == (0, b"")


def test_same_worktree_other_session_ordinary(tmp_path):
    # T-ISO-3: cwd is never read on PreToolUse.
    _bind(tmp_path, "worktree")
    result = _run(_skill("sc:implement", sid="other", cwd="/work/wt"), tmp_path)
    _assert_decision(result, tmp_path, None, "W")


def test_person_subagent_not_governed(tmp_path):
    # T-ISO-4 (X-004): unbound id plus agent_id plus the bound worktree's cwd.
    _bind(tmp_path, "worktree")
    payload = _skill("sc:implement", sid="person", agent_id="a1", cwd="/work/wt")
    _assert_decision(_run(payload, tmp_path), tmp_path, None, "W")


@pytest.mark.parametrize(
    "payload",
    [
        b"this is not json",
        b'{"hook_event_name": "PreToolUse", "tool_name": "Skill", "session_id": "unbound-x", ',
        {"hook_event_name": "PreToolUse", "session_id": SID, "tool_name": "Skill"},
        {"hook_event_name": "PreToolUse", "session_id": SID, "tool_name": "Frobnicate"},
    ],
    ids=["not-json", "truncated-unbound", "no-tool-input", "unknown-tool"],
)
def test_fail_open_shapes_ordinary(tmp_path, payload):
    # T-ISO-5: with an empty store, and with a store that holds only other ids.
    result = _run(payload, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    sessions = _store(tmp_path / "home") / "sessions"
    sessions.mkdir(parents=True)
    (sessions / "someone-else").write_text("worktree")
    if isinstance(payload, dict):
        payload = {**payload, "session_id": "unbound-x"}
    result = _run(payload, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_forged_nested_session_id(tmp_path):
    # T-ISO-6: only the top-level session_id counts.
    _bind(tmp_path, "worktree")
    ordinary = _skill("sc:implement", sid="unbound-one", meta={"session_id": SID})
    _assert_decision(_run(ordinary, tmp_path), tmp_path, None, "W")
    governed = _skill("sc:implement", tool_input={"session_id": "unbound-two"})
    _assert_decision(_run(governed, tmp_path), tmp_path, "LL-IMPL", "W")


def test_subagent_governed(tmp_path):
    """T-ISO-7: parent id plus agent_id is governed (pending OB-H1: hand-written
    shape; agent_id is never read on PreToolUse)."""
    _bind(tmp_path, "worktree")
    payload = _skill("sc:implement", agent_id="subagent-0001")
    _assert_decision(_run(payload, tmp_path), tmp_path, "LL-IMPL", "W")


def test_nested_subagent_governed(tmp_path):
    """T-ISO-8: nested shape with agent_type is governed (pending OB-H1:
    hand-written shape)."""
    _bind(tmp_path, "full")
    payload = _skill("sc:pr-submit", agent_id="nested-0002", agent_type="Explore")
    _assert_decision(_run(payload, tmp_path), tmp_path, "LL-SUBMIT", "F")


@pytest.mark.parametrize(
    "shape",
    ["missing", "invalid", "numeric", "nested-forged", "unparseable"],
)
def test_identity_loss_allows_silently(tmp_path, shape):
    # Declared fail-open limit (design section 3; overrides MR T-FC-6): with no
    # readable top-level session_id the guard cannot tell a governed session
    # from an ordinary one, so the call is allowed with no message, even while
    # the store holds a bound session. A governed session that loses its id is
    # therefore not enforced; this is accepted, not a bug.
    _bind(tmp_path, "worktree")
    payloads = {
        "missing": _skill("sc:implement", sid=None),
        "invalid": _skill("sc:implement", sid="bad id!"),
        "numeric": _skill("sc:implement", sid=12345),
        "nested-forged": _skill("sc:implement", sid=None, meta={"session_id": SID}),
        "unparseable": b'{"hook_event_name": "PreToolUse", "tool_input": {',
    }
    result = _run(payloads[shape], tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


@pytest.mark.parametrize("bound", [True, False])
def test_jq_missing(tmp_path, bound):
    # T-FC-1: governed gives LL-BROKEN at the bound level; ordinary exits 0.
    _bin(tmp_path, with_jq=False)
    _bind(tmp_path, "full")
    sid = SID if bound else "unbound-session"
    result = _run(_skill("sc:workflow", sid=sid), tmp_path)
    if bound:
        _assert_decision(result, tmp_path, "LL-BROKEN", "F")
    else:
        assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


@pytest.mark.parametrize("state", ["empty", "garbage", "degraded", "mode-000"])
@pytest.mark.parametrize("ok", [False, True])
def test_bad_state_degrades_to_worktree(tmp_path, state, ok):
    # T-FC-2: W column plus LL-STATE; an existing .ok still counts (WA, allowed).
    if state == "mode-000" and os.geteuid() == 0:
        pytest.skip("root reads a mode-000 file")
    word = {"empty": "", "garbage": "rm -rf /", "degraded": "degraded"}.get(
        state, "full"
    )
    sessions = _bind(tmp_path, word, ok)
    if state == "mode-000":
        (sessions / SID).chmod(0)
    result = _run(_skill("sc:implement"), tmp_path)
    if ok:
        _assert_decision(result, tmp_path, None, "WA")
    else:
        _assert_decision(result, tmp_path, "LL-IMPL", "W", note=True)


@pytest.mark.parametrize(
    "raw",
    [
        b'{"hook_event_name": "PreToolUse", "session_id": "sess-abc_123", "tool_name": "Skill", ',
        b'{"hook_event_name": "PreToolUse", "tool_input": {"session_id": "x"}, '
        b'"session_id": "sess-abc_123", "tool_name": "Bash" garbage',
    ],
    ids=["truncated", "bound-id-after-another"],
)
def test_not_json_governed(tmp_path, raw):
    # T-FC-5: a tool payload that is not JSON but holds a bound id: LL-BROKEN.
    _bind(tmp_path, "full-submit")
    _assert_decision(_run(raw, tmp_path), tmp_path, "LL-BROKEN", "FS")


@pytest.mark.parametrize("forged", [10, 70, 500])
def test_raw_id_scan_has_no_cap(tmp_path, forged):
    # A payload with many unbound session_id strings before the bound one must
    # still find it: a fixed cap would be a fail-open (plan Task 5 constraint).
    _bind(tmp_path, "full")
    nested = ", ".join(f'"session_id": "forged{n}"' for n in range(forged))
    raw = (
        '{"hook_event_name": "PreToolUse", "tool_input": {' + nested + "}, "
        f'"session_id": "{SID}", "tool_name": "Bash" garbage'
    ).encode()
    _assert_decision(_run(raw, tmp_path), tmp_path, "LL-BROKEN", "F")


def test_raw_id_scan_declared_limit_blocks_ordinary_with_nested_bound_id(tmp_path):
    # Declared limit (design section 3 versus T-FC-5): on a failure path a bound
    # id anywhere in broken JSON counts, so an ordinary session that sends
    # broken JSON containing a bound id is blocked.
    _bind(tmp_path, "full")
    raw = (
        b'{"hook_event_name": "PreToolUse", "session_id": "ordinary1", '
        b'"tool_input": {"session_id": "'
        + SID.encode()
        + b'"}, "tool_name": "Bash" garbage'
    )
    _assert_decision(_run(raw, tmp_path), tmp_path, "LL-BROKEN", "F")


# --- message texts (printer block, test-only route) ------------------------


def test_design_table_holds_all_eighteen_ids():
    assert sorted(_design_table()) == sorted(IDS)


@pytest.mark.parametrize("msg_id", IDS)
@pytest.mark.parametrize("level", sorted(LEVELS))
def test_every_message_prints_the_design_text(tmp_path, msg_id, level):
    result = _printer(tmp_path, msg_id, level)
    store = str(_store(tmp_path / "home"))
    assert result.returncode == 0
    assert result.stdout == b""
    assert result.stderr.decode() == _expected(msg_id, LEVELS[level], SID, store)


@pytest.mark.parametrize("msg_id", ["LL-BROKEN", "LL-NOBIND"])
def test_unknown_level_prints_bare_header(tmp_path, msg_id):
    result = _printer(tmp_path, msg_id, "")
    store = str(_store(tmp_path / "home"))
    assert result.stderr.decode() == _expected(msg_id, None, SID, store)
    assert result.stderr.decode().splitlines()[0] == "Launch-level guard:"


def test_tamper_with_invalid_sid_uses_broken_wording(tmp_path):
    result = _printer(tmp_path, "LL-TAMPER", "F", sid="")
    store = str(_store(tmp_path / "home"))
    assert result.stderr.decode() == _expected("LL-BROKEN", "full", "", store)


def test_notes_follow_the_lines_state_first(tmp_path):
    result = _printer(tmp_path, "LL-COMMIT", "W", notes="11")
    store = str(_store(tmp_path / "home"))
    assert result.stderr.decode() == (
        _expected("LL-COMMIT", "worktree", SID, store)
        + _design_note("LL-STATE")
        + "\n"
        + _design_note("LL-TEXT")
        + "\n"
    )
    assert _design_note("LL-STATE") == STATE_NOTE


# --- Task 6: Bash and Monitor normalisation (T-NRM, T-FC-7) ----------------
#
# A row whose class needs a later classifier names that task in its last field
# and is pinned with a strict xfail, so the task that reaches the class must
# drop the mark (Tasks 7 to 9, git, gh, tamper and escape, have dropped theirs).
# "?" marks a level that the T-NRM row does not pin.

LEVEL_ORDER = ("W", "WA", "F", "FS")
UNK = ("LL-UNKNOWN",) * 4
PUSH = ("LL-PUSH", "LL-PUSH", "LL-PUSH", "LL-PUSH-FORM")
COMMIT = ("LL-COMMIT", "LL-COMMIT", "LL-COMMIT", None)
MERGE = ("LL-MERGE",) * 4
GHWRITE = ("LL-GH-WRITE",) * 4
TAMPER = ("LL-TAMPER",) * 4
ESCAPE = ("LL-ESCAPE",) * 4
NONE4 = (None,) * 4
FS_ONLY = ("?", "?", "?")
STATE_PATH = "~/.cla" + "ude/state"  # spelled in two parts, as the script must

NRM_E2E = [
    # T-NRM-1: quote and backslash splicing; amendment cases N-ATK-3 to 33.
    ("nrm1-quote-push", 'g""it push origin main', PUSH, None),
    ("nrm1-backslash-push", "\\git push origin main", PUSH, None),
    ("nrm1-split-quote", "git push origin 'feature:ma''in'", PUSH, None),
    ("nrm1-split-backslash", "git push origin feature:ma\\in", PUSH, None),
    ("nrm1-quote-commit", 'g""it commit -m x', ("?", "?", "LL-COMMIT", "?"), None),
    ("nrm1-backslash-commit", "\\git commit -m x", ("?", "?", "LL-COMMIT", "?"), None),
    ("natk3", "git$'' push origin HEAD:main", PUSH, None),
    ("natk4", 'g$""it push origin HEAD:main', PUSH, None),
    ("natk15", "git$'' -c x.y=z push origin HEAD:main", PUSH, None),
    ("natk16", "git$'' merge other --no-edit", MERGE, None),
    ("natk18", "git$'' commit --allow-empty -m x", COMMIT, None),
    ("natk23", "g$''h pr merge 5", MERGE, None),
    (
        "natk24",
        "flock /tmp/l gh a$''pi -X DELETE repos/o/r/git/refs/heads/main",
        GHWRITE,
        None,
    ),
    (
        "natk30",
        f"rm -rf {STATE_PATH.replace('cla', 'cla$' + chr(39) * 2)}",
        TAMPER,
        None,
    ),
    ("natk32", "cp /tmp/s.json ~/.claude/set$''tings.json", TAMPER, None),
    ("natk33", ": > ~/.claude/hoo$''ks/launch-level-guard.sh", TAMPER, None),
    # T-NRM-2: redirections stay words.
    ("nrm2-stdin", "git commit -m x < /dev/null", FS_ONLY + (None,), None),
    ("nrm2-stdout", "git commit -m x > /tmp/log 2>&1", FS_ONLY + (None,), None),
    ("nrm2-status", "git status 2>&1 | tail -5", FS_ONLY + (None,), None),
    (
        "nrm2-push",
        "git push origin a:b 2>&1 | tail -5",
        FS_ONLY + ("LL-PUSH-FORM",),
        None,
    ),
    # T-NRM-4: \/ escapes in a tamper path.
    ("nrm4-escaped-slash", "cp x ~\\/.claude\\/\\/.\\/settings.json", TAMPER, None),
    # T-NRM-5: a continuation is not joined.
    ("nrm5-gh-api", "gh api \\\n-X PATCH repos/o/r/git/refs/heads/main", GHWRITE, None),
    ("nrm5-push", "git push origin a:b \\\nc:main", FS_ONLY + ("LL-PUSH-FORM",), None),
    (
        "nrm5-double-backslash",
        "git status \\\\\ngit -c alias.p=push p origin HEAD:main",
        UNK,
        None,
    ),
    # Design H4 overrides MR row 21 and T-NRM-5 (design section 11, "nonempty
    # PR repo operands"): the repo operand must sit in the pr create segment,
    # and the newline ends that segment, so FS gets LL-REPO, not an allow.
    (
        "nrm5-pr-create",
        'gh pr create \\\n--repo "$REPO" --title x --body y',
        ("LL-SUBMIT",) * 3 + ("LL-REPO",),
        None,
    ),
    ("nrm5-claude", "claude \\\n-p x", ESCAPE, None),
    ("nrm5-git-space", "git \\\ncommit -m x", UNK, None),
    # T-NRM-7: a quoted ">" in an assignment.
    ("nrm7-commit", 'A=">" git commit -m x', ("?", "?", "LL-COMMIT", None), None),
    ("nrm7-push", 'A=">" git push origin HEAD:main', PUSH, None),
    # T-NRM-8: NM1a, a backslash-newline inside a word, is UNKNOWN (reachable now).
    ("natk1", "gi\\\nt push origin HEAD:main", UNK, None),
    ("natk2", 'bash -c "gi\\\nt push origin HEAD:main"', UNK, None),
    ("natk17", "gi\\\nt merge other --no-edit", UNK, None),
    ("natk19", "gi\\\nt commit --allow-empty -m x", UNK, None),
    ("natk25", "g\\\nh pr merge 5", UNK, None),
    ("natk28", 'cl\\\naude -p "finish the task"', UNK, None),
    ("natk29", "rm -rf " + STATE_PATH.replace("cla", "cla\\\n"), UNK, None),
    ("natk34-tmux", "tm\\\nux send-keys approved Enter", UNK, None),
    ("natk34-orca", "or\\\nca terminal send --terminal t1 --text approved", UNK, None),
    (
        "nrm8-push-space",
        "git push origin a:b \\\n c:main",
        FS_ONLY + ("LL-PUSH-FORM",),
        None,
    ),
]


def _nrm_params():
    for name, command, ids, task in NRM_E2E:
        for level, msg_id in zip(LEVEL_ORDER, ids):
            if msg_id == "?":
                continue
            marks = ()
            if msg_id and task:
                marks = pytest.mark.xfail(
                    strict=True, reason=f"class reached in Task {task}"
                )
            yield pytest.param(
                command, level, msg_id, id=f"{name}-{level}", marks=marks
            )


def _bash(command: str, tool: str = "Bash", **extra) -> dict:
    return {
        "hook_event_name": "PreToolUse",
        "session_id": SID,
        "tool_name": tool,
        "tool_input": {"command": command, **extra},
    }


@pytest.mark.parametrize("command, level, msg_id", list(_nrm_params()))
def test_nrm_end_to_end(tmp_path, command, level, msg_id):
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(_bash(command), tmp_path)
    _assert_decision(result, tmp_path, msg_id, level, text=msg_id is not None)


@pytest.mark.parametrize("level", LEVEL_ORDER)
def test_nrm4_json_escaped_slash_decoded(tmp_path, level):
    # T-NRM-4: raw JSON bytes with \/ escapes; jq decodes them before the tamper check.
    _bind(tmp_path, *LEVEL_FILES[level])
    raw = (
        b'{"hook_event_name": "PreToolUse", "session_id": "' + SID.encode() + b'", '
        b'"tool_name": "Bash", "tool_input": {"command": '
        b'"cp x ~\\/.claude\\/settings.json"}}'
    )
    _assert_decision(_run(raw, tmp_path), tmp_path, "LL-TAMPER", level, text=True)


@pytest.mark.parametrize("level", ["W", "WA", "F"])
@pytest.mark.parametrize(
    "command",
    [
        "git push origin a:b \\\nc:main",
        "git push origin a:b \\\n c:main",
        "git push origin a:b 2>&1 | tail -5",
    ],
    ids=["nrm5-push", "nrm8-push-space", "nrm2-push"],
)
def test_nrm_push_blocked_below_fs(tmp_path, level, command):
    # T-NRM-5/8/2: a push is blocked at every level (LL-PUSH-FORM only at FS, tested above);
    # below FS the grid blocks every push form, whichever of its three ids applies.
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(_bash(command), tmp_path)
    assert result.returncode == 2
    # The printed text carries no id, so compare with each id's full message.
    store = str(_store(tmp_path / "home"))
    note = _design_note("LL-TEXT") + "\n"
    assert result.stderr.decode() in {
        _expected(i, LEVELS[level], SID, store) + note
        for i in ("LL-PUSH", "LL-PUSH-FORM", "LL-PROTECTED")
    }


def _normalise(tmp_path: Path, command: str):
    """Run only the normalise block of the script (test-only route)."""
    driver = (
        "LC_ALL=C; ll_deny() { exit 3; }; set -f; LL_CLASSES=' '; cmd=$2\n"
        'eval "$(sed -n \'/# >>> normalise/,/# <<< normalise/p\' "$1")"\n'
        'printf \'%s\\0\' "$LL_CLASSES" "$T" "$G"\n'
        'for s in "${segs[@]}"; do ws=($s); printf \'%s\\0\' "${ws[*]}"; done\n'
    )
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    result = subprocess.run(
        [BASH, "-c", driver, "_", str(HOOK), command],
        capture_output=True,
        env=_env(home, _bin(tmp_path)),
        timeout=10,
    )
    assert (result.returncode, result.stderr) == (0, b"")
    classes, t, g, *segs = result.stdout.decode().split("\0")[:-1]
    return classes.split(), t, g.split(), [s for s in segs if s]


def test_nrm_block_is_marked_once():
    text = HOOK.read_text()
    assert text.count("# >>> normalise") == 1
    assert text.count("# <<< normalise") == 1


# T-NRM-6: the worked example of FR-L-27.
@pytest.mark.parametrize(
    "command, t, segs",
    [
        (
            "git commit -F - <<'EOF'\nfix: use git for hooks\nEOF",
            "git commit -F - <<EOF\nfix: use git for hooks\nEOF",
            ["git commit -F - EOF", "fix: use git for hooks", "EOF"],
        ),
        (
            "gh api \\\n-X PATCH repos/o/r/git/refs/heads/main -f sha=x",
            None,
            ["gh api", "-X PATCH repos/o/r/git/refs/heads/main -f sha=x"],
        ),
        (
            "git push origin a:b 2>&1 | tail -5",
            None,
            ["git push origin a:b 2", "1", "tail -5"],
        ),
        (
            'A=">" git push origin HEAD:main',
            None,
            ["A= git push origin HEAD:main"],
        ),
        (
            "echo x > ~/.claude//./settings.json",
            "echo x > ~/.claude/settings.json",
            None,
        ),
        ("g$''it push origin main", "git push origin main", None),
    ],
)
def test_nrm6_worked_example(tmp_path, command, t, segs):
    classes, got_t, _, got_segs = _normalise(tmp_path, command)
    assert classes == []
    if t is not None:
        assert got_t == t
    if segs is not None:
        assert got_segs == segs


def test_nrm6_g_words_never_split(tmp_path):
    command = "git rebase -x 'git -c alias.p=push p origin HEAD:main' HEAD~1"
    _, _, g, segs = _normalise(tmp_path, command)
    words = "git rebase -x git -c alias.p push p origin head:main head~1".split()
    assert g == words * 2  # raw text then T, each lower-cased
    assert segs == ["git rebase -x git -c alias.p=push p origin HEAD:main HEAD~1"]


# T-NRM-1, T-NRM-4, T-NRM-7 and the N-ATK splices: the T text the classifiers read.
@pytest.mark.parametrize(
    "command, t",
    [
        ('g""it push origin main', "git push origin main"),
        ("\\git push origin main", "git push origin main"),
        ("git push origin 'feature:ma''in'", "git push origin feature:main"),
        ("git push origin feature:ma\\in", "git push origin feature:main"),
        ('g""it commit -m x', "git commit -m x"),
        ("\\git commit -m x", "git commit -m x"),
        ("git$'' push origin HEAD:main", "git push origin HEAD:main"),
        ('g$""it push origin HEAD:main', "git push origin HEAD:main"),
        ("git$'' -c x.y=z push origin HEAD:main", "git -c x.y=z push origin HEAD:main"),
        ("git$'' merge other --no-edit", "git merge other --no-edit"),
        ("git$'' commit --allow-empty -m x", "git commit --allow-empty -m x"),
        ("g$''h pr merge 5", "gh pr merge 5"),
        (
            "flock /tmp/l gh a$''pi -X DELETE repos/o/r/git/refs/heads/main",
            "flock /tmp/l gh api -X DELETE repos/o/r/git/refs/heads/main",
        ),
        (
            "rm -rf " + STATE_PATH.replace("cla", "cla$''"),
            "rm -rf " + STATE_PATH,
        ),
        (
            "cp /tmp/s.json ~/.claude/set$''tings.json",
            "cp /tmp/s.json ~/.claude/settings.json",
        ),
        (
            ": > ~/.claude/hoo$''ks/launch-level-guard.sh",
            ": > ~/.claude/hooks/launch-level-guard.sh",
        ),
        (
            "cp x ~\\/.claude\\/\\/.\\/settings.json",
            "cp x ~/.claude/settings.json",
        ),
        ('A=">" git commit -m x', "A=> git commit -m x"),
    ],
)
def test_nrm_splices_reach_t(tmp_path, command, t):
    classes, got_t, g, _ = _normalise(tmp_path, command)
    assert (classes, got_t) == ([], t)
    # G ends with T lower-cased, characters outside its word set made spaces.
    t_words = re.sub(r"[^a-z0-9._/~$@+:-]", " ", t.lower()).split()
    assert g[-len(t_words) :] == t_words


# T-NRM-2 and T-NRM-7: redirections and a quoted ">" stay inside their segment.
@pytest.mark.parametrize(
    "command, segs",
    [
        ("git commit -m x < /dev/null", ["git commit -m x /dev/null"]),
        ("git commit -m x > /tmp/log 2>&1", ["git commit -m x /tmp/log 2", "1"]),
        ("git status 2>&1 | tail -5", ["git status 2", "1", "tail -5"]),
        ('A=">" git commit -m x', ["A= git commit -m x"]),
    ],
)
def test_nrm_redirections_kept_as_words(tmp_path, command, segs):
    assert _normalise(tmp_path, command)[3] == segs


# T-NRM-3: each separator starts a new segment.
@pytest.mark.parametrize(
    "command",
    [
        "git status; git log",
        "git status && git log",
        "git status || git log",
        "git status | git log",
        "git status\ngit log",
        "git status $(git log)",
        "git status `git log`",
    ],
)
def test_nrm3_separators_start_segments(tmp_path, command):
    _, _, _, segs = _normalise(tmp_path, command)
    words = [s.split() for s in segs]
    assert not any("status" in w and "log" in w for w in words)
    assert any(w[:2] == ["git", "log"] for w in words)


# NM1a [B-1]: only a backslash-newline inside a word gives UNKNOWN.
@pytest.mark.parametrize(
    "command, classes",
    [
        ("gi\\\nt push origin HEAD:main", ["UNKNOWN"]),
        ('bash -c "gi\\\nt push origin HEAD:main"', ["UNKNOWN"]),
        ("rm -rf " + STATE_PATH.replace("cla", "cla\\\n"), ["UNKNOWN"]),
        ("or\\\nca terminal send --terminal t1 --text approved", ["UNKNOWN"]),
        ("git push origin a:b \\\nc:main", []),
        ("git push origin a:b \\\n c:main", []),
        ("git status \\\\\ngit -c alias.p=push p origin HEAD:main", []),
        ('gh pr create \\\n--repo "$REPO" --title x --body y', []),
        ("claude \\\n-p x", []),
        ("git \\\ncommit -m x", []),
    ],
)
def test_nrm1a_in_word_continuation(tmp_path, command, classes):
    assert _normalise(tmp_path, command)[0] == classes


# T-FC-7 and NM1: a governed command over 65,536 bytes is BIG; bytes, not characters.
BIG_TEXTS = {
    "multibyte": "€" * 21845 + "é",
    "ascii": "x" * 65537,
    "multibyte-nm1a": "gi\\\nt " + "€" * 21843 + "a" * 2,
}


@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
@pytest.mark.parametrize("name", sorted(BIG_TEXTS))
def test_nrm_fc7_over_65536_bytes_big(tmp_path, name, level):
    assert len(BIG_TEXTS[name].encode()) == 65537
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(_bash(BIG_TEXTS[name]), tmp_path)
    _assert_decision(result, tmp_path, "LL-BIG", level, text=True)


@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
def test_nrm_fc7_exactly_65536_bytes_not_big(tmp_path, level):
    command = "€" * 21845 + "a"
    assert len(command.encode()) == 65536
    _bind(tmp_path, *LEVEL_FILES[level])
    _assert_decision(_run(_bash(command), tmp_path), tmp_path, None, level)


@pytest.mark.parametrize("store", [False, True])
def test_nrm_fc7_ordinary_session_has_no_cap(tmp_path, store):
    if store:
        sessions = _store(tmp_path / "home") / "sessions"
        sessions.mkdir(parents=True)
        (sessions / "other-session").write_text("worktree")
    result = _run(_bash(BIG_TEXTS["multibyte"]), tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
def test_nrm_monitor_ws_only_is_none(tmp_path, level):
    _bind(tmp_path, *LEVEL_FILES[level])
    payload = {
        "hook_event_name": "PreToolUse",
        "session_id": SID,
        "tool_name": "Monitor",
        "tool_input": {"ws": {"url": "wss://example.test/s"}, "timeout_ms": 1000},
    }
    _assert_decision(_run(payload, tmp_path), tmp_path, None, level)


@pytest.mark.parametrize(
    "payload",
    [
        _bash("gi\\\nt push origin HEAD:main", tool="Monitor", timeout_ms=1000),
        _bash("gi\\\nt push origin HEAD:main", run_in_background=True),
    ],
    ids=["monitor", "background-bash"],
)
def test_nrm_monitor_and_background_bash_normalised(tmp_path, payload):
    _bind(tmp_path, "full-submit")
    result = _run(payload, tmp_path)
    _assert_decision(result, tmp_path, "LL-UNKNOWN", "FS", text=True)


def _counting_bin(tmp_path: Path) -> Path:
    """A bin whose sed and tr log each run, then run the real tool."""
    bindir = _bin(tmp_path)
    log = tmp_path / "calls.log"
    for tool in ("sed", "tr"):
        real = shutil.which(tool)
        (bindir / tool).unlink()
        (bindir / tool).write_text(
            f'#!{BASH}\nprintf "%s\\n" {tool} >>"{log}"\nexec "{real}" "$@"\n'
        )
        (bindir / tool).chmod(0o755)
    return log


EDIT_TOOLS = [
    ("Edit", {"file_path": "/x//./settings.json"}),
    ("Write", {"file_path": "/x/a.txt", "content": "y"}),
    ("NotebookEdit", {"notebook_path": "/x/n.ipynb", "new_source": "y"}),
]


@pytest.mark.parametrize(
    "tool_name, tool_input, counts",
    [
        ("Bash", {"command": "git status | tail -5"}, (1, 4)),
        ("Bash", {"command": "ls", "run_in_background": True}, (1, 4)),
        ("Monitor", {"command": "tail -f log", "timeout_ms": 1000}, (1, 4)),
        *[(name, ti, (1, 0)) for name, ti in EDIT_TOOLS],
        ("Skill", {"skill": "sc:workflow"}, (0, 0)),
    ],
)
def test_nrm_one_sed_four_tr(tmp_path, tool_name, tool_input, counts):
    log = _counting_bin(tmp_path)
    _bind(tmp_path, "full")
    payload = {
        "hook_event_name": "PreToolUse",
        "session_id": SID,
        "tool_name": tool_name,
        "tool_input": tool_input,
    }
    result = _run(payload, tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    calls = log.read_text().split() if log.exists() else []
    assert (calls.count("sed"), calls.count("tr")) == counts


@pytest.mark.parametrize(
    "path, want",
    [
        ("/x//./settings.json", "/x/settings.json"),
        ("~/.claude///hooks/././guard.sh", "~/.claude/hooks/guard.sh"),
        ("a/b", "a/b"),
    ],
)
def test_nrm_edit_path_squeeze(tmp_path, path, want):
    lines = [
        line.strip()
        for line in HOOK.read_text().splitlines()
        if line.strip().startswith("EPATH=$(")
    ]
    assert len(lines) == 1
    driver = f'LC_ALL=C; ll_deny() {{ exit 3; }}; LL_PATH=$1\n{lines[0]}\nprintf %s "$EPATH"\n'
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    result = subprocess.run(
        [BASH, "-c", driver, "_", path],
        capture_output=True,
        env=_env(home, _bin(tmp_path)),
        timeout=10,
    )
    assert (result.returncode, result.stdout.decode()) == (0, want)


# --- Task 7: git classification and the canonical push check (T-GIT, T-PSH) ---
#
# Every expected tuple below is written by hand from the grid of MR section 8.1
# (W, WA, F, FS); none is derived from the script's case statements. A Bash
# block always carries the LL-TEXT note.

PUSH_OK = ("LL-PUSH", "LL-PUSH", "LL-PUSH", None)  # class PUSH only
PUSHFORM = ("LL-PUSH", "LL-PUSH", "LL-PUSH", "LL-PUSH-FORM")  # PUSH and PUSHFORM
PROTECTED = ("LL-PROTECTED",) * 4
MULTILINE = "git commit -m \"$(cat <<'EOF'\nfeat: x\n{line}\nEOF\n)\""

# Grid rows 12 to 18 and 30 to 33 of MR section 8.1, git parts only (gh and
# curl parts are in GH_ORACLE below; MCP belongs to Task 10). They cover T-GIT-2, 5, 6, 10, 11, 16 and
# T-PSH-2, 3, 5 and 7.
GIT_ORACLE = {
    "NONE": (
        NONE4,
        [
            "git status",
            "git diff",
            "git log --oneline",
            "git add -A",
            "git stash",
            "git rebase origin/master",
            "git fetch origin",
            "git remote get-url origin",
            "git merge-tree a b",
            "git update-ref refs/superclaude/implement/p/T1 abc123",
            "git -C /x status",
            "NAME=x git status",
            "git --attr-source HEAD status",
            "git status 2>&1 | tail -5",
            'git -C "$(git rev-parse --show-toplevel)" status',
            # Row 30: text that names git without a gated word.
            'echo "use git for hooks"',
            'grep -rn "git worktree" docs/',
            "cd git-tools",
            "grep -rn push docs/",
            # Row 33: the pinned gaps of residual R1 (git parts).
            "G=gi; ${G}t push origin main",
            "$'\\x67it' push origin main",
            "$GIT push origin main",
            "/usr/bin/gi[t] push origin main",
        ],
    ),
    "COMMIT": (
        ("LL-COMMIT", "LL-COMMIT", "LL-COMMIT", None),
        [
            "git commit -m x",
            "git commit --only -- a b",
            "git cherry-pick x",
            "git revert x",
            "git am p.patch",
            "git commit-tree t",
            "git update-ref refs/heads/f abc123",
            "git update-ref HEAD abc123",
            "sudo git commit -m x",
            'sh -c "git commit -m x"',
            "git bisect run git commit",
            'A=">" git commit -m x',
            "git$'' commit --allow-empty -m x",
            'echo "git commit"',
            'git status && echo "I am done"',
            MULTILINE.format(line="use git for hooks"),
        ],
    ),
    "PUSH": (
        PUSH_OK,
        [
            "git push origin 3f2a9c1e:feature",
            "git push -u origin feature:feature",
            "git push origin feature",
            "git push --set-upstream origin feature",
        ],
    ),
    "PUSHFORM": (
        PUSHFORM,
        [
            "git push",
            "git push origin",
            "git push origin HEAD",
            "git push origin x:@",
            "git push upstream a:b",
            "git push --repo=x a:b",
            "git push origin a:$B",
            "git push origin a:b 2>&1",
            "git push origin f 2>&1 | tail -5",
            "cd x && git push origin a:b",
            "git push origin a:b `echo c:main`",
            "git push origin a:b \\\nc:main",
            "git-push origin feature",
            "/usr/lib/git-core/git-push origin main",
            "git push --force origin f",
            "git push origin +f:f",
            "git push --all",
            "git push --mirror",
            "git push --receive-pack=x origin a:b",
            "git push --exec=x origin a:b",
            "git push origin --all",
            "git push origin --mirror",
            "git push origin -f",
            "git push origin x:--all",
            "git --attr-source HEAD push origin main",
            "echo f:main | xargs git push origin f:f",
            'A=">" git push origin HEAD:main',
            'git -c "x.y=a status" push origin HEAD:main',
            'git rebase -x "git push origin main" main',
            "git commit -m x && git push origin f",
            "timeout 30 git push origin main",
            "GIT=git; $GIT push origin main",
            "$'git' push origin main",
            "git$'' push origin HEAD:main",
            'g$""it push origin HEAD:main',
            "timeout -s KILL 30 git send-pack /tmp/r.git HEAD:refs/heads/main",
            "taskset -c 0 git send-pack /tmp/r.git HEAD:refs/heads/main",
            "find . -maxdepth 0 -exec git send-pack /tmp/r.git HEAD:refs/heads/main \\;",
            "git rebase -x 'git send-pack /tmp/r.git HEAD:refs/heads/main' HEAD~1",
            # Row 32: pinned G1 over-match on text.
            'git commit -m "explain git push"',
            MULTILINE.format(line="git push origin main is never run"),
            "git log --grep push",
            "git log --oneline | grep push",
        ],
    ),
    "PROTECTED": (
        PROTECTED,
        [
            "git push origin main",
            "git push origin x:main",
            "git push origin x:refs/heads/master",
            "git push origin x:heads/main",
            "git push -u origin feature:main",
        ],
    ),
    "MERGE": (
        MERGE,
        [
            "git merge x",
            "git merge --abort",
            "git pull",
            "git pull --rebase",
            "git -c merge.conflictStyle=zdiff3 merge --no-commit --no-ff abc123",
            "git-merge x",
            "git$'' merge other --no-edit",
            "git log --grep merge",  # row 32a
        ],
    ),
    "UNKNOWN": (
        UNK,
        [
            "git ci",
            "git -c alias.ci=commit ci",
            "X=commit git --config-env=alias.ci=X ci",
            "git rebase -x 'git -c alias.p=push p origin HEAD:main' HEAD~1",
            "Q=sh git rebase -x 'git pu$Q origin HEAD:main' HEAD~1",
            "git rebase -x 'git `echo pu`sh origin HEAD:main' HEAD~1",
            "git $(echo push) origin a:b",
            "cmd=push; git $cmd",
            "printf x | xargs git",
            "git notes add",
            "git worktree add",
            "git remote set-url origin u",
            "git config alias.ci commit",
            'git -C "/dir with space" push',
            "git-lfs push",
            "$(git --exec-path)/git-push origin main",
            "gi\\\nt push origin HEAD:main",
            "if true; then git send-pack /tmp/r.git HEAD:refs/heads/main; fi",
            "env -u FOO git config remote.origin.push refs/heads/feature:refs/heads/main",
            "flock /tmp/l git config remote.origin.push refs/heads/feature:refs/heads/main",
            "sudo -u coder git remote set-url --push origin https://github.com/evil/x",
            # Row 31: pinned over-match in command position.
            MULTILINE.format(line="git hooks run on save"),
            "git \\\ncommit -m x",
            "git config --get-regexp alias.",
        ],
    ),
}


def _git_params(prefix: str, rows):
    for i, (command, ids) in enumerate(rows):
        for level, msg_id in zip(LEVEL_ORDER, ids):
            yield pytest.param(command, level, msg_id, id=f"{prefix}{i}-{level}")


def _git_case(tmp_path, command, level, msg_id):
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(_bash(command), tmp_path)
    _assert_decision(result, tmp_path, msg_id, level, text=msg_id is not None)


@pytest.mark.parametrize(
    "command, level, msg_id",
    [
        p
        for cls, (ids, commands) in GIT_ORACLE.items()
        for p in _git_params(f"{cls}-", [(c, ids) for c in commands])
    ],
)
def test_git_grid_oracle(tmp_path, command, level, msg_id):
    _git_case(tmp_path, command, level, msg_id)


@pytest.mark.parametrize("level", LEVEL_ORDER)
@pytest.mark.parametrize(
    "command",
    [
        "/usr/bin/env git ci",
        "/usr/bin/sudo git worktree add x",
        '/bin/bash -c "git ci"',
        "/usr/bin/timeout 30 git notes add",
        "env git ci",
    ],
    ids=["env", "sudo", "bash-c", "timeout", "bare-env"],
)
def test_git_wrapper_matched_by_basename(tmp_path, level, command):
    # NM7 / G3: a path-qualified wrapper or shell is still a wrapper, so the git
    # word after it is in command position and its UNKNOWN-class subcommand blocks.
    _git_case(tmp_path, command, level, "LL-UNKNOWN")


# T-GIT-1, 3, 7, 8, 9, 12, 13, 14, 15 and 18: the cases the oracle rows above do
# not already hold.
GIT_NAMED = [
    # T-GIT-1: read or local git commands of /sc:implement and /sc:pr-submit.
    *[
        (c, NONE4)
        for c in (
            "git rev-parse HEAD",
            "git rev-parse --show-toplevel",
            "git show --stat HEAD",
            "git branch --show-current",
            "git diff --cached --name-only",
            "git status --porcelain",
            "git log -1 --format=%H",
            "git rev-list --count origin/master..HEAD",
            "git merge-base HEAD origin/master",
            "git worktree list",
            "git config --get user.name",
            "git remote -v",
            "git ls-files -m",
            "git restore --staged a",
            "git checkout -- a",
            "git reset --hard HEAD",
            "git cat-file -t HEAD",
            "git fetch origin master",
        )
    ],
    # T-GIT-3: the three alias forms of fact T2.
    (
        "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=alias.ci GIT_CONFIG_VALUE_0=commit git ci",
        UNK,
    ),
    # T-GIT-7: update-ref.
    ('git update-ref "$ref" "$sha"', NONE4),
    ("git update-ref refs/heads/x abc123", COMMIT),
    ("git update-ref --stdin", COMMIT),
    # T-GIT-8: nested git words.
    ('git commit -m "fix git handling"', COMMIT),
    # T-GIT-9: wrappers; a wrapped commit is COMMIT, a wrapped push PUSHFORM.
    *[
        (w.format(c="git commit -m x"), COMMIT)
        for w in (
            'bash -c "{c}"',
            'sh -c "{c}"',
            "env {c}",
            "command {c}",
            "exec {c}",
            "sudo {c}",
            "nohup {c}",
            "timeout 30 {c}",
            "xargs {c}",
            "/usr/bin/{c}",
            "NAME=x {c}",
        )
    ],
    ("git -C /x commit -m x", COMMIT),
    *[
        (w.format(c="git push origin main"), PUSHFORM)
        for w in (
            'bash -c "{c}"',
            'sh -c "{c}"',
            "env {c}",
            "command {c}",
            "exec {c}",
            "sudo {c}",
            "nohup {c}",
            "xargs {c}",
            "/usr/bin/{c}",
            "NAME=x {c}",
        )
    ],
    ("git -C /x push origin main", PUSHFORM),
    ("python -c \"subprocess.run(['git','push','origin','main'])\"", PUSHFORM),
    # T-GIT-12: dashed builtins.
    ("git-commit -m x", COMMIT),
    ("cat docs/git-workflow.md", NONE4),
    # T-GIT-13: the message text passed by file.
    ("git commit -F msg.txt", COMMIT),
    # T-GIT-14: T-ATK-11, 12, 34 (10, 35 and 36 are oracle rows).
    ("git status \\\\\ngit -c alias.p=push p origin HEAD:main", UNK),
    ("git bisect run git -c alias.c=commit c", UNK),
    ("X=sh git rebase -x 'git -c alias.p=pu$X p origin HEAD:main' HEAD~1", UNK),
    # T-GIT-15.
    ("git -C 'a b' push origin HEAD:main", UNK),
    # T-GIT-18: N-ATK-8 (5, 6, 9 to 13 and 37 are oracle rows).
    (
        "if true; then git config remote.origin.push"
        " refs/heads/feature:refs/heads/main; fi",
        UNK,
    ),
    ("flock /tmp/l git send-pack /tmp/r.git HEAD:refs/heads/main", PUSHFORM),
]


@pytest.mark.parametrize("command, level, msg_id", list(_git_params("g", GIT_NAMED)))
def test_git_named_cases(tmp_path, command, level, msg_id):
    _git_case(tmp_path, command, level, msg_id)


def test_git_alias_cannot_shadow_builtin(tmp_path):
    # T-GIT-4: the hook calls the command UNKNOWN, and real git runs status, not commit.
    git = shutil.which("git")
    if git is None:
        pytest.skip("git is not installed")
    repo = tmp_path / "repo"
    repo.mkdir()
    env = {
        "HOME": str(tmp_path),
        "PATH": os.environ.get("PATH", ""),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
    }

    def run(*args):
        return subprocess.run(
            [git, "-c", "user.name=t", "-c", "user.email=t@t", *args],
            cwd=repo,
            env=env,
            capture_output=True,
            timeout=30,
        )

    assert run("init", "-q").returncode == 0
    (repo / "a").write_text("x")
    assert run("add", "a").returncode == 0
    assert run("-c", "alias.status=commit", "status").returncode == 0
    assert run("rev-parse", "--verify", "-q", "HEAD").returncode != 0
    command = "git -c alias.status=commit status"
    for level in LEVEL_ORDER:
        _git_case(tmp_path / level, command, level, "LL-UNKNOWN")


def _retry_block() -> str:
    # Extracted as tests/skills/test_implement_retry_revert.py extracts it.
    text = (
        ROOT / "src/superclaude/skills/sc-implement-protocol/refs/retry.md"
    ).read_text()
    blocks = re.findall(r"```bash\n(.*?)```", text, re.S)
    return next(b for b in blocks if "sc_retry_revert()" in b)


@pytest.mark.parametrize("level", ["WA", "F"])
@pytest.mark.parametrize(
    "command",
    [
        "retry",
        'git update-ref "refs/superclaude/implement/p/T1" "$start"',
        'idx=$(mktemp); GIT_INDEX_FILE="$idx" git read-tree HEAD && '
        'GIT_INDEX_FILE="$idx" git add -A && '
        'start=$(GIT_INDEX_FILE="$idx" git write-tree); rm -f "$idx"',
        'git -C "$(git rev-parse --show-toplevel)" status',
    ],
    ids=["retry-block", "T-OK-21", "T-OK-22", "toplevel"],
)
def test_implement_git_blocks_allowed(tmp_path, command, level):
    # T-GIT-17 [B-10].
    if command == "retry":
        command = _retry_block()
    _git_case(tmp_path, command, level, None)


# T-PSH-11 and T-PSH-12: the named push cases of FR-L-33 and FR-L-34.
PUSH_ACCEPT = [
    "git push origin feature",
    "git push -u origin feature",
    "git push --set-upstream origin feature",
    "git push origin 3f2a9c1e:feature/x",
    "git push origin feature:feature",
    "git push origin feature/main:feature/main",
    "git push origin HEAD:feature",
    "git push origin fix-394.v2",
    "  git push origin feature  ",
    "git push origin a:refs/heads/feature",
    "git push origin release_1.2",
    "git push origin feature\n",
    "git push origin refs/heads/heads/main",
]
PUSH_REJECT = [
    "git push origin a:b `echo c:main`",
    "git push origin a:b \\\n c:main",
    "git-push origin main",
    "/usr/lib/git-core/git-push origin feature",
    "git push origin +feature:feature",
    "git push --force origin feature",
    "git push --all origin",
    "git -c remote.origin.push=refs/heads/f:refs/heads/main push origin f",
    "git --config-env=remote.origin.push=V push origin f",
    "git push origin 'feature:ma''in'",
    "git push origin a:$(echo main)",
    "git push origin a:$B",
    "git push upstream feature",
    "git push origin a:b 2>&1",
    "cd x && git push origin a:b",
    "git push origin a:b; git push origin c:main",
    "git push origin :feature",
    "git push origin a:b c:main",
    "GIT_CONFIG_COUNT=1 git push origin f",
    "git push origin a:b\ngit push origin c:main",
    "git  push origin feature",
    "echo feat:main | xargs git push origin feat:feat",
    "git push origin HEAD",
    "git push origin --all",
    "git push origin --mirror",
    "git push origin -f",
    "git push origin x:--all",
    "git push origin --delete",
    "git push origin ..",
    "git push origin x:@",
]
PUSH_PROTECTED = [
    "git push origin main",
    "git push origin x:refs/heads/master",
    "git push origin x:heads/main",
    "git push origin heads/main",
    "git push -u origin feature:main",
]
# T-PSH-4, 6, 8 (Bash parts; the Write is in TAMPER_EDITS) and 10.
PUSH_NAMED = [
    ("git push origin +main", PUSHFORM),
    ("git push origin :main", PUSHFORM),
    ("git push -o ci.skip origin a:b", PUSHFORM),
    (
        "git -c remote.origin.push=refs/heads/feature:refs/heads/main"
        " push origin feature",
        UNK,
    ),
    ("git config remote.origin.push x", UNK),
    ("git push --force-with-lease origin a:b", PUSHFORM),
    ("git push -f origin a:b", PUSHFORM),
    ("git push origin +a:b", PUSHFORM),
]


@pytest.mark.parametrize(
    "command, level, msg_id",
    [
        *_git_params("PA", [(c, PUSH_OK) for c in PUSH_ACCEPT]),
        *_git_params("PD", [(c, PROTECTED) for c in PUSH_PROTECTED]),
        *_git_params("PSH", PUSH_NAMED),
    ],
)
def test_push_named_cases(tmp_path, command, level, msg_id):
    _git_case(tmp_path, command, level, msg_id)


@pytest.mark.parametrize("level", LEVEL_ORDER)
@pytest.mark.parametrize(
    "command", PUSH_REJECT, ids=[f"PR{i}" for i in range(1, len(PUSH_REJECT) + 1)]
)
def test_push_form_reject_cases(tmp_path, command, level):
    # T-PSH-12: LL-PUSH-FORM or LL-UNKNOWN at FS, LL-PUSH or LL-UNKNOWN below.
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(_bash(command), tmp_path)
    store = str(_store(tmp_path / "home"))
    note = _design_note("LL-TEXT") + "\n"
    ids = ("LL-PUSH-FORM" if level == "FS" else "LL-PUSH", "LL-UNKNOWN")
    assert (result.returncode, result.stdout) == (2, b"")
    assert result.stderr.decode() in {
        _expected(i, LEVELS[level], SID, store) + note for i in ids
    }


# --- Task 8: gh, curl and API text (H1 to H5; FR-L-35 to FR-L-39) -----------
#
# Each tuple below is written by hand from the grid (design section 8; MR
# section 8.1 rows 18 to 22), not taken from the script's case statement.

SUBMIT = ("LL-SUBMIT", "LL-SUBMIT", "LL-SUBMIT", None)
SUBMIT_REPO = ("LL-SUBMIT", "LL-SUBMIT", "LL-SUBMIT", "LL-REPO")
REPO_FLAG = '--repo "$REPO"'

GH_ORACLE = {
    "NONE": (
        NONE4,
        [
            # Row 19 and the FR-L-36 consequences.
            "gh pr view 5 --json mergeable,mergeStateStatus",
            "gh issue view 5",
            "gh pr checks 5",
            "gh pr checks",
            "gh repo view",
            "gh pr view 5",
            "gh api repos/o/r/pulls/5",
            "gh api repos/o/r/pulls/5 --jq .state",
            "gh api repos/o/r/commits/abc123/check-runs --jq .total_count",
            "gh api repos/o/r/pulls -H Accept:application/json --paginate -i --silent -q .total_count",
            "gh api --hostname github.com repos/o/r/pulls",
            "gh --version",
            "gh --help",
            "gh auth status",
            "gh -R o/r pr list",
            'echo "use gh to view"',
            # Residual R17 (N-ATK-36): a gh word out of command position.
            "flock /tmp/l gh mm 5",
        ],
    ),
    "SUBMIT": (
        SUBMIT,
        [
            # Row 20 and row 21.
            "gh issue create",
            "gh issue comment 5",
            "gh issue edit 5",
            "gh pr comment 5",
            "gh pr edit 5",
            "gh pr ready 5",
            f"gh pr create {REPO_FLAG} --base master --head f",
            "gh pr create -R o/r --title x",
            "gh pr create --repo=o/r --title x",
            "gh pr create --repo o/r --title x",
            "gh -R o/r pr create --title x",
            f'gh pr create {REPO_FLAG} --base master --head f --title "docs: explain git hooks" --body "x"',
        ],
    ),
    "REPO": (
        SUBMIT_REPO,
        [
            # Row 22 and the H4 operand rules.
            "gh pr create --title x",
            "gh pr create --repo --title x",
            "gh pr create --repo= --title x",
            "gh pr create -R -t x",
            "gh issue view 5; gh pr create --title x",
            # The operand of another segment does not count (design H4).
            "gh pr create --title x; gh pr list --repo o/r",
            'gh pr create \\\n--repo "$REPO" --title x --body y',
        ],
    ),
    "GHWRITE": (
        GHWRITE,
        [
            "gh api -X POST repos/o/r/merges",
            "gh api graphql",
            "gh api graphql -f query={viewer{login}}",
            "gh api graphql -f 'query=query { viewer { login } }'",
            "gh api repos/o/r/pulls/5/merge",
            "gh api repos/o/r/merges",
            "gh api --method GET repos/o/r/pulls",
            "gh api",
            "gh api -q .x",
            'gh api "repos/$REPO/pulls"',
            "gh api repos/o/r/pulls | jq .",
            "curl -X PATCH https://api.github.com/repos/o/r",
            "curl -sS https://api.github.com/repos/o/r/pulls",
            "wget https://uploads.github.com/repos/o/r/releases/1/assets",
            # O-21: the word api in a gh command's text.
            'gh pr create --repo o/r --title "fix api docs"',
        ],
    ),
    "MERGE": (
        MERGE,
        [
            "gh pr merge 5",
            "gh pr update-branch 5",
            "gh repo sync",
            "gh -R o/r pr merge 5 --squash",
            "/usr/bin/gh pr merge 5",
            "echo gh pr merge 5",
            "curl -X PUT https://api.github.com/repos/o/r/pulls/5/merge",
            "curl -X POST https://api.github.com/repos/o/r/merges",
            "wget --method=PUT example.test/repos/o/r/pulls/5/merge",
        ],
    ),
    "UNKNOWN": (
        UNK,
        [
            "gh alias set co 'pr merge'",
            "gh co 5",
            "gh extension install x",
            "gh pr $(echo merge) 5",
            "gh pr `echo merge` 5",
            "gh pr close 5",
            "gh repo delete o/r",
            "gh release create v1",
            "gh",
            "gh pr create -R",
            "echo gh alias list",
        ],
    ),
}


def _gh_params(prefix: str, rows):
    for i, (command, ids) in enumerate(rows):
        for level, msg_id in zip(LEVEL_ORDER, ids):
            yield pytest.param(command, level, msg_id, id=f"gh-{prefix}{i}-{level}")


@pytest.mark.parametrize(
    "command, level, msg_id",
    [
        p
        for cls, (ids, commands) in GH_ORACLE.items()
        for p in _gh_params(f"{cls}-", [(c, ids) for c in commands])
    ],
)
def test_gh_grid_oracle(tmp_path, command, level, msg_id):
    _git_case(tmp_path, command, level, msg_id)


# The T-GH cases of MR section 8.2, by their MR test names.
GH_NAMED = {
    # T-GH-1
    "test_gh_pr_merge_every_level": [
        (c, MERGE) for c in ("gh pr merge 5", "gh pr update-branch 5", "gh repo sync")
    ],
    # T-GH-2
    "test_gh_api_merge_and_ref_writes": [
        (c, GHWRITE)
        for c in (
            "gh api -X POST repos/o/r/merges -f base=main -f head=f",
            "gh api graphql -f query='mutation { mergePullRequest(input: {pullRequestId: \"x\"}) { clientMutationId } }'",
            "gh api graphql -f query='mutation { enablePullRequestAutoMerge(input: {pullRequestId: \"x\"}) { clientMutationId } }'",
            "gh api -X PATCH repos/o/r/git/refs/heads/main -f sha=abc -F force=true",
            "gh api -X PUT repos/o/r/contents/x -f message=m -f content=Yg== -f branch=main",
        )
    ],
    # T-GH-3
    "test_gh_pr_create_without_repo": [("gh pr create --title x", SUBMIT_REPO)],
    # T-GH-4
    "test_gh_pr_create_repo_forms": [
        (c, SUBMIT)
        for c in (
            f"gh pr create {REPO_FLAG} --title x",
            "gh pr create -R o/r --title x",
            "gh pr create --repo=o/r --title x",
        )
    ],
    # T-GH-5 (row 20)
    "test_gh_writes_need_submit": [
        (c, SUBMIT)
        for c in (
            "gh issue create",
            "gh issue comment 5",
            "gh pr comment 5",
            "gh pr edit 5",
            "gh pr ready 5",
        )
    ],
    # T-GH-6 (O-3)
    "test_gh_pr_ready_submit_class": [("gh pr ready 5", SUBMIT)],
    # T-GH-7 (row 19)
    "test_gh_reads_every_level": [
        (c, NONE4)
        for c in (
            "gh pr view 5 --json mergeable,mergeStateStatus",
            "gh issue view 5",
            "gh pr checks 5",
            "gh repo view",
            "gh api repos/o/r/pulls/5",
            "gh api repos/o/r/commits/abc123/check-runs --jq .total_count",
        )
    ],
    # T-GH-8
    "test_merge_url_suffix": [
        ("curl -X PUT https://api.github.com/repos/o/r/pulls/5/merge", MERGE),
        ("curl -X POST https://api.github.com/repos/o/r/merges", MERGE),
        ("gh api repos/o/r/pulls/5/merge", GHWRITE),
    ],
    # T-GH-9
    "test_gh_unknown_group_or_action": [
        (c, UNK)
        for c in (
            "gh alias set co 'pr merge'",
            "gh co 5",
            "gh extension install x",
            "gh pr $(echo merge) 5",
            "gh pr `echo merge` 5",
            "gh pr close 5",
        )
    ],
    # T-GH-10: every GHWRITE flag word and endpoint of FR-L-36; one allowed read.
    "test_gh_api_get_only": [
        *[
            (f"gh api repos/o/r/pulls {flag}", GHWRITE)
            for flag in (
                "-XPOST",
                "-X",
                "-iXPOST",
                "--method=POST",
                "--method",
                "--raw-field=x=y",
                "--raw-field",
                "-f",
                "-F",
                "-Fbody=x",
                "-fa=b",
                "--field",
                "--field=a=b",
                "--input",
                "--input=f",
            )
        ],
        *[
            (f"gh api {endpoint}", GHWRITE)
            for endpoint in ("graphql", "repos/o/r/pulls/5/merge", "repos/o/r/merges")
        ],
        ("gh api repos/o/r/pulls", NONE4),
        ("gh api repos/o/r/pulls/5", NONE4),
        (
            "gh api repos/o/r/pulls -H Accept:application/json --paginate -i --silent -q .total_count",
            NONE4,
        ),
        ("gh api repos/o/r/pulls --hostname github.com -t {{.x}}", GHWRITE),
        ("gh api repos/o/r/pulls --hostname github.com -t .x", NONE4),
    ],
    # T-GH-11: T-ATK-18, 19, 20, 31, 56 and a variable endpoint.
    "test_gh_api_shell_built_flag": [
        *[
            (c, GHWRITE)
            for c in (
                "X=X; gh api repos/o/r/git/refs/heads/main -$X DELETE",
                "gh api repos/o/r/git/refs/heads/main `echo -e '\\055X'` DELETE",
                "gh api repos/o/r/git/refs/heads/main {-X,DELETE}",
                'gh api repos/o/r/git/refs/heads/main --jq ".a >" -X DELETE',
                "gh api repos/o/r/git/refs/heads/main -X\\\nDELETE",
                'gh api "repos/$REPO/pulls"',
            )
        ],
        ("gh api repos/o/r/commits/abc123/check-runs --jq .total_count", NONE4),
    ],
    # T-GH-12
    "test_gh_text_rules": [
        (
            f'gh pr create {REPO_FLAG} --base master --head f --title "docs: explain git hooks" --body "x"',
            SUBMIT,
        ),
        ('gh pr create --repo o/r --title "fix api docs"', GHWRITE),
        ('echo "use gh to view"', NONE4),
    ],
    # T-GH-13: N-ATK-20, 21, 22 and 35 (B-3), and N-ATK-36 (residual R17).
    "test_gh_anywhere_rules": [
        ("X=ge; flock /tmp/l gh pr mer$X 5", UNK),
        ("if :; then gh repo sync; fi", MERGE),
        ("if :; then gh pr update-branch 5; fi", MERGE),
        ("if :; then gh alias set mm 'pr merge'; fi", UNK),
        ("flock /tmp/l gh mm 5", NONE4),
    ],
    # T-GH-14: N-ATK-26 (B-7).
    "test_direct_github_api_blocked": [
        (
            'curl -sS -X PATCH -H "Authorization: token $(gh auth token)" '
            "https://api.github.com/repos/o/r/git/refs/heads/main "
            '-d \'{"sha":"abc","force":true}\'',
            GHWRITE,
        ),
    ],
}


@pytest.mark.parametrize(
    "command, level, msg_id",
    [
        p
        for name, rows in GH_NAMED.items()
        for p in _gh_params(f"{name.removeprefix('test_')}-", rows)
    ],
)
def test_gh_named_cases(tmp_path, command, level, msg_id):
    _git_case(tmp_path, command, level, msg_id)


# Task 8 acceptance criteria, as written in the plan.
GH_ACCEPTANCE = [
    ("gh api repos/o/r/pulls/5 --jq .state", NONE4),
    ("gh api -X POST repos/o/r/merges", GHWRITE),
    ("gh api graphql -f query='{ viewer { login } }'", GHWRITE),
    ("gh api graphql", GHWRITE),
    ("curl -X PATCH https://api.github.com/repos/o/r", GHWRITE),
    ("gh pr create --repo o/r --title x", SUBMIT),
    ("gh pr create --title x", SUBMIT_REPO),
    ("gh pr merge 5", MERGE),
    ("gh repo sync", MERGE),
    ("gh pr view 5", NONE4),
    ("gh pr checks", NONE4),
    ("gh alias set co 'pr merge'", UNK),
]


@pytest.mark.parametrize(
    "command, level, msg_id", list(_gh_params("acc-", GH_ACCEPTANCE))
)
def test_gh_task8_acceptance(tmp_path, command, level, msg_id):
    _git_case(tmp_path, command, level, msg_id)


@pytest.mark.parametrize("tool", ["Bash", "Monitor"])
def test_gh_class_from_text_prints_text_note(tmp_path, tool):
    # A gh class from Bash or Monitor text carries the LL-TEXT note.
    _bind(tmp_path, *LEVEL_FILES["FS"])
    result = _run(_bash("gh pr merge 5", tool=tool), tmp_path)
    _assert_decision(result, tmp_path, "LL-MERGE", "FS", text=True)


# --- Task 9: tamper and escape (T-TAM, T-ESC) -------------------------------
#
# Hand-written oracle for the TAMPER and ESCAPE grid rows (MR 8.1 rows 25 to
# 27, design section 8): both classes block at every level. It is written out
# per level rather than derived from the script's case statement.
TAMPER_ESCAPE_ORACLE = {
    "TAMPER": {
        "W": "LL-TAMPER",
        "WA": "LL-TAMPER",
        "F": "LL-TAMPER",
        "FS": "LL-TAMPER",
    },
    "ESCAPE": {
        "W": "LL-ESCAPE",
        "WA": "LL-ESCAPE",
        "F": "LL-ESCAPE",
        "FS": "LL-ESCAPE",
    },
    "NONE": {"W": None, "WA": None, "F": None, "FS": None},
}
HOME_U = "/home/u"
STATE_ABS = STATE_PATH.replace("~", HOME_U)

# T-TAM-1, T-TAM-5, T-TAM-6: MR row 27 and the reinstall forms.
TAMPER_BASH = [
    f"cat {STATE_PATH}/launch-level/sessions/x",
    f"rm -rf {STATE_PATH}/launch-level",
    f"rm -rf {STATE_PATH}",
    f"cd {STATE_PATH} && rm -rf launch-level",
    f"find {STATE_ABS} -delete",
    f"mv {STATE_PATH} ~/.claude/s2",
    "cd ~/.claude && rm -rf state",
    "cd ~/.claude/ && rm -rf state",
    "echo '{\"disableAllHooks\":true}' > ~/.claude/settings.json",
    "cd ~/.claude && : > hooks/x.sh",
    "cd ~/.claude && : > hooks/launch-level-guard.sh",
    "cat ~/.gitconfig",
    "cat .git/config",
    "cat ~/.config/git/config",
    "rm -rf ~/.cla$''ude/state",
    "cp /tmp/s.json ~/.claude/set$''tings.json",
    ": > ~/.claude/hoo$''ks/launch-level-guard.sh",
    "uv run superclaude install",
    'uv run python -c "import superclaude.cli.install_hooks"',
    "uv run python -m superclaude.cli.main install",
    "~/.local/bin/superclaude install",
    "ls; uv run superclaude install --force",
    # Codex finding 4503606823: dot segments reach the store without naming it.
    "cd ~/.claude/. && mv state state.old",
    "cd ~/.claude/./ && rm -r state",
    "cd ~/.claude//. && rm -r state",
    "cd ~/.claude/x/.. && rm -r state",
    "cd ~/.claude/.. && ls",
    "ls ~/.claude/.",
]
# T-ESC-1, T-ESC-2, T-ESC-5, T-ESC-6: MR row 25 and the T-ESC forms.
ESCAPE_BASH = [
    "claude -p x",
    "/usr/local/bin/claude --print x",
    "npx @anthropic-ai/claude-code -p x",
    "npx -y @anthropic-ai/claude-code@latest -p x",
    'npx -y @anthropic-ai/claude-code@latest -p "finish the task"',
    "claude --resume abc",
    "claude --dangerously-skip-permissions",
    "ls && claude --continue",
    "orca agent launch --name w",
    "orca agent launch --name -h x",
    "orca terminal send",
    "orca terminal send --text approved",
    "orca computer type-text approved",
    "orca automations run x",
    "orca orchestration send x",
    "orca orchestration dispatch x",
    "orca worktree create --name x",
    "ls; orca agent launch",
    "tmux send-keys approved Enter",
    "tmux new-session -d 'claude \"x\"'",
    "screen -X stuff x",
    "xdotool type approved",
    "ydotool type x",
    "ccsession",
    "ccsession-orca 'x'",
    "/usr/local/bin/ccsession -h",
]
# T-TAM-4, MR row 26 and the orca allowlist pairs of T-ESC-2.
NONE_BASH = [
    "ls",
    "cat src/superclaude/hooks/scripts/launch-level-guard.sh",
    "cat docs/hook-launch-level-394.md",
    "uv run superclaude doctor",
    "grep -rn claude docs/",
    "grep claude -rn docs/",
    "which claude",
    "claude --version",
    "orca status",
    "orca status --json",
    "orca help",
    "orca --version",
    "orca worktree current",
    "orca worktree current --json",
    "orca worktree list",
    "orca worktree show x",
    "orca terminal list",
    "orca terminal show t1",
    "orca terminal read t1",
    "orca orchestration check",
    "orca orchestration inbox",
    "orca orchestration run-current",
    "orca orchestration task-list",
    "orca orchestration worker-show w1",
    "orca list --help",
    "orca agent launch -h",
    "ls ~/.claude/.cache",
    "ls ~/.claude/skills",
]


def _oracle_params(prefix: str, rows):
    for i, (payload, cls) in enumerate(rows):
        for level in LEVEL_ORDER:
            msg_id = TAMPER_ESCAPE_ORACLE[cls][level]
            yield pytest.param(payload, level, msg_id, id=f"{prefix}{i}-{level}")


def _edit(tool: str, path: str, **extra) -> dict:
    key = "notebook_path" if tool == "NotebookEdit" else "file_path"
    return {
        "hook_event_name": "PreToolUse",
        "session_id": SID,
        "tool_name": tool,
        "tool_input": {key: path, **extra},
    }


@pytest.mark.parametrize(
    "command, level, msg_id",
    [
        *_oracle_params("TAM", [(c, "TAMPER") for c in TAMPER_BASH]),
        *_oracle_params("ESC", [(c, "ESCAPE") for c in ESCAPE_BASH]),
        *_oracle_params("NONE", [(c, "NONE") for c in NONE_BASH]),
    ],
)
def test_tamper_escape_bash_oracle(tmp_path, command, level, msg_id):
    _git_case(tmp_path, command, level, msg_id)


@pytest.mark.parametrize("tool", ["Bash", "Monitor"])
@pytest.mark.parametrize(
    "command, msg_id",
    [("rm -rf " + STATE_PATH, "LL-TAMPER"), ("claude -p x", "LL-ESCAPE")],
)
def test_tamper_escape_from_monitor_text(tmp_path, tool, command, msg_id):
    _bind(tmp_path, *LEVEL_FILES["W"])
    result = _run(_bash(command, tool=tool), tmp_path)
    _assert_decision(result, tmp_path, msg_id, "W", text=True)


# T-TAM-2: each token path, a "//" path, a "/./" path and a ".." path, and
# [B-4] a Write of ~/.config/git/config (also the Write of T-PSH-8).
TAMPER_PATHS = [
    STATE_ABS + "/launch-level/sessions/x",
    "~/.claude/settings.json",
    HOME_U + "/.claude/settings.local.json",
    HOME_U + "/.claude/hooks/launch-level-guard.sh",
    HOME_U + "/notes/disableAllHooks.txt",
    HOME_U + "/.gitconfig",
    "/r/.git/config",
    "~/.config/git/config",
    HOME_U + "/.config/git/config",
    HOME_U + "//.claude/settings.json",
    HOME_U + "/.claude//hooks/x.sh",
    HOME_U + "/./.claude/hooks/x.sh",
    "/r/src/../x.py",
    "/r/src/..",
]
# T-TAM-4 and the Task 9 acceptance: a source file and the guard source path.
NONE_PATHS = [
    "src/x.py",
    "/r/src/x.py",
    "/r/src/superclaude/hooks/scripts/launch-level-guard.sh",
    "/r/.dev/hook-launch-level-394/notes.txt",
    "/r/src/..x/y.py",
]
EDIT_TOOL_NAMES = ["Edit", "Write", "NotebookEdit"]


@pytest.mark.parametrize("tool", EDIT_TOOL_NAMES)
@pytest.mark.parametrize(
    "path, level, msg_id",
    [
        *_oracle_params("TAMP", [(p, "TAMPER") for p in TAMPER_PATHS]),
        *_oracle_params("NONEP", [(p, "NONE") for p in NONE_PATHS]),
    ],
)
def test_tamper_paths(tmp_path, tool, path, level, msg_id):
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(_edit(tool, path), tmp_path)
    # Edit tools are not text classes, so no LL-TEXT note.
    _assert_decision(result, tmp_path, msg_id, level)


@pytest.mark.parametrize("level", LEVEL_ORDER)
@pytest.mark.parametrize(
    "tool, extra",
    [
        ("Write", {"content": "see ~/.claude/hooks and disableAllHooks"}),
        ("Edit", {"old_string": ".claude/hooks", "new_string": "disableAllHooks"}),
        ("NotebookEdit", {"new_source": "~/.claude/settings.json"}),
    ],
)
def test_tamper_ignores_content(tmp_path, level, tool, extra):
    # T-TAM-3, FR-L-51: contents are never read, only the path.
    _bind(tmp_path, *LEVEL_FILES[level])
    _assert_decision(
        _run(_edit(tool, "/r/src/x.py", **extra), tmp_path), tmp_path, None, level
    )


@pytest.mark.parametrize(
    "payload",
    [
        _bash("rm -rf " + STATE_PATH),
        _bash("uv run superclaude install"),
        _bash("claude -p x"),
        _bash("orca terminal send"),
        _edit("Edit", "~/.claude/settings.json"),
        _edit("Write", "~/.config/git/config"),
    ],
    ids=[
        "rm-store",
        "reinstall",
        "claude-p",
        "orca-send",
        "edit-settings",
        "write-gitconfig",
    ],
)
def test_tamper_escape_in_ordinary_session_allowed(tmp_path, payload):
    # T-TAM-7 (X-005): an unbound session is never blocked.
    _bind(tmp_path, *LEVEL_FILES["W"])
    payload = {**payload, "session_id": "ordinary-session"}
    result = _run(payload, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


# The Task 9 acceptance examples, each at every level.
TASK9_ACCEPTANCE = [
    (_edit("Edit", "~/.claude/settings.json"), "TAMPER"),
    (_edit("Write", "~/.config/git/config"), "TAMPER"),
    (_bash("rm -rf " + STATE_PATH), "TAMPER"),
    (_edit("Edit", "src/x.py"), "NONE"),
    (_edit("Write", "/r/src/x.py", content="quotes .claude/hooks here"), "NONE"),
    (_bash("npx -y @anthropic-ai/claude-code@latest -p x"), "ESCAPE"),
    (_bash("claude -p x"), "ESCAPE"),
    (_bash("tmux send-keys approved Enter"), "ESCAPE"),
    (_bash("orca terminal send"), "ESCAPE"),
    (_bash("orca worktree list"), "NONE"),
    (_bash("orca status"), "NONE"),
]


@pytest.mark.parametrize(
    "payload, level, msg_id", list(_oracle_params("acc", TASK9_ACCEPTANCE))
)
def test_tamper_escape_task9_acceptance(tmp_path, payload, level, msg_id):
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(payload, tmp_path)
    is_text = payload["tool_name"] == "Bash" and msg_id is not None
    _assert_decision(result, tmp_path, msg_id, level, text=is_text)


@pytest.mark.parametrize("level", LEVEL_ORDER)
def test_tamper_message_names_store_and_session(tmp_path, level):
    # A bound session's LL-TAMPER gives the exact rm command for its own files.
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(_edit("Edit", "~/.claude/settings.json"), tmp_path)
    store = _store(tmp_path / "home")
    rm = f'rm "{store}/sessions/{SID}" "{store}/sessions/{SID}.ok"'
    assert result.returncode == 2
    you_can = result.stderr.decode().splitlines()[3]
    assert you_can.startswith("You can: ") and you_can.endswith(f": {rm}")


# --- the full grid, Agent/Task, TURN, MCP, escape tools, gaps, corpus (Task 10)


def _tool(tool_name: str, sid: str = SID, **tool_input) -> dict:
    return {
        "hook_event_name": "PreToolUse",
        "session_id": sid,
        "tool_name": tool_name,
        "tool_input": tool_input,
    }


def _text_note(payload: dict, msg_id) -> bool:
    # LL-TEXT follows any block of a Bash or Monitor call (section 9).
    return msg_id is not None and payload["tool_name"] in ("Bash", "Monitor")


# T-GRID-1: real tool calls, at least one per class. A natural call can carry a
# second class of higher precedence; such a row lists its own decisions, and at
# FS (where that second class is allowed) its class's own oracle cell shows.
_VIA_SUBMIT = {"W": "LL-SUBMIT", "WA": "LL-SUBMIT", "F": "LL-SUBMIT", "FS": "LL-REPO"}
_VIA_PUSH = {"W": "LL-PUSH", "WA": "LL-PUSH", "F": "LL-PUSH", "FS": "LL-PUSH-FORM"}
GRID_CASES = [
    ("NONE", "skill-workflow", _skill("sc:workflow"), None),
    ("NONE", "read", _tool("Read", file_path="/etc/passwd"), None),
    ("NONE", "agent-local", _tool("Agent", prompt="git push origin main"), None),
    ("NONE", "mcp-list", _tool("mcp__github__list_issues"), None),
    ("NONE", "bash-ls", _bash("ls"), None),
    ("IMPL", "skill-implement", _skill("sc:implement"), None),
    ("TURN", "cron-create", _tool("CronCreate", prompt="approved"), None),
    ("TURN", "schedule-wakeup", _tool("ScheduleWakeup"), None),
    ("SUBMIT", "skill-pr-submit", _skill("sc:pr-submit"), None),
    ("SUBMIT", "gh-pr-create-repo", _bash(f"gh pr create {REPO_FLAG} --title x"), None),
    ("COMMIT", "git-commit", _bash("git commit -m x"), None),
    ("PUSH", "git-push-canonical", _bash("git push -u origin feature"), None),
    ("PUSHFORM", "git-push-force", _bash("git push --force origin f"), _VIA_PUSH),
    ("PROTECTED", "git-push-main", _bash("git push origin main"), None),
    ("MERGE", "gh-pr-merge", _bash("gh pr merge 5"), None),
    ("MERGE", "mcp-merge", _tool("mcp__github__merge_pull_request"), None),
    ("GHWRITE", "gh-api-graphql", _bash("gh api graphql"), None),
    ("UNKNOWN", "git-alias", _bash("git ci"), None),
    ("MCP", "mcp-push-files", _tool("mcp__github__push_files"), None),
    ("ESCAPE", "skill-issue", _skill("sc:issue"), None),
    ("ESCAPE", "agent-remote", _tool("Agent", isolation="remote"), None),
    ("ESCAPE", "workflow", _tool("Workflow"), None),
    ("TAMPER", "edit-settings", _edit("Edit", "~/.claude/settings.json"), None),
    ("SKILL", "skill-empty", _skill(""), None),
    ("BIG", "bash-big", _bash("echo " + "y" * 70_000), None),
    ("REPO", "gh-pr-create", _bash("gh pr create --title x"), _VIA_SUBMIT),
]


def _grid_params():
    for cls, case_id, payload, own in GRID_CASES:
        for level in LEVEL_ORDER:
            msg_id = (own or EXPECTED[cls])[level]
            yield pytest.param(
                payload, level, msg_id, id=f"GRID-{cls}-{case_id}-{level}"
            )


@pytest.mark.parametrize("payload, level, msg_id", list(_grid_params()))
def test_grid_policy(tmp_path, payload, level, msg_id):
    # T-GRID-1
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(payload, tmp_path)
    _assert_decision(result, tmp_path, msg_id, level, text=_text_note(payload, msg_id))


def test_grid_complete():
    # T-GRID-2: every class has an oracle row with W, WA, F and FS, and a case.
    assert len(set(GRID_CLASSES)) == 16
    assert set(EXPECTED) == set(GRID_CLASSES) | {"NONE"}
    for cls, row in EXPECTED.items():
        assert sorted(row) == sorted(LEVEL_ORDER), cls
    assert {cls for cls, *_ in GRID_CASES} == set(EXPECTED)
    for cls, _case_id, _payload, own in GRID_CASES:
        if own:
            assert own["FS"] == EXPECTED[cls]["FS"], cls


_STEP_CASES = {
    "skill-implement": _skill("sc:implement"),
    "git-commit": _bash("git commit -m x"),
    "git-push": _bash("git push -u origin feature"),
    "skill-pr-submit": _skill("sc:pr-submit"),
    "gh-pr-create-repo": _bash(f"gh pr create {REPO_FLAG} --title x"),
    "write-plan": _edit("Write", ".dev/tasks/x/plan.md"),
    "skill-workflow": _skill("sc:workflow"),
}
# T-GRID-3 (W), T-GRID-4 (F), T-GRID-5 (FS), typed from MR section 8.2.
GRID_STEPS = {
    "W": {
        "skill-implement": "LL-IMPL",
        "git-commit": "LL-COMMIT",
        "git-push": "LL-PUSH",
        "skill-pr-submit": "LL-SUBMIT",
        "gh-pr-create-repo": "LL-SUBMIT",
        "write-plan": None,
        "skill-workflow": None,
    },
    "F": {
        "skill-implement": None,
        "git-commit": "LL-COMMIT",
        "git-push": "LL-PUSH",
        "skill-pr-submit": "LL-SUBMIT",
        "gh-pr-create-repo": "LL-SUBMIT",
    },
    "FS": {
        "git-commit": None,
        "git-push": None,
        "skill-pr-submit": None,
        "gh-pr-create-repo": None,
    },
}


@pytest.mark.parametrize(
    "level, name, msg_id",
    [
        pytest.param(level, name, msg_id, id=f"GRID-step-{level}-{name}")
        for level, rows in GRID_STEPS.items()
        for name, msg_id in rows.items()
    ],
)
def test_grid_level_steps(tmp_path, level, name, msg_id):
    payload = _STEP_CASES[name]
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(payload, tmp_path)
    _assert_decision(result, tmp_path, msg_id, level, text=_text_note(payload, msg_id))


TURN_TOOLS = ["CronCreate", "CronDelete", "CronList", "Cron", "ScheduleWakeup"]


@pytest.mark.parametrize("level", LEVEL_ORDER)
@pytest.mark.parametrize("tool", TURN_TOOLS)
def test_trn_cron_schedule_turn_only_at_w(tmp_path, tool, level):
    # T-TRN-1, T-TRN-2: FR-L-43, ^Cron[A-Za-z]*$ and ^Schedule[A-Za-z]*$.
    _bind(tmp_path, *LEVEL_FILES[level])
    msg_id = "LL-TURN" if level == "W" else None
    _assert_decision(_run(_tool(tool, prompt="x"), tmp_path), tmp_path, msg_id, level)


@pytest.mark.parametrize("tool", ["cronCreate", "XCronCreate", "Cron2", "Scheduler_x"])
def test_trn_lookalike_names_stay_none(tmp_path, tool):
    _bind(tmp_path, "worktree")
    _assert_decision(_run(_tool(tool), tmp_path), tmp_path, None, "W")


@pytest.mark.parametrize(
    "payload, level, msg_id",
    [
        pytest.param(
            _bash("git push origin main", tool="Monitor"),
            "FS",
            "LL-PROTECTED",
            id="TRN-3-monitor-main",
        ),
        pytest.param(
            _bash("git commit -m x", run_in_background=True),
            "F",
            "LL-COMMIT",
            id="TRN-3-background-commit",
        ),
    ],
)
def test_trn_monitor_and_background_text_classified(tmp_path, payload, level, msg_id):
    # T-TRN-3: FR-L-44, the command is classified like a foreground Bash command.
    _bind(tmp_path, *LEVEL_FILES[level])
    _assert_decision(_run(payload, tmp_path), tmp_path, msg_id, level, text=True)


# T-TRN-4: every route that can start a turn, at W.
TRN_ROUTES = [
    ("cron-create", _tool("CronCreate", prompt="approved"), "LL-TURN"),
    ("cron-delete", _tool("CronDelete"), "LL-TURN"),
    ("schedule-wakeup", _tool("ScheduleWakeup"), "LL-TURN"),
    ("orca-send", _bash("orca terminal send --text approved"), "LL-ESCAPE"),
    ("orca-type", _bash("orca computer type-text approved"), "LL-ESCAPE"),
    ("tmux-send-keys", _bash("tmux send-keys approved Enter"), "LL-ESCAPE"),
    ("screen-stuff", _bash("screen -X stuff approved"), "LL-ESCAPE"),
    ("xdotool", _bash("xdotool type approved"), "LL-ESCAPE"),
    ("send-message", _tool("SendMessage", to="main", message="approved"), "LL-ESCAPE"),
    ("tmux-split", _bash("tm\\\nux send-keys approved Enter"), "LL-UNKNOWN"),
    ("monitor-ls", _bash("ls", tool="Monitor"), None),
    ("bash-background", _bash("ls", run_in_background=True), None),
    ("agent-background", _tool("Agent", prompt="x", run_in_background=True), None),
    ("task-background", _tool("Task", prompt="x", run_in_background=True), None),
]


@pytest.mark.parametrize(
    "payload, msg_id",
    [pytest.param(p, m, id=f"TRN-4-{name}") for name, p, m in TRN_ROUTES],
)
def test_trn_route_table_at_w(tmp_path, payload, msg_id):
    _bind(tmp_path, *LEVEL_FILES["W"])
    result = _run(payload, tmp_path)
    _assert_decision(result, tmp_path, msg_id, "W", text=_text_note(payload, msg_id))


@pytest.mark.parametrize("level", LEVEL_ORDER)
@pytest.mark.parametrize("tool", ["Agent", "Task"])
@pytest.mark.parametrize(
    "tool_input, msg_id",
    [
        pytest.param({"isolation": "remote"}, "LL-ESCAPE", id="remote"),
        pytest.param({"isolation": "worktree"}, None, id="worktree"),
        pytest.param({}, None, id="local"),
        pytest.param({"run_in_background": True}, None, id="background"),
        pytest.param(
            {"prompt": "gh pr merge 5; git push origin main"}, None, id="prompt"
        ),
    ],
)
def test_esc_agent_task_isolation(tmp_path, tool, tool_input, msg_id, level):
    # T-ESC-3, T-ISO-9: FR-L-41, FR-L-46; Agent and Task decide alike, and
    # the prompt is never scanned.
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(_tool(tool, **tool_input), tmp_path)
    _assert_decision(result, tmp_path, msg_id, level)


@pytest.mark.parametrize("level", LEVEL_ORDER)
@pytest.mark.parametrize("tool", ["Workflow", "RemoteTrigger", "SendMessage"])
def test_esc_escape_tools(tmp_path, tool, level):
    # T-ESC-4: FR-L-46.
    _bind(tmp_path, *LEVEL_FILES[level])
    _assert_decision(_run(_tool(tool), tmp_path), tmp_path, "LL-ESCAPE", level)


# T-MCP-1 to T-MCP-3: FR-L-45, N is the text after the last "__", lower case.
MCP_CASES = [
    ("mcp__github__merge_pull_request", "LL-MERGE"),
    ("mcp__github__MERGE_PULL_REQUEST", "LL-MERGE"),
    ("mcp__gitlab__accept_merge_request", "LL-MERGE"),
    ("mcp__github__push_files", "LL-MCP"),
    ("mcp__github__create_or_update_file", "LL-MCP"),
    ("mcp__github__create_pull_request", "LL-MCP"),
    ("mcp__github__delete_file", "LL-MCP"),
    ("mcp__github__create_branch", "LL-MCP"),
    ("mcp__github__update_ref", "LL-MCP"),
    ("mcp__git__git_commit", "LL-MCP"),
    ("mcp__github__list_commits", None),
    ("mcp__github__get_commit", None),
    ("mcp__github__list_issues", None),
    ("mcp__github__get_pull_request", None),
    ("mcp__github__search_pull_requests", None),
    ("mcp__github__list_merge_requests", None),
    ("mcp__github__read_file", None),
    ("mcp__github__create_issue", None),
    ("mcp__codegraph__codegraph_search", None),
    # The keyword is in the server part, not in N: NONE.
    ("mcp__merge_push__list_items", None),
]


@pytest.mark.parametrize("level", LEVEL_ORDER)
@pytest.mark.parametrize("tool, msg_id", MCP_CASES)
def test_mcp_tools(tmp_path, tool, msg_id, level):
    _bind(tmp_path, *LEVEL_FILES[level])
    _assert_decision(_run(_tool(tool), tmp_path), tmp_path, msg_id, level)


@pytest.mark.parametrize(
    "tool, tool_input",
    [
        ("mcp__github__merge_pull_request", {}),
        ("mcp__github__push_files", {}),
        ("CronCreate", {"prompt": "approved"}),
        ("Workflow", {}),
        ("Agent", {"isolation": "remote"}),
    ],
)
def test_mcp_ordinary_session_allowed(tmp_path, tool, tool_input):
    # T-MCP-4 (and the other Task 10 classes): an unbound session exits 0.
    _bind(tmp_path, *LEVEL_FILES["W"])
    result = _run(_tool(tool, sid="ordinary-session", **tool_input), tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


# T-GAP-1: design section 4 row 33. ACCEPTED LEAKS of residual risk R1 (a
# command name built from a variable, an escape or a glob, or a script file):
# each is pinned as allowed at every level, so closing one is a deliberate
# change (owner decision O-7), not a silent one.
ACCEPTED_LEAKS = {
    "T-ATK-26": "G=gi; ${G}t push origin main",
    "T-ATK-27": "GH=gh; $GH pr merge 5",
    "T-ATK-28": "$'\\x67it' push origin main",
    "N-ATK-7": "/usr/bin/gi[t] push origin HEAD:main",
    "row33-glob": "/usr/bin/gi[t] push origin main",
    "row33-script": "bash ./push.sh",
}


@pytest.mark.parametrize("level", LEVEL_ORDER)
@pytest.mark.parametrize(
    "command",
    [pytest.param(c, id=f"GAP-leak-R1-{k}") for k, c in ACCEPTED_LEAKS.items()],
)
def test_known_gaps_pinned(tmp_path, command, level):
    _git_case(tmp_path, command, level, None)


# T-COR-1 seed: rows of MR section 8.3/8.4 in its own layout (id, the class
# shown at W, WA, F and FS or "allow", the command; <NL> is a newline). Tasks 16
# and 17 append the rest of the corpus here; T-COR-2 (bare-remote replay) is
# Task 16. Rows named in ACCEPTED_LEAKS are the R1 accepted leaks.
CORPUS = r"""
T-ATK-1    PUSH      PUSH      PUSH      PUSHFORM   git push origin a:b `echo c:main`
T-ATK-2    PUSH      PUSH      PUSH      PUSHFORM   git push origin a:b \<NL>c:main
T-ATK-3    PUSH      PUSH      PUSH      PUSHFORM   git-push origin main
T-ATK-25   PUSH      PUSH      PUSH      PUSHFORM   GIT=git; $GIT push origin main
T-ATK-26   allow     allow     allow     allow      G=gi; ${G}t push origin main
T-ATK-27   allow     allow     allow     allow      GH=gh; $GH pr merge 5
T-ATK-28   allow     allow     allow     allow      $'\x67it' push origin main
T-ATK-55   TAMPER    TAMPER    TAMPER    TAMPER     cd ~/.claude && rm -rf state
T-ATK-60   ESCAPE    ESCAPE    ESCAPE    ESCAPE     claude \<NL>-p x
T-ATK-61   ESCAPE    ESCAPE    ESCAPE    ESCAPE     /usr/local/bin/claude --print x
T-OK-1     allow     allow     allow     allow      git status
T-OK-2     allow     allow     allow     allow      git diff
T-OK-3     allow     allow     allow     allow      git log --oneline
T-OVR-1    MERGE     MERGE     MERGE     MERGE      git log --grep merge
N-ATK-1    UNKNOWN   UNKNOWN   UNKNOWN   UNKNOWN    gi\<NL>t push origin HEAD:main
N-ATK-7    allow     allow     allow     allow      /usr/bin/gi[t] push origin HEAD:main
"""
CORPUS_IDS = {
    "allow": None,
    "PUSHFORM": "LL-PUSH-FORM",
    "GHWRITE": "LL-GH-WRITE",
}


def _corpus_params():
    for line in CORPUS.strip().splitlines():
        row_id, *cells = line.split(None, 5)
        command = cells.pop().replace("<NL>", "\n")
        for level, cell in zip(LEVEL_ORDER, cells):
            msg_id = CORPUS_IDS.get(cell, f"LL-{cell}")
            yield pytest.param(command, level, msg_id, id=f"COR-{row_id}-{level}")


@pytest.mark.parametrize("command, level, msg_id", list(_corpus_params()))
def test_regression_corpus(tmp_path, command, level, msg_id):
    # T-COR-1
    _git_case(tmp_path, command, level, msg_id)


# --- UserPromptSubmit: typed approval at the worktree level (Task 11) --------


def _ok_path(tmp_path: Path) -> Path:
    return _store(tmp_path / "home") / "sessions" / f"{SID}.ok"


def _approve(tmp_path: Path, text: str, **extra):
    """Send one prompt; a prompt event always allows silently."""
    result = _run(_prompt(text, **extra), tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    return result


APPROVING = [
    # T-APR-1: the whole prompt, trimmed and lower-cased.
    "approved",
    "Approved.",
    "  APPROVED!  ",
    "approved\n",
    "\t\r\napproved!\r\n",
    # T-APR-2: the first line, leading whitespace removed (case-sensitive).
    "/sc:implement x",
    "/task",
    "/sc:task y",
    "/task y",
    "/sc:implement",
    "  /sc:implement x\nmore text",
    "\n/task\tz",
    "/task\nsecond line",
]
NOT_APPROVING = [
    # T-APR-4
    "please approved",
    "approved, but",
    "/task-builder x",
    "/tasks",
    "/sc:implement-protocol",
    "/sc:pr-submit",
    "approved approved",
    "approved!!",
    "approved?",
    "approvedx",
    "not approved",
    "/sc:implementx",
    "/SC:IMPLEMENT x",
    "x\n/sc:implement y",
    "sc:implement x",
    "",
]


@pytest.mark.parametrize("text", APPROVING, ids=lambda t: f"APR-yes-{t!r}")
def test_apr_matching_prompt_writes_ok_at_w(tmp_path, text):
    # T-APR-1, T-APR-2: FR-L-16; the .ok file is empty, regular, not a link.
    sessions = _bind(tmp_path, "worktree")
    _approve(tmp_path, text)
    ok = _ok_path(tmp_path)
    assert ok.is_file() and not ok.is_symlink()
    assert ok.read_bytes() == b""
    assert sorted(p.name for p in sessions.iterdir()) == [SID, f"{SID}.ok"]


@pytest.mark.parametrize("text", NOT_APPROVING, ids=lambda t: f"APR-no-{t!r}")
def test_apr_exact_form_needed(tmp_path, text):
    # T-APR-4
    _bind(tmp_path, "worktree")
    _approve(tmp_path, text)
    assert _session_files(tmp_path) == [SID]


@pytest.mark.parametrize("agent_id", ["agent-1", "a"])
@pytest.mark.parametrize("text", ["approved", "/sc:implement x"])
def test_apr_ignored_with_agent_id(tmp_path, text, agent_id):
    # T-APR-3: a subagent prompt never approves (B5, U17).
    _bind(tmp_path, "worktree")
    _approve(tmp_path, text, agent_id=agent_id)
    assert _session_files(tmp_path) == [SID]


@pytest.mark.parametrize("word", ["full", "full-submit"])
@pytest.mark.parametrize("text", ["approved", "/sc:implement x", "/task y"])
def test_apr_ok_written_only_at_worktree(tmp_path, word, text):
    # T-APR-6: FR-L-15, nothing is written at F and FS.
    _bind(tmp_path, word)
    _approve(tmp_path, text)
    assert _session_files(tmp_path) == [SID]


def test_apr_unbound_session_cannot_approve(tmp_path):
    # T-APR-7: an unbound id writes nothing, with an empty or a nonempty store.
    _approve(tmp_path, "approved")
    assert not _store(tmp_path / "home").exists()
    _bind(tmp_path, "worktree")
    _approve(tmp_path, "approved", sid="other-session")
    _approve(tmp_path, "approved", sid=None)
    assert _session_files(tmp_path) == [SID]


@pytest.mark.parametrize("word", ["degraded", "bogus", "", "worktree\n"])
def test_apr_degraded_session_can_approve(tmp_path, word):
    # T-APR-8: an invalid word is worktree, so approval is written and unlocks IMPL.
    _bind(tmp_path, word)
    _assert_decision(
        _run(_skill("sc:implement"), tmp_path),
        tmp_path,
        "LL-IMPL",
        "W",
        note=word not in ("worktree\n",),
    )
    _approve(tmp_path, "approved")
    assert _ok_path(tmp_path).is_file()
    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, None, "WA")


@pytest.mark.parametrize("text", ["/sc:implement x", "/task y", "approved"])
def test_apr_typed_implement_then_skill_call_allowed(tmp_path, text):
    # T-APR-9: FR-L-18, in order: the Skill call is blocked before the prompt,
    # the prompt event writes .ok, then the expanded Skill call is allowed.
    _bind(tmp_path, "worktree")
    skill = _skill("sc:implement-protocol")
    _assert_decision(_run(skill, tmp_path), tmp_path, "LL-IMPL", "W")
    assert not _ok_path(tmp_path).exists()
    _approve(tmp_path, text)
    assert _ok_path(tmp_path).is_file()
    _assert_decision(_run(skill, tmp_path), tmp_path, None, "WA")
    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, None, "WA")


APR_STILL_BLOCKED = [
    ("commit", _bash("git commit -m x"), "LL-COMMIT"),
    ("push", _bash("git push origin feature"), "LL-PUSH"),
    ("pr-create", _bash("gh pr create --repo o/r --title x"), "LL-SUBMIT"),
    ("pr-submit", _skill("sc:pr-submit"), "LL-SUBMIT"),
    ("merge", _bash("gh pr merge 5"), "LL-MERGE"),
    ("push-main", _bash("git push origin main"), "LL-PROTECTED"),
]


@pytest.mark.parametrize(
    "payload, msg_id",
    [pytest.param(p, m, id=f"APR-5-{n}") for n, p, m in APR_STILL_BLOCKED],
)
def test_apr_approval_never_unlocks_commit_push_submit(tmp_path, payload, msg_id):
    # T-APR-5: FR-L-17, the typed approval gives WA, which unlocks IMPL only.
    _bind(tmp_path, "worktree")
    _approve(tmp_path, "approved")
    result = _run(payload, tmp_path)
    _assert_decision(result, tmp_path, msg_id, "WA", text=_text_note(payload, msg_id))


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory modes")
def test_apr_failed_write_shows_later_as_impl(tmp_path):
    # FR-L-17: a read-only sessions directory leaves no .ok, the prompt still
    # goes ahead, and the next Skill sc:implement call is LL-IMPL.
    sessions = _bind(tmp_path, "worktree")
    sessions.chmod(0o500)
    try:
        _approve(tmp_path, "approved")
        _approve(tmp_path, "/sc:implement x")
        assert sorted(p.name for p in sessions.iterdir()) == [SID]
        result = _run(_skill("sc:implement"), tmp_path)
    finally:
        sessions.chmod(0o700)
    _assert_decision(result, tmp_path, "LL-IMPL", "W")


def test_apr_existing_ok_link_never_followed(tmp_path):
    # Task 4 discipline: no replace, regular non-symlink files only. A link at
    # the .ok path is left alone, its target is not created and is no approval.
    _bind(tmp_path, "worktree")
    target = tmp_path / "elsewhere"
    _ok_path(tmp_path).symlink_to(target)
    _approve(tmp_path, "approved")
    assert not target.exists() and _ok_path(tmp_path).is_symlink()
    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")


def test_apr_lasts_until_a_person_deletes_the_files(tmp_path):
    # O-6: later prompts and calls never remove the approval.
    _bind(tmp_path, "worktree")
    _approve(tmp_path, "approved")
    for text in ("please approved", "/sc:pr-submit", "approved", "anything"):
        _approve(tmp_path, text)
    assert _session_files(tmp_path) == [SID, f"{SID}.ok"]
    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, None, "WA")
    _ok_path(tmp_path).unlink()
    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")


WRAPPED_TURNS = {
    "task-notification": (
        "<task-notification>\n<task-id>b1</task-id>\n<status>completed</status>\n"
        "<summary>Background command finished</summary>\n<result>\napproved\n"
        "</result>\n</task-notification>"
    ),
    "monitor-line": "<monitor-event>\napproved\n</monitor-event>",
    "subagent-result": (
        "<task-notification>\n<result>/sc:implement x</result>\n</task-notification>"
    ),
}


@pytest.mark.parametrize("text", WRAPPED_TURNS.values(), ids=list(WRAPPED_TURNS))
def test_apr_wrapped_notification_does_not_approve(tmp_path, text):
    # T-APR-10: hand-written shape until OB-H1 item 5 supplies the real one.
    _bind(tmp_path, "worktree")
    _approve(tmp_path, text)
    assert _session_files(tmp_path) == [SID]
    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")


def test_apr_prompt_runs_no_sed_or_tr(tmp_path):
    # Trimming and lower-casing are bash string operations.
    log = _counting_bin(tmp_path)
    _bind(tmp_path, "worktree")
    _approve(tmp_path, "  APPROVED!  ")
    _approve(tmp_path, "please approved " * 1000)
    assert _ok_path(tmp_path).is_file()
    assert not log.exists()


@pytest.mark.parametrize("tool", ["CronCreate", "ScheduleWakeup"])
def test_trn_turn_blocked_before_and_allowed_after_typed_approval(tmp_path, tool):
    # T-TRN-1, T-TRN-2 through the real approval route.
    _bind(tmp_path, "worktree")
    payload = _tool(tool, prompt="approved")
    _assert_decision(_run(payload, tmp_path), tmp_path, "LL-TURN", "W")
    _approve(tmp_path, "approved")
    _assert_decision(_run(payload, tmp_path), tmp_path, None, "WA")


def test_trn_routes_never_write_approval(tmp_path):
    # T-TRN-4: no route the agent can call writes an approval, and the turn a
    # background route starts arrives wrapped (T-APR-10), so IMPL stays blocked.
    _bind(tmp_path, "worktree")
    for _name, payload, _msg_id in TRN_ROUTES:
        _run(payload, tmp_path)
    for text in WRAPPED_TURNS.values():
        _approve(tmp_path, text)
    assert _session_files(tmp_path) == [SID]
    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")


# --- Task 16: push, git, alias, merge and benign corpus; T-COR-2 -------------
#
# Expected results are written by hand from design sections 4 and 5 (DD-2), not
# copied from the MR corpus columns; "override:" marks a row whose result
# differs from MR section 8.3/8.4. <R> of MR section 8.4 is the path /tmp/r.git.
# Accepted leaks are pinned as allow with their residual id of design section 16.

R16 = "/tmp/r.git"
SEND_PACK = f"git send-pack {R16} HEAD:refs/heads/main"
CONFIG_PUSH = "git config remote.origin.push refs/heads/feature:refs/heads/main"

CORPUS16 = [
    # Push routes.
    ("ATK-1", "git push origin a:b `echo c:main`", PUSHFORM),
    ("ATK-13", "git push origin --all", PUSHFORM),
    ("ATK-25", "GIT=git; $GIT push origin main", PUSHFORM),
    ("ATK-29", 'A=">" git push origin HEAD:main', PUSHFORM),
    ("ATK-50", 'bash -c "git push origin main"', PUSHFORM),
    # Aliases and variable subcommands.
    ("ATK-10", "git rebase -x 'git -c alias.p=push p origin HEAD:main' HEAD~1", UNK),
    ("ATK-35", "Q=sh git rebase -x 'git pu$Q origin HEAD:main' HEAD~1", UNK),
    ("ATK-42", "git -c alias.ci=commit ci", UNK),
    # Merges.
    ("ATK-48", "curl -X PUT https://api.github.com/repos/o/r/pulls/5/merge", MERGE),
    ("ATK-49", "git pull", MERGE),
    ("ATK-51", "gh pr merge 5", MERGE),
    # Accepted leaks, pinned allow.
    ("ATK-26", "G=gi; ${G}t push origin main", NONE4),  # R1
    ("ATK-27", "GH=gh; $GH pr merge 5", NONE4),  # R1
    ("ATK-28", "$'\\x67it' push origin main", NONE4),  # R1
    ("NATK-7", "/usr/bin/gi[t] push origin HEAD:main", NONE4),  # R1
    ("NATK-31", "rm -rf ~/.{claude,x}/state", NONE4),  # R3
    ("NATK-36", "flock /tmp/l gh mm 5", NONE4),  # R17 (gh alias, U24)
    # Benign rows that involve git or gh (T-OK-10, 11, 13, 14, 35 and 36 do not).
    ("OK-1", "git status", NONE4),
    ("OK-2", "git diff", NONE4),
    ("OK-3", "git log --oneline", NONE4),
    ("OK-4", "git fetch origin", NONE4),
    ("OK-5", "git add .dev/tasks", NONE4),
    ("OK-6", "git checkout -b x", NONE4),
    ("OK-7", "git commit -m x", COMMIT),
    ("OK-8", "gh pr view 5", NONE4),
    ("OK-9", "gh api repos/o/r/pulls", NONE4),
    ("OK-12", "grep -rn push docs/", NONE4),
    ("OK-15", "git push -u origin feature", PUSH_OK),
    (
        "OK-16",
        f'gh pr create {REPO_FLAG} --base master --head f --title "docs: explain'
        ' git hooks" --body "x"',
        SUBMIT,
    ),
    ("OK-17", 'git commit -m "fix git handling"', COMMIT),
    ("OK-18", "git push origin 3f2a9c1e:feature/x", PUSH_OK),
    ("OK-19", "gh api repos/o/r/commits/abc123/check-runs --jq .total_count", NONE4),
    (
        "OK-20",
        "REPO=\"$(git remote get-url origin | sed -E 's#(git@|https://)github.com"
        "[:/]##; s#\\.git$##')\"",
        NONE4,
    ),
    ("OK-21", 'git update-ref "refs/superclaude/implement/p/T1" "$start"', NONE4),
    (
        "OK-22",
        'idx=$(mktemp); GIT_INDEX_FILE="$idx" git read-tree HEAD && '
        'GIT_INDEX_FILE="$idx" git add -A && start=$(GIT_INDEX_FILE="$idx" '
        'git write-tree); rm -f "$idx"',
        NONE4,
    ),
    (
        "OK-23",
        '# NUL-separated revert domain of tree $1\ngit -C "$top" update-ref "$ref"'
        ' "$now" ""\nif [[ ! $last =~ step=revert ]]; then :; fi',
        NONE4,
    ),
    (
        "OK-24",
        "git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge-tree"
        " --write-tree a b",
        NONE4,
    ),
    ("OK-25", 'echo "use git for hooks"', NONE4),
    ("OK-26", 'grep -rn "git worktree" docs/', NONE4),
    ("OK-27", "git status 2>&1 | tail -5", NONE4),
    ("OK-28", "git commit -m x > /tmp/log 2>&1", COMMIT),
    (
        "OK-29",
        f"gh pr create {REPO_FLAG} \\\n  --base master --head f --title x --body y",
        SUBMIT,
    ),
    ("OK-30", "git commit -F - <<EOF\nfix: use git for hooks\nEOF", COMMIT),
    ("OK-31", "git rebase origin/master", NONE4),
    ("OK-32", "git log --cherry-pick --left-right a...b", NONE4),
    # override: MR allows at FS; H4 needs the --repo operand in the segment of
    # `pr create`, and the newline puts it in the next segment, so REPO at FS.
    ("OK-33", f"gh pr create \\\n  {REPO_FLAG} --title x --body y", SUBMIT_REPO),
    ("OK-34", "gh pr view 5 \\\n  --json mergeable,mergeStateStatus", NONE4),
    # Pinned over-blocks.
    ("OVR-1", "git log --grep merge", MERGE),
    (
        "OVR-2",
        'gh pr create --repo o/r --title "x" --body "this pull request fixes git'
        ' hooks"',
        MERGE,
    ),
    ("OVR-3", "git log --oneline | grep push", PUSHFORM),
    ("OVR-4", 'gh pr create --repo o/r --title "fix api docs"', GHWRITE),
    ("OVR-5", "git config --get-regexp alias.", UNK),
    ("OVR-6", "git \\\ncommit -m x", UNK),
    # Amendment attacks that concern git (N-ATK-39 is the Write test below).
    ("NATK-1", "gi\\\nt push origin HEAD:main", UNK),
    ("NATK-2", 'bash -c "gi\\\nt push origin HEAD:main"', UNK),
    ("NATK-3", "git$'' push origin HEAD:main", PUSHFORM),
    ("NATK-4", 'g$""it push origin HEAD:main', PUSHFORM),
    ("NATK-5", f"if true; then {SEND_PACK}; fi", UNK),
    ("NATK-6", f"find . -maxdepth 0 -exec {SEND_PACK} \\;", PUSHFORM),
    ("NATK-8", f"if true; then {CONFIG_PUSH}; fi", UNK),
    ("NATK-9", f"env -u FOO {CONFIG_PUSH}", UNK),
    ("NATK-10", f"flock /tmp/l {CONFIG_PUSH}", UNK),
    # Second step of N-ATK-8, 9, 10 and 39: the canonical push is allowed at FS;
    # a pre-set push config is residual R11 (the agent cannot set one).
    ("NATK-8-step2", "git push origin feature", PUSH_OK),  # R11
    ("NATK-11", f"timeout -s KILL 30 {SEND_PACK}", PUSHFORM),
    ("NATK-12", f"git rebase -x '{SEND_PACK}' HEAD~1", PUSHFORM),
    ("NATK-13", f"taskset -c 0 {SEND_PACK}", PUSHFORM),
    ("NATK-14", "git rebase -x 'gi\\\nt push origin HEAD:main' HEAD~1", UNK),
    ("NATK-15", "git$'' -c x.y=z push origin HEAD:main", PUSHFORM),
    ("NATK-16", "git$'' merge other --no-edit", MERGE),
    ("NATK-17", "gi\\\nt merge other --no-edit", UNK),
    ("NATK-18", "git$'' commit --allow-empty -m x", COMMIT),
    ("NATK-19", "gi\\\nt commit --allow-empty -m x", UNK),
    (
        "NATK-37",
        "sudo -u coder git remote set-url --push origin https://github.com/evil/x",
        UNK,
    ),
    # Design section 10, git rows.
    ("EDGE-title", 'gh pr create --repo o/r --title "docs: explain git hooks"', SUBMIT),
    ("EDGE-stash", "git stash push -m wip", PUSHFORM),
    ("EDGE-stash-u", "git stash -u -m x", NONE4),
    ("EDGE-pipe", "git push origin f 2>&1 | tail -5", PUSHFORM),
    ("EDGE-slashes", "git push origin x:refs/heads//main", PUSH_OK),
    ("EDGE-c-remote", "git -c remote.origin.push=x:main push origin f", UNK),
    # The section 5.1 table calls `config` NONE; G2 (`remote.`) makes it UNKNOWN,
    # which is the section 10 row, R8 (d).
    ("EDGE-config-url", "git config --get remote.origin.url", UNK),
    ("EDGE-heredoc", "cat > Makefile <<EOF\nall:\\\n\techo x\nEOF", UNK),
    ("EDGE-scope", 'git commit -m "fix(ccsession): x"', ESCAPE),
    ("EDGE-install-hooks", "git add src/superclaude/cli/install_hooks.py", TAMPER),
    # Regression: nonempty PR repo operand (H4).
    ("REG-repo-option", "gh pr create --repo --title x", SUBMIT_REPO),
    # A value option with no value at all is UNKNOWN (G4: "a value-taking Git/gh
    # option with no following value adds UNKNOWN"), which precedes SUBMIT.
    ("REG-repo-dangling", "gh pr create --title x --repo", UNK),
    ("REG-repo-empty-eq", "gh pr create --repo= --title x", SUBMIT_REPO),
    ("REG-repo-R", "gh pr create -R o/r --title x", SUBMIT),
    ("REG-repo-eq", "gh pr create --repo=o/r --title x", SUBMIT),
    # Regression: protected destination (one `refs/heads/` or `heads/` stripped).
    ("REG-prot-refs", "git push origin x:refs/heads/main", PROTECTED),
    ("REG-prot-heads", "git push origin x:heads/master", PROTECTED),
    ("REG-prot-u", "git push -u origin master", PROTECTED),
    ("REG-prot-twice", "git push origin x:refs/heads/refs/heads/main", PUSH_OK),
    ("REG-prot-head", "git push origin x:HEAD", PUSHFORM),
]
assert len({row[0] for row in CORPUS16}) == len(CORPUS16), "duplicate corpus id"


@pytest.mark.parametrize(
    "command, level, msg_id",
    [
        pytest.param(command, level, msg_id, id=f"{row_id}-{level}")
        for row_id, command, ids in CORPUS16
        for level, msg_id in zip(LEVEL_ORDER, ids)
    ],
)
def test_corpus16(tmp_path, command, level, msg_id):
    # T-COR-1, Task 16 rows.
    _git_case(tmp_path, command, level, msg_id)


@pytest.mark.parametrize("level", LEVEL_ORDER)
def test_corpus16_natk39_write_git_config(tmp_path, level):
    # N-ATK-39: the Write of the push redirect is TAMPER; its second step is the
    # NATK-8-step2 row (R11).
    _bind(tmp_path, *LEVEL_FILES[level])
    content = '[remote "origin"]\n\tpush = refs/heads/feature:refs/heads/main\n'
    result = _run(_edit("Write", "~/.config/git/config", content=content), tmp_path)
    _assert_decision(result, tmp_path, "LL-TAMPER", level)


@pytest.mark.parametrize(
    "payload",
    [
        {
            "hook_event_name": "PostToolUse",
            "session_id": SID,
            "tool_name": "Bash",
            "tool_input": {
                "hook_event_name": "PreToolUse",
                "command": "git push origin main",
            },
        },
        {
            "hook_event_name": "PreToolUse",
            "session_id": SID,
            "tool_name": "Read",
            "tool_input": {"tool_name": "Bash", "command": "git push origin main"},
        },
    ],
    ids=["REG-dispatch-nested-event", "REG-dispatch-nested-tool"],
)
def test_corpus16_typed_top_level_dispatch(tmp_path, payload):
    # Regression: only the top-level event and tool_name dispatch. A nested
    # PreToolUse under PostToolUse is a bound other event (LL-BROKEN); a nested
    # Bash under Read is the Read tool (NONE).
    _bind(tmp_path, "full-submit")
    result = _run(payload, tmp_path)
    if payload["hook_event_name"] == "PostToolUse":
        _assert_decision(result, tmp_path, "LL-BROKEN", "FS")
    else:
        _assert_decision(result, tmp_path, None, "FS")


@pytest.mark.parametrize(
    "sid", [None, "bad id!"], ids=["REG-idloss-missing", "REG-idloss-invalid"]
)
def test_corpus16_identity_loss_push_allowed(tmp_path, sid):
    # Regression (design section 10 row 3): no readable id, store non-empty with
    # a bound worktree session: allowed silently, no enforcement claim.
    _bind(tmp_path, "worktree")
    payload = _bash("git push origin main")
    if sid is None:
        del payload["session_id"]
    else:
        payload["session_id"] = sid
    result = _run(payload, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_corpus16_no_replacement_binding(tmp_path):
    # Regression (B8): a later marker with a full-submit record never replaces
    # the worktree binding; the record is consumed and a push stays blocked at W.
    _pending(tmp_path, "worktree")
    _run(_prompt(_marker() + " plan"), tmp_path)
    _assert_bound(tmp_path, SID, "worktree")
    record = _pending(tmp_path, "full-submit", NONCE2)
    result = _run(_prompt(_marker(NONCE2) + " plan"), tmp_path)
    assert (result.returncode, result.stderr) == (0, b"")
    _assert_bound(tmp_path, SID, "worktree")
    assert not record.exists()
    result = _run(_bash("git push origin feature"), tmp_path)
    _assert_decision(result, tmp_path, "LL-PUSH", "W", text=True)


# T-COR-2: the real push attacks of MR section 8.3 (and the N-ATK push rows),
# adapted to a temporary clone whose HEAD (feature) is ahead of remote main.
# Leaks T-ATK-26 and T-ATK-28 are real but residual R1, so they are not replayed.
COR2_ATTACKS = {
    "ATK-1": "git push origin feature:x `echo feature:main`",
    "ATK-2": "git push origin feature:x \\\nfeature:main",
    "ATK-4": "/usr/lib/git-core/git-push origin HEAD:main",
    "ATK-5": "$(git --exec-path)/git-push origin HEAD:main",
    "ATK-10": "git rebase -x 'git -c alias.p=push p origin HEAD:main' HEAD~1",
    "ATK-11": "git status \\\\\ngit -c alias.p=push p origin HEAD:main",
    "ATK-13": "git push origin --all",
    "ATK-14": "git push origin --mirror",
    "ATK-25": "GIT=git; $GIT push origin HEAD:main",
    "ATK-29": 'A=">" git push origin HEAD:main',
    "ATK-32": 'git -c "x.y=a status" push origin HEAD:main',
    "ATK-34": "X=sh git rebase -x 'git -c alias.p=pu$X p origin HEAD:main' HEAD~1",
    "ATK-35": "Q=sh git rebase -x 'git pu$Q origin HEAD:main' HEAD~1",
    "ATK-36": "git rebase -x 'git `echo pu`sh origin HEAD:main' HEAD~1",
    "ATK-37": "$'git' push origin HEAD:main",
    "ATK-38": "echo feature:main | xargs git push origin feature:feature",
    "ATK-39": "git push origin 'feature:ma''in'",
    "ATK-40": 'g""it push origin HEAD:main',
    "ATK-41": "\\git push origin HEAD:main",
    "ATK-45": "git --attr-source HEAD push origin HEAD:main",
    "ATK-50": 'bash -c "git push origin HEAD:main"',
    "ATK-57": "git rebase -x 'G=gi; ${G}t push origin HEAD:main' HEAD~1",
    "NATK-1": "gi\\\nt push origin HEAD:main",
    "NATK-2": 'bash -c "gi\\\nt push origin HEAD:main"',
    "NATK-3": "git$'' push origin HEAD:main",
    "NATK-4": 'g$""it push origin HEAD:main',
    "NATK-5": "if true; then git send-pack {R} HEAD:refs/heads/main; fi",
    "NATK-6": "find . -maxdepth 0 -exec git send-pack {R} HEAD:refs/heads/main \\;",
    "NATK-11": "timeout -s KILL 30 git send-pack {R} HEAD:refs/heads/main",
    "NATK-12": "git rebase -x 'git send-pack {R} HEAD:refs/heads/main' HEAD~1",
    "NATK-13": "taskset -c 0 git send-pack {R} HEAD:refs/heads/main",
    "NATK-15": "git$'' -c x.y=z push origin HEAD:main",
}


def test_cor2_replay_real_attacks(tmp_path):
    # T-COR-2: the guard runs first on each command and only a command it allows
    # is executed, in a clone of a bare remote under tmp_path (never a real one).
    git = shutil.which("git")
    if git is None:
        pytest.skip("git is not installed")
    remote, clone = tmp_path / "remote.git", tmp_path / "clone"
    env = {
        "HOME": str(tmp_path / "githome"),
        "PATH": os.environ.get("PATH", ""),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@t",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@t",
    }

    def sh(command, cwd=clone):
        return subprocess.run(
            [BASH, "-c", command], cwd=cwd, env=env, capture_output=True, timeout=30
        )

    def refs():
        out = subprocess.run(
            [git, "--git-dir", str(remote), "for-each-ref"],
            env=env,
            capture_output=True,
            check=True,
            timeout=30,
        )
        return out.stdout.decode()

    def commit(name):
        (clone / name).write_text(name)
        assert sh(f"git add {name} && git commit -q -m {name}").returncode == 0

    clone.mkdir()
    assert sh(f"git init -q --bare {remote}", cwd=tmp_path).returncode == 0
    assert sh(f"git init -q -b main && git remote add origin {remote}").returncode == 0
    commit("a")
    assert sh("git push -q origin main").returncode == 0
    assert sh("git checkout -q -b feature").returncode == 0
    commit("b")
    assert sh("git push -q origin feature").returncode == 0
    commit("c")
    before = refs()
    assert "refs/heads/main" in before and "refs/heads/feature" in before

    for row_id, command in COR2_ATTACKS.items():
        command = command.replace("{R}", str(remote))
        for level in LEVEL_ORDER:
            guard = tmp_path / "guard" / f"{row_id}-{level}"
            _bind(guard, *LEVEL_FILES[level])
            result = _run(_bash(command), guard)
            if result.returncode == 0:
                sh(command)
            assert result.returncode == 2, (row_id, level)
            assert refs() == before, (row_id, level)

    # The permitted canonical push: blocked below FS, allowed and real at FS.
    for level in LEVEL_ORDER:
        guard = tmp_path / "guard" / f"permitted-{level}"
        _bind(guard, *LEVEL_FILES[level])
        result = _run(_bash("git push origin feature"), guard)
        assert result.returncode == (0 if level == "FS" else 2), level
        if level == "FS":
            assert sh("git push -q origin feature").returncode == 0
    head = sh("git rev-parse HEAD").stdout.decode().strip()
    after = refs()
    assert after != before
    assert f"{head} commit\trefs/heads/feature" in after
    main = [line for line in before.splitlines() if line.endswith("refs/heads/main")]
    assert main and main[0] in after.splitlines()


# --- Task 17: gh api writes, tamper, escape, benign, N-ATK, messages, AC map --
#
# Expected results are written by hand from design sections 4, 5 and 10 (DD-2),
# not copied from the MR corpus columns; every row below agrees with MR section
# 8.3/8.4 (no "override:" was needed). The leaks N-ATK-31 and 36, the git rows
# N-ATK-1 to 19 and 37, T-OVR-1 to 6 and the git/gh T-OK rows are in Task 16.

CORPUS17 = [
    # gh api writes (H2: method, field, graphql or a non-plain form).
    ("ATK-6", "gh api --method=POST repos/o/r/merges", GHWRITE),
    ("ATK-18", "X=X; gh api repos/o/r/git/refs/heads/main -$X DELETE", GHWRITE),
    ("ATK-47", "gh api graphql -f query='mutation{mergePullRequest}'", GHWRITE),
    # Tamper and escape.
    ("ATK-21", f"rm -rf {STATE_PATH}", TAMPER),
    ("ATK-55", "cd ~/.cla" + "ude && rm -rf state", TAMPER),
    ("ATK-60", "claude \\\n-p x", ESCAPE),
    # Benign rows without git or gh (T-OK-14 is the Edit row below).
    ("OK-10", "uv run pytest", NONE4),
    ("OK-11", "make sync-dev", NONE4),
    ("OK-13", "cat README.md", NONE4),
    ("OK-35", "grep -rn claude docs/", NONE4),
    ("OK-36", "grep claude -rn docs/", NONE4),
    # Amendment attacks not in Task 16.
    ("NATK-20", "X=ge; flock /tmp/l gh pr mer$X 5", UNK),
    ("NATK-21", "if :; then gh repo sync; fi", MERGE),
    ("NATK-22", "if :; then gh pr update-branch 5; fi", MERGE),
    ("NATK-23", "g$''h pr merge 5", MERGE),
    (
        "NATK-24",
        "flock /tmp/l gh a$''pi -X DELETE repos/o/r/git/refs/heads/main",
        GHWRITE,
    ),
    ("NATK-25", "g\\\nh pr merge 5", UNK),
    # H5: `$(` ends the segment, so the api.github.com word has no gh word.
    (
        "NATK-26",
        'curl -sS -X PATCH -H "Authorization: token $(gh auth token)" '
        "https://api.github.com/repos/o/r/git/refs/heads/main "
        '-d \'{"sha":"abc","force":true}\'',
        GHWRITE,
    ),
    ("NATK-27", 'npx -y @anthropic-ai/claude-code@latest -p "finish the task"', ESCAPE),
    ("NATK-28", 'cl\\\naude -p "finish the task"', UNK),
    # NM1a comes first; the split word names no tamper path.
    ("NATK-29", "rm -rf ~/.cla\\\nude/state", UNK),
    ("NATK-30", "rm -rf ~/.cla$''ude/state", TAMPER),
    ("NATK-32", "cp /tmp/s.json ~/.cla" + "ude/set$''tings.json", TAMPER),
    ("NATK-33", ": > ~/.cla" + "ude/hoo$''ks/launch-level-guard.sh", TAMPER),
    ("NATK-34-tmux", "tm\\\nux send-keys approved Enter", UNK),
    ("NATK-34-orca", "or\\\nca terminal send --terminal t1 --text approved", UNK),
    ("NATK-35", "if :; then gh alias set mm 'pr merge'; fi", UNK),
    ("NATK-38", "uv run python -m superclaude.cli.main install", TAMPER),
    # Design section 10, rows not yet in Task 16 (or restated as a Task 17 row).
    (
        "EDGE17-title-fs",
        "gh pr create --repo o/r --base master --head f "
        '--title "docs: explain git hooks" --body-file /tmp/b',
        SUBMIT,
    ),
    (
        "EDGE17-pr-body",
        'gh pr create --repo o/r --title x --body "this pull request names git"',
        MERGE,
    ),
    ("EDGE17-orca-continuation", "orca \\\nworktree list", ESCAPE),
    ("EDGE17-scope", 'git commit -m "fix(ccsession): handle tags"', ESCAPE),
    ("EDGE17-multibyte-big", "echo " + "é" * 32766, ("LL-BIG",) * 4),
]
assert len({row[0] for row in CORPUS17}) == len(CORPUS17), "duplicate corpus id"
assert len({r[0]: r[1] for r in CORPUS17}["EDGE17-multibyte-big"].encode()) == 65537


@pytest.mark.parametrize(
    "command, level, msg_id",
    [
        pytest.param(command, level, msg_id, id=f"{row_id}-{level}")
        for row_id, command, ids in CORPUS17
        for level, msg_id in zip(LEVEL_ORDER, ids)
    ],
)
def test_corpus17(tmp_path, command, level, msg_id):
    # T-COR-1, Task 17 rows; LL-TEXT follows every Bash block.
    _git_case(tmp_path, command, level, msg_id)


PAYLOADS17 = [
    ("OK-14", _edit("Edit", "/repo/src/superclaude/x.py"), NONE4),
    # FR-L-51: contents are never checked, only the path.
    (
        "EDGE17-write-quote",
        _edit("Write", "/repo/docs/notes.md", content="see ~/.cla" + "ude/hooks/x.sh"),
        NONE4,
    ),
    (
        "EDGE17-monitor-ws",
        _tool("Monitor", ws={"url": "wss://example.test/feed"}, timeout_ms=5000),
        NONE4,
    ),
]


@pytest.mark.parametrize(
    "payload, level, msg_id",
    [
        pytest.param(payload, level, msg_id, id=f"{row_id}-{level}")
        for row_id, payload, ids in PAYLOADS17
        for level, msg_id in zip(LEVEL_ORDER, ids)
    ],
)
def test_corpus17_other_tools(tmp_path, payload, level, msg_id):
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(payload, tmp_path)
    _assert_decision(result, tmp_path, msg_id, level, text=_text_note(payload, msg_id))


# T-MSG-1 to T-MSG-3: one oracle payload per message id, run through the real
# script (the printer-only route is test_every_message_prints_the_design_text).
MSG_CASES = {
    "LL-IMPL": ("W", _skill("sc:implement")),
    "LL-COMMIT": ("W", _bash("git commit -m x")),
    "LL-PUSH": ("W", _bash("git push origin feature")),
    "LL-PUSH-FORM": ("FS", _bash("git push --force origin f")),
    "LL-PROTECTED": ("W", _bash("git push origin main")),
    "LL-MERGE": ("W", _bash("gh pr merge 5")),
    "LL-GH-WRITE": ("W", _bash("gh api graphql")),
    "LL-SUBMIT": ("W", _skill("sc:pr-submit")),
    "LL-REPO": ("FS", _bash("gh pr create --title x")),
    "LL-UNKNOWN": ("W", _bash("git ci")),
    "LL-MCP": ("W", _tool("mcp__github__push_files")),
    "LL-ESCAPE": ("W", _tool("Workflow")),
    "LL-TURN": ("W", _tool("CronCreate", prompt="approved")),
    "LL-TAMPER": ("W", _edit("Edit", "~/.cla" + "ude/settings.json")),
    "LL-SKILL": ("W", _skill("")),
    "LL-BIG": ("W", _bash("echo " + "y" * 70_000)),
    "LL-BROKEN": ("F", {"hook_event_name": "PostToolUse", "session_id": SID}),
    # No record and no binding: the level is unknown, so the bare header.
    "LL-NOBIND": (None, _prompt("Example: " + _marker() + " plan")),
}
assert sorted(MSG_CASES) == sorted(IDS), "message id without an oracle payload"


def _msg_run(tmp_path, msg_id):
    level, payload = MSG_CASES[msg_id]
    if level is not None:
        _bind(tmp_path, *LEVEL_FILES[level])
    return level, payload, _run(payload, tmp_path)


@pytest.mark.parametrize("msg_id", IDS)
def test_every_message_has_header_and_three_lines(tmp_path, msg_id):
    # T-MSG-1: header, then Blocked:, Why:, You can:, then only Note: lines.
    level, _payload, result = _msg_run(tmp_path, msg_id)
    assert result.returncode == 2 and result.stdout == b""
    lines = result.stderr.decode().splitlines()
    header = HEADER.format(level=LEVELS[level]) if level else "Launch-level guard:"
    assert lines[0] == header
    assert [line.split(" ", 2)[0] for line in lines[1:3]] == ["Blocked:", "Why:"]
    assert lines[3].startswith("You can: ")
    assert all(line.startswith("Note: ") for line in lines[4:])


@pytest.mark.parametrize("msg_id", IDS)
def test_every_message_id_reachable(tmp_path, msg_id):
    # T-MSG-2: the payload produces exactly its id's design text.
    level, payload, result = _msg_run(tmp_path, msg_id)
    if level is None:
        assert (result.returncode, result.stdout) == (2, b"")
        assert result.stderr.decode() == _nobind(tmp_path)
        return
    text = payload.get("tool_name") in ("Bash", "Monitor")
    _assert_decision(result, tmp_path, msg_id, level, text=text)


@pytest.mark.parametrize("msg_id", IDS)
def test_no_unresolved_template_variables(tmp_path, msg_id):
    # T-MSG-3
    _level, _payload, result = _msg_run(tmp_path, msg_id)
    out = result.stderr.decode()
    assert out and not re.search(r"\{(level|store|sid)\}", out)


# T-MSG-4: competing classes in one call; the higher class names the message.
PRECEDENCE = [
    ("tamper-over-merge", "git merge x; cat ~/.cla" + "ude/settings.json", TAMPER),
    ("merge-over-ghwrite", "gh api graphql; gh pr merge 5", MERGE),
    ("submit-over-repo", "gh pr create --title x", SUBMIT_REPO),
    ("push-over-pushform", "git push --force origin f", PUSHFORM),
    ("protected-over-push", "git push origin main", PROTECTED),
]


@pytest.mark.parametrize(
    "command, level, msg_id",
    [
        pytest.param(command, level, msg_id, id=f"MSG4-{case_id}-{level}")
        for case_id, command, ids in PRECEDENCE
        for level, msg_id in zip(LEVEL_ORDER, ids)
    ],
)
def test_precedence_order(tmp_path, command, level, msg_id):
    _git_case(tmp_path, command, level, msg_id)


@pytest.mark.parametrize(
    "level, rendering",
    [
        ("W", "worktree"),
        ("WA", "worktree (approved)"),
        ("F", "full"),
        ("FS", "full --submit"),
    ],
)
def test_level_rendered_in_header(tmp_path, level, rendering):
    # T-MSG-5: the four renderings, typed here, through the real script.
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(_tool("mcp__github__merge_pull_request"), tmp_path)
    assert result.returncode == 2
    first = result.stderr.decode().splitlines()[0]
    assert first == (
        "Launch-level guard: this session was started by /sc:issue --claim"
        f" at level {rendering}."
    )


@pytest.mark.parametrize(
    "payload, msg_id",
    [
        pytest.param(_skill("sc:implement"), "LL-IMPL", id="skill"),
        pytest.param(_bash("git commit -m x"), "LL-COMMIT", id="bash"),
        pytest.param(_bash("gh pr merge 5", tool="Monitor"), "LL-MERGE", id="monitor"),
        pytest.param(
            _edit("Edit", "~/.cla" + "ude/hooks/x.sh"), "LL-TAMPER", id="edit"
        ),
        pytest.param(_tool("mcp__github__merge_pull_request"), "LL-MERGE", id="mcp"),
        pytest.param(_tool("Agent", isolation="remote"), "LL-ESCAPE", id="agent"),
        pytest.param(_bash("git status"), None, id="allowed-bash"),
    ],
)
def test_state_and_text_notes(tmp_path, payload, msg_id):
    # T-MSG-6: a degraded session gets LL-STATE on every block (first), LL-TEXT
    # only on a Bash or Monitor block, and an allowed call stays silent.
    _bind(tmp_path, "garbage")
    result = _run(payload, tmp_path)
    text = _text_note(payload, msg_id)
    _assert_decision(result, tmp_path, msg_id, "W", note=msg_id is not None, text=text)


@pytest.mark.parametrize("missing", ["tr", "sed"])
def test_internal_error_prints_broken(tmp_path, missing):
    # T-FC-3: PATH without tr, then without sed, governed Bash: LL-BROKEN.
    bindir = tmp_path / "bin"
    bindir.mkdir()
    for tool in ("cat", "sed", "tr", "mkdir", "mv", "ln", "rm", "jq"):
        if tool != missing:
            (bindir / tool).symlink_to(shutil.which(tool))
    _bind(tmp_path, "full")
    result = _run(_bash("git status"), tmp_path)
    assert result.returncode == 2 and result.stdout == b""
    # bash's own "command not found" line comes first; the message is the rest.
    store = str(_store(tmp_path / "home"))
    expected = _expected("LL-BROKEN", "full", SID, store)
    out = result.stderr.decode()
    assert out.endswith("\n" + expected) and f"{missing}: command not found" in out


# Design section 11 acceptance map: each AC lists the cases that must exist.
# Ids are kept as (family, number) so this table never matches its own search.
AC_MAP = {
    "AC-1": [("GRID", 3), ("SKL", 1), ("APR", 5), ("APR", 9), ("NRM", 8), ("GIT", 18)],
    "AC-2": [
        ("GRID", 4),
        ("GRID", 5),
        ("GIT", 17),
        ("PSH", 8),
        ("PSH", 11),
        ("GH", 12),
    ],
    "AC-3": [("APR", n) for n in (1, 2, 3, 4, 10)] + [("TRN", 1), ("TRN", 4)],
    "AC-4": [("ISO", n) for n in (1, 4, 7, 8, 9)] + [("REG", 3)],
    "AC-5": [("BIND", 2), ("BIND", 7), ("BIND", 13)]
    + [("TAM", n) for n in (1, 2, 6)]
    + [("FC", 2)],
    "AC-6": [("PSH", 4), ("PSH", 12), ("GIT", 9), ("GIT", 14), ("NRM", 1)]
    + [("GH", 2), ("GH", 11), ("GH", 14), ("MCP", 1), ("COR", 2)],
    "AC-7": [("MSG", 1), ("MSG", 2), ("MSG", 3), ("FC", 3)],
    "AC-8": [("GRID", 1), ("GRID", 2)]
    + [("SPD", n) for n in range(1, 6)]
    + [("COR", 1), ("GAP", 1)],
}
# T-REG-3 (the hooks.json matcher) is an unlabelled test in the registration
# module; it is located by its function name instead of a label.
AC_LOCATED = {
    ("REG", 3): (
        "test_launch_level_guard_registration.py",
        "def test_matcher_matches_the_guarded_tools_and_not_the_others(",
    ),
}


@pytest.mark.parametrize("ac", sorted(AC_MAP))
def test_acceptance_map_cases_present(ac):
    source = Path(__file__).read_text()
    missing = []
    for fam, n in AC_MAP[ac]:
        if (fam, n) in AC_LOCATED:
            name, needle = AC_LOCATED[(fam, n)]
            if needle not in (Path(__file__).parent / name).read_text():
                missing.append((fam, n))
        elif not re.search(rf"T-{fam}-{n}(?!\d)", source):
            missing.append((fam, n))
    assert not missing, (ac, missing)
