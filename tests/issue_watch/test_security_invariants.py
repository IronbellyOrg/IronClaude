"""Security invariants of the issue watcher (plan step 8.3).

These tests pin the controls of design section 9.1 that cut across modules:

- T1, NFR-001, AC-7: the only text a poll types into a session is
  ``/sc:orchestrator --wake <wake id>`` for an id of the one wake-id shape, and
  the only text in a mailbox message is that id, whatever GitHub, the config or
  the login holds.
- T5, T9, NFR-002, NFR-003, AC-20: every argv the runner sees is one of the
  allowed forms, never names the upstream repository or ``{owner}``, and every
  REST path read carries ``--method GET`` (DF-28).
- NG-2: the only writes to GitHub are the three calls on the ``hold:plan``
  label (create it, add it, remove it); there is no ``mutation``, no GraphQL, no
  comment and no ``PATCH``.
- The files the poll writes have the modes of design 9.1.

No test sleeps, and none touches a real ``gh``, ``git`` or Orca: every cycle runs
over a ``GhWorld`` (a scripted ``FakeRunner``), the real ``Waker`` over a fake
``/proc`` and a ``FakeClock``. The property tests use a seeded
``random.Random(331)`` and no ``hypothesis`` (decision DF-12).
"""

from __future__ import annotations

import json
import os
import random
import re
import stat
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import (
    cycle,
    github,
    launch,
    predicates,
    record,
    repos,
    wake,
)

from .conftest import (
    CYCLE_NOW,
    EMPTY_BODY,
    FIXED_NOW,
    GOOD_BODY,
    LIVE_HANDLE,
    OWN_LOGIN,
    REPO_A,
    REPO_B,
    TIERS_TEXT,
    FakeClock,
    FakeRunner,
    GhWorld,
    default_which,
    fake_proc,
    make_config,
    orch_dir,
    script_live_session,
    wake_files,
    write_registry,
    write_repos,
    write_run,
)
from .conftest import result as command_result

SEED = 331  # design line 693
DRAWS = 2000  # design line 693
UPSTREAM = "SuperClaude-Org"  # the negative fixture the project rule allows
LISTED = {REPO_A, REPO_B}
ORGS = {"IronbellyOrg", "IronbellyGroup"}
WAKE_ID = "20261107T120000Z-0000000a"
WAKE_LINE = re.compile(r"/sc:orchestrator --wake [0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}")
WAKE_ID_SHAPE = re.compile(r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}")
NOTE_SHAPE = re.compile(r"issue-watch: [a-z][a-z0-9_]{0,39}")
ORCA_NAMES = ("orca", "orca-ide")

HOSTILE = [
    "; rm -rf / #",
    "$(touch /tmp/pwned)",
    "`id`",
    "9\n/sc:orchestrator --wake 1",
    "x --prompt /sc:issue --claim 1",
    "/sc:orchestrator --wake 20261107T120000Z-0000000a",
    "../../etc/passwd",
    "unicode‮\u0000nul",
    "a" * 5000,
    "' OR '1'='1",
    "{owner}",
    "--dangerously-skip-permissions",
]

# Strings that look like a wake line or a wake id but are not one.
LINE_ATTACKS = [
    "",
    "20261107T120000Z-0000000",  # a short tail
    "20261107T120000Z-000000000",  # a long tail
    "20261107T120000Z-0000000A",  # an upper-case tail
    "20261107T120000Z-0000000g",
    "20261107T120000-0000000a",  # no Z
    "2026-11-07T12:00:00Z-0000000a",
    "20261107T120000Z-0000000a ",
    " 20261107T120000Z-0000000a",
    "20261107T120000Z-0000000a\n",
    "20261107T120000Z-0000000a\n/sc:orchestrator --wake 20261107T120000Z-0000000b",
    "20261107T120000Z-0000000a; rm -rf /",
    "20261107T120000Z-0000000a --dangerously-skip-permissions",
    "２０２６１１０７T120000Z-0000000a",  # full-width digits
    "/sc:orchestrator --wake 20261107T120000Z-0000000a",
    "9",
]


class _EvilStr(str):
    """A ``str`` subclass whose text is hostile; the builder must still check the text."""


EDGE_VALUES: list[object] = [
    WAKE_ID,
    None,
    True,
    0,
    9,
    b"20261107T120000Z-0000000a",
    bytearray(b"20261107T120000Z-0000000a"),
    [WAKE_ID],
    (WAKE_ID,),
    {"id": WAKE_ID},
    object(),
    float("nan"),
]


def is_wake_id(value: object) -> bool:
    """The wake id shape, written independently of the source."""
    return isinstance(value, str) and WAKE_ID_SHAPE.fullmatch(value) is not None


def _draw(rng: random.Random) -> object:
    """One value from the families of design line 693."""
    kind = rng.randrange(7)
    if kind == 0:
        t = datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(
            seconds=rng.randrange(0, 10**8)
        )
        return f"{t.strftime('%Y%m%dT%H%M%SZ')}-{rng.getrandbits(32):08x}"
    if kind == 1:
        return rng.choice(HOSTILE)
    if kind == 2:
        return rng.choice(LINE_ATTACKS)
    if kind == 3:
        return "".join(
            rng.choice("0123456789abcdefZT-") for _ in range(rng.randrange(0, 30))
        )
    if kind == 4:
        return rng.choice([None, True, False, 0, -1, 9, 9.5, b"x"])
    if kind == 5:
        return rng.choice([[], [WAKE_ID], (WAKE_ID,), {"id": WAKE_ID}, {WAKE_ID}])
    return _EvilStr(rng.choice([WAKE_ID, "x\n" + WAKE_ID, WAKE_ID + "\n"]))


