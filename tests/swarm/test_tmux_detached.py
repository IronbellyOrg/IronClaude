"""T07.02 -- ``cli/swarm/tmux.py`` detached-run wrapper contract.

Covers the acceptance criteria from
``.dev/releases/Current/MultiModelSwarm/tasklist/phase-7-tasklist.md``:

* ``session_name`` derives ``swarm-<job_id>`` and rejects tmux-illegal
  characters (``:`` / ``.`` / whitespace).
* ``is_tmux_available`` returns False when tmux is missing OR when the
  caller is already inside a tmux session.
* ``has_session`` / ``list_swarm_sessions`` return safe defaults when
  tmux is missing.
* ``attach`` / ``kill`` raise ``TmuxUnavailableError`` when tmux is
  missing; ``attach`` raises ``TmuxSessionMissingError`` for unknown
  job_ids; ``kill`` is idempotent on missing sessions.
* When tmux IS available: ``launch_detached`` spawns a background
  session that survives the launcher exit (verified by killing the
  launching subprocess and confirming ``has_session`` stays True);
  ``kill`` tears it down.
* Module exposes the names required by T07.07 / T07.08 / T07.11.

Tests that require an actual tmux binary are gated on
``shutil.which('tmux')`` -- the suite is "passes or skips cleanly" per
the task's verification clause.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import time
import uuid

import pytest

from superclaude.cli.swarm import tmux as swarm_tmux

TMUX_PRESENT = shutil.which("tmux") is not None
NOT_NESTED = "TMUX" not in os.environ

requires_tmux = pytest.mark.skipif(
    not TMUX_PRESENT,
    reason="tmux binary not installed; detached swarm mode unavailable",
)


# ---------------------------------------------------------------------------
# Pure-Python contract -- runs unconditionally
# ---------------------------------------------------------------------------


def test_session_name_prefix_and_round_trip() -> None:
    assert swarm_tmux.SESSION_PREFIX == "swarm-"
    assert swarm_tmux.session_name("abc123") == "swarm-abc123"


@pytest.mark.parametrize(
    "bad_id",
    ["", "has space", "with:colon", "with.dot", "tab\there", "new\nline"],
)
def test_session_name_rejects_illegal_chars(bad_id: str) -> None:
    with pytest.raises(ValueError):
        swarm_tmux.session_name(bad_id)


def test_exported_surface_matches_consumer_tasks() -> None:
    """T07.07 / T07.08 / T07.11 call these names -- pin the surface."""
    for name in (
        "SESSION_PREFIX",
        "TmuxUnavailableError",
        "TmuxSessionMissingError",
        "is_tmux_available",
        "session_name",
        "has_session",
        "launch_detached",
        "attach",
        "kill",
        "list_swarm_sessions",
    ):
        assert hasattr(swarm_tmux, name), f"public surface missing {name!r}"
        assert name in swarm_tmux.__all__, f"{name!r} not exported in __all__"


def test_is_tmux_available_reflects_path_and_nesting() -> None:
    """Mirrors sprint behavior: True iff tmux on PATH AND not inside tmux."""
    actual = swarm_tmux.is_tmux_available()
    expected = TMUX_PRESENT and NOT_NESTED
    assert actual is expected


def test_error_class_hierarchy() -> None:
    assert issubclass(swarm_tmux.TmuxUnavailableError, RuntimeError)
    assert issubclass(swarm_tmux.TmuxSessionMissingError, LookupError)


def test_launch_detached_rejects_empty_command(monkeypatch) -> None:
    """Empty command must raise before any subprocess call."""
    # Force the tmux-availability branch open so the empty-command
    # ValueError is what actually fires (rather than the missing-tmux
    # guard) on hosts without tmux.
    monkeypatch.setattr(swarm_tmux.shutil, "which", lambda _: "/usr/bin/tmux")
    monkeypatch.setattr(swarm_tmux, "has_session", lambda _job_id: False)
    with pytest.raises(ValueError):
        swarm_tmux.launch_detached("job-x", [])


# ---------------------------------------------------------------------------
# tmux-missing path -- exercised when tmux is genuinely absent
# ---------------------------------------------------------------------------


@pytest.mark.skipif(TMUX_PRESENT, reason="this branch only fires when tmux is absent")
def test_no_tmux_paths_are_safe() -> None:
    assert swarm_tmux.is_tmux_available() is False
    assert swarm_tmux.has_session("anything") is False
    assert swarm_tmux.list_swarm_sessions() == []
    with pytest.raises(swarm_tmux.TmuxUnavailableError):
        swarm_tmux.launch_detached("job-x", ["sleep", "1"])
    with pytest.raises(swarm_tmux.TmuxUnavailableError):
        swarm_tmux.attach("job-x")
    with pytest.raises(swarm_tmux.TmuxUnavailableError):
        swarm_tmux.kill("job-x")


@pytest.mark.skipif(
    TMUX_PRESENT, reason="patched-tmux path covers monkeypatched absence"
)
def test_no_tmux_paths_via_monkeypatch(monkeypatch) -> None:
    """Force the no-tmux branch even when tmux IS installed."""
    monkeypatch.setattr(swarm_tmux.shutil, "which", lambda _: None)
    assert swarm_tmux.is_tmux_available() is False
    assert swarm_tmux.has_session("anything") is False
    assert swarm_tmux.list_swarm_sessions() == []
    with pytest.raises(swarm_tmux.TmuxUnavailableError):
        swarm_tmux.launch_detached("job-x", ["sleep", "1"])
    with pytest.raises(swarm_tmux.TmuxUnavailableError):
        swarm_tmux.attach("job-x")
    with pytest.raises(swarm_tmux.TmuxUnavailableError):
        swarm_tmux.kill("job-x")


# When tmux IS available, still exercise the monkeypatched-no-tmux path so
# the no-tmux branches are covered on CI machines that ship tmux.
@requires_tmux
def test_no_tmux_paths_via_monkeypatch_when_tmux_present(monkeypatch) -> None:
    monkeypatch.setattr(swarm_tmux.shutil, "which", lambda _: None)
    assert swarm_tmux.is_tmux_available() is False
    assert swarm_tmux.has_session("anything") is False
    assert swarm_tmux.list_swarm_sessions() == []
    with pytest.raises(swarm_tmux.TmuxUnavailableError):
        swarm_tmux.launch_detached("job-x", ["sleep", "1"])
    with pytest.raises(swarm_tmux.TmuxUnavailableError):
        swarm_tmux.attach("job-x")
    with pytest.raises(swarm_tmux.TmuxUnavailableError):
        swarm_tmux.kill("job-x")


# ---------------------------------------------------------------------------
# Live-tmux integration -- skipped when tmux missing
# ---------------------------------------------------------------------------


def _unique_job_id() -> str:
    return f"t702-{uuid.uuid4().hex[:10]}"


@pytest.fixture
def live_job_id():
    """Yield a unique job_id and guarantee its tmux session is killed."""
    job_id = _unique_job_id()
    try:
        yield job_id
    finally:
        # Best-effort cleanup; ignore errors so a failed launch does not
        # mask the underlying assertion.
        if TMUX_PRESENT and swarm_tmux.has_session(job_id):
            swarm_tmux.kill(job_id)


@requires_tmux
def test_has_session_false_when_missing(live_job_id: str) -> None:
    assert swarm_tmux.has_session(live_job_id) is False


@requires_tmux
def test_kill_missing_is_idempotent(live_job_id: str) -> None:
    assert swarm_tmux.kill(live_job_id) is False
    assert swarm_tmux.kill(live_job_id) is False


@requires_tmux
def test_attach_missing_raises_session_missing(live_job_id: str) -> None:
    with pytest.raises(swarm_tmux.TmuxSessionMissingError):
        # The "attach" itself never blocks because has_session returns
        # False first; no PTY required.
        swarm_tmux.attach(live_job_id)


@requires_tmux
def test_launch_detached_creates_session_and_kill_tears_down(
    live_job_id: str,
) -> None:
    name = swarm_tmux.launch_detached(live_job_id, ["sleep", "30"])
    assert name == f"swarm-{live_job_id}"
    assert swarm_tmux.has_session(live_job_id) is True
    assert name in swarm_tmux.list_swarm_sessions()

    # Idempotent guard: a second launch_detached with the same job_id
    # must refuse rather than clobber.
    with pytest.raises(RuntimeError):
        swarm_tmux.launch_detached(live_job_id, ["sleep", "30"])

    assert swarm_tmux.kill(live_job_id) is True
    # Give tmux a beat to remove the session record.
    for _ in range(20):
        if not swarm_tmux.has_session(live_job_id):
            break
        time.sleep(0.05)
    assert swarm_tmux.has_session(live_job_id) is False
    # Second kill -> no-op.
    assert swarm_tmux.kill(live_job_id) is False


@requires_tmux
def test_detached_session_survives_caller_exit(tmp_path) -> None:
    """AC-008 / FR-014 -- detached session must outlive the launching process.

    We spawn a short-lived Python subprocess that calls
    ``launch_detached`` and immediately exits. After the subprocess is
    gone, the tmux session must still be live until we kill it.
    """
    job_id = _unique_job_id()
    launcher = subprocess.run(
        [
            "python",
            "-c",
            (
                "from superclaude.cli.swarm import tmux as t;"
                f"print(t.launch_detached({job_id!r}, ['sleep', '30']))"
            ),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        assert launcher.returncode == 0, (
            f"launcher failed: stdout={launcher.stdout!r} stderr={launcher.stderr!r}"
        )
        assert launcher.stdout.strip() == f"swarm-{job_id}"
        # Launching process has exited; session must still be live.
        assert swarm_tmux.has_session(job_id) is True
    finally:
        if swarm_tmux.has_session(job_id):
            swarm_tmux.kill(job_id)


def _completion_spec(tmp_path, enabled=True):
    import json

    from superclaude.cli.swarm.commands import _build_spec_from_lens

    spec = _build_spec_from_lens("bare-review")
    spec["job_id"] = "completion-" + uuid.uuid4().hex[:12]
    target = tmp_path / "target.txt"
    target.write_text("Review this isolated completion test target.\n" * 10)
    spec["target"]["path"] = str(target)
    spec["output"]["dir"] = str(tmp_path / "out")
    spec["transport"]["kind"] = "stub"
    spec["runtime"]["on_completion"]["write_done_sentinel"] = enabled
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec))
    return spec, path


@pytest.mark.parametrize("enabled", [False, True])
@pytest.mark.parametrize("relative_output", [False, True])
def test_detached_parent_defers_completion_to_actual_child(
    tmp_path, monkeypatch, enabled, relative_output
):
    import json
    from pathlib import Path

    from click.testing import CliRunner

    from superclaude.cli.swarm.commands import run_cmd

    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    spec, path = _completion_spec(tmp_path, enabled)
    out = tmp_path / "out"
    requests = []
    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: True)

    def launch(job_id, argv, **kwargs):
        assert not (out / "done.json").exists()
        requests.append(argv)
        return swarm_tmux.session_name(job_id)

    monkeypatch.setattr(swarm_tmux, "launch_detached", launch)
    monkeypatch.chdir(tmp_path)
    parent = CliRunner().invoke(
        run_cmd,
        [str(path), "--detached", "--output", "out" if relative_output else str(out)],
    )
    assert parent.exit_code == 0, parent.output
    assert not (out / "done.json").exists()
    assert len(requests) == 1
    snapshot = Path(requests[0][-1])
    assert snapshot.is_absolute()
    assert requests[0][5:7] == ["--output", str(out.resolve())]
    assert (
        json.loads(snapshot.read_text())["runtime"]["on_completion"][
            "write_done_sentinel"
        ]
        is enabled
    )
    # Execute precisely the captured child request, not a repaired test-only argv.
    child = CliRunner().invoke(run_cmd, requests[0][5:])
    assert child.exit_code == 0, child.output
    assert (out / "done.json").exists() is enabled
    assert (out / "return-contract.yaml").is_file()
    assert json.loads((out / ".swarm-state.json").read_text())["state"] == "terminal"
    if enabled:
        import yaml

        marker = json.loads((out / "done.json").read_text())
        assert (
            marker["terminal_status"]
            == yaml.safe_load((out / "return-contract.yaml").read_text())["status"]
        )
        assert marker["contract_path"] == str((out / "return-contract.yaml").resolve())
        assert (
            json.loads((out / ".swarm-state.json").read_text())["state"] == "terminal"
        )


@requires_tmux
@pytest.mark.skipif(
    not NOT_NESTED, reason="nested tmux does not support detached launch"
)
def test_detached_live_cli_child_publishes_completion(tmp_path, monkeypatch):
    import json
    import sys
    from pathlib import Path

    spec, path = _completion_spec(tmp_path)
    out = tmp_path / "out"
    home = tmp_path / "home"
    home.mkdir()
    env = dict(
        os.environ,
        HOME=str(home),
        PYTHONPATH=str(Path(__file__).resolve().parents[2] / "src"),
        PYTHONDONTWRITEBYTECODE="1",
    )
    command = [
        "uv",
        "run",
        "--no-project",
        "--python",
        sys.executable,
        "superclaude",
        "swarm",
        "run",
        str(path),
        "--detached",
        "--output",
        str(out),
    ]
    result = subprocess.run(
        command, capture_output=True, text=True, env=env, timeout=30
    )
    try:
        assert result.returncode == 0, result.stdout + result.stderr
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline and not (out / "done.json").exists():
            if not swarm_tmux.has_session(spec["job_id"]):
                break
            time.sleep(0.1)
        assert (out / "done.json").is_file(), (
            f"child ended without completion: {sorted(p.name for p in out.iterdir())}"
        )
        import yaml

        marker = json.loads((out / "done.json").read_text())
        assert (
            marker["terminal_status"]
            == yaml.safe_load((out / "return-contract.yaml").read_text())["status"]
            == "success"
        )
        assert (
            json.loads((out / ".swarm-state.json").read_text())["state"] == "terminal"
        )
    finally:
        if swarm_tmux.has_session(spec["job_id"]):
            swarm_tmux.kill(spec["job_id"])
