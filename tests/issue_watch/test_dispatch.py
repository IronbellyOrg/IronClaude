"""Task 23: the dispatcher core, over a fake runner and a fake clock.

Every path is under ``tmp_path``; no real ``orca``, ``gh``, ``git`` or ``superclaude`` runs.
"""

from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import cycle, defaults, dispatch, generate, record
from superclaude.cli.issue_watch.generate import Base, Outcome

from .conftest import CYCLE_NOW, FakeClock, result

ORCA = "/opt/orca/bin/orca"
SC = "/home/u/.local/bin/superclaude"
DEFAULTS = defaults.Defaults()
NAMES = ["Alpha", "Beta", "Gamma", "Delta"]


def _path(name: str) -> str:
    return f"/home/u/ws/{name}"


class World:
    """Orca, git and the children behind one runner; children can advance the clock."""

    def __init__(self, tmp_path: Path, names, clock: FakeClock) -> None:
        self.tmp, self.names, self.clock = tmp_path, list(names), clock
        self.base = Base(tmp_path / "config", tmp_path / "state", tmp_path / "wt")
        self.calls: list[tuple[tuple[str, ...], float]] = []
        self.children: dict[str, object] = {}
        self.listing_reply = None
        # what the read-only pre-child checks see (plan Task 24); a test changes one at a time
        self.labels = ["bug", DEFAULTS.trigger_label]
        self.field_ok = True
        self.projects = ["PVT_abc"]
        self.worktree_origin: dict[str, str] = {}
        self.no_worktree: set[str] = set()
        self.not_git: set[str] = set()
        self.trigger: str | None = None  # a per-repo labels.trigger in every config

    # -- the files a generated config would have ------------------------------------------
    def config(self, name: str, *, enabled: bool = True) -> Path:
        work = self.tmp / "wt" / name / "Coordinator"
        if name not in self.no_worktree:
            work.mkdir(parents=True, exist_ok=True)
            if name not in self.not_git:
                (work / ".git").write_text("gitdir: /elsewhere\n")
        directory = self.base.config_dir / dispatch.SUBDIR
        directory.mkdir(parents=True, exist_ok=True)
        approvers = directory / f"{name}-approvers.txt"
        approvers.write_text("11\n")
        approvers.chmod(0o600)
        path = directory / f"{name}.json"
        path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "enabled": enabled,
                    "repo": f"IronbellyOrg/{name}",
                    "project_id": "PVT_abc",
                    "worktree": str(self.tmp / "wt" / name / "Coordinator"),
                    "approvers_file": str(approvers),
                    "state_dir": str(self.state_dir(name)),
                    **({"labels": {"trigger": self.trigger}} if self.trigger else {}),
                }
            )
        )
        path.chmod(0o600)
        return path

    def state_dir(self, name: str) -> Path:
        return self.tmp / "state" / "issue-watch" / name

    def child(
        self,
        name: str,
        *,
        stdout="cycle: cycle_complete\nexit: 0\n",
        code=0,
        seconds=1.0,
        timed_out=False,
    ):
        def reply() -> object:
            self.clock.advance(seconds)
            return result(
                stdout="" if timed_out or code < 0 else stdout,
                returncode=code,
                timed_out=timed_out,
            )

        self.children[name] = reply

    # -- the runner ------------------------------------------------------------------------
    def run(self, argv, timeout, *, cwd=None):
        key = tuple(argv)
        self.calls.append((key, timeout))
        if key == (ORCA, "repo", "list"):
            if self.listing_reply is not None:
                return self.listing_reply
            lines = [
                f"00000000-0000-4000-8000-{i:012d}  {n}  {_path(n)}"
                for i, n in enumerate(self.names, 1)
            ]
            return result(stdout="\n".join(lines) + "\n")
        if key[0] == "git":
            parts = key[2].rstrip("/").rsplit("/", 2)
            name = parts[1] if parts[2] == "Coordinator" else parts[2]
            if parts[2] == "Coordinator" and name in self.worktree_origin:
                return result(stdout=self.worktree_origin[name])
            return result(stdout=f"https://github.com/IronbellyOrg/{name}.git\n")
        if key[:3] == ("gh", "label", "list"):
            return result(stdout=json.dumps([{"name": n} for n in self.labels]))
        if key[:3] == ("gh", "api", "--method") and "issue-fields" in key[4]:
            option = "Yes" if self.field_ok else "No"
            row = {"name": "Approved", "data_type": "single_select"}
            row["options"] = [{"name": option}]
            return result(stdout=json.dumps([row]))
        if key[:3] == ("gh", "api", "graphql"):
            nodes = [{"id": i, "number": n} for n, i in enumerate(self.projects, 1)]
            body = {"data": {"repository": {"projectsV2": {"nodes": nodes}}}}
            return result(stdout=json.dumps(body))
        assert key[0] == SC and key[1:4] == ("issue-watch", "once", "--config"), key
        name = Path(key[4]).stem
        return self.children[name]()

    def started(self) -> list[str]:
        return [Path(k[4]).stem for k, _ in self.calls if k[0] == SC]


