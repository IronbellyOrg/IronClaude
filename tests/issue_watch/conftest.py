"""Shared fakes for the issue-watch tests: scripted runner, clock, waker and GitHub world."""

from __future__ import annotations

import json
import shutil
import sys
from collections.abc import Callable
from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import audit, cycle, github, launch, record, wake
from superclaude.cli.issue_watch.predicates import file_key, format_utc
from superclaude.cli.issue_watch.record import FileStore, Store, StoreDoc
from superclaude.cli.issue_watch.runner import CommandResult

Script = dict[
    tuple[str, ...], "CommandResult | Callable[[list[str], str | None], CommandResult]"
]


def result(
    stdout: str = "",
    stderr: str = "",
    returncode: int | None = 0,
    *,
    timed_out: bool = False,
    spawn_error: str | None = None,
    argv: tuple[str, ...] = (),
) -> CommandResult:
    """Build a ``CommandResult``; a timeout or spawn error has no return code."""
    if timed_out or spawn_error is not None:
        returncode = None
    return CommandResult(
        argv=tuple(argv),
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
        timed_out=timed_out,
        spawn_error=spawn_error,
        duration_s=0.0,
    )


class FakeClock:
    """A clock that only moves when ``advance`` is called (no sleeping)."""

    def __init__(self, now: datetime, mono: float = 0.0) -> None:
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        self._now = now
        self._mono = float(mono)

    def now(self) -> datetime:
        """Return the current UTC time."""
        return self._now

    def monotonic(self) -> float:
        """Return the monotonic reading in seconds."""
        return self._mono

    def advance(self, seconds: float) -> None:
        """Move both readings forward by ``seconds``."""
        self._now = self._now + timedelta(seconds=seconds)
        self._mono += float(seconds)


class FakeRunner:
    """A ``Runner`` that answers from a script and records every call.

    The script maps a full argv tuple to a ``CommandResult`` or to a callable
    ``(argv, cwd) -> CommandResult``. ``matchers`` holds ``(predicate, reply)``
    pairs tried after the exact script, for calls whose argv varies (a search
    time). An argv in neither gets return code 99 and is added to ``unexpected``.
    ``timeouts`` holds the ``timeout`` of every call, in call order.
    """

    def __init__(self, script: Script | None = None) -> None:
        self.script: Script = dict(script or {})
        self.matchers: list[tuple[Callable[[tuple[str, ...]], bool], object]] = []
        self.calls: list[tuple[tuple[str, ...], str | None]] = []
        self.timeouts: list[float] = []
        self.unexpected: list[tuple[str, ...]] = []

    def run(
        self, argv: list[str], timeout: float, *, cwd: str | None = None
    ) -> CommandResult:
        """Record the call and its timeout, and return the scripted reply."""
        key = tuple(argv)
        self.calls.append((key, cwd))
        self.timeouts.append(timeout)
        assert timeout is not None, f"a None timeout reached the runner: {argv!r}"
        reply = self.script.get(key)
        if reply is None:
            reply = next((r for pred, r in self.matchers if pred(key)), None)
        if reply is None:
            self.unexpected.append(key)
            return result(stderr="fake: unscripted argv", returncode=99, argv=key)
        if callable(reply):
            return reply(list(argv), cwd)  # type: ignore[operator]
        return reply  # type: ignore[return-value]

    def argvs(self, program: str | None = None) -> list[tuple[str, ...]]:
        """Every argv seen, in call order; only those of ``program`` when given."""
        return [a for a, _ in self.calls if program is None or a[0] == program]


@pytest.fixture
def fake_runner():
    """Factory for ``FakeRunner``; fails the test if any runner saw an unscripted argv."""
    made: list[FakeRunner] = []

    def make(script: Script | None = None) -> FakeRunner:
        runner = FakeRunner(script)
        made.append(runner)
        return runner

    yield make
    for runner in made:
        assert not runner.unexpected, f"unscripted argv: {runner.unexpected}"


FIXED_NOW = datetime(2026, 11, 7, 12, 0, 0, tzinfo=timezone.utc)
CYCLE_NOW = FIXED_NOW + timedelta(hours=1)

CRASH_POINTS = (None, "C1", "C3", "C4", "C5")


