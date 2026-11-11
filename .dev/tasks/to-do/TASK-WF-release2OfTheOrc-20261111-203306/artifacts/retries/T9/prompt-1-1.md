331b769452785ffd6e6b37e980e2357ff4305906
Review one task for spec compliance.

Task brief: 
## Task 9: Wire the question read into the collector

Depends on: Task 6, Task 8

Edit `src/superclaude/cli/observe/collector.py` and add tests to `tests/observe/test_collector.py`.

- `CycleSource` gains `read_questions(clock, budget_deadline, run_id)`; `FixtureSource` returns a `FAILED` result with code `not-found`-style `no-question-fixture` unless a question fixture is supplied (fixture questions are synthetic and labelled so).
- `Collector.__init__` takes `questions: bool = False`. When true and a `run_id` is set, each cycle reads worker-list with a 4-call page cap (`LiveSource.read_pages` gets `max_calls`), then makes exactly one `read_questions` call inside the same cycle budget and merges the result with the store from Task 8. `CycleResult` gains optional fields with defaults (`questions`, `question_state`, `question_code`, `question_last_success_mono`), so existing callers and tests are unchanged.
- A failed question read never changes the worker-list state, the backoff or the retained records; a failed worker-list read never discards retained questions.

Acceptance criteria:
- `uv run pytest tests/observe/test_collector.py -v` passes, including: with questions on, one cycle logs worker-list calls plus exactly one message call and never more than 5 subprocesses (a fake worker-list that always says `hasMore` stops at 4 pages, plus 1 message call); with questions off the argv log is unchanged from release 1 (still 5 pages possible, T4 intact).
- A `consumer-fenced` question reply leaves the ledger `OK` and sets `question_state` to `FAILED` with the code; a later good read recovers.
- The message call is skipped, with `question_code` `overrun`, when the cycle budget is already spent.

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

Start sha: 331b769452785ffd6e6b37e980e2357ff4305906
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/adapter.py b/src/superclaude/cli/observe/adapter.py
index d8bcfcc6e..3d4c95074 100644
--- a/src/superclaude/cli/observe/adapter.py
+++ b/src/superclaude/cli/observe/adapter.py
@@ -77,6 +77,7 @@ CODES = frozenset(
         "empty-page",
         "consumer-fenced",
         "no-active-terminal",
+        "no-question-fixture",
     }
 )
 # Error codes of an ``{"ok": false, "error": {"code": ...}}`` envelope -> source codes.
@@ -410,7 +411,11 @@ class LiveSource:
         )
 
     def read_pages(
-        self, clock: Any, budget_deadline: float, run_id: str | None = None
+        self,
+        clock: Any,
+        budget_deadline: float,
+        run_id: str | None = None,
+        max_calls: int = MAX_CALLS_PER_CYCLE,
     ) -> SourceResult:
         if not self.discover():
             return SourceResult("FAILED", code="not-found")
@@ -466,7 +471,7 @@ class LiveSource:
                 return self._stop(pages, "empty-page", "", calls)
             if has_more is not True:
                 return SourceResult("OK", tuple(pages), calls=calls)
-            if calls >= MAX_CALLS_PER_CYCLE:
+            if calls >= max_calls:
                 return SourceResult("PARTIAL", tuple(pages), capped=True, calls=calls)
             if next_cursor is None or (
                 isinstance(next_cursor, str) and not next_cursor
diff --git a/src/superclaude/cli/observe/collector.py b/src/superclaude/cli/observe/collector.py
index 308dbeae9..4e1020866 100644
--- a/src/superclaude/cli/observe/collector.py
+++ b/src/superclaude/cli/observe/collector.py
@@ -21,12 +21,17 @@ from superclaude.cli.observe.parse import (
     load_fixture,
     merge,
     parse_page,
+    parse_questions,
 )
+from superclaude.cli.observe.questions import merge_questions, window_is_full
 
 INTERVAL = 15.0  # seconds between cycle starts
 CYCLE_BUDGET = 15.0  # a cycle never runs longer than this
 MAX_BACKOFF = 60.0  # after failures the wait doubles, never above this
 JOIN_TIMEOUT = 5.0  # how long stop() waits for the polling thread
+QUESTION_PAGE_CAP = (
+    4  # worker-list calls per cycle when questions are on (4 + 1 message call)
+)
 
 
 @dataclass(frozen=True)
@@ -47,6 +52,16 @@ class CycleResult:
     last_success_wall: float | None  # wall time of the same moment (display only)
     namespace: str
     duration: float = 0.0  # monotonic seconds this cycle took
+    # R2 question source (one named Run). Defaults describe "questions off".
+    question_state: str = "OFF"  # "OFF" | "NOT_POLLED" | "OK" | "FAILED"
+    question_code: str | None = None  # code of the last question read when FAILED
+    questions: Any = (
+        None  # QuestionState of the retained questions, None until a good read
+    )
+    question_read: Any = (
+        None  # ParsedQuestions of the last good read (counts, no bodies)
+    )
+    question_last_success_mono: float | None = None
 
 
 class CycleSource(Protocol):
@@ -65,17 +80,24 @@ class CycleSource(Protocol):
         self, clock: Any, budget_deadline: float, run_id: str | None = None
     ) -> SourceResult: ...
 
