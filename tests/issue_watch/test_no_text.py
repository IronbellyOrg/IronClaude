"""No GitHub text reaches the watcher's output (design T1 and T11, NFR-001, NFR-006).

Hostile replies carry the canary ``PWNED-TITLE`` as a label name, as an
assignee or actor login, inside non-JSON ``gh`` stdout, inside ``gh`` stderr
longer than 500 bytes on a failing call, in extra ``title`` and ``body`` fields
and in wrong-typed fields. Whole ``once`` cycles (real and dry-run) and the
``status`` command run over them through the real CLI, and the canary must never
appear in any file under the state directory (rotated audit files included), in
any recorded argv, prompt or launch argument, or in the captured output of the
commands. The audit lines keep a closed key set, the real runner keeps at most
500 bytes of stderr, and no ``gh`` argv asks for title, body or comment text.

Every scenario proves the canary was served to the code (``SpyRunner``), so a
pass cannot come from text that never entered. The checkers are fed bad input
in their own tests, so they cannot pass vacuously.
"""

from __future__ import annotations

import dataclasses
import json
import re
import sys
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.issue_watch import audit, cli, cycle, github, launch
from superclaude.cli.issue_watch import runner as runner_mod
from superclaude.cli.issue_watch.cli import issue_watch_group
from superclaude.cli.issue_watch.launch import LaunchOutcome, OrcaLauncher
from superclaude.cli.issue_watch.runner import CommandResult, SubprocessRunner

from .conftest import (
    APPROVER_ID,
    CYCLE_NOW,
    ORCA_PATH,
    ORIGIN_URL,
    OWN_LOGIN,
    T_APPROVED,
    T_TRIGGER,
    FailingStore,
    FakeClock,
    FakeLauncher,
    FakeRunner,
    GhWorld,
    default_events,
    label_event,
    load_fixture,
    make_config,
    marker_comment,
    write_scenario,
)
from .conftest import result as command_result

# The real assembly, taken at import before any test patches ``cli.build_deps``.
_REAL_BUILD_DEPS = cli.build_deps

SENT = "PWNED-TITLE"
STEM = "PWNED"  # a shorter needle also catches a truncated or re-cased copy
HOSTILE_PAD = "x" * 600
PROMPT_SHAPE = re.compile(r"^/sc:issue --claim [1-9][0-9]{0,8}$")
LOCAL_MOUNTINFO = "1 0 0:1 / / rw - ext4 /dev/sda1 rw\n"
FILLER = "#"  # first character of the padding line the rotation test writes

# The closed audit schema, written out here so the test does not read it from the
# module it checks (audit.py ``_COMMON`` and ``_KEYS``).
_COMMON_KEYS = {"kind", "ts", "host", "login", "cycle_id", "dry_run", "reason"}
CLOSED_KEYS = {
    "cycle": _COMMON_KEYS
    | {"exit", "gh_calls", "duration_ms", "discovery_count", "clock_skew_s"},
    "decision": _COMMON_KEYS
    | {"issue", "approver_id", "approval_event_id", "approved_at", "state", "note"},
    "warning": _COMMON_KEYS | {"issue", "discovery_count", "clock_skew_s"},
}
FALLBACK_KEYS = {"kind", "ts", "host", "exit", "reason"}


def hostile_stderr(sign: str = "") -> str:
    """More than 500 bytes of stderr with the canary first and ``sign`` after it."""
    text = f"{SENT} {sign} {HOSTILE_PAD}"
    assert len(text.encode("utf-8")) > 500
    return text


# ==============================================================================
# The checkers
# ==============================================================================


def audit_files(state_dir: Path) -> list[Path]:
    """``audit.jsonl`` and every rotated file."""
    return sorted(state_dir.glob("audit.jsonl*"))


def read_audit(state_dir: Path) -> list[dict]:
    """Every audit line of every audit file, parsed; padding lines are skipped."""
    lines: list[dict] = []
    for path in audit_files(state_dir):
        for raw in path.read_text("utf-8").splitlines():
            if not raw.startswith(FILLER):
                lines.append(json.loads(raw))
    return lines


def assert_closed_audit(lines: Iterable[dict]) -> None:
    """Every line has a known kind, only keys of that kind, scalars and a known reason."""
    for ln in lines:
        assert ln["kind"] in CLOSED_KEYS, ln
        extra = set(ln) - CLOSED_KEYS[ln["kind"]]
        assert not extra, f"audit keys outside the closed set: {sorted(extra)}"
        assert ln["reason"] in audit.REASONS, ln
        assert all(isinstance(v, (str, int, bool, type(None))) for v in ln.values()), ln


