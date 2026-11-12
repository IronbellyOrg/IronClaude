"""Tests for the read side of ``superclaude sweep`` (DESIGN section 11, ``test_probes_allowlist.py`` row).

Covers NFR-003, NFR-014, FR-021, FR-026, FR-020, NFR-007, GQ-109, M7, the SPEC section 11
failure modes and the FR-010 inputs that ``probes`` produces (the ``collect`` source rows,
``truncated`` and the path-B time fields).

Two kinds of fake are used, and neither starts a process (the autouse guard in
``conftest.py`` enforces that):

* ``fake_run`` stands in for ``subprocess.run``. The real ``_orca`` and ``_git`` run on top of
  it, so argv[0], the allowlist, the result classes and the byte limits are exercised end to
  end.
* ``patch_orca`` and ``patch_git`` (``conftest.py``) replace the two seams for the ``collect``
  cases that need exact control of what Orca returns.

Budget tests inject a fake clock; nothing here waits on a real one. The template list, the id
shapes, the FR-021 forbidden verbs, the limits and every reason string are written out as
literals taken from DESIGN, so a changed constant in ``probes.py`` fails here.
"""

from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from superclaude.cli.sweep import probes, report
from superclaude.cli.sweep.classify import classify_all
from superclaude.cli.sweep.models import SweepContext

REPO = Path(__file__).resolve().parents[2]
SWEEP_DIR = REPO / "src" / "superclaude" / "cli" / "sweep"
FIXTURES = Path(__file__).parent / "fixtures"

UTC = timezone.utc
NOW = datetime(2026, 11, 8, 12, 0, 0, tzinfo=UTC)
KIB = 1024
MIB = 1024 * 1024

RUN = "run_a4723d345399"  # the captured Run id (step 1.0a)
RUN1 = "run_000000000001"
RUN2 = "run_000000000002"
RUN3 = "run_000000000003"
DISPATCH = "ctx_4e3237d227c3"  # a captured Dispatch id

# DESIGN 7.3: the ten templates, token for token. ``<run>`` and ``<dispatch>`` are placeholders.
EXPECTED_TEMPLATES = (
    ("orchestration", "run-current"),
    ("orchestration", "worker-list", "--run", "<run>", "--json"),
    ("orchestration", "worker-show", "--dispatch", "<dispatch>", "--json"),
    ("orchestration", "task-list", "--ready", "--run", "<run>", "--json"),
    ("orchestration", "task-list", "--run", "<run>", "--json"),
    ("worktree", "ps", "--json"),
    ("worktree", "list", "--json"),
    ("worktree", "current", "--json"),
    ("worktree", "ps", "--agent-wait"),
    ("worktree", "ps", "--agent-wait", "--json"),
)
# The four templates DESIGN 7.3 marks "not called in Phase 1".
NOT_CALLED = (
    ("worktree", "list", "--json"),
    ("worktree", "current", "--json"),
    ("worktree", "ps", "--agent-wait"),
    ("worktree", "ps", "--agent-wait", "--json"),
)
# FR-021, DESIGN 7.3: the forbidden verbs live in this test and nowhere in ``probes.py``.
FORBIDDEN_VERBS = (
    "check",
    "ask",
    "reply",
    "send",
    "inbox",
    "open",
    "worker-start",
    "task-create",
    "task-update",
    "dispatch",
    "stop",
    "rm",
)
_ID_RES = {
    "<run>": re.compile(r"run_[0-9a-f]{12}"),
    "<dispatch>": re.compile(r"ctx_[0-9a-f]{12}"),
}
GIT_STATUS = ("status", "--porcelain=v1", "-z", "--branch", "--untracked-files=all")

CONCRETE_ARGV = tuple(
    tuple(
        RUN if tok == "<run>" else DISPATCH if tok == "<dispatch>" else tok
        for tok in template
    )
    for template in EXPECTED_TEMPLATES
)


def _is_template_argv(argv: tuple[str, ...]) -> bool:
    """True when ``argv`` equals one template token for token (placeholders by id shape)."""
    for template in EXPECTED_TEMPLATES:
        if len(template) == len(argv) and all(
            (_ID_RES[t].fullmatch(a) is not None) if t in _ID_RES else t == a
            for t, a in zip(template, argv)
        ):
            return True
    return False


# --- Orca argv builders ------------------------------------------------------------------


def wl(run: str) -> tuple[str, ...]:
    return ("orchestration", "worker-list", "--run", run, "--json")


def tl_ready(run: str) -> tuple[str, ...]:
    return ("orchestration", "task-list", "--ready", "--run", run, "--json")


def tl_all(run: str) -> tuple[str, ...]:
    return ("orchestration", "task-list", "--run", run, "--json")


def ws(dispatch: str) -> tuple[str, ...]:
    return ("orchestration", "worker-show", "--dispatch", dispatch, "--json")


PS = ("worktree", "ps", "--json")
RUN_CURRENT = ("orchestration", "run-current")


# --- Fakes -------------------------------------------------------------------------------


class FakeClock:
    """The fake ``Budget`` clock; time moves only when a test advances it."""

    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


class FakeRun:
    """Stands in for ``subprocess.run``; records every call and answers from canned replies.

    A reply is a ``(returncode, stdout, stderr)`` tuple, an exception instance (raised), or a
    callable ``(argv, kwargs) -> tuple`` (it may raise). Orca replies are keyed by the argv
    after the binary; every git call gets ``git``.
    """

    def __init__(self) -> None:
        self.calls: list[dict] = []
        self.orca: dict[tuple[str, ...], object] = {}
        self.git: object = (0, b"## main\0", b"")
        self.default: object = (1, b"", b"no canned reply")

    def reply(self, *args, code=0, out=b"", err=b"", raises=None) -> None:
        self.orca[tuple(args)] = raises if raises is not None else (code, out, err)

    def __call__(self, argv, **kwargs):
        self.calls.append({"argv": list(argv), "kwargs": kwargs})
        if argv[0] == "git":
            reply = self.git
        else:
            reply = self.orca.get(tuple(argv[1:]), self.default)
        if isinstance(reply, BaseException):
            raise reply
        if callable(reply):
            reply = reply(list(argv), kwargs)
        code, out, err = reply
        return SimpleNamespace(returncode=code, stdout=out, stderr=err)

    @property
    def orca_argv(self) -> list[tuple[str, ...]]:
        return [tuple(c["argv"][1:]) for c in self.calls if c["argv"][0] != "git"]

    @property
    def git_argv(self) -> list[list[str]]:
        return [c["argv"] for c in self.calls if c["argv"][0] == "git"]


@pytest.fixture
def fake_run(monkeypatch) -> FakeRun:
    """Patch ``subprocess.run`` inside the test (after the autouse guard) and clear the env."""
    run = FakeRun()
    monkeypatch.setattr(probes.subprocess, "run", run)
    monkeypatch.delenv("ORCA_CLI_COMMAND", raising=False)
    return run


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture(autouse=True)
def _no_orca_version_file(monkeypatch):
    """``collect`` reads Orca's package.json; a test must not depend on the host's copy."""
    monkeypatch.setattr(probes, "read_orca_version", lambda: None)


def _body(obj: object) -> bytes:
    return json.dumps(obj).encode("utf-8")


def _envelope(result: object) -> bytes:
    return _body({"id": "req-1", "ok": True, "result": result})


def _error_envelope(code: str, message: str) -> bytes:
    return _body(
        {"id": "req-1", "ok": False, "error": {"code": code, "message": message}}
    )


def _captured(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text("utf-8"))


def _apply(fake_run: FakeRun, args: tuple[str, ...], reply: object) -> None:
    """Install ``reply`` (a tuple, or a factory that makes the exception to raise)."""
    if callable(reply):
        fake_run.reply(*args, raises=reply())
    else:
        code, out, err = reply  # type: ignore[misc]
        fake_run.reply(*args, code=code, out=out, err=err)


def _ctx(root: Path, runs: tuple[str, ...] = (RUN,)) -> SweepContext:
    window = timedelta(hours=6)
    return SweepContext(
        now=NOW, window=window, window_start=NOW - window, root=root, runs=tuple(runs)
    )


def _collect(sweep_root, clock, runs: tuple[str, ...] = (RUN1,), **budget_kw):
    budget = probes.Budget(clock=clock, **budget_kw)
    return probes.collect(_ctx(sweep_root.root, runs), runs, sweep_root.root, budget)


# --- Canned Orca data for the patch_orca cases -------------------------------------------


def did(n: int) -> str:
    return f"ctx_{n:012x}"


def _rows(ids, status: str = "completed") -> list[dict]:
    return [
        {"dispatchId": d, "taskId": f"task_{i}", "dispatchStatus": status}
        for i, d in enumerate(ids)
    ]


def _show_result(dispatch: str, run: str = RUN1, **dispatch_over) -> dict:
    dispatch_fields = {
        "id": dispatch,
        "runId": run,
        "status": "completed",
        "assigneeHandle": f"term_{dispatch}",
        "dispatchedAt": "2026-11-08 07:00:00",
        "completedAt": "2026-11-08T08:00:00Z",
    }
    dispatch_fields.update(dispatch_over)
    return {
        "dispatch": dispatch_fields,
        "projection": {"liveness": {"verdict": "exited"}},
        "terminal": {},
    }


def _stock_run(orca, run: str, rows: list[dict], *, tasks: list[dict] | None = None):
    """Canned ``worker-list``, both ``task-list`` calls and one ``worker-show`` per row id."""
    orca.respond(
        wl(run),
        {
            "workers": rows,
            "page": {"limit": 100, "total": len(rows), "hasMore": False},
        },
    )
    orca.respond(tl_ready(run), {"tasks": []})
    orca.respond(tl_all(run), {"tasks": tasks or []})
    for row in rows:
        dispatch = row["dispatchId"]
        orca.respond(ws(dispatch), _show_result(dispatch, run))


