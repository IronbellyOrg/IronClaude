"""No GitHub text reaches the watcher's output (design T1 and T11, NFR-001, NFR-006).

The poll reads two kinds of text: the title and body of an assigned issue (the
search row and the re-read) and nothing else. The body is only tested for a plan
and dropped. The title travels in exactly one place: the ``title`` of a plan
request in a wake file under the orchestrator repository. This file proves that.

Hostile replies carry the canary ``PWNED-TITLE`` as a title, a body, a label
name, an assignee login, inside non-JSON ``gh`` stdout, inside ``gh`` stderr
longer than 500 bytes on a failing call, in extra fields and in wrong-typed
fields. Whole ``once`` cycles (real and dry-run) and the ``status`` command run
over them through the real CLI and the real ``Waker`` (over a spy runner and a
fake ``/proc``), and the canary must never appear in any file under the state
directory (rotated audit files included), in any recorded argv (the typed line
and the mailbox message included), in the captured output of the commands, or in
a wake file outside the title of a plan request.

Every scenario proves the canary was served to the code (``SpyRunner``), so a
pass cannot come from text that never entered. The checkers are fed bad input in
their own tests, so they cannot pass vacuously.
"""

from __future__ import annotations

import dataclasses
import json
import re
import sys
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.issue_watch import audit, cli, cycle, github, wake
from superclaude.cli.issue_watch import runner as runner_mod
from superclaude.cli.issue_watch.cli import issue_watch_group
from superclaude.cli.issue_watch.runner import CommandResult, SubprocessRunner

from .conftest import (
    CYCLE_NOW,
    EMPTY_BODY,
    GOOD_BODY,
    ORCA_PATH,
    OWN_LOGIN,
    REPO_A,
    TIERS_TEXT,
    FailingStore,
    FakeClock,
    FakeRunner,
    GhWorld,
    fake_proc,
    load_fixture,
    make_config,
    orch_dir,
    script_live_session,
    write_registry,
    write_run,
    write_scenario,
)
from .conftest import result as command_result

# The real assembly, taken at import before any test patches ``cli.build_deps``.
_REAL_BUILD_DEPS = cli.build_deps

SENT = "PWNED-TITLE"
STEM = "PWNED"  # a shorter needle also catches a truncated or re-cased copy
HOSTILE_PAD = "x" * 600
WAKE_LINE_SHAPE = re.compile(
    r"^/sc:orchestrator --wake [0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}$"
)
WAKE_ID_IN = re.compile(r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}")
UNREAD_NOTE = re.compile(r"^issue-watch: [a-z][a-z0-9_]{0,39}$")
LOCAL_MOUNTINFO = "1 0 0:1 / / rw - ext4 /dev/sda1 rw\n"
FILLER = "#"  # first character of the padding line the rotation test writes

# The closed audit schema, written out here so the test does not read it from the
# module it checks (audit.py ``_COMMON`` and ``_KEYS``).
_COMMON_KEYS = {"kind", "ts", "host", "login", "cycle_id", "dry_run", "reason"}
CLOSED_KEYS = {
    "cycle": _COMMON_KEYS | {"exit", "gh_calls", "duration_ms", "discovery_count", "clock_skew_s"},
    "decision": _COMMON_KEYS
    | {"repo", "issue", "state", "note", "orchestrator", "wake_id", "stages"},
    "warning": _COMMON_KEYS | {"repo", "issue", "discovery_count", "clock_skew_s"},
}  # fmt: skip
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


def wake_files_of(config: cycle.Config) -> list[Path]:
    """Every wake and acknowledgment file under the orchestrator repository."""
    base = config.orchestrator_repo / ".orchestrator"
    return [p for p in sorted(base.rglob("*.json")) if "wakes" in p.parts]