def assert_state_dir_clean(state_dir: Path, skip: tuple[str, ...] = ()) -> list[Path]:
    """Scan every file under ``state_dir`` (``Path.rglob``) for the canary bytes."""
    files = [p for p in sorted(state_dir.rglob("*")) if p.is_file()]
    for path in files:
        if path.name in skip:
            continue
        assert STEM.encode() not in path.read_bytes().upper(), (
            f"the canary reached {path}"
        )
    return files


_TEXT_WORDS = re.compile(r"\b(title|body|bodyText|bodyHTML|text|message|rename)\b")
_MARKER_BOOLEAN = re.compile(r'\(\.body \| contains\("[^"]*"\)\)')
_JSON_FIELDS = {"number", "labels", "assignees", "state"}


def text_requests(argv: Iterable[str]) -> list[str]:
    """Reasons this ``gh`` argv could return issue title, body or comment text."""
    argv = list(argv)
    if not argv or argv[0] != "gh":
        return []
    found: list[str] = []
    if argv[1:2] == ["issue"]:
        if "--json" not in argv:
            found.append("gh issue without --json prints titles")
        else:
            fields = set(argv[argv.index("--json") + 1].split(","))
            if fields - _JSON_FIELDS:
                found.append(f"--json fields {sorted(fields - _JSON_FIELDS)}")
    if "--template" in argv or "-t" in argv:
        found.append("a --template")
    jq = None
    for flag in ("--jq", "-q"):
        if flag in argv:
            jq = argv[argv.index(flag) + 1]
            if _TEXT_WORDS.search(_MARKER_BOOLEAN.sub("", jq)):
                found.append(f"{flag} names a text field: {jq}")
    if any(a.startswith("repos/") for a in argv) and jq is None:
        found.append("a REST path without --jq returns the whole body")
    for a in argv:
        if a.startswith("query=") and _TEXT_WORDS.search(a):
            found.append("a GraphQL query names a text field")
    return found


class SpyRunner(FakeRunner):
    """A ``FakeRunner`` that also keeps every reply it served."""

    def __init__(self, script=None) -> None:
        super().__init__(script)
        self.served: list[CommandResult] = []

    def run(
        self, argv: list[str], timeout: float, *, cwd: str | None = None
    ) -> CommandResult:
        reply = super().run(argv, timeout, cwd=cwd)
        self.served.append(reply)
        return reply

    def canary_served(self) -> bool:
        """True when a reply handed to the code held the canary."""
        return any(
            SENT in r.stdout or SENT in r.stderr or SENT in (r.spawn_error or "")
            for r in self.served
        )


def assert_no_text(
    state_dir: Path,
    outputs: dict[str, str],
    spy: SpyRunner,
    launcher: FakeLauncher | None = None,
    skip: tuple[str, ...] = (),
) -> None:
    """The whole no-text invariant over one scenario."""
    assert_state_dir_clean(state_dir, skip)
    for label, text in outputs.items():
        assert STEM not in text.upper(), f"the canary reached {label}: {text!r}"
    argvs = [argv for argv, _cwd in spy.calls]
    if launcher is not None:
        argvs += launcher.argvs
        assert STEM not in repr(launcher.calls)
    for argv in argvs:
        assert not any(STEM in a.upper() for a in argv), argv
        assert text_requests(argv) == [], argv
        if "--prompt" in argv:
            assert PROMPT_SHAPE.fullmatch(argv[argv.index("--prompt") + 1]), argv
    assert_closed_audit(read_audit(state_dir))


# ==============================================================================
# Running a scenario through the real CLI
# ==============================================================================


def write_config(path: Path, config: cycle.Config) -> Path:
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "enabled": config.enabled,
                "project_id": config.project_id,
                "worktree": str(config.worktree),
                "approvers_file": str(config.approvers_file),
                "state_dir": str(config.state_dir),
            }
        ),
        encoding="utf-8",
    )
    return path


