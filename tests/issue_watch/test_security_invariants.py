"""Security invariants of the issue watcher (plan step 8.3).

These tests pin the controls of design section 9.1 that cut across modules:

- T1, NFR-001, AC-7: the only text after ``--prompt`` is ``/sc:issue --claim <n>``
  for an ``int`` in 1..999999999, whatever GitHub, the config or the login holds.
- T5, T9, NFR-002, NFR-003, AC-20: every argv the runner sees is one of the
  allowed forms, never names the upstream repository, ``{owner}``, a title or a
  body, and every REST path call carries ``--method GET`` (DF-28).
- NG-2: nothing writes to GitHub (no ``mutation``, no POST to a REST path).
- T10: the launch argv is the 12-element list of FR-013 with no extra flag.

No test sleeps, and none touches a real ``gh``, ``git`` or Orca: every cycle runs
over a ``GhWorld`` (a scripted ``FakeRunner``) and a ``FakeClock``. The property
test uses a seeded ``random.Random(331)`` and no ``hypothesis`` (decision DF-12).
"""

from __future__ import annotations

import json
import os
import random
import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import cycle, github, launch, record
from superclaude.cli.issue_watch.launch import (
    OrcaLauncher,
    build_claim_prompt,
    launch_argv,
)

from .conftest import (
    APPROVER_ID,
    CYCLE_NOW,
    FIXED_NOW,
    ORCA_PATH,
    OWN_LOGIN,
    T_APPROVED,
    T_TRIGGER,
    FakeClock,
    FakeLauncher,
    FakeRunner,
    GhWorld,
    default_which,
    label_event,
    load_fixture,
    make_config,
    marker_comment,
)
from .conftest import result as command_result

SEED = 331  # design line 693
DRAWS = 2000  # design line 693
MAX_N = 999_999_999  # FR-012, written here and not imported
UPSTREAM = "SuperClaude-Org"  # the negative fixture the project rule allows
FORK = "IronbellyOrg/IronClaude"

# Every prompt a launch may carry. ``fullmatch`` (not ``$``) so a trailing newline
# fails too.
_PROMPT_RE = re.compile(r"/sc:issue --claim [1-9][0-9]{0,8}")
_TEXT_FIELD = re.compile(r"(?i)\b(?:title|body\w*)\b")
_REST_PATH = re.compile(
    r"repos/IronbellyOrg/IronClaude/issues/[1-9][0-9]{0,8}(?:/(?:events|comments))?"
)
_QUERIES = ("query=" + github.EDITS_QUERY, "query=" + github.PROJECT_ITEMS_QUERY)
_T_MARK = T_APPROVED + timedelta(minutes=1)  # a claim marker after the approval

HOSTILE = [
    "; rm -rf / #",
    "$(touch /tmp/pwned)",
    "`id`",
    "9\n/sc:issue --claim 1",
    "x --prompt /sc:issue --claim 1",
    "/sc:issue --claim 1",
    "../../etc/passwd",
    "unicode‮\u0000nul",
    "a" * 5000,
    "' OR '1'='1",
    "{owner}",
    "--dangerously-skip-permissions",
]

# Strings that look like a claim prompt but are not one.
PROMPT_ATTACKS = [
    "",
    "/sc:issue --claim 0",
    "/sc:issue --claim 09",
    "/sc:issue --claim 1000000000",
    "/sc:issue --claim -1",
    "/sc:issue --claim 9\n",
    "/sc:issue --claim 9\n/sc:issue --claim 10",
    "/sc:issue --claim 9 ; rm -rf /",
    "/sc:issue --claim 9 --dangerously-skip-permissions",
    "/sc:issue --claim  9",
    " /sc:issue --claim 9",
    "/sc:issue --claim 9 ",
    "/sc:issue --claim 9.0",
    "/sc:issue --claim 0x9",
    "/sc:issue --claim ９",  # a full-width digit
    "/sc:issue --claim True",
    "/sc:issue --claim",
    "/sc:issue --claim abc",
    "/SC:ISSUE --CLAIM 9",
    "sc:issue --claim 9",
    "9",
]


class _EvilInt(int):
    """An ``int`` subclass whose text is hostile; ``type(n) is int`` must reject it."""

    def __str__(self) -> str:
        return "1; rm -rf /"

    __repr__ = __str__