@pytest.fixture
def world(tmp_path):
    return World(tmp_path, NAMES[:3], FakeClock(CYCLE_NOW))


def sweep(w: World, **over) -> dispatch.SweepResult:
    args = dict(
        orca=ORCA,
        superclaude=SC,
        defaults=DEFAULTS,
        base=w.base,
        deps_factory=lambda cfg: pytest.fail("no first run expected"),
        monotonic=w.clock.monotonic,
        now=w.clock.now,
    )
    args.update(over)
    return dispatch.run_sweep(w, **args)


def prepare(w: World, names=None) -> None:
    for name in names or w.names:
        w.config(name)
        w.child(name)


def test_the_order_rotates_across_three_sweeps(world) -> None:
    prepare(world)
    orders = []
    for _ in range(3):
        before = len(world.started())
        out = sweep(world)
        assert out.ok and out.stopped_after is None and out.skipped == ()
        orders.append(world.started()[before:])
    assert orders == [
        ["Alpha", "Beta", "Gamma"],
        ["Beta", "Gamma", "Alpha"],
        ["Gamma", "Alpha", "Beta"],
    ]


def test_the_loop_stops_after_the_first_launched_line(world) -> None:
    prepare(world)
    world.child("Alpha", stdout="cycle: cycle_complete\nexit: 0\nlaunched: 12\n")
    out = sweep(world)
    assert world.started() == ["Alpha"]
    assert out.stopped_after == "Alpha"
    assert [(c.name, c.launched, c.attempted) for c in out.children] == [
        ("Alpha", 12, None)
    ]
    assert [(s.name, s.reason) for s in out.skipped] == [
        ("Beta", "stopped_after_launch"),
        ("Gamma", "stopped_after_launch"),
    ]


def test_the_loop_stops_after_an_attempted_line(world) -> None:
    prepare(world)
    world.child("Alpha")
    world.child("Beta", stdout="cycle: launch_unknown\nexit: 7\nattempted: 5\n", code=7)
    out = sweep(world)
    assert world.started() == ["Alpha", "Beta"]
    assert out.stopped_after == "Beta"
    beta = out.children[1]
    assert (beta.exit_code, beta.reason, beta.attempted) == (7, "launch_unknown", 5)
    assert [(s.name, s.reason) for s in out.skipped] == [
        ("Gamma", "stopped_after_launch")
    ]


def test_a_sweep_that_stopped_early_starts_the_next_one_where_it_stopped(world) -> None:
    prepare(world)
    world.child("Alpha", stdout="cycle: cycle_complete\nexit: 0\nlaunched: 3\n")
    sweep(world)
    world.child("Alpha")  # nothing is launched any more
    before = len(world.started())
    sweep(world)
    assert world.started()[before:] == ["Beta", "Gamma", "Alpha"]


