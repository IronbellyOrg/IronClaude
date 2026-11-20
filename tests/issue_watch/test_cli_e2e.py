"""End-to-end tests of ``superclaude issue-watch`` as a real process (plan step 8.2).

Each test runs ``python -m superclaude.cli.main issue-watch ...`` with an
explicit ``env=`` from the ``stub_path`` fixture, so the only ``gh``, ``orca``,
``orca-ide``, ``git`` and ``ccsession`` the process can reach are the PATH stubs
written into ``tmp_path`` (decisions DF-10, DF-34, DF-55, DF-56). Replies are
built from the ``GhWorld`` fixtures, with the clock of the user reply set to the
real time.

The poll wakes an orchestrator through a live Orca session, which a PATH stub
cannot fake (the session is found from the real ``/proc``). The wake tests
therefore script a workspace with no session whose start fails: the poll writes
the wake file, finds no session, marks the workspace unread and exits 7. That is
a real run of every part except the typed line, which the unit tests cover.

Covers FR-001, FR-003, FR-010, NFR-002, NFR-009, NFR-010 and AC-1.
"""

from __future__ import annotations

import json
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from superclaude.cli.issue_watch import cycle, github
from superclaude.cli.issue_watch.predicates import parse_utc

from .conftest import (
    OWN_LOGIN,
    REPO_A,
    STUB_TOOLS,
    FakeClock,
    GhWorld,
    make_config,
    read_calls,
    write_ack,
    write_scenario,
)

ORIGIN_TEXT = "https://github.com/IronbellyOrg/IronClaude\n"
PROBE_REPLY = {"topics": [{"name": "orca-cli"}]}
ISSUE = 9
KEY = f"{REPO_A}#{ISSUE}"
USER_ARGV = ["api", "user", "--include"]
IDLE_OK = "cycle: cycle_complete\nexit: 0\n"
NO_SESSION = "cycle: no_session\nexit: 7\n"


def assert_local_filesystem(tmp_path: Path) -> None:
    """Fail when ``tmp_path`` is on a network filesystem (a failure, not a bypass)."""
    mountinfo = Path("/proc/self/mountinfo").read_text(
        encoding="utf-8", errors="replace"
    )
    fs_type = cycle.fs_type_of(tmp_path, mountinfo)
    assert fs_type not in cycle.NETWORK_FS_TYPES, (
        "tmp_path is on a network filesystem; set TMPDIR to a local directory"
    )