class CrashingStore:
    """A ``Store`` that delegates to ``real`` and raises ``SystemExit`` at a crash point.

    ``save`` counts its calls. In a cycle that wakes someone, save 1 is the
    ``pending`` save before anything is sent and save 2 is the final commit.

    - ``C1`` raises before delegating save 1.
    - ``C3`` delegates save 1, then raises in the same call (a kill between the
      ``pending`` write and the wake file).
    - ``C4`` raises at save 2 before delegating.
    - ``C5`` delegates save 2, then raises in the same call.

    ``crash_at=None`` is a pure passthrough. C2 (during ``write_prepared_bytes``)
    is injected by ``test_crash_injection.py`` by patching ``os.replace``.
    """

    def __init__(self, real: Store, crash_at: str | None = None) -> None:
        if crash_at not in CRASH_POINTS:
            raise ValueError(f"unknown crash point: {crash_at!r}")
        self.real = real
        self.crash_at = crash_at
        self.saves = 0

    @property
    def state_dir(self) -> Path:
        """The wrapped store's state directory."""
        return self.real.state_dir

    @property
    def migrated(self) -> bool:
        """True when the wrapped store's last load migrated a lower version."""
        return self.real.migrated

    def load(self) -> StoreDoc:
        """Delegate to the wrapped store."""
        return self.real.load()

    def save(self, doc: StoreDoc) -> None:
        """Count the call, delegate, and raise ``SystemExit`` at the crash point."""
        self.saves += 1
        if (self.crash_at, self.saves) in (("C1", 1), ("C4", 2)):
            raise SystemExit(f"crash {self.crash_at}")
        self.real.save(doc)
        if (self.crash_at, self.saves) in (("C3", 1), ("C5", 2)):
            raise SystemExit(f"crash {self.crash_at}")

    def lock(self) -> AbstractContextManager[None]:
        """Delegate to the wrapped store."""
        return self.real.lock()

    def disabled(self) -> bool:
        """Delegate to the wrapped store."""
        return self.real.disabled()

    def disabled_since(self) -> datetime | None:
        """Delegate to the wrapped store."""
        return self.real.disabled_since()


class FailingStore:
    """A ``Store`` that delegates to ``real`` and raises ``error`` on chosen saves."""

    def __init__(
        self,
        real: Store,
        fail_saves: tuple[int, ...] = (),
        error: BaseException | None = None,
    ) -> None:
        self.real = real
        self.fail_saves = fail_saves
        self.error = OSError("fake: disk full") if error is None else error
        self.saves = 0

    @property
    def state_dir(self) -> Path:
        """The wrapped store's state directory."""
        return self.real.state_dir

    @property
    def migrated(self) -> bool:
        """True when the wrapped store's last load migrated a lower version."""
        return self.real.migrated

    def load(self) -> StoreDoc:
        """Delegate to the wrapped store."""
        return self.real.load()

    def save(self, doc: StoreDoc) -> None:
        """Count the call; raise ``error`` on a listed call, else delegate."""
        self.saves += 1
        if self.saves in self.fail_saves:
            raise self.error
        self.real.save(doc)

    def lock(self) -> AbstractContextManager[None]:
        """Delegate to the wrapped store."""
        return self.real.lock()

    def disabled(self) -> bool:
        """Delegate to the wrapped store."""
        return self.real.disabled()

    def disabled_since(self) -> datetime | None:
        """Delegate to the wrapped store."""
        return self.real.disabled_since()


@pytest.fixture
def tmp_state(tmp_path, monkeypatch) -> FileStore:
    """An initialised ``FileStore`` (no baseline pending); HOME and XDG stay in ``tmp_path``."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    return record.init_state(tmp_path / "state", FIXED_NOW, baseline=False)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "_assumed_shape"
OWN_LOGIN = "owner-login"
OWN_ID = 1001
REPO_A = "IronbellyOrg/IronClaude"
REPO_B = "IronbellyGroup/example"
ORCA_PATH = "/opt/orca/bin/" + launch._ORCA_CLIS[0]
TIERS_TEXT = (FIXTURE_DIR / "ccsession_help_tiers.txt").read_text(encoding="utf-8")

GOOD_BODY = "## Priority\nP2\n\n## Fix approach\nChange the poll.\n\n## Test plan\nRun the tests.\n"
EMPTY_BODY = "Something is wrong and nobody has planned it yet.\n"


def load_fixture(name: str) -> dict:
    """Return one ``_assumed_shape`` fixture; each call parses a fresh copy."""
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def default_which(name: str) -> str | None:
    """Resolve only the first Orca CLI name, to an absolute path (no real PATH)."""
    return ORCA_PATH if name == launch._ORCA_CLIS[0] else None


def stamp(value: datetime | str) -> str:
    """A ``datetime`` as the ``...Z`` text gh gives; a string unchanged."""
    return format_utc(value) if isinstance(value, datetime) else value


# --- the orchestrator repository on disk -------------------------------------------


def write_repos(orch: Path, **over: object) -> Path:
    """Write ``<orch>/repos.yaml`` with two listed repos; ``over`` replaces top-level keys."""
    import yaml

    doc: dict[str, object] = {
        "schema_version": 1,
        "orgs": ["IronbellyOrg", "IronbellyGroup"],
        "grants": ["issue.assign", "issue.hold", "pr.merge"],
        "repos": [
            {
                "repo": REPO_A,
                "enabled": True,
                "checkout": str(orch.parent / "checkouts" / "IronClaude"),
                "max_in_flight": 3,
            },
            {
                "repo": REPO_B,
                "enabled": True,
                "checkout": None,
                "clone_parent": str(orch.parent / "checkouts"),
            },
        ],
    }
    doc.update(over)
    (orch / "repos.yaml").write_text(yaml.safe_dump(doc), encoding="utf-8")
    return orch / "repos.yaml"


def make_config(tmp_path: Path, **overrides: object) -> cycle.Config:
    """A valid enabled ``Config`` whose every path is inside ``tmp_path``.

    The orchestrator repo is ``tmp_path / "orch"`` with a ``repos.yaml`` (two
    repos) and the checkout of the first repo; the state directory is
    ``tmp_path / "state"``, the one ``tmp_state`` initialises.
    """
    orch = tmp_path / "orch"
    values: dict[str, object] = {
        "enabled": True,
        "owner_account_id": None,
        "orchestrator_repo": orch,
        "state_dir": tmp_path / "state",
        "session_tag_prefix": "orchestrator",
    }
    values.update(overrides)
    if values["orchestrator_repo"] == orch:
        orch.mkdir(exist_ok=True)
        (tmp_path / "checkouts" / "IronClaude").mkdir(parents=True, exist_ok=True)
        if not (orch / "repos.yaml").exists():
            write_repos(orch)
    return cycle.Config(**values)  # type: ignore[arg-type]


def orch_dir(config: cycle.Config) -> Path:
    """``<orchestrator repo>/.orchestrator``."""
    path = config.orchestrator_repo / ".orchestrator"
    path.mkdir(exist_ok=True)
    return path


def write_json(path: Path, data: object) -> Path:
    """Write ``data`` as JSON, creating the folder."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def write_registry(config: cycle.Config, entries: dict[str, dict]) -> Path:
    """Write the registry; each value gets a default ``created_at`` and ``status``."""
    full = {}
    for ident, item in entries.items():
        short = ident.rsplit("-", 1)[0]
        full[ident] = {
            "repo": REPO_A,
            "tag": f"orchestrator-{ident}",
            "created_at": "2026-11-07T11:00:00Z",
            "status": "active",
            **item,
        }
        assert short
    return write_json(orch_dir(config) / "orchestrators.json", full)


