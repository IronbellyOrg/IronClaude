"""``run-ledger-record.sh`` run with bash, a stubbed PATH and the Task 8 fixtures.

Marked ``integration``: the script is a real process (the autouse guard of ``conftest.py``
lets only such tests start one). No real ``superclaude`` or Orca is involved.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "src/superclaude/hooks/scripts/run-ledger-record.sh"
FIXTURES = Path(__file__).parent / "fixtures"
FIXTURE_ID = "run_e97be8837462"
TOOLS = ("jq", "cat", "grep", "head", "date", "mkdir", "bash")


def make_path(tmp_path: Path, with_superclaude: bool) -> tuple[Path, Path]:
    """A PATH folder holding only the tools the script needs, plus a recording `superclaude` stub."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for tool in TOOLS:
        os.symlink(shutil.which(tool), bin_dir / tool)
    record = tmp_path / "superclaude-args.txt"
    if with_superclaude:
        stub = bin_dir / "superclaude"
        stub.write_text(f'#!/usr/bin/env bash\necho "$@" >> "{record}"\n')
        stub.chmod(0o755)
    return bin_dir, record


def run_hook(tmp_path, payload, with_superclaude=True, raw=None, extra_env=None):
    bin_dir, record = make_path(tmp_path, with_superclaude)
    env = {
        "PATH": str(bin_dir),
        "HOME": str(tmp_path / "home"),
        "XDG_STATE_HOME": str(tmp_path / "state"),
        **(extra_env or {}),
    }
    stdin = raw if raw is not None else json.dumps(payload)
    proc = subprocess.run(
        [str(shutil.which("bash")), str(SCRIPT)],
        input=stdin,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    calls = record.read_text().splitlines() if record.exists() else []
    return proc, calls, tmp_path / "state" / "superclaude" / "run-ledger-hook.log"


def bash_payload(command: str, stdout: str = "", tool_name: str = "Bash") -> dict:
    return {
        "hook_event_name": "PostToolUse",
        "tool_name": tool_name,
        "tool_input": {"command": command},
        "tool_response": {
            "stdout": stdout,
            "stderr": "",
            "interrupted": False,
            "isImage": False,
        },
    }


@pytest.mark.integration
def test_hook_extracts_run_id_from_fixture(tmp_path):
    payload = json.loads((FIXTURES / "posttooluse_run_create.json").read_text())
    proc, calls, log = run_hook(tmp_path, payload)
    assert (proc.returncode, proc.stdout, proc.stderr) == (0, "", "")
    assert calls == [f"sweep ledger --add {FIXTURE_ID}"]
    assert not log.exists()


@pytest.mark.integration
def test_hook_worker_start_prefers_the_run_flag_and_string_responses_work(tmp_path):
    command = (
        "orca orchestration worker-start --run run_aaaaaaaaaaaa --task task_1 --json"
    )
    payload = bash_payload(command, stdout="started run_bbbbbbbbbbbb")
    proc, calls, _ = run_hook(tmp_path, payload)
    assert proc.returncode == 0
    assert calls == ["sweep ledger --add run_aaaaaaaaaaaa"]
    string_response = {
        **bash_payload("orca orchestration run-create --json"),
        "tool_response": "made run_cccccccccccc",
    }
    second = tmp_path / "second"
    second.mkdir()
    proc, calls, _ = run_hook(second, string_response)
    assert proc.returncode == 0
    assert calls == ["sweep ledger --add run_cccccccccccc"]


@pytest.mark.integration
@pytest.mark.parametrize(
    "payload",
    [
        bash_payload("orca orchestration run-list --json", stdout="run_aaaaaaaaaaaa"),
        bash_payload("ls -la", stdout="run_aaaaaaaaaaaa"),
        bash_payload(
            "orca orchestration run-create --json",
            stdout="run_aaaaaaaaaaaa",
            tool_name="Read",
        ),
        {"tool_name": "Bash", "tool_input": {}},
    ],
)
def test_hook_ignores_other_commands(tmp_path, payload):
    proc, calls, log = run_hook(tmp_path, payload)
    assert (proc.returncode, proc.stdout, proc.stderr) == (0, "", "")
    assert calls == []
    assert not log.exists()


@pytest.mark.integration
def test_hook_no_id_logs_and_exits_0(tmp_path):
    payload = bash_payload(
        "orca orchestration run-create --json", stdout='{"ok": false}'
    )
    proc, calls, log = run_hook(tmp_path, payload)
    assert (proc.returncode, proc.stdout, proc.stderr) == (0, "", "")
    assert calls == []
    lines = log.read_text().splitlines()
    assert len(lines) == 1
    assert "run-create: no Run id found" in lines[0]


@pytest.mark.integration
def test_hook_fails_open_when_superclaude_missing(tmp_path):
    payload = json.loads((FIXTURES / "posttooluse_run_create.json").read_text())
    proc, calls, _ = run_hook(tmp_path, payload, with_superclaude=False)
    assert (proc.returncode, proc.stdout, proc.stderr) == (0, "", "")
    assert calls == []
    bad = tmp_path / "bad-json"
    bad.mkdir()
    proc, _, _ = run_hook(bad, None, raw="{not json")
    assert (proc.returncode, proc.stdout) == (0, "")


@pytest.mark.integration
@pytest.mark.parametrize(
    ("command", "extra_env", "recorded"),
    [
        ("orca-ide orchestration run-create --json", None, True),
        ("/home/u/.local/bin/orca-ide orchestration run-create --json", None, True),
        ("/usr/bin/orca orchestration worker-start --run run_aaaaaaaaaaaa", None, True),
        ("cd /x && orca-ide orchestration run-create --json", None, True),
        (
            "my-orca orchestration run-create --json",
            {"ORCA_CLI_COMMAND": "/opt/bin/my-orca"},
            True,
        ),
        ("my-orca orchestration run-create --json", None, False),  # not a known name
        (
            "neworca orchestration run-create --json",
            None,
            False,
        ),  # the name must be the whole word
        ("orca-ide orchestration run-list --json", None, False),
    ],
)
def test_hook_recognises_the_supported_orca_command_names(
    tmp_path, command, extra_env, recorded
):
    payload = bash_payload(command, stdout="made run_dddddddddddd")
    proc, calls, _ = run_hook(tmp_path, payload, extra_env=extra_env)
    assert (proc.returncode, proc.stdout, proc.stderr) == (0, "", "")
    expected = "run_aaaaaaaaaaaa" if "worker-start" in command else "run_dddddddddddd"
    assert calls == ([f"sweep ledger --add {expected}"] if recorded else [])