# ==============================================================================
# NFR-001, AC-7: the typed line and the mailbox message hold the wake id only
# ==============================================================================


def test_wake_line_property(tmp_path):
    """AC-7, NFR-001: the line is built only from a wake id and matches the line pattern."""
    rng = random.Random(SEED)
    draws = list(EDGE_VALUES) + [_draw(rng) for _ in range(DRAWS)]
    runner = FakeRunner()
    waker = wake.Waker(runner, proc_root=tmp_path, sleep=lambda s: None)
    target = wake.WakeTargetRun("ironclaude-1", "t-1", tmp_path, "run_1", "tier1b")
    now = CYCLE_NOW
    kinds, valid = Counter(), Counter()
    for index, value in enumerate(draws):
        where = f"draw {index}: {value!r:.200} ({type(value).__name__})"
        kinds[type(value).__name__] += 1
        if is_wake_id(value):
            valid["valid"] += 1
            line = launch.build_wake_line(value)
            assert line == f"/sc:orchestrator --wake {value}", where
            assert WAKE_LINE.fullmatch(line), where
        else:
            valid["invalid"] += 1
            with pytest.raises(ValueError):
                launch.build_wake_line(value)
            # the delivery refuses it before any call: nothing is sent, nothing is typed
            with pytest.raises(ValueError):
                waker.deliver("/o/orca", target, value, now, 20.0)  # type: ignore[arg-type]
            assert runner.calls == [], where
    assert valid["valid"] >= 200 and valid["invalid"] >= 1200, valid
    assert {"str", "NoneType", "bool", "int", "list", "tuple", "dict"} <= set(kinds), (
        kinds
    )
    for attack in LINE_ATTACKS:
        with pytest.raises(ValueError):
            launch.build_wake_line(attack)
    assert runner.calls == []


def test_new_wake_id_is_always_in_the_shape_and_refuses_a_bad_tail():
    created = datetime(2026, 11, 7, 12, 0, tzinfo=timezone.utc)
    assert WAKE_ID_SHAPE.fullmatch(wake.new_wake_id(created))
    assert wake.new_wake_id(created, "0000000a") == WAKE_ID
    for tail in ("0000000A", "xyz", "0000000", "000000000", "0000000a\n", "../x"):
        with pytest.raises(ValueError):
            wake.new_wake_id(created, tail)


@pytest.mark.parametrize(
    "tag", [*HOSTILE, "", "a b", "a" * 80, "-lead", "--tier", ".dot", "x;y"]
)
def test_a_session_command_refuses_a_hostile_tag(tag):
    with pytest.raises(ValueError):
        launch.session_command(tag, "tier1b")


@pytest.mark.parametrize("tier", [*HOSTILE, "", "tier 1", "TIER1", "t;x", "a" * 80])
def test_a_session_command_refuses_a_hostile_tier(tier):
    with pytest.raises(ValueError):
        launch.session_command("orchestrator-ironclaude-1", tier)


def test_a_session_command_is_one_fixed_shape():
    assert (
        launch.session_command("orchestrator-ironclaude-1", "tier1b")
        == "ccsession orchestrator-ironclaude-1 --tier tier1b"
    )


@pytest.mark.parametrize(
    "title",
    [
        *HOSTILE,
        "tab\tand\nnewline",
        "bell\x07",
        "esc\x1b[31mred",
        "x" * 5000,
        "",
        "‮text",
    ],
    ids=lambda v: repr(v)[:20],
)
def test_a_plan_title_is_printable_and_short_and_never_empty(title):
    clean = wake.clean_title(title)
    assert clean.isprintable() and 1 <= len(clean) <= wake.PLAN_TITLE_MAX


@pytest.mark.parametrize(
    ("repo", "number"),
    [
        ("o/r", 0),
        ("o/r", True),
        ("o/r", "9"),
        ("o r/x", 9),
        ("o/r\n", 9),
        ("/r", 9),
        ("o/r", 10**9),
    ],
)
def test_an_issue_url_is_only_built_from_a_valid_repo_and_number(repo, number):
    with pytest.raises(ValueError):
        wake.issue_url(repo, number)
    assert wake.issue_url("o/r", 9) == "https://github.com/o/r/issues/9"


# ==============================================================================
# The cycle harness: a GhWorld over a real store, the real Waker over a fake /proc,
# so every argv goes through one runner.
# ==============================================================================


