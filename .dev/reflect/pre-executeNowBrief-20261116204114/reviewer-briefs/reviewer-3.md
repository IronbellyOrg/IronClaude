# Reviewer 3 brief (refactorer persona, model class opus)

## T1 card excerpt

F4. Line numbers that the plan itself will shift. plan:69 (Task 5) and plan:143 (Task 12) cite `commands.py:177-178` as the `--questions` with `--fixture` refusal. Live today: src/superclaude/cli/observe/commands.py:177-178. Task 4 deletes commands.py:142 (plan:60), so after Task 4 the lines are 176-177. Task 12 writes that citation into a design document, where it would be wrong from the day it is written.

F5. Task 1 leaves an orphan comment. src/superclaude/cli/observe/terminal.py:41 reads "# Palette table (CD-8): empty, so every style is plain text and meaning lives in words." The plan deletes `PALETTE` at :42 and the attrs block :44-53 (plan:31) but not :41; source.md:19 gives the range :41-53. The comment would describe a table that no longer exists.

F6. Task 5 leaves an orphan comment. src/superclaude/cli/observe/collector.py:102 reads "# SYNTHETIC question cycles: each an envelope dict or ``{"fail": <code>}``." The plan removes :103 and :104 state (plan:69) but not :102; source.md:19 gives :102-104.

F7. tests/observe/test_snapshot_schema.py:1 says "no ID assigned in acceptance-tests.md". Task 12 (plan:143) assigns the id in acceptance-tests.md, but no task updates this docstring, so it becomes false.

F8. The plan uses the label T7 for the debate row (Task 9, plan:107) and for the spec test T7 (Task 12, plan:143); T5, T8 and T9 are also spec test ids in acceptance-tests.md. Plan:51 does mark T34 as "spec test", but the other labels are not disambiguated.

## Verified true (re-Read in this run)

- Every line range named for Tasks 1, 2, 3, 6, 7, 8, 9, 10, 11 and 12 matches live files (terminal.py:42,44-53,161-172,33,37,38,72-74,18,21; adapter.py:65-82,340; parse.py:177,195,409,647,723-733; view.py:209,732,693,718; export.py:14,18,24-25,29-34,195; test_render.py:95-100; test_question_quiet_scope.py:192-203; test_golden_contract.py:214-215,518-519; prd.md:106,491,423,469; SPEC.md:104,106; owner-decisions-and-risks.md:22,24; acceptance-tests.md:25,28,51,56,64-66).
- The 9-case count for Task 1 is right: 1 + 5 + 1 + 2.
- No protected rule is touched: QUESTION_GATE_TEXT (commands.py:68-70, pinned at tests/observe/test_commands.py:632) is outside every edit; the forbidden-word test at tests/observe/test_adapter.py:158-192 counts words in adapter.py and Task 2's deletion adds none; the SENSITIVE scan removed by Task 9 still runs over the same files via tests/observe/test_fixtures.py:185-191.
- The QUESTION-OBSERVATION text edits in Task 10 are not pinned by any test (no test greps "off until" or "refused until"); the pinned help phrases are tests/observe/test_commands.py:727, :728, :738.
- Dependency order is sound: Tasks 3 and 6 both edit parse.py, Tasks 4 and 10 both edit commands.py, Tasks 10 and 11 both edit prd.md; each pair is ordered.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T20:41Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp

### .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:76-115
```markdown
## Phase 2: Remove dead counters, one panel field and the production schema import (R3, R2, S2, T8, T5, T7)

## Task 6: Remove the two aggregate unrecognised-key counters from parse.py (R3)

Depends on: Task 3

Edit `src/superclaude/cli/observe/parse.py`: delete `ParsedPage.unrecognised_keys` (:177) and its sum in `parse_page`'s return (:409), and `Coverage.unrecognised_keys` (:195) and its sum (:647). Keep `_FIELDS`, `_KNOWN`, `_count_unexpected`, `_BLOCK_FIELDS` (:91-93, the sanitizer block mode), the per-row field and its count (:155, :356), and the inspector line in `PKG/view.py:407`. Adjust only test assertions that read an aggregate counter (a `page.unrecognised_keys` or `coverage.unrecognised_keys` access); the per-row reads in `tests/observe/test_parse.py:188`, `:198`, `tests/observe/test_fixtures.py:145`, `:166` and `tests/observe/test_view.py:722` stay.

Acceptance criteria:
- Grep for `unrecognised_keys` matches only the per-row field, the `_count_unexpected` call in the row builder, `PKG/view.py:407` and the per-row test reads; no page-level or coverage-level counter remains, and `PKG/export.py` and `PKG/view.py` do not read one.
- The row-level tests listed above pass unchanged.
- The gate passes and the passed count equals the count before the task, unless an aggregate-only assertion was removed from an otherwise kept test.

## Task 7: Remove QuestionsPanel.count_text (R2)

Edit `src/superclaude/cli/observe/view.py`: delete the `count_text` field of `QuestionsPanel` (:209) and its assignment `count_text=open_text` (:732). Keep `open_text` (it is also used at :693 and :718) and the other 21 fields; make no comment edits. Do not edit any golden file.

Acceptance criteria:
- Grep for `count_text` over `src/superclaude/cli/observe` and `tests/observe` finds nothing; `open_text` is still used by the counts line and the header cell.
- The panel tests (`tests/observe/test_question_cap.py:71-134`, `tests/observe/test_view.py`, `tests/observe/test_render.py`) and the questions-off golden test (`tests/observe/test_render.py:616-629`) pass with `tests/observe/golden_release1_surface.json` unchanged (`git diff` shows no change to it). The export fields `open_total`, `window_full`, `retained`, `evicted` read at `PKG/export.py:165-168` still work.
- No test function is deleted: the passed count is unchanged and the gate passes.

## Task 8: Move the snapshot schema load and validation out of export.py into the test conftest (S2)

Edit `src/superclaude/cli/observe/export.py`: remove the `from importlib import resources` import (:14), `from jsonschema import Draft7Validator` (:18), `SCHEMA_PACKAGE` and `SCHEMA_FILE` (:24-25), and the `SCHEMA` load plus `Draft7Validator.check_schema` call (:29-34); keep `SCHEMA_VERSION` (:23, used at :195) and re-check that `resources` has no other use in the file. Edit `tests/observe/conftest.py`: define `SCHEMA` there (read `snapshot.schema.json` from the package `superclaude.cli.observe` with `importlib.resources`, parse it, and run `Draft7Validator.check_schema` on it). Change the imports at `tests/observe/test_commands.py:34` and `tests/observe/test_snapshot_schema.py:15` to `from tests.observe.conftest import SCHEMA` (the style the tests already use for conftest helpers). In `tests/observe/test_snapshot_schema.py` (:52-72) remove only the assertion that now compares the file with a copy of itself (`assert json.loads(text) == SCHEMA`, :60) and any read that exists only for it; keep `Draft7Validator.check_schema(SCHEMA)`, the draft-07 `$schema` check and the closed-object checks.

Acceptance criteria:
- `PKG/export.py` no longer imports `jsonschema` or `importlib.resources` and defines no `SCHEMA`; Grep shows `SCHEMA` is read only from `tests/observe/conftest.py` by the two test modules.
- `tests/observe/test_snapshot_schema.py::test_the_schema_ships_in_the_package_is_draft_7_and_closed_on_the_producer_side` and every snapshot validation test still pass, and a snapshot written by `export.py` still validates against the schema.
- No test function is deleted: the passed count is unchanged and the gate passes.

## Task 9: Fix the vacuous render assertion and remove two duplicated test blocks (T8, T5, T7)

Edit `tests/observe/test_render.py` (T8): replace the assertion at :95-100 that ends in `or True` with `assert len(overflow) == 1`; keep all 27 cases of the test. If the corrected assertion fails, report that as a finding and do not loosen it. Edit `tests/observe/test_question_quiet_scope.py` (T5): delete only `test_t51_the_backend_refuses_every_consuming_argv_it_could_be_given` (:192-203, the test of the fake mailbox itself); keep :137-145, :148-171, :174-179 and :182-189 and the fake's own argv assertions. Edit `tests/observe/test_golden_contract.py` (T7): in the two golden leak scans delete only the duplicated `for what, pattern in SENSITIVE.items(): assert not pattern.search(...)` pairs (:214-215 and :518-519); keep the `isascii` checks (:213, :517), the 32-character rule (:216), the run, terminal and message id rule (:520) and :521-527; remove the `SENSITIVE` import there only if it becomes unused. The surviving guard for the removed scans is `tests/observe/test_fixtures.py:185-191`, which runs the same patterns over every packaged fixture.

Acceptance criteria:
- `tests/observe/test_render.py` has no `or True`; the test passes with all 27 parametrized cases.
- `test_t51_the_backend_refuses_every_consuming_argv_it_could_be_given` no longer exists; the other tests in `tests/observe/test_question_quiet_scope.py` pass; `tests/observe/test_adapter.py:158-192` still holds the forbidden-prefix tests.
- `tests/observe/test_golden_contract.py` still contains the 32-character rule and the id rule and passes; `tests/observe/test_fixtures.py:185-191` passes.
- The task states one deleted test function (T5) and the gate passes with the passed count reduced by exactly 1.
```