def _stock_ps(orca, paths=()) -> None:
    orca.respond(
        PS, {"worktrees": [{"path": str(p)} for p in paths], "truncated": False}
    )


def _spend(monkeypatch, fake, clock: FakeClock, seconds) -> None:
    """Wrap the Orca fake so every call uses fake-clock time (a number or ``(timeout, args)``)."""

    def run(*args, timeout):
        result = fake(*args, timeout=timeout)
        clock.advance(seconds(timeout, args) if callable(seconds) else seconds)
        return result

    monkeypatch.setattr(probes, "_orca", run)


def _stock_captured(fake_run: FakeRun, worktree_paths) -> list[str]:
    """Reply with the captured fixtures for ``RUN``; ``worktree ps`` lists ``worktree_paths``."""
    listing = _captured("captured-worker-list.json")
    fake_run.reply(*wl(RUN), out=_body(listing))
    fake_run.reply(
        *tl_ready(RUN), out=_body(_captured("captured-task-list-ready.json"))
    )
    fake_run.reply(*tl_all(RUN), out=_body(_captured("captured-task-list.json")))
    for n in range(1, 6):
        show = _captured(f"captured-worker-show-{n}.json")
        fake_run.reply(*ws(show["result"]["dispatch"]["id"]), out=_body(show))
    ps = _captured("captured-worktree-ps.json")
    sample = ps["result"]["worktrees"][0]
    ps["result"]["worktrees"] = [dict(sample, path=str(p)) for p in worktree_paths]
    fake_run.reply(*PS, out=_body(ps))
    return [row["dispatchId"] for row in listing["result"]["workers"]]


# ===========================================================================================
# NFR-003, NFR-014, FR-021, GQ-109: the allowlists
# ===========================================================================================


def test_allowed_orca_is_exactly_the_ten_templates():
    assert probes.ALLOWED_ORCA == EXPECTED_TEMPLATES
    assert len(set(probes.ALLOWED_ORCA)) == 10


def test_allowed_orca_names_seven_verbs():
    verbs = {
        t[1] if t[0] == "orchestration" else f"worktree {t[1]}"
        for t in probes.ALLOWED_ORCA
    }
    assert verbs == {
        "run-current",
        "worker-list",
        "worker-show",
        "task-list",
        "worktree ps",
        "worktree list",
        "worktree current",
    }


def test_other_allowlist_constants_are_pinned():
    assert probes.ORCA_BINARY_DEFAULT == "orca-ide"
    assert probes.FORBIDDEN_TOKENS == frozenset({"--include-remote"})
    assert probes.ALLOWED_GIT == (GIT_STATUS,)
    assert probes.RUN_ID_RE == r"run_[0-9a-f]{12}"
    assert probes.DISPATCH_ID_RE == r"ctx_[0-9a-f]{12}"


@pytest.mark.parametrize("argv", CONCRETE_ARGV, ids=lambda a: " ".join(a))
def test_every_template_is_accepted(argv):
    probes.check_orca_argv(argv)  # raises ValueError when refused


@pytest.mark.parametrize("flags", [(), ("--json",)], ids=["no-json", "json"])
def test_worktree_ps_agent_wait_templates_are_accepted(fake_run, flags):
    args = ("worktree", "ps", "--agent-wait", *flags)
    probes.check_orca_argv(args)
    fake_run.reply(*args, out=_envelope({"worktrees": []}))

    probes._orca(*args, timeout=5.0)

    assert fake_run.orca_argv == [
        args
    ]  # the allowlist let the call through to the process
    assert fake_run.calls[0]["argv"][0] == "orca-ide"


NEGATIVE_ARGV = {
    "check": ("orchestration", "check"),
    "inbox": ("orchestration", "inbox"),
    "worker-read": ("orchestration", "worker-read", "--dispatch", DISPATCH, "--json"),
    "gate-list": ("orchestration", "gate-list", "--run", RUN, "--json"),
    "extra-flag": (*wl(RUN), "--verbose"),
    "include-remote-last": ("worktree", "ps", "--json", "--include-remote"),
    "include-remote-first": ("--include-remote", "worktree", "ps", "--json"),
    "include-remote-with-agent-wait": (
        "worktree",
        "ps",
        "--agent-wait",
        "--include-remote",
    ),
    "include-remote-alone": ("--include-remote",),
    "run-list": ("orchestration", "run-list"),
    "run-list-json": ("orchestration", "run-list", "--json"),
    "run-current-with-json": ("orchestration", "run-current", "--json"),
    "flag-prefix": ("worktree", "ps", "--agent"),
    "worker-list-without-json": ("orchestration", "worker-list", "--run", RUN),
    "reordered-flags": ("orchestration", "worker-list", "--json", "--run", RUN),
    "verb-prefix-only": ("orchestration",),
    "empty": (),
    "run-id-uppercase": wl("run_A4723D345399"),
    "run-id-too-short": wl("run_a4723d34539"),
    "run-id-with-suffix": wl(RUN + "0"),
    "dispatch-id-as-run": wl(DISPATCH),
    "run-id-as-dispatch": ws(RUN),
    "dispatch-id-bad-shape": ws("ctx_xyz"),
    "non-string-token": ("orchestration", 5),
}


@pytest.mark.parametrize("argv", NEGATIVE_ARGV.values(), ids=NEGATIVE_ARGV.keys())
def test_negative_argv_raises_value_error_before_a_subprocess(fake_run, argv):
    with pytest.raises(ValueError):
        probes.check_orca_argv(argv)
    with pytest.raises(ValueError):
        probes._orca(*argv, timeout=5.0)
    assert fake_run.calls == []  # no process was started for a refused argv


@pytest.mark.parametrize("argv", NEGATIVE_ARGV.values(), ids=NEGATIVE_ARGV.keys())
def test_recorded_argv_fake_refuses_the_same_negatives(patch_orca, argv):
    with pytest.raises(ValueError):
        probes._orca(*argv, timeout=5.0)
    assert (
        patch_orca.calls == []
    )  # the fake checks first and records only an allowed argv


@pytest.mark.parametrize("verb", FORBIDDEN_VERBS)
def test_fr021_forbidden_verbs_are_in_no_template_and_are_refused(fake_run, verb):
    assert all(verb not in template for template in probes.ALLOWED_ORCA)
    for group in ("orchestration", "worktree"):
        for argv in (
            (group, verb),
            (group, verb, "--json"),
            (group, verb, "--run", RUN, "--json"),
            (group, verb, "--dispatch", DISPATCH, "--json"),
        ):
            with pytest.raises(ValueError):
                probes._orca(*argv, timeout=5.0)
    assert fake_run.calls == []


def test_probes_source_holds_no_write_verb_even_as_a_string():
    tree = ast.parse((SWEEP_DIR / "probes.py").read_text("utf-8"))
    strings = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }
    # "dispatch" is also the name of the JSON object in a ``worker-show`` reply, which
    # ``parse_worker_show`` reads; it is a key there, never an argv token.
    assert strings.isdisjoint(set(FORBIDDEN_VERBS) - {"dispatch"})


GIT_NEGATIVE = {
    "rev-parse": ("rev-parse", "HEAD"),
    "rev-parse-bare": ("rev-parse",),
    "log": ("log",),
    "log-oneline": ("log", "--oneline"),
    "branch": ("branch",),
    "version": ("--version",),
    "stash": ("stash",),
    "stash-list": ("stash", "list"),
    "stash-push": ("stash", "push", "-u"),
    "stash-pop": ("stash", "pop"),
    "stash-drop": ("stash", "drop"),
    "stash-apply": ("stash", "apply"),
    "stash-show": ("stash", "show"),
    "status-short": ("status", "--short"),
    "status-extra-flag": (*GIT_STATUS, "--ignored"),
    "status-prefix": GIT_STATUS[:-1],
    "status-reordered": (GIT_STATUS[0], GIT_STATUS[2], GIT_STATUS[1], *GIT_STATUS[3:]),
    "empty": (),
}


@pytest.mark.parametrize("args", GIT_NEGATIVE.values(), ids=GIT_NEGATIVE.keys())
def test_git_negatives_raise_value_error_before_a_subprocess(fake_run, args):
    with pytest.raises(ValueError):
        probes.check_git_args(args)
    with pytest.raises(ValueError):
        probes._git(Path("/work/tree-a"), *args, timeout=5.0)
    assert fake_run.calls == []


def test_the_one_git_call_is_accepted(fake_run):
    probes.check_git_args(GIT_STATUS)

    probes._git(Path("/work/tree-a"), *GIT_STATUS, timeout=5.0)

    (argv,) = fake_run.git_argv
    assert argv == ["git", "--no-optional-locks", "-C", "/work/tree-a", *GIT_STATUS]


# ===========================================================================================
# NFR-003: argv[0] and the full-sweep recording
# ===========================================================================================


def test_orca_binary_default_is_orca_ide_never_bare_orca(fake_run):
    assert probes.orca_binary() == "orca-ide"
    assert probes.orca_binary() != "orca"


def test_orca_binary_is_orca_cli_command_when_set(fake_run, monkeypatch):
    monkeypatch.setenv("ORCA_CLI_COMMAND", "/opt/custom/orca-x")
    assert probes.orca_binary() == "/opt/custom/orca-x"


def test_argv0_is_orca_ide_by_default_then_orca_cli_command(fake_run, monkeypatch):
    fake_run.reply(*PS, out=_envelope({"worktrees": []}))

    probes._orca(*PS, timeout=5.0)
    monkeypatch.setenv("ORCA_CLI_COMMAND", "/opt/custom/orca-x")
    probes._orca(*PS, timeout=5.0)

    assert [c["argv"] for c in fake_run.calls] == [
        ["orca-ide", *PS],
        ["/opt/custom/orca-x", *PS],
    ]
    kwargs = fake_run.calls[0]["kwargs"]
    assert kwargs["timeout"] == 5.0
    assert kwargs["check"] is False
    assert kwargs["stdin"] is subprocess.DEVNULL