def classify_argv(argv: object, listed: set[str] = LISTED) -> str:
    """Return the NFR-002 form name of ``argv`` or fail with the offending argv."""
    argv = list(argv)  # type: ignore[call-overload]
    shown = f"offending argv: {argv!r:.600}"
    assert argv and all(isinstance(a, str) for a in argv), shown
    # NFR-003, T5: the upstream repository and the placeholder never appear.
    for needle in (UPSTREAM, "{owner}"):
        assert not any(needle.lower() in a.lower() for a in argv), f"{needle}: {shown}"
    # NG-2: no mutation, no GraphQL, no comment, no PATCH or PUT.
    assert not any("mutation" in a.lower() or a == "graphql" for a in argv), shown
    assert not any(re.search(r"/comments?\b", a) for a in argv), shown
    assert argv[1:3] != ["issue", "comment"] and argv[1:3] != ["issue", "edit"], shown
    assert not any(a.upper() in ("PUT", "PATCH") for a in argv), shown

    def repo_of(path: str) -> str:
        m = re.match(r"repos/([^/]+/[^/]+)/", path)
        assert m and m.group(1) in listed, shown
        return m.group(1)

    if argv == ["gh", "api", "user", "--include"]:
        return "user"
    if argv == ["ccsession", "--help"]:
        return "tiers"
    if argv[:2] == ["gh", "api"]:
        assert argv[2] in ("--method",) and argv[3] in ("GET", "POST", "DELETE"), shown
        method, path = argv[3], argv[4]
        if path == "search/issues":
            assert method == "GET" and len(argv) == 11, shown
            assert argv[5] == "-f" and argv[7:10] == ["-F", "per_page=100", "--jq"], (
                shown
            )
            query = argv[6]
            m = re.fullmatch(
                r"q=is:issue is:open assignee:([A-Za-z0-9-]{1,39}) org:([A-Za-z0-9-]{1,39})",
                query,
            )
            if m:
                assert m.group(2) in ORGS and argv[10] == github.SEARCH_ASSIGNED_JQ, (
                    shown
                )
                return "search_assigned"
            assert re.fullmatch(
                r"q=(mentions:[A-Za-z0-9-]{1,39} updated:>=[0-9T:Z-]{20} org:[A-Za-z0-9-]{1,39}"
                r"|is:issue is:open no:assignee created:>=[0-9T:Z-]{20} org:[A-Za-z0-9-]{1,39}"
                r"|involves:[A-Za-z0-9-]{1,39} updated:>=[0-9T:Z-]{20} org:[A-Za-z0-9-]{1,39}"
                r" -assignee:[A-Za-z0-9-]{1,39})",
                query,
            ), shown
            assert argv[10] == github.SEARCH_INFO_JQ, shown
            return "search_info"
        repo = repo_of(path)
        if method == "GET" and re.fullmatch(
            rf"repos/{re.escape(repo)}/issues/[1-9][0-9]{{0,8}}", path
        ):
            assert argv[5:] == ["--jq", github.REREAD_JQ], shown
            return "reread"
        if method == "GET" and path.endswith("/timeline"):
            assert re.fullmatch(
                rf"repos/{re.escape(repo)}/issues/[1-9][0-9]{{0,8}}/timeline", path
            ), shown
            assert argv[5:] == ["-F", "per_page=100", "--jq", github.TIMELINE_JQ], shown
            return "timeline"
        if method == "GET" and "/branches/" in path:
            assert re.fullmatch(
                rf"repos/{re.escape(repo)}/branches/[A-Za-z0-9._/-]{{1,200}}", path
            ), shown
            assert (
                not path.split("/branches/")[1].startswith("-") and ".." not in path
            ), shown
            assert argv[5:] == ["--jq", github.BRANCH_JQ], shown
            return "branch"
        if method == "GET":
            assert path == f"repos/{repo}/labels/hold:plan" and len(argv) == 5, shown
            return "label_get"
        # The three writes: all on the one label, nothing else.
        if method == "POST" and path == f"repos/{repo}/labels":
            assert argv[5:] == [
                "-f", "name=hold:plan", "-f", "color=FBCA04",
                "-f", "description=The issue has no plan yet; set by the issue watcher",
            ], shown  # fmt: skip
            return "label_create"
        if method == "POST":
            assert re.fullmatch(
                rf"repos/{re.escape(repo)}/issues/[1-9][0-9]{{0,8}}/labels", path
            ), shown
            assert argv[5:] == ["-f", "labels[]=hold:plan"], shown
            return "label_add"
        assert method == "DELETE", shown
        assert re.fullmatch(
            rf"repos/{re.escape(repo)}/issues/[1-9][0-9]{{0,8}}/labels/hold:plan", path
        ), shown
        assert len(argv) == 5, shown
        return "label_remove"
    if argv[:2] == ["gh", "issue"]:
        if argv[2] == "develop":
            assert argv[3] == "--list" and re.fullmatch(r"[1-9][0-9]{0,8}", argv[4]), (
                shown
            )
            assert argv[5] == "--repo" and argv[6] in listed and len(argv) == 7, shown
            return "develop"
        assert argv[2] == "view" and re.fullmatch(r"[1-9][0-9]{0,8}", argv[3]), shown
        assert argv[4] == "--repo" and argv[5] in listed and argv[6] == "--json", shown
        assert argv[7] in ("updatedAt", "labels") and len(argv) == 8, shown
        return "issue_view"
    if argv[0] == "git":
        assert len(argv) == 6 and argv[1] == "-C" and os.path.isabs(argv[2]), shown
        assert argv[3:] == ["remote", "get-url", "origin"], shown
        return "origin"
    assert os.path.isabs(argv[0]) and os.path.basename(argv[0]) in ORCA_NAMES, shown
    rest = argv[1:]
    if rest == ["skills", "list", "--json"]:
        return "probe"
    if rest[:2] == ["terminal", "list"]:
        assert rest[2] == "--worktree" and rest[3].startswith("path:/"), shown
        assert rest[4:] == ["--json"], shown
        return "terminal_list"
    if rest[:2] == ["terminal", "create"]:
        assert rest[2] == "--worktree" and rest[3].startswith("path:/"), shown
        assert rest[4:] == ["--json"], shown
        return "terminal_create"
    if rest[:2] == ["terminal", "read"]:
        assert re.fullmatch(r"term_[A-Za-z0-9_-]+", rest[3]), shown
        assert rest[2] == "--terminal" and rest[4:] == ["--screen", "--json"], shown
        return "terminal_read"
    if rest[:2] == ["terminal", "wait"]:
        assert rest[2] == "--terminal" and rest[4:6] == ["--for", "tui-idle"], shown
        assert (
            rest[6] == "--timeout-ms" and rest[7].isdigit() and rest[8:] == ["--json"]
        ), shown
        return "terminal_wait"
    if rest[:2] == ["terminal", "send"]:
        assert rest[2] == "--terminal" and re.fullmatch(
            r"term_[A-Za-z0-9_-]+", rest[3]
        ), shown
        assert rest[4] == "--text" and (
            WAKE_LINE.fullmatch(rest[5])
            or re.fullmatch(
                r"orchestrator-[a-z0-9]{1,12}-[1-9][0-9]{0,5}", rest[5]
            )  # the name question
            or re.fullmatch(
                r"ccsession orchestrator-[a-z0-9-]+ --tier [a-z0-9]+", rest[5]
            )
        ), shown
        assert rest[6:] in (
            ["--enter", "--wait-submit", "15", "--json"],
            ["--enter", "--wait-submit", "5", "--json"],
        ), shown
        return "terminal_send"
    if rest[:2] == ["orchestration", "send"]:
        assert rest[2] == "--to" and re.fullmatch(r"run:[A-Za-z0-9_-]+", rest[3]), shown
        assert rest[4:6] == ["--type", "status"], shown
        assert rest[6] == "--subject" and re.fullmatch(
            r"orchestrator-wake " + WAKE_ID_SHAPE.pattern, rest[7]
        ), shown
        payload = json.loads(rest[9])
        assert rest[8] == "--payload" and rest[10:] == ["--json"], shown
        assert set(payload) == {"kind", "wake_id"} and is_wake_id(payload["wake_id"]), (
            shown
        )
        return "mailbox"
    if rest[:2] == ["worktree", "set"]:
        assert rest[2] == "--worktree" and rest[3].startswith("path:/"), shown
        assert rest[4] == "--unread" and rest[5] == "--comment", shown
        assert NOTE_SHAPE.fullmatch(rest[6]) and rest[7:] == ["--json"], shown
        return "unread_mark"
    if rest[:2] == ["worktree", "show"]:
        assert (
            re.fullmatch(r"issue:[1-9][0-9]{0,8}", rest[3]) and rest[2] == "--worktree"
        ), shown
        assert rest[4:] == ["--json"], shown
        return "worktree_show"
    if rest[:2] == ["reference", "find"]:
        assert re.fullmatch(
            r"https://github\.com/[^/]+/[^/]+/issues/[1-9][0-9]{0,8}", rest[2]
        ), shown
        assert rest[3:] == ["--json"], shown
        return "reference_find"
    raise AssertionError(shown)