def invoke(*args: str):
    """Run ``issue-watch <args>``; anything but a clean exit is a test failure."""
    out = CliRunner().invoke(issue_watch_group, list(args))
    assert out.exception is None or isinstance(out.exception, SystemExit), repr(
        out.exception
    )
    return out


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    """HOME, XDG and mountinfo stay local for every test of this file."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    monkeypatch.setattr(cycle, "_read_mountinfo", lambda: LOCAL_MOUNTINFO)


def refuse_real_processes(monkeypatch) -> list[tuple[str, ...]]:
    """Make ``SubprocessRunner.run`` fail the test; returns the argvs it was given."""
    calls: list[tuple[str, ...]] = []

    def refuse(self, argv, timeout, *, cwd=None):
        calls.append(tuple(argv))
        raise AssertionError(f"a real subprocess call was attempted: {argv!r}")

    monkeypatch.setattr(runner_mod.SubprocessRunner, "run", refuse)
    return calls


@dataclass(frozen=True)
class Scenario:
    id: str
    setup: Callable[[GhWorld], None]
    dry_ok: bool = True  # False: the canary only arrives at a step a dry-run skips
    real_launcher: bool = False  # True: launch through OrcaLauncher over the spy
    expect_state: str | None = None  # state of issue 7 after a real (not dry) cycle


def _launched_every_time(n: int) -> LaunchOutcome:
    return LaunchOutcome("launched", f"op-test-{n:04d}", "ok")


class Run:
    """One scenario's world, deps, launcher and command outputs."""

    def __init__(self, tmp_path, tmp_state, monkeypatch, sc: Scenario | None = None):
        self.tmp_path = tmp_path
        self.state_dir = tmp_state.state_dir
        self.spy = SpyRunner()
        self.world = GhWorld(
            FakeClock(CYCLE_NOW), make_config(tmp_path), runner=self.spy
        )
        self.world.issue(7)
        if sc is not None:
            sc.setup(self.world)
        self.launcher = FakeLauncher(_launched_every_time)
        deps = self.world.deps(tmp_path, tmp_state, launcher=self.launcher)
        if sc is not None and sc.real_launcher:
            deps = dataclasses.replace(deps, launcher=OrcaLauncher(self.spy))
        self.deps = deps
        self.config_path = write_config(tmp_path / "cfg.json", self.world.config)
        self.outputs: dict[str, str] = {}
        self.real_calls = refuse_real_processes(monkeypatch)
        monkeypatch.setattr(cli, "build_deps", lambda config: self.deps)

    def command(self, label: str, *args: str):
        out = invoke(*args, "--config", str(self.config_path))
        self.outputs[label] = out.output
        return out

    def once(self, dry: bool = False, label: str = "once"):
        return self.command(label, "once", *(["--dry-run"] if dry else []))

    def status(self):
        self.command("status", "status")
        self.command("status --json", "status", "--json")

    def check(self, skip: tuple[str, ...] = ()) -> None:
        assert_no_text(self.state_dir, self.outputs, self.spy, self.launcher, skip)


# ==============================================================================
# Scenarios: the canary in every kind of reply the cycle reads
# ==============================================================================

PER_ISSUE = ("comments", "events", "edits", "items", "reread")
LAUNCH_ONLY = ("probe", "reread")  # called only when a launch is attempted
SIGNS = (
    "",
    "HTTP 401 gh auth login",
    "HTTP 429 rate limit",
    "HTTP 403",
    "read:project",
    "HTTP 502",
)


def _fail(world: GhWorld, call: str, reply: CommandResult) -> None:
    world.fail(call, reply, 7 if call in PER_ISSUE else None, times=None)


def _hostile_label_names(world: GhWorld) -> None:
    cfg = world.config
    events = default_events(cfg) + [
        label_event(
            3,
            "labeled",
            SENT,
            T_APPROVED + timedelta(minutes=1),
            actor_login=SENT,
            title=SENT,
        ),
        label_event(4, "unlabeled", SENT, T_APPROVED + timedelta(minutes=2)),
    ]
    world.issue(
        7,
        labels=[cfg.trigger_label, cfg.approval_label, SENT],
        events=events,
        discovered={"title": SENT, "body": SENT},
        reread={"title": SENT, "body": SENT},
    )


def _hostile_logins(world: GhWorld) -> None:
    cfg = world.config
    events = [
        label_event(
            1,
            "labeled",
            cfg.trigger_label,
            T_TRIGGER,
            actor_id=2001,
            actor_login=SENT,
        ),
        label_event(
            2,
            "labeled",
            cfg.approval_label,
            T_APPROVED,
            actor_id=APPROVER_ID,
            actor_login=SENT,
        ),
    ]
    world.issue(6, assignees=[OWN_LOGIN, SENT])  # assigned_other
    world.issue(
        7,
        events=events,
        markers=[marker_comment(60, T_TRIGGER, login=SENT, marker=True, body=SENT)],
        edits={
            "comments": [
                {"id": 61, "author": SENT, "created_at": T_TRIGGER, "edited_at": None}
            ]
        },
    )