def assert_wake_files_clean(config: cycle.Config) -> int:
    """The canary is absent from every wake file but a plan request's title.

    Returns how many plan-request titles carried it (the one allowed place).
    """
    carried = 0
    for path in wake_files_of(config):
        data = json.loads(path.read_text("utf-8"))
        for item in data.get("plan_requests", []):
            if STEM in item["title"].upper():
                carried += 1
            item["title"] = ""
        assert STEM not in json.dumps(data).upper(), f"the canary reached {path}"
    return carried


_TEXT_WORDS = re.compile(
    r"\b(title|body|bodyText|bodyHTML|text|message|rename|comment|comments)\b"
)
# The two reads that return text, and the words each may name.
_SEARCH_ASSIGNED = re.compile(r"^q=is:issue is:open assignee:")
# the hold label: read, create and add or remove (a label has a name, a colour, a note)
_LABEL_PATH = re.compile(r"repos/[^/]+/[^/]+/(issues/\d+/)?labels(/hold:plan)?")


def text_requests(argv: Iterable[str]) -> list[str]:
    """Reasons this ``gh`` argv could return text the poll may not read.

    Allowed: the S1 search names ``title`` and ``body``; the re-read names
    ``body``. Nothing else names a text field, and no call has a template.
    """
    argv = list(argv)
    if not argv or argv[0] != "gh":
        return []
    found: list[str] = []
    if argv[1:3] == ["issue", "develop"]:
        pass  # the linked branch names, nothing else
    elif argv[1:2] == ["issue"] and "--json" not in argv:
        found.append("gh issue without --json prints titles")
    elif argv[1:2] == ["issue"]:
        fields = set(argv[argv.index("--json") + 1].split(","))
        if fields - {"updatedAt", "labels"}:
            found.append(f"--json fields {sorted(fields - {'updatedAt', 'labels'})}")
    if "--template" in argv or "-t" in argv:
        found.append("a --template")
    jq = None
    for flag in ("--jq", "-q"):
        if flag in argv:
            jq = argv[argv.index(flag) + 1]
            words = set(_TEXT_WORDS.findall(jq))
            if len(argv) > 6 and _SEARCH_ASSIGNED.match(argv[6]):
                words -= {"title", "body"}
            elif len(argv) > 4 and re.fullmatch(
                r"repos/[^/]+/[^/]+/issues/\d+", argv[4]
            ):
                words -= {"body"}
            if words:
                found.append(f"{flag} names a text field {sorted(words)}: {jq}")
    paths = [a for a in argv if a.startswith("repos/")]
    if paths and jq is None and not _LABEL_PATH.fullmatch(paths[0]):
        found.append("a REST path without --jq returns the whole body")
    for a in argv:
        if a.startswith("query=") and _TEXT_WORDS.search(a):
            found.append("a GraphQL query names a text field")
    return found


def orca_text_problems(argv: list[str]) -> list[str]:
    """Orca argv that could carry GitHub text: the typed line, the mailbox, the unread note."""
    found: list[str] = []
    if argv[1:3] == ["terminal", "send"]:
        line = argv[argv.index("--text") + 1]
        if not WAKE_LINE_SHAPE.fullmatch(line):
            found.append(f"a typed line that is not the wake line: {line!r}")
    if argv[1:3] == ["orchestration", "send"]:
        subject = argv[argv.index("--subject") + 1]
        payload = json.loads(argv[argv.index("--payload") + 1])
        if not re.fullmatch(r"orchestrator-wake " + WAKE_ID_IN.pattern, subject):
            found.append(f"a mailbox subject with more than the wake id: {subject!r}")
        if set(payload) != {"kind", "wake_id"} or not WAKE_ID_IN.fullmatch(
            payload["wake_id"]
        ):
            found.append(f"a mailbox payload with more than the wake id: {payload!r}")
    if argv[1:3] == ["worktree", "set"]:
        note = argv[argv.index("--comment") + 1]
        if not UNREAD_NOTE.fullmatch(note):
            found.append(f"an unread note that is not fixed text: {note!r}")
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
    skip: tuple[str, ...] = (),
) -> None:
    """The whole no-text invariant over one scenario (the wake files are checked apart)."""
    assert_state_dir_clean(state_dir, skip)
    for label, text in outputs.items():
        assert STEM not in text.upper(), f"the canary reached {label}: {text!r}"
    for argv, _cwd in spy.calls:
        assert not any(STEM in a.upper() for a in argv), argv
        assert text_requests(argv) == [], argv
        assert orca_text_problems(list(argv)) == [], argv
    assert_closed_audit(read_audit(state_dir))


