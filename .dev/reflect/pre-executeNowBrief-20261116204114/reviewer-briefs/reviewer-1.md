# Reviewer 1 brief (analyzer persona, model class sonnet)

## T1 card excerpt

## Findings (each grounded; path:line re-read in this run)

F1. Task 4 acceptance cannot pass as written. plan:63 says "Grep finds no `closure_evidence`, `never_read` or `CLOSURE_EVIDENCE` in `src/superclaude/cli/observe` or `tests/observe`". The plan edits only tests/observe/test_questions.py :46, :52, :98 (plan:60), so the kept test at tests/observe/test_questions.py:50 `test_nothing_is_ever_closed_and_closure_evidence_is_unavailable` still contains the string `closure_evidence`. tests/observe/test_view.py:174 `test_a_released_row_without_an_outcome_never_reads_done_complete_or_settled` contains the substring `never_read`. Both are unrelated to the removed properties. An executor following the criterion literally cannot pass it, and the plan forbids renaming or deleting that test (plan:65). After :52 is deleted that test's name also claims something it no longer asserts.

F2. Task 5 acceptance cannot pass as written. plan:72 says Grep for `question_fixture` and `_question_index` "finds only the string code `no-question-fixture`". The plan renames the test to `test_a_fixture_source_has_no_question_fixture` (plan:69), which contains `question_fixture`; the current name at tests/observe/test_collector.py:662 does too. The hyphenated code `no-question-fixture` does not match the underscore pattern at all, so the criterion is wrong in both directions.

F3. A source requirement is dropped. source.md:49-53 ("Acceptance for the whole package") has three checks: the final pytest count equals 694 minus removed tests, the `grep -rn "run-use"` check, and the `git status --short` scope check. The plan has no whole-package acceptance and no task that runs those checks; plan:21, :123 and :127 mention run-use only as a "keep" instruction. The final count is never stated (the plan only says Task 1 removes 9 cases and Task 9 removes 1, so 684).

F4. Line numbers that the plan itself will shift. plan:69 (Task 5) and plan:143 (Task 12) cite `commands.py:177-178` as the `--questions` with `--fixture` refusal. Live today: src/superclaude/cli/observe/commands.py:177-178. Task 4 deletes commands.py:142 (plan:60), so after Task 4 the lines are 176-177. Task 12 writes that citation into a design document, where it would be wrong from the day it is written.

F5. Task 1 leaves an orphan comment. src/superclaude/cli/observe/terminal.py:41 reads "# Palette table (CD-8): empty, so every style is plain text and meaning lives in words." The plan deletes `PALETTE` at :42 and the attrs block :44-53 (plan:31) but not :41; source.md:19 gives the range :41-53. The comment would describe a table that no longer exists.

F6. Task 5 leaves an orphan comment. src/superclaude/cli/observe/collector.py:102 reads "# SYNTHETIC question cycles: each an envelope dict or ``{"fail": <code>}``." The plan removes :103 and :104 state (plan:69) but not :102; source.md:19 gives :102-104.

F7. tests/observe/test_snapshot_schema.py:1 says "no ID assigned in acceptance-tests.md". Task 12 (plan:143) assigns the id in acceptance-tests.md, but no task updates this docstring, so it becomes false.

F8. The plan uses the label T7 for the debate row (Task 9, plan:107) and for the spec test T7 (Task 12, plan:143); T5, T8 and T9 are also spec test ids in acceptance-tests.md. Plan:51 does mark T34 as "spec test", but the other labels are not disambiguated.

## Verified true (re-Read in this run)
## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T20:41Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp

### .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:27-74
```markdown
## Phase 1: Remove production code that only tests call (R1 and T9)

## Task 1: Remove the unused palette, glyphs and box style from terminal.py and their tests (R1 part, T9)

Edit `src/superclaude/cli/observe/terminal.py`: delete `PALETTE` (:42), `_FORBIDDEN_ATTRS` with its comment (:44-53), `palette_style` (:161-172), the glyph entries `sep`, `vrule` and `cross` in the glyph table (:33, :37, :38), the `TerminalPolicy.box_style` property (:72-74), and the imports `from rich import box` (:18) and `from rich.style import Style` (:21) once Grep shows no remaining use in the file. Keep `safe_box=policy.ascii` in `make_console`.

Edit `tests/observe/test_terminal.py`: delete `test_colour_only_where_the_palette_sets_it` (:56-59), `test_palette_refuses_forbidden_styles` and `test_palette_accepts_plain_colour_and_bold` (:73-82), the T28 header comment (:62) and `test_no_blink_code_in_any_console_output` with its parametrize decorator (:65-70); drop the `box_style` assertion at :126; change the two `sep` assertions in `test_glyph_table_maps_to_ascii` (:132-133) to assert the `selected` glyph under the UTF and the ASCII policy instead; remove the `box` and `palette_style` imports if they become unused. The no-blink guard that survives is `tests/observe/test_render.py:182-190` (real screen, every width, both colour modes); do not edit that file in this task.

Acceptance criteria:
- Grep over `src/superclaude/cli/observe` and `tests/observe` finds no `PALETTE`, `_FORBIDDEN_ATTRS`, `palette_style`, `box_style`, or glyph names `"sep"`, `"vrule"`, `"cross"`.
- `tests/observe/test_render.py:182-190` (no blink) still exists and passes; the `safe_box` test around `tests/observe/test_terminal.py:142-149` and the ASCII-mode test pass.
- The task states the number of test functions it deleted (expected 4: the palette-colour test, the forbidden-styles test, the plain-colour test and the no-blink test) and the number of collected cases that disappear (expected 9: the forbidden-styles test runs 5 cases and the no-blink test 2), and the gate passes with the passed count lower by exactly that number.

## Task 2: Remove the unused CODES set from adapter.py (R1 part)

Edit `src/superclaude/cli/observe/adapter.py`: delete the `CODES` frozenset (:65-82) and reword the comment at :340 (`# a code from CODES, or "exit:<n>"`) so it no longer names `CODES`. Edit `tests/observe/test_adapter.py`: delete only the assertion `assert expected in adapter.CODES` (:719); keep the exact-code assertion at :718 and the rest of `test_error_envelopes_map_to_source_codes_whatever_the_exit_status`.

Acceptance criteria:
- Grep for `\bCODES\b` over `src/superclaude/cli/observe` and `tests/observe` finds nothing.
- `tests/observe/test_adapter.py:718` still asserts the exact source code (`consumer-fenced` and `no-active-terminal`) and the test passes.
- No test function is deleted: the passed count is unchanged and the gate passes. `PKG/adapter.py`'s argv allow-list, forbidden prefixes and error mapping are otherwise unchanged (`git diff` of the file shows only the deleted set and the reworded comment).

## Task 3: Remove Fixture.parse from parse.py and route its test callers through parse_page and apply_frozen (R1 part)

Edit `src/superclaude/cli/observe/parse.py`: delete the `Fixture.parse` method (:723-733). Keep `Fixture.cycle` and `apply_frozen` (:736; also used by `PKG/collector.py:297`). Edit `tests/observe/test_fixtures.py`: the three callers (`fixture.parse(...)` at :44, :141 and :149) must call `parse_page(cycle.envelope, namespace, cycle_number, source_rank_base)` followed by `apply_frozen(parsed, cycle.frozen, source_rank_base)` through one small local helper in the test file, with the same arguments the removed method used. The frozen-marker test (`test_a_frozen_fixture_row_comes_out_of_the_loader_with_fixture_frozen_true`, spec test T34) and `test_every_variant_loads_and_every_cycle_parses` keep their names and assertions.

Acceptance criteria:
- Grep for `fixture.parse(` and `def parse(` inside the `Fixture` class finds nothing; `apply_frozen` and `parse_page` are still used by `PKG/collector.py`.
- Both tests named above pass with their original assertions, including that only `w-003` is frozen and that the source-rank offsets are honoured.
- No test function is deleted: the passed count is unchanged and the gate passes.

## Task 4: Remove closure_evidence, never_read, CLOSURE_EVIDENCE and Deps.extra (R1 part)