def test_full_sweep_records_only_template_argv(sweep_root, fake_run, clock):
    other = sweep_root.worktree("wt-a")
    _stock_captured(fake_run, [sweep_root.root, other])

    inp = _collect(sweep_root, clock, (RUN,))

    orca_argv = fake_run.orca_argv
    assert inp.orca_available is True
    assert orca_argv and all(_is_template_argv(a) for a in orca_argv)
    # worker-list, two task-list calls, five worker-show calls and one worktree ps.
    assert len(orca_argv) == 1 + 2 + 5 + 1
    assert {c["argv"][0] for c in fake_run.calls} == {"orca-ide", "git"}
    assert inp.orca_binary == "orca-ide"


@pytest.mark.parametrize("template", NOT_CALLED, ids=lambda t: " ".join(t))
def test_full_sweep_issues_zero_argv_for_the_not_called_templates(
    sweep_root, fake_run, clock, template
):
    _stock_captured(fake_run, [sweep_root.root])

    _collect(sweep_root, clock, (RUN,))

    assert [a for a in fake_run.orca_argv if a == template] == []
    assert [
        a
        for a in fake_run.orca_argv
        if a[:2] in (("worktree", "list"), ("worktree", "current"))
    ] == []
    assert [a for a in fake_run.orca_argv if "--agent-wait" in a] == []


def test_full_sweep_argv0_follows_orca_cli_command(
    sweep_root, fake_run, clock, monkeypatch
):
    monkeypatch.setenv("ORCA_CLI_COMMAND", "/opt/custom/orca-x")
    _stock_captured(fake_run, [sweep_root.root])

    inp = _collect(sweep_root, clock, (RUN,))

    argv0 = {c["argv"][0] for c in fake_run.calls if c["argv"][0] != "git"}
    assert argv0 == {"/opt/custom/orca-x"}
    assert inp.orca_binary == "/opt/custom/orca-x"
    assert all(_is_template_argv(a) for a in fake_run.orca_argv)


def test_full_sweep_runs_one_lock_free_git_status_per_worktree(
    sweep_root, fake_run, clock
):
    other = sweep_root.worktree("wt-a")
    _stock_captured(fake_run, [sweep_root.root, other])

    _collect(sweep_root, clock, (RUN,))

    paths = [str(sweep_root.root.resolve()), str(other.resolve())]
    assert [a[:4] for a in fake_run.git_argv] == [
        ["git", "--no-optional-locks", "-C", p] for p in paths
    ]
    assert all(a[4:] == list(GIT_STATUS) for a in fake_run.git_argv)


# ===========================================================================================
# FR-026: result classes
# ===========================================================================================

ORCA_OK = (0, _envelope({"worktrees": []}), b"")

CLASS_CASES = [
    pytest.param(ORCA_OK, "ok", None, id="ok"),
    pytest.param(
        lambda: FileNotFoundError(2, "No such file or directory"),
        "unavailable",
        "binary not found: orca-ide",
        id="binary-not-found",
    ),
    pytest.param(
        lambda: subprocess.TimeoutExpired(["orca-ide"], 5.0),
        "unavailable",
        "timeout after 5 s",
        id="timeout",
    ),
    pytest.param(
        (1, _error_envelope("runtime_unavailable", "Orca is not running"), b""),
        "unavailable",
        "runtime_unavailable",
        id="marker-as-error-code",
    ),
    pytest.param(
        (1, b"", b"runtime_unavailable\nsecond line\n"),
        "unavailable",
        "runtime_unavailable",
        id="marker-as-first-stderr-line",
    ),
    pytest.param(
        (1, b"", b"boom\n"), "call_failed", "orca call failed (exit 1)", id="exit-1"
    ),
    pytest.param(
        (3, _error_envelope("run_not_found", "Run was not found."), b""),
        "call_failed",
        "orca call failed (exit 3)",
        id="exit-3-with-other-error-code",
    ),
    # The quoted-marker negative fixtures: the marker counts only as the error code or the
    # whole first stderr line.
    pytest.param(
        (1, b"", b'error: "runtime_unavailable" is only quoted here\n'),
        "call_failed",
        "orca call failed (exit 1)",
        id="quoted-marker-in-stderr-line",
    ),
    pytest.param(
        (1, b"", b"failed\nruntime_unavailable\n"),
        "call_failed",
        "orca call failed (exit 1)",
        id="marker-on-second-stderr-line",
    ),
    pytest.param(
        (1, _error_envelope("other_error", "runtime_unavailable"), b""),
        "call_failed",
        "orca call failed (exit 1)",
        id="marker-inside-error-message",
    ),
    pytest.param(
        (1, b"runtime_unavailable", b""),
        "call_failed",
        "orca call failed (exit 1)",
        id="marker-in-plain-stdout",
    ),
    pytest.param(
        (0, _envelope({"worktrees": [], "note": "runtime_unavailable"}), b""),
        "ok",
        None,
        id="marker-inside-an-ok-result",
    ),
    # A malformed body with exit 0.
    pytest.param(
        (0, b"not json at all", b""),
        "call_failed",
        "orca call failed (invalid response)",
        id="zero-exit-not-json",
    ),
    pytest.param(
        (0, b"", b""),
        "call_failed",
        "orca call failed (invalid response)",
        id="zero-exit-empty-body",
    ),
    pytest.param(
        (0, _body({"ok": True}), b""),
        "call_failed",
        "orca call failed (invalid response)",
        id="zero-exit-ok-without-result",
    ),
    pytest.param(
        (0, _body({"ok": False, "result": {}}), b""),
        "call_failed",
        "orca call failed (invalid response)",
        id="zero-exit-ok-false",
    ),
    pytest.param(
        (0, _body({"ok": True, "result": []}), b""),
        "call_failed",
        "orca call failed (invalid response)",
        id="zero-exit-result-is-a-list",
    ),
    pytest.param(
        (0, _body([1, 2]), b""),
        "call_failed",
        "orca call failed (invalid response)",
        id="zero-exit-body-is-a-list",
    ),
]


@pytest.mark.parametrize(("reply", "kind", "reason"), CLASS_CASES)
def test_orca_result_classes(fake_run, reply, kind, reason):
    _apply(fake_run, PS, reply)

    result = probes._orca(*PS, timeout=5.0)

    assert (result.kind, result.reason) == (kind, reason)
    if kind == "ok":
        assert isinstance(result.data, dict)
    else:
        assert result.data is None


def test_ok_data_is_the_envelope_result_object(fake_run):
    _apply(
        fake_run,
        PS,
        (0, _envelope({"worktrees": [], "note": "runtime_unavailable"}), b""),
    )

    result = probes._orca(*PS, timeout=5.0)

    assert result.data == {"worktrees": [], "note": "runtime_unavailable"}


def test_a_process_that_cannot_start_is_unavailable_with_the_binary_named(fake_run):
    _apply(fake_run, PS, lambda: PermissionError(13, "Permission denied"))

    result = probes._orca(*PS, timeout=5.0)

    assert result.kind == "unavailable"
    assert result.reason is not None
    assert result.reason.startswith("could not start orca-ide: ")


def test_empty_run_current_body_is_call_failed_invalid_response(fake_run):
    _apply(fake_run, RUN_CURRENT, (0, b"", b""))

    result = probes._orca(*RUN_CURRENT, timeout=5.0)

    assert (result.kind, result.data, result.reason) == (
        "call_failed",
        None,
        "orca call failed (invalid response)",
    )


def test_captured_no_binding_fixture_is_no_binding(fake_run, clock):
    # Step 1.0a row 3: the no-binding shape was captured (exit 0, one plain sentence). The
    # bound shape was not seen, so no test here pins how a bound ``run-current`` prints.
    captured = _captured("captured-run-current.json")
    assert captured["exit_code"] == 0
    assert captured["stdout"] == "No Run is bound to this terminal.\n"
    fake_run.reply(*RUN_CURRENT, out=captured["stdout"].encode("utf-8"))

    result = probes._orca(*RUN_CURRENT, timeout=5.0)
    assert (result.kind, result.data, result.reason) == (
        "no_binding",
        None,
        "no Run bound",
    )

    with pytest.raises(probes.BindingError) as exc:
        probes.bind_run(probes.Budget(clock=clock))
    assert str(exc.value) == "no Run bound: pass --run <id>"


FIRST_CALL_CAUSES = [
    pytest.param(
        lambda: FileNotFoundError(2, "No such file or directory"),
        "binary not found: orca-ide",
        id="binary-not-found",
    ),
    pytest.param(
        lambda: subprocess.TimeoutExpired(["orca-ide"], 10.0),
        "timeout after 10 s",
        id="timeout",
    ),
    pytest.param(
        (1, _error_envelope("runtime_unavailable", "Orca is not running"), b""),
        "runtime_unavailable",
        id="marker-as-error-code",
    ),
    pytest.param(
        (1, b"", b"runtime_unavailable\n"),
        "runtime_unavailable",
        id="marker-as-first-stderr-line",
    ),
    pytest.param((1, b"", b"boom\n"), "orca call failed (exit 1)", id="nonzero-exit"),
    pytest.param((0, b"", b""), "orca call failed (invalid response)", id="empty-body"),
    pytest.param(
        (0, b"  \n", b""), "orca call failed (invalid response)", id="blank-body"
    ),
    pytest.param(
        (0, f"{RUN1} and {RUN2}\n".encode(), b""),
        "orca call failed (invalid response)",
        id="two-run-ids",
    ),
]