def _hostile_extra_fields(world: GhWorld) -> None:
    world.issue(
        7,
        markers=[
            marker_comment(70, T_TRIGGER, login="someone", marker=False, body=SENT)
        ],
        discovered={"title": SENT, "body": SENT, "url": SENT},
        reread={"title": SENT, "body": SENT},
    )


def _build_scenarios() -> list[Scenario]:
    out = [
        Scenario("label_names", _hostile_label_names),
        Scenario("login_like_strings", _hostile_logins),
        Scenario("extra_text_fields", _hostile_extra_fields),
        Scenario(
            "malformed_discovery_number",
            lambda w: w.issue(7, discovered={"number": SENT}),
        ),
        Scenario(
            "malformed_event_time",
            lambda w: w.issue(
                7,
                events=default_events(w.config)
                + [label_event(3, "labeled", SENT, SENT)],
            ),
        ),
        Scenario(
            "malformed_edit_time",
            lambda w: w.issue(7, edits={"created_at": SENT}),
        ),
        Scenario(
            "malformed_project_item",
            lambda w: w.issue(7, items=[{"project_id": SENT, "status": SENT}]),
        ),
        Scenario(
            "malformed_reread_state",
            lambda w: w.issue(7, reread={"state": SENT}),
            dry_ok=False,
        ),
        Scenario(
            "spawn_error_text",
            lambda w: _fail(w, "discover", command_result(spawn_error=SENT)),
        ),
        Scenario(
            "timeout_with_stderr",
            lambda w: _fail(
                w, "events", command_result(timed_out=True, stderr=hostile_stderr())
            ),
        ),
    ]
    for call in ("user", "discover", "origin", "probe", *PER_ISSUE):
        out.append(
            Scenario(
                f"non_json_stdout_{call}",
                lambda w, c=call: _fail(
                    w, c, command_result(stdout=f"{SENT} <html>not json</html>")
                ),
                dry_ok=call not in LAUNCH_ONLY,
            )
        )
        for number, sign in enumerate(SIGNS):
            out.append(
                Scenario(
                    f"stderr_{call}_{number}",
                    lambda w, c=call, s=sign: _fail(
                        w, c, command_result(stderr=hostile_stderr(s), returncode=1)
                    ),
                    dry_ok=call not in LAUNCH_ONLY,
                )
            )
    return out


def _orca_reply(world: GhWorld, reply: CommandResult) -> None:
    argv = launch.launch_argv(ORCA_PATH, world.config.worktree, "/sc:issue --claim 7")
    world.runner.script[tuple(argv)] = reply


LAUNCH_SCENARIOS = [
    Scenario(
        "launch_non_json",
        lambda w: _orca_reply(w, command_result(stdout=f"{SENT} started")),
        dry_ok=False,
        real_launcher=True,
    ),
    Scenario(
        "launch_stderr_over_500_bytes",
        lambda w: _orca_reply(
            w, command_result(stderr=hostile_stderr("failed"), returncode=1)
        ),
        dry_ok=False,
        real_launcher=True,
    ),
    Scenario(
        "launch_operation_unknown_text",
        lambda w: _orca_reply(
            w,
            command_result(
                stderr=f"{launch.OP_UNKNOWN_TEXT} {hostile_stderr()}", returncode=1
            ),
        ),
        dry_ok=False,
        real_launcher=True,
    ),
    Scenario(
        "launch_ok_with_text_fields",
        lambda w: _orca_reply(
            w,
            command_result(
                # [UNVERIFIED, assumed shape] the reply comes from the fixture
                # (design 636, 840) so FU-1 changes it in one place.
                stdout=json.dumps(
                    {
                        **load_fixture("orca_launch_success.json")["payload"],
                        "title": SENT,
                        "body": SENT,
                    }
                )
            ),
        ),
        dry_ok=False,
        real_launcher=True,
        expect_state="launched",
    ),
]

SCENARIOS = _build_scenarios() + LAUNCH_SCENARIOS
CASES = [(sc, False) for sc in SCENARIOS] + [
    (sc, True) for sc in SCENARIOS if sc.dry_ok
]