Edit `src/superclaude/cli/observe/questions.py`: delete the `closure_evidence` property (:70-72), the `never_read` property (:74-76) and the constant `CLOSURE_EVIDENCE` (:25). Edit `src/superclaude/cli/observe/commands.py`: delete the `extra` field of `Deps` (:142) and `field` from the `from dataclasses import dataclass, field` import (:14), after Grep confirms `field(` has no other use there and nothing passes `extra=` to `Deps`. Edit `tests/observe/test_questions.py`: at :46 change the tuple assertion to check only `state.last_read_cycle == 1`; delete the two `closure_evidence` assertions at :52 and :98. The on-screen wording `unavailable (no source)` stays pinned by `PKG/view.py` (`QUESTIONS_CLOSED`, :65, and the counts line, :693) and the view tests.

Acceptance criteria:
- Grep finds no `closure_evidence`, `never_read` or `CLOSURE_EVIDENCE` in `src/superclaude/cli/observe` or `tests/observe`, and no `extra:` field in `Deps`.
- `tests/observe/test_questions.py` tests for T11, T12 and the no-read-marker case still pass; the closure-wording assertions in `tests/observe/test_view.py` still pass.
- No test function is deleted: the passed count is unchanged and the gate passes.

## Task 5: Remove the synthetic question replay from FixtureSource (R1 part)

Edit `src/superclaude/cli/observe/collector.py`: in `FixtureSource` remove the `question_fixture` constructor argument (:97), `self._question_fixture` (:103), `self._question_index` and the replay loop in `read_questions` (:128-142); keep `read_questions` as a two-line method that returns `SourceResult("FAILED", code="no-question-fixture")` (the `CycleSource` protocol needs it). Edit `tests/observe/test_collector.py`: in `test_a_fixture_source_has_no_question_fixture_unless_one_is_supplied` keep the assertions up to the `no-question-fixture` check (:662-666), delete the synthetic-replay part (:667-678), and rename the test to `test_a_fixture_source_has_no_question_fixture` so the name is true. `--questions` with `--fixture` stays refused at `PKG/commands.py:177-178`.

Acceptance criteria:
- Grep for `question_fixture` and `_question_index` finds only the string code `no-question-fixture`.
- The refusal test for `--questions` with `--fixture` in `tests/observe/test_commands.py` and the collector tests that use `FixtureSource` pass; `FixtureSource` still satisfies the `CycleSource` protocol (the collector tests that build one with `questions=True` pass).
- No test function is deleted: the passed count is unchanged and the gate passes.
```

### src/superclaude/cli/observe/terminal.py:30-74
```python

# Glyph table: name -> (unicode form, ASCII form). Everything else non-ASCII maps to "?".
GLYPHS: dict[str, tuple[str, str]] = {
    "sep": ("·", "."),
    "selected": ("▸", "@"),
    "truncate": (">", ">"),
    "hrule": ("─", "-"),
    "vrule": ("│", "|"),
    "cross": ("┼", "+"),
}

# Palette table (CD-8): empty, so every style is plain text and meaning lives in words.
PALETTE: dict[str, str] = {}

# Style attributes the observer never uses; the background is never painted either.
_FORBIDDEN_ATTRS = (
    "blink",
    "blink2",
    "dim",
    "italic",
    "underline",
    "underline2",
    "conceal",
)


@dataclass(frozen=True)
class TerminalPolicy:
    width: int
    height: int
    no_color: bool
    ascii: bool
    width_class: str  # "full" | "line" | "short" | "narrow"

    @property
    def too_narrow(self) -> bool:
        return self.width_class == "narrow"

    @property
    def too_small(self) -> bool:
        return self.height < MIN_ROWS

    @property
    def box_style(self) -> box.Box:
        return box.ASCII if self.ascii else box.SQUARE
