"""Behavioral tests for block-bare-python.sh (issue #357).

The hook is a PreToolUse(Bash) gate: it blocks (exit 2, message on stderr) a
command that runs bare python, python3, pip or pip3 as a command word, allows
everything else (exit 0), and fails open (exit 0) on any input it cannot judge.
Each case runs the real script with a JSON payload on stdin and HOME inside
tmp_path, like tests/hooks/test_freshness_pre_edit_create_case.py.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest

HOOK = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "superclaude"
    / "hooks"
    / "scripts"
    / "block-bare-python.sh"
)
BASH = shutil.which("bash") or "/bin/bash"


def _run(stdin: bytes, home: Path, env_path: str | None = None):
    env = os.environ.copy()
    env["HOME"] = str(home)
    if env_path is not None:
        env["PATH"] = env_path
    started = time.monotonic()
    result = subprocess.run(
        [BASH, str(HOOK)], input=stdin, capture_output=True, env=env, timeout=10
    )
    return result, time.monotonic() - started


def _bash(command: str) -> bytes:
    return json.dumps(
        {"tool_name": "Bash", "tool_input": {"command": command}}
    ).encode()


BLOCKED = {
    # Plan Task 2 blocked list.
    "python3-c": "python3 -c 1",
    "python-script": "python script.py",
    "pip-install": "pip install requests",
    "pip3-install": "pip3 install x",
    "abs-python3": "/usr/bin/python3 -V",
    "venv-python": ".venv/bin/python -m pytest",
    "and-chain": "cd /tmp && python3 x.py",
    "semicolon-chain": "ls; python3 x.py",
    "pipe-issue-command": "echo '{}' | python3 -c 'import sys,json; json.load(sys.stdin)'",
    "or-chain": "false || pip install x",
    "background": "make build & python3 x.py",
    "second-line": "echo first\npython3 x.py",
    "dollar-subst": "echo $(python3 -c 1)",
    "backtick-subst": "echo `python3 -c 1`",
    "subshell": "(python3 x.py)",
    "if-condition": "if python3 -c 1; then echo ok; fi",
    "for-body": 'for f in *.py; do python3 "$f"; done',
    "assignment-prefix": "FOO=1 python3 x.py",
    "env-wrapper": "env FOO=1 python3 x.py",
    "sudo-wrapper": "sudo pip install x",
    "timeout-wrapper": "timeout 30 python3 x.py",
    "nohup-wrapper": "nohup python3 x.py",
    "exec-wrapper": "exec python3 x.py",
    # Amendments AMD-03/AMD-04/AMD-05 (reflect invariant probe E-cases).
    "quoted-dollar-subst": 'x="$(python3 -c 1)"',
    "quoted-backtick-subst": 'x="`python3 -c 1`"',
    "nested-quoted-subst": 'echo "$(echo "$(python3 -c 1)")"',
    "comment-then-python3": "# note\npython3 x.py",
    "apostrophe-comment-then-python3": "# don't do this\npython3 x.py",
    "comment-backslash-no-continuation-E1": "echo a # C:\\\npython3 E1",
    "unquoted-heredoc-apostrophe-E3": "cat <<EOF\ndon't\nEOF\npython3 E3",
    "unquoted-heredoc-subst-E4": "cat <<EOF\nv=$(python3 E4)\nEOF",
    "tab-stripped-heredoc-E5": "cat <<-'EOF'\n\tbody\n\tEOF\npython3 E5",
    "here-string-E6": "cat <<< '{}'\npython3 E6",
    "quoted-heredoc-apostrophe": "cat > notes.md <<'EOF'\nit's text\nEOF\npython3 x.py",
    "redirect-first-E7": "< in.json python3 E7",
    "redirect-out-first-E8": ">out.txt python3 E8",
    "double-quoted-word-E9": '"python3" E9',
    "single-quoted-word-E9b": "'python3' E9b",
    "backslash-word-E9c": "\\python3 E9c",
    "quoted-path-word-E10": '"$PWD/bin/python3" E10',
    "ansi-c-quote-E11": "printf %s $'don\\'t'; python3 E11",
    "subst-in-assignment-E13": "PYTHONPATH=$(pwd)/src python3 E13",
    "arith-in-subst-E15": 'echo "$(echo $((1+2)) )"; python3 E15',
    "continuation": "FOO=1 \\\n  python3 x.py",
    "shell-heredoc": "bash <<'EOF'\npython3 x.py\nEOF",
    "sudo-user-option": "sudo -u bob python3 x.py",
    "nice-n-option": "nice -n 10 python3 x.py",
    "env-path-form": "/usr/bin/env python3 x.py",
    "function-body": "f() { python3 x.py; }",
    "case-body": "case $x in a) python3 x.py;; esac",
    "process-subst": "diff <(python3 a.py) b.txt",
}

ALLOWED = {
    # Plan Task 2 allowed list.
    "uv-run-python": "uv run python -c 1",
    "uv-run-no-project": "uv run --no-project python x.py",
    "uv-pip": "uv pip install requests",
    "uvx": "uvx ruff check .",
    "and-uv": "cd /tmp && uv run python x.py",
    "grep-pattern": "grep -rn python3 src/",
    "rg-quoted": "rg 'pip install' docs/",
    "path-arg": "ls src/python3/lib",
    "file-arg": "cat requirements-python.txt",
    "echo-double-quoted": 'echo "python3 -c 1"',
    "echo-single-quoted": "echo 'pip install x'",
    "commit-message": 'git commit -m "stop calling python3 directly"',
    "bash-c-string": 'bash -c "python3 x.py"',
    "command-v": "command -v python3",
    "which": "which pip",
    "type": "type python3",
    "pipe-jq": "jq . file.json | head",
    "read-parse-line": (
        "seekable=$(uv run --no-project python -c "
        "\"import os;f=os.open('$NODE',0);os.lseek(f,1,0);print(1)\" 2>/dev/null||echo 0)"
    ),
    # Amendment AMD-02: allowed `;`-chained cases.
    "semicolon-uv": "ls; uv run python x.py",
    "semicolon-echo-mention": "echo a; echo python3",
    "and-then-mention": "uv run python a.py && echo python3",
    # Amendments AMD-03/AMD-05.
    "subst-path-arg-E12": "ls -d $(pwd)/bin/python3",
    "multiline-commit-heredoc": (
        "git commit -m \"$(cat <<'EOF'\n"
        'fix(hooks): block "echo x | python3 -c" calls\n'
        "\n"
        "Use `uv run python` instead of python3.\n"
        "EOF\n"
        ')"'
    ),
    "uv-continuation": "uv run --no-project \\\n  python x.py",
    "comment-mention": "# don't call python3 (use uv)\nuv run python x.py",
    "array-assignment": "arr=(python3 pip); echo ${#arr[@]}",
    "quoted-heredoc-text": "cat > notes.md <<'EOF'\nRun `python3 x.py` to reproduce (pip; too)\nEOF",
    "here-string-mention": 'jq . <<< \'{"cmd": "python3 x"}\'',
}


@pytest.mark.parametrize("command", BLOCKED.values(), ids=BLOCKED.keys())
def test_blocked(command: str, tmp_path: Path) -> None:
    result, _ = _run(_bash(command), tmp_path)
    assert result.returncode == 2, result.stderr.decode()
    stderr = result.stderr.decode()
    assert stderr.startswith("UV-ONLY BLOCK:")
    assert "uv run python" in stderr
    assert "jq" in stderr


@pytest.mark.parametrize("command", ALLOWED.values(), ids=ALLOWED.keys())
def test_allowed(command: str, tmp_path: Path) -> None:
    result, _ = _run(_bash(command), tmp_path)
    assert result.returncode == 0, result.stderr.decode()
    assert result.stderr == b""


FAIL_OPEN = {
    "non-json": b"this is not json",
    "empty-stdin": b"",
    "read-tool": json.dumps(
        {"tool_name": "Read", "tool_input": {"file_path": "python3"}}
    ).encode(),
    "bash-no-command": json.dumps({"tool_name": "Bash", "tool_input": {}}).encode(),
    "bash-empty-command": _bash(""),
}


@pytest.mark.parametrize("stdin", FAIL_OPEN.values(), ids=FAIL_OPEN.keys())
def test_fail_open(stdin: bytes, tmp_path: Path) -> None:
    result, _ = _run(stdin, tmp_path)
    assert result.returncode == 0, result.stderr.decode()


def test_fail_open_when_jq_missing(tmp_path: Path) -> None:
    """jq absent from PATH: exit 0 and the jq-branch-only marker (AMD-07)."""
    empty_bin = tmp_path / "bin"
    empty_bin.mkdir()
    result, _ = _run(_bash("python3 -c 1"), tmp_path, env_path=str(empty_bin))
    assert result.returncode == 0
    assert b"block-bare-python: jq not found" in result.stderr


def _long_command(size: int) -> str:
    chunk = "echo " + "a" * 75 + "; "
    return chunk * (size // len(chunk)) + "python3 x.py"


def test_100kb_command_blocked_under_one_second(tmp_path: Path) -> None:
    command = _long_command(100_000)
    assert len(command) >= 99_000
    result, elapsed = _run(_bash(command), tmp_path)
    assert result.returncode == 2, result.stderr.decode()
    assert elapsed < 1


def test_200kb_command_on_stdin_blocked(tmp_path: Path) -> None:
    """Above the 128 KB single-argument limit: the command must still be scanned (AMD-06)."""
    command = _long_command(200_000)
    assert len(command) > 131_072
    result, _ = _run(_bash(command), tmp_path)
    assert result.returncode == 2, result.stderr.decode()