# ==============================================================================
# Running a scenario through the real CLI
# ==============================================================================


def write_config(path: Path, config: cycle.Config) -> Path:
    path.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "enabled": config.enabled,
                "orchestrator_repo": str(config.orchestrator_repo),
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


class Run:
    """One scenario's world, deps and command outputs.

    The world holds issue 7 (planned, assigned to the user) and issue 5 (no plan,
    so it is held and, an hour later, asked for in a plan request). The
    orchestrator ``ironclaude-1`` is registered with a live Run and a live session
    in a fake ``/proc``, so the typed line and the mailbox message are really sent.
    """

    def __init__(self, tmp_path, tmp_state, monkeypatch, sc: Scenario | None = None):
        self.tmp_path = tmp_path
        self.state_dir = tmp_state.state_dir
        self.spy = SpyRunner()
        self.world = GhWorld(
            FakeClock(CYCLE_NOW), make_config(tmp_path), runner=self.spy
        )
        write_registry(self.world.config, {"ironclaude-1": {}})
        write_run(self.world.config, "ironclaude-1")
        self.world.issue(
            REPO_A, 7, title=SENT, body=GOOD_BODY.replace("Run the tests.", SENT)
        )
        self.world.issue(
            REPO_A,
            5,
            title=f"{SENT} held",
            body=EMPTY_BODY + SENT,
            branches=[("issue-5-x", CYCLE_NOW)],
        )
        if sc is not None:
            sc.setup(self.world)
        script_live_session(self.spy)
        waker = wake.Waker(
            self.spy, proc_root=fake_proc(tmp_path), sleep=lambda s: None
        )
        self.deps = self.world.deps(tmp_path, tmp_state, waker=waker)
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

    def two_cycles(self, dry: bool = False):
        """One cycle, then one an hour later (the hold's plan request falls due)."""
        first = self.once(dry, "once 1")
        self.world.clock.advance(3600)
        second = self.once(dry, "once 2")
        return first, second

    def status(self):
        self.command("status", "status")
        self.command("status --json", "status", "--json")

    def check(self, skip: tuple[str, ...] = ()) -> int:
        assert_no_text(self.state_dir, self.outputs, self.spy, skip)
        return assert_wake_files_clean(self.world.config)


# ==============================================================================
# The base case: the title is in exactly one place
# ==============================================================================


def test_the_title_reaches_only_the_plan_request_in_the_wake_file(
    tmp_path, tmp_state, monkeypatch
):
    run = Run(tmp_path, tmp_state, monkeypatch)
    first, second = run.two_cycles()
    run.status()
    assert first.exit_code == 0 and second.exit_code == 0, (first.output, second.output)
    assert run.spy.canary_served()
    # a wake for issue 7 and a plan request for issue 5 were sent through the real Waker
    sends = [a for a, _ in run.spy.calls if list(a[1:3]) == ["terminal", "send"]]
    assert len(sends) == 2
    assert all(WAKE_LINE_SHAPE.fullmatch(a[a.index("--text") + 1]) for a in sends)
    mailbox = [a for a, _ in run.spy.calls if list(a[1:3]) == ["orchestration", "send"]]
    assert len(mailbox) == 2
    assert run.check() == 1  # the one plan-request title, nowhere else


def test_a_dry_run_writes_the_shadow_file_and_it_stays_clean(
    tmp_path, tmp_state, monkeypatch
):
    run = Run(tmp_path, tmp_state, monkeypatch)
    out = run.once(dry=True)
    assert f"would_wake: {REPO_A}#7" in out.output
    names = {p.name for p in assert_state_dir_clean(run.state_dir)}
    assert {"dispatch.json", "dry-run.json", "audit.jsonl"} <= names
    assert run.spy.canary_served()
    assert not [a for a, _ in run.spy.calls if list(a[1:3]) == ["terminal", "send"]]
    assert run.check() == 0  # a dry run writes no wake file