### src/superclaude/cli/observe/export.py:9-35
```python
from __future__ import annotations

import json
import os
import tempfile
from importlib import resources
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator

from superclaude.cli.observe.sanitize import sanitize
from superclaude.cli.observe.view import ORDER_UNKNOWN_FLAG, UNKNOWN, RowView, View

SCHEMA_VERSION = 1
SCHEMA_PACKAGE = "superclaude.cli.observe"
SCHEMA_FILE = "snapshot.schema.json"
SNAPSHOT_NAME = "snapshot.json"
UNKNOWN_TEXT = "UNKNOWN"  # the snapshot spelling of a missing value

SCHEMA: dict = json.loads(
    resources.files(SCHEMA_PACKAGE).joinpath(SCHEMA_FILE).read_text(encoding="utf-8")
)
Draft7Validator.check_schema(
    SCHEMA
)  # a broken schema fails at import, not in the field

```

### src/superclaude/cli/observe/export.py:159-170
```python

def _questions_dict(panel: Any) -> dict:
    """The optional ``questions`` group: ids, times and counts only (never subject or body)."""
    out: dict = {
        "runId": panel.run_id,
        "state": panel.state,
        "observedOpen": _unknown(panel.open_total),
        "windowFull": panel.window_full,
        "retained": panel.retained,
        "evicted": panel.evicted,
        "closureEvidence": "unavailable",
        "items": [
```

### tests/observe/test_snapshot_schema.py:1-22
```python
"""Snapshot v1 schema test (CAP-10, recorded owner decision 2; no ID assigned in acceptance-tests.md)."""

from __future__ import annotations

import copy
import json
import re
from importlib import resources

import pytest
from jsonschema import Draft7Validator

from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector, FixtureSource
from superclaude.cli.observe.export import SCHEMA, snapshot_json
from superclaude.cli.observe.parse import VARIANTS, load_fixture
from superclaude.cli.observe.view import Session, build_view
from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows

VALIDATOR = Draft7Validator(SCHEMA)


```

### tests/observe/test_snapshot_schema.py:51-75
```python
# -- the schema file ---------------------------------------------------------------------------------------------


def test_the_schema_ships_in_the_package_is_draft_7_and_closed_on_the_producer_side():
    text = (
        resources.files("superclaude.cli.observe")
        .joinpath("snapshot.schema.json")
        .read_text(encoding="utf-8")
    )
    assert json.loads(text) == SCHEMA
    Draft7Validator.check_schema(SCHEMA)
    assert SCHEMA["$schema"].endswith("draft-07/schema#")
    closed = [
        SCHEMA,
        SCHEMA["properties"]["producer"],
        SCHEMA["properties"]["source"],
        SCHEMA["properties"]["page"],
        SCHEMA["properties"]["collection"],
        SCHEMA["definitions"]["row"],
        SCHEMA["definitions"]["row"]["properties"]["stage"],
        SCHEMA["definitions"]["row"]["properties"]["liveness"],
        SCHEMA["definitions"]["row"]["properties"]["evidence"],
    ]
    assert all(node["additionalProperties"] is False for node in closed)

```

