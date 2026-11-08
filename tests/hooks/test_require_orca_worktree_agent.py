"""Behavioral tests for require-orca-worktree-agent.sh.

The hook is a PreToolUse(Bash) gate: it blocks (exit 2, message on stderr) a
command that runs `orca worktree create` without `--agent`, allows everything
else (exit 0), and fails open (exit 0) on any input it cannot judge. Each case
runs the real script with a JSON payload on stdin and HOME inside tmp_path,
like tests/hooks/test_block_bare_python.py.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest

HOOK = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "superclaude"
    / "hooks"
    / "scripts"
    / "require-orca-worktree-agent.sh"
)
BASH = shutil.which("bash") or "/bin/bash"

BLOCK_MESSAGE = (
    "ORCA WORKTREE BLOCK: every Orca worktree gets an agent, and this command runs "
    "`orca worktree create` without `--agent`.\n"
    'Use: orca worktree create --name <name> --agent claude --prompt "<task>"\n'
    "The session that creates the worktree becomes its orchestrator (or a "
    "coordinator under another orchestrator) and owns that agent.\n"
    "Supervised workers use `orca orchestration worker-start`.\n"
)


def _run(stdin: bytes, home: Path, env_path: str | None = None):
    env = os.environ.copy()
    env["HOME"] = str(home)
    if env_path is not None:
        env["PATH"] = env_path
    return subprocess.run(
        [BASH, str(HOOK)], input=stdin, capture_output=True, env=env, timeout=10
    )


def _bash(command: str) -> bytes:
    return json.dumps(
        {"tool_name": "Bash", "tool_input": {"command": command}}
    ).encode()


BLOCKED = {
    "bare-create": "orca worktree create --name x",
    "create-with-other-flags": 'orca worktree create --name x --prompt "do it"',
    "after-cd-and": "cd /x && orca worktree create --name x",
    "dollar-subst": "echo $(orca worktree create --name x)",
    "backtick-subst": "echo `orca worktree create --name x`",
    "abs-path": "/usr/local/bin/orca worktree create --name x",
    "env-wrapper": "env X=1 orca worktree create --name x",
    "sudo-wrapper": "sudo orca worktree create --name x",
    "command-wrapper": "command orca worktree create --name x",
    "after-pipe": "echo a | orca worktree create --name x",
    "second-line": "echo first\norca worktree create --name x",
    "after-comment-line": "# note\norca worktree create --name x",
    "agent-first-bare-second": (
        "orca worktree create --name a --agent claude --prompt t ; "
        "orca worktree create --name b"
    ),
    "bare-first-agent-second": (
        "orca worktree create --name b ; "
        "orca worktree create --name a --agent claude --prompt t"
    ),
    "agent-in-other-command": "echo --agent ; orca worktree create --name x",
    "inner-bare-in-agent-command": (
        "orca worktree create --name $(orca worktree create --name y) --agent claude"
    ),
    "inner-bare-in-quoted-subst": (
        'orca worktree create --name x --agent claude --prompt "$(orca worktree create --name y)"'
    ),
    "subshell": "(orca worktree create --name x)",
    "if-condition": "if orca worktree create --name x; then echo ok; fi",
    "or-chain": "false || orca worktree create --name x",
    "background": "make build & orca worktree create --name x",
    "assignment-prefix": "ORCA_X=1 orca worktree create --name x",
    "redirect-after": "orca worktree create --name x > out.txt",
    "continuation": "orca worktree \\\n  create --name x",
    "global-option-first": "orca --json worktree create --name x",
    "shell-heredoc": "bash <<'EOF'\norca worktree create --name x\nEOF",
    # PR #449 review: a command word built by a substitution or a variable.
    "subst-command-word": "$(printf orca) worktree create --name x",
    "variable-command-word": "$ORCA worktree create --name x",
    "braced-variable-command-word": "${ORCA:-orca} worktree create --name x",
    "subst-command-word-after-chain": "cd /x && $(printf orca) worktree create --name x",
}

ALLOWED = {
    "subst-command-word-with-agent": (
        "$(printf orca) worktree create --name x --agent claude --prompt t"
    ),
    "variable-command-word-other-command": "$EDITOR notes.md",
    "subst-command-word-other-args": "$(which jq) --version",
    "create-with-agent": "orca worktree create --name x --agent claude --prompt t",
    "create-with-agent-equals": "orca worktree create --name x --agent=claude",
    "create-help": "orca worktree create --help",
    "create-short-help": "orca worktree create -h",
    "worktree-list": "orca worktree list",
    "list-name-create": "orca worktree list --name create",
    "worktree-rm": "orca worktree rm --worktree name:x",
    "terminal-list": "orca terminal list --worktree path:/x --json",
    "orchestration-worker-start": "orca orchestration worker-start --name x",
    "quoted-echo": 'echo "orca worktree create"',
    "single-quoted-echo": "echo 'orca worktree create --name x'",
    "commit-message": 'git commit -m "block orca worktree create without --agent"',
    "grep-pattern": "grep -rn 'orca worktree create' docs/",
    "comment-mention": "# orca worktree create is blocked\nls",
    "quoted-heredoc-text": "cat > notes.md <<'EOF'\nrun orca worktree create --name x\nEOF",
    "bash-c-ceiling": 'bash -c "orca worktree create --name x"',
    "command-v": "command -v orca",
    "agent-after-chain": "cd /x && orca worktree create --name x --agent claude --prompt t",
}


@pytest.mark.parametrize("command", BLOCKED.values(), ids=BLOCKED.keys())
def test_blocked(command: str, tmp_path: Path) -> None:
    result = _run(_bash(command), tmp_path)
    assert result.returncode == 2, result.stderr.decode()
    assert result.stdout == b""
    assert result.stderr.decode() == BLOCK_MESSAGE


@pytest.mark.parametrize("command", ALLOWED.values(), ids=ALLOWED.keys())
def test_allowed(command: str, tmp_path: Path) -> None:
    result = _run(_bash(command), tmp_path)
    assert result.returncode == 0, result.stderr.decode()
    assert result.stdout == b""
    assert result.stderr == b""


FAIL_OPEN = {
    "non-json": b"this is not json",
    "empty-stdin": b"",
    "read-tool": json.dumps(
        {"tool_name": "Read", "tool_input": {"file_path": "orca worktree create"}}
    ).encode(),
    "bash-no-command": json.dumps({"tool_name": "Bash", "tool_input": {}}).encode(),
    "bash-empty-command": _bash(""),
}


@pytest.mark.parametrize("stdin", FAIL_OPEN.values(), ids=FAIL_OPEN.keys())
def test_fail_open(stdin: bytes, tmp_path: Path) -> None:
    result = _run(stdin, tmp_path)
    assert result.returncode == 0, result.stderr.decode()


def _bin_with(tmp_path: Path, names: list[str]) -> Path:
    """A PATH directory that holds only the named real tools."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in names:
        real = shutil.which(name)
        assert real, f"{name} is needed on the test host"
        (bin_dir / name).symlink_to(real)
    return bin_dir