WRITE_FORMS = {"label_create", "label_add", "label_remove"}
ORCA_ACTION_FORMS = {
    "terminal_create",
    "terminal_send",
    "mailbox",
    "unread_mark",
}


@dataclass
class Ran:
    """What one scripted scenario did."""

    results: list[cycle.CycleResult]
    world: GhWorld
    store: record.FileStore
    forms: list[str]
    argvs: list[tuple[str, ...]]

    @property
    def lines(self) -> list[dict]:
        path = self.store.state_dir / "audit.jsonl"
        return [json.loads(t) for t in path.read_text(encoding="utf-8").splitlines()]


Play = Callable[[GhWorld, Callable[..., cycle.CycleResult]], None]


def run_world(root: Path, play: Play, **world_kwargs: object) -> Ran:
    """Run ``play`` over a world in ``root`` and classify every argv.

    ``play(world, step)``: add issues to the world, then call ``step(advance=0,
    dry=False)`` for each cycle. The orchestrator ``ironclaude-1`` is registered
    with a live Run and a live session, so a wake is typed for real.
    """
    root.mkdir(parents=True, exist_ok=True)
    store = record.init_state(root / "state", FIXED_NOW, baseline=False)
    config = make_config(root)
    write_registry(config, {"ironclaude-1": {}})
    write_run(config, "ironclaude-1")
    runner = FakeRunner()
    world = GhWorld(FakeClock(CYCLE_NOW), config, runner=runner, **world_kwargs)
    script_live_session(runner)
    waker = wake.Waker(runner, proc_root=fake_proc(root), sleep=lambda s: None)
    results: list[cycle.CycleResult] = []

    def step(advance: float = 0, dry: bool = False) -> cycle.CycleResult:
        world.clock.advance(advance)
        res = cycle.run_cycle(world.deps(root, store, waker=waker), dry)
        results.append(res)
        return res

    play(world, step)
    assert not runner.unexpected, f"unscripted argv: {runner.unexpected}"
    argvs = [argv for argv, _ in runner.calls]
    forms = [classify_argv(argv) for argv in argvs]
    # FR-029 (design 8.5): every call has a timeout of at most 120 s; gh, git and
    # the probes get 5..20 s.
    for form, (argv, _cwd), seconds in zip(forms, runner.calls, runner.timeouts):
        assert 0 < seconds <= 120.0, (argv, seconds)
        if form in WRITE_FORMS or form in {
            "user",
            "search_assigned",
            "search_info",
            "reread",
            "origin",
            "probe",
        }:
            assert 5.0 <= seconds <= 20.0, (argv, seconds)
    return Ran(results, world, store, forms, argvs)


# -- the scenarios of the argv scan ---------------------------------------------


def _idle(world, step):
    step()


def _wake(world, step):
    world.issue(REPO_A, 9)
    step()


def _hold_and_request(world, step):
    world.issue(REPO_A, 5, body=EMPTY_BODY, branches=[("issue-5-x", CYCLE_NOW)])
    step()
    step(advance=3600)


def _wake_and_hold(world, step):
    world.issue(REPO_A, 9)
    world.issue(REPO_A, 5, body=EMPTY_BODY, branches=[("issue-5-x", CYCLE_NOW)])
    step()
    step(advance=3600)


def _release(world, step):
    world.issue(REPO_A, 5, body=EMPTY_BODY)
    step()
    world.issues[(REPO_A, 5)].body = GOOD_BODY
    step(advance=300)
    step(advance=300)


def _backlog(world, step):
    world.issue(REPO_A, 5, body=EMPTY_BODY, labels=["hold:backlog"])
    step()