EDGE_VALUES: list[object] = [
    9,  # the FR-012 GWT: only 9 returns a string
    "9",
    True,
    False,
    0,
    -1,
    10**9,
    9.0,
    1,
    MAX_N,
    MAX_N + 1,
    -MAX_N,
    10**100,
    -(10**100),
    9.5,
    float("nan"),
    float("inf"),
    float("-inf"),
    None,
    "",
    "09",
    " 9",
    "9 ",
    "9\n",
    b"9",
    bytearray(b"9"),
    [9],
    (9,),
    {"n": 9},
    {9},
    _EvilInt(5),
    object(),
]


def is_claim_number(value: object) -> bool:
    """The FR-012 rule, written independently of the source."""
    return type(value) is int and 1 <= value <= MAX_N


def is_claim_prompt(value: object) -> bool:
    return isinstance(value, str) and _PROMPT_RE.fullmatch(value) is not None


def _draw(rng: random.Random) -> object:
    """One value from the families of design line 693."""
    kind = rng.randrange(9)
    if kind == 0:
        return rng.randint(1, MAX_N)
    if kind == 1:
        return rng.choice([1, 9, 10, 99, 100, 99_999_999, MAX_N])
    if kind == 2:
        base = rng.choice([0, -1, MAX_N + 1, 10**9, 2**31, 2**63, -(2**63), MAX_N])
        return base + rng.randint(-2, 2)
    if kind == 3:
        return rng.randint(-(10**12), 10**12)
    if kind == 4:
        number = str(rng.randint(-5, MAX_N + 5))
        return rng.choice(
            [*HOSTILE, number, " " + number, number + "\n", "0" + number, "+" + number]
        )
    if kind == 5:
        return rng.choice(
            [9.0, float(rng.randint(1, MAX_N)), rng.random() * 1e9, float("nan")]
        )
    if kind == 6:
        return rng.choice([True, False])
    if kind == 7:
        return None
    return rng.choice([[], [9], ["9"], (9,), {"n": 9}, b"9", bytearray(b"9"), {9}])


# ==============================================================================
# The cycle harness: a GhWorld over a real store and a real OrcaLauncher, so the
# launch argv goes through the runner like every other argv.
# ==============================================================================


def _literal_launch(orca: str, worktree: object, n: int) -> tuple[str, ...]:
    """The FR-013 launch argv written out in full (T10), not built by the source."""
    return (
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
        f"/sc:issue --claim {n}",
        "--json",
    )


def classify_argv(argv: object, worktree: object) -> str:
    """Return the NFR-002 form name of ``argv`` or fail with the offending argv.

    The names are ``user``, ``discover``, ``rest``, ``graphql``, ``origin``,
    ``probe`` and ``launch``.
    """
    argv = list(argv)  # type: ignore[call-overload]
    shown = f"offending argv: {argv!r:.600}"
    assert argv and all(isinstance(a, str) for a in argv), shown
    # NFR-003, T5: the upstream repository and the placeholder never appear.
    for needle in (UPSTREAM, "{owner}"):
        assert not any(needle.lower() in a.lower() for a in argv), f"{needle}: {shown}"
    # NG-2: nothing writes.
    assert not any("mutation" in a.lower() for a in argv), f"mutation: {shown}"
    assert not any(a.upper() in ("POST", "PUT", "PATCH", "DELETE") for a in argv), (
        f"write method: {shown}"
    )
    for i, arg in enumerate(argv):
        if arg in ("--method", "-X", "--request"):
            assert argv[i + 1 : i + 2] == ["GET"], f"method is not GET: {shown}"
    # NFR-002: no title, body or comment body field. The one body access is the
    # jq boolean ``contains(<marker>)`` of the G4 projection.
    for arg in argv:
        probe = (
            arg.replace(".body | contains(", "", 1) if arg == github.MARKER_JQ else arg
        )
        assert not _TEXT_FIELD.search(probe), f"title or body field: {shown}"

    if argv == ["gh", "api", "user", "--include"]:
        return "user"
    if argv[:3] == ["gh", "issue", "list"]:
        assert len(argv) == 15, shown
        assert argv[3:8] == ["--repo", FORK, "--state", "open", "--label"], shown
        assert argv[9] == "--assignee", shown
        assert argv[11:] == [
            "--json",
            "number,labels,assignees,state",
            "-L",
            "100",
        ], shown
        return "discover"
    if argv[:2] == ["gh", "api"] and argv[2:4] == ["--method", "GET"]:
        assert _REST_PATH.fullmatch(argv[4]), shown
        assert argv[-2] == "--jq", shown
        if argv[4].endswith("/comments"):
            assert argv[-1] == github.MARKER_JQ, shown
        elif argv[4].endswith("/events"):
            assert argv[-1] == github.EVENTS_JQ, shown
        else:
            assert argv[-1] == github.REREAD_JQ and len(argv) == 7, shown
        return "rest"
    if argv[:4] == ["gh", "api", "graphql", "-f"]:
        assert argv[4] in _QUERIES, shown
        assert argv[5] == "-F" and re.fullmatch(r"number=[1-9][0-9]{0,8}", argv[6]), (
            shown
        )
        assert len(argv) in (7, 9), shown
        if len(argv) == 9:
            assert argv[7] == "-f" and argv[8].startswith("after="), shown
        return "graphql"
    if argv[0] == "git":
        assert len(argv) == 6 and argv[1] == "-C", shown
        assert os.path.isabs(argv[2]), shown
        assert argv[3:] == ["remote", "get-url", "origin"], shown
        return "origin"
    assert os.path.isabs(argv[0]), shown
    if argv[1:] == ["skills", "list", "--json"]:
        return "probe"
    assert len(argv) == 12 and argv[1:3] == ["agent", "launch"], shown
    prompt = argv[10]
    assert is_claim_prompt(prompt), shown
    assert tuple(argv) == _literal_launch(argv[0], worktree, int(prompt.split()[-1])), (
        shown
    )
    return "launch"