def test_fail_open_when_jq_missing(tmp_path: Path) -> None:
    bin_dir = _bin_with(tmp_path, ["awk", "cat"])
    result = _run(_bash("orca worktree create --name x"), tmp_path, str(bin_dir))
    assert result.returncode == 0
    assert b"require-orca-worktree-agent: jq not found" in result.stderr


def test_fail_open_when_awk_missing(tmp_path: Path) -> None:
    bin_dir = _bin_with(tmp_path, ["jq", "cat"])
    result = _run(_bash("orca worktree create --name x"), tmp_path, str(bin_dir))
    assert result.returncode == 0
    assert b"require-orca-worktree-agent: awk not found" in result.stderr


def test_fail_open_when_scanner_fails(tmp_path: Path) -> None:
    """An awk that prints the verdict word but exits non-zero must not block."""
    bin_dir = _bin_with(tmp_path, ["jq", "cat"])
    fake_awk = bin_dir / "awk"
    fake_awk.write_text("#!/bin/sh\necho orca\nexit 3\n")
    fake_awk.chmod(fake_awk.stat().st_mode | stat.S_IXUSR)
    result = _run(_bash("orca worktree create --name x"), tmp_path, str(bin_dir))
    assert result.returncode == 0, result.stderr.decode()
    assert result.stderr == b""


def test_script_is_executable_and_runs_no_python() -> None:
    assert os.access(HOOK, os.X_OK)
    text = HOOK.read_text()
    code = [ln for ln in text.splitlines() if not ln.lstrip().startswith("#")]
    assert not any(w in ("python", "python3", "uv") for ln in code for w in ln.split())
