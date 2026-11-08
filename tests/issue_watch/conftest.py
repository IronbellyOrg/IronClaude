"""Shared fakes for the issue-watch tests: scripted runner and controllable clock."""

from __future__ import annotations

import json
import shutil
import sys
from collections.abc import Callable
from contextlib import AbstractContextManager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import audit, cycle, github, launch, record
from superclaude.cli.issue_watch.launch import LaunchOutcome, launch_argv
from superclaude.cli.issue_watch.predicates import format_utc
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
    ``(argv, cwd) -> CommandResult``. An argv missing from the script gets
    return code 99 and is added to ``unexpected``. ``timeouts`` holds the
    ``timeout`` of every call, in call order, so a test can show which value
    reached the runner.
    """

    def __init__(self, script: Script | None = None) -> None:
        self.script: Script = dict(script or {})
        self.calls: list[tuple[tuple[str, ...], str | None]] = []
        self.timeouts: list[float] = []
        self.unexpected: list[tuple[str, ...]] = []

    def run(
        self, argv: list[str], timeout: float, *, cwd: str | None = None
    ) -> CommandResult:
        """Record the call and its timeout, and return the scripted reply."""
        # The caller must test Deadline.timeout_for for None before it calls a
        # Runner (design 8.5, FR-029); a None here is a missing guard (Gate C C-11).
        key = tuple(argv)
        self.calls.append((key, cwd))
        self.timeouts.append(timeout)
        assert timeout is not None, f"a None timeout reached the runner: {argv!r}"
        reply = self.script.get(key)
        if reply is None:
            self.unexpected.append(key)
            return result(stderr="fake: unscripted argv", returncode=99, argv=key)
        if callable(reply):
            return reply(list(argv), cwd)
        return reply


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

CRASH_POINTS = (None, "C1", "C3", "C4", "C5")


class CrashingStore:
    """A ``Store`` that delegates to ``real`` and raises ``SystemExit`` at a crash point.

    ``save`` counts its calls. Save 1 is the ``pending`` save before a launch and
    save 2 is the outcome save after it (design section 7.6):

    - ``C1`` raises before delegating save 1.
    - ``C3`` delegates save 1, then raises in the same call.
    - ``C4`` raises at save 2 before delegating.
    - ``C5`` delegates save 2, then raises in the same call.

    ``crash_at=None`` is a pure passthrough. C2 (during ``write_prepared_bytes``)
    is not reachable through the Store seam: ``test_crash_injection.py`` injects
    it by patching ``os.replace`` (decision DF-15).
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
    """A ``Store`` that delegates to ``real`` and raises ``error`` on chosen saves.

    ``fail_saves`` holds the 1-based numbers of the ``save`` calls that raise
    ``error`` (an ``OSError`` by default) before anything is written, so the file
    on disk is as the previous save left it. Every other save delegates.
    ``saves`` counts all calls. Unlike ``CrashingStore`` it raises an ordinary
    exception, which ``run_cycle`` can see (Gate C fix C-6, C-7, C-3).
    """

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
    """An initialised ``FileStore`` under ``tmp_path``; HOME and XDG stay inside it."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    return record.init_state(tmp_path / "state", FIXED_NOW)


class FakeLauncher:
    """A ``Launcher`` that answers from ``outcomes`` and records every call.

    ``outcomes`` is a list of ``LaunchOutcome`` consumed in call order, or a
    callable ``(call_number) -> LaunchOutcome`` with ``call_number`` starting at
    1. ``calls`` holds ``(orca, str(worktree), prompt, timeout)`` per call and
    ``argvs`` the 12-element argv ``launch_argv`` builds from the same inputs,
    so a prompt the real launcher would refuse raises ``ValueError`` here too
    and records nothing. ``raises`` (an exception instance or class) is raised
    instead of returning, after the call is recorded, and consumes no outcome.
    ``on_call`` runs after recording and before the raise or the return: a test
    uses it to read ``dispatch.json`` at launch time or to create ``DISABLED``
    mid-cycle. An exhausted list fails the test with ``AssertionError``.
    """

    def __init__(
        self,
        outcomes: list[LaunchOutcome] | Callable[[int], LaunchOutcome] | None = None,
        *,
        raises: BaseException | type[BaseException] | None = None,
        on_call: Callable[[], None] | None = None,
    ) -> None:
        self._outcomes = outcomes if callable(outcomes) else list(outcomes or [])
        self.raises = raises
        self.on_call = on_call
        self.calls: list[tuple[str, str, str, float]] = []
        self.argvs: list[list[str]] = []

    def launch(
        self, orca: str, worktree: Path, prompt: str, timeout: float
    ) -> LaunchOutcome:
        """Record the call, run ``on_call``, then raise or return the next outcome."""
        argv = launch_argv(orca, worktree, prompt)
        self.calls.append((orca, str(worktree), prompt, timeout))
        self.argvs.append(argv)
        if self.on_call is not None:
            self.on_call()
        if self.raises is not None:
            raise self.raises
        if callable(self._outcomes):
            return self._outcomes(len(self.calls))
        if not self._outcomes:
            raise AssertionError("FakeLauncher: no outcome left for this launch")
        return self._outcomes.pop(0)


# ==============================================================================
# Part 4: the deps factory and the scripted GitHub world (plan step 6.4).
#
# Every gh or Orca reply whose shape is unverified is built from an
# ``_assumed_shape`` fixture (decision DF-32), never from inline JSON. Two
# replies have no fixture and are written here: the Orca ``skills list --json``
# probe reply (the shape ``install_user_setup._find_orca`` already reads) and
# ``git remote get-url`` (plain text).
# ==============================================================================

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "_assumed_shape"

OWN_LOGIN = "owner-login"
OWN_ID = 1001
APPROVER_ID = 1001
PROJECT_ID = "PVT_test_project_0001"
ORIGIN_URL = "https://github.com/IronbellyOrg/IronClaude.git"
FOREIGN_ORIGIN_URL = "https://github.com/example-org/other-repo.git"
ORCA_PATH = "/opt/orca/bin/" + launch._ORCA_CLIS[0]

# ``tmp_state`` creates the store at FIXED_NOW, and an approval must come after it.
T_TRIGGER = FIXED_NOW + timedelta(minutes=1)
T_APPROVED = FIXED_NOW + timedelta(minutes=2)
CYCLE_NOW = FIXED_NOW + timedelta(hours=1)


def load_fixture(name: str) -> dict:
    """Return one ``_assumed_shape`` fixture; each call parses a fresh copy."""
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def _stamp(value: object) -> object:
    """A ``datetime`` as the ``...Z`` text gh gives; any other value unchanged."""
    return format_utc(value) if isinstance(value, datetime) else value


def _stamped(item: dict) -> dict:
    return {key: _stamp(value) for key, value in item.items()}


def default_which(name: str) -> str | None:
    """Resolve only the first Orca CLI name, to an absolute path (no real PATH)."""
    return ORCA_PATH if name == launch._ORCA_CLIS[0] else None


def make_config(tmp_path: Path, **overrides: object) -> cycle.Config:
    """A valid enabled ``Config`` whose every path is inside ``tmp_path``.

    The worktree directory and an approvers file (mode 0o600, holding account
    id 1001) are created unless ``overrides`` names another path. The state
    directory is ``tmp_path / "state"``, the one ``tmp_state`` initialises.
    """
    worktree = tmp_path / "worktree"
    approvers = tmp_path / "approvers"
    values: dict[str, object] = {
        "enabled": True,
        "trigger_label": cycle.DEFAULT_TRIGGER_LABEL,
        "approval_label": cycle.DEFAULT_APPROVAL_LABEL,
        "project_id": PROJECT_ID,
        "owner_account_id": None,
        "worktree": worktree,
        "approvers_file": approvers,
        "state_dir": tmp_path / "state",
    }
    values.update(overrides)
    if values["worktree"] == worktree:
        worktree.mkdir(exist_ok=True)
    if values["approvers_file"] == approvers and not approvers.exists():
        approvers.write_text(f"{APPROVER_ID}\n", encoding="utf-8")
        approvers.chmod(0o600)
    return cycle.Config(**values)  # type: ignore[arg-type]


def launched_outcome() -> LaunchOutcome:
    """The outcome ``orca_launch_success.json`` parses to."""
    reply = load_fixture("orca_launch_success.json")["payload"]
    return launch.outcome_of(result(stdout=json.dumps(reply)))


def unknown_outcome() -> LaunchOutcome:
    """The ``unknown`` outcome ``orca_launch_unknown.json`` parses to."""
    fixture = load_fixture("orca_launch_unknown.json")
    return launch.outcome_of(
        result(stderr=fixture["stderr"], returncode=fixture["exit"])
    )


def spawn_error_outcome() -> LaunchOutcome:
    """The ``spawn_error`` outcome of a launch that could not start."""
    return launch.outcome_of(result(spawn_error="fake: no such file"))


def _launched_every_time(call_number: int) -> LaunchOutcome:
    return LaunchOutcome("launched", f"op-test-{call_number:04d}", "ok")


def make_deps(
    tmp_path: Path,
    tmp_state: FileStore,
    *,
    runner: FakeRunner | None = None,
    launcher: FakeLauncher | None = None,
    clock: FakeClock | None = None,
    config: cycle.Config | None = None,
    host: str = "test-host",
    which: Callable[[str], str | None] | None = None,
) -> cycle.Deps:
    """Build a ``cycle.Deps`` over the fakes and a real ``AuditLog``.

    The store is ``tmp_state`` and the audit log is in its directory. Defaults:
    an empty ``FakeRunner`` (every call is unexpected), a ``FakeLauncher`` that
    launches every time with a fresh operation id, ``FakeClock(CYCLE_NOW)``,
    ``make_config(tmp_path)`` and ``default_which``.
    """
    return cycle.Deps(
        runner=FakeRunner() if runner is None else runner,
        store=tmp_state,
        launcher=FakeLauncher(_launched_every_time) if launcher is None else launcher,
        clock=FakeClock(CYCLE_NOW) if clock is None else clock,
        audit=audit.AuditLog(tmp_state.state_dir),
        config=make_config(tmp_path) if config is None else config,
        which=default_which if which is None else which,
        host=host,
    )


def label_event(event_id: int, event: str, label: str | None, at: object, **over):
    """One G3 item shaped like ``rest_events_page.json``; ``over`` replaces fields."""
    item = load_fixture("rest_events_page.json")["payload"][0]
    item.update(id=event_id, event=event, label=label, created_at=at)
    item.update(over)
    return item


def default_events(config: cycle.Config) -> list[dict]:
    """The trigger label added by the author, then the approval by an approver."""
    return [
        label_event(
            1,
            "labeled",
            config.trigger_label,
            T_TRIGGER,
            actor_id=2001,
            actor_login="issue-author",
        ),
        label_event(
            2,
            "labeled",
            config.approval_label,
            T_APPROVED,
            actor_id=APPROVER_ID,
            actor_login=OWN_LOGIN,
        ),
    ]


def marker_comment(
    comment_id: int,
    at: object,
    *,
    login: str | None = OWN_LOGIN,
    marker: bool = True,
    updated_at: object = None,
    **over,
):
    """One G4 item shaped like ``rest_comments_marker.json`` (own claim by default)."""
    item = load_fixture("rest_comments_marker.json")["payload"][0]
    item.update(
        id=comment_id,
        login=login,
        created_at=at,
        updated_at=at if updated_at is None else updated_at,
        marker=marker,
    )
    item.update(over)
    return item


@dataclass
class _Fail:
    how: object
    times: int | None
    after: int
    used: int = 0


class _ArgvRecorder:
    """A ``Runner`` that records each argv and fails it: it learns exact argv."""

    def __init__(self) -> None:
        self.argvs: list[tuple[str, ...]] = []

    def run(
        self, argv: list[str], timeout: float, *, cwd: str | None = None
    ) -> CommandResult:
        key = tuple(argv)
        self.argvs.append(key)
        return result(returncode=1, argv=key)


# stderr-only failures, and failures that are an exit-0 GraphQL error body.
_STDERR_FAILURES = {
    "auth": "gh_stderr_auth_401.json",
    "rate": "gh_stderr_rate_429.json",
    "rate_403": "gh_stderr_rate_403.json",
    "transient": "gh_stderr_http_502.json",
    "scope": "gh_stderr_scope_read_project.json",
}
_BODY_FAILURES = {
    "scope_graphql": "gh_graphql_insufficient_scopes.json",
    "rate_graphql": "gh_graphql_rate_limited.json",
}
_PLAIN_FAILURES = frozenset(
    {"timeout", "spawn_error", "non_json", "failed", "foreign_origin"}
)
_ISSUE_KEYS = frozenset(
    {
        "labels",
        "assignees",
        "state",
        "listed",
        "events",
        "markers",
        "edits",
        "items",
        "reread",
        "discovered",
    }
)


class GhWorld:
    """A scripted GitHub, git and Orca world behind one ``FakeRunner``.

    ``issue(n, **spec)`` adds an issue and registers, in ``runner.script``, the
    exact argv the ``github.argv_*`` builders give for it, so a cycle test
    states its scenario in a few lines. Replies are built when the call is made,
    so changing a spec or the clock after registration still takes effect.

    The shared calls are the own login (``owner-login``, id 1001, a ``Date``
    header taken from the clock plus ``skew_s``), the worktree origin check,
    discovery and, when ``which`` resolves an Orca CLI, its probe. An issue
    spec may hold:

    - ``labels``, ``assignees``: default ``[trigger, approval]`` and ``[login]``;
    - ``state``: the ``gh issue list`` state, default ``"OPEN"``;
    - ``listed``: how many times discovery lists it (0 hides it, 2 repeats it);
    - ``discovered``: raw overrides of the discovery item (labels, assignees);
    - ``events``: G3 items from ``label_event`` (default ``default_events``);
    - ``markers``: G4 items from ``marker_comment`` (default none);
    - ``edits``: ``created_at``, ``edited_at`` and ``comments`` (list of
      ``{id, author, created_at, edited_at}``); default the fixture as it is;
    - ``items``: Project items (list of ``{project_id, status, archived}``);
      default one live item in the configured project with status Backlog;
    - ``reread``: raw overrides of the G7 re-read reply.

    Events and comments are served in pages of ``github.PAGE_SIZE``; the two
    GraphQL reads are served as one page (shortcut: add multi-page cursors when a
    test needs them).

    ``fail(call, how)`` makes a call fail and ``on(call, fn)`` runs ``fn`` when
    it is made. ``call`` is ``user``, ``discover``, ``origin``, ``probe``,
    ``events``, ``comments``, ``edits``, ``items`` or ``reread``; the last five
    take an issue number or None for every issue.
    """

    def __init__(
        self,
        clock: FakeClock,
        config: cycle.Config,
        *,
        login: str = OWN_LOGIN,
        account_id: int = OWN_ID,
        which: Callable[[str], str | None] | None = None,
        runner: FakeRunner | None = None,
    ) -> None:
        self.clock = clock
        self.config = config
        self.account_id = account_id
        self.which = default_which if which is None else which
        self.runner = FakeRunner() if runner is None else runner
        self.skew_s = 0.0
        self.date_text: str | None = None
        self.user_retry_after: str | None = "120"
        self.origin_url = ORIGIN_URL
        self.issues: dict[int, dict] = {}
        self._login = login
        self._fails: dict[tuple[str, int | None], list[_Fail]] = {}
        self._hooks: dict[tuple[str, int | None], list[Callable[[], None]]] = {}
        self._seen: dict[tuple[str, int | None], int] = {}
        self._register_shared()

    # -- the scenario API ------------------------------------------------------

    @property
    def login(self) -> str:
        """The own login ``api user`` answers with."""
        return self._login

    @login.setter
    def login(self, value: str) -> None:
        self._login = value
        self._register_shared()

    def issue(self, n: int, **spec: object) -> GhWorld:
        """Add (or replace) issue ``n``; the default is fully eligible."""
        self._check_keys(spec)
        cfg = self.config
        self.issues[n] = {
            "labels": [cfg.trigger_label, cfg.approval_label],
            "assignees": [self.login],
            "state": "OPEN",
            "listed": 1,
            "events": None,
            "markers": [],
            "edits": None,
            "items": None,
            "reread": None,
            "discovered": None,
            **spec,
        }
        self._register_issue(n)
        return self

    def issues_from(self, numbers: range | list[int], **spec: object) -> GhWorld:
        """Add every number of ``numbers`` with the same ``spec``."""
        for n in numbers:
            self.issue(n, **spec)
        return self

    def update(self, n: int, **spec: object) -> GhWorld:
        """Change fields of issue ``n``."""
        self._check_keys(spec)
        self.issues[n].update(spec)
        return self

    def fail(
        self,
        call: str,
        how: object = "timeout",
        n: int | None = None,
        *,
        times: int | None = 1,
        after: int = 0,
    ) -> GhWorld:
        """Make ``call`` fail ``times`` times (None: always) after ``after`` calls.

        ``how`` is ``timeout``, ``spawn_error``, ``non_json``, ``failed``,
        ``auth``, ``rate``, ``rate_403``, ``transient``, ``scope``,
        ``scope_graphql``, ``rate_graphql``, ``foreign_origin`` (origin only),
        a ``CommandResult`` or a ``(argv, cwd) -> CommandResult`` callable. A G1
        ``rate`` reply carries ``user_retry_after``.
        """
        known = (
            _PLAIN_FAILURES | set(_STDERR_FAILURES) | set(_BODY_FAILURES)
            if isinstance(how, str)
            else None
        )
        if known is not None and how not in known:
            raise ValueError(f"unknown failure {how!r}")
        self._fails.setdefault((call, n), []).append(_Fail(how, times, after))
        return self

    def on(self, call: str, fn: Callable[[], None], n: int | None = None) -> GhWorld:
        """Run ``fn`` each time ``call`` is made, before the reply is chosen."""
        self._hooks.setdefault((call, n), []).append(fn)
        return self

    @property
    def gh_argvs(self) -> list[tuple[str, ...]]:
        """Every ``gh`` argv the runner has seen, in call order."""
        return [argv for argv, _ in self.runner.calls if argv[0] == "gh"]

    def deps(
        self, tmp_path: Path, tmp_state: FileStore, **kwargs: object
    ) -> cycle.Deps:
        """``make_deps`` over this world's runner, clock, config and ``which``."""
        return make_deps(
            tmp_path,
            tmp_state,
            runner=self.runner,
            clock=self.clock,
            config=self.config,
            which=self.which,
            **kwargs,  # type: ignore[arg-type]
        )

    # -- registration ----------------------------------------------------------

    @staticmethod
    def _check_keys(spec: dict) -> None:
        unknown = set(spec) - _ISSUE_KEYS
        if unknown:
            raise TypeError(f"unknown issue field(s): {sorted(unknown)}")

    def _served(
        self,
        call: str,
        n: int | None,
        build: Callable[[tuple[str, ...]], CommandResult],
    ):
        """A script entry: count the call, run hooks, apply a failure or build."""
        keys = [(call, n)] if n is None else [(call, n), (call, None)]

        def serve(argv: list[str], cwd: str | None) -> CommandResult:
            key_argv = tuple(argv)
            for key in keys:
                self._seen[key] = self._seen.get(key, 0) + 1
            for key in keys:
                for hook in list(self._hooks.get(key, ())):
                    hook()
            for key in keys:
                for fail in self._fails.get(key, ()):
                    if self._seen[key] > fail.after and (
                        fail.times is None or fail.used < fail.times
                    ):
                        fail.used += 1
                        return self._failure(fail.how, call, key_argv)
            return build(key_argv)

        return serve

    def _register_shared(self) -> None:
        script, cfg = self.runner.script, self.config
        script[tuple(github.argv_user())] = self._served("user", None, self._user_reply)
        try:
            discover = github.argv_discover(cfg.trigger_label, self.login)
        except ValueError:  # an invalid login never reaches discovery
            pass
        else:
            script[tuple(discover)] = self._served(
                "discover", None, self._discovery_reply
            )
        origin = _ArgvRecorder()
        launch.check_origin(origin, cfg.worktree, 1.0)
        script[origin.argvs[0]] = self._served("origin", None, self._origin_reply)
        probe = _ArgvRecorder()
        launch.find_orca(probe, which=self.which, timeout=1.0)
        for argv in probe.argvs:
            script[argv] = self._served("probe", None, self._probe_reply)

    def _register_issue(self, n: int) -> None:
        script = self.runner.script
        for page in range(1, github.PAGE_CAP + 1):
            script[tuple(github.argv_events(n, page))] = self._served(
                "events", n, lambda argv, p=page: self._events_reply(argv, n, p)
            )
            script[tuple(github.argv_comments(n, page))] = self._served(
                "comments", n, lambda argv, p=page: self._comments_reply(argv, n, p)
            )
        script[tuple(github.argv_edits(n))] = self._served(
            "edits", n, lambda argv: self._ok(argv, self._edits_payload(n))
        )
        script[tuple(github.argv_project_items(n))] = self._served(
            "items", n, lambda argv: self._ok(argv, self._items_payload(n))
        )
        script[tuple(github.argv_reread(n))] = self._served(
            "reread", n, lambda argv: self._ok(argv, self._reread_payload(n))
        )

    # -- replies ---------------------------------------------------------------

    @staticmethod
    def _ok(argv: tuple[str, ...], payload: object) -> CommandResult:
        return result(stdout=json.dumps(payload), argv=argv)

    def _with_headers(self, raw: str) -> tuple[str, str]:
        """Split a G1 fixture: the head with a fresh Date and Retry-After, the body."""
        head, _, body = raw.partition("\n\n")
        date = self.date_text
        if date is None:
            now = self.clock.now() + timedelta(seconds=self.skew_s)
            date = format_datetime(now, usegmt=True)
        lines: list[str] = []
        for line in head.split("\n"):
            name = line.split(":", 1)[0].lower()
            if name == "date":
                line = f"Date: {date}"
            elif name == "retry-after":
                if self.user_retry_after is None:
                    continue
                line = f"Retry-After: {self.user_retry_after}"
            lines.append(line)
        return "\n".join(lines), body

    def _user_reply(self, argv: tuple[str, ...]) -> CommandResult:
        head, body = self._with_headers(load_fixture("gh_api_user_include.json")["raw"])
        who = {**json.loads(body), "login": self.login, "id": self.account_id}
        return result(stdout=f"{head}\n\n{json.dumps(who)}\n", argv=argv)

    def _user_rate_reply(self, argv: tuple[str, ...]) -> CommandResult:
        fixture = load_fixture("gh_api_user_include_429.json")
        head, body = self._with_headers(fixture["raw"])
        return result(
            stdout=f"{head}\n\n{body}",
            stderr=fixture["stderr"],
            returncode=fixture["exit"],
            argv=argv,
        )

    def _origin_reply(self, argv: tuple[str, ...]) -> CommandResult:
        return result(stdout=self.origin_url + "\n", argv=argv)

    def _probe_reply(self, argv: tuple[str, ...]) -> CommandResult:
        # The shape install_user_setup._find_orca reads: a list of named topics.
        return self._ok(argv, {"topics": [{"name": "orca-cli"}]})

    def _discovery_reply(self, argv: tuple[str, ...]) -> CommandResult:
        template = load_fixture("gh_issue_list.json")["payload"][0]
        items: list[dict] = []
        for n, spec in self.issues.items():
            item = {
                **template,
                "number": n,
                "labels": [{"name": name} for name in spec["labels"]],
                "assignees": [{"login": name} for name in spec["assignees"]],
                "state": spec["state"],
                **(spec["discovered"] or {}),
            }
            items += [item] * int(spec["listed"])
        return self._ok(argv, items)

    def _paged(
        self, argv: tuple[str, ...], items: list[dict], page: int
    ) -> CommandResult:
        size = github.PAGE_SIZE
        chunk = items[(page - 1) * size : page * size]
        return self._ok(argv, [_stamped(item) for item in chunk])

    def _events_reply(self, argv: tuple[str, ...], n: int, page: int) -> CommandResult:
        events = self.issues[n]["events"]
        events = default_events(self.config) if events is None else events
        return self._paged(argv, events, page)

    def _comments_reply(
        self, argv: tuple[str, ...], n: int, page: int
    ) -> CommandResult:
        return self._paged(argv, self.issues[n]["markers"], page)

    def _edits_payload(self, n: int) -> dict:
        payload = load_fixture("graphql_edits.json")["payload"]
        spec = self.issues[n]["edits"]
        if spec is None:
            return payload
        issue = payload["data"]["repository"]["issue"]
        template = issue["comments"]["nodes"][0]
        if "created_at" in spec:
            issue["createdAt"] = _stamp(spec["created_at"])
        if "edited_at" in spec:
            issue["lastEditedAt"] = _stamp(spec["edited_at"])
        if "comments" in spec:
            issue["comments"]["nodes"] = [
                {
                    **template,
                    "databaseId": c["id"],
                    "author": None
                    if c.get("author") is None
                    else {"login": c["author"]},
                    "createdAt": _stamp(c["created_at"]),
                    "lastEditedAt": _stamp(c.get("edited_at")),
                }
                for c in spec["comments"]
            ]
        return payload

    def _items_payload(self, n: int) -> dict:
        payload = load_fixture("graphql_project_items.json")["payload"]
        connection = payload["data"]["repository"]["issue"]["projectItems"]
        template = connection["nodes"][0]
        specs = self.issues[n]["items"]
        connection["nodes"] = [
            {
                **template,
                "isArchived": spec.get("archived", False),
                "project": {"id": spec.get("project_id", self.config.project_id)},
                "fieldValueByName": None
                if spec.get("status", "Backlog") is None
                else {
                    **template["fieldValueByName"],
                    "name": spec.get("status", "Backlog"),
                },
            }
            for spec in ([{}] if specs is None else specs)
        ]
        return payload

    def _reread_payload(self, n: int) -> dict:
        spec = self.issues[n]
        body = load_fixture("gh_issue_reread.json")["payload"]
        body.update(
            number=n,
            state="open",
            labels=list(spec["labels"]),
            assignees=list(spec["assignees"]),
        )
        body.update(spec["reread"] or {})
        return body

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
            return result(stdout=FOREIGN_ORIGIN_URL + "\n", argv=argv)
        if how == "rate" and call == "user":
            return self._user_rate_reply(argv)
        if how in _STDERR_FAILURES:
            fixture = load_fixture(_STDERR_FAILURES[how])
            return result(
                stderr=fixture["stderr"], returncode=fixture["exit"], argv=argv
            )
        if how in _BODY_FAILURES:
            return self._ok(argv, load_fixture(_BODY_FAILURES[how])["payload"])
        raise ValueError(f"unknown failure {how!r}")