@dataclass
class Ran:
    """What one scripted cycle did."""

    result: cycle.CycleResult
    world: GhWorld
    store: record.FileStore
    forms: list[str]
    argvs: list[tuple[str, ...]]
    launches: list[tuple[str, ...]]

    @property
    def lines(self) -> list[dict]:
        path = self.store.state_dir / "audit.jsonl"
        return [json.loads(t) for t in path.read_text(encoding="utf-8").splitlines()]

    @property
    def decisions(self) -> list[tuple[int, str]]:
        return [
            (ln["issue"], ln["reason"]) for ln in self.lines if ln["kind"] == "decision"
        ]

    @property
    def prompts(self) -> list[str]:
        return [argv[argv.index("--prompt") + 1] for argv in self.launches]


def run_world(
    root: Path,
    build: Callable[[GhWorld], None],
    *,
    dry_run: bool = False,
    config_over: dict | None = None,
    **world_kwargs: object,
) -> Ran:
    """Run one cycle in ``root`` over a ``GhWorld`` and classify every argv.

    ``build`` adds the issues. A launch reply is scripted for each issue under
    the literal argv, so a launch argv that differs from FR-013 is an unscripted
    argv (exit 99, a failed run).
    """
    root.mkdir(parents=True, exist_ok=True)
    store = record.init_state(root / "state", FIXED_NOW)
    config = make_config(root, **(config_over or {}))
    world = GhWorld(FakeClock(CYCLE_NOW), config, **world_kwargs)
    build(world)
    reply = load_fixture("orca_launch_success.json")["payload"]
    for n in world.issues:
        if not is_claim_number(n):
            continue
        key = _literal_launch(ORCA_PATH, config.worktree, n)
        world.runner.script[key] = command_result(stdout=json.dumps(reply), argv=key)
    deps = world.deps(root, store, launcher=OrcaLauncher(world.runner))
    res = cycle.run_cycle(deps, dry_run)

    assert not world.runner.unexpected, f"unscripted argv: {world.runner.unexpected}"
    argvs = [argv for argv, _ in world.runner.calls]
    forms = [classify_argv(argv, config.worktree) for argv in argvs]
    # FR-029 (design 8.5): gh, git and probe calls get 5..20 s; a launch is never
    # shortened from 120 s and is the only call that passes a cwd.
    for form, (argv, cwd), seconds in zip(
        forms, world.runner.calls, world.runner.timeouts
    ):
        if form == "launch":
            assert (seconds, cwd) == (120.0, str(config.worktree)), argv
        else:
            assert 5.0 <= seconds <= 20.0 and cwd is None, (argv, seconds, cwd)
    launches = [a for a, f in zip(argvs, forms) if f == "launch"]
    return Ran(res, world, store, forms, argvs, launches)


# -- the five scenarios of the argv scan --------------------------------------