@pytest.mark.parametrize(
    "sc,dry",
    CASES,
    ids=[f"{sc.id}-{'dry' if dry else 'real'}" for sc, dry in CASES],
)
def test_canary_never_leaves_a_hostile_cycle(sc, dry, tmp_path, tmp_state, monkeypatch):
    run = Run(tmp_path, tmp_state, monkeypatch, sc)
    once = run.once(dry)
    run.status()
    # The text entered the code, a cycle line was written, and no launch was
    # attempted in a dry-run, so the scan below is not vacuous.
    assert run.spy.canary_served(), f"{sc.id}: the canary never reached the code"
    assert any(ln["kind"] == "cycle" for ln in read_audit(run.state_dir))
    if dry:
        assert run.launcher.calls == []
        assert not any(
            c[0][:3] == (ORCA_PATH, "agent", "launch") for c in run.spy.calls
        )
    elif sc.expect_state is not None:
        # The scenario names a launch success; a changed reply shape that turns
        # it into an ``unknown`` launch must fail here, not pass unnoticed.
        assert tmp_state.load().entries[7].state == sc.expect_state, sc.id
    run.check()
    assert "cycle:" in once.output


def test_a_launching_cycle_records_the_prompt_and_stays_clean(
    tmp_path, tmp_state, monkeypatch
):
    """The label-name scenario really launches, so the argv scan has a launch to scan."""
    sc = next(s for s in SCENARIOS if s.id == "label_names")
    run = Run(tmp_path, tmp_state, monkeypatch, sc)
    out = run.once()
    run.status()
    assert out.exit_code == 0 and "cycle: cycle_complete" in out.output
    assert [c[2] for c in run.launcher.calls] == ["/sc:issue --claim 7"]
    assert run.launcher.argvs[0][run.launcher.argvs[0].index("--prompt") + 1] == (
        "/sc:issue --claim 7"
    )
    assert run.spy.canary_served()
    run.check()


def test_a_dry_run_writes_the_shadow_file_and_it_stays_clean(
    tmp_path, tmp_state, monkeypatch
):
    sc = next(s for s in SCENARIOS if s.id == "label_names")
    run = Run(tmp_path, tmp_state, monkeypatch, sc)
    out = run.once(dry=True)
    assert "would_launch: 7" in out.output
    names = {p.name for p in assert_state_dir_clean(run.state_dir)}
    assert {"dispatch.json", "dry-run.json", "audit.jsonl"} <= names
    run.check()


def test_status_after_an_unknown_launch_prints_no_canary(
    tmp_path, tmp_state, monkeypatch
):
    """An ``unknown`` entry makes ``status`` print more (stale, retry), still no text."""
    sc = next(s for s in SCENARIOS if s.id == "launch_operation_unknown_text")
    run = Run(tmp_path, tmp_state, monkeypatch, sc)
    out = run.once()
    assert out.exit_code == 7
    run.status()
    assert "counts: unknown=1" in run.outputs["status"]
    assert run.spy.canary_served()
    run.check()


# ==============================================================================
# Rotated audit files
# ==============================================================================


def test_rotated_audit_files_are_scanned_and_stay_clean(
    tmp_path, tmp_state, monkeypatch
):
    sc = Scenario(
        "events_stderr",
        lambda w: _fail(
            w, "events", command_result(stderr=hostile_stderr("HTTP 502"), returncode=1)
        ),
    )
    run = Run(tmp_path, tmp_state, monkeypatch, sc)
    run.once(label="once 1")
    first_ids = {ln["cycle_id"] for ln in read_audit(run.state_dir)}
    assert first_ids
    log = run.state_dir / "audit.jsonl"
    with open(log, "ab") as handle:  # push it past the rotation size
        handle.write((FILLER * audit.ROTATE_BYTES + "\n").encode("ascii"))
    run.once(label="once 2")
    rotated = run.state_dir / "audit.jsonl.1"
    assert rotated.exists(), "the second cycle did not rotate the audit log"
    in_rotated = {
        json.loads(raw)["cycle_id"]
        for raw in rotated.read_text("utf-8").splitlines()
        if not raw.startswith(FILLER)
    }
    assert first_ids <= in_rotated
    assert rotated in assert_state_dir_clean(run.state_dir)
    assert run.spy.canary_served()
    run.check()


# ==============================================================================
# Errors and the crash line
# ==============================================================================