class Watcher:
    """One config, one state directory and the CLI as a subprocess."""

    def __init__(self, tmp_path: Path, env: dict[str, str]) -> None:
        self.tmp_path = tmp_path
        self.env = env
        self.config = make_config(tmp_path)
        self.state_dir = self.config.state_dir
        self.config_path = tmp_path / "issue-watch.json"
        self.config_path.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "enabled": True,
                    "orchestrator_repo": str(self.config.orchestrator_repo),
                    "state_dir": str(self.state_dir),
                }
            ),
            encoding="utf-8",
        )
        self.stubbin = tmp_path / "stubbin"
        self.log = Path(env["IW_STUB_LOG"])

    def cli(self, verb: str, *extra: str) -> subprocess.CompletedProcess:
        """Run ``issue-watch <verb> [extra] --config <file>`` as a real process."""
        return subprocess.run(
            [
                sys.executable,
                # `-m` on a module its package already imports warns on stderr
                "-W",
                "ignore:'superclaude.cli.main' found in sys.modules:RuntimeWarning",
                "-m",
                "superclaude.cli.main",
                "issue-watch",
                verb,
                *extra,
                "--config",
                str(self.config_path),
            ],
            env=self.env,
            cwd=self.env["HOME"],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )

    def init_state(self, *extra: str) -> datetime:
        """Run ``init-state`` and return the ``created_at`` it stamped."""
        done = self.cli("init-state", *extra)
        assert (done.returncode, done.stderr) == (0, ""), done
        assert done.stdout == f"state created: {self.state_dir}\n", done.stdout
        return parse_utc(self.store()["created_at"])

    def store(self) -> dict:
        """The parsed ``dispatch.json``."""
        return json.loads((self.state_dir / "dispatch.json").read_text("utf-8"))

    def audit_lines(self) -> list[dict]:
        """Every line of ``audit.jsonl``, oldest first."""
        path = self.state_dir / "audit.jsonl"
        return [json.loads(x) for x in path.read_text("utf-8").splitlines()]

    def calls(self) -> list[dict]:
        """Every stub call so far, in call order across the stubs."""
        return read_calls(self.log)

    def wake_files(self) -> list[Path]:
        folder = self.config.orchestrator_repo / ".orchestrator" / "wakes"
        if not folder.exists():
            return []
        return sorted(
            p for p in folder.glob("*.json") if not p.name.endswith(".ack.json")
        )

    def script(self, world: GhWorld) -> Path:
        """Write the stub scenario: every exact reply of ``world`` and the Orca replies."""
        rules: dict[str, list[dict]] = {name: [] for name in STUB_TOOLS}
        for argv, reply in world.runner.script.items():
            if argv[0] not in ("gh", "git", "ccsession"):
                continue
            answer = reply(list(argv), None)
            rules[argv[0]].append(
                {
                    "argv_prefix": list(argv[1:]),
                    "exit": answer.returncode,
                    "stdout": answer.stdout,
                    "stderr": answer.stderr,
                }
            )
        # The three information streams carry a time in their query: match the start.
        rules["gh"].append(
            {
                "argv_prefix": ["api", "--method", "GET", "search/issues"],
                "stdout": json.dumps(
                    {"total_count": 0, "incomplete_results": False, "items": []}
                ),
            }
        )
        for tool in ("orca", "orca-ide"):
            rules[tool] += [
                {
                    "argv_prefix": ["skills", "list", "--json"],
                    "stdout": json.dumps(PROBE_REPLY),
                },
                {
                    "argv_prefix": ["terminal", "list"],
                    "stdout": json.dumps({"terminals": []}),
                },
                {"argv_prefix": ["terminal", "create"], "exit": 1},
                {"argv_prefix": ["worktree", "set"], "stdout": "{}"},
            ]
        return write_scenario(self.tmp_path, rules)


def make_watcher(tmp_path: Path, stub_path: dict[str, str]) -> Watcher:
    return Watcher(tmp_path, stub_path)


def world_for(watcher: Watcher) -> GhWorld:
    """A ``GhWorld`` whose clock is the real time, for the ``Date`` header of the user reply."""
    return GhWorld(FakeClock(datetime.now(timezone.utc)), watcher.config)


def argv_of(call: dict) -> tuple[str, list[str]]:
    return call["tool"], call["argv"]


def gh_argvs(calls: list[dict]) -> list[list[str]]:
    return [c["argv"] for c in calls if c["tool"] == "gh"]


def orca_calls(calls: list[dict]) -> list[dict]:
    return [c for c in calls if c["tool"] in ("orca", "orca-ide")]


def is_search(argv: list[str]) -> bool:
    return argv[:4] == ["api", "--method", "GET", "search/issues"]


def test_ac1_fixture_guard_names_resolve_to_stubs(tmp_path, stub_path):
    """AC-1 guard: only the stubs are reachable, nothing else."""
    assert_local_filesystem(tmp_path)
    stubbin, linkbin = tmp_path / "stubbin", tmp_path / "linkbin"
    assert stub_path["PATH"] == f"{stubbin}:{linkbin}"
    for name in STUB_TOOLS:
        assert shutil.which(name, path=stub_path["PATH"]) == str(stubbin / name), name
    assert sorted(p.name for p in stubbin.iterdir()) == sorted(STUB_TOOLS)
    assert sorted(p.name for p in linkbin.iterdir()) == ["python3"]
    assert set(stub_path) == {
        "PATH",
        "HOME",
        "XDG_STATE_HOME",
        "IW_STUB_SCENARIO",
        "IW_STUB_LOG",
    }, sorted(stub_path)