```

### src/superclaude/cli/observe/collector.py:92-141
```python
class FixtureSource:
    """Replays a fixture variant's cycles in order and repeats the last (never calls Orca)."""

    mode = "fixture"

    def __init__(self, variant: str, question_fixture: list | None = None) -> None:
        self.variant = variant
        self._fixture = load_fixture(variant)
        self._index = 0
        self.frozen_positions: frozenset = frozenset()  # of the cycle read last
        # SYNTHETIC question cycles: each an envelope dict or ``{"fail": <code>}``.
        self._question_fixture = question_fixture
        self._question_index = 0

    @property
    def available(self) -> bool:
        return True

    @property
    def namespace(self) -> str:
        return f"fixture:{self.variant}"

    def read_pages(
        self,
        clock: Any,
        budget_deadline: float,
        run_id: str | None = None,
        max_calls: int = 5,
    ) -> SourceResult:
        entry = self._fixture.cycle(self._index)
        self._index += 1
        self.frozen_positions = entry.frozen
        if entry.envelope is None:
            return SourceResult("FAILED", code=entry.fail)
        return SourceResult("OK", pages=(entry.envelope,), calls=1)

    def read_questions(
        self, clock: Any, budget_deadline: float, run_id: str
    ) -> SourceResult:
        """Replay the supplied synthetic question cycles, else fail with a plain code."""
        if not self._question_fixture:
            return SourceResult("FAILED", code="no-question-fixture")
        entry = self._question_fixture[
            min(self._question_index, len(self._question_fixture) - 1)
        ]
        self._question_index += 1
        if isinstance(entry, dict) and "fail" in entry and "result" not in entry:
            return SourceResult("FAILED", code=str(entry["fail"]))
        return SourceResult("OK", pages=(entry,), calls=1)

```

### src/superclaude/cli/observe/questions.py:19-77
```python
from superclaude.cli.observe.parse import UNKNOWN, Question

RETENTION_BOUND = 1000
WINDOW_ROWS = 100  # one read returning exactly this many rows may have lost older ones
NO_LONGER_IN_WINDOW = "no longer in source window"
RETENTION_EXCEEDED = "unknown (retention exceeded)"
CLOSURE_EVIDENCE = "unavailable (no source)"


@dataclass(frozen=True)
class QuestionRecord:
    key: tuple  # (Run id, message id)
    question: Question
    first_seen_cycle: int
    last_seen_cycle: int
    in_window: bool  # False: a later successful read did not return it

    @property
    def status_text(self) -> str:
        return "" if self.in_window else NO_LONGER_IN_WINDOW


@dataclass(frozen=True)
class QuestionState:
    """Immutable retained state. ``records`` are oldest created first, unknown created last."""

    records: tuple[QuestionRecord, ...] = ()
    evicted: int = 0  # records dropped at the bound; the open total counts them
    # Newest evicted keys, at most RETENTION_BOUND, so a re-seen one is not counted twice.
    # shortcut: an older evicted key that returns can be counted again; the total is
    # already "unknown (retention exceeded)" then. Upgrade only if exact counts are needed.
    evicted_keys: tuple = ()
    window_full: bool = False  # the last successful read returned exactly 100 rows
    last_read_cycle: int = 0  # cycle of the last successful question read; 0 = never
    identity_unknown_rows: int = (
        0  # rows of the last successful read with no id (not kept)
    )

    @property
    def retained(self) -> int:
        return len(self.records)

    @property
    def open_total(self) -> int:
        """Observed open questions: retained plus evicted. Never falls on eviction."""
        return len(self.records) + self.evicted

    @property
    def open_total_text(self) -> str:
        return RETENTION_EXCEEDED if self.evicted else str(len(self.records))

    @property
    def closure_evidence(self) -> str:
        return CLOSURE_EVIDENCE

    @property
    def never_read(self) -> bool:
        return self.last_read_cycle == 0

```

### tests/observe/test_questions.py:40-99
```python
def test_a_good_read_retains_rows_oldest_created_first_unknown_last():
    rows = [q(3), q(1, created=UNKNOWN), q(2)]
    state = merge_questions(None, rows, 1, False, True, RUN)
    assert ids(state) == ["msg_000002", "msg_000003", "msg_000001"]
    assert state.open_total == 3 and state.open_total_text == "3"
    assert state.retained == 3 and state.evicted == 0
    assert (state.last_read_cycle, state.never_read) == (1, False)
    assert all(r.in_window and r.first_seen_cycle == 1 for r in state.records)