@pytest.mark.parametrize(("reply", "reason"), FIRST_CALL_CAUSES)
def test_each_unavailable_cause_on_call_one_stops_the_binding(
    fake_run, clock, reply, reason
):
    _apply(fake_run, RUN_CURRENT, reply)
    budget = probes.Budget(clock=clock)

    with pytest.raises(probes.BindingError) as exc:
        probes.bind_run(budget)

    assert str(exc.value) == (
        f"Orca unavailable ({reason}); no Run binding could be established: "
        "pass --run <id>"
    )
    assert budget.orca_calls == 1
    assert fake_run.orca_argv == [RUN_CURRENT]


def test_nonzero_exit_is_unavailable_on_call_one_and_call_failed_later(fake_run, clock):
    _apply(fake_run, PS, (1, b"", b"boom\n"))
    budget = probes.Budget(clock=clock)

    first = probes._call(budget, *PS)
    later = probes._call(budget, *PS)

    assert (first.kind, first.reason) == ("unavailable", "orca call failed (exit 1)")
    assert (later.kind, later.reason) == ("call_failed", "orca call failed (exit 1)")


LIST_CALLS = [
    pytest.param(wl(RUN), "workers", id="worker-list"),
    pytest.param(tl_ready(RUN), "tasks", id="task-list-ready"),
    pytest.param(tl_all(RUN), "tasks", id="task-list"),
    pytest.param(PS, "worktrees", id="worktree-ps"),
]


@pytest.mark.parametrize(("argv", "key"), LIST_CALLS)
def test_empty_lists_are_accepted(patch_orca, clock, argv, key):
    patch_orca.respond(argv, {key: []})

    result = probes._call(probes.Budget(clock=clock), *argv)

    assert (result.kind, result.data, result.reason) == ("ok", {key: []}, None)


BAD_SHAPES = {
    "missing": lambda key: {},
    "null": lambda key: {key: None},
    "dict": lambda key: {key: {}},
    "string": lambda key: {key: "rows"},
}


@pytest.mark.parametrize("shape", BAD_SHAPES)
@pytest.mark.parametrize(("argv", "key"), LIST_CALLS)
def test_wrong_shape_list_reply_is_unavailable_on_call_one_and_call_failed_later(
    patch_orca, clock, argv, key, shape
):
    bad = BAD_SHAPES[shape](key)
    invalid = "orca call failed (invalid response)"

    patch_orca.respond(argv, bad)  # the first Orca call of a fresh budget
    first = probes._call(probes.Budget(clock=clock), *argv)
    assert (first.kind, first.data, first.reason) == ("unavailable", None, invalid)

    budget = probes.Budget(clock=clock)  # a later call: one good call came first
    patch_orca.respond(PS, {"worktrees": []})
    assert probes._call(budget, *PS).kind == "ok"
    patch_orca.respond(argv, bad)
    later = probes._call(budget, *argv)
    assert (later.kind, later.data, later.reason) == ("call_failed", None, invalid)


def test_worker_show_reply_has_no_list_key_and_is_accepted(patch_orca, clock):
    patch_orca.respond(ws(DISPATCH), {})

    result = probes._call(probes.Budget(clock=clock), *ws(DISPATCH))

    assert (result.kind, result.data) == ("ok", {})


def test_collect_continues_on_disk_sources_after_an_unavailable_first_call(
    sweep_root, patch_orca, patch_git, clock
):
    patch_orca.respond(
        wl(RUN1), kind="unavailable", reason="binary not found: orca-ide"
    )

    inp = _collect(sweep_root, clock)

    assert [c["args"] for c in patch_orca.calls] == [
        wl(RUN1)
    ]  # Orca reads stop at call one
    assert inp.orca_available is False
    rows = {s.name: s for s in inp.sources}
    assert rows[f"orca worker-list {RUN1}"].unscanned == "binary not found: orca-ide"
    for name in (
        f"orca task-list --ready {RUN1}",
        f"orca task-list {RUN1}",
        "orca worktree ps",
    ):
        assert rows[name].coverage == "unscanned"
        assert rows[name].unscanned == "orca unavailable"
    assert rows[f"git status {sweep_root.root.resolve()}"].coverage == "read"


@pytest.mark.parametrize(
    "failure",
    [
        pytest.param(((1, b"", b"boom\n"), "orca call failed (exit 1)"), id="exit-1"),
        pytest.param(
            ((0, b"<html>oops</html>", b""), "orca call failed (invalid response)"),
            id="malformed-zero-exit",
        ),
    ],
)
def test_a_middle_worker_show_failure_leaves_the_sweep_going(
    sweep_root, fake_run, clock, failure
):
    reply, reason = failure
    ids = _stock_captured(fake_run, [sweep_root.root])
    middle = ids[2]
    fake_run.reply(*ws(middle), code=reply[0], out=reply[1], err=reply[2])

    inp = _collect(sweep_root, clock, (RUN,))

    rows = {s.name: s for s in inp.sources}
    assert rows[f"orca worker-show {middle}"].coverage == "unscanned"
    assert rows[f"orca worker-show {middle}"].unscanned == reason
    assert all(
        rows[f"orca worker-show {d}"].coverage == "read" for d in ids if d != middle
    )
    assert inp.orca_available is True  # a failed show is call_failed, never unavailable
    assert PS in fake_run.orca_argv  # the later Orca reads still ran
    by_dispatch = {o.dispatch: o for o in inp.orca_rows}
    assert len(by_dispatch) == 5
    assert by_dispatch[middle].session_join is None
    assert all(
        o.session_join is not None for d, o in by_dispatch.items() if d != middle
    )


# ===========================================================================================
# FR-020, NFR-007: Budget
# ===========================================================================================


def test_call_timeout_is_the_smaller_of_per_call_and_the_time_left(clock):
    budget = probes.Budget(clock=clock)
    assert budget.call_timeout() == 10.0
    assert budget.cut() is False
    clock.advance(70)  # 20 s left
    assert budget.call_timeout() == 10.0
    assert budget.cut() is False
    clock.advance(10)  # 10 s left: not below the per-call limit
    assert budget.call_timeout() == 10.0
    assert budget.cut() is False
    clock.advance(5)  # 5 s left
    assert budget.call_timeout() == 5.0
    assert budget.cut() is True
    clock.advance(4.5)  # 0.5 s left: under 1 s
    assert budget.call_timeout() is None


def test_with_20_s_left_the_per_call_timeout_is_at_most_20_s(clock):
    budget = probes.Budget(per_call_s=30.0, clock=clock)
    clock.advance(70)

    timeout = budget.call_timeout()

    assert timeout == 20.0
    assert budget.cut() is True


def test_budget_reason_texts(clock):
    budget = probes.Budget(clock=clock)
    assert budget.budget_reason() == "unscanned: time budget reached (90 s)"
    assert budget.show_cap_reason() == "show cap reached (50)"


def _drain(budget: probes.Budget, run: str) -> int:
    count = 0
    while budget.take_show(run):
        count += 1
    return count


def test_share_shows_splits_evenly_and_the_remainder_goes_to_the_first_run(clock):
    budget = probes.Budget(clock=clock)
    budget.share_shows(("a", "b", "c"))

    assert [_drain(budget, r) for r in ("a", "b", "c")] == [18, 16, 16]


def test_share_shows_hands_unneeded_shows_to_the_runs_that_need_more(clock):
    budget = probes.Budget(clock=clock)
    budget.share_shows(("a", "b"), {"a": 10, "b": 60})

    assert [_drain(budget, r) for r in ("a", "b")] == [10, 40]


def test_take_show_stops_at_the_cap_without_a_share(clock):
    budget = probes.Budget(clock=clock)

    assert _drain(budget, "a") == 50
    assert budget.take_show("b") is False


def test_budget_cut_timeout_is_call_failed_never_unavailable(patch_orca, clock):
    budget = probes.Budget(clock=clock)
    clock.advance(85)  # 5 s left, so the call's timeout is cut below 10 s
    patch_orca.respond(PS, kind="unavailable", reason="timeout after 5 s")

    result = probes._call(budget, *PS)

    assert (result.kind, result.reason) == (
        "call_failed",
        "unscanned: time budget reached (90 s)",
    )
    assert patch_orca.calls[0]["timeout"] == 5.0


def test_a_timeout_that_was_not_cut_is_unavailable(patch_orca, clock):
    patch_orca.respond(PS, kind="unavailable", reason="timeout after 10 s")

    result = probes._call(probes.Budget(clock=clock), *PS)

    assert (result.kind, result.reason) == ("unavailable", "timeout after 10 s")


def test_with_20_s_left_every_orca_timeout_is_at_most_20_s(
    sweep_root, patch_orca, patch_git, clock, monkeypatch
):
    _stock_run(patch_orca, RUN1, _rows([did(1), did(2)]))
    _stock_ps(patch_orca)
    # The first call uses 70 s of the 90 s, leaving 20 s.
    _spend(
        monkeypatch,
        patch_orca,
        clock,
        lambda timeout, args: 70.0 if len(patch_orca.calls) == 1 else 0.0,
    )

    _collect(sweep_root, clock, per_call_s=30.0)

    timeouts = [c["timeout"] for c in patch_orca.calls]
    assert timeouts[0] == 30.0
    assert all(t <= 20.0 for t in timeouts[1:])
    assert timeouts[1] == 20.0


def test_60_rows_give_50_worker_show_and_bound_reached_10(
    sweep_root, patch_orca, patch_git, clock
):
    ids = [did(i) for i in range(60)]
    _stock_run(patch_orca, RUN1, _rows(ids))
    _stock_ps(patch_orca)

    inp = _collect(sweep_root, clock)

    shows = [c["args"] for c in patch_orca.calls if c["args"][1] == "worker-show"]
    assert len(shows) == 50
    assert len(inp.orca_rows) == 60  # a row the cap cut keeps its identity
    cut = [s for s in inp.sources if s.unscanned == "show cap reached (50)"]
    assert len(cut) == 10
    result = classify_all(inp, _ctx(sweep_root.root, (RUN1,)))
    assert result.summary["bound_reached"] == 10