def test_fr001_idle_cycle_reads_only_and_exits_0(tmp_path, stub_path):
    """FR-001, NFR-009: nothing assigned: the user, the searches, no write, no Orca call."""
    assert_local_filesystem(tmp_path)
    watcher = make_watcher(tmp_path, stub_path)
    watcher.init_state("--no-baseline")
    watcher.script(world_for(watcher))

    done = watcher.cli("once")

    assert done.returncode == 0, done
    assert done.stdout == IDLE_OK, done.stdout
    assert done.stderr == ""
    calls = watcher.calls()
    gh = gh_argvs(calls)
    assert gh[0] == USER_ARGV
    assert all(is_search(argv) for argv in gh[1:]), gh
    # one assigned search per listed org, then the three information searches per org
    assert len(gh) == 1 + 2 * 4, gh
    assert not orca_calls(calls), calls
    assert not [c for c in calls if c["tool"] == "git"], calls  # no candidate: no check
    cycle_lines = [x for x in watcher.audit_lines() if x["kind"] == "cycle"]
    assert len(cycle_lines) == 1, watcher.audit_lines()
    line = cycle_lines[0]
    assert (line["exit"], line["reason"], line["dry_run"]) == (
        0,
        "cycle_complete",
        False,
    )
    assert (line["login"], line["gh_calls"]) == (OWN_LOGIN, len(gh))
    assert watcher.store()["entries"] == {}
    assert watcher.store()["last_completed_cycle_at"] is not None
    assert watcher.wake_files() == []


def test_the_search_calls_ask_for_no_text_beyond_the_projection(tmp_path, stub_path):
    """FR-003: every call is the fixed argv list; the first line of the user call is plain."""
    assert_local_filesystem(tmp_path)
    watcher = make_watcher(tmp_path, stub_path)
    watcher.init_state("--no-baseline")
    world = world_for(watcher)
    world.issue(REPO_A, ISSUE)
    watcher.script(world)

    watcher.cli("once")

    searches = [argv for argv in gh_argvs(watcher.calls()) if is_search(argv)]
    assigned = [a for a in searches if a[5].startswith("q=is:issue is:open assignee:")]
    assert len(assigned) == 2  # one per listed org
    assert github.argv_search_assigned("IronbellyOrg", OWN_LOGIN)[1:] in assigned


def test_the_first_cycle_records_what_is_assigned_and_wakes_nobody(tmp_path, stub_path):
    """Design 4.3 rule 5: the baseline cycle marks every assigned issue seen, no wake."""
    assert_local_filesystem(tmp_path)
    watcher = make_watcher(tmp_path, stub_path)
    watcher.init_state()  # baseline on, the default
    world = world_for(watcher)
    world.issue(REPO_A, ISSUE)
    watcher.script(world)

    done = watcher.cli("once")

    assert (done.returncode, done.stdout, done.stderr) == (0, IDLE_OK, "")
    assert not orca_calls(watcher.calls())
    entry = watcher.store()["entries"][KEY]
    assert (entry["state"], entry["ack_reason"]) == ("acked", "baseline")
    assert watcher.store()["baseline"] is False
    assert watcher.wake_files() == []
    # the second cycle sees the issue as known and does nothing more
    again = watcher.cli("once")
    assert (again.returncode, again.stdout) == (0, IDLE_OK)
    assert not orca_calls(watcher.calls())


def test_fr010_an_assigned_issue_gets_a_wake_file_and_exit_7_without_a_session(
    tmp_path, stub_path
):
    """FR-010: the wake file is written, the session cannot be started, the workspace is marked."""
    assert_local_filesystem(tmp_path)
    watcher = make_watcher(tmp_path, stub_path)
    watcher.init_state("--no-baseline")
    world = world_for(watcher)
    world.issue(REPO_A, ISSUE)
    watcher.script(world)

    done = watcher.cli("once")

    assert done.returncode == 7, done
    assert done.stdout == NO_SESSION, done.stdout
    assert done.stderr == ""
    calls = watcher.calls()
    orca = orca_calls(calls)
    assert [c["argv"][:2] for c in orca if c["argv"][:2] != ["skills", "list"]] == [
        ["terminal", "list"],
        ["terminal", "create"],
        ["worktree", "set"],
    ], orca
    assert all(
        c["tool"] == "orca-ide" for c in orca
    )  # the first name is resolved first
    mark = next(c["argv"] for c in orca if c["argv"][:2] == ["worktree", "set"])
    assert "--unread" in mark
    assert mark[mark.index("--comment") + 1] == "issue-watch: no_session"
    (wake_path,) = watcher.wake_files()
    assert stat.S_IMODE(wake_path.stat().st_mode) == 0o600
    data = json.loads(wake_path.read_text("utf-8"))
    assert data["schema"] == "orchestrator-wake/1"
    assert [(i["repo"], i["number"]) for i in data["assigned"]] == [(REPO_A, ISSUE)]
    entry = watcher.store()["entries"][KEY]
    assert entry["state"] == "unknown"
    assert (entry["orchestrator"], entry["wake_id"]) == (
        "ironclaude-1",
        data["wake_id"],
    )
    decisions = [x for x in watcher.audit_lines() if x["kind"] == "decision"]
    assert [(x["issue"], x["reason"]) for x in decisions] == [(ISSUE, "no_session")]
    lines = watcher.audit_lines()
    assert (lines[-1]["kind"], lines[-1]["exit"]) == ("cycle", 7)