@pytest.fixture
def gh_world(tmp_path):
    """Factory for ``GhWorld``; fails the test if a runner saw an unscripted argv.

    ``make(clock=None, config=None, **kwargs)``: the clock defaults to
    ``FakeClock(CYCLE_NOW)`` and the config to ``make_config(tmp_path)``.
    """
    made: list[GhWorld] = []

    def make(
        *,
        clock: FakeClock | None = None,
        config: cycle.Config | None = None,
        **kwargs,
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
        # FR-029, design 8.5 (Gate C C-11): every call of every scripted cycle got
        # a timeout, never below the 5 s floor and never above the longest
        # configured one (20 s for gh; 10 s for git and the probe).
        for seconds in world.runner.timeouts:
            assert seconds is not None and 5.0 <= seconds <= 20.0, (
                f"timeout out of range: {world.runner.timeouts}"
            )


# ==============================================================================
# Part 5: the stub-on-PATH fixture and the scenario helpers (plan step 8.1).
#
# ``test_cli_e2e.py`` runs the real CLI as a subprocess whose ``PATH`` holds four
# stubs and nothing else, so no real ``gh``, ``orca``, ``orca-ide`` or ``git`` can
# run (decisions DF-10, DF-34, DF-55, DF-56). The stubs are written into
# ``tmp_path`` at test time; nothing executable is committed.
# ==============================================================================

STUB_TOOLS = ("gh", "orca", "orca-ide", "git")
STUB_UNSCRIPTED_STDERR = "stub: unscripted argv"

# One template for all four stubs. Standard library only; the shebang names
# /usr/bin/env by absolute path and finds python3 in linkbin.
_STUB_TEMPLATE = '''#!/usr/bin/env python3
"""PATH stub for __TOOL__, written by tests/issue_watch/conftest.py."""

import json
import os
import sys
import time

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
    records = []
    log = os.environ.get("IW_STUB_LOG")
    call = 1
    if log and os.path.exists(log):
        with open(log, encoding="utf-8") as handle:
            for line in handle:
                if "tool" in json.loads(line):
                    call += 1
    records.append(
        {
            "call": call,
            "tool": TOOL,
            "argc": len(argv),
            "cwd": os.getcwd(),
            "matched": rule is not None,
        }
    )
    for index, arg in enumerate(argv):
        records.append({"call": call, "i": index, "arg": arg})
    state_dir = os.environ.get("IW_STUB_STATE_DIR")
    if state_dir and TOOL in ("orca", "orca-ide") and argv[:2] == ["agent", "launch"]:
        try:
            with open(os.path.join(state_dir, "dispatch.json"), "rb") as handle:
                text = handle.read().decode("utf-8", "replace")
        except OSError:
            text = None
        records.append({"call": call, "dispatch_json": text})
    if log:
        blob = "".join(json.dumps(record) + "\\n" for record in records)
        fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        try:
            os.write(fd, blob.encode("utf-8"))
        finally:
            os.close(fd)
    if rule is None:
        sys.stderr.write("__UNSCRIPTED__\\n")
        sys.stderr.flush()
        sys.exit(99)
    if rule.get("sleep"):
        time.sleep(float(rule["sleep"]))
    sys.stdout.buffer.write(rule.get("stdout", "").encode("utf-8"))
    sys.stdout.buffer.flush()
    sys.stderr.buffer.write(rule.get("stderr", "").encode("utf-8"))
    sys.stderr.buffer.flush()
    sys.exit(int(rule.get("exit", 0)))


main()
'''


def write_scenario(tmp_path: Path, rules: dict[str, list[dict]]) -> Path:
    """Write ``tmp_path / "scenario.json"`` (the file ``IW_STUB_SCENARIO`` names).

    ``rules`` maps a stub name to its rules, each ``{"argv_prefix": [...],
    "exit": int, "stdout": str, "stderr": str, "sleep": float}`` with only
    ``argv_prefix`` required. The first rule whose prefix starts the arguments
    wins. Returns the path. Calling it again replaces the scenario.
    """
    for tool, tool_rules in rules.items():
        if tool not in STUB_TOOLS:
            raise ValueError(f"no stub named {tool!r}")
        for rule in tool_rules:
            prefix = rule.get("argv_prefix")
            if not isinstance(prefix, list) or not all(
                isinstance(arg, str) for arg in prefix
            ):
                raise ValueError(f"argv_prefix must be a list of str: {rule!r}")
    path = tmp_path / "scenario.json"
    path.write_text(json.dumps(rules), encoding="utf-8")
    return path


def read_calls(log_path: Path | str) -> list[dict]:
    """Rebuild the stub calls from the JSONL log, in call order.

    Each item is ``{"call", "tool", "argv", "cwd", "matched"}`` (``argv`` is the
    list of arguments after the program name) plus ``dispatch_json`` (the text,
    or None when the file was missing) only when the stub took the FR-010
    snapshot before answering. A missing log is an empty list.
    """
    path = Path(log_path)
    if not path.exists():
        return []
    calls: dict[int, dict] = {}
    args: dict[int, dict[int, str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        number = record["call"]
        if "tool" in record:
            calls[number] = {
                "call": number,
                "tool": record["tool"],
                "argc": record["argc"],
                "cwd": record["cwd"],
                "matched": record["matched"],
            }
        elif "i" in record:
            args.setdefault(number, {})[record["i"]] = record["arg"]
        else:
            calls[number]["dispatch_json"] = record["dispatch_json"]
    out = []
    for number in sorted(calls):
        call = calls[number]
        given = args.get(number, {})
        assert sorted(given) == list(range(call.pop("argc"))), (
            f"stub log call {number} is missing arguments: {sorted(given)}"
        )
        call["argv"] = [given[i] for i in range(len(given))]
        out.append(call)
    return out


@pytest.fixture
def stub_path(tmp_path):
    """The environment for a subprocess that can only reach the four stubs.

    Creates ``<tmp_path>/stubbin`` (executable ``gh``, ``orca``, ``orca-ide`` and
    ``git``) and ``<tmp_path>/linkbin`` (only ``python3``, a symlink to
    ``sys.executable``). Returns a dict whose ``PATH`` is exactly
    ``<tmp>/stubbin:<tmp>/linkbin``, plus ``HOME``, ``XDG_STATE_HOME``,
    ``IW_STUB_SCENARIO`` (starts as an empty scenario: every call is unscripted),
    ``IW_STUB_LOG`` (JSONL, read it with ``read_calls``) and nothing else. A test
    sets ``IW_STUB_STATE_DIR`` itself to get the FR-010 ``dispatch.json`` snapshot.
    The process never inherits the test environment. At teardown the test fails
    if any stub call matched no scenario rule.
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
            f"{name} resolves to {found!r}, not the stub {stubbin / name}"
        )
    yield env
    unmatched = [
        (call["tool"], call["argv"]) for call in read_calls(log) if not call["matched"]
    ]
    assert not unmatched, f"stub saw unscripted argv: {unmatched}"