def write_run(
    config: cycle.Config,
    ident: str,
    status: str = "active",
    run_id: str | None = "run_1",
) -> Path:
    """Write ``runs/<id>.json``."""
    data: dict[str, object] = {"status": status}
    if run_id is not None:
        data["run_id"] = run_id
    return write_json(orch_dir(config) / "runs" / f"{ident}.json", data)


def write_state_file(
    config: cycle.Config,
    repo: str,
    number: int,
    status: str = "in_progress",
    orchestrator: str | None = "ironclaude-1",
) -> Path:
    """Write the per-issue state file of an orchestrator."""
    data: dict[str, object] = {"status": status}
    if orchestrator is not None:
        data["orchestrator"] = orchestrator
    return write_json(
        orch_dir(config) / "issues" / f"{file_key(repo, number)}.json", data
    )


def write_plan_record(
    config: cycle.Config, repo: str, number: int, requested_at: datetime, status: str
) -> Path:
    """Write the plan record of ONE plan request."""
    name = (
        f"plan-{file_key(repo, number)}.{requested_at.strftime('%Y%m%dT%H%M%SZ')}.json"
    )
    return write_json(orch_dir(config) / "issues" / name, {"status": status})


def write_ack(
    config: cycle.Config,
    wake_id: str,
    taken: list[tuple[str, int]] = (),
    skipped: list[tuple[str, int, str]] = (),
    rejected: list[int] = (),
) -> Path:
    """Write ``<wake_id>.ack.json`` as an orchestrator does (3.6)."""
    data = {
        "schema": wake.ACK_SCHEMA,
        "wake_id": wake_id,
        "acked_at": "2026-11-07T13:05:00Z",
        "orchestrator": {"id": "ironclaude-1", "run_id": "run_1", "host": "h"},
        "taken": [{"repo": r, "number": n} for r, n in taken],
        "skipped": [{"repo": r, "number": n, "reason": why} for r, n, why in skipped],
        "rejected_items": [{"index": i, "reason": "malformed_item"} for i in rejected],
        "warnings": [],
    }
    return write_json(orch_dir(config) / "wakes" / f"{wake_id}.ack.json", data)


def wake_files(config: cycle.Config) -> list[Path]:
    """The wake files (not acknowledgments) of the orchestrator repo, oldest id first."""
    folder = config.orchestrator_repo / ".orchestrator" / "wakes"
    if not folder.exists():
        return []
    return sorted(p for p in folder.glob("*.json") if not p.name.endswith(".ack.json"))


def read_wake(path: Path) -> dict:
    """Parse one wake file."""
    return json.loads(path.read_text(encoding="utf-8"))


# --- the fake waker ------------------------------------------------------------------


