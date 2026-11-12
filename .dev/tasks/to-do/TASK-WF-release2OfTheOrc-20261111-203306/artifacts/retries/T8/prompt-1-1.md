759924f31781b03261c9a62851e99dbafd5455f0
Review one task for spec compliance.

Task brief: 
## Task 8: Build the question retention store in questions.py

Depends on: Task 7

Create `src/superclaude/cli/observe/questions.py` and `tests/observe/test_questions.py` (SPECDIR `adapter-contract.md` "R2 onward" as rewritten by Task 4; PRD FR-17).

- A pure store, no I/O: `merge_questions(previous, parsed_rows, cycle, window_full, source_ok)` returns a new immutable state. Keyed by (Run, `qid`). Each record keeps `first_seen_cycle`, `last_seen_cycle`, `in_window` and the `Question` fields.
- A question seen before and absent from a later successful read stays and is marked `no longer in source window`. A failed question read changes nothing. Nothing is ever marked closed: closure evidence is `unavailable (no source)`.
- Bound 1,000 records; when exceeded the oldest-created record is evicted, an `evicted` counter grows, the open total never goes down, and `open_total_text` reads `unknown (retention exceeded)` with the retained count shown. Order is oldest created first, unknown created time last.
- `window_full` is true when one read returned exactly 100 messages; it is carried in the state for the disclosure.

Acceptance criteria:
- `uv run pytest tests/observe/test_questions.py -v` passes: T46 (1,001 distinct questions keep the open total from falling and show `unknown (retention exceeded)` with 1,000 retained); T11 (a failed read keeps every record); T12 (a question missing from the next successful read stays, marked `no longer in source window`); a handled question that Orca still returns is listed again as open (no read marker exists), asserted by a test that names this limit.
- Two Runs' questions with the same `qid` stay two records (key includes the Run).

Global constraints: 
## Constraints