def test_crash_line_names_the_exception_class_never_its_text(
    tmp_path, tmp_state, monkeypatch
):
    sc = next(s for s in SCENARIOS if s.id == "label_names")
    run = Run(tmp_path, tmp_state, monkeypatch, sc)
    failing = FailingStore(
        tmp_state, fail_saves=(1,), error=RuntimeError(f"boom {SENT}")
    )
    run.deps = dataclasses.replace(run.deps, store=failing)
    out = run.once()
    assert SENT in str(failing.error) and failing.saves == 1
    assert out.exit_code == 1
    assert "cycle_crashed: RuntimeError" in out.output
    (fallback,) = [json.loads(x) for x in out.output.splitlines() if x.startswith("{")]
    assert set(fallback) == FALLBACK_KEYS and fallback["reason"] == "cycle_crashed"
    assert run.spy.canary_served()
    run.check()


def test_a_crash_inside_a_gh_call_prints_no_exception_text(
    tmp_path, tmp_state, monkeypatch
):
    run = Run(tmp_path, tmp_state, monkeypatch)
    discover = tuple(github.argv_discover(run.world.config.trigger_label, OWN_LOGIN))

    def explode(argv, cwd):
        raise ValueError(f"explode {SENT}")

    run.spy.script[discover] = explode
    out = run.once()
    assert out.exit_code == 1 and "cycle_crashed: ValueError" in out.output
    run.check()


def test_a_build_deps_failure_prints_no_exception_text(
    tmp_path, tmp_state, monkeypatch
):
    run = Run(tmp_path, tmp_state, monkeypatch)

    def broken(config):
        raise OSError(f"cannot build {SENT}")

    monkeypatch.setattr(cli, "build_deps", broken)
    out = run.once()
    assert out.exit_code == 1 and "cycle_crashed: OSError" in out.output
    run.check()


DAMAGED_STORES = {
    "invalid_json": f'{{"schema_version": 1, "entries": {{"{SENT}": ',
    "text_in_version": json.dumps({"schema_version": SENT, "entries": {}}),
    "text_in_entries": json.dumps({"schema_version": 1, "entries": {SENT: {}}}),
}


@pytest.mark.parametrize("name", sorted(DAMAGED_STORES))
def test_a_damaged_store_is_reported_by_reason_only(
    name, tmp_path, tmp_state, monkeypatch
):
    """The store file holds the canary, so only its reason may reach the outputs."""
    run = Run(tmp_path, tmp_state, monkeypatch)
    (run.state_dir / "dispatch.json").write_text(DAMAGED_STORES[name], encoding="utf-8")
    once = run.once()
    status = run.command("status", "status")
    status_json = run.command("status --json", "status", "--json")
    assert once.exit_code == 6 and "cycle: store_invalid" in once.output
    assert status.exit_code == 6 and status_json.exit_code == 6
    assert "store_invalid" in status.output
    assert SENT in (run.state_dir / "dispatch.json").read_text("utf-8")
    run.check(skip=("dispatch.json",))


# ==============================================================================
# The real runner and the real process boundary
# ==============================================================================


def test_real_runner_keeps_at_most_500_bytes_of_stderr():
    code = f"import sys; sys.stderr.write({SENT!r} + 'x' * 2000); sys.exit(1)"
    got = SubprocessRunner().run([sys.executable, "-I", "-S", "-c", code], 30)
    assert got.returncode == 1
    assert got.stderr.startswith(SENT), "the canary did not reach the runner"
    assert len(got.stderr.encode("utf-8")) == runner_mod.STDERR_CAP_BYTES == 500


def test_real_runner_cuts_stderr_on_a_character_boundary():
    code = "import sys; sys.stderr.buffer.write('é'.encode() * 1000); sys.exit(1)"
    got = SubprocessRunner().run([sys.executable, "-I", "-S", "-c", code], 30)
    assert 0 < len(got.stderr.encode("utf-8")) <= 500
    assert "�" not in got.stderr and set(got.stderr) == {"é"}


def test_real_runner_caps_stderr_of_a_timed_out_command():
    code = (
        f"import sys, time; sys.stderr.write({SENT!r} + 'x' * 2000); "
        "sys.stderr.flush(); time.sleep(60)"
    )
    got = SubprocessRunner().run([sys.executable, "-I", "-S", "-c", code], 3.0)
    assert got.timed_out and got.returncode is None
    assert len(got.stderr.encode("utf-8")) <= 500


