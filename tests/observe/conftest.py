"""Shared support for tests/observe: fake clock, fake runner and discovery, console factory.

Every test in this package runs with ``subprocess.Popen`` and ``subprocess.run`` replaced by a
function that raises, unless the test carries the marker ``observe_real_process`` (AD-16, T36).
"""

from __future__ import annotations

import io
import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
from importlib import resources

import pytest
from jsonschema import Draft7Validator

from superclaude.cli.observe.terminal import make_console, resolve_policy

BASE_TIME = datetime(2026, 11, 8, 12, 0, 0, tzinfo=timezone.utc)
WORKER_LIST_BASE = ["orchestration", "worker-list", "--json", "--limit", "100"]
DISCOVERY_TAIL = ["skills", "list", "--json"]
QUESTION_BASE = ["orchestration", "check", "--all", "--types", "question"]

# The snapshot schema as shipped in the package; a broken schema fails at collection.
SCHEMA: dict = json.loads(
    resources.files("superclaude.cli.observe")
    .joinpath("snapshot.schema.json")
    .read_text(encoding="utf-8")
)
Draft7Validator.check_schema(SCHEMA)


# -- subprocess guard -------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _subprocess_guard(request, monkeypatch):
    if request.node.get_closest_marker("observe_real_process"):
        return

    def refuse(*args, **kwargs):
        raise AssertionError(
            "subprocess is blocked in tests/observe; mark the test observe_real_process to lift the guard"
        )

    monkeypatch.setattr(subprocess, "Popen", refuse)
    monkeypatch.setattr(subprocess, "run", refuse)


# -- fake clock ---------------------------------------------------------------------------


class FakeClock:
    """Monotonic time, wall time and the local time zone, all under the test's control."""

    def __init__(
        self,
        monotonic: float = 1000.0,
        wall: float | None = None,
        tz: timezone = timezone.utc,
    ):
        self._mono = monotonic
        self._wall = BASE_TIME.timestamp() if wall is None else wall
        self.tz = tz

    def monotonic(self) -> float:
        return self._mono

    def wall(self) -> float:
        return self._wall

    def local_tz(self) -> timezone:
        return self.tz

    def advance(self, seconds: float) -> None:
        self._mono += seconds
        self._wall += seconds

    def jump_wall(self, seconds: float) -> None:
        """A wall-clock jump that leaves monotonic time alone."""
        self._wall += seconds


@pytest.fixture
def fake_clock() -> FakeClock:
    return FakeClock()


# -- fake runner and discovery (one shared argv log) ---------------------------------------


def argv_allowed(argv) -> bool:
    """The only argv the observer may ever run: worker-list (with optional pairs), discovery,
    or the one R2 message template for one named Run."""
    argv = list(argv)
    if len(argv) < 2 or not all(isinstance(a, str) for a in argv):
        return False
    tail = argv[1:]
    if tail == DISCOVERY_TAIL:
        return True
    if tail[:5] == QUESTION_BASE:
        return (
            len(tail) == 8
            and tail[5] == "--run"
            and not tail[6].startswith("-")
            and tail[7] == "--json"
        )
    if tail[:5] != WORKER_LIST_BASE:
        return False
    rest = tail[5:]
    if rest[:1] == ["--run"] and len(rest) >= 2 and not rest[1].startswith("-"):
        rest = rest[2:]
    if rest[:1] == ["--cursor"] and len(rest) >= 2 and not rest[1].startswith("-"):
        rest = rest[2:]
    return rest == []


class FakeRunner:
    """``Runner`` stand-in: logs every argv, raises on one outside the allow-list.

    ``responses`` holds ``(returncode, stdout)`` pairs, exceptions, or callables
    ``f(argv, timeout) -> (returncode, stdout)``; the last one repeats when they run out.
    """

    def __init__(self, log: list, responses: list | None = None):
        self.log = log
        self.responses = responses if responses is not None else [(0, "{}")]
        self.timeouts: list[float] = []
        self.calls = 0

    def __call__(self, argv, timeout):
        self.log.append(list(argv))
        self.timeouts.append(timeout)
        if not argv_allowed(argv):
            raise AssertionError(f"argv outside the allow-list: {list(argv)!r}")
        response = self.responses[min(self.calls, len(self.responses) - 1)]
        self.calls += 1
        if isinstance(response, BaseException):
            raise response
        if callable(response):
            return response(argv, timeout)
        return response