# ==============================================================================
# Hostile content in every field the poll reads
# ==============================================================================


def _hostile_labels(world: GhWorld) -> None:
    world.issue(REPO_A, 7, labels=[SENT, "hold:backlog-ish"], body=GOOD_BODY)
    world.issue(REPO_A, 8, labels=[SENT], body=GOOD_BODY)


def _hostile_co_assignee(world: GhWorld) -> None:
    world.issue(REPO_A, 6, assignees=[OWN_LOGIN, SENT])  # assigned_other, skipped
    world.issue(REPO_A, 4, assignees=[SENT])  # not ours at all


def _extra_fields(world: GhWorld) -> None:
    """The search rows carry extra text fields a projection would never give."""
    original = world.runner.script

    def decorate(reply):
        def served(argv, cwd):
            got = reply(argv, cwd)
            data = json.loads(got.stdout)
            for item in data["items"]:
                item.update(
                    {
                        "comments": SENT,
                        "url": SENT,
                        "user": {"login": SENT},
                        "text": SENT,
                    }
                )
            return dataclasses.replace(got, stdout=json.dumps(data))

        return served

    for argv, reply in list(original.items()):
        if argv[:5] == ("gh", "api", "--method", "GET", "search/issues"):
            original[argv] = decorate(reply)


def _malformed(field: str, value: object) -> Callable[[GhWorld], None]:
    def setup(world: GhWorld) -> None:
        def decorate(reply):
            def served(argv, cwd):
                got = reply(argv, cwd)
                data = json.loads(got.stdout)
                for item in data["items"]:
                    item[field] = value
                return dataclasses.replace(got, stdout=json.dumps(data))

            return served

        for argv, reply in list(world.runner.script.items()):
            if argv[:5] == ("gh", "api", "--method", "GET", "search/issues"):
                world.runner.script[argv] = decorate(reply)

    return setup


CONTENT_SCENARIOS = [
    Scenario("label_names", _hostile_labels),
    Scenario("co_assignee_login", _hostile_co_assignee),
    Scenario("extra_text_fields", _extra_fields),
    Scenario("malformed_number", _malformed("number", SENT)),
    Scenario("malformed_state", _malformed("state", SENT)),
    Scenario("malformed_updated_at", _malformed("updated_at", SENT)),
    Scenario("malformed_repository_url", _malformed("repository_url", SENT)),
    Scenario("malformed_labels", _malformed("labels", SENT)),
    Scenario("malformed_assignees", _malformed("assignees", [{"login": SENT}])),
    Scenario("malformed_title", _malformed("title", [SENT])),
    Scenario("malformed_body", _malformed("body", {"text": SENT})),
    Scenario("unicode_login", lambda w: w.issue(REPO_A, 3, assignees=[OWN_LOGIN, f"{SENT}\n‮"])),
]  # fmt: skip


@pytest.mark.parametrize("dry", [False, True], ids=["real", "dry"])
@pytest.mark.parametrize("sc", CONTENT_SCENARIOS, ids=lambda sc: sc.id)
def test_hostile_content_never_leaves_a_cycle(
    sc, dry, tmp_path, tmp_state, monkeypatch
):
    run = Run(tmp_path, tmp_state, monkeypatch, sc)
    run.two_cycles(dry)
    run.status()
    assert run.spy.canary_served(), f"{sc.id}: the canary never reached the code"
    assert any(ln["kind"] == "cycle" for ln in read_audit(run.state_dir))
    run.check()


# ==============================================================================
# Hostile replies of every call the poll makes
# ==============================================================================