def test_nothing_is_ever_closed_and_closure_evidence_is_unavailable():
    state = merge_questions(None, [q(1)], 1, False, True, RUN)
    assert state.closure_evidence == "unavailable (no source)"
    assert not any("closed" in f.name for f in dataclasses.fields(state.records[0]))
    assert not hasattr(state.records[0], "closed")


def test_t11_a_failed_read_keeps_every_record_and_changes_nothing():
    state = merge_questions(None, [q(1), q(2)], 1, True, True, RUN)
    after = merge_questions(state, [], 2, False, False, RUN)
    assert after is state
    assert after.window_full is True and after.last_read_cycle == 1
    assert ids(after) == ids(state)
    assert all(r.in_window for r in after.records)


def test_t12_a_question_missing_from_the_next_good_read_stays_marked():
    first = merge_questions(None, [q(1), q(2)], 1, False, True, RUN)
    second = merge_questions(first, [q(2), q(3)], 2, False, True, RUN)
    by_id = {r.question.qid: r for r in second.records}
    assert set(by_id) == {"msg_000001", "msg_000002", "msg_000003"}
    assert by_id["msg_000001"].in_window is False
    assert by_id["msg_000001"].status_text == NO_LONGER_IN_WINDOW
    assert by_id["msg_000001"].last_seen_cycle == 1
    assert by_id["msg_000002"].in_window and by_id["msg_000002"].first_seen_cycle == 1
    assert by_id["msg_000002"].last_seen_cycle == 2
    assert by_id["msg_000003"].first_seen_cycle == 2
    assert (
        second.open_total == 3
    )  # a question leaving the window never lowers the total
    third = merge_questions(second, [q(1)], 3, False, True, RUN)  # it comes back
    assert {r.question.qid: r.in_window for r in third.records}["msg_000001"] is True


def test_an_empty_good_read_keeps_everything_marked_and_never_closes():
    first = merge_questions(None, [q(1), q(2)], 1, False, True, RUN)
    second = merge_questions(first, [], 2, False, True, RUN)
    assert second.open_total == 2
    assert all(not r.in_window for r in second.records)


def test_a_handled_question_that_orca_still_returns_is_listed_again_as_open():
    # Known limit: ``check --all`` rows carry no read or acknowledged marker (REPORT 2.2,
    # steps 8 and 9), so the observer cannot tell a handled question from a fresh one.
    first = merge_questions(None, [q(1)], 1, False, True, RUN)
    handled_and_still_returned = merge_questions(first, [q(1)], 2, False, True, RUN)
    (record,) = handled_and_still_returned.records
    assert record.in_window and handled_and_still_returned.open_total == 1
    assert handled_and_still_returned.closure_evidence == "unavailable (no source)"

```

### tests/observe/test_collector.py:662-678
```python
def test_a_fixture_source_has_no_question_fixture_unless_one_is_supplied(fake_clock):
    plain = Collector(FixtureSource("base"), fake_clock, run_id=QRUN, questions=True)
    result = plain.run_once()
    assert result.state == "OK" and result.question_state == "FAILED"
    assert result.question_code == "no-question-fixture"
    synthetic = [json.loads(question_reply((1, 2))[1]), {"fail": "timeout"}]
    supplied = Collector(
        FixtureSource("base", question_fixture=synthetic),
        fake_clock,
        run_id=QRUN,
        questions=True,
    )
    first = supplied.run_once()
    assert first.question_state == "OK" and first.questions.retained == 2
    second = supplied.run_once()
    assert (second.question_state, second.question_code) == ("FAILED", "timeout")
    assert second.questions is first.questions
```

### tests/observe/test_terminal.py:56-83
```python
def test_colour_only_where_the_palette_sets_it():
    assert terminal.PALETTE == {}  # CD-8: empty palette, plain text
    assert not palette_style("anything")  # a null style
    assert "\x1b" not in render(policy(), palette_style("anything"))


# -- T28: no blink, faint, italic, underline ------------------------------------