@dataclass(frozen=True)
class Scenario:
    build: Callable[[GhWorld], None]
    dry_run: bool
    exit_code: int
    reason: str
    forms: tuple[str, ...]
    decisions: tuple[tuple[int, str], ...]


def _idle(world: GhWorld) -> None:
    pass


def _eligible(world: GhWorld) -> None:
    world.issue(9)


def _claimed(world: GhWorld) -> None:
    world.issue(9, markers=[marker_comment(1, _T_MARK)])


def _rate_limited(world: GhWorld) -> None:
    world.issue(9)
    world.fail("events", "rate", n=9)


_START = ("user", "origin", "discover")
SCENARIOS = {
    "idle": Scenario(_idle, False, 0, "cycle_complete", _START, ()),
    "eligible": Scenario(
        _eligible,
        False,
        0,
        "cycle_complete",
        (
            *_START,
            "rest",  # comments (the claim marker)
            "rest",  # events (the approval)
            "graphql",  # edits
            "graphql",  # project items
            "probe",
            "rest",  # re-read of the issue
            "rest",  # re-read of the events
            "graphql",  # re-read of the project items
            "origin",
            "launch",
        ),
        ((9, "launched"),),
    ),
    "claimed": Scenario(
        _claimed,
        False,
        0,
        "cycle_complete",
        (*_START, "rest", "rest"),
        ((9, "claimed"),),
    ),
    "rate_limited": Scenario(
        _rate_limited, False, 5, "rate_limit_clamped", (*_START, "rest", "rest"), ()
    ),
    "dry_run": Scenario(
        _eligible,
        True,
        0,
        "cycle_complete",
        (*_START, "rest", "rest", "graphql", "graphql"),
        ((9, "launched"),),
    ),
}
ALL_FORMS = {"user", "discover", "rest", "graphql", "origin", "probe", "launch"}


# ==============================================================================
# NFR-001, AC-7, FR-012: the prompt boundary
# ==============================================================================


def test_prompt_regex_property(tmp_path):
    """AC-7, FR-012, NFR-001: every prompt matches the claim regex over the corpus."""
    rng = random.Random(SEED)
    draws = list(EDGE_VALUES) + [_draw(rng) for _ in range(DRAWS)]
    assert len(draws) == DRAWS + len(EDGE_VALUES)

    worktree = tmp_path / "worktree"
    runner = FakeRunner()
    real_launcher = OrcaLauncher(runner)
    fake_launcher = FakeLauncher()
    valid = Counter()
    kinds = Counter()
    for index, value in enumerate(draws):
        where = f"draw {index}: {value!r:.200} ({type(value).__name__})"
        kinds[type(value).__name__] += 1
        if is_claim_number(value):
            valid["valid"] += 1
            prompt = build_claim_prompt(value)
            assert prompt == f"/sc:issue --claim {value}", where
            assert is_claim_prompt(prompt), where
            argv = launch_argv(ORCA_PATH, worktree, prompt)
            assert len(argv) == 12 and argv[10] == prompt, where
            assert argv[9] == "--prompt", where
        else:
            valid["invalid"] += 1
            with pytest.raises(ValueError):
                build_claim_prompt(value)
        # The launch layer takes only a string that is itself a claim prompt, so a
        # raw drawn value can never become the --prompt argument.
        if not is_claim_prompt(value):
            with pytest.raises(ValueError):
                launch_argv(ORCA_PATH, worktree, value)  # type: ignore[arg-type]
            with pytest.raises(ValueError):
                real_launcher.launch(ORCA_PATH, worktree, value, 120.0)  # type: ignore[arg-type]
            with pytest.raises(ValueError):
                fake_launcher.launch(ORCA_PATH, worktree, value, 120.0)  # type: ignore[arg-type]
            assert runner.calls == [] and fake_launcher.calls == [], where

    # The generator is not degenerate: both outcomes and every family occur.
    assert valid["valid"] >= 400 and valid["invalid"] >= 1200, valid
    assert {"int", "str", "float", "bool", "NoneType", "list", "tuple", "dict"} <= set(
        kinds
    ), kinds

    for attack in PROMPT_ATTACKS:
        with pytest.raises(ValueError):
            launch_argv(ORCA_PATH, worktree, attack)
        with pytest.raises(ValueError):
            real_launcher.launch(ORCA_PATH, worktree, attack, 120.0)
        with pytest.raises(ValueError):
            fake_launcher.launch(ORCA_PATH, worktree, attack, 120.0)
    assert runner.calls == [] and fake_launcher.calls == []

    # Full cycles over the same generator: the numbers GitHub can hand over
    # (the two bounds and drawn valid ones) each give one launch whose --prompt
    # matches the pattern.
    numbers = [1, 9, MAX_N] + [rng.randint(1, MAX_N) for _ in range(9)]
    for k, n in enumerate(numbers):
        ran = run_world(tmp_path / f"cycle-{k}", lambda w, n=n: w.issue(n))
        assert (ran.result.exit_code, ran.result.launched_issue) == (0, n), n
        assert ran.prompts == [f"/sc:issue --claim {n}"], f"cycle {k}: issue {n}"
        assert all(is_claim_prompt(p) for p in ran.prompts), n
        assert ran.store.load().entries[n].launches == 1, n