### tests/observe/test_commands.py:14-40
```python

import pytest
from click.testing import CliRunner
from jsonschema import Draft7Validator
from rich.cells import cell_len

import superclaude.cli.observe as observe_pkg
import superclaude.cli.observe.commands as commands
from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector, FixtureSource
from superclaude.cli.observe.commands import (
    NO_TERMINAL_TEXT,
    POSIX_ONLY_TEXT,
    Deps,
    Options,
    SystemClock,
    execute,
    observe_group,
    run_loop,
)
from superclaude.cli.observe.export import SCHEMA
from superclaude.cli.observe.view import GAP_NOTICE, Key
from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows

VALIDATOR = Draft7Validator(SCHEMA)
KEYS_MODULE = "superclaude.cli.observe.keys"

```

### tests/observe/test_render.py:80-107
```python
@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize("n_runs", [5, 8, 10])
@pytest.mark.parametrize("n_rows", [50, 80, 100])
def test_matrix_lines_fit_counts_are_k_of_n_and_overflow_names_the_total(
    fake_clock, n_rows, n_runs, width
):
    view = generated_view(fake_clock, n_rows, n_runs)
    policy = policy_for(width, height=30)
    lines = screen_lines(view, policy)
    assert all(cell_len(line) <= width for line in lines)
    assert len(lines) <= 30
    for line in lines:
        for k, n in re.findall(r"(\d+) of (\d+)", line):
            assert int(k) <= int(n)
    overflow = [l for l in lines if re.match(r"^\d+/\d+ shown", l)]
    assert (
        len(overflow) == 1
        and overflow[0].startswith(f"{len(view.window(30).rows) if False else ''}")
        is True
        or True
    )
    x, y = map(int, re.match(r"^(\d+)/(\d+) shown", overflow[0]).groups())
    assert y == n_rows and x < y and f"+{y - x} more" in overflow[0]
    assert any(
        l.endswith(f"| collected {n_rows} / reported {n_rows}")
        or f"collected {n_rows} / reported {n_rows}" in l
        for l in lines
    )
```

### tests/observe/test_question_quiet_scope.py:137-204
```python
def test_t51_repeated_reads_on_a_quiet_scope_leave_ids_order_and_mailbox_unchanged():
    backend = FakeOrcaMailbox(probe_rows(6))
    ids = observe_quiet_scope(backend, cycles=5)
    assert len(ids) == 6 and ids == sorted(ids)  # oldest created first, stable
    assert (
        backend.reads == 6 and backend.delivery is None and backend.acknowledged == []
    )
    assert PASS_SCOPE.startswith("a pass covers only the visible effects tested")
    assert all(row["delivered_at"] is None for row in backend.rows), PASS_SCOPE


def test_t51_the_observer_never_sends_a_consuming_or_narrowing_argv():
    backend = FakeOrcaMailbox(probe_rows(3))
    log = []

    def spy(argv, timeout):
        log.append(list(argv))
        return backend(argv, timeout)

    clock = FakeClock()
    collector = Collector(
        LiveSource(FakeRunner([], [spy]), FakeDiscover([])),
        clock,
        run_id=QRUN,
        questions=True,
    )
    for _ in range(3):
        collector.run_once()
        clock.advance(15.0)
    messages = [a for a in log if "check" in a]
    assert len(messages) == 3 and all(a[1:6] == QUESTION_BASE for a in messages)
    for argv in log:
        for token in CONSUMING_TOKENS:
            assert token not in argv
    assert all(a.count("check") == 1 and "--all" in a for a in messages)


def test_t51_a_consuming_fake_makes_the_same_check_fail_so_the_test_can_detect_it():
    backend = FakeOrcaMailbox(probe_rows(4))
    backend.consuming = True
    with pytest.raises(AssertionError, match="changed the mailbox state"):
        observe_quiet_scope(backend, cycles=3)
    assert backend.delivery is not None  # the fake really did consume


def test_t51_the_check_is_sensitive_to_a_new_question_so_quiet_means_no_sender_write():
    backend = FakeOrcaMailbox(probe_rows(3))
    clock = FakeClock()
    collector = observer_over(backend, clock)
    before = [r.question.qid for r in collector.run_once().questions.records]
    backend.send(make_question_rows(1, start=10))  # a sender writes: not a quiet scope
    after = [r.question.qid for r in collector.run_once().questions.records]
    assert after != before and set(before) < set(after)


def test_t51_the_backend_refuses_every_consuming_argv_it_could_be_given():
    backend = FakeOrcaMailbox(probe_rows(1))
    bad = [
        ["/o", "orchestration", "check", "--json"],
        ["/o", "orchestration", "check", "--all", "--ack", "d1"],
        ["/o", "orchestration", "check", "--all", "--wait"],
        ["/o", "orchestration", "check", "--peek", "--types", "question"],
    ]
    for argv in bad:
        with pytest.raises(AssertionError):
            backend(argv, 1.0)
    assert backend.reads == 0 and backend.delivery is None
```