def _dry_run(world, step):
    world.issue(REPO_A, 9)
    world.issue(REPO_A, 5, body=EMPTY_BODY)
    step(dry=True)
    step(advance=3600, dry=True)


def _rate_limited(world, step):
    world.issue(REPO_A, 9)
    world.fail("search", "rate", times=None)
    step()


SCENARIOS: dict[str, Play] = {
    "idle": _idle,
    "wake": _wake,
    "hold_and_request": _hold_and_request,
    "wake_and_hold": _wake_and_hold,
    "release": _release,
    "backlog": _backlog,
    "dry_run": _dry_run,
    "rate_limited": _rate_limited,
}


@pytest.mark.parametrize("name", list(SCENARIOS))
def test_every_argv_of_a_scenario_is_an_allowed_form(tmp_path, name):
    """AC-20, NFR-002, NFR-003: every argv of every cycle is one allowed form."""
    ran = run_world(tmp_path, SCENARIOS[name])
    assert ran.forms, name  # the scan saw calls
    cycle_lines = [ln for ln in ran.lines if ln["kind"] == "cycle"]
    assert len(cycle_lines) == len(ran.results)
    gh = sum(
        f
        in {
            "user", "search_assigned", "search_info", "reread", "issue_view", "develop",
            "branch", "timeline", "label_get", "label_create", "label_add", "label_remove",
        }
        for f in ran.forms
    )  # fmt: skip
    assert sum(ln["gh_calls"] for ln in cycle_lines) == gh, name


def test_the_scenarios_together_use_every_allowed_form(tmp_path):
    """AC-20: GET only on reads, the label writes and the Orca calls are all reached."""
    seen: Counter[str] = Counter()
    every: list[tuple[str, ...]] = []
    for name, play in SCENARIOS.items():
        ran = run_world(tmp_path / name, play)
        seen.update(ran.forms)
        every += ran.argvs
    required = {
        "user", "tiers", "search_assigned", "search_info", "reread", "issue_view",
        "develop", "branch", "timeline", "label_get", "label_create", "label_add",
        "label_remove", "origin", "probe", "terminal_list", "terminal_read",
        "terminal_wait", "terminal_send", "mailbox", "worktree_show", "reference_find",
    }  # fmt: skip
    assert required <= set(seen), sorted(required - set(seen))
    assert set(seen) <= required | {"unread_mark", "terminal_create"}, seen
    for argv in every:
        assert not any(UPSTREAM.lower() in a.lower() for a in argv), argv
        assert not any("{owner}" in a for a in argv), argv
        if argv[:2] == ("gh", "api") and argv[2] != "user":
            assert argv[2] == "--method" and argv[3] in ("GET", "POST", "DELETE"), argv
    # NG-2 over all of them at once: writes are the three calls on the hold label.
    writes = [
        a
        for a in every
        if a[:2] == ("gh", "api") and a[3] != "GET" and a[2] == "--method"
    ]
    assert writes and all("hold:plan" in " ".join(a) for a in writes), writes
    assert {a[3] for a in writes} == {"POST", "DELETE"}


def test_a_dry_run_makes_no_write_and_no_orca_action(tmp_path):
    ran = run_world(tmp_path, _dry_run)
    assert not (set(ran.forms) & (WRITE_FORMS | ORCA_ACTION_FORMS)), ran.forms
    assert {r.would_wake for r in ran.results} >= {(f"{REPO_A}#9",)}
    assert wake_files(ran.world.config) == []
    assert not (ran.store.state_dir / "dispatch.json").read_text().count("woken")


def test_the_backlog_label_is_never_written_and_nothing_is_read_for_it(tmp_path):
    ran = run_world(tmp_path, _backlog)
    assert not (
        set(ran.forms) & (WRITE_FORMS | ORCA_ACTION_FORMS | {"reread", "develop"})
    )
    assert all("hold:backlog" not in " ".join(a) for a in ran.argvs)


def test_the_typed_line_the_cycle_sends_is_the_wake_line(tmp_path):
    ran = run_world(tmp_path, _wake)
    sends = [a for a in ran.argvs if a[1:3] == ("terminal", "send")]
    assert len(sends) == 1
    text = sends[0][sends[0].index("--text") + 1]
    (path,) = wake_files(ran.world.config)
    assert text == f"/sc:orchestrator --wake {path.stem}"
    assert sends[0][sends[0].index("--terminal") + 1] == LIVE_HANDLE


# ==============================================================================
# NFR-001, T1: hostile login and hostile config stop before any argv uses them
# ==============================================================================


@pytest.mark.parametrize(
    "login",
    [*HOSTILE, "owner-login\n", "", "bad_login!", "a" * 40, "-lead", "x y"],
    ids=lambda v: repr(v)[:20],
)
def test_a_hostile_own_login_stops_before_any_argv_uses_it(tmp_path, login):
    ran = run_world(tmp_path, _wake, login=login)
    res = ran.results[0]
    assert (res.exit_code, res.reason) == (3, "login_invalid")
    gh = [a for a in ran.argvs if a[0] == "gh"]
    assert gh == [("gh", "api", "user", "--include")], f"login: {login!r:.100}"
    assert not [a for a in ran.argvs if a[0] not in ("gh", "ccsession")]
    assert ran.store.load().entries == {}
    assert wake_files(ran.world.config) == []
    (line,) = ran.lines
    assert (line["kind"], line["exit"], line["reason"]) == ("cycle", 3, "login_invalid")
    assert line["login"] is None  # a rejected login is never written


def _bad_repos(**over):
    def write(orch: Path) -> None:
        write_repos(orch, **over)

    return write