@pytest.mark.parametrize("env", [{}, {"NO_COLOR": "1"}])
def test_no_blink_code_in_any_console_output(env):
    for style in ("bold", "red", "green on black", "reverse"):
        out = render(policy(env), style)
        params = [p for m in SGR.findall(out) for p in m.split(";")]
        assert "5" not in params and "6" not in params


@pytest.mark.parametrize("spec", ["blink", "dim", "italic", "underline", "on red"])
def test_palette_refuses_forbidden_styles(monkeypatch, spec):
    monkeypatch.setitem(terminal.PALETTE, "bad", spec)
    with pytest.raises(ValueError):
        palette_style("bad")


def test_palette_accepts_plain_colour_and_bold(monkeypatch):
    monkeypatch.setitem(terminal.PALETTE, "ok", "bold red")
    assert palette_style("ok").bold

```

### tests/observe/test_terminal.py:111-136
```python
@pytest.mark.parametrize(
    ("encoding", "flags", "expected"),
    [
        ("utf-8", None, False),
        ("UTF-8", {}, False),
        ("utf8", {}, False),
        ("ascii", {}, True),
        ("latin-1", {}, True),
        (None, {}, True),
        ("utf-8", {"ascii": True}, True),
    ],
)
def test_ascii_mode_from_flag_or_non_utf8_encoding(encoding, flags, expected):
    pol = policy(encoding=encoding, flags=flags)
    assert pol.ascii is expected
    assert pol.box_style is (box.ASCII if expected else box.SQUARE)


def test_glyph_table_maps_to_ascii():
    ascii_pol = policy(flags={"ascii": True})
    utf_pol = policy()
    assert terminal.glyph("sep", utf_pol) == "·"
    assert terminal.glyph("sep", ascii_pol) == "."
    assert terminal.glyph("selected", ascii_pol) == "@"
    assert all(terminal.glyph(name, ascii_pol).isascii() for name in terminal.GLYPHS)

```

### src/superclaude/cli/observe/adapter.py:65-82
```python
# Closed set of source codes besides ``exit:<n>``.
CODES = frozenset(
    {
        "timeout",
        "spawn-error",
        "output-cap",
        "json",
        "shape",
        "not-found",
        "overrun",
        "cursor-rejected",
        "cursor-stalled",
        "empty-page",
        "consumer-fenced",
        "no-active-terminal",
        "no-question-fixture",
    }
)
```

### tests/observe/test_adapter.py:705-722
```python
@pytest.mark.parametrize(
    "code,expected",
    [
        ("consumer_fenced", "consumer-fenced"),
        ("no_active_terminal", "no-active-terminal"),
    ],
)
@pytest.mark.parametrize("status", [1, 0])
def test_error_envelopes_map_to_source_codes_whatever_the_exit_status(
    code, expected, status, argv_log, fake_clock
):
    source, runner = source_with([error_reply(code, status)], argv_log)
    result = read_questions(source, fake_clock)
    assert (result.state, result.code, result.pages) == ("FAILED", expected, ())
    assert expected in adapter.CODES
    assert sum(1 for a in argv_log if a[1:3] == ["orchestration", "check"]) == 1
    assert runner.calls == 1

```

### src/superclaude/cli/observe/parse.py:714-749
```python
@dataclass(frozen=True)
class Fixture:
    variant: str
    cycles: tuple[FixtureCycle, ...]

    def cycle(self, index: int) -> FixtureCycle:
        """Cycle ``index`` (0-based); past the end the last cycle repeats."""
        return self.cycles[min(index, len(self.cycles) - 1)]

    def parse(
        self, index: int, namespace: str, cycle: int, source_rank_base: int = 0
    ) -> ParsedPage:
        """Parse a non-failing cycle with ``parse_page``, then mark frozen rows."""
        entry = self.cycle(index)
        if entry.envelope is None:
            raise ValueError(
                f"fixture cycle {index} is a failure ({entry.fail}), it has no page"
            )
        parsed = parse_page(entry.envelope, namespace, cycle, source_rank_base)
        return apply_frozen(parsed, entry.frozen, source_rank_base)