### tests/observe/test_golden_contract.py:203-217
```python
# -- nothing sensitive is committed ---------------------------------------------------------------------------------------------


@pytest.mark.parametrize("name", GOLDEN)
def test_golden_files_hold_no_path_handle_token_credential_url_or_escape_byte(name):
    text = (
        resources.files(FIXTURE_PACKAGE)
        .joinpath(f"{name}.json")
        .read_text(encoding="utf-8")
    )
    assert "\x1b" not in text and text.isascii()
    for what, pattern in SENSITIVE.items():
        assert not pattern.search(text), f"{name}: {what}"
    assert not re.search(r"[A-Za-z0-9_+=-]{32,}", text.replace("redacted", ""))

```

### tests/observe/test_golden_contract.py:506-528
```python


@pytest.mark.parametrize("name", QUESTION_GOLDEN)
def test_question_golden_files_hold_no_path_handle_token_credential_url_or_escape_byte(
    name,
):
    text = (
        resources.files(FIXTURE_PACKAGE)
        .joinpath(f"{name}.json")
        .read_text(encoding="utf-8")
    )
    assert "\x1b" not in text and text.isascii()
    for what, pattern in SENSITIVE.items():
        assert not pattern.search(text), f"{name}: {what}"
    assert not re.search(r"run_[0-9a-f]{12}|term_|msg_[0-9a-f]*[a-f][0-9a-f]*\b", text)
    for cycle in load_fixture(name).cycles:
        for message in ((cycle.envelope or {}).get("result") or {}).get("messages", []):
            assert set(message) == MESSAGE_KEYS  # key names kept, none added
            assert (
                message["body"] == "redacted" and message["from_handle"] == "redacted"
            )
            assert re.fullmatch(r"msg_\d{12}", message["id"])

```

### tests/observe/test_fixtures.py:170-192
```python
# -- nothing sensitive in committed fixtures -------------------------------------------------

SENSITIVE = {
    "absolute path": re.compile(
        r"(?<![\w.:/-])/(?:home|Users|tmp|var|etc|usr|opt|root|mnt|srv)/|\b[A-Za-z]:\\\\"
    ),
    "terminal handle": re.compile(r"term_"),
    "token": re.compile(
        r"sk-[A-Za-z0-9]{16,}|gh[pousr]_[A-Za-z0-9]{16,}|xox[abprs]-|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{10,}"
        r"|[A-Fa-f0-9]{32,}|Bearer\s+\S+|(?i:secret|password|api[_-]?key)\"?\s*[:=]"
    ),
    "credential url": re.compile(r"://[^/\s\"]*:[^/\s\"]*@"),
}


@pytest.mark.parametrize("path", fixture_files(), ids=lambda p: p.name)
def test_committed_fixtures_hold_no_path_handle_token_or_escape_byte(path):
    text = path.read_text(encoding="utf-8")
    assert "\x1b" not in text
    assert not any(ord(ch) < 0x20 and ch not in "\n" for ch in text)
    for what, pattern in SENSITIVE.items():
        assert not pattern.search(text), f"{path.name}: {what}"

```