@pytest.mark.parametrize(
    "hostile",
    [
        {"repos": [{"repo": "../../etc", "enabled": True, "checkout": "/tmp/x"}]},
        {"repos": [{"repo": "o/r; rm -rf /", "enabled": True, "checkout": "/tmp/x"}]},
        {
            "repos": [
                {
                    "repo": f"{UPSTREAM}/SuperClaude_Framework x",
                    "enabled": True,
                    "checkout": "/tmp/x",
                }
            ]
        },
        {"repos": [{"repo": REPO_A, "enabled": True, "checkout": "relative/path"}]},
        {
            "repos": [
                {
                    "repo": REPO_A,
                    "enabled": True,
                    "checkout": "/tmp/x",
                    "orchestrator_tier": "tier1b; id",
                }
            ]
        },
        {"repos": [{"repo": REPO_A, "enabled": "yes", "checkout": "/tmp/x"}]},
        {"orgs": ["IronbellyOrg; id"]},
        {"schema_version": 2},
    ],
    ids=lambda v: str(v)[:40],
)
def test_a_hostile_repos_file_is_refused_before_any_github_call(tmp_path, hostile):
    root = tmp_path
    config = make_config(root)
    write_repos(config.orchestrator_repo, **hostile)
    store = record.init_state(root / "state", FIXED_NOW, baseline=False)
    runner = FakeRunner()
    world = GhWorld(FakeClock(CYCLE_NOW), config, runner=runner)
    res = cycle.run_cycle(world.deps(root, store), False)
    assert (res.exit_code, res.reason) == (2, "repos_invalid")
    assert [a for a in runner.argvs() if a[0] != "ccsession"] == []
    assert not runner.unexpected


def test_repos_yaml_is_read_with_safe_load_only(tmp_path):
    """A YAML tag that would run code is refused, and nothing runs."""
    marker = tmp_path / "pwned"
    text = f"!!python/object/apply:os.system ['touch {marker}']\n"
    config = make_config(tmp_path)
    (config.orchestrator_repo / "repos.yaml").write_text(text, encoding="utf-8")
    runner = FakeRunner({("ccsession", "--help"): command_result(stdout=TIERS_TEXT)})
    with pytest.raises(repos.ReposError):
        repos.load_repos(config.orchestrator_repo, runner, 5.0)
    assert not marker.exists()
    src = Path(repos.__file__).read_text(encoding="utf-8")
    assert (
        "yaml.safe_load" in src and "yaml.load(" not in src and "yaml.unsafe" not in src
    )


# ==============================================================================
# NFR-002, NFR-003, AC-20, T5, T9, DF-28: the argv builders and the scan itself
# ==============================================================================


def test_every_argv_builder_of_the_package_gives_an_allowed_form():
    when = datetime(2026, 11, 7, 12, 0, tzinfo=timezone.utc)
    expected: list[tuple[list[str], str]] = [
        (github.argv_user(), "user"),
        (github.argv_search_assigned("IronbellyOrg", OWN_LOGIN), "search_assigned"),
        *(
            (
                github.argv_search_info(s, "IronbellyGroup", OWN_LOGIN, when),
                "search_info",
            )
            for s in github.STREAMS
        ),
    ]
    for repo in (REPO_A, REPO_B):
        expected += [
            (github.argv_label_get(repo), "label_get"),
            (github.argv_label_create(repo), "label_create"),
        ]
        for n in (1, 9, 100, 999_999_999):
            expected += [
                (github.argv_reread(repo, n), "reread"),
                (github.argv_issue_updated(repo, n), "issue_view"),
                (github.argv_issue_labels(repo, n), "issue_view"),
                (github.argv_develop_list(repo, n), "develop"),
                (github.argv_timeline(repo, n), "timeline"),
                (github.argv_label_add(repo, n), "label_add"),
                (github.argv_label_remove(repo, n), "label_remove"),
            ]
        expected.append((github.argv_branch_date(repo, "issue-9-fix/x.y_z"), "branch"))
    recorder = FakeRunner()
    assert (
        launch.check_origin(recorder, Path("/tmp/x"), REPO_A, 5.0) == "origin_mismatch"
    )
    assert launch.find_orca(recorder, which=default_which, timeout=5.0) is None
    expected += [(list(a), f) for a, f in zip(recorder.argvs(), ("origin", "probe"))]
    assert len(recorder.argvs()) == 2
    for argv, form in expected:
        assert classify_argv(argv) == form, argv


def test_the_argv_builders_refuse_hostile_arguments():
    for bad in HOSTILE:
        for build in (
            lambda b: github.argv_reread(b, 9),
            lambda b: github.argv_label_get(b),
            lambda b: github.argv_label_create(b),
            lambda b: github.argv_label_add(b, 9),
            lambda b: github.argv_label_remove(b, 9),
            lambda b: github.argv_develop_list(b, 9),
            lambda b: github.argv_timeline(b, 9),
            lambda b: github.argv_search_assigned(b, OWN_LOGIN),
            lambda b: github.argv_search_assigned("IronbellyOrg", b),
        ):
            with pytest.raises(ValueError):
                build(bad)
    for bad in (0, -1, True, "9", 10**9, 9.0, None, "9; id"):
        with pytest.raises(ValueError):
            github.argv_reread(REPO_A, bad)  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            github.argv_label_add(REPO_A, bad)  # type: ignore[arg-type]
    for name in ("-x", "a..b", "a b", "a;b", "", "x" * 201, "a\nb"):
        with pytest.raises(ValueError):
            github.argv_branch_date(REPO_A, name)


