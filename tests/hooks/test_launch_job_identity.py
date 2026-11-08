"""Real Linux session tests; deliberate setsid escape is NOT containment."""

import json
import os
import shlex
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/hooks/scripts/launch-job-identity.sh"
)
pytestmark = pytest.mark.skipif(sys.platform != "linux", reason="Linux proc contract")


def wait_for(check, timeout=8):
    until = time.monotonic() + timeout
    while time.monotonic() < until:
        result = check()
        if result:
            return result
        time.sleep(0.03)
    raise AssertionError("timed out waiting for job event")


class Harness:
    def __init__(self, tmp):
        self.home = tmp / "home"
        self.home.mkdir(mode=0o700)
        self.root = self.home / ".claude/state/launch-level"
        (self.root / "sessions").mkdir(parents=True, mode=0o700)
        self.root.chmod(0o700)
        self.env = dict(
            os.environ,
            HOME=str(self.home),
            UV_PYTHON=sys.executable,
            UV_PYTHON_DOWNLOADS="never",
        )
        self.processes = []
        self.bind("old")

    def bind(self, sid, content="worktree\n"):
        path = self.root / "sessions" / sid
        path.write_text(content)
        path.chmod(0o600)
        return path

    def call(self, *args, **kwargs):
        return subprocess.run(
            ["/bin/bash", str(SCRIPT), *args],
            env=self.env,
            capture_output=True,
            text=True,
            timeout=10,
            **kwargs,
        )

    def token(self, command, sid="old"):
        result = self.call("prepare", sid, command)
        assert result.returncode == 0, result.stderr
        return result.stdout.strip()

    def start(self, command):
        token = self.token(command)
        process = subprocess.Popen(
            ["bash", str(SCRIPT), "run", token],
            env=self.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.processes.append(process)
        return process

    def selector(self, output):
        return f"bash {shlex.quote(str(SCRIPT))} identify > {shlex.quote(str(output))}"

    def records(self):
        return list((self.root / "jobs").glob("*.json"))

    def live_record(self):
        return wait_for(lambda: self.records())[0]

    def identify(self, pid=None):
        result = self.call("identify", *([] if pid is None else [str(pid)]))
        assert result.returncode == 0
        return json.loads(result.stdout)

    def cleanup(self):
        # Only fixture-owned session leaders are signalled; no shared group kill.
        for path in self.records():
            value = json.loads(path.read_text())
            try:
                os.kill(value["pid"], signal.SIGTERM)
            except ProcessLookupError:
                pass
        for process in self.processes:
            try:
                process.communicate(timeout=4)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate(timeout=4)


@pytest.fixture
def job(tmp_path):
    harness = Harness(tmp_path)
    try:
        yield harness
    finally:
        harness.cleanup()


def test_output_status_stdin_environment_and_cwd(job, tmp_path):
    job.env["JOB_VALUE"] = "literal $() ' value"
    token = job.token(
        'read -r line; printf "%s|%s|%s" "$line" "$JOB_VALUE" "$PWD"; printf error >&2; exit 7'
    )
    result = job.call("run", token, input="stdin survives\n", cwd=tmp_path)
    assert result.returncode == 7
    assert result.stdout == f"stdin survives|{job.env['JOB_VALUE']}|{tmp_path}"
    assert result.stderr == "error"
    assert not job.records()
    assert not list((job.root / "requests").iterdir())
    assert job.call("run", token).returncode == 2


@pytest.mark.parametrize("mode", ["run", "execute"])
def test_child_restores_python_ignored_signals(job, mode):
    signals = [
        name[3:] for name in ("SIGPIPE", "SIGXFZ", "SIGXFSZ") if hasattr(signal, name)
    ]
    command = (
        f"trap -p {' '.join(signals)}; "
        "yes | head -n 1; printf 'producer=%s\\n' \"${PIPESTATUS[0]}\""
    )
    args = (
        ("run", job.token(command))
        if mode == "run"
        else ("execute", "old", "", command)
    )
    result = job.call(*args)
    assert result.returncode == 0
    assert result.stdout == "y\nproducer=141\n"
    assert result.stderr == ""
    assert not job.records()


@pytest.mark.parametrize("mode", ["run", "execute"])
@pytest.mark.parametrize(
    "char",
    ["😀", "é", "\x01", '"', "\\"],
    ids=["emoji", "bmp", "control", "quote", "slash"],
)
def test_maximum_command_survives_json_expansion(job, mode, char):
    sid, tool = "s" * 128, "t" * 128
    job.bind(sid)
    prefix = "printf request-ok; # "
    command = prefix + char * ((32768 - len(prefix.encode())) // len(char.encode()))
    assert 32765 <= len(command.encode()) <= 32768
    if mode == "run":
        prepared = job.call("prepare", sid, command, tool)
        assert prepared.returncode == 0, prepared.stderr
        result = job.call("run", prepared.stdout.strip())
    else:
        result = job.call("execute", sid, tool, command)
    assert (result.returncode, result.stdout, result.stderr) == (0, "request-ok", "")
    assert not job.records()
    assert not list((job.root / "requests").iterdir())


@pytest.mark.parametrize("char", ["😀", "é"], ids=["emoji", "bmp"])
def test_hook_unicode_command_survives_request_serialization(job, char):
    prefix = "printf request-ok; # "
    command = prefix + char * ((32768 - len(prefix.encode())) // len(char.encode()))
    result = job.call(input=json.dumps(hook_event(command), ensure_ascii=False))
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)["hookSpecificOutput"]
    assert "permissionDecision" not in output
    executed = execute_rewritten(job, output["updatedInput"])
    assert (executed.returncode, executed.stdout, executed.stderr) == (
        0,
        "request-ok",
        "",
    )
    assert not job.records()


@pytest.mark.parametrize(
    "sid,content",
    [
        ("missing", None),
        ("old", ""),
        ("old", "full\nextra"),
        ("old", "degraded"),
        ("../bad", None),
    ],
)
def test_prepare_requires_exact_existing_governed_session(job, sid, content):
    if content is not None:
        job.bind(sid, content)
    result = job.call("prepare", sid, "printf secret-command")
    assert result.returncode == 2
    assert "secret-command" not in result.stderr
    assert not (job.root / "requests").exists()


@pytest.mark.parametrize("level", ["worktree", "full", "full-submit", "full-submit\n"])
def test_allowed_levels_and_tool_id(job, level):
    job.bind("old", level)
    result = job.call("prepare", "old", "true", "tool_1")
    assert result.returncode == 0
    data = json.loads((job.root / "requests" / result.stdout.strip()).read_text())
    assert data["tool_use_id"] == "tool_1"
    assert job.call("run", result.stdout.strip()).returncode == 0
    assert job.call("prepare", "old", "true", "../tool").returncode == 2


@pytest.mark.parametrize(
    "target", ["session", "sessions", "root", "request", "requests"]
)
def test_symlink_components_refused(job, tmp_path, target):
    token = job.token("touch SHOULD_NOT_EXIST")
    paths = {
        "session": job.root / "sessions/old",
        "sessions": job.root / "sessions",
        "root": job.root,
        "request": job.root / "requests" / token,
        "requests": job.root / "requests",
    }
    path = paths[target]
    moved = tmp_path / "moved"
    path.rename(moved)
    path.symlink_to(moved, target_is_directory=moved.is_dir())
    result = job.call("run", token, cwd=tmp_path)
    assert result.returncode == 2
    assert not (tmp_path / "SHOULD_NOT_EXIST").exists()
    # Restore before fixture cleanup: it should not follow attacker state.
    path.unlink()
    moved.rename(path)


@pytest.mark.parametrize(
    "damage",
    [
        "json",
        "oversize",
        "mode",
        "directory",
        "bad_sid",
        "bad_tool",
        "bad_command",
        "extra",
        "missing",
        "hardlink",
    ],
)
def test_bad_requests_never_execute(job, tmp_path, damage):
    marker = tmp_path / "side-effect"
    token = job.token(f"touch {marker}")
    path = job.root / "requests" / token
    if damage == "directory":
        path.unlink()
        path.mkdir(mode=0o700)
    elif damage == "missing":
        path.unlink()
    elif damage == "hardlink":
        os.link(path, tmp_path / "alias")
    else:
        data = json.loads(path.read_text())
        path.chmod(0o600)
        if damage == "json":
            path.write_text("{")
        elif damage == "oversize":
            path.write_text("x" * (6 * 32768 + 1025))
        elif damage == "mode":
            path.chmod(0o644)
        else:
            if damage == "bad_sid":
                data["session_id"] = "../old"
            elif damage == "bad_tool":
                data["tool_use_id"] = 42
            elif damage == "bad_command":
                data["command"] = ["touch", str(marker)]
            else:
                data["extra"] = True
            path.write_text(json.dumps(data))
    assert job.call("run", token).returncode == 2
    assert not marker.exists()
    if damage == "oversize":
        assert path.exists()  # rejected by the size guard before consumption
    assert job.call("run", "../../invalid").returncode == 2


def test_atomic_concurrent_consumption(job, tmp_path):
    marker = tmp_path / "count"
    token = job.token(f"printf x >> {marker}")
    children = [
        subprocess.Popen(
            ["bash", str(SCRIPT), "run", token],
            env=job.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        for _ in range(2)
    ]
    for child in children:
        child.communicate(timeout=10)
    assert sorted(child.returncode for child in children) == [0, 2]
    assert marker.read_text() == "x"


def test_old_orphan_keeps_origin_new_ordinary_and_forged_environment_do_not(
    job, tmp_path
):
    ready, go, output = (tmp_path / name for name in ("ready", "go", "selected"))
    command = f"(printf '%s' \"$BASHPID\" > {ready}; while [ ! -e {go} ]; do sleep .03; done; {job.selector(output)}) & exit 9"
    process = job.start(command)
    wait_for(ready.exists)
    record = job.live_record()
    identity = json.loads(record.read_text())
    orphan = int(wait_for(lambda: ready.read_text()))
    wait_for(
        lambda: (
            int(Path(f"/proc/{orphan}/stat").read_text().rsplit(")", 1)[1].split()[1])
            == identity["pid"]
        )
    )
    assert process.poll() is None  # main shell exited; reparented orphan holds job open
    job.bind("new", "full")
    job.env.update(
        CLAUDE_SESSION_ID="old",
        CCSESSION_LAUNCH_ID=str(identity["pid"]),
        LAUNCH_LEVEL="worktree",
    )
    assert job.identify() == {"status": "ordinary"}
    independent = subprocess.run(
        ["bash", str(SCRIPT), "identify"],
        env=job.env,
        capture_output=True,
        text=True,
        start_new_session=True,
        timeout=10,
    )
    assert json.loads(independent.stdout) == {"status": "ordinary"}
    assert job.identify(identity["pid"]) == {"status": "governed", "session_id": "old"}
    go.touch()
    stdout, stderr = process.communicate(timeout=10)
    assert (process.returncode, stdout, stderr) == (9, "", "")
    assert json.loads(output.read_text()) == {"status": "governed", "session_id": "old"}
    assert not record.exists()


@pytest.mark.parametrize(
    "damage", ["pid", "start", "boot", "json", "sid", "mode", "zombie_or_dead"]
)
def test_corrupt_or_stale_job_record_is_unknown_not_human(job, tmp_path, damage):
    ready = tmp_path / "ready"
    process = job.start(f"touch {ready}; sleep 30")
    wait_for(ready.exists)
    path = job.live_record()
    original = path.read_text()
    value = json.loads(original)
    pid = value["pid"]
    path.chmod(0o600)
    if damage == "json":
        path.write_text("{")
    elif damage == "mode":
        path.chmod(0o644)
    elif damage == "zombie_or_dead":
        os.kill(pid, signal.SIGKILL)
        # Pipe EOF waits for surviving children too; inspect before communicate.
        live = [
            int(p.name)
            for p in Path("/proc").iterdir()
            if p.name.isdecimal()
            and int(p.name) != pid
            and _session_of(int(p.name)) == pid
        ]
        try:
            assert live
            assert job.identify(live[0]) == _unknown("orphaned", path)
        finally:
            for member in live:
                try:
                    os.kill(member, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            process.communicate(timeout=5)
            path.unlink()
        return
    else:
        if damage == "pid":
            value["pid"] += 1
        elif damage == "start":
            value["start"] += 1
        elif damage == "boot":
            value["boot"] = "00000000-0000-0000-0000-000000000000"
        else:
            value["session_id"] = "../bad"
        path.write_text(json.dumps(value))
    reason = "stale" if damage in ("start", "boot") else "unreadable"
    try:
        assert job.identify(pid) == _unknown(reason, path)
    finally:
        path.chmod(0o600)
        path.write_text(original)


def _unknown(reason, record):
    # FR-025 shape: unknown with a reason and the absolute record path.
    return {"status": "unknown", "reason": reason, "record": str(record)}


def _session_of(pid):
    try:
        return int(Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[3])
    except (OSError, IndexError, ValueError):
        return None


def test_release_live_job_and_invalid_bound_state(job, tmp_path):
    go, output, ready = (tmp_path / name for name in ("go", "output", "ready"))
    process = job.start(
        f"touch {ready}; while [ ! -e {go} ]; do sleep .03; done; {job.selector(output)}"
    )
    wait_for(ready.exists)
    record = job.live_record()
    pid = json.loads(record.read_text())["pid"]
    job.bind("old", "broken")
    assert job.identify(pid) == _unknown("unreadable", record)
    (job.root / "sessions/old").unlink()
    assert job.identify(pid) == {"status": "ordinary", "reason": "released"}
    go.touch()
    process.communicate(timeout=10)
    assert json.loads(output.read_text()) == {
        "status": "ordinary",
        "reason": "released",
    }
    assert not job.records()


@pytest.mark.parametrize("signum", [signal.SIGTERM, signal.SIGINT, signal.SIGHUP])
def test_signal_cancellation_cleans_ordinary_descendants_only(job, tmp_path, signum):
    ready = tmp_path / "ready"
    outsider = subprocess.Popen(["sleep", "30"])
    process = job.start(f"sleep 30 & printf '%s' $! > {ready}; wait")
    try:
        wait_for(ready.exists)
        child = int(ready.read_text())
        supervisor = json.loads(job.live_record().read_text())["pid"]
        os.kill(supervisor, signum)
        process.communicate(timeout=6)
        assert process.returncode == 128 + signum
        assert not Path(f"/proc/{child}").exists()
        assert outsider.poll() is None
        assert not job.records()
    finally:
        outsider.terminate()
        outsider.wait(timeout=3)


def test_main_shell_status_survives_cancellation_during_background_wait(job, tmp_path):
    ready = tmp_path / "ready"
    process = job.start(f"sleep 30 & touch {ready}; exit 4")
    wait_for(ready.exists)
    time.sleep(0.15)
    pid = json.loads(job.live_record().read_text())["pid"]
    os.kill(pid, signal.SIGTERM)
    process.communicate(timeout=6)
    assert process.returncode == 4
    assert not job.records()


def test_intentional_new_session_escape_explicitly_unselected(job, tmp_path):
    output, ready, go, detached_pid = (
        tmp_path / name for name in ("output", "ready", "go", "pid")
    )
    detached = f"echo $$ > {detached_pid}; touch {ready}; while [ ! -e {go} ]; do sleep .03; done; {job.selector(output)}"
    process = job.start(
        f"setsid bash -c {shlex.quote(detached)} </dev/null >/dev/null 2>&1 &"
    )
    try:
        wait_for(ready.exists)
        process.communicate(timeout=5)
        assert process.returncode == 0
        assert not job.records()
        go.touch()
        wait_for(lambda: output.exists() and output.stat().st_size)
        assert json.loads(output.read_text()) == {"status": "ordinary"}
    finally:
        if detached_pid.exists():
            try:
                os.kill(int(detached_pid.read_text()), signal.SIGKILL)
            except ProcessLookupError:
                pass


def test_missing_and_invalid_proc_identity(job):
    assert job.identify(2147483647) == {"status": "unknown"}
    assert job.identify(-1) == {"status": "unknown"}
    assert job.identify("not-a-pid") == {"status": "unknown"}
    assert job.identify() == {"status": "ordinary"}
    assert job.call("prepare", "old", "x" * 32769).returncode == 2
    assert job.call("bad-mode").returncode == 2


@pytest.mark.parametrize("target", ["home", "root", "sessions", "session", "requests"])
def test_unsafe_modes_refused(job, target):
    token = job.token("true")
    paths = {
        "home": job.home,
        "root": job.root,
        "sessions": job.root / "sessions",
        "session": job.root / "sessions/old",
        "requests": job.root / "requests",
    }
    path = paths[target]
    original = path.stat().st_mode & 0o777
    path.chmod(0o777 if path.is_dir() else 0o644)
    try:
        assert job.call("run", token).returncode == 2
        if target != "requests":
            assert job.call("prepare", "old", "true").returncode == 2
    finally:
        path.chmod(original)


def test_bad_home_and_symlinked_home_are_not_identity_authority(job, tmp_path):
    alias = tmp_path / "home-link"
    alias.symlink_to(job.home, target_is_directory=True)
    for home in (str(alias), "relative-home"):
        job.env["HOME"] = home
        assert job.call("prepare", "old", "true").returncode == 2
        assert job.identify() == {"status": "unknown"}


def test_invalid_and_symlinked_job_registry_unknown(job, tmp_path):
    process = job.start("sleep 30")
    path = job.live_record()
    pid = json.loads(path.read_text())["pid"]
    moved = tmp_path / "record"
    path.rename(moved)
    path.symlink_to(moved)
    try:
        assert job.identify(pid) == _unknown("unreadable", path)
    finally:
        path.unlink()
        moved.rename(path)
    process.send_signal(signal.SIGTERM)
    process.communicate(timeout=6)
    assert process.returncode == 143
    assert not job.records()


def test_request_release_before_run_consumes_authorization(job, tmp_path):
    marker = tmp_path / "forbidden"
    token = job.token(f"touch {marker}")
    (job.root / "sessions/old").unlink()
    assert job.call("run", token).returncode == 2
    job.bind("old")
    assert job.call("run", token).returncode == 2
    assert not marker.exists()


def test_deep_json_and_nul_command_fail_with_plain_diagnostics(job):
    for data in (
        "[" * 2000 + "]" * 2000,
        json.dumps(
            {"session_id": "old", "tool_use_id": None, "command": "bad\u0000command"}
        ),
    ):
        token = job.token("true")
        path = job.root / "requests" / token
        path.chmod(0o600)
        path.write_text(data)
        result = job.call("run", token)
        assert result.returncode == 2
        assert (
            result.stderr
            == "launch job: invalid invocation or unavailable private state\n"
        )


def test_cancellation_escalates_for_uncooperative_child(job, tmp_path):
    ready = tmp_path / "ready"
    process = job.start(f"trap '' TERM; touch {ready}; while :; do sleep .1; done")
    wait_for(ready.exists)
    record = json.loads(job.live_record().read_text())
    os.kill(record["pid"], signal.SIGTERM)
    process.communicate(timeout=6)
    assert process.returncode == 137
    assert not job.records()


def hook_event(command="true", sid="old", **fields):
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "session_id": sid,
        "tool_use_id": "toolu_01ABC123",
        "cwd": "/not-binding-authority",
        "tool_input": {"command": command},
    }
    event.update(fields)
    return event


def adapt(job, event, script=SCRIPT):
    return subprocess.run(
        ["/bin/bash", str(script)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        env=job.env,
        timeout=10,
    )


def rewritten(job, event, script=SCRIPT):
    before = set(job.root.rglob("*"))
    result = adapt(job, event, script)
    assert set(job.root.rglob("*")) == before  # permission evaluation creates no state
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    output = json.loads(result.stdout)
    specific = output["hookSpecificOutput"]
    assert specific["hookEventName"] == "PreToolUse"
    assert "permissionDecision" not in specific
    assert set(specific) == {"hookEventName", "updatedInput", "additionalContext"}
    assert "cd does not persist" in specific["additionalContext"]
    return specific["updatedInput"]


def execute_rewritten(job, updated, **kwargs):
    return subprocess.run(
        ["/bin/bash", "-c", updated["command"]],
        env=job.env,
        capture_output=True,
        text=True,
        timeout=10,
        **kwargs,
    )


def test_hook_replaces_whole_input_without_approval_and_executes(job, tmp_path):
    output = tmp_path / "origin"
    job.env["JOB_VALUE"] = "literal $dollar ' and newline\nvalue"
    command = f'read -r line; printf "%s|%s|%s" "$line" "$JOB_VALUE" "$PWD"; printf error >&2; {job.selector(output)}; exit 13'
    inputs = {
        "command": command,
        "timeout": 2300,
        "run_in_background": False,
        "description": "keep exactly",
        "cwd": str(tmp_path),
        "future_field": {"array": [1, None, "literal"]},
    }
    updated = rewritten(job, hook_event(tool_input=inputs))
    assert {k: v for k, v in updated.items() if k != "command"} == {
        k: v for k, v in inputs.items() if k != "command"
    }
    assert shlex.split(updated["command"])[2:] == [
        "execute",
        "old",
        "toolu_01ABC123",
        command,
    ]
    assert not (job.root / "requests").exists()
    result = execute_rewritten(job, updated, input="stdin survives\n", cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (
        13,
        f"stdin survives|{job.env['JOB_VALUE']}|{tmp_path}",
        "error",
    )
    assert json.loads(output.read_text()) == {"status": "governed", "session_id": "old"}
    assert not list((job.root / "requests").iterdir())
    assert not job.records()


@pytest.mark.parametrize("sid", ["unbound", "", None, 123, "../old"])
def test_hook_unbound_and_unverifiable_ids_are_silent_without_state_creation(job, sid):
    event = hook_event(sid=sid, parent_session_id="old", agent_id="child")
    result = adapt(job, event)
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")
    assert not (job.root / "requests").exists()


@pytest.mark.parametrize("home", ["missing", "unset", "fresh"])
def test_hook_missing_ordinary_home_or_store_does_not_require_uv(job, tmp_path, home):
    job.env["PATH"] = str(tmp_path / "no-binaries")
    if home == "unset":
        job.env.pop("HOME")
    else:
        job.env["HOME"] = str(tmp_path / home)
        if home == "fresh":
            Path(job.env["HOME"]).mkdir(mode=0o700)
    result = adapt(job, hook_event(sid="ordinary"))
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")
    assert not (tmp_path / home / ".claude").exists()


@pytest.mark.parametrize("tool", ["Monitor", "Read", "Write"])
def test_hook_non_bash_is_explicitly_out_of_scope(job, tool):
    result = adapt(job, hook_event(tool_name=tool))
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")
    assert not (job.root / "requests").exists()


@pytest.mark.parametrize(
    "raw",
    [
        "{",
        "[]",
        "null",
        '["session_id", "old"]',
        '{"tool_name":"Bash","subagent":{"session_id":"old"}}',
        pytest.param(" " * ((1 << 20) + 1), id="oversized-envelope"),
    ],
)
def test_unparseable_or_unverifiable_envelope_does_not_guess_governance(job, raw):
    result = job.call(input=raw)
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")
    assert not (job.root / "requests").exists()


@pytest.mark.parametrize(
    "change",
    [
        {"tool_input": None},
        {"tool_input": []},
        {"tool_input": {}},
        {"tool_input": {"command": 12}},
        {"tool_input": {"command": "bad\u0000value"}},
        {"tool_input": {"command": "x" * 32769}},
        {"tool_use_id": 17},
        {"agent_id": {"parent_session_id": "old"}},
        {"agent_type": ["Explore"]},
        {"hook_event_name": "SessionStart"},
        {"padding": "x" * 66000},
        {"tool_name": None},
        {"tool_name": 1},
        {"future_value": float("nan")},
    ],
)
def test_bound_malformed_hook_call_blocks_plainly_without_ticket(job, change):
    result = adapt(job, hook_event(**change))
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr == "launch job: governed Bash call cannot be wrapped safely\n"
    assert not (job.root / "requests").exists()


@pytest.mark.parametrize("damage", ["bad-level", "mode", "symlink", "root-mode"])
def test_hook_explicit_but_misconfigured_binding_blocks(job, tmp_path, damage):
    path = job.root / "sessions/old"
    if damage == "bad-level":
        job.bind("old", "invalid")
    elif damage == "mode":
        path.chmod(0o644)
    elif damage == "root-mode":
        job.root.chmod(0o777)
    else:
        path.unlink()
        target = tmp_path / "fake-level"
        target.write_text("worktree")
        target.chmod(0o600)
        path.symlink_to(target)
    result = adapt(job, hook_event())
    assert result.returncode == 2
    assert result.stdout == ""
    assert not (job.root / "requests").exists()


@pytest.mark.parametrize(
    "command,expected",
    [
        (
            "printf '%s' 'literal $(touch NEVER_EXECUTE) `false` ; & | < >'",
            "literal $(touch NEVER_EXECUTE) `false` ; & | < >",
        ),
        (
            "printf '%s' \"quotes ' and \\\"double\\\"\"\nprintf '\\nline two\\n'",
            'quotes \' and "double"\nline two\n',
        ),
        ("printf '%s' $'it\\'s\\na Bash literal'", "it's\na Bash literal"),
        ("printf '%s' 'Unicode café'", "Unicode café"),
    ],
)
def test_hook_literal_shell_content_is_not_reparsed_or_evaluated(
    job, tmp_path, command, expected
):
    updated = rewritten(job, hook_event(command))
    result = execute_rewritten(job, updated, cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")
    assert not (tmp_path / "NEVER_EXECUTE").exists()


def test_hook_origin_and_background_lifetime_survive_new_event_and_release(
    job, tmp_path
):
    ready, go, output = (tmp_path / name for name in ("ready", "go", "origin"))
    command = f"(touch {ready}; while [ ! -e {go} ]; do sleep .03; done; {job.selector(output)}) & exit 8"
    updated = rewritten(
        job,
        hook_event(command, tool_input={"command": command, "run_in_background": True}),
    )
    assert updated["run_in_background"] is True
    process = subprocess.Popen(
        ["/bin/bash", "-c", updated["command"]],
        env=job.env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    job.processes.append(process)
    wait_for(ready.exists)
    identity = json.loads(job.live_record().read_text())
    assert job.identify(identity["pid"]) == {"status": "governed", "session_id": "old"}
    new_event = adapt(job, hook_event(sid="new-unbound"))
    assert (new_event.returncode, new_event.stdout, new_event.stderr) == (0, "", "")
    assert process.poll() is None
    job.bind("new-bound", "full")
    new_output = tmp_path / "new-origin"
    new_call = rewritten(job, hook_event(job.selector(new_output), sid="new-bound"))
    assert execute_rewritten(job, new_call).returncode == 0
    assert json.loads(new_output.read_text()) == {
        "status": "governed",
        "session_id": "new-bound",
    }
    assert job.identify(identity["pid"])["session_id"] == "old"
    (job.root / "sessions/old").unlink()
    go.touch()
    stdout, stderr = process.communicate(timeout=10)
    assert (process.returncode, stdout, stderr) == (8, "", "")
    assert json.loads(output.read_text()) == {
        "status": "ordinary",
        "reason": "released",
    }
    assert not job.records()


def test_hook_top_level_subagent_session_only_and_no_parent_inference(job):
    job.bind("agent-session", "full")
    updated = rewritten(
        job,
        hook_event(
            "true",
            sid="agent-session",
            agent_id="agent_1",
            agent_type="Explore",
            parent_session_id="old",
        ),
    )
    assert shlex.split(updated["command"])[2:4] == ["execute", "agent-session"]
    assert not (job.root / "requests").exists()
    assert execute_rewritten(job, updated).returncode == 0
    result = adapt(
        job,
        hook_event(sid="unbound-agent", agent_id="agent_1", parent_session_id="old"),
    )
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")


def test_hook_release_before_execution_creates_no_replayable_ticket(job, tmp_path):
    marker = tmp_path / "never"
    updated = rewritten(job, hook_event(f"touch {marker}"))
    (job.root / "sessions/old").unlink()
    assert execute_rewritten(job, updated).returncode == 2
    assert not (job.root / "requests").exists()
    assert not job.records()
    assert not marker.exists()


def test_hook_refuses_conflicting_wrapper_without_second_ticket(job):
    updated = rewritten(job, hook_event())
    result = adapt(job, hook_event(updated["command"]))
    assert result.returncode == 2
    assert result.stdout == ""
    assert not (job.root / "requests").exists()
    assert execute_rewritten(job, updated).returncode == 0


def test_hook_actual_self_location_with_spaces_and_symlink(job, tmp_path):
    import shutil

    folder = tmp_path / "space and ' quote"
    folder.mkdir()
    copied = folder / SCRIPT.name
    shutil.copy2(SCRIPT, copied)
    alias = tmp_path / "hook alias"
    alias.symlink_to(copied)
    updated = rewritten(job, hook_event("printf relocated"), script=alias)
    result = execute_rewritten(job, updated, cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "relocated", "")


@pytest.mark.parametrize("failure", ["uv", "interpreter"])
def test_hook_failed_startup_creates_no_ticket_to_replay(job, tmp_path, failure):
    marker = tmp_path / "never"
    updated = rewritten(job, hook_event(f"touch {marker}"))
    if failure == "uv":
        job.env["PATH"] = str(tmp_path / "no-binaries")
    else:
        job.env["UV_PYTHON"] = str(tmp_path / "missing-interpreter")
    result = execute_rewritten(job, updated)
    assert result.returncode == 2
    assert not marker.exists()
    assert not (job.root / "requests").exists()
    assert not job.records()


def test_hook_cleanup_does_not_overwrite_outer_exit_trap_or_status(job, tmp_path):
    outer = tmp_path / "outer-trap"
    updated = rewritten(job, hook_event("exit 17"))
    command = f"trap {shlex.quote(f'printf outer > {outer}')} EXIT; {updated['command']}; status=$?; exit $status"
    result = subprocess.run(
        ["/bin/bash", "-c", command],
        env=job.env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 17
    assert outer.read_text() == "outer"
    assert not list((job.root / "requests").iterdir())


def test_execution_never_follows_symlinked_request_directory(job, tmp_path):
    marker = tmp_path / "never"
    updated = rewritten(job, hook_event(f"touch {marker}"))
    decoy = tmp_path / "decoy"
    decoy.mkdir(mode=0o700)
    sentinel = decoy / "keep"
    sentinel.write_text("do not unlink")
    (job.root / "requests").symlink_to(decoy, target_is_directory=True)
    assert execute_rewritten(job, updated).returncode == 2
    assert not marker.exists()
    assert list(decoy.iterdir()) == [sentinel]
    assert sentinel.read_text() == "do not unlink"


def test_hook_fresh_shell_cwd_contract_is_explicit_and_repeatable(job, tmp_path):
    child = tmp_path / "child"
    child.mkdir()
    first = rewritten(job, hook_event(f"cd {child}; pwd"))
    first_result = execute_rewritten(job, first, cwd=tmp_path)
    assert first_result.stdout.strip() == str(child)
    second = rewritten(job, hook_event("pwd"))
    assert execute_rewritten(job, second, cwd=tmp_path).stdout.strip() == str(tmp_path)
    explicit = rewritten(job, hook_event(f"cd {child} && pwd"))
    assert execute_rewritten(job, explicit, cwd=tmp_path).stdout.strip() == str(child)


@pytest.mark.parametrize("fault", ["platform", "proc", "fcntl"])
def test_hook_fault_injection_blocks_bound_unsupported_runtime_before_publication(
    job, fault
):
    # Fault injection is NOT evidence from a non-Linux live harness.
    source = SCRIPT.read_text().split("<<'PY'\n", 1)[1].rsplit("\nPY\n", 1)[0]
    prefixes = {
        "platform": "import sys; sys.platform = 'darwin'\n",
        "proc": "import builtins; original_open = builtins.open\ndef guarded_open(path, *args, **kwargs):\n if str(path).startswith('/proc/'): raise OSError('unsupported proc')\n return original_open(path, *args, **kwargs)\nbuiltins.open = guarded_open\n",
        "fcntl": "import sys; sys.modules['fcntl'] = None\n",
    }
    result = subprocess.run(
        [
            "uv",
            "run",
            "--no-project",
            "python",
            "-I",
            "-c",
            prefixes[fault] + source,
            str(SCRIPT),
        ],
        input=json.dumps(hook_event()),
        env=job.env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr == "launch job: governed Bash call cannot be wrapped safely\n"
    assert not (job.root / "requests").exists()


def test_bound_duplicate_json_fields_block_without_leaking_command(job):
    raw = '{"session_id":"old","tool_name":"Bash","hook_event_name":"PreToolUse","tool_input":{"command":"secret","command":"true"}}'
    result = job.call(input=raw)
    assert result.returncode == 2
    assert result.stdout == ""
    assert "secret" not in result.stderr
    assert not (job.root / "requests").exists()


def test_bound_hook_missing_uv_blocks_only_with_jq_positive_identity(job, tmp_path):
    jq_only_path(job, tmp_path)
    result = adapt(job, hook_event("touch NEVER_EXECUTE"))
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr == "launch job: UV is required for this invocation\n"
    assert not (job.root / "requests").exists()


def test_withheld_hook_rewrite_leaves_no_authorization_ticket_or_job(job, tmp_path):
    marker = tmp_path / "rejected-command"
    before = set(job.root.rglob("*"))
    updated = rewritten(job, hook_event(f"touch {marker}"))
    # Model permission rejection: never execute the successfully emitted command.
    assert shlex.split(updated["command"])[2] == "execute"
    assert set(job.root.rglob("*")) == before
    assert not (job.root / "requests").exists()
    assert not job.records()
    assert not marker.exists()
    assert job.call("run", "0" * 32).returncode == 2
    assert not marker.exists()


def test_accepted_execution_creates_and_consumes_exactly_one_runtime_request(job):
    import ctypes
    import struct

    requests = job.root / "requests"
    requests.mkdir(mode=0o700)
    libc = ctypes.CDLL(None, use_errno=True)
    fd = libc.inotify_init1(os.O_NONBLOCK | os.O_CLOEXEC)
    assert fd >= 0
    try:
        assert libc.inotify_add_watch(fd, os.fsencode(requests), 0x100 | 0x200) >= 0
        updated = rewritten(
            job, hook_event(f"/bin/bash {shlex.quote(str(SCRIPT))} identify")
        )
        result = execute_rewritten(job, updated)
        assert result.returncode == 0, result.stderr
        assert json.loads(result.stdout) == {"status": "governed", "session_id": "old"}
        data = os.read(fd, 65536)
        events = []
        at = 0
        while at < len(data):
            _, mask, _, size = struct.unpack_from("iIII", data, at)
            name = data[at + 16 : at + 16 + size].split(b"\0")[0].decode()
            if len(name) == 32 and all(c in "0123456789abcdef" for c in name):
                events.append((mask, name))
            at += 16 + size
        assert len(events) == 2, events
        assert events[0][0] == 0x100  # IN_CREATE: runtime atomic publication
        assert events[1] == (0x200, events[0][1])  # IN_DELETE: one-use consumption
        assert not list(requests.iterdir())
        assert not job.records()
    finally:
        os.close(fd)


def test_execution_finally_cleans_only_its_ticket_if_run_startup_fails(job, tmp_path):
    # Fault injection targets the tiny publication/consumption boundary only.
    source = SCRIPT.read_text().split("<<'PY'\n", 1)[1].rsplit("\nPY\n", 1)[0]
    assert source.count("        return run(token)\n") == 1
    source = source.replace(
        "        return run(token)\n",
        "        raise OSError('injected startup failure')\n",
    )
    requests = job.root / "requests"
    requests.mkdir(mode=0o700)
    unrelated = requests / "untouched"
    unrelated.write_text("keep")
    marker = tmp_path / "never"
    result = subprocess.run(
        [
            "uv",
            "run",
            "--no-project",
            "python",
            "-I",
            "-c",
            source,
            str(SCRIPT),
            "execute",
            "old",
            "tool_1",
            f"touch {marker}",
        ],
        env=job.env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 2
    assert not marker.exists()
    assert list(requests.iterdir()) == [unrelated]
    assert unrelated.read_text() == "keep"
    assert not job.records()


def jq_only_path(job, tmp_path):
    import shutil

    jq = shutil.which("jq")
    assert jq is not None, "jq is required for the fallback parser tests"
    binary_dir = tmp_path / "jq-only"
    binary_dir.mkdir()
    (binary_dir / "jq").symlink_to(jq)
    job.env["PATH"] = str(binary_dir)


@pytest.mark.parametrize("sid", ["ordinary", "different", "old-prefix", "old\n"])
@pytest.mark.parametrize("explicit_hook", [False, True])
def test_missing_uv_existing_other_binding_does_not_select_ordinary(
    job, tmp_path, sid, explicit_hook
):
    jq_only_path(job, tmp_path)
    before = set(job.root.rglob("*"))
    args = ("hook",) if explicit_hook else ()
    result = job.call(*args, input=json.dumps(hook_event(sid=sid)))
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")
    assert set(job.root.rglob("*")) == before


def test_missing_uv_stale_store_without_session_binding_is_inert(job, tmp_path):
    jq_only_path(job, tmp_path)
    (job.root / "sessions/old").unlink()
    (job.root / "sessions").rmdir()
    result = adapt(job, hook_event())
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")
    assert not (job.root / "requests").exists()


def test_missing_uv_and_jq_is_unavailable_adaptation_not_positive_identity(
    job, tmp_path
):
    job.env["PATH"] = str(tmp_path / "no-binaries")
    before = set(job.root.rglob("*"))
    result = adapt(job, hook_event())
    # No parser can establish the bound event: this is not proof of a human.
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")
    assert set(job.root.rglob("*")) == before


@pytest.mark.parametrize(
    "raw",
    [
        "{",
        '{"tool_name":"Bash","nested":{"session_id":"old"}}',
        '{"tool_name":"Bash","session_id":123}',
        '{"tool_name":"Bash","session_id":"../old"}',
        '{"tool_name":"Monitor","session_id":"old"}',
        '{"tool_name":"Bash","session_id":"old"} {"session_id":"old"}',
    ],
)
def test_missing_uv_fallback_never_guesses_from_invalid_or_unsupported_envelope(
    job, tmp_path, raw
):
    jq_only_path(job, tmp_path)
    result = job.call(input=raw)
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")
    assert not (job.root / "requests").exists()


@pytest.mark.parametrize(
    "args",
    [
        ("prepare", "old", "true"),
        ("run", "0" * 32),
        ("identify",),
        ("execute", "old", "tool_1", "true"),
    ],
)
def test_explicit_runtime_modes_still_fail_plainly_without_uv(job, tmp_path, args):
    job.env["PATH"] = str(tmp_path / "no-binaries")
    result = job.call(*args)
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr == "launch job: UV is required for this invocation\n"
    assert not (job.root / "requests").exists()


class LocalPushFixture:
    """Disposable TEST POLICY, not the production O-22 pre-push installation."""

    def __init__(self, job, base):
        self.base = base
        self.work = base / "clone"
        self.remote = base / "remote.git"
        self.log = base / "pre-push-evidence.jsonl"
        self.env = {
            key: value for key, value in job.env.items() if not key.startswith("GIT_")
        }
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null")
        job.env = self.env.copy()
        self.git("init", "--bare", "--initial-branch=main", str(self.remote))
        self.git("clone", str(self.remote), str(self.work))
        self.local("config", "user.name", "Local identity fixture")
        self.local("config", "user.email", "fixture@example.invalid")
        self.a = self.commit("initial")
        assert self.local("remote", "get-url", "origin").stdout.strip() == str(
            self.remote
        )
        self.local("push", "origin", "HEAD:refs/heads/main", "HEAD:refs/heads/master")
        self.b = self.commit("human")
        self.c = self.commit("governed")
        policy = """import json, os, subprocess, sys
selected = subprocess.run(['/bin/bash', sys.argv[1], 'identify'], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=5)
identity = json.loads(selected.stdout) if selected.returncode == 0 else {'status': 'unknown'}
blocked = False
for line in sys.stdin:
    local_ref, local_sha, remote_ref, remote_sha = line.split()
    deny = identity.get('status') == 'governed' and remote_ref in ('refs/heads/main', 'refs/heads/master')
    row = {'policy': 'TEST ONLY: positive-governed exact-protected-ref', 'identity': identity, 'actor_session': os.getsid(0), 'remote_ref': remote_ref, 'local_sha': local_sha, 'remote_sha': remote_sha, 'refused': deny}
    fd = os.open(sys.argv[2], os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try: os.write(fd, (json.dumps(row) + '\\n').encode())
    finally: os.close(fd)
    blocked = blocked or deny
if blocked: print('fixture policy refuses governed protected ref', file=sys.stderr)
sys.exit(1 if blocked else 0)
"""
        hook = self.work / ".git/hooks/pre-push"
        hook.write_text(
            "#!/bin/bash\nexec "
            + shlex.join(
                [
                    "uv",
                    "run",
                    "--no-project",
                    "python",
                    "-I",
                    "-c",
                    policy,
                    str(SCRIPT),
                    str(self.log),
                ]
            )
            + "\n"
        )
        hook.chmod(0o700)

    def git(self, *args, check=True):
        result = subprocess.run(
            ["git", "-C", str(self.base), *args],
            env=self.env,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if check:
            assert result.returncode == 0, result.stderr
        return result

    def local(self, *args, check=True):
        return self.git("-C", str(self.work), *args, check=check)

    def commit(self, label):
        (self.work / "fixture.txt").write_text(label + "\n")
        self.local("add", "fixture.txt")
        self.local("-c", "commit.gpgsign=false", "commit", "-m", label)
        return self.local("rev-parse", "HEAD").stdout.strip()

    def remote_ref(self, branch):
        result = self.git(
            "--git-dir",
            str(self.remote),
            "rev-parse",
            "--verify",
            "refs/heads/" + branch,
            check=False,
        )
        return result.stdout.strip() if result.returncode == 0 else None

    def push_command(self, branch, sha=None):
        return shlex.join(
            [
                "git",
                "-C",
                str(self.work),
                "push",
                "origin",
                (sha or self.c) + ":refs/heads/" + branch,
            ]
        )

    def events(self):
        return (
            [json.loads(line) for line in self.log.read_text().splitlines()]
            if self.log.exists()
            else []
        )


@pytest.fixture
def local_push(job, tmp_path):
    return LocalPushFixture(job, tmp_path)


@pytest.mark.parametrize("branch", ["main", "master"])
def test_real_git_old_governed_background_human_same_clone_reset_and_release(
    job, local_push, tmp_path, branch
):
    fixture = local_push
    ready, go, release, first, second = (
        tmp_path / name for name in ("ready", "go", "release", "first", "second")
    )
    push = fixture.push_command(branch)
    first_out, second_out = tmp_path / "first-push.out", tmp_path / "second-push.out"
    command = f'(touch {ready}; while [ ! -e {go} ]; do sleep .03; done; {push} > {first_out} 2>&1; printf "%s" "$?" > {first}; while [ ! -e {release} ]; do sleep .03; done; {push} > {second_out} 2>&1; printf "%s" "$?" > {second}) & exit 0'
    process = job.start(command)
    try:
        wait_for(ready.exists)
        original = json.loads(job.live_record().read_text())
        assert fixture.remote_ref(branch) == fixture.a
        # Independent ordinary process pushes in the identical clone while the old job lives.
        human = fixture.local(
            "push", "origin", fixture.b + ":refs/heads/" + branch, check=False
        )
        assert human.returncode == 0, human.stderr
        assert fixture.remote_ref(branch) == fixture.b
        ordinary_command = f"/bin/bash {shlex.quote(str(SCRIPT))} identify"
        event = hook_event(ordinary_command, sid="new-unbound-reset")
        unbound = adapt(job, event)
        assert (unbound.returncode, unbound.stdout, unbound.stderr) == (0, "", "")
        ordinary = subprocess.run(
            ["/bin/bash", "-c", ordinary_command],
            env=job.env,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert json.loads(ordinary.stdout) == {"status": "ordinary"}
        assert job.identify(original["pid"]) == {
            "status": "governed",
            "session_id": "old",
        }
        go.touch()
        assert int(wait_for(lambda: first.read_text() if first.exists() else "")) != 0
        assert fixture.remote_ref(branch) == fixture.b
        assert process.poll() is None
        assert job.identify(original["pid"])["session_id"] == "old"
        (job.root / "sessions/old").unlink()
        release.touch()
        assert wait_for(lambda: second.read_text() if second.exists() else "") == "0"
        stdout, stderr = process.communicate(timeout=10)
        assert (process.returncode, stdout, stderr) == (0, "", "")
        assert fixture.remote_ref(branch) == fixture.c
        rows = fixture.events()
        assert len(rows) == 3
        assert (
            rows[0]["identity"] == {"status": "ordinary"}
            and rows[0]["local_sha"] == fixture.b
        )
        assert (
            rows[1]["identity"] == {"status": "governed", "session_id": "old"}
            and rows[1]["refused"] is True
        )
        assert rows[1]["local_sha"] == fixture.c and rows[1]["remote_sha"] == fixture.b
        assert (
            rows[2]["identity"] == {"status": "ordinary", "reason": "released"}
            and rows[2]["refused"] is False
        )
        assert not job.records()
        print(
            json.dumps(
                {
                    "case": "concurrent-local-protected-push-release",
                    "branch": branch,
                    "remote_initial": fixture.a,
                    "remote_after_human_and_governed_refusal": fixture.b,
                    "remote_after_release": fixture.remote_ref(branch),
                    "hook_events": rows,
                },
                sort_keys=True,
            )
        )
    finally:
        go.touch()
        release.touch()


@pytest.mark.parametrize("branch", ["feature/main", "main-extra"])
def test_real_git_test_policy_only_refuses_exact_protected_refs(
    job, local_push, branch
):
    fixture = local_push
    assert fixture.remote_ref(branch) is None
    updated = rewritten(job, hook_event(fixture.push_command(branch)))
    result = execute_rewritten(job, updated)
    assert result.returncode == 0, result.stderr
    assert fixture.remote_ref(branch) == fixture.c
    (row,) = fixture.events()
    assert row["identity"] == {"status": "governed", "session_id": "old"}
    assert row["refused"] is False
    print(
        json.dumps(
            {
                "case": "exact-ref-test-policy",
                "remote_after": fixture.remote_ref(branch),
                "hook_event": row,
            },
            sort_keys=True,
        )
    )


def test_real_git_controlled_resume_same_logical_id_new_job_not_live_cli_resume(
    job, local_push
):
    fixture = local_push
    for _ in range(2):
        token = job.token(fixture.push_command("main"))
        result = job.call("run", token)
        assert result.returncode != 0
        assert fixture.remote_ref("main") == fixture.a
        assert job.call("run", token).returncode == 2
        assert not job.records()
    rows = fixture.events()
    assert len(rows) == 2
    assert all(
        row["identity"] == {"status": "governed", "session_id": "old"}
        and row["refused"]
        for row in rows
    )
    assert rows[0]["actor_session"] != rows[1]["actor_session"]
    print(
        json.dumps(
            {
                "case": "controlled-resume-new-kernel-job-not-cli-resume",
                "remote_unchanged": fixture.remote_ref("main"),
                "hook_events": rows,
            },
            sort_keys=True,
        )
    )


def test_real_git_deliberate_setsid_escape_is_unselected_not_retained(
    job, local_push, tmp_path
):
    fixture = local_push
    before = tmp_path / "before-escape"
    command = (
        job.selector(before)
        + "; setsid /bin/bash -c "
        + shlex.quote(fixture.push_command("main"))
    )
    result = job.call("run", job.token(command))
    assert result.returncode == 0, result.stderr
    assert json.loads(before.read_text()) == {"status": "governed", "session_id": "old"}
    assert fixture.remote_ref("main") == fixture.c
    (row,) = fixture.events()
    assert row["identity"] == {"status": "ordinary"} and row["refused"] is False
    print(
        json.dumps(
            {
                "case": "LIMIT-deliberate-new-session-escape",
                "remote_after": fixture.remote_ref("main"),
                "hook_event": row,
            },
            sort_keys=True,
        )
    )


def test_real_git_killed_supervisor_is_unknown_not_proven_human(
    job, local_push, tmp_path
):
    fixture = local_push
    ready, go, done = (tmp_path / name for name in ("ready", "go", "done"))
    push = fixture.push_command("main")
    output = tmp_path / "push.out"
    command = f'(printf "%s" "$BASHPID" > {ready}; while [ ! -e {go} ]; do sleep .03; done; {push} > {output} 2>&1; printf "%s" "$?" > {done}) & exit 0'
    process = job.start(command)
    record = None
    try:
        child = int(wait_for(lambda: ready.read_text() if ready.exists() else ""))
        record = job.live_record()
        identity = json.loads(record.read_text())
        assert job.identify(child)["status"] == "governed"
        os.kill(identity["pid"], signal.SIGKILL)
        wait_for(lambda: job.identify(child) == _unknown("orphaned", record))
        go.touch()
        assert wait_for(lambda: done.read_text() if done.exists() else "") == "0"
        process.communicate(timeout=10)
        assert process.returncode == 137
        assert fixture.remote_ref("main") == fixture.c
        (row,) = fixture.events()
        assert row["identity"] == _unknown("orphaned", record) and row["refused"] is False
        print(
            json.dumps(
                {
                    "case": "LIMIT-supervisor-kill-unknown-test-policy-allows-only-because-not-positive",
                    "remote_after": fixture.remote_ref("main"),
                    "hook_event": row,
                },
                sort_keys=True,
            )
        )
    finally:
        go.touch()
        if record is not None:
            record.unlink(missing_ok=True)


def test_live_probe_redaction_keeps_only_selector_identity(tmp_path):
    import importlib.util

    path = Path(__file__).parent / "fixtures/launch_level/live_probe.py"
    spec = importlib.util.spec_from_file_location("launch_level_live_probe", path)
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)
    canary = "fixture-private-canary-not-a-real-credential"
    data = {
        "api_key": canary,
        "stdout": "unrelated text "
        + canary
        + "\n"
        + json.dumps({"status": "governed", "session_id": "safe", "command": canary}),
    }
    filtered = probe.identities(data)
    assert filtered == [{"status": "governed", "session_id": "safe"}]
    assert probe.identities(
        {"status": "ordinary", "reason": "released", "extra": canary}
    ) == [{"status": "ordinary", "reason": "released"}]
    log = tmp_path / "redacted.jsonl"
    probe.append(log, {"selector_results": filtered})
    assert canary not in log.read_text()
    assert log.stat().st_mode & 0o777 == 0o600