# ==============================================================================
# NFR-001, T1: hostile GitHub, config and login text never reaches the prompt
# ==============================================================================


@pytest.mark.parametrize("hostile", HOSTILE, ids=[f"h{i}" for i in range(len(HOSTILE))])
def test_hostile_labels_logins_and_commenters_never_reach_the_prompt(tmp_path, hostile):
    """NFR-001, AC-7: hostile GitHub text never reaches the prompt or any argv."""

    def build(world: GhWorld) -> None:
        cfg = world.config
        events = [
            label_event(
                1,
                "labeled",
                cfg.trigger_label,
                T_TRIGGER,
                actor_id=2001,
                actor_login=hostile,
            ),
            label_event(
                2,
                "labeled",
                cfg.approval_label,
                T_APPROVED,
                actor_id=APPROVER_ID,
                actor_login=hostile + "-approver",
            ),
        ]
        world.issue(
            9,
            labels=[cfg.trigger_label, cfg.approval_label, hostile],
            events=events,
            markers=[
                marker_comment(1, _T_MARK, login=hostile, marker=True),
                marker_comment(2, _T_MARK, login=hostile + "2", marker=False),
            ],
        )

    ran = run_world(tmp_path, build)
    assert ran.result.exit_code == 0 and ran.result.reason == "cycle_complete"
    assert ran.result.launched_issue == 9
    assert ran.prompts == ["/sc:issue --claim 9"], f"hostile: {hostile!r:.100}"
    assert ran.forms == list(SCENARIOS["eligible"].forms)
    for argv in ran.argvs:
        assert not any(hostile in arg for arg in argv), (
            f"{hostile!r:.100} in {argv!r:.300}"
        )


@pytest.mark.parametrize("hostile", HOSTILE[:6], ids=[f"h{i}" for i in range(6)])
def test_a_hostile_assignee_blocks_the_launch(tmp_path, hostile):
    ran = run_world(tmp_path, lambda w: w.issue(9, assignees=[OWN_LOGIN, hostile]))
    assert (ran.result.exit_code, ran.result.reason) == (0, "cycle_complete")
    assert ran.decisions == [(9, "assigned_other")], f"hostile: {hostile!r:.100}"
    assert ran.launches == [] and ran.result.launched_issue is None
    assert ran.forms == list(_START)
    assert ran.store.load().entries == {}


@pytest.mark.parametrize(
    ("trigger", "approval"),
    [
        ("$(touch /tmp/pwned) `id`; rm -rf /", "approved' OR '1'='1"),
        ("x --prompt /sc:issue --claim 1", "{owner} ../../etc"),
        ("trigger‮label", "approved --json"),
    ],
)
def test_hostile_config_labels_stay_one_argv_element_and_never_reach_the_prompt(
    tmp_path, trigger, approval
):
    ran = run_world(
        tmp_path,
        lambda w: w.issue(9),
        config_over={"trigger_label": trigger, "approval_label": approval},
    )
    assert (ran.result.exit_code, ran.result.launched_issue) == (0, 9)
    assert ran.prompts == ["/sc:issue --claim 9"]
    holders = [argv for argv in ran.argvs if any(trigger in arg for arg in argv)]
    assert len(holders) == 1 and holders[0][:3] == ("gh", "issue", "list"), holders
    assert holders[0][holders[0].index("--label") + 1] == trigger  # one element
    assert not any(approval in arg for argv in ran.argvs for arg in argv)