def _pend(w: World, name: str, *, at) -> None:
    state_dir = w.state_dir(name)
    store = record.init_state(state_dir, CYCLE_NOW - timedelta(days=1))
    ctx = record.PendingContext(
        approver_id=11,
        approval_event_id=77,
        approved_at=CYCLE_NOW - timedelta(hours=1),
        launch_cwd=str(w.tmp),
        launch_login="owner-login",
        launch_account_id=1001,
    )
    store.save(record.mark_pending(store.load(), 9, ctx, at))


def test_a_child_killed_after_255_s_with_a_pending_entry_stops_the_loop(world) -> None:
    prepare(world)
    world.child("Alpha", seconds=255.0, timed_out=True)
    _pend(
        world, "Alpha", at=CYCLE_NOW + timedelta(seconds=10)
    )  # created during this sweep
    out = sweep(world)
    assert world.started() == ["Alpha"]
    alpha = out.children[0]
    assert (alpha.killed, alpha.exit_code, alpha.reason) == (
        True,
        None,
        "child_timeout",
    )
    assert out.stopped_after == "Alpha"
    assert [s.name for s in out.skipped] == ["Beta", "Gamma"]
    # every child got the 255 second kill time
    assert {t for k, t in world.calls if k[0] == SC} == {dispatch.CHILD_TIMEOUT_S}
    assert (
        dispatch.CHILD_TIMEOUT_S == 255.0
        and dispatch.CHILD_TIMEOUT_S > cycle.DEADLINE_TOTAL_S
    )


def test_the_same_kill_with_no_pending_entry_lets_the_later_repos_run(world) -> None:
    prepare(world)
    world.child("Alpha", seconds=255.0, timed_out=True)
    record.init_state(world.state_dir("Alpha"), CYCLE_NOW - timedelta(days=1))
    out = sweep(world)
    assert world.started() == [
        "Alpha",
        "Beta",
        "Gamma",
    ]  # the timeout never kills the loop
    assert out.stopped_after is None and out.children[0].killed is True


def test_an_entry_from_before_this_sweep_does_not_stop_the_loop(world) -> None:
    prepare(world)
    world.child("Alpha", seconds=255.0, timed_out=True)
    _pend(world, "Alpha", at=CYCLE_NOW - timedelta(hours=5))  # an old entry
    out = sweep(world)
    assert world.started() == ["Alpha", "Beta", "Gamma"] and out.stopped_after is None


def test_a_child_ended_by_a_signal_with_a_new_pending_entry_stops_the_loop(
    world,
) -> None:
    prepare(world)
    world.child("Alpha", seconds=3.0, code=-9)  # SIGKILL: negative code, no launch line
    _pend(world, "Alpha", at=CYCLE_NOW + timedelta(seconds=10))
    out = sweep(world)
    alpha = out.children[0]
    assert (alpha.killed, alpha.exit_code, alpha.reason) == (True, None, "child_signal")
    assert world.started() == ["Alpha"] and out.stopped_after == "Alpha"


def test_a_child_ended_by_a_signal_with_no_pending_entry_lets_the_later_repos_run(
    world,
) -> None:
    prepare(world)
    world.child("Alpha", seconds=3.0, code=-15)
    record.init_state(world.state_dir("Alpha"), CYCLE_NOW - timedelta(days=1))
    out = sweep(world)
    assert world.started() == ["Alpha", "Beta", "Gamma"] and out.stopped_after is None


def test_a_killed_child_with_an_unreadable_store_stops_the_loop(world) -> None:
    prepare(world)
    world.child("Alpha", seconds=255.0, timed_out=True)
    world.state_dir("Alpha").mkdir(parents=True)
    (world.state_dir("Alpha") / "dispatch.json").write_text("{not json")
    out = sweep(world)
    assert world.started() == ["Alpha"] and out.stopped_after == "Alpha"