- Shorthand. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`. PKG is `src/superclaude/cli/observe/`. TESTS is `tests/observe/`. REPORT is the file `RESEARCH-REPORT-phase2-gate.md` in the folder `TASK-RESEARCH-phase2-gate-20261111-200400` under `.dev/tasks/` (the folder may sit in to-do or done); its recorded evidence is the `research/evidence/` folder next to it, files numbered 01 to 27. OWNER is `.dev/issues/409/owner-decisions-20261111.md`. "The probe shapes" are the recorded outputs in REPORT's evidence folder: envelope `{id, ok, result:{acknowledged, count, messages[], runId}, _meta}`; message row keys `id` (msg_...), `run_id`, `delivery_contract`, `from_handle`, `to_handle`, `subject`, `body`, `type`, `priority`, `thread_id`, `payload`, `created_at`, `delivered_at`; error envelope `{ok:false, error:{code, message}}` with codes `consumer_fenced` (exit status 1) and `no_active_terminal`.
- Scope is release 2 only, as fixed by OWNER and REPORT sections 7 to 9. Decision 8: only messages of type `question`, labelled "coordinator questions", never "human". Decision 6: read permission for one named Run, `--types question`, never `run-use`. The owner has not yet named the Run (open question for the owner; Task 17 is blocked until they do).
- Fixed design basis, not reopened. One named Run only; no rotation across Runs; the observer runs where it already holds the Run. Every read passes `--types question`. Only `check --all` is used: `--peek` hides acked rows so it is not a source. Question identity is `message.id`, labelled UNVERIFIED for any Run other than the probe Runs and the coordinator's own Run; a worker `dispatchId` is never a question identity. The disclosure text, verbatim, is `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`.
- UNVERIFIED facts that stay gated risks, each with a named verification task and never an assumption. Q-1: whether an observer terminal that has a handle but holds no Run can read (Task 16). Q-2: the effect of `run-use` on a live coordinator (not tested, forbidden for the observer; Task 6 pins `run-use` as a forbidden argv and Task 2 records Q-2 as never tested). Message rate on a Run other than the coordinator's own, and identity on real traffic (Task 17). Whether `ask` writes type `question` (Q-3) is recorded in the register as UNVERIFIED; no R2 behaviour depends on it because the label says "coordinator questions" and the observer lists type `question` rows however they were written.
- Safety. No consuming read (`check` without `--all` or `--peek`, `check --ack`), no `run-use`, `run-create`, `send`, `ask`, `reply` or `reset` against any Run except where a task names a throwaway probe Run and a non-consuming form. Raw Orca output is never logged, committed or exported; committed samples hold only redacted values (no terminal handle, token, credential or absolute path). Bodies of messages are received by the observer process (acquisition cannot be undone by dropping them at parse time), so the design never claims bodies were not acquired; it only does not keep or show them.
- Rules carried from release 1. UV only (`uv run pytest ...`). Python 3.10 compatible, no new dependency. A fact the source does not give is the `UNKNOWN` sentinel and renders as `unknown`; unknown is never 0, false, blank or `null`. Source loss never closes a question, lowers an open count or turns a value into `failed`. Every source string passes `sanitize` before it reaches the view model; strings render as literal text, never Rich markup; truncation uses cell width. Plan edits touch only `src/`, `tests/`, `.dev/issues/409/` and this package's `./artifacts/`; nothing under `.claude/`.
- Out of scope: R3 links (QUESTION-LINK), `inbox`, closure evidence, history beyond the 100-row window, `--include-remote`, write-back, per-question selection and marking (the `m` key keeps its release 1 meaning), any message call other than the one template.
- Plan-author choices (PROPOSED, the owner may change them). The opt-in flag is `--questions`, valid only with `--run <runId>` and a live source. The message call budget is one call per cycle; when questions are on, worker-list paging is limited to 4 calls so the cycle total stays inside the 5-call cap. The panel shows `subject` and age only, never `body`. The reason column reads `reason unknown` because no verified reason field exists. Retention is in memory for the process, bounded at 1,000 records.
- Gate honesty. QUESTION-OBSERVATION is NOT passed as of this plan: proof (a) failed as worded, proof (b) is partly proven, proof (c) is unmeasured, non-consumption passed only as the Run's owner on a probe Run. The live question read is guarded by one constant that Task 18 may flip only against an owner-written record.

Start sha: 759924f31781b03261c9a62851e99dbafd5455f0
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/questions.py b/src/superclaude/cli/observe/questions.py
new file mode 100644
index 000000000..c594a6857
--- /dev/null
+++ b/src/superclaude/cli/observe/questions.py
@@ -0,0 +1,140 @@
+"""Question retention for the R2 coordinator-questions panel (adapter-contract.md, "R2 onward").
+
+A pure store with no I/O. Questions are kept by (Run, ``message.id``) until closure evidence
+is seen; no closure source exists, so nothing is ever closed. A question that a later
+successful read no longer returns stays, marked ``no longer in source window``. A failed
+read changes nothing. The store is bounded at 1,000 records; the open total never falls, so
+beyond the bound it reads ``unknown (retention exceeded)`` with the retained count.
+
+Limit (no read marker): ``check --all`` rows carry no read or acknowledged marker, so a
+question the coordinator already handled is listed again as open for as long as Orca still
+returns it. ``seen`` is not ``resolved``, and neither is "handled".
+"""
+
+from __future__ import annotations
+
+from dataclasses import dataclass, replace
+from typing import Any
+
+from superclaude.cli.observe.parse import UNKNOWN, Question
+
+RETENTION_BOUND = 1000
+WINDOW_ROWS = 100  # one read returning exactly this many rows may have lost older ones
+NO_LONGER_IN_WINDOW = "no longer in source window"
+RETENTION_EXCEEDED = "unknown (retention exceeded)"
+CLOSURE_EVIDENCE = "unavailable (no source)"
+
+
+@dataclass(frozen=True)
+class QuestionRecord:
+    key: tuple  # (Run id, message id)
+    question: Question
+    first_seen_cycle: int
+    last_seen_cycle: int
+    in_window: bool  # False: a later successful read did not return it
+
+    @property
+    def status_text(self) -> str:
+        return "" if self.in_window else NO_LONGER_IN_WINDOW
+
+
+@dataclass(frozen=True)
+class QuestionState:
+    """Immutable retained state. ``records`` are oldest created first, unknown created last."""
+
+    records: tuple[QuestionRecord, ...] = ()
+    evicted: int = 0  # records dropped at the bound; the open total counts them
+    window_full: bool = False  # the last successful read returned exactly 100 rows
+    last_read_cycle: int = 0  # cycle of the last successful question read; 0 = never
+    identity_unknown_rows: int = (
+        0  # rows of the last successful read with no id (not kept)
+    )
+
+    @property
+    def retained(self) -> int:
+        return len(self.records)
+
+    @property
+    def open_total(self) -> int:
+        """Observed open questions: retained plus evicted. Never falls on eviction."""
+        return len(self.records) + self.evicted
+
+    @property
+    def open_total_text(self) -> str:
+        return RETENTION_EXCEEDED if self.evicted else str(len(self.records))
+
+    @property
+    def closure_evidence(self) -> str:
+        return CLOSURE_EVIDENCE
+
+    @property
+    def never_read(self) -> bool:
+        return self.last_read_cycle == 0
+
+
+def _order(record: QuestionRecord) -> tuple:
+    epoch = record.question.created_epoch
+    known = epoch is not UNKNOWN
+    return (not known, epoch if known else 0.0, str(record.key[0]), str(record.key[1]))
+
+
+def _key(question: Question, run_id: Any) -> tuple:
+    run = question.run_id if question.run_id is not UNKNOWN else run_id
+    return (run, question.qid)
+
+
+def merge_questions(
+    previous: QuestionState | None,
+    parsed_rows: Any,
+    cycle: int,
+    window_full: bool,
+    source_ok: bool,
+    run_id: Any = UNKNOWN,
+) -> QuestionState:
+    """Return the new retained state; ``previous`` is never modified.
+
+    ``source_ok`` False (a failed read) returns ``previous`` unchanged. A row with no
+    identity is counted and not retained. ``run_id`` is the Run that was read, used for a
+    row that carries no ``run_id`` of its own.
+    """
+    state = previous if previous is not None else QuestionState()
+    if not source_ok:
+        return state
+    seen: dict[tuple, Question] = {}
+    anonymous = 0
+    for question in parsed_rows:
+        if question.qid is UNKNOWN or question.identity_unknown:
+            anonymous += 1
+            continue
+        seen[_key(question, run_id)] = question
+    records: dict[tuple, QuestionRecord] = {}
+    for record in state.records:
+        if record.key in seen:
+            records[record.key] = replace(
+                record,
+                question=seen[record.key],
+                last_seen_cycle=cycle,
+                in_window=True,
+            )
+        else:
+            records[record.key] = replace(record, in_window=False)
+    for key, question in seen.items():
+        if key not in records:
+            records[key] = QuestionRecord(key, question, cycle, cycle, True)
+    ordered = sorted(records.values(), key=_order)
+    evicted = state.evicted
+    if len(ordered) > RETENTION_BOUND:
+        evicted += len(ordered) - RETENTION_BOUND
+        ordered = ordered[-RETENTION_BOUND:]  # drop the oldest created
+    return QuestionState(
+        records=tuple(ordered),
+        evicted=evicted,
+        window_full=bool(window_full),
+        last_read_cycle=cycle,
+        identity_unknown_rows=anonymous,
+    )
+
+
+def window_is_full(raw_count: int) -> bool:
+    """True when one read returned exactly 100 messages (the source gives no total)."""
+    return raw_count == WINDOW_ROWS
diff --git a/tests/observe/test_questions.py b/tests/observe/test_questions.py
new file mode 100644
index 000000000..ed736a91d
--- /dev/null
+++ b/tests/observe/test_questions.py
@@ -0,0 +1,160 @@
+"""Question retention tests (T11, T12, T46 in acceptance-tests.md; FR-17 in the PRD)."""
+
+from __future__ import annotations
+
+import dataclasses
+
+import pytest
+
+from superclaude.cli.observe.parse import UNKNOWN, Question
+from superclaude.cli.observe.questions import (
+    NO_LONGER_IN_WINDOW,
+    RETENTION_BOUND,
+    RETENTION_EXCEEDED,
+    QuestionState,
+    merge_questions,
+    window_is_full,
+)
+
+RUN = "run_14cfcbd8edf2"
+OTHER = "run_c1badaa6576b"
+
+
+def q(i, run=RUN, created=None, **kw):
+    epoch = 1_794_000_000.0 + i if created is None else created
+    return Question(
+        qid=f"msg_{i:06d}",
+        run_id=run,
+        namespace="orca-a",
+        subject=f"question {i}",
+        created_at="2026-11-11T20:01:11Z",
+        created_epoch=epoch,
+        **kw,
+    )
+
+
+def ids(state):
+    return [r.question.qid for r in state.records]
+
+
+def test_a_good_read_retains_rows_oldest_created_first_unknown_last():
+    rows = [q(3), q(1, created=UNKNOWN), q(2)]
+    state = merge_questions(None, rows, 1, False, True, RUN)
+    assert ids(state) == ["msg_000002", "msg_000003", "msg_000001"]
+    assert state.open_total == 3 and state.open_total_text == "3"
+    assert state.retained == 3 and state.evicted == 0
+    assert (state.last_read_cycle, state.never_read) == (1, False)
+    assert all(r.in_window and r.first_seen_cycle == 1 for r in state.records)
+
+
+def test_nothing_is_ever_closed_and_closure_evidence_is_unavailable():
+    state = merge_questions(None, [q(1)], 1, False, True, RUN)
+    assert state.closure_evidence == "unavailable (no source)"
+    assert not any("closed" in f.name for f in dataclasses.fields(state.records[0]))
+    assert not hasattr(state.records[0], "closed")
+
+
+def test_t11_a_failed_read_keeps_every_record_and_changes_nothing():
+    state = merge_questions(None, [q(1), q(2)], 1, True, True, RUN)
+    after = merge_questions(state, [], 2, False, False, RUN)
+    assert after is state
+    assert after.window_full is True and after.last_read_cycle == 1
+    assert ids(after) == ids(state)
+    assert all(r.in_window for r in after.records)
+
+
+def test_t12_a_question_missing_from_the_next_good_read_stays_marked():
+    first = merge_questions(None, [q(1), q(2)], 1, False, True, RUN)
+    second = merge_questions(first, [q(2), q(3)], 2, False, True, RUN)
+    by_id = {r.question.qid: r for r in second.records}
+    assert set(by_id) == {"msg_000001", "msg_000002", "msg_000003"}
+    assert by_id["msg_000001"].in_window is False
+    assert by_id["msg_000001"].status_text == NO_LONGER_IN_WINDOW
+    assert by_id["msg_000001"].last_seen_cycle == 1
+    assert by_id["msg_000002"].in_window and by_id["msg_000002"].first_seen_cycle == 1
+    assert by_id["msg_000002"].last_seen_cycle == 2
+    assert by_id["msg_000003"].first_seen_cycle == 2
+    assert (
+        second.open_total == 3
+    )  # a question leaving the window never lowers the total
+    third = merge_questions(second, [q(1)], 3, False, True, RUN)  # it comes back
+    assert {r.question.qid: r.in_window for r in third.records}["msg_000001"] is True
+
+
+def test_an_empty_good_read_keeps_everything_marked_and_never_closes():
+    first = merge_questions(None, [q(1), q(2)], 1, False, True, RUN)
+    second = merge_questions(first, [], 2, False, True, RUN)
+    assert second.open_total == 2
+    assert all(not r.in_window for r in second.records)
+
+
+def test_a_handled_question_that_orca_still_returns_is_listed_again_as_open():
+    # Known limit: ``check --all`` rows carry no read or acknowledged marker (REPORT 2.2,
+    # steps 8 and 9), so the observer cannot tell a handled question from a fresh one.
+    first = merge_questions(None, [q(1)], 1, False, True, RUN)
+    handled_and_still_returned = merge_questions(first, [q(1)], 2, False, True, RUN)
+    (record,) = handled_and_still_returned.records
+    assert record.in_window and handled_and_still_returned.open_total == 1
+    assert handled_and_still_returned.closure_evidence == "unavailable (no source)"
+
+
+def test_t46_1001_distinct_questions_never_lower_the_open_total():
+    state = None
+    totals = []
+    for start in range(0, 1001, 100):
+        batch = [q(i) for i in range(start, min(start + 100, 1001))]
+        state = merge_questions(state, batch, start // 100 + 1, True, True, RUN)
+        totals.append(state.open_total)
+    assert totals == sorted(totals) and totals[-1] == 1001
+    assert state.retained == RETENTION_BOUND == 1000
+    assert state.evicted == 1 and state.open_total == 1001
+    assert state.open_total_text == RETENTION_EXCEEDED == "unknown (retention exceeded)"
+    assert "msg_000000" not in ids(state)  # the oldest created is the one evicted
+    assert "msg_001000" in ids(state)
+    again = merge_questions(state, [], 99, False, False, RUN)
+    assert again.open_total == 1001 and again.retained == 1000
+
+
+def test_two_runs_with_the_same_message_id_stay_two_records():
+    rows = [q(1, run=RUN), q(1, run=OTHER)]
+    state = merge_questions(None, rows, 1, False, True, RUN)
+    assert state.retained == 2
+    assert {r.key for r in state.records} == {
+        (OTHER, "msg_000001"),
+        (RUN, "msg_000001"),
+    }
+
+
+def test_a_row_without_its_own_run_uses_the_run_that_was_read():
+    state = merge_questions(None, [q(1, run=UNKNOWN)], 1, False, True, RUN)
+    assert state.records[0].key == (RUN, "msg_000001")
+
+
+def test_rows_without_an_identity_are_counted_and_not_retained():
+    rows = [q(1), dataclasses.replace(q(2), qid=UNKNOWN, flags=("identity unknown",))]
+    state = merge_questions(None, rows, 1, False, True, RUN)
+    assert state.retained == 1 and state.identity_unknown_rows == 1
+
+
+@pytest.mark.parametrize(
+    "n,expected", [(99, False), (100, True), (101, False), (0, False)]
+)
+def test_window_full_means_exactly_100_rows(n, expected):
+    assert window_is_full(n) is expected
+
+
+def test_window_full_is_carried_by_the_state_and_cleared_by_a_smaller_read():
+    state = merge_questions(None, [q(1)], 1, True, True, RUN)
+    assert state.window_full is True
+    state = merge_questions(state, [q(1)], 2, False, True, RUN)
+    assert state.window_full is False
+
+
+def test_merge_is_pure_the_previous_state_is_not_modified():
+    first = merge_questions(None, [q(1)], 1, False, True, RUN)
+    snapshot = (first.records, first.evicted, first.window_full)
+    merge_questions(first, [q(2)], 2, True, True, RUN)
+    assert (first.records, first.evicted, first.window_full) == snapshot
+    assert isinstance(first, QuestionState)
+    with pytest.raises(dataclasses.FrozenInstanceError):
+        first.evicted = 5  # type: ignore[misc]


Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