@pytest.mark.parametrize(
    "login",
    [*HOSTILE, "owner-login\n", "", "bad_login!", "a" * 40, "-lead", "x y"],
    ids=lambda v: repr(v)[:20],
)
def test_a_hostile_own_login_stops_before_any_argv_uses_it(tmp_path, login):
    ran = run_world(tmp_path, lambda w: w.issue(9), login=login)
    assert (ran.result.exit_code, ran.result.reason) == (3, "login_invalid")
    assert ran.argvs == [("gh", "api", "user", "--include")], f"login: {login!r:.100}"
    assert ran.launches == [] and ran.result.launched_issue is None
    assert ran.store.load().entries == {}
    (line,) = ran.lines
    assert (line["kind"], line["exit"], line["reason"]) == ("cycle", 3, "login_invalid")
    assert line["login"] is None  # a rejected login is never written


@pytest.mark.parametrize(
    "number",
    ["9", "9; rm -rf /", True, False, 0, -1, 10**9, 9.0, 9.5, None, [9], {"n": 9}, ""],
    ids=lambda v: repr(v)[:20],
)
def test_a_discovery_number_that_is_not_a_claim_number_launches_nothing(
    tmp_path, number
):
    ran = run_world(tmp_path, lambda w: w.issue(9, discovered={"number": number}))
    assert (ran.result.exit_code, ran.result.reason) == (3, "gh_non_json")
    assert ran.forms == list(_START), f"number: {number!r}"
    assert ran.launches == [] and ran.result.launched_issue is None
    assert ran.store.load().entries == {}


# ==============================================================================
# NFR-002, NFR-003, AC-20, T5, T9, DF-28: the argv scan
# ==============================================================================


@pytest.mark.parametrize("name", list(SCENARIOS))
def test_every_argv_of_the_cycle_is_an_allowed_form(tmp_path, name):
    """AC-20, NFR-002, NFR-003: every argv of a cycle is one allowed read form."""
    sc = SCENARIOS[name]
    ran = run_world(tmp_path, sc.build, dry_run=sc.dry_run)
    assert (ran.result.exit_code, ran.result.reason) == (sc.exit_code, sc.reason), name
    assert ran.forms == list(sc.forms), name  # the scan saw every call, in order
    assert ran.decisions == list(sc.decisions), name
    cycle_lines = [ln for ln in ran.lines if ln["kind"] == "cycle"]
    assert [(ln["exit"], ln["reason"], ln["dry_run"]) for ln in cycle_lines] == [
        (sc.exit_code, sc.reason, sc.dry_run)
    ]
    assert cycle_lines[0]["gh_calls"] == sum(
        f in ("user", "discover", "rest", "graphql") for f in ran.forms
    )
    launches = ran.forms.count("launch")
    if name == "eligible":
        assert launches == 1 and ran.result.launched_issue == 9
        entry = ran.store.load().entries[9]
        assert (entry.state, entry.launches) == ("launched", 1)
    else:
        assert launches == 0 and ran.result.launched_issue is None
    if name == "dry_run":
        assert ran.result.would_launch == 9 and "probe" not in ran.forms
        assert ran.store.load().entries == {}
    if name == "claimed":
        assert ran.store.load().entries[9].state == "claimed"
    if name == "rate_limited":
        wait = ran.store.load().next_permitted_at
        assert wait == CYCLE_NOW + timedelta(seconds=3600)


def test_the_five_cycles_together_use_every_allowed_form_and_nothing_else(tmp_path):
    """AC-20, NFR-002, NFR-003: GET only on REST and no upstream name in any argv."""
    seen: Counter[str] = Counter()
    every: list[tuple[str, ...]] = []
    for name, sc in SCENARIOS.items():
        ran = run_world(tmp_path / name, sc.build, dry_run=sc.dry_run)
        seen.update(ran.forms)
        every += ran.argvs
    assert set(seen) == ALL_FORMS, seen
    assert seen["launch"] == 1  # only the eligible, non-dry-run cycle launches
    # NG-2 over all of them at once: nothing but GET on REST, no write verb.
    for argv in every:
        assert not any(UPSTREAM.lower() in a.lower() for a in argv), argv
        assert not any("{owner}" in a for a in argv), argv
        if argv[:2] == ("gh", "api") and argv[2] not in ("user", "graphql"):
            assert argv[2:4] == ("--method", "GET"), argv