def test_an_error_exit_with_a_new_pending_entry_stops_the_loop(world) -> None:
    prepare(world)
    world.child("Alpha", seconds=3.0, code=1)  # error exit, no launch line
    _pend(world, "Alpha", at=CYCLE_NOW + timedelta(seconds=10))
    out = sweep(world)
    assert world.started() == ["Alpha"] and out.stopped_after == "Alpha"


def test_an_error_exit_with_no_new_entry_lets_the_later_repos_run(world) -> None:
    prepare(world)
    world.child("Alpha", seconds=3.0, code=1)
    record.init_state(world.state_dir("Alpha"), CYCLE_NOW - timedelta(days=1))
    out = sweep(world)
    assert world.started() == ["Alpha", "Beta", "Gamma"] and out.stopped_after is None


def test_an_error_exit_with_an_unreadable_store_lets_the_later_repos_run(world) -> None:
    prepare(world)
    world.child("Alpha", seconds=3.0, code=1)
    world.state_dir("Alpha").mkdir(parents=True)
    (world.state_dir("Alpha") / "dispatch.json").write_text("{not json")
    out = sweep(world)
    assert world.started() == ["Alpha", "Beta", "Gamma"] and out.stopped_after is None


def test_the_270_second_cap_reports_the_repos_not_reached(tmp_path) -> None:
    w = World(tmp_path, NAMES, FakeClock(CYCLE_NOW))
    prepare(w)
    for name in w.names:
        w.child(name, seconds=100.0)
    out = sweep(w)
    # the order is by name (Alpha, Beta, Delta, Gamma); children start at 0, 100 and 200 s
    assert w.started() == ["Alpha", "Beta", "Delta"]
    assert [(s.name, s.reason) for s in out.skipped] == [("Gamma", "loop_cap")]
    assert out.elapsed_s == 300.0 and dispatch.LOOP_CAP_S == 270.0
    # the next sweep starts at the repo that was not reached
    w.clock.advance(1)
    for name in w.names:
        w.child(name, seconds=1.0)
    before = len(w.started())
    sweep(w)
    assert w.started()[before:][0] == "Gamma"


def test_setup_that_crosses_the_cap_starts_no_child_and_reports_loop_cap(
    world, monkeypatch
) -> None:
    world.config("Alpha")
    world.config("Gamma")
    world.child("Alpha")
    world.child("Gamma")

    def slow_ensure(repo, defs, runner, base):
        world.clock.advance(280.0)  # generating Beta's config takes longer than the cap
        world.config(repo.name, enabled=False)
        return Outcome("generated", repo.name, config_path=base.config_dir)

    monkeypatch.setattr(dispatch, "ensure_config", slow_ensure)

    def enable(path, defs, runner, deps_factory):
        data = json.loads(Path(path).read_text())
        data["enabled"] = True
        Path(path).write_text(json.dumps(data))

    monkeypatch.setattr(dispatch, "first_run", enable)
    out = sweep(world)
    assert world.started() == ["Alpha"]
    assert ("Beta", "loop_cap") in [(s.name, s.reason) for s in out.skipped]
    assert ("Gamma", "loop_cap") in [(s.name, s.reason) for s in out.skipped]


def test_a_repo_with_no_config_is_generated_and_checked_before_it_runs(
    world, monkeypatch
) -> None:
    world.config("Alpha")
    world.config("Gamma")
    for name in ("Alpha", "Beta", "Gamma"):
        world.child(name)
    order: list[str] = []

    def fake_ensure(repo, defs, runner, base):
        order.append(f"ensure:{repo.name}")
        world.config(repo.name, enabled=False)
        return Outcome("generated", repo.name, config_path=base.config_dir)

    def fake_first_run(path, defs, runner, deps_factory):
        order.append(f"first_run:{Path(path).stem}")
        data = json.loads(Path(path).read_text())
        data["enabled"] = True
        Path(path).write_text(json.dumps(data))

    monkeypatch.setattr(dispatch, "ensure_config", fake_ensure)
    monkeypatch.setattr(dispatch, "first_run", fake_first_run)
    out = sweep(world)
    assert order == ["ensure:Beta", "first_run:Beta"]
    assert out.generated == ("Beta",)
    assert world.started() == ["Alpha", "Beta", "Gamma"]


