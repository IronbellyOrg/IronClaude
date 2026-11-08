"""End-to-end tests of ``superclaude issue-watch`` as a real process (plan step 8.2).

Each test runs ``python -m superclaude.cli.main issue-watch ...`` with an
explicit ``env=`` from the ``stub_path`` fixture, so the only ``gh``, ``orca``,
``orca-ide`` and ``git`` the process can reach are the PATH stubs written into
``tmp_path`` (decisions DF-10, DF-34, DF-55, DF-56). Replies are built from the
``GhWorld`` fixtures, with event times generated after ``init-state`` has
stamped the store ``created_at`` from the real clock.

Covers FR-001, FR-003, FR-010, FR-013, NFR-002, NFR-009, NFR-010 and AC-1.
The sleeping-stub timeout (AC-19) is not tested here: it is split into a runner
unit test and in-process cycle tests (DF-55).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from superclaude.cli.issue_watch import cycle, github
from superclaude.cli.issue_watch.predicates import parse_utc

from .conftest import (
    APPROVER_ID,
    OWN_LOGIN,
    PROJECT_ID,
    STUB_TOOLS,
    FakeClock,
    GhWorld,
    label_event,
    load_fixture,
    make_config,
    read_calls,
    write_scenario,
)

ORIGIN_TEXT = "https://github.com/IronbellyOrg/IronClaude\n"
PROBE_REPLY = {"topics": [{"name": "orca-cli"}]}
ISSUE = 9

# FR-003, written out in full: the contract is the literal list.
DISCOVERY_ARGV = [
    "issue",
    "list",
    "--repo",
    "IronbellyOrg/IronClaude",
    "--state",
    "open",
    "--label",
    "issue-watch:trigger",
    "--assignee",
    OWN_LOGIN,
    "--json",
    "number,labels,assignees,state",
    "-L",
    "100",
]
USER_ARGV = ["api", "user", "--include"]


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
                    "schema_version": 1,
                    "enabled": True,
                    "project_id": PROJECT_ID,
                    "worktree": str(self.config.worktree),
                    "approvers_file": str(self.config.approvers_file),
                    "state_dir": str(self.state_dir),
                }
            ),
            encoding="utf-8",
        )
        self.stubbin = tmp_path / "stubbin"
        self.log = Path(env["IW_STUB_LOG"])

    def cli(self, verb: str) -> subprocess.CompletedProcess:
        """Run ``issue-watch <verb> --config <file>`` as a real process."""
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
                "--config",
                str(self.config_path),
            ],
            env=self.env,
            cwd=self.env["HOME"],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    def init_state(self) -> datetime:
        """Run ``init-state`` and return the ``created_at`` it stamped."""
        done = self.cli("init-state")
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
        """Every stub call so far, in call order across the four stubs."""
        return read_calls(self.log)

    def script(self, world: GhWorld, *, launch_reply: dict | None = None) -> Path:
        """Write the stub scenario: every ``gh`` reply of ``world``, git and Orca."""
        rules: dict[str, list[dict]] = {"gh": [], "git": [], "orca-ide": []}
        for argv, reply in world.runner.script.items():
            if argv[0] != "gh":
                continue
            answer = reply(list(argv), None)
            rules["gh"].append(
                {
                    "argv_prefix": list(argv[1:]),
                    "exit": answer.returncode,
                    "stdout": answer.stdout,
                    "stderr": answer.stderr,
                }
            )
        rules["git"].append(
            {
                "argv_prefix": [
                    "-C",
                    str(self.config.worktree),
                    "remote",
                    "get-url",
                    "origin",
                ],
                "stdout": ORIGIN_TEXT,
            }
        )
        rules["orca-ide"].append(
            {
                "argv_prefix": ["skills", "list", "--json"],
                "stdout": json.dumps(PROBE_REPLY),
            }
        )
        if launch_reply is not None:
            rules["orca-ide"].append(
                {"argv_prefix": ["agent", "launch"], "stdout": json.dumps(launch_reply)}
            )
        return write_scenario(self.tmp_path, rules)


def make_watcher(tmp_path: Path, stub_path: dict[str, str]) -> Watcher:
    stub_path["IW_STUB_STATE_DIR"] = str(tmp_path / "state")
    return Watcher(tmp_path, stub_path)


def world_for(watcher: Watcher, *, now: datetime | None = None) -> GhWorld:
    """A ``GhWorld`` whose clock is the real time, for the G1 ``Date`` header."""
    clock = FakeClock(datetime.now(timezone.utc) if now is None else now)
    return GhWorld(clock, watcher.config)


def argv_of(call: dict) -> tuple[str, list[str]]:
    return call["tool"], call["argv"]


def eligible_issue(world: GhWorld, created: datetime) -> None:
    """Issue 9: trigger, then an approval by the approver, both after ``created``.

    The store was stamped at ``created``, so the trigger comes one second and the
    approval two seconds after it (an approval at or before it is
    ``approval_before_init``). Body and comment edits predate the approval.
    """
    config = world.config
    world.issue(
        ISSUE,
        events=[
            label_event(
                1,
                "labeled",
                config.trigger_label,
                created + timedelta(seconds=1),
                actor_id=2001,
                actor_login="issue-author",
            ),
            label_event(
                2,
                "labeled",
                config.approval_label,
                created + timedelta(seconds=2),
                actor_id=APPROVER_ID,
                actor_login=OWN_LOGIN,
            ),
        ],
        edits={
            "created_at": created - timedelta(seconds=30),
            "comments": [
                {
                    "id": 5001,
                    "author": "issue-author",
                    "created_at": created - timedelta(seconds=20),
                    "edited_at": None,
                }
            ],
        },
    )


def launch_argv_literal(orca: str, worktree: Path) -> list[str]:
    """The FR-013 argv, written out element by element (12 elements)."""
    return [
        orca,
        "agent",
        "launch",
        "--agent",
        "claude",
        "--worktree",
        f"path:{worktree}",
        "--surface",
        "terminal",
        "--prompt",
        "/sc:issue --claim 9",
        "--json",
    ]


def expected_eligible_sequence(watcher: Watcher) -> list[tuple[str, list[str]]]:
    """Every external call of the one-eligible-issue cycle, in order (FR-001)."""
    wt = str(watcher.config.worktree)
    git = ["-C", wt, "remote", "get-url", "origin"]
    return [
        ("gh", USER_ARGV),
        ("git", git),
        ("gh", DISCOVERY_ARGV),
        ("gh", github.argv_comments(ISSUE, 1)[1:]),
        ("gh", github.argv_events(ISSUE, 1)[1:]),
        ("gh", github.argv_edits(ISSUE)[1:]),
        ("gh", github.argv_project_items(ISSUE)[1:]),
        ("orca-ide", ["skills", "list", "--json"]),
        ("gh", github.argv_reread(ISSUE)[1:]),
        ("gh", github.argv_events(ISSUE, 1)[1:]),
        ("gh", github.argv_project_items(ISSUE)[1:]),
        ("git", git),
        ("orca-ide", launch_argv_literal("ORCA", watcher.config.worktree)[1:]),
    ]


def test_ac1_fixture_guard_names_resolve_to_stubs(tmp_path, stub_path):
    """AC-1 guard: only the four stubs are reachable, nothing else."""
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


def test_fr001_idle_cycle_makes_exactly_two_gh_calls(tmp_path, stub_path):
    """FR-001 GWT, NFR-009: an idle cycle exits 0 after `api user` and discovery."""
    assert_local_filesystem(tmp_path)
    watcher = make_watcher(tmp_path, stub_path)
    watcher.init_state()
    world = world_for(watcher)  # no issue: discovery lists nothing
    watcher.script(world)

    done = watcher.cli("once")

    assert done.returncode == 0, done
    assert done.stdout == "cycle: cycle_complete\nexit: 0\n", done.stdout
    assert done.stderr == ""
    calls = watcher.calls()
    gh_calls = [argv_of(c)[1] for c in calls if c["tool"] == "gh"]
    assert gh_calls == [USER_ARGV, DISCOVERY_ARGV], gh_calls
    assert [c["tool"] for c in calls] == ["gh", "git", "gh"], calls
    assert not [c for c in calls if c["tool"] in ("orca", "orca-ide")], calls
    cycle_lines = [x for x in watcher.audit_lines() if x["kind"] == "cycle"]
    assert len(cycle_lines) == 1, watcher.audit_lines()
    line = cycle_lines[0]
    assert (line["exit"], line["reason"], line["dry_run"]) == (
        0,
        "cycle_complete",
        False,
    )
    assert (line["login"], line["gh_calls"], line["discovery_count"]) == (
        OWN_LOGIN,
        2,
        0,
    )
    assert watcher.store()["entries"] == {}
    assert watcher.store()["last_completed_cycle_at"] is not None


def test_fr010_fr013_eligible_issue_launches_once_through_orca_ide(tmp_path, stub_path):
    """FR-010, FR-013, FR-003, AC-1: one launch, 12-element argv, pending at launch."""
    assert_local_filesystem(tmp_path)
    watcher = make_watcher(tmp_path, stub_path)
    created = watcher.init_state()
    world = world_for(watcher)
    eligible_issue(world, created)
    watcher.script(
        world, launch_reply=load_fixture("orca_launch_success.json")["payload"]
    )
    orca_ide = str(watcher.stubbin / "orca-ide")

    done = watcher.cli("once")

    assert done.returncode == 0, done
    assert done.stdout == "cycle: cycle_complete\nexit: 0\n", done.stdout
    assert done.stderr == ""
    calls = watcher.calls()
    # every external call, in order; the stub never sees the program path
    assert [argv_of(c) for c in calls] == expected_eligible_sequence(watcher), [
        argv_of(c) for c in calls
    ]
    # FR-013: the 12-element argv, with the program path, equals the literal list
    launches = [c for c in calls if c["argv"][:2] == ["agent", "launch"]]
    assert len(launches) == 1, launches
    launch_call = launches[0]
    assert launch_call["tool"] == "orca-ide"
    assert [orca_ide, *launch_call["argv"]] == launch_argv_literal(
        orca_ide, watcher.config.worktree
    )
    assert len([orca_ide, *launch_call["argv"]]) == 12
    assert launch_call["argv"][launch_call["argv"].index("--prompt") + 1] == (
        "/sc:issue --claim 9"
    )
    assert Path(launch_call["cwd"]).resolve() == watcher.config.worktree.resolve()
    # orca-ide is resolved first, so the plain orca stub is never called
    assert not [c for c in calls if c["tool"] == "orca"], calls
    # FR-003: the discovery argv is the literal list and asks for no text field
    discoveries = [c for c in calls if c["argv"][:2] == ["issue", "list"]]
    assert [c["argv"] for c in discoveries] == [DISCOVERY_ARGV]
    for call in calls:
        for arg in call["argv"]:
            assert not {"title", "body", "comments"} & set(arg.split(",")), arg
    # FR-010: the entry was already pending, launches 1, consumed_at set, at launch time
    assert "dispatch_json" in launch_call, launch_call
    at_launch = json.loads(launch_call["dispatch_json"])["entries"][str(ISSUE)]
    assert at_launch["state"] == "pending", at_launch
    assert at_launch["launches"] == 1, at_launch
    assert at_launch["consumed_at"] is not None, at_launch
    assert at_launch["launch_cwd"] == str(watcher.config.worktree), at_launch
    # no other stub call took a snapshot
    assert [c["call"] for c in calls if "dispatch_json" in c] == [launch_call["call"]]
    # the final store shows the launch
    final = watcher.store()["entries"][str(ISSUE)]
    assert final["state"] == "launched", final
    assert final["launches"] == 1, final
    assert final["operation_id"] == "op-test-0001", final
    # the audit trail: one launched decision, then the cycle line
    lines = watcher.audit_lines()
    decisions = [x for x in lines if x["kind"] == "decision"]
    assert [(x["issue"], x["reason"], x["state"]) for x in decisions] == [
        (ISSUE, "launched", "launched")
    ], lines
    assert lines[-1]["kind"] == "cycle"
    assert (lines[-1]["exit"], lines[-1]["reason"]) == (0, "cycle_complete")


def test_nfr010_second_once_launches_nothing(tmp_path, stub_path):
    """NFR-010: the second `once` on the same state makes no launch."""
    assert_local_filesystem(tmp_path)
    watcher = make_watcher(tmp_path, stub_path)
    created = watcher.init_state()
    world = world_for(watcher)
    eligible_issue(world, created)
    watcher.script(
        world, launch_reply=load_fixture("orca_launch_success.json")["payload"]
    )

    first = watcher.cli("once")
    assert (first.returncode, first.stdout) == (0, "cycle: cycle_complete\nexit: 0\n")
    first_calls = len(watcher.calls())
    entry_after_first = watcher.store()["entries"][str(ISSUE)]
    assert entry_after_first["state"] == "launched"

    second = watcher.cli("once")

    assert second.returncode == 0, second
    assert second.stdout == "cycle: cycle_complete\nexit: 0\n", second.stdout
    assert second.stderr == ""
    calls = watcher.calls()
    launches = [c for c in calls if c["argv"][:2] == ["agent", "launch"]]
    assert len(launches) == 1, launches  # still the one of the first run
    second_calls = calls[first_calls:]
    assert not [c for c in second_calls if c["tool"] in ("orca", "orca-ide")], (
        second_calls
    )
    # the dispatched issue is only checked for a claim marker (comments read)
    assert [argv_of(c) for c in second_calls] == [
        ("gh", USER_ARGV),
        ("git", ["-C", str(watcher.config.worktree), "remote", "get-url", "origin"]),
        ("gh", DISCOVERY_ARGV),
        ("gh", github.argv_comments(ISSUE, 1)[1:]),
    ], [argv_of(c) for c in second_calls]
    # the store entry is unchanged: one launch, same operation, same consumption
    entry_after_second = watcher.store()["entries"][str(ISSUE)]
    for key in ("state", "launches", "operation_id", "consumed_at", "pending_at"):
        assert entry_after_second[key] == entry_after_first[key], key
    decisions = [x for x in watcher.audit_lines() if x["kind"] == "decision"]
    assert [x["reason"] for x in decisions] == ["launched", "already_dispatched"]
    assert [x["issue"] for x in decisions] == [ISSUE, ISSUE]