class _RecordingRunner:
    """Keeps every ``CommandResult`` of the runner it wraps."""

    def __init__(self, inner) -> None:
        self.inner = inner
        self.results: list[CommandResult] = []

    def run(self, argv, timeout, *, cwd=None):
        got = self.inner.run(argv, timeout, cwd=cwd)
        self.results.append(got)
        return got


def test_once_over_real_processes_keeps_500_bytes_and_prints_no_stderr_text(
    tmp_path, tmp_state, stub_path, monkeypatch
):
    """The real runner and the real CLI assembly over PATH stubs: ``gh`` fails with
    more than 500 bytes of stderr holding the canary, and none of it escapes."""
    for key, value in stub_path.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setattr(cycle, "_read_mountinfo", lambda: LOCAL_MOUNTINFO)
    write_scenario(
        tmp_path,
        {
            "gh": [
                {
                    "argv_prefix": ["api", "user", "--include"],
                    "stdout": load_fixture("gh_api_user_include.json")["raw"],
                },
                {
                    "argv_prefix": ["issue", "list"],
                    "stderr": hostile_stderr("HTTP 502"),
                    "exit": 1,
                },
            ],
            "git": [{"argv_prefix": ["-C"], "stdout": ORIGIN_URL + "\n"}],
        },
    )
    recorded: list[_RecordingRunner] = []

    def build(config):
        deps = _REAL_BUILD_DEPS(config)
        spy = _RecordingRunner(deps.runner)
        recorded.append(spy)
        return dataclasses.replace(deps, runner=spy, launcher=OrcaLauncher(spy))

    monkeypatch.setattr(cli, "build_deps", build)
    config = make_config(tmp_path)
    path = write_config(tmp_path / "cfg.json", config)
    out = invoke("once", "--config", str(path))
    status = invoke("status", "--config", str(path))
    (spy,) = recorded
    (discover,) = [r for r in spy.results if r.argv[:3] == ("gh", "issue", "list")]
    assert discover.returncode == 1
    assert discover.stderr.startswith(SENT), "the canary did not reach the runner"
    assert len(discover.stderr.encode("utf-8")) == 500
    assert out.exit_code != 0 and "cycle:" in out.output
    for text in (out.output, status.output):
        assert STEM not in text.upper()
    assert_state_dir_clean(tmp_state.state_dir)
    assert_closed_audit(read_audit(tmp_state.state_dir))
    assert any(ln["kind"] == "cycle" for ln in read_audit(tmp_state.state_dir))


# ==============================================================================
# No code path asks gh for title, body or comment text
# ==============================================================================


def _every_builder_argv() -> list[list[str]]:
    cfg = cycle.DEFAULT_TRIGGER_LABEL
    argvs = [github.argv_user(), github.argv_discover(cfg, OWN_LOGIN)]
    for page in range(1, github.PAGE_CAP + 1):
        argvs.append(github.argv_events(7, page))
        argvs.append(github.argv_comments(7, page))
    for after in (None, "Y3Vyc29yOjE="):
        argvs.append(github.argv_edits(7, after))
        argvs.append(github.argv_project_items(7, after))
    argvs.append(github.argv_reread(7))
    return argvs


def test_no_argv_builder_asks_gh_for_text():
    argvs = _every_builder_argv()
    assert len(argvs) == 2 + 2 * github.PAGE_CAP + 4 + 1
    for argv in argvs:
        assert text_requests(argv) == [], argv
    # The one allowed use of ``.body`` is the boolean marker test of G4.
    assert "contains" in github.MARKER_JQ and ".body" in github.MARKER_JQ
    assert text_requests(github.argv_comments(7, 1)) == []


@pytest.mark.parametrize(
    "argv",
    [
        ["gh", "issue", "list", "--json", "number,title"],
        ["gh", "issue", "list", "--json", "number,labels,body"],
        ["gh", "issue", "list"],
        ["gh", "issue", "view", "7", "--json", "comments"],
        ["gh", "api", "--method", "GET", "repos/o/r/issues/7/comments"],
        ["gh", "api", "--method", "GET", "repos/o/r/issues/7", "--jq", "{title}"],
        ["gh", "api", "--method", "GET", "repos/o/r/issues/7", "-q", ".body"],
        [
            "gh",
            "api",
            "--method",
            "GET",
            "repos/o/r/issues/7",
            "--jq",
            ".body | length",
        ],
        ["gh", "api", "graphql", "-f", "query=query { issue { title } }"],
        [
            "gh",
            "api",
            "graphql",
            "-f",
            "query=query { comments { nodes { bodyText } } }",
        ],
        ["gh", "issue", "list", "--json", "number", "--template", "{{.title}}"],
    ],
)
def test_the_text_request_scan_flags_each_bad_argv(argv):
    assert text_requests(argv) != []