+    def read_questions(
+        self, clock: Any, budget_deadline: float, run_id: str
+    ) -> SourceResult: ...
+
 
 class FixtureSource:
     """Replays a fixture variant's cycles in order and repeats the last (never calls Orca)."""
 
     mode = "fixture"
 
-    def __init__(self, variant: str) -> None:
+    def __init__(self, variant: str, question_fixture: list | None = None) -> None:
         self.variant = variant
         self._fixture = load_fixture(variant)
         self._index = 0
         self.frozen_positions: frozenset = frozenset()  # of the cycle read last
+        # SYNTHETIC question cycles: each an envelope dict or ``{"fail": <code>}``.
+        self._question_fixture = question_fixture
+        self._question_index = 0
 
     @property
     def available(self) -> bool:
@@ -86,7 +108,11 @@ class FixtureSource:
         return f"fixture:{self.variant}"
 
     def read_pages(
-        self, clock: Any, budget_deadline: float, run_id: str | None = None
+        self,
+        clock: Any,
+        budget_deadline: float,
+        run_id: str | None = None,
+        max_calls: int = 5,
     ) -> SourceResult:
         entry = self._fixture.cycle(self._index)
         self._index += 1
@@ -95,6 +121,20 @@ class FixtureSource:
             return SourceResult("FAILED", code=entry.fail)
         return SourceResult("OK", pages=(entry.envelope,), calls=1)
 
+    def read_questions(
+        self, clock: Any, budget_deadline: float, run_id: str
+    ) -> SourceResult:
+        """Replay the supplied synthetic question cycles, else fail with a plain code."""
+        if not self._question_fixture:
+            return SourceResult("FAILED", code="no-question-fixture")
+        entry = self._question_fixture[
+            min(self._question_index, len(self._question_fixture) - 1)
+        ]
+        self._question_index += 1
+        if isinstance(entry, dict) and "fail" in entry and "result" not in entry:
+            return SourceResult("FAILED", code=str(entry["fail"]))
+        return SourceResult("OK", pages=(entry,), calls=1)
+
 
 class Collector:
     """Drives one source on a timer; ``latest()`` is the one published reference."""
@@ -107,6 +147,7 @@ class Collector:
         budget: float = CYCLE_BUDGET,
         max_backoff: float = MAX_BACKOFF,
         run_id: str | None = None,
+        questions: bool = False,
     ) -> None:
         self._source = source
         self._clock = clock
@@ -114,6 +155,7 @@ class Collector:
         self._budget = budget
         self._max_backoff = max_backoff
         self._run_id = run_id
+        self._questions = bool(questions and run_id)  # one named Run only
         self._wait = interval
         self._lock = threading.Lock()  # guards the published reference
         self._cycle_lock = threading.Lock()  # one cycle at a time
@@ -131,6 +173,7 @@ class Collector:
             last_success_mono=None,
             last_success_wall=None,
             namespace="",
+            question_state="NOT_POLLED" if self._questions else "OFF",
         )
 
     # -- publication -----------------------------------------------------------------------
@@ -148,6 +191,59 @@ class Collector:
         """Seconds to wait before the next cycle: the interval, doubled after failures."""
         return self._wait
 