class _Recorder:
    """A runner that records each argv and fails it (the argv is what matters)."""

    def __init__(self) -> None:
        self.argvs: list[tuple[str, ...]] = []

    def run(self, argv, timeout, *, cwd=None):
        self.argvs.append(tuple(argv))
        return command_result(returncode=1, argv=tuple(argv))


def test_every_argv_builder_of_the_package_gives_an_allowed_form(tmp_path):
    """AC-20, NFR-002, NFR-003: every argv builder of the package is in the scan."""
    worktree = tmp_path / "worktree"
    trigger = cycle.DEFAULT_TRIGGER_LABEL
    expected: list[tuple[list[str], str]] = [
        (github.argv_user(), "user"),
        (github.argv_discover(trigger, OWN_LOGIN), "discover"),
    ]
    for n in (1, 9, 100, MAX_N):
        for page in range(1, github.PAGE_CAP + 1):
            expected.append((github.argv_events(n, page), "rest"))
            expected.append((github.argv_comments(n, page), "rest"))
        expected.append((github.argv_reread(n), "rest"))
        for cursor in (None, "Y3Vyc29yOnYyOpHOAAAB", "a.b:c-d_e=="):
            expected.append((github.argv_edits(n, cursor), "graphql"))
            expected.append((github.argv_project_items(n, cursor), "graphql"))
        expected.append(
            (launch_argv(ORCA_PATH, worktree, build_claim_prompt(n)), "launch")
        )
    recorder = _Recorder()
    assert launch.check_origin(recorder, worktree, 5.0) == "origin_mismatch"
    assert launch.find_orca(recorder, which=default_which, timeout=5.0) is None
    expected += [
        (list(argv), form) for argv, form in zip(recorder.argvs, ("origin", "probe"))
    ]
    assert len(recorder.argvs) == 2
    for argv, form in expected:
        assert classify_argv(argv, worktree) == form, argv


BAD_ARGVS = {
    "post_to_rest": [
        "gh",
        "api",
        "--method",
        "POST",
        "repos/IronbellyOrg/IronClaude/issues/9/comments",
    ],
    "rest_without_method": [
        "gh",
        "api",
        "repos/IronbellyOrg/IronClaude/issues/9/events",
        "-F",
        "per_page=100",
        "-F",
        "page=1",
        "--jq",
        github.EVENTS_JQ,
    ],
    "rest_method_delete_after_get": [
        "gh",
        "api",
        "--method",
        "GET",
        "repos/IronbellyOrg/IronClaude/issues/9",
        "--method",
        "DELETE",
        "--jq",
        github.REREAD_JQ,
    ],
    "upstream_repository": [
        "gh",
        "api",
        "--method",
        "GET",
        f"repos/{UPSTREAM}/SuperClaude_Framework/issues/9",
        "--jq",
        github.REREAD_JQ,
    ],
    "owner_placeholder": [
        "gh",
        "api",
        "--method",
        "GET",
        "repos/{owner}/{repo}/issues/9",
        "--jq",
        github.REREAD_JQ,
    ],
    "body_field_in_jq": [
        "gh",
        "api",
        "--method",
        "GET",
        "repos/IronbellyOrg/IronClaude/issues/9/events",
        "-F",
        "per_page=100",
        "-F",
        "page=1",
        "--jq",
        "[.[] | {id, body}]",
    ],
    "title_field_in_list": [
        "gh",
        "issue",
        "list",
        "--repo",
        FORK,
        "--state",
        "open",
        "--label",
        "t",
        "--assignee",
        "me",
        "--json",
        "number,title",
        "-L",
        "100",
    ],
    "list_of_the_upstream": [
        "gh",
        "issue",
        "list",
        "--repo",
        f"{UPSTREAM}/SuperClaude_Framework",
        "--state",
        "open",
        "--label",
        "t",
        "--assignee",
        "me",
        "--json",
        "number,labels,assignees,state",
        "-L",
        "100",
    ],
    "graphql_mutation": [
        "gh",
        "api",
        "graphql",
        "-f",
        "query=mutation { addComment }",
        "-F",
        "number=9",
    ],
    "graphql_other_query": [
        "gh",
        "api",
        "graphql",
        "-f",
        "query={ viewer { login } }",
        "-F",
        "number=9",
    ],
    "issue_comment": ["gh", "issue", "comment", "9", "--body", "x"],
    "shell": ["bash", "-c", "gh api user"],
    "git_push": ["git", "push", "origin", "master"],
    "git_relative_directory": ["git", "-C", "rel", "remote", "get-url", "origin"],
    "launch_with_a_permission_flag": [
        *_literal_launch(ORCA_PATH, "/wt", 9)[:-1],
        "--dangerously-skip-permissions",
        "--json",
    ],
    "launch_with_a_free_prompt": [
        *_literal_launch(ORCA_PATH, "/wt", 9)[:10],
        "do something else",
        "--json",
    ],
    "launch_with_another_agent": [
        *_literal_launch(ORCA_PATH, "/wt", 9)[:4],
        "codex",
        *_literal_launch(ORCA_PATH, "/wt", 9)[5:],
    ],
    "launch_with_a_relative_orca": list(_literal_launch("orca", "/wt", 9)),
}