def test_nfr010_an_acknowledgment_ends_the_wait_and_the_next_cycle_is_quiet(
    tmp_path, stub_path
):
    """NFR-010: once the orchestrator acknowledges, nothing is sent again."""
    assert_local_filesystem(tmp_path)
    watcher = make_watcher(tmp_path, stub_path)
    watcher.init_state("--no-baseline")
    world = world_for(watcher)
    world.issue(REPO_A, ISSUE)
    watcher.script(world)
    assert watcher.cli("once").returncode == 7
    first_calls = len(watcher.calls())
    wake_id = watcher.store()["entries"][KEY]["wake_id"]
    write_ack(watcher.config, wake_id, taken=[(REPO_A, ISSUE)])

    second = watcher.cli("once")

    assert second.returncode == 0, second
    assert second.stdout == IDLE_OK, second.stdout
    assert second.stderr == ""
    later = watcher.calls()[first_calls:]
    # only reads: the probe and the look for the orchestrator's session
    assert {tuple(c["argv"][:2]) for c in orca_calls(later)} <= {
        ("skills", "list"),
        ("terminal", "list"),
    }, later
    entry = watcher.store()["entries"][KEY]
    assert entry["state"] == "acked"
    # the acknowledged wake file and its acknowledgment are moved, never deleted
    assert watcher.wake_files() == []
    done = watcher.config.orchestrator_repo / ".orchestrator" / "wakes" / "done"
    assert sorted(p.name for p in done.iterdir()) == [
        f"{wake_id}.ack.json",
        f"{wake_id}.json",
    ]
    decisions = [x["reason"] for x in watcher.audit_lines() if x["kind"] == "decision"]
    assert decisions == ["no_session", "acked"]


def test_a_dry_run_writes_nothing_and_calls_no_orca(tmp_path, stub_path):
    """The dry run reads GitHub and decides; it writes no wake file, no store, no label."""
    assert_local_filesystem(tmp_path)
    watcher = make_watcher(tmp_path, stub_path)
    watcher.init_state("--no-baseline")
    world = world_for(watcher)
    world.issue(REPO_A, ISSUE)
    watcher.script(world)
    before = (watcher.state_dir / "dispatch.json").read_bytes()

    done = watcher.cli("once", "--dry-run")

    assert done.returncode == 0, done
    assert done.stdout.splitlines()[-1] == f"would_wake: {KEY}", done.stdout
    assert not orca_calls(watcher.calls())
    assert watcher.wake_files() == []
    assert (watcher.state_dir / "dispatch.json").read_bytes() == before
    assert watcher.audit_lines()[-1]["dry_run"] is True


def test_check_config_prints_the_routing_without_writing(tmp_path, stub_path):
    """The real tier list is read through ``ccsession --help``; nothing is written."""
    assert_local_filesystem(tmp_path)
    watcher = make_watcher(tmp_path, stub_path)
    watcher.script(world_for(watcher))

    done = watcher.cli("check-config")

    assert done.returncode == 0, done
    assert done.stdout.startswith("configuration is valid\n")
    assert "next issue goes to a new ironclaude-1" in done.stdout
    calls = watcher.calls()
    assert [argv_of(c) for c in calls] == [("ccsession", ["--help"])]
    assert not watcher.state_dir.exists()