+    # -- the question source (R2) ----------------------------------------------------------
+    @staticmethod
+    def _carry(previous: CycleResult) -> dict[str, Any]:
+        """The question fields of ``previous``: a failed or absent read changes none of them."""
+        return {
+            "question_state": previous.question_state,
+            "question_code": previous.question_code,
+            "questions": previous.questions,
+            "question_read": previous.question_read,
+            "question_last_success_mono": previous.question_last_success_mono,
+        }
+
+    def _question_fields(
+        self, previous: CycleResult, started: float, number: int, namespace: str
+    ) -> dict[str, Any]:
+        fields = self._carry(previous)
+        if not self._questions:
+            return fields
+        deadline = started + self._budget
+        if self._clock.monotonic() >= deadline:
+            return {**fields, "question_state": "FAILED", "question_code": "overrun"}
+        reply = self._source.read_questions(self._clock, deadline, self._run_id)
+        parsed = None
+        code = reply.code if reply.state != "OK" else None
+        if reply.state == "OK" and reply.pages:
+            try:
+                parsed = parse_questions(
+                    reply.pages[0], namespace, number, self._run_id
+                )
+            except ShapeError:
+                code = "shape"
+        if parsed is None:
+            return {
+                **fields,
+                "question_state": "FAILED",
+                "question_code": code or "json",
+            }
+        retained = merge_questions(
+            previous.questions,
+            parsed.rows,
+            number,
+            window_is_full(parsed.raw_count),
+            True,
+            self._run_id,
+        )
+        return {
+            "question_state": "OK",
+            "question_code": None,
+            "questions": retained,
+            "question_read": parsed,
+            "question_last_success_mono": self._clock.monotonic(),
+        }
+
     # -- one cycle -------------------------------------------------------------------------
     def run_once(self) -> CycleResult:
         """One synchronous cycle (used by ``--once``, by tests and by the polling thread)."""
@@ -169,12 +265,14 @@ class Collector:
                         last_success_mono=None,
                         last_success_wall=None,
                         namespace="",
+                        **self._carry(previous),
                     )
                 )
             number = previous.cycle + 1
             started = self._clock.monotonic()
+            extra = {"max_calls": QUESTION_PAGE_CAP} if self._questions else {}
             reply = self._source.read_pages(
-                self._clock, started + self._budget, self._run_id
+                self._clock, started + self._budget, self._run_id, **extra
             )
             namespace = self._source.namespace
             pages: list[ParsedPage] = []
@@ -189,6 +287,10 @@ class Collector:
                     break
                 pages.append(apply_frozen(parsed, frozen, base))
                 base += parsed.raw_count
+            # One message call in the same cycle budget; its failure touches nothing below.
+            question_fields = self._question_fields(
+                previous, started, number, namespace
+            )
             duration = self._clock.monotonic() - started
             common: dict[str, Any] = {
                 "cycle": number,
@@ -197,6 +299,7 @@ class Collector:
                 "diagnostic": reply.diagnostic,
                 "namespace": namespace,
                 "duration": duration,
+                **question_fields,
             }
             if not pages:
                 # First page failed: the previous snapshot, coverage and last success stay.
diff --git a/tests/observe/test_collector.py b/tests/observe/test_collector.py
index 5782a379e..b6dc28a0f 100644
--- a/tests/observe/test_collector.py
+++ b/tests/observe/test_collector.py
@@ -418,3 +418,261 @@ def test_the_collector_reads_time_only_from_the_injected_clock():
     )
     assert not re.search(r"\btime\.(monotonic|time|sleep|perf_counter)\(", text)
     assert "subprocess" not in text and "observe.view" not in text