def test_50_rows_give_50_worker_show_and_bound_reached_0(
    sweep_root, patch_orca, patch_git, clock
):
    ids = [did(i) for i in range(50)]
    _stock_run(patch_orca, RUN1, _rows(ids))
    _stock_ps(patch_orca)

    inp = _collect(sweep_root, clock)

    shows = [c["args"] for c in patch_orca.calls if c["args"][1] == "worker-show"]
    assert len(shows) == 50
    result = classify_all(inp, _ctx(sweep_root.root, (RUN1,)))
    assert result.summary["bound_reached"] == 0


def test_two_runs_of_40_rows_get_25_shows_each(
    sweep_root, patch_orca, patch_git, clock
):
    first = [did(i) for i in range(40)]
    second = [did(0x100 + i) for i in range(40)]
    _stock_run(patch_orca, RUN1, _rows(first))
    _stock_run(patch_orca, RUN2, _rows(second))
    _stock_ps(patch_orca)

    inp = _collect(sweep_root, clock, (RUN1, RUN2))

    shown = [c["args"][3] for c in patch_orca.calls if c["args"][1] == "worker-show"]
    assert len([d for d in shown if d in first]) == 25
    assert len([d for d in shown if d in second]) == 25
    result = classify_all(inp, _ctx(sweep_root.root, (RUN1, RUN2)))
    assert result.summary["bound_reached"] == 30


def test_full_timeout_fakes_finish_under_120_s_and_still_render(
    sweep_root, patch_orca, patch_git, clock, monkeypatch
):
    runs = (RUN1, RUN2, RUN3)
    for n, run in enumerate(runs, start=1):
        _stock_run(patch_orca, run, _rows([did(10 * n), did(10 * n + 1)]))
    _stock_ps(patch_orca)
    start = clock.now
    _spend(
        monkeypatch, patch_orca, clock, lambda timeout, args: timeout
    )  # every call takes its full timeout

    inp = _collect(sweep_root, clock, runs)

    elapsed = clock.now - start
    assert elapsed == 90.0 and elapsed < 120
    assert (
        len(patch_orca.calls) == 9
    )  # nine list calls use the 90 s; nothing starts after
    assert inp.orca_available is True  # a budget cut is never an outage
    rows = {s.name: s for s in inp.sources}
    assert rows[f"orca worker-show {did(10)}"].unscanned == "time budget reached (90 s)"
    assert (
        rows[f"git status {sweep_root.root.resolve()}"].unscanned
        == "time budget reached (90 s)"
    )
    assert len(inp.orca_rows) == 6  # every row keeps its identity
    ctx = _ctx(sweep_root.root, runs)
    text = report.render(
        classify_all(inp, ctx), ctx
    )  # the sweep still renders its report (publication is not exercised here)
    assert "time budget reached" in text


def test_every_call_timing_out_still_collects_and_renders(sweep_root, fake_run, clock):
    def hang(argv, kwargs):
        clock.advance(kwargs["timeout"])  # the call uses its whole timeout
        raise subprocess.TimeoutExpired(argv, kwargs["timeout"])

    fake_run.default = hang
    fake_run.git = hang
    start = clock.now

    inp = _collect(sweep_root, clock)

    assert clock.now - start < 120
    assert inp.orca_available is False
    assert fake_run.orca_argv == [
        wl(RUN1)
    ]  # a timeout on call one is unavailable and stops Orca reads
    ctx = _ctx(sweep_root.root)
    assert report.render(classify_all(inp, ctx), ctx)


# ===========================================================================================
# FR-010 inputs: the collect source rows and truncated
# ===========================================================================================


def test_collect_worker_list_source_rows_and_truncated(
    sweep_root, patch_orca, patch_git, clock, monkeypatch
):
    # The row names start with the literal word ``orca``, not ``$ORCA_CLI_COMMAND``.
    monkeypatch.setenv("ORCA_CLI_COMMAND", "/opt/custom/orca-x")

    # R1 worker-list ok, R2 worker-list call_failed (it is not Orca call one).
    _stock_run(patch_orca, RUN1, [])
    _stock_run(patch_orca, RUN2, [])
    patch_orca.respond(wl(RUN2), kind="call_failed", reason="orca call failed (exit 1)")
    _stock_ps(patch_orca)
    inp = _collect(sweep_root, clock, (RUN1, RUN2))
    rows = {s.name: s for s in inp.sources}
    names = [s.name for s in inp.sources if s.name.startswith("orca worker-list")]
    assert names == [f"orca worker-list {RUN1}", f"orca worker-list {RUN2}"]
    assert rows[f"orca worker-list {RUN1}"].unscanned is None
    assert rows[f"orca worker-list {RUN2}"].unscanned == "orca call failed (exit 1)"
    assert inp.orca_available is True

    # A failed ``task-list --run R2`` marks ``orca task-list R2`` and not its worker-list row.
    patch_orca.calls.clear()
    _stock_run(patch_orca, RUN2, [])
    patch_orca.respond(
        tl_all(RUN2), kind="call_failed", reason="orca call failed (exit 1)"
    )
    inp = _collect(sweep_root, clock, (RUN1, RUN2))
    rows = {s.name: s for s in inp.sources}
    assert rows[f"orca task-list {RUN2}"].unscanned == "orca call failed (exit 1)"
    assert rows[f"orca worker-list {RUN2}"].unscanned is None
    assert rows[f"orca task-list {RUN1}"].unscanned is None

    # A full page of 100 rows sets truncated; 99 rows leave it False.
    for count, expected in ((100, True), (99, False)):
        patch_orca.calls.clear()
        _stock_run(patch_orca, RUN1, _rows([did(i) for i in range(count)]))
        inp = _collect(sweep_root, clock)
        assert inp.truncated is expected, count


def test_collect_worker_list_source_rows_budget_spent_before_r2(
    sweep_root, patch_orca, patch_git, clock, monkeypatch
):
    _stock_run(patch_orca, RUN1, [])
    _stock_run(patch_orca, RUN2, [])
    _stock_ps(patch_orca)
    # The last R1 call (``task-list --run R1``) uses the whole budget.
    _spend(
        monkeypatch,
        patch_orca,
        clock,
        lambda timeout, args: (
            90.0 if args[1] == "task-list" and "--ready" not in args else 0.0
        ),
    )

    inp = _collect(sweep_root, clock, (RUN1, RUN2))

    assert [c for c in patch_orca.calls if RUN2 in c["args"]] == []  # no argv for R2
    row = next(s for s in inp.sources if s.name == f"orca worker-list {RUN2}")
    assert row.coverage == "unscanned"
    assert f"unscanned: {row.unscanned}" == "unscanned: time budget reached (90 s)"
    assert inp.orca_available is True


@pytest.mark.parametrize("state", ["missing", "empty", "unreadable"])
def test_collect_worker_list_source_rows_orca_tabs(
    sweep_root, patch_orca, patch_git, clock, monkeypatch, state
):
    _stock_run(patch_orca, RUN1, [])
    _stock_ps(patch_orca)
    if state != "missing":
        sweep_root.tabs.mkdir(parents=True)
    if state == "unreadable":
        real_scandir = os.scandir

        def scandir(path="."):
            if str(path) == str(sweep_root.tabs):
                raise PermissionError(13, "Permission denied", str(path))
            return real_scandir(path)

        monkeypatch.setattr(probes.os, "scandir", scandir)

    inp = _collect(sweep_root, clock)

    row = next(s for s in inp.sources if s.name == "ccsession orca-tabs")
    if state == "unreadable":
        assert (row.coverage, row.unscanned) == (
            "unscanned",
            "tab map folder not readable",
        )
    else:  # a missing folder and an empty readable one are readable and empty
        assert (row.coverage, row.unscanned) == ("0 entries", None)


# ===========================================================================================
# FR-020: byte limits, the nine boundary fixtures
# ===========================================================================================

BOUNDARY = [
    pytest.param(-1, True, id="limit-minus-1"),
    pytest.param(0, True, id="at-the-limit"),
    pytest.param(1, False, id="limit-plus-1"),
]


def test_byte_limits_are_pinned():
    assert probes.CONTRACT_LIMIT == MIB
    assert probes.LEDGER_LIMIT == MIB
    assert probes.LEDGER_SPLIT == 512 * KIB
    assert probes.TRANSCRIPT_TAIL == 256 * KIB
    assert probes.OUTPUT_LIMIT == 8 * MIB
    assert probes.WORKER_LIST_PAGE == 100


def _contract_bytes(size: int) -> bytes:
    head = b'worker_contract_version: "1"\nworker_status: "succeeded"\n'
    data = head + b"#" * (size - len(head) - 1) + b"\n"
    assert len(data) == size
    return data


@pytest.mark.parametrize(("delta", "readable"), BOUNDARY)
def test_contract_size_boundary(sweep_root, delta, readable):
    path = sweep_root.contract(text=_contract_bytes(MIB + delta))

    record = probes.read_contract(path, sweep_root.root)

    if readable:
        assert record is not None
        assert record.worker_status == "succeeded"
    else:
        assert record is None  # the limit is hit only when the size is over it


def _ledger_bytes(size: int, final: str) -> bytes:
    line = b"FINAL: all tasks complete\n"
    filler = b"x" * (size - len(line) - 1) + b"\n"
    data = line + filler if final == "start" else filler + line
    assert len(data) == size
    return data


@pytest.mark.parametrize(("delta", "found"), BOUNDARY)
def test_ledger_size_boundary(sweep_root, delta, found):
    # FINAL sits at the very start: found while the whole file is read, lost once only the
    # tail is searched (size over the limit).
    folder = sweep_root.package("pkg", ledger=_ledger_bytes(MIB + delta, "start"))

    assert probes.read_ledger(folder / "progress.md", sweep_root.root) is found