def test_a_repo_whose_generation_is_skipped_is_reported_not_run(
    world, monkeypatch
) -> None:
    world.config("Alpha")
    world.config("Gamma")
    world.child("Alpha")
    world.child("Gamma")
    monkeypatch.setattr(
        dispatch,
        "ensure_config",
        lambda repo, d, r, b: Outcome("skipped", repo.name, "no_project"),
    )
    out = sweep(world)
    assert world.started() == ["Alpha", "Gamma"]
    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "no_project")]


def test_a_config_that_is_not_enabled_is_skipped_with_a_reason(world) -> None:
    prepare(world)
    world.config("Beta", enabled=False)
    out = sweep(world)
    assert world.started() == ["Alpha", "Gamma"]
    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "not_enabled")]


@pytest.mark.parametrize(
    "reply",
    [
        result(stderr="boom", returncode=1),
        result(timed_out=True),
        result(spawn_error="FileNotFoundError"),
        result(stdout="not a list\n"),
    ],
)
def test_a_failed_orca_list_gives_an_error_result_not_a_clean_one(world, reply) -> None:
    prepare(world)
    world.listing_reply = reply
    out = sweep(world)
    assert out.ok is False and out.error in {
        "list_failed",
        "list_timeout",
        "unreadable_list",
    }
    assert out.children == () and world.started() == []


def test_an_empty_but_successful_list_is_a_clean_empty_sweep(world) -> None:
    world.listing_reply = result(stdout="")
    out = sweep(world)
    assert out.ok is True and out.error is None and out.children == ()


def test_each_childs_exit_code_and_reason_are_kept(world) -> None:
    prepare(world)
    world.child("Alpha", stdout="cycle: gh_auth_failed\nexit: 3\n", code=3, seconds=2.0)
    world.child("Beta", stdout="cycle: cycle_complete\nexit: 0\n", seconds=3.0)
    out = sweep(world)
    assert [(c.name, c.exit_code, c.reason) for c in out.children] == [
        ("Alpha", 3, "gh_auth_failed"),
        ("Beta", 0, "cycle_complete"),
        ("Gamma", 0, "cycle_complete"),
    ]
    assert [c.seconds for c in out.children][:2] == [2.0, 3.0]
    # a failing child without a launch never stops the loop
    assert out.stopped_after is None and world.started() == ["Alpha", "Beta", "Gamma"]


def test_a_child_that_cannot_start_never_kills_the_loop(world) -> None:
    prepare(world)
    world.children["Alpha"] = lambda: result(spawn_error="FileNotFoundError")
    out = sweep(world)
    assert (out.children[0].reason, out.children[0].killed) == ("spawn_error", False)
    assert world.started() == ["Alpha", "Beta", "Gamma"]


def test_the_child_command_is_an_absolute_argv_with_the_config_path(world) -> None:
    prepare(world)
    sweep(world)
    children = [k for k, _ in world.calls if k[0] == SC]
    assert children[0] == (
        SC,
        "issue-watch",
        "once",
        "--config",
        str(world.base.config_dir / dispatch.SUBDIR / "Alpha.json"),
    )
    assert all(Path(k[4]).is_absolute() for k in children)


@pytest.mark.parametrize("orca,sc", [("orca", SC), (ORCA, "superclaude")])
def test_relative_program_paths_are_refused_because_cron_has_no_path(
    world, orca, sc
) -> None:
    with pytest.raises(ValueError):
        sweep(world, orca=orca, superclaude=sc)
    assert world.calls == []


def test_the_rotation_file_is_private_and_a_broken_one_restarts_at_the_first_repo(
    world,
) -> None:
    prepare(world)
    sweep(world)
    path = world.base.state_dir / "issue-watch" / dispatch.ROTATION_FILE
    assert json.loads(path.read_text()) == {"next": 1}
    assert oct(path.stat().st_mode & 0o777) == "0o600"
    path.write_text("garbage")
    before = len(world.started())
    sweep(world)
    assert world.started()[before:][0] == "Alpha"