class FakeWaker:
    """A ``Waker`` that answers from ``outcome`` and records every call.

    ``outcome`` is a ``WakeOutcome``, a list consumed in call order, or a callable
    ``(target, wake_id, call_number) -> WakeOutcome``. ``dead`` holds the tags that
    have no live session (``find_session`` gives ``[]``); ``blind`` makes
    ``find_session`` unreadable (None). ``on_deliver`` runs before the reply: a test
    uses it to look at the wake file at the moment of delivery or to kill the cycle.
    """

    def __init__(
        self,
        outcome: wake.WakeOutcome | list | Callable | None = None,
        *,
        dead: set[str] | None = None,
        blind: bool = False,
        on_deliver: Callable[[wake.WakeTargetRun, str], None] | None = None,
    ) -> None:
        self.outcome = outcome or wake.WakeOutcome("woken", "typed", "sent", typed=True)
        self.dead = dead or set()
        self.blind = blind
        self.on_deliver = on_deliver
        self.deliveries: list[tuple[wake.WakeTargetRun, str, bool]] = []
        self.unread: list[str] = []
        self.lookups: list[str] = []

    def find_session(self, orca: str, workspace: Path, tag: str, timeout: float):
        """``[]`` for a dead tag, None when blind, else one fake live terminal."""
        self.lookups.append(tag)
        if self.blind:
            return None
        return [] if tag in self.dead else [{"handle": "term_live-0001"}]

    def deliver(
        self,
        orca: str,
        target: wake.WakeTargetRun,
        wake_id: str,
        now: datetime,
        timeout: float,
        *,
        start_session: bool = True,
    ) -> wake.WakeOutcome:
        """Record the call, run ``on_deliver``, then return the next outcome."""
        self.deliveries.append((target, wake_id, start_session))
        if self.on_deliver is not None:
            self.on_deliver(target, wake_id)
        if callable(self.outcome):
            return self.outcome(target, wake_id, len(self.deliveries))
        if isinstance(self.outcome, list):
            return self.outcome.pop(0)
        return self.outcome

    def mark_unread(
        self, orca: str, workspace: Path, reason: str, timeout: float
    ) -> bool:
        """Record the reason of an unread mark."""
        self.unread.append(reason)
        return True


def make_deps(
    tmp_path: Path,
    tmp_state: FileStore,
    *,
    runner: FakeRunner | None = None,
    waker: FakeWaker | None = None,
    clock: FakeClock | None = None,
    config: cycle.Config | None = None,
    host: str = "test-host",
    which: Callable[[str], str | None] | None = None,
    store: Store | None = None,
) -> cycle.Deps:
    """Build a ``cycle.Deps`` over the fakes and a real ``AuditLog``.

    Wake ids are ``<time>-0000000N`` with N counting up, so a test can name them.
    """
    counter = iter(range(1, 1000))
    return cycle.Deps(
        runner=FakeRunner() if runner is None else runner,
        store=tmp_state if store is None else store,
        waker=FakeWaker() if waker is None else waker,  # type: ignore[arg-type]
        clock=FakeClock(CYCLE_NOW) if clock is None else clock,
        audit=audit.AuditLog(tmp_state.state_dir),
        config=make_config(tmp_path) if config is None else config,
        which=default_which if which is None else which,
        host=host,
        wake_token=lambda: f"{next(counter):08x}",
    )


# --- the scripted GitHub, git and Orca world ------------------------------------------


@dataclass
class _Fail:
    how: object
    times: int | None
    after: int
    used: int = 0


@dataclass
class Issue:
    """One issue of the scripted world."""

    repo: str
    number: int
    labels: list[str] = field(default_factory=list)
    assignees: list[str] = field(default_factory=lambda: [OWN_LOGIN])
    state: str = "open"
    title: str = "A title"
    body: str = GOOD_BODY
    updated_at: datetime = datetime(2026, 11, 7, 11, 0, 0, tzinfo=timezone.utc)
    pull_request: bool = False
    branches: list[tuple[str, datetime]] = field(default_factory=list)
    timeline: list[dict] = field(default_factory=list)
    session: bool = False  # an Orca worktree for the issue exists


_PLAIN_FAILURES = frozenset(
    {"timeout", "spawn_error", "non_json", "failed", "foreign_origin"}
)
_STDERR_FAILURES = {
    "auth": "gh_stderr_auth_401.json",
    "rate": "gh_stderr_rate_429.json",
    "rate_403": "gh_stderr_rate_403.json",
    "transient": "gh_stderr_http_502.json",
    "not_found": "gh_stderr_http_404.json",
}