PER_ISSUE = (
    "reread",
    "label_get",
    "label_create",
    "label_add",
    "updated",
    "develop",
    "timeline",
    "branch",
)
FAIL_CALLS = (
    "user",
    "tiers",
    "search",
    "info",
    "origin",
    "probe",
    "worktree",
    "reference",
    *PER_ISSUE,
)
SIGNS = (
    "",
    "HTTP 401 gh auth login",
    "HTTP 429 rate limit",
    "HTTP 403",
    "HTTP 502",
)


def _fail(call: str, reply: CommandResult) -> Callable[[GhWorld], None]:
    return lambda world: world.fail(call, reply, times=None)


def _failure_scenarios() -> list[Scenario]:
    out = [
        Scenario("spawn_error_text", _fail("search", command_result(spawn_error=SENT))),
        Scenario(
            "timeout_with_stderr",
            _fail("search", command_result(timed_out=True, stderr=hostile_stderr())),
        ),
    ]
    for call in FAIL_CALLS:
        out.append(
            Scenario(
                f"non_json_stdout_{call}",
                _fail(call, command_result(stdout=f"{SENT} <html>not json</html>")),
            )
        )
        for number, sign in enumerate(SIGNS):
            out.append(
                Scenario(
                    f"stderr_{call}_{number}",
                    _fail(
                        call,
                        command_result(stderr=hostile_stderr(sign), returncode=1),
                    ),
                )
            )
    return out


FAILURES = _failure_scenarios()


@pytest.mark.parametrize("dry", [False, True], ids=["real", "dry"])
@pytest.mark.parametrize("sc", FAILURES, ids=lambda sc: sc.id)
def test_a_hostile_failure_leaves_no_canary(sc, dry, tmp_path, tmp_state, monkeypatch):
    run = Run(tmp_path, tmp_state, monkeypatch, sc)
    run.two_cycles(dry)
    run.status()
    served = run.spy.canary_served()
    if not dry:
        # The call is reached in a real cycle, so this scan is not vacuous. (A
        # dry run makes no write and no Orca call, so it may never reach some.)
        assert served, f"{sc.id}: the canary never reached the code"
    assert any(ln["kind"] == "cycle" for ln in read_audit(run.state_dir)) or (
        not dry and sc.id.endswith("_user")
    )
    run.check()


# ==============================================================================
# Rotated audit files
# ==============================================================================