def test_ledger_over_the_limit_is_read_as_head_and_tail(sweep_root):
    folder = sweep_root.package("pkg", ledger=_ledger_bytes(MIB + 1, "end"))

    assert probes.read_ledger(folder / "progress.md", sweep_root.root) is True
    (record,) = probes.read_packages(sweep_root.root)
    assert record.has_final_line is True


def test_ledger_tail_drops_a_first_line_that_the_cut_split(sweep_root):
    size = MIB + 1
    cut = (
        size - 512 * KIB
    )  # the tail starts exactly at "FINAL: x", the end of a longer line
    head = b"a" * cut + b"FINAL: x\n"
    data = head + b"b" * (size - len(head) - 1) + b"\n"
    assert len(data) == size
    folder = sweep_root.package("pkg", ledger=data)

    assert probes.read_ledger(folder / "progress.md", sweep_root.root) is False


def test_a_contract_over_1_mib_is_unscanned_with_a_reason(
    sweep_root, patch_orca, patch_git, clock
):
    path = sweep_root.contract(text=_contract_bytes(MIB + 1))
    _stock_contract_run(patch_orca, path)

    inp = _collect(sweep_root, clock)

    row = next(s for s in inp.sources if s.name == f"contract {did(1)}")
    assert (row.coverage, row.unscanned) == ("unscanned", "over 1 MiB")
    assert inp.contracts == ()


def test_contract_mtime_and_source_age_come_from_the_file_time(
    sweep_root, patch_orca, patch_git, clock, monkeypatch
):
    # TST-F5 (SP-15): the Waiting (a) Age is computed from ``ContractRecord.mtime``, so the
    # file time read from disk and the age of the ``contract <dispatch>`` source row are
    # asserted from a real file whose time is set to exactly one hour before ``now``.
    path = sweep_root.contract()
    stamp = (NOW - timedelta(hours=1)).timestamp()
    os.utime(path, (stamp, stamp))
    monkeypatch.setattr(probes, "_utcnow", lambda: NOW)  # ``collect`` reads this clock
    _stock_contract_run(patch_orca, path)

    record = probes.read_contract(path, sweep_root.root)
    inp = _collect(sweep_root, clock)

    assert record is not None
    assert record.mtime == NOW - timedelta(hours=1)
    assert record.mtime.tzinfo is not None
    row = next(s for s in inp.sources if s.name == f"contract {did(1)}")
    assert (row.coverage, row.age_seconds) == ("read", 3600)
    (collected,) = inp.contracts
    assert collected.mtime == NOW - timedelta(hours=1)


def _record(ts: str, session: str = "s1", pad: int = 0) -> bytes:
    fields = {"type": "user", "timestamp": ts, "sessionId": session, "pad": "x" * pad}
    return (json.dumps(fields) + "\n").encode("utf-8")


def _transcript_bytes(size: int) -> bytes:
    """A transcript of exactly ``size`` bytes: record A at 07:00:00Z, then B at 08:00:00Z."""
    first = _record("2026-11-08T07:00:00Z")
    last = _record("2026-11-08T08:00:00Z")
    data = first + _record("2026-11-08T08:00:00Z", pad=size - len(first) - len(last))
    assert len(data) == size
    return data


@pytest.mark.parametrize(("delta", "complete"), BOUNDARY)
def test_transcript_tail_boundary(sweep_root, delta, complete):
    path = sweep_root.transcript(raw=_transcript_bytes(256 * KIB + delta))

    tail = probes.read_transcript_tail(path)

    assert tail.readable is True
    assert tail.tail_complete is complete
    assert tail.last_record_ts == datetime(2026, 11, 8, 8, 0, 0, tzinfo=UTC)
    expected_first = (
        7 if complete else 8
    )  # over the limit the first partial record is dropped
    assert tail.first_record_ts == datetime(
        2026, 11, 8, expected_first, 0, 0, tzinfo=UTC
    )


def _orca_stdout(size: int) -> tuple[bytes, bytes]:
    """A valid ok reply padded so that stdout plus a 10-byte stderr total ``size`` bytes."""
    body = _envelope({"worktrees": []})
    err = b"0123456789"
    return body + b" " * (size - len(err) - len(body)), err


@pytest.mark.parametrize(("delta", "ok"), BOUNDARY)
def test_subprocess_output_boundary_for_orca(fake_run, delta, ok):
    out, err = _orca_stdout(8 * MIB + delta)
    fake_run.reply(*PS, out=out, err=err)

    result = probes._orca(*PS, timeout=5.0)

    if ok:
        assert (result.kind, result.data) == ("ok", {"worktrees": []})
    else:
        assert (result.kind, result.data, result.reason) == (
            "call_failed",
            None,
            "output over 8 MiB",
        )


@pytest.mark.parametrize(("delta", "ok"), BOUNDARY)
def test_subprocess_output_boundary_for_git(fake_run, delta, ok):
    size = 8 * MIB + delta
    fake_run.git = (0, b"x" * (size - 10), b"0123456789")

    if ok:
        assert (
            len(probes._git(Path("/work/tree-a"), *GIT_STATUS, timeout=5.0))
            == size - 10
        )
    else:
        with pytest.raises(probes.GitCallFailed) as exc:
            probes._git(Path("/work/tree-a"), *GIT_STATUS, timeout=5.0)
        assert str(exc.value) == f"output over {8 * MIB} bytes"


# ===========================================================================================
# SPEC section 11 failure modes (DESIGN 7.2 observation rules)
# ===========================================================================================


def _stock_contract_run(orca, contract: Path, run: str = RUN1) -> None:
    """One worker whose Task spec names ``contract``; its text is how collect finds the file."""
    _stock_run(
        orca,
        run,
        _rows([did(1)]),
        tasks=[{"id": "task_0", "spec": f"Write the contract to {contract}"}],
    )
    _stock_ps(orca)


@pytest.mark.parametrize("how", ["stat-fails", "git-fails"])
def test_worktree_removed_between_the_seams_is_unscanned_and_the_others_continue(
    sweep_root, patch_orca, patch_git, clock, monkeypatch, how
):
    gone = sweep_root.worktree("gone")
    keep = sweep_root.worktree("keep")
    _stock_run(patch_orca, RUN1, [])
    _stock_ps(patch_orca, [gone, keep])
    fake = patch_orca

    def removed_after_ps(*args, timeout):
        result = fake(*args, timeout=timeout)
        if args == PS and how == "stat-fails":
            shutil.rmtree(gone)  # gone after Orca named it, before git or stat reads it
        return result

    monkeypatch.setattr(probes, "_orca", removed_after_ps)
    if how == "git-fails":
        patch_git.respond(
            gone.resolve(), probes.GitCallFailed("git exited 128: not a repository")
        )

    inp = _collect(sweep_root, clock)

    rows = {s.name: s for s in inp.sources}
    gone_row = rows[f"git status {gone.resolve()}"]
    assert (gone_row.coverage, gone_row.unscanned) == (
        "unscanned",
        "worktree not readable",
    )
    for ok_path in (keep.resolve(), sweep_root.root.resolve()):
        assert rows[f"git status {ok_path}"].coverage == "read"
    states = {w.path: w for w in inp.worktrees}
    assert states[str(gone.resolve())].status_read is False
    assert states[str(keep.resolve())].status_read is True


def test_list_and_show_disagree_and_the_show_value_is_used():
    list_row = {
        "dispatchId": DISPATCH,
        "dispatchStatus": "dispatched",
        "terminalState": "live",
        "projection": {
            "parent": "ctx_aaaaaaaaaaaa",
            "resource": {"terminalState": "live"},
            "nextAction": {"kind": "wait"},
        },
    }
    show = {
        "dispatch": {"id": DISPATCH, "status": "completed"},
        "projection": {
            "parent": "ctx_bbbbbbbbbbbb",
            "resource": {"terminalState": "released"},
            "nextAction": {"kind": "none"},
        },
    }

    obs = probes.parse_worker_show(RUN, list_row, show)

    assert obs.status == "completed"
    assert obs.dispatch_status == "completed"
    assert obs.parent == "ctx_bbbbbbbbbbbb"
    assert obs.terminal_state == "released"
    assert obs.next_action == "none"


def test_a_list_row_with_no_show_keeps_the_show_only_fields_unknown():
    list_row = {"dispatchId": DISPATCH, "dispatchStatus": "dispatched"}

    obs = probes.parse_worker_show(RUN, list_row, None)

    assert obs.dispatch == DISPATCH
    assert obs.status is None and obs.dispatch_status is None
    assert obs.liveness_verdict is None
    assert obs.session_join is None
    assert obs.dispatch_started is None and obs.dispatch_ended is None
    assert obs.agent_wait_present is False


def test_parse_worker_show_reads_no_agent_wait_field_until_its_names_are_captured():
    # Open item 6: no live ``agentWait`` name was captured, so nothing is read from either
    # place it might sit, and no wait time is guessed from any key (FIN-F1).
    wait = {"since": "2026-11-08T10:00:00Z", "kind": "question"}
    show = {
        "dispatch": {"id": DISPATCH, "status": "dispatched"},
        "projection": {"agentWait": wait},
        "agentWait": wait,
    }

    obs = probes.parse_worker_show(RUN, {"dispatchId": DISPATCH}, show)

    assert obs.agent_wait is None
    assert obs.agent_wait_present is False
    assert obs.agent_wait_since is None


def test_one_missing_and_one_extra_worker_show_key_raise_nothing():
    list_row = {"dispatchId": DISPATCH}
    result = _captured("captured-worker-show-1.json")["result"]
    base = probes.parse_worker_show(RUN, list_row, result)
    assert base.liveness_verdict == "exited"

    missing = json.loads(json.dumps(result))
    del missing["projection"]["liveness"]  # one missing key
    obs = probes.parse_worker_show(RUN, list_row, missing)
    assert obs.liveness_verdict is None
    assert obs == replace(
        base, liveness_verdict=None
    )  # every other field is read as before

    extra = json.loads(json.dumps(result))
    extra["brandNewKey"] = {"anything": [1, 2]}  # one extra key
    extra["dispatch"]["brandNewField"] = "x"
    assert probes.parse_worker_show(RUN, list_row, extra) == base