class GhWorld:
    """A scripted GitHub, git, ccsession and Orca world behind one ``FakeRunner``.

    ``issue(repo, n, **spec)`` adds an issue; the reads of the poll (the searches,
    the re-read, the hold's label calls and its evidence reads) answer from the
    current state when the call is made, so a test can change the world between
    cycles. The label writes of the hold change the world (``labels``,
    ``updated_at``). ``fail(call, how)`` makes a call fail and ``on(call, fn)`` runs
    ``fn`` when it is made. ``call`` is ``user``, ``tiers``, ``search``, ``info``,
    ``reread``, ``label_get``, ``label_create``, ``label_add``, ``label_remove``,
    ``updated``, ``labels``, ``develop``, ``branch``, ``timeline``, ``origin``,
    ``probe``, ``worktree`` or ``reference``; the per-issue ones take ``(repo, n)``.
    """

    def __init__(
        self,
        clock: FakeClock,
        config: cycle.Config,
        *,
        login: str = OWN_LOGIN,
        account_id: int = OWN_ID,
        runner: FakeRunner | None = None,
        tiers_text: str | None = None,
    ) -> None:
        self.clock = clock
        self.config = config
        self.login = login
        self.account_id = account_id
        self.runner = FakeRunner() if runner is None else runner
        self.tiers_text = TIERS_TEXT if tiers_text is None else tiers_text
        self.issues: dict[tuple[str, int], Issue] = {}
        self.info: dict[str, list[dict]] = {
            "mentions": [],
            "could_assign": [],
            "affects": [],
        }
        self.origins: dict[str, str] = {}
        self.existing_labels: set[str] = set()
        self.skew_s = 0.0
        self._fails: dict[tuple[str, object], list[_Fail]] = {}
        self._hooks: dict[tuple[str, object], list[Callable[[], None]]] = {}
        self._seen: dict[tuple[str, object], int] = {}
        self._register()

    # -- the scenario API ------------------------------------------------------------

    def issue(self, repo: str, number: int, **spec: object) -> Issue:
        """Add (or replace) an issue; the default is open, assigned to the user and planned."""
        item = Issue(repo, number, **spec)  # type: ignore[arg-type]
        self.issues[(repo, number)] = item
        self._register_issue(item)
        return item

    def fail(
        self,
        call: str,
        how: object = "timeout",
        key: object = None,
        *,
        times: int | None = 1,
        after: int = 0,
    ) -> GhWorld:
        """Make ``call`` fail ``times`` times (None: always) after ``after`` calls."""
        if isinstance(how, str) and how not in _PLAIN_FAILURES | set(_STDERR_FAILURES):
            raise ValueError(f"unknown failure {how!r}")
        self._fails.setdefault((call, key), []).append(_Fail(how, times, after))
        return self

    def on(self, call: str, fn: Callable[[], None], key: object = None) -> GhWorld:
        """Run ``fn`` each time ``call`` is made, before the reply is chosen."""
        self._hooks.setdefault((call, key), []).append(fn)
        return self

    def count(self, call: str, key: object = None) -> int:
        """How many times ``call`` was made."""
        return self._seen.get((call, key), 0)

    @property
    def gh_argvs(self) -> list[tuple[str, ...]]:
        """Every ``gh`` argv the runner has seen, in call order."""
        return self.runner.argvs("gh")

    def deps(
        self, tmp_path: Path, tmp_state: FileStore, **kwargs: object
    ) -> cycle.Deps:
        """``make_deps`` over this world's runner, clock and config."""
        return make_deps(
            tmp_path,
            tmp_state,
            runner=self.runner,
            clock=self.clock,
            config=self.config,
            **kwargs,  # type: ignore[arg-type]
        )

    # -- registration ------------------------------------------------------------------

    def _served(
        self, call: str, key: object, build: Callable[[tuple[str, ...]], CommandResult]
    ):
        keys = [(call, key)] if key is None else [(call, key), (call, None)]

        def serve(argv: list[str], cwd: str | None) -> CommandResult:
            argv_t = tuple(argv)
            for k in keys:
                self._seen[k] = self._seen.get(k, 0) + 1
            for k in keys:
                for hook in list(self._hooks.get(k, ())):
                    hook()
            for k in keys:
                for fail in self._fails.get(k, ()):
                    if self._seen[k] > fail.after and (
                        fail.times is None or fail.used < fail.times
                    ):
                        fail.used += 1
                        return self._failure(fail.how, call, argv_t)
            return build(argv_t)

        return serve

    @staticmethod
    def _ok(argv: tuple[str, ...], payload: object) -> CommandResult:
        return result(stdout=json.dumps(payload), argv=argv)

    def _register(self) -> None:
        script = self.runner.script
        script[tuple(github.argv_user())] = self._served("user", None, self._user_reply)
        script[("ccsession", "--help")] = self._served(
            "tiers", None, lambda argv: result(stdout=self.tiers_text, argv=argv)
        )
        probe = FakeRunner()
        launch.find_orca(probe, which=default_which, timeout=1.0)
        for argv in probe.argvs():
            script[argv] = self._served(
                "probe", None, lambda a: self._ok(a, {"topics": [{"name": "orca-cli"}]})
            )
        for org in ("IronbellyOrg", "IronbellyGroup"):
            try:
                script[tuple(github.argv_search_assigned(org, self.login))] = (
                    self._served(
                        "search", org, lambda a, o=org: self._search_reply(a, o)
                    )
                )
            except ValueError:
                pass
        self.runner.matchers.append(
            (
                lambda a: (
                    a[:5] == ("gh", "api", "--method", "GET", "search/issues")
                    and (
                        "mentions:" in a[6]
                        or "no:assignee" in a[6]
                        or "involves:" in a[6]
                    )
                ),
                self._info_reply,
            )
        )
        self.runner.matchers.append(
            (
                lambda a: a[:1] == ("orca",) and a[1:3] == ("worktree", "show"),
                self._worktree_reply,
            )
        )
        self.runner.matchers.append(
            (
                lambda a: a[:1] == ("orca",) and a[1:3] == ("reference", "find"),
                self._reference_reply,
            )
        )

    def _register_issue(self, item: Issue) -> None:
        script, key = self.runner.script, (item.repo, item.number)
        repo, n = item.repo, item.number
        script[tuple(github.argv_reread(repo, n))] = self._served(
            "reread", key, lambda a: self._reread_reply(a, item)
        )
        script[tuple(github.argv_issue_updated(repo, n))] = self._served(
            "updated", key, lambda a: self._ok(a, {"updatedAt": stamp(item.updated_at)})
        )
        script[tuple(github.argv_issue_labels(repo, n))] = self._served(
            "labels",
            key,
            lambda a: self._ok(a, {"labels": [{"name": x} for x in item.labels]}),
        )
        script[tuple(github.argv_label_add(repo, n))] = self._served(
            "label_add", key, lambda a: self._label_add(a, item)
        )
        script[tuple(github.argv_label_remove(repo, n))] = self._served(
            "label_remove", key, lambda a: self._label_remove(a, item)
        )
        script[tuple(github.argv_develop_list(repo, n))] = self._served(
            "develop",
            key,
            lambda a: result(
                stdout="".join(f"{b}\thttps://x/{b}\n" for b, _ in item.branches),
                argv=a,
            ),
        )
        script[tuple(github.argv_timeline(repo, n))] = self._served(
            "timeline", key, lambda a: self._ok(a, item.timeline)
        )
        for name, when in item.branches:
            script[tuple(github.argv_branch_date(repo, name))] = self._served(
                "branch", key, lambda a, w=when: self._ok(a, {"date": stamp(w)})
            )
        script[tuple(github.argv_label_get(repo))] = self._served(
            "label_get", repo, self._label_get
        )
        script[tuple(github.argv_label_create(repo))] = self._served(
            "label_create", repo, self._label_create
        )
        checkout = self._checkout_of(repo)
        if checkout is not None:
            argv = ("git", "-C", str(checkout), "remote", "get-url", "origin")
            script[argv] = self._served(
                "origin",
                repo,
                lambda a, r=repo: result(
                    stdout=self.origins.get(r, f"https://github.com/{r}.git") + "\n",
                    argv=a,
                ),
            )

    def _checkout_of(self, repo: str) -> str | None:
        """The ``checkout`` of ``repo`` in ``repos.yaml``, read without validation."""
        import yaml

        try:
            raw = yaml.safe_load(
                (self.config.orchestrator_repo / "repos.yaml").read_text()
            )
            return next(r.get("checkout") for r in raw["repos"] if r["repo"] == repo)
        except (OSError, KeyError, StopIteration, TypeError, yaml.YAMLError):
            return None

    # -- replies --------------------------------------------------------------------------

    def _with_headers(self, raw: str) -> tuple[str, str]:
        head, _, body = raw.partition("\n\n")
        now = self.clock.now() + timedelta(seconds=self.skew_s)
        lines = []
        for text_line in head.split("\n"):
            name = text_line.split(":", 1)[0].lower()
            lines.append(
                f"Date: {format_datetime(now, usegmt=True)}"
                if name == "date"
                else text_line
            )
        return "\n".join(lines), body

    def _user_reply(self, argv: tuple[str, ...]) -> CommandResult:
        head, body = self._with_headers(load_fixture("gh_api_user_include.json")["raw"])
        who = {**json.loads(body), "login": self.login, "id": self.account_id}
        return result(stdout=f"{head}\n\n{json.dumps(who)}\n", argv=argv)

    def _user_rate_reply(
        self, argv: tuple[str, ...], retry_after: str | None = "120"
    ) -> CommandResult:
        fixture = load_fixture("gh_api_user_include_429.json")
        head, body = self._with_headers(fixture["raw"])
        lines = [x for x in head.split("\n") if not x.lower().startswith("retry-after")]
        if retry_after is not None:
            lines.append(f"Retry-After: {retry_after}")
        return result(
            stdout="\n".join(lines) + "\n\n" + body,
            stderr=fixture["stderr"],
            returncode=fixture["exit"],
            argv=argv,
        )

    def _search_reply(self, argv: tuple[str, ...], org: str) -> CommandResult:
        items = []
        for (repo, _), item in sorted(self.issues.items()):
            if (
                repo.split("/")[0] != org
                or item.state != "open"
                or self.login not in item.assignees
            ):
                continue
            items.append(
                {
                    "repository_url": f"https://api.github.com/repos/{repo}",
                    "number": item.number,
                    "state": item.state,
                    "updated_at": stamp(item.updated_at),
                    "labels": list(item.labels),
                    "assignees": list(item.assignees),
                    "pull_request": item.pull_request,
                    "title": item.title,
                    "body": item.body,
                }
            )
        return self._ok(
            argv,
            {"total_count": len(items), "incomplete_results": False, "items": items},
        )

    def _info_reply(self, argv: tuple[str, ...]) -> CommandResult:
        query = argv[6]
        stream = (
            "mentions"
            if query.startswith("q=mentions:")
            else "could_assign"
            if "no:assignee" in query
            else "affects"
        )
        org = query.rsplit("org:", 1)[1].split()[0]
        calls = [("info", None), ("info", stream)]
        for k in calls:
            self._seen[k] = self._seen.get(k, 0) + 1
        for k in calls:
            for fail in self._fails.get(k, ()):
                if self._seen[k] > fail.after and (
                    fail.times is None or fail.used < fail.times
                ):
                    fail.used += 1
                    return self._failure(fail.how, "info", argv)
        items = [i for i in self.info[stream] if i["repo"].split("/")[0] == org]
        rows = [
            {
                "repository_url": f"https://api.github.com/repos/{i['repo']}",
                "number": i["number"],
                "updated_at": stamp(i["updated_at"]),
                "pull_request": i.get("pull_request", False),
            }
            for i in items
        ]
        return self._ok(
            argv, {"total_count": len(rows), "incomplete_results": False, "items": rows}
        )

    def _reread_reply(self, argv: tuple[str, ...], item: Issue) -> CommandResult:
        return self._ok(
            argv,
            {
                "number": item.number,
                "state": item.state,
                "labels": list(item.labels),
                "assignees": list(item.assignees),
                "body": item.body,
            },
        )

    def _label_get(self, argv: tuple[str, ...]) -> CommandResult:
        repo = argv[-1].split("/labels/")[0].removeprefix("repos/")
        if repo in self.existing_labels:
            return self._ok(argv, {"name": "hold:plan"})
        return self._failure("not_found", "label_get", argv)

    def _label_create(self, argv: tuple[str, ...]) -> CommandResult:
        repo = argv[4].removeprefix("repos/").removesuffix("/labels")
        self.existing_labels.add(repo)
        return self._ok(argv, {"name": "hold:plan"})

    def _label_add(self, argv: tuple[str, ...], item: Issue) -> CommandResult:
        if "hold:plan" not in item.labels:
            item.labels.append("hold:plan")
        item.updated_at = self.clock.now()
        return self._ok(argv, [{"name": x} for x in item.labels])

    def _label_remove(self, argv: tuple[str, ...], item: Issue) -> CommandResult:
        if "hold:plan" in item.labels:
            item.labels.remove("hold:plan")
        item.updated_at = self.clock.now()
        return self._ok(argv, [{"name": x} for x in item.labels])

    def _issue_of_selector(self, text: str) -> Issue | None:
        number = int(text.removeprefix("issue:")) if text.startswith("issue:") else None
        return next((i for i in self.issues.values() if i.number == number), None)

    def _worktree_reply(self, argv: tuple[str, ...]) -> CommandResult:
        item = self._issue_of_selector(argv[argv.index("--worktree") + 1])
        for k in (("worktree", None),):
            self._seen[k] = self._seen.get(k, 0) + 1
        for fail in self._fails.get(("worktree", None), ()):
            if self._seen[("worktree", None)] > fail.after and (
                fail.times is None or fail.used < fail.times
            ):
                fail.used += 1
                return self._failure(fail.how, "worktree", argv)
        if item is not None and item.session:
            return self._ok(
                argv, load_fixture("orca_worktree_show_found.json")["payload"]
            )
        none = load_fixture("orca_worktree_show_none.json")
        return result(
            stdout=json.dumps(none["payload"]), returncode=none["exit"], argv=argv
        )

    def _reference_reply(self, argv: tuple[str, ...]) -> CommandResult:
        self._seen[("reference", None)] = self._seen.get(("reference", None), 0) + 1
        return self._ok(argv, {"ok": True, "result": {"matches": []}})

    def _failure(self, how: object, call: str, argv: tuple[str, ...]) -> CommandResult:
        if isinstance(how, CommandResult):
            return how
        if callable(how):
            return how(list(argv), None)
        if how == "timeout":
            return result(timed_out=True, argv=argv)
        if how == "spawn_error":
            return result(spawn_error="fake: no such file", argv=argv)
        if how == "non_json":
            return result(stdout="not json", argv=argv)
        if how == "failed":
            return result(returncode=1, argv=argv)
        if how == "foreign_origin":
            return result(
                stdout="https://github.com/example-org/other-repo.git\n", argv=argv
            )
        if how == "rate" and call == "user":
            return self._user_rate_reply(argv)
        if how in _STDERR_FAILURES:
            fixture = load_fixture(_STDERR_FAILURES[str(how)])
            return result(
                stderr=fixture["stderr"], returncode=fixture["exit"], argv=argv
            )
        raise ValueError(f"unknown failure {how!r}")