_LABEL_CREATE = github.argv_label_create(REPO_A)
BAD_ARGVS = {
    "post_to_a_comment": ["gh", "api", "--method", "POST", f"repos/{REPO_A}/issues/9/comments", "-f", "body=x"],
    "post_to_another_label": ["gh", "api", "--method", "POST", f"repos/{REPO_A}/issues/9/labels", "-f", "labels[]=bug"],
    "post_to_the_issue": ["gh", "api", "--method", "POST", f"repos/{REPO_A}/issues/9", "-f", "state=closed"],
    "patch_the_issue": ["gh", "api", "--method", "PATCH", f"repos/{REPO_A}/issues/9", "-f", "state=closed"],
    "delete_another_label": ["gh", "api", "--method", "DELETE", f"repos/{REPO_A}/issues/9/labels/bug"],
    "delete_the_issue_labels": ["gh", "api", "--method", "DELETE", f"repos/{REPO_A}/issues/9/labels"],
    "rest_without_method": ["gh", "api", f"repos/{REPO_A}/issues/9", "--jq", github.REREAD_JQ],
    "rest_get_without_jq": ["gh", "api", "--method", "GET", f"repos/{REPO_A}/issues/9"],
    "unlisted_repository": ["gh", "api", "--method", "GET", "repos/other-org/other/issues/9", "--jq", github.REREAD_JQ],
    "upstream_repository": ["gh", "api", "--method", "GET", f"repos/{UPSTREAM}/SuperClaude_Framework/issues/9", "--jq", github.REREAD_JQ],
    "owner_placeholder": ["gh", "api", "--method", "GET", "repos/{owner}/{repo}/issues/9", "--jq", github.REREAD_JQ],
    "another_jq": ["gh", "api", "--method", "GET", f"repos/{REPO_A}/issues/9", "--jq", "."],
    "search_with_another_jq": [*github.argv_search_assigned("IronbellyOrg", OWN_LOGIN)[:-1], "."],
    "search_of_an_unlisted_org": github.argv_search_assigned("other-org", OWN_LOGIN),
    "search_for_a_stranger_text": [*github.argv_search_assigned("IronbellyOrg", OWN_LOGIN)[:6], "q=is:issue is:open assignee:x org:IronbellyOrg label:bug", *github.argv_search_assigned("IronbellyOrg", OWN_LOGIN)[7:]],
    "graphql_mutation": ["gh", "api", "graphql", "-f", "query=mutation { addComment }"],
    "graphql_query": ["gh", "api", "graphql", "-f", "query={ viewer { login } }"],
    "issue_comment": ["gh", "issue", "comment", "9", "--body", "x"],
    "issue_edit": ["gh", "issue", "edit", "9", "--add-label", "x"],
    "issue_view_title": ["gh", "issue", "view", "9", "--repo", REPO_A, "--json", "title"],
    "issue_view_of_the_upstream": ["gh", "issue", "view", "9", "--repo", f"{UPSTREAM}/SuperClaude_Framework", "--json", "labels"],
    "develop_into_a_branch": ["gh", "issue", "develop", "9", "--repo", REPO_A],
    "shell": ["bash", "-c", "gh api user"],
    "git_push": ["git", "push", "origin", "master"],
    "git_relative_directory": ["git", "-C", "rel", "remote", "get-url", "origin"],
    "relative_orca": ["orca", "skills", "list", "--json"],
    "orca_launch": ["/o/orca-ide", "agent", "launch", "--agent", "claude", "--prompt", "/sc:issue --claim 9 --pipeline none", "--json"],
    "typed_free_text": ["/o/orca-ide", "terminal", "send", "--terminal", "term_a", "--text", "do something else", "--enter", "--wait-submit", "15", "--json"],
    "typed_line_with_extra_text": ["/o/orca-ide", "terminal", "send", "--terminal", "term_a", "--text", f"/sc:orchestrator --wake {WAKE_ID} x", "--enter", "--wait-submit", "15", "--json"],
    "mailbox_with_a_title": ["/o/orca-ide", "orchestration", "send", "--to", "run:r1", "--type", "status", "--subject", "orchestrator-wake " + WAKE_ID, "--payload", json.dumps({"kind": "k", "wake_id": WAKE_ID, "title": "t"}), "--json"],
    "mailbox_subject_with_text": ["/o/orca-ide", "orchestration", "send", "--to", "run:r1", "--type", "status", "--subject", "hello", "--payload", json.dumps({"kind": "k", "wake_id": WAKE_ID}), "--json"],
    "unread_note_with_text": ["/o/orca-ide", "worktree", "set", "--worktree", "path:/w", "--unread", "--comment", "a title from GitHub", "--json"],
    "worktree_removal": ["/o/orca-ide", "worktree", "rm", "--worktree", "path:/w"],
}  # fmt: skip


@pytest.mark.parametrize("name", list(BAD_ARGVS))
def test_the_argv_scan_rejects_a_forbidden_argv(name):
    """AC-20, NFR-002, NFR-003: the scan rejects a write, a text field, an upstream."""
    with pytest.raises(AssertionError):
        classify_argv(BAD_ARGVS[name])


def test_the_scan_accepts_the_reference_forms():
    assert classify_argv(github.argv_label_add(REPO_A, 9)) == "label_add"
    assert (
        classify_argv(
            ["/o/orca-ide", "terminal", "send", "--terminal", "term_a", "--text", f"/sc:orchestrator --wake {WAKE_ID}", "--enter", "--wait-submit", "15", "--json"]
        )
        == "terminal_send"
    )  # fmt: skip


# ==============================================================================
# NG-2, NFR-003: the module constants of github.py
# ==============================================================================