class FakeDiscover:
    """``Discover`` stand-in: logs the discovery argv the real helper would run."""

    def __init__(self, log: list, path: str | None = "/opt/fake/orca"):
        self.log = log
        self.path = path
        self.calls = 0

    def __call__(self):
        self.calls += 1
        self.log.append([self.path or "orca", *DISCOVERY_TAIL])
        return self.path


@pytest.fixture
def argv_log() -> list:
    return []


@pytest.fixture
def fake_runner(argv_log) -> FakeRunner:
    return FakeRunner(argv_log)


@pytest.fixture
def fake_discover(argv_log) -> FakeDiscover:
    return FakeDiscover(argv_log)


# -- data and console helpers ----------------------------------------------------------------


def make_rows(n_rows: int, n_runs: int) -> list[dict]:
    """``n_rows`` valid worker rows spread over ``n_runs`` distinct runs (T16 matrix)."""
    rows = []
    for i in range(1, n_rows + 1):
        observed = (BASE_TIME - timedelta(seconds=3 * i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows.append(
            {
                "dispatchId": f"w-{i:03d}",
                "taskId": f"t-{i:03d}",
                "runId": f"run-{(i - 1) % n_runs}",
                "workerState": "running" if i % 2 else "idle",
                "dispatchStatus": "active",
                "terminalState": "active",
                "projection": {
                    "outcome": "none",
                    "nextAction": {"kind": "wait" if i % 3 else "none"},
                    "liveness": {
                        "verdict": "alive",
                        "source": "terminal",
                        "observedAt": observed,
                    },
                    "evidence": {"lastObservedAt": observed},
                },
            }
        )
    return rows


def make_envelope(
    rows: list[dict], total: int | None = None, has_more: bool = False
) -> dict:
    page = {"hasMore": has_more, "limit": 100}
    if total is not None:
        page["total"] = total
    return {"result": {"workers": rows, "page": page, "scope": {"source": "all"}}}


@pytest.fixture(name="make_rows")
def make_rows_fixture():
    return make_rows


@pytest.fixture
def console_factory():
    """``console_factory(width=160, height=40, ascii=False, no_color=False) -> (console, policy)``."""

    def factory(
        width: int = 160, height: int = 40, ascii: bool = False, no_color: bool = False
    ):
        env = {"NO_COLOR": "1"} if no_color else {}
        policy = resolve_policy(env, "utf-8", {"ascii": ascii}, width, height)
        return make_console(policy, file=io.StringIO(), record=True), policy

    return factory


# -- R2 question rows (probe shapes, SYNTHETIC values) ------------------------------------------

QRUN = "run_14cfcbd8edf2"


def question_payload(
    dispatch_id: str = "disp_synthetic01",
    question: str = "synthetic question text",
    **extra,
) -> str:
    """A payload JSON string in the observed shape (dispatchId, taskId, question, options)."""
    body = {
        "dispatchId": dispatch_id,
        "taskId": "task_synthetic01",
        "question": question,
        "options": ["yes", "no"],
    }
    body.update(extra)
    return json.dumps(body)


def _payload_dispatch(payload) -> str | None:
    """The ``dispatchId`` of a payload given as a dict or a JSON string, else None."""
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except ValueError:
            return None
    found = payload.get("dispatchId") if isinstance(payload, dict) else None
    return found if isinstance(found, str) and found else None


def make_question_rows(
    n: int,
    run: str = QRUN,
    start: int = 0,
    newest_first: bool = True,
    subject=None,
    payload=None,
    from_handle=None,
) -> list[dict]:
    """``n`` synthetic ``question`` message rows with the recorded key names, no real values.

    Row ``i`` is created ``i`` seconds after a fixed base, so a higher id is a newer question;
    ``newest_first`` returns them in the order ``check --all`` gives them (REPORT, evidence 14).
    ``payload`` is used as given for every row. Without ``from_handle`` the sender is the
    observed shape ``dispatch:<dispatchId>`` when the payload names a dispatch, else
    ``term_synthetic``.
    """
    sender = from_handle
    if sender is None:
        dispatch = _payload_dispatch(payload)
        sender = f"dispatch:{dispatch}" if dispatch else "term_synthetic"
    rows = []
    for i in range(start, start + n):
        created = BASE_TIME - timedelta(seconds=3600) + timedelta(seconds=i)
        rows.append(
            {
                "id": f"msg_{i:012x}",
                "run_id": run,
                "delivery_contract": "current_delivery",
                "from_handle": sender,
                "to_handle": f"run:{run}",
                "subject": f"synthetic question {i}" if subject is None else subject,
                "body": "synthetic body",
                "type": "question",
                "priority": "normal",
                "thread_id": None,
                "payload": payload,
                "created_at": created.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "delivered_at": None,
            }
        )
    return list(reversed(rows)) if newest_first else rows


def make_question_envelope(rows: list[dict], run: str = QRUN) -> dict:
    """The recorded envelope shape of one ``check --all`` read."""
    return {
        "id": "00000000-0000-0000-0000-000000000000",
        "ok": True,
        "result": {
            "acknowledged": None,
            "count": len(rows),
            "messages": rows,
            "runId": run,
        },
        "_meta": {"runtimeId": "00000000-0000-0000-0000-000000000001"},
    }


def make_question_error(code: str) -> dict:
    """An ``{"ok": false, "error": {...}}`` envelope as recorded for the two known codes."""
    return {
        "id": "00000000-0000-0000-0000-000000000002",
        "ok": False,
        "error": {"code": code, "message": code},
    }


def routed_runner_responses(worker, message):
    """One runner response callable for worker-list and message calls.

    ``worker`` and ``message`` are each a response (a pair or a callable) or a list of them:
    the nth call of that kind gets the nth response and the last one repeats.
    """
    queues = {
        "worker": list(worker) if isinstance(worker, list) else [worker],
        "message": list(message) if isinstance(message, list) else [message],
    }
    seen = {"worker": 0, "message": 0}

    def respond(argv, timeout):
        kind = "message" if "check" in argv else "worker"
        queue = queues[kind]
        pick = queue[min(seen[kind], len(queue) - 1)]
        seen[kind] += 1
        return pick(argv, timeout) if callable(pick) else pick

    return respond


# A question row of the list on screen: an optional marker (selected glyph, its ASCII form or two
# spaces), then the age and two spaces. With the per-row "reason unknown" gone from the screen
# (one title note says it once), this is how a test counts question rows.
QUESTION_ROW = re.compile(
    r"^(?:[▸@] |  )?(?:\d+[smhd]|unknown|age unknown \(clock skew\))  \S"
)


def question_rows(lines) -> list[str]:
    """The question-row lines of a screen, in order."""
    return [ln for ln in lines if QUESTION_ROW.match(ln)]


# -- frame-aware helpers (the questions-on screens are framed from the frame phase on) ---------------------

_TOP_ROW = re.compile(
    r"^ ?[╭┏+][─━-] (.*?) [─━-]*[╮┓+]$"
)  # corner, rule, title, rule, corner
_BOTTOM_ROW = re.compile(r"^ ?[╰┗+][─━-]+[╯┛+]$")
_BODY_ROW = re.compile(r"^ ?[│┃|] (.*) [│┃|]$")


_HEAD_PANES = (
    "COORDINATOR QUESTIONS",
    "OBSERVATION WINDOW",
)  # full width, one pad cell


def unframe(line: str) -> str:
    """``line`` without its margin, its left and right border glyph (rounded, heavy or ASCII)
    and one padding cell on each side; trailing spaces are removed. A top or bottom border row
    has no body and becomes the empty string (read its title with ``title_of``). A line that is
    not framed is returned as it is."""
    if _TOP_ROW.match(line) or _BOTTOM_ROW.match(line):
        return ""
    match = _BODY_ROW.match(line)
    return match.group(1).rstrip() if match else line


def title_of(lines) -> list[str]:
    """The text inset in every top border of ``lines``, in order."""
    return [m.group(1) for ln in lines if (m := _TOP_ROW.match(ln))]


def unframed(lines) -> list[str]:
    """``lines`` as the plain screen read before the frames: each top border becomes its title
    row, each body row loses its borders, each bottom border is dropped, other lines stay."""
    out: list[str] = []
    border_only = False  # the table pane of the ledger: no margin and no pad cell
    for ln in lines:
        if m := _TOP_ROW.match(ln):
            out.append(m.group(1))
            border_only = not ln.startswith(" ") and m.group(1) not in _HEAD_PANES
        elif _BOTTOM_ROW.match(ln):
            continue
        elif border_only and ln[:1] in "│┃|" and ln[-1:] in "│┃|":
            out.append(ln[1:-1].rstrip())
        else:
            out.append(unframe(ln))
    return out


def pane_body(lines, title: str, policy=None) -> list[str]:
    """The unframed body rows of the frame whose top border contains ``title`` (empty when no
    such frame is drawn): the rows between that top border and the next bottom border.
    ``policy`` is accepted for the signature the plan names; the border patterns already match
    the Unicode and the ASCII forms, so it changes nothing."""
    start = next(
        (i for i, ln in enumerate(lines) if _TOP_ROW.match(ln) and title in ln), None
    )
    if start is None:
        return []
    body: list[str] = []
    for ln in lines[start + 1 :]:
        if _BOTTOM_ROW.match(ln):
            break
        body.append(unframe(ln))
    return body


def split_columns(line: str, left_width: int, gap: int = 2) -> tuple[str, str]:
    """A two-column screen row as its two panes: the first ``left_width`` cells (the margin and
    the left pane) and what follows the ``gap``. Both parts are returned as they are drawn, so
    each can be passed to ``unframe``. The margin of the right pane is the gap's last cell."""
    return line[:left_width], line[left_width + gap - 1 :]


_PANE_END = "╮╯│┓┛┃+|"


def split_panes(lines, width: int) -> list[str]:
    """``lines`` (framed, as drawn at ``width`` columns) with every two-column desk row split into
    its two panes: for a run of consecutive two-column rows the left panes come first, then the
    right panes, each with its margin, blank halves dropped. Single-column rows stay as they are.
    The left pane is ``width - 4 - 80`` cells at 160 columns and above (question and list over
    the evidence) and ``width - 4 - 46`` at 116 up to 159 (evidence beside the list)."""
    if width >= 160:
        left = width - 4 - 80
    elif width >= 116:
        left = width - 4 - 46
    else:
        return list(lines)
    cut = 1 + left  # the margin and the left pane

    def two_columns(line: str) -> bool:
        if len(line) < cut + 2 or line[cut : cut + 2] != "  ":
            return False
        if line[:cut].strip():  # a left pane: its right border ends the left half
            return line[cut - 1] in _PANE_END
        # a blank left half (the left column is shorter): a pane border follows the gap
        return len(line) > cut + 2 and line[cut + 2] in "╭╰│┏┗┃+|"

    out: list[str] = []
    run: list[tuple[str, str]] = []

    def flush() -> None:
        out.extend(a for a, _ in run if a.strip())
        out.extend(b for _, b in run if b.strip())
        run.clear()

    for ln in lines:
        if two_columns(ln):
            run.append((ln[:cut].rstrip(), (" " + ln[cut + 2 :]).rstrip()))
        else:
            flush()
            out.append(ln)
    flush()
    return out


def panes_flat(lines, left_width: int | None = None, gap: int = 2) -> str:
    """The text of every pane of a screen as one flat string, whitespace collapsed: for a screen
    with two columns (``left_width`` given) each framed row is split into its two panes and the
    left panes are read before the right ones; other lines are read as they are."""
    left: list[str] = []
    right: list[str] = []
    for ln in lines:
        if left_width is not None and len(ln) > left_width + gap:
            a, b = split_columns(ln, left_width, gap)
            if _BODY_ROW.match(a) or _TOP_ROW.match(a) or _BOTTOM_ROW.match(a):
                left.append(unframed([a])[0] if unframed([a]) else "")
                right.append(unframed([b])[0] if unframed([b]) else "")
                continue
        left.append(unframed([ln])[0] if unframed([ln]) else "")
    return " ".join(" ".join(left + right).split())


# -- styled-output helpers (the screen carries SGR from the colour phase on) ------------------------------

_SGR = re.compile(r"\x1b\[([0-9;]*)m")


def strip_sgr(text: str) -> str:
    """``text`` with every SGR (colour and weight) escape sequence removed."""
    return _SGR.sub("", text)


def sgr_params(text: str) -> set[str]:
    """The parameter strings of every SGR sequence in ``text`` (for example ``"1;38;2;250;178;25"``)."""
    return set(_SGR.findall(text))