@pytest.mark.parametrize(
    "show", [{}, [], "text", 5, {"dispatch": "x"}, {"projection": []}]
)
def test_a_show_of_the_wrong_shape_raises_nothing(show):
    obs = probes.parse_worker_show(RUN, {"dispatchId": DISPATCH}, show)

    assert obs.dispatch == DISPATCH
    assert obs.status is None


def test_relative_report_dir_resolves_against_the_worker_worktree():
    # The WC-16 worked example names a relative folder.
    text = "run it with --report-dir .dev/tdd/auth-1/ and report back"
    named = probes.OrcaObservation(
        run=RUN1, dispatch=did(1), worktree_path="/w1", task_spec_text=text
    )
    assert probes._contract_candidates(named) == (
        Path("/w1/.dev/tdd/auth-1/return-contract.yaml"),
    )
    # With no worktree path a relative folder names nothing.
    unplaced = probes.OrcaObservation(run=RUN1, dispatch=did(1), task_spec_text=text)
    assert probes._contract_candidates(unplaced) == ()
    # An absolute folder is read as before.
    absolute = probes.OrcaObservation(
        run=RUN1,
        dispatch=did(1),
        worktree_path="/w1",
        task_spec_text="--report-dir /r/x/",
    )
    assert probes._contract_candidates(absolute) == (Path("/r/x/return-contract.yaml"),)


@pytest.mark.parametrize(
    "text, folder",
    [
        ('--report-dir "/tmp/my project/reports"', "/tmp/my project/reports"),
        ("--output-dir='/tmp/my project/r/'", "/tmp/my project/r"),
        ('--report-dir "rel dir/x"', "/w1/rel dir/x"),
        ("--report-dir /tmp/plain/", "/tmp/plain"),
    ],
)
def test_quoted_report_dir_is_taken_whole_with_its_spaces(text, folder):
    # A quoted path with spaces is one argument, not a path cut at the first space.
    obs = probes.OrcaObservation(
        run=RUN1, dispatch=did(1), worktree_path="/w1", task_spec_text=text
    )
    assert probes._contract_candidates(obs) == (Path(folder) / "return-contract.yaml",)


def test_symlink_out_contract_is_outside_root(
    sweep_root, patch_orca, patch_git, clock, tmp_path
):
    outside = tmp_path / "outside" / "return-contract.yaml"
    outside.parent.mkdir()
    outside.write_text('worker_contract_version: "1"\n', encoding="utf-8")
    link = sweep_root.root / ".dev" / "reports" / "run" / "return-contract.yaml"
    link.parent.mkdir(parents=True)
    link.symlink_to(outside)
    assert probes.read_contract(link, sweep_root.root) is None
    _stock_contract_run(patch_orca, link)

    inp = _collect(sweep_root, clock)

    row = next(s for s in inp.sources if s.name == f"contract {did(1)}")
    assert (row.coverage, row.unscanned) == ("unscanned", "outside root")
    assert inp.contracts == ()


def test_symlink_out_ledger_is_outside_root(
    sweep_root, patch_orca, patch_git, clock, tmp_path
):
    outside = tmp_path / "outside-progress.md"
    outside.write_text("FINAL: all tasks complete\n", encoding="utf-8")
    folder = sweep_root.package("pkg", ledger=None)
    ledger = folder / "progress.md"
    ledger.symlink_to(outside)
    assert probes.read_ledger(ledger, sweep_root.root) is None
    _stock_run(patch_orca, RUN1, [])
    _stock_ps(patch_orca)

    inp = _collect(sweep_root, clock)

    row = next(s for s in inp.sources if s.name == f"package ledger {ledger}")
    assert (row.coverage, row.unscanned) == ("unscanned", "outside root")


def test_symlink_out_transcript_is_outside_root(
    sweep_root, patch_orca, patch_git, clock, tmp_path
):
    outside = tmp_path / "outside.jsonl"
    outside.write_bytes(_record("2026-11-08T07:00:00Z"))
    path = sweep_root.transcript(stamps=("2026-11-08T07:00:00Z",))
    path.unlink()
    path.symlink_to(outside)
    tail = probes.read_transcript_tail(path, path.parent)
    assert tail.readable is False
    _stock_run(patch_orca, RUN1, [])
    _stock_ps(patch_orca)

    inp = _collect(sweep_root, clock)

    row = next(s for s in inp.sources if s.name == f"transcript {path}")
    assert (row.coverage, row.unscanned) == ("unscanned", "outside root")
    assert all(not t.readable for t in inp.transcripts)


def test_symlink_out_tab_map_entry_is_outside_root(
    sweep_root, patch_orca, patch_git, clock, tmp_path
):
    outside = tmp_path / "outside-entry"
    outside.write_text("session\n/work\nterm_handle\n", encoding="utf-8")
    sweep_root.tabs.mkdir(parents=True)
    (sweep_root.tabs / "tab1+leaf1").symlink_to(outside)
    assert probes.read_tab_map(sweep_root.state) == ()
    _stock_run(patch_orca, RUN1, [])
    _stock_ps(patch_orca)

    inp = _collect(sweep_root, clock)

    row = next(s for s in inp.sources if s.name == "ccsession orca-tabs")
    assert (row.coverage, row.unscanned) == ("unscanned", "outside root")
    assert inp.tab_map == ()


def _change_on_read(monkeypatch, target: Path, change) -> list[int]:
    """Patch ``Path.read_bytes`` so ``change(n)`` rewrites ``target`` after its n-th read."""
    real = Path.read_bytes
    reads: list[int] = []

    def read_bytes(self):
        data = real(self)
        if self == target:
            reads.append(1)
            change(len(reads))
        return data

    monkeypatch.setattr(Path, "read_bytes", read_bytes)
    return reads


def test_a_contract_changed_between_two_reads_is_re_read_once(sweep_root, monkeypatch):
    path = sweep_root.contract(worker_status="running")
    settled = path.read_bytes().replace(b"running", b"succeeded")

    def change(n: int) -> None:
        if n == 1:
            path.write_bytes(settled)  # a second writer finishes the contract mid-read

    reads = _change_on_read(monkeypatch, path, change)

    record = probes.read_contract(path, sweep_root.root)

    assert len(reads) == 2  # one read and exactly one re-read
    assert record is not None
    assert record.worker_status == "succeeded"  # the re-read value, not the first read


def test_a_contract_that_changes_on_every_read_is_an_inconsistent_observation(
    sweep_root, patch_orca, patch_git, clock, monkeypatch
):
    path = sweep_root.contract(worker_status="running")

    def change(n: int) -> None:
        with open(path, "ab") as handle:
            handle.write(b"# edit %d\n" % n)

    reads = _change_on_read(monkeypatch, path, change)
    assert probes.read_contract(path, sweep_root.root) is None
    assert len(reads) == 2  # the re-read also saw a change, so there is no third read

    _stock_contract_run(patch_orca, path)
    inp = _collect(sweep_root, clock)

    row = next(s for s in inp.sources if s.name == f"contract {did(1)}")
    assert (row.coverage, row.unscanned) == (
        "unscanned",
        "conflict: inconsistent observation",
    )
    assert inp.contracts == ()


@pytest.mark.parametrize(
    "text, field, expected",
    [
        pytest.param(  # a trailing comment is not part of the value
            "worker_status: blocked  # waiting on owner\n",
            "worker_status",
            "blocked",
            id="trailing-comment",
        ),
        pytest.param(  # a plain scalar continued on an indented line is one value
            "blocked_question: first line\n  second line\n",
            "blocked_question",
            "first line second line",
            id="continued-plain-scalar",
        ),
        pytest.param(  # a quoted flow item may hold a comma
            'artifacts: [a.md, "b, c.md"]\nworker_status: succeeded\n',
            "artifacts",
            (Path("a.md"), Path("b, c.md")),
            id="quoted-flow-item-with-comma",
        ),
        pytest.param(  # a flow list followed by a comment still parses as a list
            "artifacts: [a.md, b.md]   # the outputs\n",
            "artifacts",
            (Path("a.md"), Path("b.md")),
            id="flow-list-with-comment",
        ),
        pytest.param(  # invalid YAML is a record with no fields, never an error
            "worker_status: [unclosed\n", "worker_status", None, id="invalid-yaml"
        ),
        pytest.param(  # a document that is not a mapping carries no fields
            "- worker_status\n- blocked\n", "worker_status", None, id="not-a-mapping"
        ),
        pytest.param(  # too deeply nested for the parser: still no error
            "[" * 5000, "worker_status", None, id="nested-too-deep"
        ),
        pytest.param(  # a scalar the loader rejects raises ValueError, not YAMLError
            "worker_status: blocked\nreason: 2026-13-45\n",
            "worker_status",
            None,
            id="rejected-date-scalar",
        ),
    ],
)
def test_contract_fields_are_read_by_yaml_safe_load(sweep_root, text, field, expected):
    path = sweep_root.contract(text=text)

    record = probes.read_contract(path, sweep_root.root)

    assert record is not None
    if field == "artifacts":
        assert record.artifacts == expected
    else:
        assert getattr(record, field) == expected