# ==============================================================================
# Mutation guards: the checkers must fail on what they exist to catch
# ==============================================================================


def test_state_scan_flags_the_canary_in_any_file_including_rotated_ones(tmp_path):
    for name in (
        "dispatch.json",
        "dry-run.json",
        "audit.jsonl",
        "audit.jsonl.3",
        "x/y",
    ):
        state = tmp_path / name.replace("/", "_")
        state.mkdir()
        target = state / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f'{{"k": "{SENT}"}}\n', encoding="utf-8")
        with pytest.raises(AssertionError):
            assert_state_dir_clean(state)
        assert assert_state_dir_clean(state, skip=(target.name,)) == [target]


def test_output_scan_flags_the_canary_in_every_kind_of_output(tmp_path, tmp_state):
    spy = SpyRunner()
    state = tmp_state.state_dir
    for label in ("once", "status", "status --json"):
        with pytest.raises(AssertionError):
            assert_no_text(state, {label: f"x {SENT} y"}, spy)
    assert_no_text(state, {"once": "cycle: cycle_complete"}, spy)


def test_argv_scan_flags_a_canary_or_a_bad_prompt_in_a_recorded_call(
    tmp_path, tmp_state
):
    state = tmp_state.state_dir
    spy = SpyRunner()
    spy.calls.append((("gh", "api", "user", SENT), None))
    with pytest.raises(AssertionError):
        assert_no_text(state, {}, spy)
    spy = SpyRunner()
    spy.calls.append(
        (("orca", "agent", "launch", "--prompt", "/sc:issue --claim x"), None)
    )
    with pytest.raises(AssertionError):
        assert_no_text(state, {}, spy)
    launcher = FakeLauncher(_launched_every_time)
    launcher.calls.append(("orca", "wt", f"/sc:issue --claim 1 {SENT}", 1.0))
    with pytest.raises(AssertionError):
        assert_no_text(state, {}, SpyRunner(), launcher)


def test_closed_key_check_flags_an_extra_key_and_an_unknown_reason():
    good = {
        "kind": "warning",
        "ts": "2026-11-07T13:00:00Z",
        "host": "h",
        "login": None,
        "cycle_id": "0" * 32,
        "dry_run": False,
        "reason": "clock_skew",
    }
    assert_closed_audit([good])
    for bad in (
        {**good, "title": "x"},
        {**good, "stderr": "x"},
        {**good, "labels": ["x"]},
        {**good, "reason": SENT},
        {**good, "kind": "note"},
        {**good, "issue": {"title": "x"}},
    ):
        with pytest.raises((AssertionError, KeyError)):
            assert_closed_audit([bad])
    with pytest.raises(AssertionError):  # a cycle-only key on a warning line
        assert_closed_audit([{**good, "exit": 0}])


def test_the_audit_builders_refuse_text_keys_and_text_values():
    stamp = {
        "ts": "2026-11-07T13:00:00Z",
        "host": "h",
        "login": "owner-login",
        "cycle_id": "0" * 32,
        "dry_run": False,
    }
    with pytest.raises(ValueError):
        audit.line("warning", **stamp, reason="clock_skew", title=SENT)
    with pytest.raises(ValueError):
        audit.decision_line(**stamp, reason="launched", issue=7, state=SENT)
    with pytest.raises(ValueError):
        audit.warning_line(**stamp, reason=SENT)
    with pytest.raises(ValueError):
        audit.stderr_fallback(SENT, 1)


def test_the_spy_reports_a_canary_only_when_one_was_served():
    spy = SpyRunner(
        {("a",): command_result(stderr=f"{SENT}"), ("b",): command_result()}
    )
    spy.run(["b"], 5.0)
    assert not spy.canary_served()
    spy.run(["a"], 5.0)
    assert spy.canary_served()


def test_a_scenario_run_cannot_start_a_real_process(tmp_path, tmp_state, monkeypatch):
    run = Run(tmp_path, tmp_state, monkeypatch)
    with pytest.raises(AssertionError, match="real subprocess"):
        SubprocessRunner().run([sys.executable, "-c", "pass"], 5.0)
    assert run.real_calls == [(sys.executable, "-c", "pass")]