def test_rotated_audit_files_are_scanned_and_stay_clean(
    tmp_path, tmp_state, monkeypatch
):
    sc = Scenario(
        "search_stderr",
        _fail(
            "search", command_result(stderr=hostile_stderr("HTTP 502"), returncode=1)
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
    run = Run(tmp_path, tmp_state, monkeypatch)
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
    search = tuple(github.argv_search_assigned("IronbellyOrg", OWN_LOGIN))

    def explode(argv, cwd):
        raise ValueError(f"explode {SENT}")

    run.spy.script[search] = explode
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
    "invalid_json": f'{{"schema_version": 2, "entries": {{"{SENT}": ',
    "text_in_version": json.dumps({"schema_version": SENT, "entries": {}}),
    "text_in_entries": json.dumps({"schema_version": 2, "entries": {SENT: {}}}),
    "text_in_holds": json.dumps(
        {"schema_version": 2, "holds": {SENT: {"state": SENT}}}
    ),
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
    """The real runner and the real CLI assembly over PATH stubs: the search fails with
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
                    "argv_prefix": ["api", "--method", "GET", "search/issues"],
                    "stderr": hostile_stderr("HTTP 502"),
                    "exit": 1,
                },
            ],
            "ccsession": [{"argv_prefix": ["--help"], "stdout": TIERS_TEXT}],
        },
    )
    recorded: list[_RecordingRunner] = []

    def build(config):
        deps = _REAL_BUILD_DEPS(config)
        spy = _RecordingRunner(deps.runner)
        recorded.append(spy)
        return dataclasses.replace(deps, runner=spy, waker=wake.Waker(spy))

    monkeypatch.setattr(cli, "build_deps", build)
    config = make_config(tmp_path)
    path = write_config(tmp_path / "cfg.json", config)
    out = invoke("once", "--config", str(path))
    status = invoke("status", "--config", str(path))
    (spy,) = recorded
    searches = [
        r
        for r in spy.results
        if r.argv[:5] == ("gh", "api", "--method", "GET", "search/issues")
    ]
    assert searches and all(r.returncode == 1 for r in searches)
    assert searches[0].stderr.startswith(SENT), "the canary did not reach the runner"
    assert len(searches[0].stderr.encode("utf-8")) == 500
    assert out.exit_code != 0 and "cycle:" in out.output
    for text in (out.output, status.output):
        assert STEM not in text.upper()
    assert_state_dir_clean(tmp_state.state_dir)
    assert_closed_audit(read_audit(tmp_state.state_dir))
    assert any(ln["kind"] == "cycle" for ln in read_audit(tmp_state.state_dir))


# ==============================================================================
# No code path asks gh for text beyond the two reads
# ==============================================================================


def _every_builder_argv() -> list[list[str]]:
    from datetime import datetime, timezone

    when = datetime(2026, 11, 7, 12, 0, tzinfo=timezone.utc)
    argvs = [
        github.argv_user(),
        github.argv_search_assigned("IronbellyOrg", OWN_LOGIN),
        *(
            github.argv_search_info(s, "IronbellyOrg", OWN_LOGIN, when)
            for s in ("mentions", "could_assign", "affects")
        ),
        github.argv_reread(REPO_A, 7),
        github.argv_issue_updated(REPO_A, 7),
        github.argv_issue_labels(REPO_A, 7),
        github.argv_develop_list(REPO_A, 7),
        github.argv_branch_date(REPO_A, "issue-7-x"),
        github.argv_timeline(REPO_A, 7),
        github.argv_label_get(REPO_A),
        github.argv_label_create(REPO_A),
        github.argv_label_add(REPO_A, 7),
        github.argv_label_remove(REPO_A, 7),
    ]
    return argvs


def test_no_argv_builder_asks_gh_for_text_beyond_the_two_reads():
    argvs = _every_builder_argv()
    assert len(argvs) == 15
    for argv in argvs:
        assert text_requests(argv) == [], argv
    # the two reads that do return text name exactly the fields the design allows
    assert {"title", "body"} <= set(_TEXT_WORDS.findall(github.SEARCH_ASSIGNED_JQ))
    assert set(_TEXT_WORDS.findall(github.REREAD_JQ)) == {"body"}
    for jq in (github.SEARCH_INFO_JQ, github.TIMELINE_JQ, github.BRANCH_JQ):
        assert _TEXT_WORDS.findall(jq) == []


@pytest.mark.parametrize(
    "argv",
    [
        ["gh", "issue", "list", "--json", "number,title"],
        ["gh", "issue", "list"],
        ["gh", "issue", "view", "7", "--json", "comments"],
        ["gh", "issue", "view", "7", "--json", "updatedAt,body"],
        ["gh", "api", "--method", "GET", "repos/o/r/issues/7/comments"],
        ["gh", "api", "--method", "GET", "repos/o/r/issues/7", "--jq", "{title}"],
        ["gh", "api", "--method", "GET", "repos/o/r/issues/7", "-q", ".comments"],
        ["gh", "api", "--method", "GET", "repos/o/r/pulls/7", "--jq", ".body | length"],
        ["gh", "api", "--method", "GET", "repos/o/r/issues/7/timeline", "--jq", "[.[] | .body]"],
        ["gh", "api", "--method", "GET", "search/issues", "-f", "q=involves:me org:o", "--jq", "{title}"],
        ["gh", "api", "graphql", "-f", "query=query { issue { title } }"],
        ["gh", "api", "graphql", "-f", "query=query { comments { nodes { bodyText } } }"],
        ["gh", "issue", "view", "7", "--json", "updatedAt", "--template", "{{.title}}"],
    ],
)  # fmt: skip
def test_the_text_request_scan_flags_each_bad_argv(argv):
    assert text_requests(argv) != []


@pytest.mark.parametrize(
    "argv",
    [
        ["orca", "terminal", "send", "--terminal", "t", "--text", f"/sc:orchestrator --wake {SENT}"],
        ["orca", "terminal", "send", "--terminal", "t", "--text", "/sc:orchestrator --wake 20261107T120000Z-0000000a extra"],
        ["orca", "orchestration", "send", "--subject", f"orchestrator-wake {SENT}", "--payload", '{"kind":"x","wake_id":"20261107T120000Z-0000000a"}'],
        ["orca", "orchestration", "send", "--subject", "orchestrator-wake 20261107T120000Z-0000000a", "--payload", '{"kind":"x","wake_id":"20261107T120000Z-0000000a","title":"t"}'],
        ["orca", "worktree", "set", "--comment", f"issue-watch: {SENT}"],
    ],
)  # fmt: skip
def test_the_orca_scan_flags_text_in_a_line_a_message_or_a_note(argv):
    assert orca_text_problems(argv) != []


def test_the_orca_scan_accepts_the_fixed_forms():
    wid = "20261107T120000Z-0000000a"
    payload = json.dumps({"kind": "orchestrator-wake", "wake_id": wid})
    assert (
        orca_text_problems(
            ["o", "terminal", "send", "--text", f"/sc:orchestrator --wake {wid}"]
        )
        == []
    )
    assert (
        orca_text_problems(
            [
                "o",
                "orchestration",
                "send",
                "--subject",
                f"orchestrator-wake {wid}",
                "--payload",
                payload,
            ]
        )
        == []
    )
    assert (
        orca_text_problems(
            ["o", "worktree", "set", "--comment", "issue-watch: no_session"]
        )
        == []
    )


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


def test_wake_file_scan_allows_only_a_plan_request_title(tmp_path):
    config = make_config(tmp_path)
    wakes = orch_dir(config) / "wakes"
    wakes.mkdir()
    ok = {"assigned": [], "plan_requests": [{"title": f"{SENT} x", "repo": REPO_A}]}
    (wakes / "a.json").write_text(json.dumps(ok), encoding="utf-8")
    assert assert_wake_files_clean(config) == 1
    bad = {"assigned": [{"title": SENT}], "plan_requests": []}
    (wakes / "b.json").write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(AssertionError):
        assert_wake_files_clean(config)
    (wakes / "b.json").write_text(
        json.dumps({"plan_requests": [{"title": "t", "missing": [SENT]}]}),
        encoding="utf-8",
    )
    with pytest.raises(AssertionError):
        assert_wake_files_clean(config)


def test_output_scan_flags_the_canary_in_every_kind_of_output(tmp_path, tmp_state):
    spy = SpyRunner()
    state = tmp_state.state_dir
    for label in ("once", "status", "status --json"):
        with pytest.raises(AssertionError):
            assert_no_text(state, {label: f"x {SENT} y"}, spy)
    assert_no_text(state, {"once": "cycle: cycle_complete"}, spy)


def test_argv_scan_flags_a_canary_or_a_bad_line_in_a_recorded_call(tmp_path, tmp_state):
    state = tmp_state.state_dir
    spy = SpyRunner()
    spy.calls.append((("gh", "api", "user", SENT), None))
    with pytest.raises(AssertionError):
        assert_no_text(state, {}, spy)
    spy = SpyRunner()
    spy.calls.append(
        (("orca", "terminal", "send", "--text", "/sc:orchestrator --wake x"), None)
    )
    with pytest.raises(AssertionError):
        assert_no_text(state, {}, spy)
    spy = SpyRunner()
    spy.calls.append((("gh", "issue", "list", "--json", "number,title"), None))
    with pytest.raises(AssertionError):
        assert_no_text(state, {}, spy)


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
        audit.decision_line(**stamp, reason="woken", repo=REPO_A, issue=7, state=SENT)
    with pytest.raises(ValueError):
        audit.decision_line(**stamp, reason="woken", repo=SENT, issue=7)
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
    assert ORCA_PATH.endswith("orca-ide")