@pytest.mark.parametrize("budget_spent", [False, True], ids=["budget-left", "spent"])
def test_a_changed_contract_is_re_read_only_while_the_budget_allows(
    sweep_root, patch_orca, patch_git, clock, monkeypatch, budget_spent
):
    # NFR-007 (DESIGN 7.2): one re-read of a changed input only while the budget allows;
    # with no budget left the row is a conflict after one read (FIN-F8).
    path = sweep_root.contract(worker_status="running")
    settled = path.read_bytes().replace(b"running", b"succeeded")

    def change(n: int) -> None:
        if n == 1:
            path.write_bytes(settled)  # a second writer finishes the contract mid-read
            if budget_spent:
                clock.advance(1000.0)  # the 90 s total is gone before the re-read

    reads = _change_on_read(monkeypatch, path, change)
    _stock_contract_run(patch_orca, path)

    inp = _collect(sweep_root, clock)

    row = next(s for s in inp.sources if s.name == f"contract {did(1)}")
    if budget_spent:
        assert len(reads) == 1  # no re-read
        assert (row.coverage, row.unscanned) == (
            "unscanned",
            "conflict: inconsistent observation",
        )
        assert inp.contracts == ()
    else:
        assert len(reads) == 2  # one read and one re-read
        assert (row.coverage, row.unscanned) == ("read", None)
        assert [c.worker_status for c in inp.contracts] == ["succeeded"]


def test_duplicate_dispatch_rows_with_two_states_give_one_conflict_row(
    sweep_root, patch_orca, patch_git, clock
):
    rows = [
        {"dispatchId": did(1), "taskId": "task_0", "dispatchStatus": "completed"},
        {"dispatchId": did(1), "taskId": "task_0", "dispatchStatus": "dispatched"},
    ]
    _stock_run(patch_orca, RUN1, rows)
    _stock_ps(patch_orca)

    inp = _collect(sweep_root, clock)
    result = classify_all(inp, _ctx(sweep_root.root, (RUN1,)))

    assert [
        a for a in (c["args"] for c in patch_orca.calls) if a[1] == "worker-show"
    ] == []
    ids = [c.row.row_id for c in result.rows if c.row.row_id.startswith("orca:")]
    assert ids == [f"orca:{did(1)}"]
    merged = result.rows[0]
    assert merged.classification.class_name == "could not determine"
    assert merged.classification.rule == "fallback"
    assert "conflict: duplicate Dispatch rows disagree" in merged.classification.notes


# ===========================================================================================
# M7: parse_status and read_worktree
# ===========================================================================================

STATUS_HEADERS = [
    pytest.param("## main...origin/main [ahead 3]", 3, True, "ahead 3", id="ahead-3"),
    pytest.param(
        "## main...origin/main [ahead 2, behind 1]",
        2,
        True,
        "ahead 2",
        id="ahead-and-behind",
    ),
    pytest.param("## main...origin/main", 0, True, None, id="upstream-no-ahead"),
    pytest.param(
        "## main...origin/main [behind 2]", 0, True, None, id="upstream-behind-only"
    ),
    pytest.param("## main", None, False, "no upstream", id="no-upstream"),
    pytest.param(
        "## main...origin/main [gone]", None, None, "upstream gone", id="upstream-gone"
    ),
    pytest.param(
        "## HEAD (no branch)", None, None, "detached HEAD", id="detached-head"
    ),
    pytest.param(
        "## No commits yet on main", None, None, "no commits yet", id="no-commits-yet"
    ),
]


@pytest.mark.parametrize(("header", "ahead", "has_upstream", "note"), STATUS_HEADERS)
def test_parse_status_branch_header(header, ahead, has_upstream, note):
    parsed = probes.parse_status(header + "\0")

    assert parsed.branch_header == header[3:]
    assert (parsed.ahead, parsed.has_upstream, parsed.header_note) == (
        ahead,
        has_upstream,
        note,
    )
    assert parsed.entries == ()


UNPUSHED = {
    "ahead-3": True,
    "ahead-and-behind": True,
    "upstream-no-ahead": False,
    "upstream-behind-only": False,
    "no-upstream": None,
    "upstream-gone": None,
    "detached-head": None,
    "no-commits-yet": None,
}


@pytest.mark.parametrize(("header", "ahead", "has_upstream", "note"), STATUS_HEADERS)
def test_read_worktree_unpushed_follows_the_branch_header(
    sweep_root, patch_git, clock, request, header, ahead, has_upstream, note
):
    case = request.node.callspec.id
    patch_git.respond(sweep_root.root, header + "\0")

    state, row = probes.read_worktree(sweep_root.root, probes.Budget(clock=clock))

    assert row.coverage == "read"
    assert state.status_read is True
    assert state.upstream_note == note
    if case in UNPUSHED:
        assert state.unpushed is UNPUSHED[case]
    assert state.uncommitted is False


def test_parse_status_rename_pair_in_z_form():
    raw = (
        "## main\0R  new name.txt\0old name.txt\0 M other.py\0C  copy.txt\0source.txt\0"
    )

    parsed = probes.parse_status(raw)

    assert parsed.entries == (
        ("R ", "new name.txt"),
        ("R ", "old name.txt"),
        (" M", "other.py"),
        ("C ", "copy.txt"),
        ("C ", "source.txt"),
    )


def test_parse_status_untracked_path_under_dev_tasks():
    path = ".dev/tasks/to-do/pkg/progress.md"

    parsed = probes.parse_status(f"## main\0?? {path}\0")

    assert parsed.entries == (("??", path),)


def test_read_worktree_untracked_dev_tasks_path_is_unsaved_and_marks_the_package_active(
    sweep_root, patch_git, clock
):
    sweep_root.package("pkg", ledger="")
    path = ".dev/tasks/to-do/pkg/progress.md"
    patch_git.respond(sweep_root.root, f"## main...origin/main\0?? {path}\0")

    state, _ = probes.read_worktree(sweep_root.root, probes.Budget(clock=clock))

    assert state.dev_tasks_unsaved is True
    assert state.uncommitted is True
    assert state.changed_paths == (path,)
    (package,) = state.packages
    assert package.id == "pkg"
    assert package.active is True


# ===========================================================================================
# R3-B1 (FR-010): the path-B time fields
# ===========================================================================================


def test_read_transcript_tail_sets_first_and_last_record_ts(sweep_root):
    path = sweep_root.transcript(
        stamps=(
            "2026-11-08T07:00:01Z",
            "2026-11-08T07:00:05Z",
            "2026-11-08T07:00:09Z",
        )
    )

    tail = probes.read_transcript_tail(path)

    assert tail.first_record_ts == datetime(2026, 11, 8, 7, 0, 1, tzinfo=UTC)
    assert tail.last_record_ts == datetime(2026, 11, 8, 7, 0, 9, tzinfo=UTC)
    assert tail.first_record_ts.tzinfo is not None
    assert tail.last_record_ts.tzinfo is not None
    assert tail.session_id == "session-0001"
    assert tail.tail_complete is True


def test_read_transcript_tail_first_record_ts_is_minimum(sweep_root):
    path = sweep_root.transcript(
        stamps=(
            "2026-11-08T07:00:05Z",
            "2026-11-08T07:00:01Z",
            "2026-11-08T07:00:09Z",
        )
    )

    tail = probes.read_transcript_tail(path)

    assert tail.first_record_ts == datetime(2026, 11, 8, 7, 0, 1, tzinfo=UTC)


def test_read_transcript_tail_first_record_ts_over_256k(sweep_root):
    # Record A (07:00:00Z) is 100 KiB and holds the byte where the tail starts, so it is
    # dropped. The first complete tail record is B at 08:00:00Z.
    raw = (
        _record("2026-11-08T07:00:00Z", pad=100 * KIB)
        + _record("2026-11-08T08:00:00Z")
        + _record("2026-11-08T08:00:30Z", pad=200 * KIB)
    )
    assert len(raw) > 256 * KIB
    path = sweep_root.transcript(raw=raw)

    tail = probes.read_transcript_tail(path)

    assert tail.first_record_ts == datetime(2026, 11, 8, 8, 0, 0, tzinfo=UTC)
    assert tail.last_record_ts == datetime(2026, 11, 8, 8, 0, 30, tzinfo=UTC)
    assert tail.tail_complete is False


def test_worker_show_dispatch_times_sqlite_form():
    show = {
        "dispatch": {
            "id": DISPATCH,
            "dispatchedAt": "2026-11-08 07:00:00",
            "completedAt": None,
            "status": "dispatched",
        }
    }

    obs = probes.parse_worker_show(RUN, {"dispatchId": DISPATCH}, show)

    assert obs.dispatch_started == datetime(2026, 11, 8, 7, 0, 0, tzinfo=UTC)
    assert obs.dispatch_started.tzinfo is not None
    assert obs.dispatch_ended is None
    assert obs.dispatch_status == "dispatched"


def test_worker_show_dispatch_times_iso_z_form():
    show = {
        "dispatch": {
            "id": DISPATCH,
            "dispatchedAt": "2026-11-08T07:00:00.123Z",
            "completedAt": "2026-11-08T08:00:00Z",
            "status": "completed",
        }
    }

    obs = probes.parse_worker_show(RUN, {"dispatchId": DISPATCH}, show)

    assert obs.dispatch_started == datetime(2026, 11, 8, 7, 0, 0, 123000, tzinfo=UTC)
    assert obs.dispatch_ended == datetime(2026, 11, 8, 8, 0, 0, tzinfo=UTC)
    assert obs.dispatch_started.utcoffset() == timedelta(0)
    assert obs.dispatch_ended.utcoffset() == timedelta(0)


@pytest.mark.parametrize(
    "dispatch",
    [
        {"id": DISPATCH, "status": "dispatched"},
        {"id": DISPATCH, "dispatchedAt": "yesterday", "completedAt": "soon"},
    ],
    ids=["no-times", "bad-times"],
)
def test_worker_show_dispatch_times_missing_or_bad(dispatch):
    obs = probes.parse_worker_show(
        RUN, {"dispatchId": DISPATCH}, {"dispatch": dispatch}
    )

    assert obs.dispatch_started is None
    assert obs.dispatch_ended is None
    assert obs.dispatch == DISPATCH