def test_no_string_constant_of_github_py_contains_mutation_or_upstream():
    constants = {
        name: value
        for name, value in vars(github).items()
        if isinstance(value, str) and not name.startswith("__")
    }
    # The scan is not vacuous: it sees the constants it exists to guard.
    assert {
        "SEARCH_ASSIGNED_JQ",
        "SEARCH_INFO_JQ",
        "REREAD_JQ",
        "TIMELINE_JQ",
        "BRANCH_JQ",
    } <= set(constants)
    for name, value in constants.items():
        assert "mutation" not in value.lower(), f"github.{name} contains mutation"
        assert "graphql" not in value.lower(), f"github.{name} names GraphQL"
        assert UPSTREAM.lower() not in value.lower(), f"github.{name} names upstream"
        assert "{owner}" not in value, f"github.{name} holds the {{owner}} placeholder"


def test_the_removed_queries_and_launch_builders_are_gone():
    for name in (
        "EDITS_QUERY",
        "PROJECT_ITEMS_QUERY",
        "MARKER_JQ",
        "EVENTS_JQ",
        "REPO",
        "argv_discover",
        "argv_events",
        "argv_comments",
        "argv_edits",
        "argv_project_items",
    ):
        assert not hasattr(github, name), name  # fmt: skip
    for name in ("launch_argv", "build_claim_prompt", "OP_UNKNOWN_TEXT"):
        assert not hasattr(launch, name), name


def test_the_hold_label_writer_asks_the_guard_before_every_write():
    runner = FakeRunner()
    asked: list[list[str]] = []

    def refuse(argv: list[str]) -> str:
        asked.append(argv)
        return "no_grant"

    writer = github.LabelWriter(runner, refuse)
    budget, timeout = github.CallBudget(), (lambda: 5.0)
    for got in (
        writer.ensure(budget, REPO_A, timeout),
        writer.add(budget, REPO_A, 9, timeout),
        writer.remove(budget, REPO_A, 9, timeout),
    ):
        assert got.reason == "hold_write_failed", got
    assert runner.calls == []  # a refused write is never run
    assert [classify_argv(a) for a in asked] == [
        "label_get",
        "label_add",
        "label_remove",
    ]


def test_a_repos_file_with_an_unknown_key_or_an_odd_grant_never_puts_it_in_an_argv(
    tmp_path,
):
    """Unknown keys are ignored (the orchestrator shares the file); a grant is only compared."""
    config = make_config(tmp_path)
    extra = [
        {
            "repo": REPO_A,
            "enabled": True,
            "checkout": str(tmp_path / "checkouts" / "IronClaude"),
            "note": "x; id",
        }
    ]
    write_repos(
        config.orchestrator_repo, repos=extra, grants=["issue.hold", "pr.merge; id"]
    )
    runner = FakeRunner({("ccsession", "--help"): command_result(stdout=TIERS_TEXT)})
    doc = repos.load_repos(config.orchestrator_repo, runner, 5.0)
    assert doc.has_grant("issue.hold") and not doc.has_grant("issue.assign")
    assert "pr.merge; id" in doc.grants and runner.argvs() == [("ccsession", "--help")]


# ==============================================================================
# The files the poll writes (design 9.1)
# ==============================================================================


def test_the_files_the_poll_writes_have_private_modes(tmp_path):
    ran = run_world(tmp_path, _wake_and_hold)
    state = ran.store.state_dir
    assert stat.S_IMODE(state.stat().st_mode) == 0o700
    for name in ("dispatch.json", "lock", "audit.jsonl"):
        assert stat.S_IMODE((state / name).stat().st_mode) == 0o600, name
    files = wake_files(ran.world.config)
    assert files
    for path in files:
        assert stat.S_IMODE(path.stat().st_mode) == 0o600, path
        assert path.stat().st_size <= 64 * 1024
    for sub in (orch_dir(ran.world.config), orch_dir(ran.world.config) / "wakes"):
        assert not stat.S_IMODE(sub.stat().st_mode) & 0o022, (
            sub
        )  # nobody else can write


def test_the_poll_never_writes_an_ack_or_a_rejection_file(tmp_path):
    ran = run_world(tmp_path, _wake_and_hold)
    names = [p.name for p in (orch_dir(ran.world.config) / "wakes").iterdir()]
    assert names and not [
        n for n in names if n.endswith((".ack.json", ".rejected.json"))
    ]


def test_dispatch_json_has_the_schema_2_keys_and_no_text(tmp_path):
    ran = run_world(tmp_path, _wake_and_hold)
    raw = json.loads((ran.store.state_dir / "dispatch.json").read_text("utf-8"))
    assert set(raw) == {
        "schema_version", "created_at", "next_permitted_at", "last_completed_cycle_at",
        "last_poll_at", "rate_streak", "baseline", "info_seen", "consumed_log",
        "entries", "holds",
    }  # fmt: skip
    assert raw["schema_version"] == 2
    entry_keys = {
        "repo", "issue", "state", "attempts", "wake_attempts", "operation_id", "wake_id",
        "woken_at", "ack_reason", "orchestrator", "consumed_at", "pending_at",
        "created_at", "updated_at", "lease_expires_at", "last_reason",
    }  # fmt: skip
    assert raw["entries"] and all(set(e) == entry_keys for e in raw["entries"].values())
    hold_keys = {
        "state", "first_held_at", "seen_updated_at", "last_evidence_at", "evidence_kind",
        "plan_requested_at", "plan_request_orchestrator", "plan_request", "plan_acked_at",
        "plan_wake_id", "plan_attempts", "plan_woken_at", "missing",
    }  # fmt: skip
    assert raw["holds"] and all(set(h) == hold_keys for h in raw["holds"].values())
    assert "A title" not in json.dumps(raw)  # the issue title is not stored


def test_the_predicates_reject_hostile_repos_logins_and_numbers():
    for bad in HOSTILE:
        assert not predicates.valid_repo(bad) and not predicates.valid_login(bad)
    assert not predicates.valid_issue_number(True)
    assert cycle.SCHEMA_VERSION == 2 and record.SCHEMA_VERSION == 2