def apply_frozen(
    parsed: ParsedPage, frozen: frozenset, source_rank_base: int = 0
) -> ParsedPage:
    """Set ``fixture_frozen`` on the rows at the given raw positions (fixture mode only)."""
    if not frozen:
        return parsed
    rows = tuple(
        replace(row, fixture_frozen=True)
        if row.source_rank - source_rank_base in frozen
        else row
        for row in parsed.rows
    )
    return replace(parsed, rows=rows)

```

### tests/observe/test_fixtures.py:36-46
```python
@pytest.mark.parametrize("variant", VARIANTS)
def test_every_variant_loads_and_every_cycle_parses(variant):
    fixture = load_fixture(variant)
    assert fixture.variant == variant and fixture.cycles
    for index, cycle in enumerate(fixture.cycles):
        if cycle.fail is not None:
            assert cycle.envelope is None and cycle.fail
            continue
        page = fixture.parse(index, f"fixture:{variant}", index + 1)
        assert page.raw_count == len(cycle.envelope["result"]["workers"])

```

### tests/observe/test_fixtures.py:136-168
```python
# -- frozen marker (T34) ---------------------------------------------------------------------


def test_a_frozen_fixture_row_comes_out_of_the_loader_with_fixture_frozen_true():
    fixture = load_fixture("base")
    page = fixture.parse(0, "fixture:base", 1)
    frozen = [r.dispatch_id for r in page.rows if r.fixture_frozen]
    assert frozen == ["w-003"]
    assert "fixtureOnly" not in fixture.cycle(0).envelope["result"]["workers"][2]
    assert page.rows[2].unrecognised_keys == 0
    # source-rank offsets are honoured
    assert [
        r.dispatch_id
        for r in fixture.parse(0, "fixture:base", 1, 100).rows
        if r.fixture_frozen
    ] == ["w-003"]


def test_the_same_json_fed_straight_to_parse_page_leaves_it_false():
    raw = (
        resources.files(FIXTURE_PACKAGE)
        .joinpath("base.json")
        .read_text(encoding="utf-8")
    )
    import json

    envelope = json.loads(raw)["cycles"][0]
    page = parse_page(envelope, "fixture:base", 1)
    assert not any(r.fixture_frozen for r in page.rows)
    assert (
        page.rows[2].unrecognised_keys == 1
    )  # fixtureOnly is just an unknown key here

```

### src/superclaude/cli/observe/commands.py:125-143
```python

@dataclass
class Deps:
    """Everything outside the package, replaceable in tests. ``None`` means the real thing."""

    runner: Callable | None = None
    discover: Callable | None = None
    clock: Any = None
    env: Any = None
    encoding: str | None = None
    size: Callable[[], tuple[int, int]] | None = None
    platform: str | None = None
    key_source: Any = None
    screen_factory: Callable[[], Any] | None = None
    state_directory: Path | None = None
    stdout: Any = None
    interval: float | None = None
    extra: dict = field(default_factory=dict)

```

### src/superclaude/cli/observe/commands.py:168-188
```python
def _questions_on(options: Options) -> bool:
    """True only when ``--questions`` is asked for and the gate guard is open."""
    return bool(options.questions and QUESTION_GATE_PASSED)


def _question_refusal(options: Options) -> tuple[int, str] | None:
    """(exit code, plain message) when ``--questions`` cannot run; checked before any Orca call."""
    if not options.questions:
        return None
    if options.fixture:
        return 2, QUESTIONS_NEED_LIVE_TEXT
    if not options.run_id:
        return 2, QUESTIONS_NEED_RUN_TEXT
    try:
        check_run_id(options.run_id)
    except ArgvRejected as exc:
        return 2, f"--questions needs a valid --run id: {exc}"
    if not QUESTION_GATE_PASSED:
        return 1, QUESTION_GATE_TEXT
    return None

```


## Coverage slice

| Requirement | Plan item | Status | Grounding |
|---|---|---|---|
| INF-008 | Tasks 1-5 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:29-74 |
| INF-009 | Tasks 1-5 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:29-74 |
| INF-010 | Tasks 1-5 acceptance | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:35-38,44-47,53-56,62-65,71-74 |
| INF-011 | Task 1 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:33 |
| INF-012 | Task 6 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:78-87 |
| INF-013 | Task 7 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:89-96 |