+
+
+# -- R2: the question read inside the cycle (one named Run) ------------------------------------------------
+
+QRUN = "run_14cfcbd8edf2"
+
+
+def question_reply(ids=(1, 2), run=QRUN, n=None):
+    count = len(ids) if n is None else n
+    rows = [
+        {
+            "id": f"msg_{i:012x}",
+            "run_id": run,
+            "type": "question",
+            "subject": f"probe question {i}",
+            "created_at": f"2026-11-11T20:01:{10 + i % 40:02d}Z",
+        }
+        for i in (ids if n is None else range(n))
+    ]
+    envelope = {
+        "id": "e",
+        "ok": True,
+        "result": {
+            "acknowledged": None,
+            "count": count,
+            "messages": rows,
+            "runId": run,
+        },
+    }
+    return 0, json.dumps(envelope)
+
+
+def error_reply(code="consumer_fenced", status=1):
+    envelope = {"ok": False, "error": {"code": code, "message": "Nothing changed."}}
+    return status, json.dumps(envelope)
+
+
+def routed(worker, message):
+    """One runner response callable for both kinds of call.
+
+    ``worker`` and ``message`` are each a response (a pair or a callable) or a list of them:
+    the nth call of that kind gets the nth response, and the last one repeats.
+    """
+    queues = {
+        "worker": list(worker) if isinstance(worker, list) else [worker],
+        "message": list(message) if isinstance(message, list) else [message],
+    }
+    seen = {"worker": 0, "message": 0}
+
+    def respond(argv, timeout):
+        kind = "message" if "check" in argv else "worker"
+        queue = queues[kind]
+        pick = queue[min(seen[kind], len(queue) - 1)]
+        seen[kind] += 1
+        return pick(argv, timeout) if callable(pick) else pick
+
+    return respond
+
+
+def calls_of(argv_log):
+    worker = [a for a in argv_log if a[1:3] == ["orchestration", "worker-list"]]
+    message = [a for a in argv_log if a[1:3] == ["orchestration", "check"]]
+    return worker, message
+
+
+def questions_on(responses, clock, argv_log, **kw):
+    return live(responses, clock, argv_log, run_id=QRUN, questions=True, **kw)
+
+
+def test_questions_on_one_cycle_is_worker_list_pages_plus_exactly_one_message_call(
+    fake_clock, argv_log
+):
+    counter = {"n": 0}
+
+    def always_more(argv, timeout):
+        counter["n"] += 1
+        return reply(100, True, f"c{counter['n']}", 9999, tag=str(counter["n"]))
+
+    collector, runner, _ = questions_on(
+        [routed(always_more, question_reply((1, 2)))], fake_clock, argv_log
+    )
+    result = collector.run_once()
+    worker, message = calls_of(argv_log)
+    assert len(worker) == 4 and len(message) == 1
+    assert (
+        runner.calls == 5
+    )  # never more than 5 subprocesses (discovery is not one of them)
+    assert message[0] == [
+        ORCA, "orchestration", "check", "--all", "--types", "question",
+        "--run", QRUN, "--json",
+    ]  # fmt: skip
+    assert "--peek" not in message[0]
+    assert (result.state, result.coverage.stopped_by_cap) == ("PARTIAL", True)
+    assert result.question_state == "OK" and result.question_code is None
+    assert [r.question.qid for r in result.questions.records] == [
+        "msg_000000000001",
+        "msg_000000000002",
+    ]
+    assert result.question_last_success_mono == fake_clock.monotonic()
+
+
+def test_questions_off_leaves_release_1_behaviour_and_the_argv_log_unchanged(
+    fake_clock, argv_log
+):
+    counter = {"n": 0}
+
+    def always_more(argv, timeout):
+        counter["n"] += 1
+        return reply(100, True, f"c{counter['n']}", 9999, tag=str(counter["n"]))
+
+    collector, runner, _ = live([always_more], fake_clock, argv_log)
+    result = collector.run_once()
+    worker, message = calls_of(argv_log)
+    assert len(worker) == 5 and message == [] and runner.calls == 5  # T4 intact
+    assert result.question_state == "OFF" and result.questions is None
+    assert (result.question_code, result.question_read) == (None, None)
+    assert result.question_last_success_mono is None
+    # questions=True without a Run is the same as off: one named Run only.
+    collector, runner, _ = live([reply()], fake_clock, [], run_id=None, questions=True)
+    assert collector.run_once().question_state == "OFF"
+
+
+def test_a_consumer_fenced_reply_leaves_the_ledger_ok_and_a_good_read_recovers(
+    fake_clock, argv_log
+):
+    collector, _, _ = questions_on(
+        [
+            routed(
+                [reply(2), reply(2, tag="b"), reply(2, tag="c")],
+                [
+                    question_reply((1,)),
+                    error_reply("consumer_fenced", 1),
+                    question_reply((1, 2)),
+                ],
+            )
+        ],
+        fake_clock,
+        argv_log,
+    )
+    first = collector.run_once()
+    assert first.question_state == "OK"
+    fenced = collector.run_once()
+    assert fenced.state == "OK"  # the worker ledger is untouched
+    assert (fenced.question_state, fenced.question_code) == (
+        "FAILED",
+        "consumer-fenced",
+    )
+    assert fenced.questions is first.questions  # retained questions stay
+    assert fenced.question_last_success_mono == first.question_last_success_mono
+    assert collector.next_interval == 15.0  # no backoff from a question failure
+    healed = collector.run_once()
+    assert (healed.question_state, healed.question_code) == ("OK", None)
+    assert healed.questions.retained == 2
+
+
+def test_no_active_terminal_and_shape_and_json_failures_keep_retained_questions(
+    fake_clock, argv_log
+):
+    bad = {"id": "e", "ok": True, "result": {"runId": QRUN, "messages": None}}
+    collector, _, _ = questions_on(
+        [
+            routed(
+                [reply(1, tag=t) for t in "abcd"],
+                [
+                    question_reply((7,)),
+                    error_reply("no_active_terminal", 1),
+                    (0, json.dumps(bad)),
+                    (0, "not json"),
+                ],
+            )
+        ],
+        fake_clock,
+        argv_log,
+    )
+    good = collector.run_once()
+    for code in ("no-active-terminal", "shape", "json"):
+        result = collector.run_once()
+        assert result.state == "OK"
+        assert (result.question_state, result.question_code) == ("FAILED", code)
+        assert result.questions is good.questions
+
+
+def test_a_failed_worker_list_read_never_discards_retained_questions(
+    fake_clock, argv_log
+):
+    collector, _, _ = questions_on(
+        [
+            routed(
+                [reply(2), (2, ""), (2, "")],
+                [
+                    question_reply((1,)),
+                    question_reply((1, 2)),
+                    error_reply("consumer_fenced", 1),
+                ],
+            )
+        ],
+        fake_clock,
+        argv_log,
+    )
+    collector.run_once()
+    worker_down = collector.run_once()
+    assert worker_down.state == "FAILED" and worker_down.code == "exit:2"
+    assert worker_down.question_state == "OK" and worker_down.questions.retained == 2
+    both_down = collector.run_once()
+    assert both_down.state == "FAILED" and both_down.question_state == "FAILED"
+    assert both_down.questions is worker_down.questions
+    assert both_down.snapshot is not None  # the last good rows stay too
+
+
+def test_the_message_call_is_skipped_with_overrun_when_the_budget_is_spent(
+    fake_clock, argv_log
+):
+    def slow_worker(argv, timeout):
+        fake_clock.advance(20.0)  # the worker-list read uses up the 15 s cycle budget
+        return reply(1)
+
+    collector, runner, _ = questions_on(
+        [routed(slow_worker, question_reply((1,)))], fake_clock, argv_log
+    )
+    result = collector.run_once()
+    worker, message = calls_of(argv_log)
+    assert len(worker) == 1 and message == []
+    assert (result.question_state, result.question_code) == ("FAILED", "overrun")
+    assert result.questions is None
+
+
+def test_exactly_100_rows_sets_window_full_in_the_retained_state(fake_clock, argv_log):
+    collector, _, _ = questions_on(
+        [
+            routed(
+                [reply(1), reply(1, tag="b")],
+                [question_reply(n=100), question_reply((1,))],
+            )
+        ],
+        fake_clock,
+        argv_log,
+    )
+    assert collector.run_once().questions.window_full is True
+    assert collector.run_once().questions.window_full is False
+
+
+def test_a_fixture_source_has_no_question_fixture_unless_one_is_supplied(fake_clock):
+    plain = Collector(FixtureSource("base"), fake_clock, run_id=QRUN, questions=True)
+    result = plain.run_once()
+    assert result.state == "OK" and result.question_state == "FAILED"
+    assert result.question_code == "no-question-fixture"
+    synthetic = [json.loads(question_reply((1, 2))[1]), {"fail": "timeout"}]
+    supplied = Collector(
+        FixtureSource("base", question_fixture=synthetic),
+        fake_clock,
+        run_id=QRUN,
+        questions=True,
+    )
+    first = supplied.run_once()
+    assert first.question_state == "OK" and first.questions.retained == 2
+    second = supplied.run_once()
+    assert (second.question_state, second.question_code) == ("FAILED", "timeout")
+    assert second.questions is first.questions


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