@pytest.fixture
def gh_world(tmp_path):
    """Factory for ``GhWorld``; fails the test if a runner saw an unscripted argv.

    ``make(clock=None, config=None, **kwargs)``: the clock defaults to
    ``FakeClock(CYCLE_NOW)`` and the config to ``make_config(tmp_path)``.
    """
    made: list[GhWorld] = []

    def make(
        *, clock: FakeClock | None = None, config: cycle.Config | None = None, **kwargs
    ) -> GhWorld:
        world = GhWorld(
            FakeClock(CYCLE_NOW) if clock is None else clock,
            make_config(tmp_path) if config is None else config,
            **kwargs,
        )
        made.append(world)
        return world

    yield make
    for world in made:
        assert not world.runner.unexpected, (
            f"unscripted argv: {world.runner.unexpected}"
        )
        for seconds in world.runner.timeouts:
            assert seconds is not None and 5.0 <= seconds <= 120.0, (
                f"timeout out of range: {world.runner.timeouts}"
            )


STUB_TOOLS = ("gh", "orca", "orca-ide", "git", "ccsession")
STUB_UNSCRIPTED_STDERR = "stub: unscripted argv"

# One template for every stub. Standard library only; the shebang names
# /usr/bin/env by absolute path and finds python3 in linkbin.
_STUB_TEMPLATE = '''#!/usr/bin/env python3
"""PATH stub for __TOOL__, written by tests/issue_watch/conftest.py."""

import json
import os
import sys

TOOL = "__TOOL__"


def main():
    argv = sys.argv[1:]
    rule = None
    scenario = os.environ.get("IW_STUB_SCENARIO")
    if scenario:
        with open(scenario, encoding="utf-8") as handle:
            for candidate in json.load(handle).get(TOOL, []):
                prefix = candidate["argv_prefix"]
                if argv[: len(prefix)] == prefix:
                    rule = candidate
                    break
    log = os.environ.get("IW_STUB_LOG")
    if log:
        record = {"tool": TOOL, "argv": argv, "cwd": os.getcwd(), "matched": rule is not None}
        fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        try:
            os.write(fd, (json.dumps(record) + "\\n").encode("utf-8"))
        finally:
            os.close(fd)
    if rule is None:
        sys.stderr.write("__UNSCRIPTED__\\n")
        sys.stderr.flush()
        sys.exit(99)
    sys.stdout.buffer.write(rule.get("stdout", "").encode("utf-8"))
    sys.stdout.buffer.flush()
    sys.stderr.buffer.write(rule.get("stderr", "").encode("utf-8"))
    sys.stderr.buffer.flush()
    sys.exit(int(rule.get("exit", 0)))


main()
'''