def test_nothing_is_written_outside_tmp_path(world, tmp_path) -> None:
    prepare(world)
    sweep(world)
    assert not (tmp_path / "home").exists()
    assert generate.Base.default().config_dir.expanduser() != world.base.config_dir


# --- plan Task 24: the account rate wait and the pre-child checks -------------------------


def _rate_limited(w: World, name: str, minutes: float = 10.0):
    """A child that ended `rate_limited` and a store that holds the time it may run again."""
    until = CYCLE_NOW + timedelta(minutes=minutes)
    store = record.init_state(w.state_dir(name), CYCLE_NOW - timedelta(days=1))
    store.save(record.set_next_permitted(store.load(), until))
    w.child(name, stdout="cycle: rate_limited\nexit: 5\n", code=5)
    return until


def _wait_file(w: World) -> Path:
    return w.base.state_dir / "issue-watch" / dispatch.RATE_WAIT_FILE


def test_a_rate_limited_child_stops_later_children_until_the_stored_time(world) -> None:
    prepare(world)
    until = _rate_limited(world, "Alpha")
    out = sweep(world)
    assert world.started() == ["Alpha"]
    assert out.children[0].reason == "rate_limited" and out.waiting_until == until
    assert [(s.name, s.reason) for s in out.skipped] == [
        ("Beta", "account_rate_wait"),
        ("Gamma", "account_rate_wait"),
    ]
    stored = json.loads(_wait_file(world).read_text())
    assert stored == {"next_permitted_at": until.strftime("%Y-%m-%dT%H:%M:%SZ")}
    assert oct(_wait_file(world).stat().st_mode & 0o777) == "0o600"


def test_a_restart_of_the_loop_honours_the_file_until_its_time(world) -> None:
    prepare(world)
    until = _rate_limited(world, "Alpha")
    sweep(world)
    calls = len(world.calls)
    world.clock.advance(60)  # a new sweep a minute later: still waiting
    again = sweep(world)
    assert again.waiting_until == until and again.children == ()
    assert len(world.calls) == calls  # no orca list, no gh read, no child
    world.clock.advance(10 * 60)  # past the stored time
    for name in world.names:
        world.child(name)
    after = sweep(world)
    assert after.waiting_until is None and len(after.children) == 3


def test_a_rate_limit_clamped_child_does_not_write_the_file(world) -> None:
    prepare(world)
    world.child("Alpha", stdout="cycle: rate_limit_clamped\nexit: 5\n", code=5)
    out = sweep(world)
    assert not _wait_file(world).exists()
    assert world.started() == ["Alpha", "Beta", "Gamma"] and out.waiting_until is None