### src/superclaude/cli/observe/view.py:195-222
```python
@dataclass(frozen=True)
class QuestionsPanel:
    """The R2 panel for one named Run (adapter-contract.md "R2 onward", rendering-rules.md)."""

    run_id: str
    state: str  # "PENDING" | "OK" | "STALE" | "FAILED"
    code: str | None
    title: str
    run_line: str
    disclosure: str
    state_lines: tuple[str, ...]  # the first line always names the state of the read
    counts_line: str
    caveat_line: str  # the source has no read marker
    header_cell: str  # the freshness-strip cell, with the same state words
    count_text: str  # the count as a phrase, never a bare number when it may be partial
    lines: tuple[QuestionLine, ...]  # oldest created first
    empty_text: str | None
    window_full_text: str | None
    notes: tuple[str, ...]
    retention_line: str
    summary: str  # one line; stands in for the gap notice once the source has read
    replaces_gap: bool
    open_total: Any  # int, or UNKNOWN when retention was exceeded or nothing was read
    retained: int
    evicted: int
    window_full: bool

    def window(
```

### src/superclaude/cli/observe/view.py:715-735
```python
        clock.wall() if since is None else since, clock.local_tz(), "%H:%M"
    )
    summary = (
        f"coordinator questions: {QUESTIONS_COUNT_LABEL} {open_text}; {status}; "
        f"one Run only: {run}; best effort, coverage unknown"
    )
    return QuestionsPanel(
        run_id=run,
        state=state,
        code=code,
        title=QUESTIONS_TITLE,
        run_line=f"one Run only: {run}",
        disclosure=QUESTIONS_DISCLOSURE,
        state_lines=tuple(state_lines),
        counts_line=counts_line,
        caveat_line=QUESTIONS_NO_MARKER,
        header_cell=header_cell,
        count_text=open_text,
        lines=lines,
        empty_text=empty_text,
        window_full_text=QUESTIONS_WINDOW_FULL if window_full else None,
```

### src/superclaude/cli/observe/parse.py:150-200
```python
        str, ...
    ] = ()  # attributes that are UNKNOWN because the source omitted them
    flags: tuple[
        str, ...
    ] = ()  # "identity unknown", "order unknown", "conflict (time went back)"
    unrecognised_keys: int = 0
    reobserved: bool = True
    fixture_frozen: bool = False  # set only by the fixture loader, never by parse_page

    @property
    def identity_unknown(self) -> bool:
        return IDENTITY_UNKNOWN in self.flags


@dataclass(frozen=True)
class ParsedPage:
    rows: tuple[Row, ...]
    raw_count: int  # entries in result.workers, malformed ones included
    cycle: int
    namespace: str
    has_more: bool
    total: Any = UNKNOWN  # int or UNKNOWN
    limit: Any = UNKNOWN  # int or UNKNOWN
    scope: Any = UNKNOWN  # sanitized object or UNKNOWN
    counts: Any = UNKNOWN  # sanitized object, passed through, never summed
    warnings: tuple[str, ...] = ()
    malformed_rows: int = 0
    unrecognised_keys: int = 0


@dataclass(frozen=True)
class Coverage:
    page_totals: tuple = ()  # result.page.total of each page read (int or UNKNOWN)
    pages_read: int = 0
    empty_page: int | None = (
        None  # 1-based index of a page with no workers while its total is above 0
    )
    has_more_at_stop: bool = False
    duplicates: int = 0
    total_changed: bool = False  # page.total differed between pages
    stopped_by_cap: bool = False
    stopped_by_error: str | None = None
    collected: int = 0  # distinct rows read this cycle
    identity_unknown_rows: int = 0
    malformed_rows: int = 0
    unrecognised_keys: int = 0

    @property
    def reported_total(self) -> Any:
        """``page.total`` of the last page read (``UNKNOWN`` when it was absent)."""
        return self.page_totals[-1] if self.page_totals else UNKNOWN
```


## Coverage slice

| Requirement | Plan item | Status | Grounding |
|---|---|---|---|
| INF-014 | Task 8 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:98-105 |
| INF-015 | Task 9 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:107-115 |
| INF-016 | Task 9 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:107-115 |
| INF-017 | Task 9 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:107-115 |
| INF-012 | Task 6 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:78-87 |
| INF-013 | Task 7 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:89-96 |
