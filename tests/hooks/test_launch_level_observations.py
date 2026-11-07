"""Pending live observations for the launch-level hook (issue #394), and tests of the log-only probe.

The observations need a real governed session and have not been run: each is a skipped test with a reason.
The synthetic payloads in fixtures/launch_level/ob_h1 are not observations.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "launch_level" / "ob_h1"
PROBE = FIXTURES / "log-only-probe.sh"
BASH = shutil.which("bash") or "/bin/bash"


def _run_probe(payload: bytes, log: str | None, tmp_path: Path):
    env = {k: v for k, v in os.environ.items() if k != "LAUNCH_LEVEL_PROBE_LOG"}
    env["HOME"] = str(tmp_path)
    if log is not None:
        env["LAUNCH_LEVEL_PROBE_LOG"] = log
    return subprocess.run(
        [BASH, str(PROBE)], input=payload, capture_output=True, env=env, timeout=10
    )


def test_fixtures_are_nine_json_objects_with_an_event_name():
    files = sorted(FIXTURES.glob("item[1-9]-*.json"))
    assert [f.name[4] for f in files] == list("123456789")
    for f in files:
        data = json.loads(f.read_text())
        assert isinstance(data, dict) and isinstance(data["hook_event_name"], str), (
            f.name
        )
    assert (FIXTURES / "README.md").is_file()
    assert os.access(PROBE, os.X_OK)


def test_probe_appends_exactly_one_line_per_call(tmp_path):
    log = tmp_path / "probe.log"
    payload = (FIXTURES / "item2-skill-keys.json").read_bytes()
    for count in (1, 2):
        result = _run_probe(payload, str(log), tmp_path)
        assert result.returncode == 0
        assert result.stdout == b"" and result.stderr == b""
        lines = log.read_text().splitlines()
        assert len(lines) == count
    assert json.loads(lines[-1])["tool_name"] == "Skill"


def test_probe_flattens_a_multiline_payload_to_one_line(tmp_path):
    log = tmp_path / "probe.log"
    pretty = json.dumps(
        {"hook_event_name": "PreToolUse", "session_id": "s"}, indent=2
    ).encode()
    assert _run_probe(pretty, str(log), tmp_path).returncode == 0
    assert len(log.read_text().splitlines()) == 1


def test_probe_with_log_path_unset_prints_nothing_and_exits_zero(tmp_path):
    result = _run_probe(b'{"hook_event_name": "PreToolUse"}', None, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert list(tmp_path.iterdir()) == []


def test_probe_with_unwritable_log_path_exits_zero_silently(tmp_path):
    target_dir = tmp_path / "a-directory"
    target_dir.mkdir()
    for bad in (str(target_dir), str(tmp_path / "missing" / "dir" / "probe.log")):
        result = _run_probe(b'{"hook_event_name": "PreToolUse"}', bad, tmp_path)
        assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


_PENDING = [f"OB-H1 item {n}" for n in range(1, 10)] + ["OB-H2", "OB-H3", "OB-CTX"]


@pytest.mark.parametrize("item", _PENDING)
def test_pending_live_observation(item):
    pytest.skip(f"{item}: needs a real governed session and has not been run")