def test_an_expired_wait_file_is_ignored(world) -> None:
    prepare(world)
    path = _wait_file(world)
    path.parent.mkdir(parents=True)
    past = (CYCLE_NOW - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    path.write_text(json.dumps({"next_permitted_at": past}))
    out = sweep(world)
    assert out.waiting_until is None and world.started() == ["Alpha", "Beta", "Gamma"]


def test_a_broken_wait_file_is_ignored(world) -> None:
    prepare(world)
    path = _wait_file(world)
    path.parent.mkdir(parents=True)
    path.write_text("garbage")
    assert sweep(world).waiting_until is None


def _created(w: World) -> list:
    return [k for k, _ in w.calls if k[:3] == ("gh", "label", "create")]


@pytest.mark.parametrize(
    "arrange, reason",
    [
        (lambda w: w.no_worktree.add("Beta"), "worktree_invalid"),
        (lambda w: w.not_git.add("Beta"), "worktree_not_git"),
        (
            lambda w: w.worktree_origin.update(
                Beta="https://github.com/SomeoneElse/Beta.git\n"
            ),
            "origin_mismatch",
        ),
        (lambda w: w.labels.remove(DEFAULTS.trigger_label), "label_missing"),
        (lambda w: setattr(w, "field_ok", False), "approved_field_missing"),
        (lambda w: setattr(w, "projects", []), "no_project"),
        (lambda w: setattr(w, "projects", ["PVT_other"]), "project_mismatch"),
        (lambda w: setattr(w, "projects", ["PVT_abc", "PVT_two"]), "project_ambiguous"),
    ],
)
def test_each_failed_pre_child_check_gives_its_own_skip_reason_and_creates_nothing(
    tmp_path, arrange, reason
) -> None:
    w = World(tmp_path, ["Beta"], FakeClock(CYCLE_NOW))
    arrange(w)
    prepare(w)
    out = sweep(w)
    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", reason)]
    assert out.children == () and w.started() == []
    assert reason in dispatch.SKIP_REASONS
    assert _created(w) == []  # the loop never creates a label
    assert not any(k[:2] == ("gh", "project") for k, _ in w.calls)


def test_the_label_precheck_uses_the_configs_own_trigger_label(tmp_path) -> None:
    w = World(tmp_path, ["Beta"], FakeClock(CYCLE_NOW))
    w.trigger = "go-watch"
    w.labels = ["bug", "go-watch"]  # the current default label does not exist
    prepare(w)
    out = sweep(w)
    assert w.started() == ["Beta"] and out.skipped == ()
    w.labels = [
        "bug",
        DEFAULTS.trigger_label,
    ]  # only the default exists: the config's does not
    out = sweep(w)
    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "label_missing")]


def test_a_failed_pre_child_check_skips_only_that_repo(world) -> None:
    world.no_worktree.add("Beta")  # set before the configs are written
    prepare(world)
    out = sweep(world)
    assert world.started() == ["Alpha", "Gamma"]
    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "worktree_invalid")]


def test_a_failed_label_or_field_read_is_reported_not_treated_as_missing(
    world, monkeypatch
) -> None:
    prepare(world)
    real = world.run

    def run(argv, timeout, *, cwd=None):
        if tuple(argv)[:3] == ("gh", "label", "list"):
            return result(stderr="HTTP 502", returncode=1)
        return real(argv, timeout, cwd=cwd)

    world.run = run  # type: ignore[method-assign]
    out = sweep(world)
    assert {s.reason for s in out.skipped} == {"label_check_failed"}
    assert world.started() == []


def test_the_org_field_is_read_once_per_owner_per_sweep(world) -> None:
    prepare(world)
    sweep(world)
    reads = [k for k, _ in world.calls if "issue-fields" in " ".join(k)]
    assert len(reads) == 1  # one owner, three repos


def test_every_skip_reason_a_sweep_gives_is_in_the_documented_table(world) -> None:
    prepare(world)
    world.no_worktree.add("Beta")
    world.config("Beta")
    out = sweep(world)
    for item in out.skipped:
        assert item.reason in dispatch.SKIP_REASONS
    from superclaude.cli.issue_watch import audit

    for reason, text in dispatch.SKIP_REASONS.items():
        assert text and (reason in audit.REASON_TABLE or "(audit reason" not in text), (
            reason
        )


def test_every_reason_the_generator_and_the_repo_list_can_give_is_in_the_table() -> (
    None
):
    """The sweep passes these through; the table must name each (plan Task 24, AC 2)."""
    import re

    pkg = Path(dispatch.__file__).parent
    generated = set(
        re.findall(r'_skip\(name, "([a-z_]+)"\)', (pkg / "generate.py").read_text())
    )
    listed = set(re.findall(r'skip\("([a-z_]+)"\)', (pkg / "repos.py").read_text()))
    assert {"no_project", "project_ambiguous", "generated_invalid"} <= generated
    assert {"path_in_tmp", "foreign_owner"} <= listed
    assert (generated | listed) <= set(dispatch.SKIP_REASONS), (
        generated | listed
    ) - set(dispatch.SKIP_REASONS)