@pytest.mark.parametrize("name", list(BAD_ARGVS))
def test_the_argv_scan_rejects_a_forbidden_argv(name):
    """AC-20, NFR-002, NFR-003: the scan rejects a write, a body field, an upstream."""
    with pytest.raises(AssertionError):
        classify_argv(BAD_ARGVS[name], "/wt")


def test_the_scan_accepts_the_reference_launch_argv():
    assert classify_argv(_literal_launch(ORCA_PATH, "/wt", 9), "/wt") == "launch"


# ==============================================================================
# NG-2, NFR-003: the module constants of github.py
# ==============================================================================


def test_no_string_constant_of_github_py_contains_mutation():
    constants = {
        name: value
        for name, value in vars(github).items()
        if isinstance(value, str) and not name.startswith("__")
    }
    # The scan is not vacuous: it sees the constants it exists to guard.
    assert {"REPO", "EVENTS_JQ", "MARKER_JQ", "REREAD_JQ", "EDITS_QUERY"} <= set(
        constants
    )
    assert "PROJECT_ITEMS_QUERY" in constants
    for name, value in constants.items():
        assert "mutation" not in value.lower(), f"github.{name} contains mutation"
        assert UPSTREAM.lower() not in value.lower(), f"github.{name} names upstream"
        assert "{owner}" not in value, f"github.{name} holds the {{owner}} placeholder"


@pytest.mark.parametrize("name", ["EDITS_QUERY", "PROJECT_ITEMS_QUERY"])
def test_both_graphql_constants_name_the_literal_repository_and_only_read(name):
    query = getattr(github, name)
    assert github.REPO == FORK
    assert 'repository(owner: "IronbellyOrg", name: "IronClaude")' in query, name
    assert query.startswith("query("), name  # an operation that reads
    assert "mutation" not in query.lower() and "subscription" not in query.lower()
    assert "$owner" not in query and "$name" not in query and "{owner}" not in query
    assert "$after: String)" in query and "String!" not in query  # DF-14
    assert not _TEXT_FIELD.search(query), f"{name} asks for a title or body"


# ==============================================================================
# T10: the launch argv is the 12-element list of FR-013
# ==============================================================================


@pytest.mark.parametrize(
    ("orca", "worktree"),
    [
        (ORCA_PATH, "/tmp/x"),
        ("/usr/local/bin/orca", "/home/coder/workspaces/my wt"),
        ("/o", "/w; rm -rf /"),
    ],
)
def test_launch_argv_is_the_twelve_element_list_with_no_extra_flag(orca, worktree):
    argv = launch_argv(orca, worktree, "/sc:issue --claim 9")
    assert argv == [
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
    assert len(argv) == 12
    flags = [a for a in argv[1:] if a.startswith("--")]
    assert flags == ["--agent", "--worktree", "--surface", "--prompt", "--json"]
    assert not any("permission" in a or "dangerous" in a or "skip" in a for a in argv)
    assert launch.ORCA_AGENT == "claude"


def test_the_launch_the_cycle_makes_is_the_literal_argv_in_the_worktree(tmp_path):
    ran = run_world(tmp_path, lambda w: w.issue(9))
    worktree = ran.world.config.worktree
    assert ran.launches == [
        (
            ORCA_PATH,
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
        )
    ]
    assert len(ran.launches[0]) == 12
    assert [cwd for argv, cwd in ran.world.runner.calls if "launch" in argv] == [
        str(worktree)
    ]
    # Only the launch carries the prompt flag; no gh or git argv has one.
    assert [a for a in ran.argvs if "--prompt" in a] == ran.launches