def write_scenario(tmp_path: Path, rules: dict[str, list[dict]]) -> Path:
    """Write ``tmp_path / "scenario.json"`` (the file ``IW_STUB_SCENARIO`` names).

    ``rules`` maps a stub name to its rules, each ``{"argv_prefix": [...], "exit":
    int, "stdout": str, "stderr": str}`` with only ``argv_prefix`` required. The
    first rule whose prefix starts the arguments wins.
    """
    for tool, tool_rules in rules.items():
        if tool not in STUB_TOOLS:
            raise ValueError(f"no stub named {tool!r}")
        for rule in tool_rules:
            prefix = rule.get("argv_prefix")
            if not isinstance(prefix, list) or not all(
                isinstance(a, str) for a in prefix
            ):
                raise ValueError(f"argv_prefix must be a list of str: {rule!r}")
    path = tmp_path / "scenario.json"
    path.write_text(json.dumps(rules), encoding="utf-8")
    return path


def read_calls(log_path: Path | str) -> list[dict]:
    """The stub calls from the JSONL log, in call order; a missing log is empty."""
    path = Path(log_path)
    if not path.exists():
        return []
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x]


@pytest.fixture
def stub_path(tmp_path):
    """The environment for a subprocess that can only reach the stubs.

    Creates ``<tmp_path>/stubbin`` (executable ``gh``, ``orca``, ``orca-ide``,
    ``git`` and ``ccsession``) and ``<tmp_path>/linkbin`` (only ``python3``).
    Returns a dict whose ``PATH`` is exactly those two folders, plus ``HOME``,
    ``XDG_STATE_HOME``, ``IW_STUB_SCENARIO`` and ``IW_STUB_LOG``. At teardown the
    test fails if any stub call matched no scenario rule.
    """
    stubbin = tmp_path / "stubbin"
    linkbin = tmp_path / "linkbin"
    home = tmp_path / "home"
    for directory in (stubbin, linkbin, home):
        directory.mkdir(exist_ok=True)
    for name in STUB_TOOLS:
        stub = stubbin / name
        stub.write_text(
            _STUB_TEMPLATE.replace("__TOOL__", name).replace(
                "__UNSCRIPTED__", STUB_UNSCRIPTED_STDERR
            ),
            encoding="utf-8",
        )
        stub.chmod(0o755)
    (linkbin / "python3").symlink_to(sys.executable)
    log = tmp_path / "stub-calls.jsonl"
    log.touch()
    env = {
        "PATH": f"{stubbin}:{linkbin}",
        "HOME": str(home),
        "XDG_STATE_HOME": str(tmp_path / "xdg"),
        "IW_STUB_SCENARIO": str(write_scenario(tmp_path, {})),
        "IW_STUB_LOG": str(log),
    }
    for name in STUB_TOOLS:
        found = shutil.which(name, path=env["PATH"])
        assert found == str(stubbin / name), (
            f"{name} resolves to {found!r}, not the stub"
        )
    yield env
    unmatched = [(c["tool"], c["argv"]) for c in read_calls(log) if not c["matched"]]
    assert not unmatched, f"stub saw unscripted argv: {unmatched}"
