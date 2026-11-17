578416f74dd1a207745a4e5a09b5cb040cce71a0
Review one task for spec compliance.

Task brief: 
## Task 10: Add the coordinator questions panel to view.py and render.py

Depends on: Task 8, Task 9

Edit `src/superclaude/cli/observe/view.py`, `src/superclaude/cli/observe/render.py` and add tests to `tests/observe/test_view.py` and `tests/observe/test_render.py` (rendering rules as rewritten by Task 5).

- With questions on, `build_view` adds a question section: title `COORDINATOR QUESTIONS`, line `one Run only: <runId>`, the disclosure `bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between reads may be lost`, the counts line `observed open: n | closed by evidence: unavailable (no source)`, one line per question oldest first (age, sanitized subject, `reason unknown`), windowed with `x/y shown` when the height cannot hold them, and `window full: older questions may be missing` when exactly 100 rows came back.
- States in plain words: never read yet (`question read pending`), `FAILED (consumer-fenced)` and `FAILED (no-active-terminal)` with the sentence `this terminal does not hold the named Run; the observer never binds to a Run`, STALE after 45 s without a good question read (monotonic clock), and an empty good read reads `no observed questions in this source window; not proof none exist`, never `no questions`.
- The header cell `MESSAGES_CELL` reads `coordinator questions: one Run, last read <age> ago` when on; with questions off it keeps `messages UNVERIFIED (not read)`. `GAP_NOTICE` is replaced by the panel only when questions are on and the source has read once; otherwise it stays (T9, T47). The ledger title stays `worker-reported, not questions`.
- Header and panel stay at or under the terminal width at 160, 116 and 80 columns; the too-small diagnostic (T49) still carries a question-source line.
- The `m` key keeps marking worker rows only; it never changes the question count.

Acceptance criteria:
- `uv run pytest tests/observe/test_view.py tests/observe/test_render.py -v` passes with new tests: T19 title text present; T47 with questions off is byte-identical to release 1 output; T10 `m` on every worker row leaves `observed open` unchanged; T12 and T11 render the retained and `no longer in source window` lines; an empty good read never contains the words `no questions`; every screen line has `cell_len <= W` at 160, 116 and 80; a subject with `[bold]` renders literally; the fenced state names the sentence above.
- With retention exceeded the count reads `unknown (retention exceeded)` and shows the retained count.

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

Start sha: 578416f74dd1a207745a4e5a09b5cb040cce71a0
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/collector.py b/src/superclaude/cli/observe/collector.py
index 4e1020866..abf93b5e9 100644
--- a/src/superclaude/cli/observe/collector.py
+++ b/src/superclaude/cli/observe/collector.py
@@ -62,6 +62,10 @@ class CycleResult:
         None  # ParsedQuestions of the last good read (counts, no bodies)
     )
     question_last_success_mono: float | None = None
+    question_run: str | None = None  # the one named Run, only when questions are on
+    question_retention_wall: float | None = (
+        None  # wall time retention started (display only)
+    )
 
 
 class CycleSource(Protocol):
@@ -174,6 +178,8 @@ class Collector:
             last_success_wall=None,
             namespace="",
             question_state="NOT_POLLED" if self._questions else "OFF",
+            question_run=run_id if self._questions else None,
+            question_retention_wall=clock.wall() if self._questions else None,
         )
 
     # -- publication -----------------------------------------------------------------------
@@ -201,6 +207,8 @@ class Collector:
             "questions": previous.questions,
             "question_read": previous.question_read,
             "question_last_success_mono": previous.question_last_success_mono,
+            "question_run": previous.question_run,
+            "question_retention_wall": previous.question_retention_wall,
         }
 
     def _question_fields(
@@ -237,6 +245,7 @@ class Collector:
             self._run_id,
         )
         return {
+            **fields,
             "question_state": "OK",
             "question_code": None,
             "questions": retained,
diff --git a/src/superclaude/cli/observe/render.py b/src/superclaude/cli/observe/render.py
index 78b37cd57..fed76f2dc 100644
--- a/src/superclaude/cli/observe/render.py
+++ b/src/superclaude/cli/observe/render.py
@@ -7,6 +7,8 @@ from data (never markup strings). It never imports the adapter or the collector.
 
 from __future__ import annotations
 
+from dataclasses import replace
+
 from rich.cells import cell_len
 from rich.console import Group
 from rich.text import Text
@@ -26,6 +28,7 @@ from superclaude.cli.observe.view import (
     INSPECTOR_TITLE,
     NO_MATCH_TEXT,
     CountsToken,
+    QuestionsPanel,
     RowView,
     View,
     text_of,
@@ -291,6 +294,27 @@ def _notes(view: View) -> list[str]:
     return ["  ".join(parts)] if parts else []
 
 
+def _panel_lines(
+    panel: QuestionsPanel, policy: TerminalPolicy, capacity: int | None
+) -> list[str]:
+    """The coordinator-questions block: header lines, up to ``capacity`` questions, notes."""
+    width = policy.width
+    lines = wrap(panel.title, width, policy)
+    lines += wrap(panel.run_line, width, policy)
+    lines += wrap(panel.disclosure, width, policy)
+    for state_line in panel.state_lines:
+        lines += wrap(state_line, width, policy)
+    lines += wrap(panel.counts_line, width, policy)
+    shown, cut = panel.window(capacity)
+    lines += [clip(q.text, width, policy) for q in shown]
+    if cut:
+        lines += wrap(cut, width, policy)
+    for text in (panel.empty_text, panel.window_full_text, *panel.notes):
+        if text:
+            lines += wrap(text, width, policy)
+    return lines + wrap(panel.retention_line, width, policy)
+
+
 def screen_lines(
     view: View, policy: TerminalPolicy, message: str | None = None
 ) -> list[str]:
@@ -310,19 +334,19 @@ def screen_lines(
         lines += wrap(view.collected_text, width, policy)
         return lines + wrap(view.gap_notice, width, policy)
 
-    top: list[str] = []
-    top += wrap(view.header1, width, policy)
-    top += wrap(view.header2, width, policy)
-    top += counts_lines(view.counts_tokens, policy)
+    head: list[str] = []
+    head += wrap(view.header1, width, policy)
+    head += wrap(view.header2, width, policy)
+    head += counts_lines(view.counts_tokens, policy)
     if view.changes_line:
-        top += wrap(view.changes_line, width, policy)
-    top += wrap(view.gap_notice, width, policy)
+        head += wrap(view.changes_line, width, policy)
+    tail: list[str] = []
     for note in _notes(view):
-        top += wrap(note, width, policy)
+        tail += wrap(note, width, policy)
     if view.focus == "filter":
-        top += wrap("/" + view.filter_text, width, policy)
+        tail += wrap("/" + view.filter_text, width, policy)
     if message:
-        top += wrap(message, width, policy)
+        tail += wrap(message, width, policy)
 
     # The footer is one line when it fits, else the key list and the counts on two lines.
     window_probe = view.window(None)
@@ -333,6 +357,32 @@ def screen_lines(
         else 1 + len(wrap(view.footer_counts(window_probe), width, policy))
     )
 
+    # The R2 panel stands in for the gap notice once the question source has read; in the
+    # inspector only its one-line summary (``gap_notice``) is shown, so the inspector keeps room.
+    panel = view.questions
+    inspecting = view.focus == "inspector" and view.inspector is not None
+    if panel is not None and panel.replaces_gap and not inspecting:
+        ledger_fixed = len(wrap(view.ledger_title, width, policy)) + (
+            2 if policy.width_class == "full" and view.visible_rows else 0
+        )
+        base = len(
+            _panel_lines(replace(panel, lines=(), empty_text=None), policy, None)
+        )
+        spare = policy.height - (
+            len(head) + len(tail) + base + footer_height + ledger_fixed + 1 + 3
+        )  # 1 overflow line and at least 3 ledger rows stay
+        if spare >= 1:
+            gap_part = _panel_lines(panel, policy, spare)
+        else:  # no room for the panel: its one-line summary stands in for it
+            gap_part = wrap(view.gap_notice, width, policy)
+    else:
+        gap_part = wrap(view.gap_notice, width, policy)
+        if (
+            panel is not None and not panel.replaces_gap
+        ):  # questions on, nothing read yet
+            gap_part += wrap(panel.summary, width, policy)
+    top = head + gap_part + tail
+
     if view.focus == "inspector" and view.inspector is not None:
         footer_lines = [clip(INSPECTOR_HELP, width, policy)]
         body = _inspector_lines(
diff --git a/src/superclaude/cli/observe/view.py b/src/superclaude/cli/observe/view.py
index af4f07ca6..1782bfa5e 100644
--- a/src/superclaude/cli/observe/view.py
+++ b/src/superclaude/cli/observe/view.py
@@ -49,6 +49,24 @@ NO_READ_YET = "no successful worker-list read yet"
 EMPTY_NOTICE = "no observed items in this source window; not proof none exist"
 NOT_AVAILABLE_TEXT = "NOT AVAILABLE (no Orca CLI validated)"
 MESSAGES_CELL = "messages UNVERIFIED (not read)"
+# R2 coordinator-questions panel (one named Run); every literal is defined here once.
+QUESTIONS_TITLE = "COORDINATOR QUESTIONS"
+QUESTIONS_DISCLOSURE = (
+    "bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; "
+    "bursts over 100 rows between reads may be lost"
+)
+QUESTIONS_WINDOW_FULL = "window full: older questions may be missing"
+QUESTIONS_PENDING = "question read pending"
+QUESTIONS_NOT_HELD = (
+    "this terminal does not hold the named Run; the observer never binds to a Run"
+)
+QUESTIONS_EMPTY = "no observed questions in this source window; not proof none exist"
+QUESTIONS_REASON = "reason unknown"  # no verified reason field exists (PROPOSED)
+QUESTIONS_CLOSED = "closed by evidence: unavailable (no source)"
+QUESTIONS_RETENTION = (
+    "retention reset at {hhmm}; questions observed before this start are not retained"
+)
+QUESTIONS_FENCE_CODES = ("consumer-fenced", "no-active-terminal")
 UNAVAILABLE = "unavailable (no source)"
 ABSENT_IN_SOURCE = "unknown (absent in source)"
 PARTIAL_CAP_TEXT = (
@@ -151,6 +169,52 @@ class SnapshotMeta:
     collection_duplicates_ignored: int | None
 
 
+@dataclass(frozen=True)
+class QuestionLine:
+    """One retained coordinator question, display-ready. No body, handle or payload."""
+
+    qid: str  # the full message id
+    text: str  # "age  subject  reason unknown[  no longer in source window]"
+    created_at: Any  # source text or UNKNOWN (exports)
+    age_seconds: Any  # number or UNKNOWN (exports)
+    in_window: bool
+
+
+@dataclass(frozen=True)
+class QuestionsPanel:
+    """The R2 panel for one named Run (adapter-contract.md "R2 onward", rendering-rules.md)."""
+
+    run_id: str
+    state: str  # "PENDING" | "OK" | "STALE" | "FAILED"
+    code: str | None
+    title: str
+    run_line: str
+    disclosure: str
+    state_lines: tuple[str, ...]
+    counts_line: str
+    lines: tuple[QuestionLine, ...]  # oldest created first
+    empty_text: str | None
+    window_full_text: str | None
+    notes: tuple[str, ...]
+    retention_line: str
+    summary: str  # one line; stands in for the gap notice once the source has read
+    replaces_gap: bool
+    open_total: Any  # int, or UNKNOWN when retention was exceeded or nothing was read
+    retained: int
+    evicted: int
+    window_full: bool
+
+    def window(
+        self, capacity: int | None
+    ) -> tuple[tuple[QuestionLine, ...], str | None]:
+        """The question lines that fit ``capacity`` and the ``x/y shown`` text when cut."""
+        total = len(self.lines)
+        if capacity is None or capacity >= total:
+            return self.lines, None
+        keep = max(capacity, 1)
+        return self.lines[:keep], f"{keep}/{total} shown"
+
+
 @dataclass(frozen=True)
 class Window:
     rows: tuple[RowView, ...]
@@ -195,6 +259,7 @@ class View:
     inspector: tuple[tuple[str, str], ...] | None
     help_line: str
     inspector_scroll: int = 0
+    questions: QuestionsPanel | None = None  # None unless R2 questions are on
 
     def window(self, capacity: int | None) -> Window:
         """The rows that fit ``capacity`` lines, always including the selected visible row."""
@@ -498,6 +563,119 @@ def _source_counts_text(snapshot: Any) -> str:
     return "source counts: " + " / ".join(parts)
 
 
+def _questions_panel(result: Any, clock: Any) -> QuestionsPanel | None:
+    """The coordinator-questions panel, or None when the question source is off."""
+    qstate = getattr(result, "question_state", "OFF")
+    if qstate == "OFF":
+        return None
+    run = result.question_run if result.question_run else "unknown"
+    retained = result.questions
+    last = result.question_last_success_mono
+    age = None if last is None else format_age(clock.monotonic() - last)
+    code = result.question_code if qstate == "FAILED" else None
+    if qstate == "NOT_POLLED":
+        state = "PENDING"
+    elif qstate == "FAILED":
+        state = "FAILED"
+    elif last is None or clock.monotonic() - last >= STALE_SECONDS:
+        state = "STALE"
+    else:
+        state = "OK"
+
+    state_lines: list[str] = []
+    if state == "PENDING":
+        state_lines.append(QUESTIONS_PENDING)
+        status = QUESTIONS_PENDING
+    elif state == "FAILED":
+        text = f"FAILED ({code_label(code)})" + (f" {age}" if age else "")
+        state_lines.append(text)
+        if code in QUESTIONS_FENCE_CODES:
+            state_lines.append(QUESTIONS_NOT_HELD)
+        status = f"FAILED ({code_label(code)})"
+    elif state == "STALE":
+        state_lines.append(f"STALE {age or 'never'}")
+        status = f"STALE {age or 'never'}"
+    else:
+        status = "read OK"
+
+    if retained is None:
+        open_total: Any = UNKNOWN
+        open_text = "unknown (no question read yet)"
+        lines: tuple[QuestionLine, ...] = ()
+        count_retained = evicted = 0
+        window_full = False
+    else:
+        open_total = UNKNOWN if retained.evicted else retained.open_total
+        open_text = retained.open_total_text
+        if retained.evicted:
+            open_text += f" (retained {retained.retained})"
+        count_retained, evicted = retained.retained, retained.evicted
+        window_full = retained.window_full
+        built = []
+        for record in retained.records:
+            q = record.question
+            epoch = q.created_epoch
+            seconds = UNKNOWN if epoch is UNKNOWN else max(0.0, clock.wall() - epoch)
+            shown_age = "unknown" if seconds is UNKNOWN else format_age(seconds)
+            parts = [shown_age, text_of(q.subject), QUESTIONS_REASON]
+            if not record.in_window:
+                parts.append(record.status_text)
+            built.append(
+                QuestionLine(
+                    qid=text_of(q.qid),
+                    text="  ".join(parts),
+                    created_at=q.created_at,
+                    age_seconds=seconds,
+                    in_window=record.in_window,
+                )
+            )
+        lines = tuple(built)
+    counts_line = f"observed open: {open_text} | {QUESTIONS_CLOSED}"
+
+    notes: list[str] = []
+    read = result.question_read
+    if read is not None:
+        for count, label in (
+            (read.contradictory_rows, "contradictory rows ignored"),
+            (read.malformed_rows, "malformed rows skipped"),
+            (read.duplicates, "duplicate rows ignored"),
+            (read.identity_unknown_rows, "rows with identity unknown not retained"),
+        ):
+            if count:
+                notes.append(f"{count} {label}")
+    empty_text = (
+        QUESTIONS_EMPTY
+        if state in ("OK", "STALE") and retained is not None and not lines
+        else None
+    )
+    since = result.question_retention_wall
+    hhmm = format_local(
+        clock.wall() if since is None else since, clock.local_tz(), "%H:%M"
+    )
+    summary = f"coordinator questions: observed open {open_text}; {status}; one Run only: {run}"
+    return QuestionsPanel(
+        run_id=run,
+        state=state,
+        code=code,
+        title=QUESTIONS_TITLE,
+        run_line=f"one Run only: {run}",
+        disclosure=QUESTIONS_DISCLOSURE,
+        state_lines=tuple(state_lines),
+        counts_line=counts_line,
+        lines=lines,
+        empty_text=empty_text,
+        window_full_text=QUESTIONS_WINDOW_FULL if window_full else None,
+        notes=tuple(notes),
+        retention_line=QUESTIONS_RETENTION.format(hhmm=hhmm),
+        summary=summary,
+        replaces_gap=qstate in ("OK", "FAILED"),
+        open_total=open_total,
+        retained=count_retained,
+        evicted=evicted,
+        window_full=window_full,
+    )
+
+
 def _changes(rows: tuple[Row, ...], session: Session) -> tuple[frozenset, int]:
     """(identities of rows to star, k for ``changed since``): added, removed or changed rows."""
     baseline = session.baseline
@@ -545,7 +723,17 @@ def build_view(result: Any, session: Session, clock: Any) -> View:
     header1 = "  ".join(header_parts)
 
     fresh_cell, age = _freshness(result, clock, state)
-    cells = [fresh_cell, MESSAGES_CELL]
+    panel = _questions_panel(result, clock)
+    if panel is None:
+        messages_cell = MESSAGES_CELL
+    else:
+        last = result.question_last_success_mono
+        messages_cell = (
+            "coordinator questions: one Run, not read yet"
+            if last is None
+            else f"coordinator questions: one Run, last read {format_age(clock.monotonic() - last)} ago"
+        )
+    cells = [fresh_cell, messages_cell]
     if snapshot is not None and snapshot.warnings:
         cells.append(f"source warnings: {len(snapshot.warnings)} (inspector)")
     if result.code == "overrun":
@@ -643,7 +831,9 @@ def build_view(result: Any, session: Session, clock: Any) -> View:
         poll_age=age,
         counts_tokens=tuple(tokens),
         collected_text=collected_text,
-        gap_notice=GAP_NOTICE,
+        gap_notice=panel.summary
+        if panel is not None and panel.replaces_gap
+        else GAP_NOTICE,
         ledger_title=LEDGER_TITLE,
         ledger_empty=ledger_empty,
         changes_line=changes_line,
@@ -664,6 +854,7 @@ def build_view(result: Any, session: Session, clock: Any) -> View:
         else None,
         help_line=KEYS_LINE,
         inspector_scroll=session.inspector_scroll,
+        questions=panel,
     )
 
 
diff --git a/tests/observe/conftest.py b/tests/observe/conftest.py
index b18950f2b..ecf39a14b 100644
--- a/tests/observe/conftest.py
+++ b/tests/observe/conftest.py
@@ -218,3 +218,89 @@ def console_factory():
         return make_console(policy, file=io.StringIO(), record=True), policy
 
     return factory
+
+
+# -- R2 question rows (probe shapes, SYNTHETIC values) ------------------------------------------
+
+QRUN = "run_14cfcbd8edf2"
+
+
+def make_question_rows(
+    n: int,
+    run: str = QRUN,
+    start: int = 0,
+    newest_first: bool = True,
+    subject=None,
+) -> list[dict]:
+    """``n`` synthetic ``question`` message rows with the recorded key names, no real values.
+
+    Row ``i`` is created ``i`` seconds after a fixed base, so a higher id is a newer question;
+    ``newest_first`` returns them in the order ``check --all`` gives them (REPORT, evidence 14).
+    """
+    rows = []
+    for i in range(start, start + n):
+        created = BASE_TIME - timedelta(seconds=3600) + timedelta(seconds=i)
+        rows.append(
+            {
+                "id": f"msg_{i:012x}",
+                "run_id": run,
+                "delivery_contract": "current_delivery",
+                "from_handle": "term_synthetic",
+                "to_handle": f"run:{run}",
+                "subject": f"synthetic question {i}" if subject is None else subject,
+                "body": "synthetic body",
+                "type": "question",
+                "priority": "normal",
+                "thread_id": None,
+                "payload": None,
+                "created_at": created.strftime("%Y-%m-%dT%H:%M:%SZ"),
+                "delivered_at": None,
+            }
+        )
+    return list(reversed(rows)) if newest_first else rows
+
+
+def make_question_envelope(rows: list[dict], run: str = QRUN) -> dict:
+    """The recorded envelope shape of one ``check --all`` read."""
+    return {
+        "id": "00000000-0000-0000-0000-000000000000",
+        "ok": True,
+        "result": {
+            "acknowledged": None,
+            "count": len(rows),
+            "messages": rows,
+            "runId": run,
+        },
+        "_meta": {"runtimeId": "00000000-0000-0000-0000-000000000001"},
+    }
+
+
+def make_question_error(code: str) -> dict:
+    """An ``{"ok": false, "error": {...}}`` envelope as recorded for the two known codes."""
+    return {
+        "id": "00000000-0000-0000-0000-000000000002",
+        "ok": False,
+        "error": {"code": code, "message": code},
+    }
+
+
+def routed_runner_responses(worker, message):
+    """One runner response callable for worker-list and message calls.
+
+    ``worker`` and ``message`` are each a response (a pair or a callable) or a list of them:
+    the nth call of that kind gets the nth response and the last one repeats.
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
diff --git a/tests/observe/release1_surface.py b/tests/observe/release1_surface.py
new file mode 100644
index 000000000..d2d089355
--- /dev/null
+++ b/tests/observe/release1_surface.py
@@ -0,0 +1,62 @@
+"""The questions-off surface of the observer, as a plain dict (T47 byte-identity with release 1).
+
+``golden_release1_surface.json`` was generated by running ``surface()`` against the release 1
+source, ``git archive 9e2608b03 src/superclaude`` (the commit before release 2), with
+``PYTHONPATH=<that tree>:.`` and ``uv run python``. A test runs ``surface()`` against the
+current source and compares it with that file, so "questions off is byte-identical to
+release 1" is checked against release 1's own bytes, not against the current code.
+
+This module uses only names that exist in release 1.
+"""
+
+from __future__ import annotations
+
+import io
+
+from rich.console import Console
+
+from superclaude.cli.observe.collector import Collector, FixtureSource
+from superclaude.cli.observe.export import record_text, snapshot_json
+from superclaude.cli.observe.render import render, screen_lines
+from superclaude.cli.observe.terminal import make_console, resolve_policy
+from superclaude.cli.observe.view import Session, build_view
+from tests.observe.conftest import FakeClock
+
+VARIANTS = ("base", "empty", "source-loss", "injection", "missing-fields")
+WIDTHS = (160, 116, 80)
+HEIGHTS = (40, 12)
+
+
+def _policy(width: int, height: int):
+    return resolve_policy({}, "utf-8", {"ascii": False}, width, height)
+
+
+def _printed(view, policy) -> str:
+    buffer = io.StringIO()
+    console: Console = make_console(policy, file=buffer, record=True)
+    console.print(render(view, policy))
+    return buffer.getvalue()
+
+
+def surface() -> dict:
+    out: dict = {}
+    for variant in VARIANTS:
+        clock = FakeClock()
+        collector = Collector(FixtureSource(variant), clock)
+        result = collector.run_once()
+        result = collector.run_once()
+        view = build_view(result, Session(), clock)
+        entry: dict = {
+            "header1": view.header1,
+            "header2": view.header2,
+            "gap_notice": view.gap_notice,
+            "record_text": record_text(view),
+            "snapshot_json": snapshot_json(view),
+        }
+        for width in WIDTHS:
+            for height in HEIGHTS:
+                policy = _policy(width, height)
+                entry[f"lines_{width}x{height}"] = screen_lines(view, policy)
+            entry[f"printed_{width}"] = _printed(view, _policy(width, 40))
+        out[variant] = entry
+    return out
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index bcf2a3ca9..50116a8bc 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -407,3 +407,221 @@ def test_render_returns_renderables_and_never_sorts_or_decides_literals(fake_clo
         r"observe\.(adapter|collector|parse)\b|sorted\(|\.sort\(|from_markup|Console\(",
         text,
     )
+
+
+# -- R2: the coordinator questions panel on screen (T19, T47, T49, T12, T11, T23) ------------------------------------------
+
+from superclaude.cli.observe.view import (  # noqa: E402
+    QUESTIONS_NOT_HELD,
+    Key,
+    apply_key,
+)
+from tests.observe.conftest import (  # noqa: E402
+    QRUN,
+    make_question_envelope,
+    make_question_error,
+    make_question_rows,
+    routed_runner_responses,
+)
+
+
+def question_result(message, clock, n_workers=4):
+    worker = (0, json.dumps(make_envelope(make_rows(n_workers, 1), total=n_workers)))
+    runner = FakeRunner([], [routed_runner_responses(worker, message)])
+    collector = Collector(
+        LiveSource(runner, FakeDiscover([])), clock, run_id=QRUN, questions=True
+    )
+    return collector, collector.run_once()
+
+
+def ok_message(rows):
+    return 0, json.dumps(make_question_envelope(rows))
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_t19_the_screen_carries_the_title_disclosure_and_one_line_per_question(
+    fake_clock, width
+):
+    _, result = question_result(ok_message(make_question_rows(5)), fake_clock)
+    lines = screen_lines(build_view(result, Session(), fake_clock), policy_for(width))
+    flat = " ".join(" ".join(lines).split())
+    assert "COORDINATOR QUESTIONS" in flat
+    assert f"one Run only: {QRUN}" in flat
+    assert "at most 100 rows per read, not 100 questions" in flat
+    assert "bounded best effort; coverage unknown" in flat
+    assert "bursts over 100 rows between reads may be lost" in flat
+    assert "observed open: 5 | closed by evidence: unavailable (no source)" in flat
+    assert (
+        "retention reset at 12:00; questions observed before this start are not retained"
+        in flat
+    )
+    assert sum("reason unknown" in l for l in lines) == 5
+    assert "synthetic body" not in flat and GAP_NOTICE not in lines
+    assert all(cell_len(l) <= width for l in lines)
+
+
+@pytest.mark.parametrize("height", [40, 24, 14])
+@pytest.mark.parametrize("width", WIDTHS)
+def test_every_screen_line_fits_at_160_116_and_80_with_the_panel(
+    fake_clock, width, height
+):
+    rows = make_question_rows(
+        30, subject="界" * 60 + " [bold]x[/bold] very long subject " * 4
+    )
+    _, result = question_result(ok_message(rows), fake_clock)
+    policy = policy_for(width, height=height)
+    lines = screen_lines(build_view(result, Session(), fake_clock), policy)
+    assert all(cell_len(l) <= width for l in lines)
+    assert len(lines) <= height or policy.too_small
+    if height >= 24:
+        assert any("[bold]x[/bold]" in l or "界" in l for l in lines)
+
+
+def test_a_long_question_list_is_windowed_with_x_of_y_shown(fake_clock):
+    _, result = question_result(ok_message(make_question_rows(60)), fake_clock)
+    policy = policy_for(120, height=30)
+    lines = screen_lines(build_view(result, Session(), fake_clock), policy)
+    shown = [l for l in lines if l.endswith("/60 shown")]
+    assert len(shown) == 1 and len(lines) <= 30
+    assert sum("reason unknown" in l for l in lines) < 60
+    assert any(
+        l.startswith("collected") or "collected 4" in l for l in lines
+    )  # counts stay
+
+
+def test_t47_questions_off_the_screen_is_the_release_1_screen(fake_clock):
+    off = fixture_view("base", fake_clock)
+    lines = screen_lines(off, policy_for(160))
+    assert GAP_NOTICE in lines and not any("COORDINATOR" in l for l in lines)
+    assert any("messages UNVERIFIED (not read)" in l for l in lines)
+
+
+def test_the_pending_screen_keeps_the_gap_notice_and_adds_one_pending_line(fake_clock):
+    collector, _ = question_result(ok_message([]), fake_clock)
+    pending = collector.latest()  # a fresh collector's NOT_POLLED result
+    fresh = Collector(
+        LiveSource(FakeRunner([], [(0, "{}")]), FakeDiscover([])),
+        fake_clock,
+        run_id=QRUN,
+        questions=True,
+    ).latest()
+    lines = screen_lines(build_view(fresh, Session(), fake_clock), policy_for(160))
+    assert GAP_NOTICE in lines
+    assert any("question read pending" in l for l in lines)
+    assert pending.question_state == "OK"
+
+
+def test_the_fenced_state_names_the_sentence_and_keeps_the_retained_lines(fake_clock):
+    fenced = (1, json.dumps(make_question_error("consumer_fenced")))
+    collector, first = question_result(
+        [ok_message(make_question_rows(2)), fenced], fake_clock
+    )
+    second = collector.run_once()
+    lines = screen_lines(build_view(second, Session(), fake_clock), policy_for(160))
+    flat = " ".join(lines)
+    assert "FAILED (consumer fenced)" in flat and QUESTIONS_NOT_HELD in flat
+    assert sum("reason unknown" in l for l in lines) == 2
+    assert "observed open: 2 |" in flat and first.question_state == "OK"
+
+
+def test_t12_a_question_that_left_the_window_stays_listed_on_screen(fake_clock):
+    collector, _ = question_result(
+        [ok_message(make_question_rows(2)), ok_message(make_question_rows(2, start=1))],
+        fake_clock,
+    )
+    lines = screen_lines(
+        build_view(collector.run_once(), Session(), fake_clock), policy_for(160)
+    )
+    assert sum("no longer in source window" in l for l in lines) == 1
+    assert sum("reason unknown" in l for l in lines) == 3
+
+
+def test_an_empty_good_read_screen_says_not_proof_and_never_no_questions(fake_clock):
+    _, result = question_result(ok_message([]), fake_clock)
+    lines = screen_lines(build_view(result, Session(), fake_clock), policy_for(160))
+    flat = " ".join(lines)
+    assert "no observed questions in this source window; not proof none exist" in flat
+    assert "no questions" not in flat.lower()
+
+
+def test_window_full_text_is_on_screen_at_exactly_100_rows(fake_clock):
+    _, result = question_result(ok_message(make_question_rows(100)), fake_clock)
+    lines = screen_lines(
+        build_view(result, Session(), fake_clock), policy_for(160, height=60)
+    )
+    assert "window full: older questions may be missing" in lines
+
+
+@pytest.mark.parametrize("height", [1, 3, MIN_ROWS - 1])
+def test_t49_the_too_small_diagnostic_carries_a_question_source_line(
+    fake_clock, height
+):
+    _, result = question_result(ok_message(make_question_rows(2)), fake_clock)
+    view = build_view(result, Session(), fake_clock)
+    lines = screen_lines(view, policy_for(120, height=height))
+    assert lines[0].startswith("terminal too small")
+    assert view.gap_notice in lines and view.gap_notice.startswith(
+        "coordinator questions:"
+    )
+
+
+@pytest.mark.parametrize("width", [79, 60, 40])
+def test_below_80_columns_the_diagnostic_keeps_the_question_source_line(
+    fake_clock, width
+):
+    _, result = question_result(ok_message(make_question_rows(2)), fake_clock)
+    view = build_view(result, Session(), fake_clock)
+    lines = screen_lines(view, policy_for(width))
+    flat = "".join("".join(lines).split())
+    assert "".join(view.gap_notice.split()) in flat
+    assert all(cell_len(l) <= width for l in lines)
+
+
+def test_the_inspector_keeps_room_by_showing_only_the_one_line_summary(fake_clock):
+    _, result = question_result(ok_message(make_question_rows(40)), fake_clock)
+    session, _ = apply_key(
+        Session(), Key("down"), build_view(result, Session(), fake_clock), fake_clock
+    )
+    session, _ = apply_key(
+        session, Key("enter"), build_view(result, session, fake_clock), fake_clock
+    )
+    view = build_view(result, session, fake_clock)
+    lines = screen_lines(view, policy_for(120, height=30))
+    assert view.focus == "inspector" and view.gap_notice in lines
+    assert not any("reason unknown" in l for l in lines)
+
+
+def test_ascii_mode_renders_only_ascii_for_a_non_ascii_subject(fake_clock):
+    rows = make_question_rows(2, subject="héllo wörld 界")
+    _, result = question_result(ok_message(rows), fake_clock)
+    lines = screen_lines(
+        build_view(result, Session(), fake_clock), policy_for(120, ascii=True)
+    )
+    assert all(ord(ch) < 128 for l in lines for ch in l)
+    assert not any(bad_chars(l) for l in lines)
+
+
+def test_rendering_the_panel_twice_is_byte_identical(fake_clock):
+    _, result = question_result(ok_message(make_question_rows(7)), fake_clock)
+    view = build_view(result, Session(), fake_clock)
+    policy = policy_for(116)
+    assert printed(view, policy) == printed(view, policy)
+
+
+# -- T47: questions off is byte-identical to release 1 (against release 1's own recorded bytes) ------------------------
+
+
+def test_t47_questions_off_is_byte_identical_to_the_recorded_release_1_surface():
+    from tests.observe.release1_surface import surface
+
+    golden = json.loads(
+        (Path(__file__).parent / "golden_release1_surface.json").read_text(
+            encoding="utf-8"
+        )
+    )
+    current = surface()
+    assert current.keys() == golden.keys()
+    for variant, expected in golden.items():
+        assert current[variant].keys() == expected.keys(), variant
+        for key, text in expected.items():
+            assert current[variant][key] == text, f"{variant}:{key}"
diff --git a/tests/observe/test_view.py b/tests/observe/test_view.py
index 0994decb8..e6e8f327c 100644
--- a/tests/observe/test_view.py
+++ b/tests/observe/test_view.py
@@ -867,3 +867,229 @@ def test_view_reexports_unknown_and_is_the_only_place_that_names_it_as_a_screen_
         path = Path(view_module.__file__).with_name(name)
         if path.exists():
             assert "observe.parse" not in path.read_text(encoding="utf-8")
+
+
+# -- R2: the coordinator questions panel (T19, T47, T10, T11, T12, T46) --------------------------------------------------
+
+import dataclasses  # noqa: E402
+
+import pytest  # noqa: E402
+
+from superclaude.cli.observe.parse import parse_questions  # noqa: E402
+from superclaude.cli.observe.questions import merge_questions  # noqa: E402
+from superclaude.cli.observe.view import (  # noqa: E402
+    MESSAGES_CELL,
+    QUESTIONS_DISCLOSURE,
+    QUESTIONS_NOT_HELD,
+    Key,
+    apply_key,
+)
+from tests.observe.conftest import (  # noqa: E402
+    QRUN,
+    make_question_envelope,
+    make_question_error,
+    make_question_rows,
+    routed_runner_responses,
+)
+
+WORKER = rows_reply(make_rows(3, 1), total=3)
+
+
+def question_pair(rows):
+    return 0, json.dumps(make_question_envelope(rows))
+
+
+def error_pair(code, status=1):
+    return status, json.dumps(make_question_error(code))
+
+
+def questions_collector(message, clock, argv_log=None, worker=WORKER):
+    argv_log = [] if argv_log is None else argv_log
+    runner = FakeRunner(argv_log, [routed_runner_responses(worker, message)])
+    return Collector(
+        LiveSource(runner, FakeDiscover(argv_log, "/opt/fake/orca")),
+        clock,
+        run_id=QRUN,
+        questions=True,
+    )
+
+
+def panel_of(result, clock, session=None):
+    return build_view(result, session or Session(), clock)
+
+
+def test_t19_the_panel_title_and_disclosure_are_literal_and_the_gap_notice_is_replaced(
+    fake_clock,
+):
+    result = questions_collector(
+        question_pair(make_question_rows(2)), fake_clock
+    ).run_once()
+    view = panel_of(result, fake_clock)
+    panel = view.questions
+    assert panel.title == "COORDINATOR QUESTIONS"
+    assert panel.run_line == f"one Run only: {QRUN}"
+    assert "at most 100 rows per read, not 100 questions" in panel.disclosure
+    assert "bounded best effort; coverage unknown" in panel.disclosure
+    assert panel.disclosure == QUESTIONS_DISCLOSURE
+    assert panel.disclosure.endswith("bursts over 100 rows between reads may be lost")
+    assert view.gap_notice != GAP_NOTICE and "Human" not in view.gap_notice
+    assert view.gap_notice.startswith("coordinator questions:")
+    assert view.ledger_title == LEDGER_TITLE  # the worker ledger keeps its own title
+    assert "coordinator questions: one Run, last read 0s ago" in view.header2
+    assert MESSAGES_CELL not in view.header2
+    assert panel.counts_line == (
+        "observed open: 2 | closed by evidence: unavailable (no source)"
+    )
+    assert [q.text.endswith("reason unknown") for q in panel.lines] == [True, True]
+    assert [q.qid for q in panel.lines] == ["msg_000000000000", "msg_000000000001"]
+
+
+def test_t47_with_questions_off_the_view_is_the_release_1_view(fake_clock, argv_log):
+    collector = live_collector([WORKER], fake_clock, argv_log)
+    result = collector.run_once()
+    view = build_view(result, Session(), fake_clock)
+    assert view.questions is None and view.gap_notice == GAP_NOTICE
+    assert MESSAGES_CELL in view.header2 and "coordinator" not in view.header2
+    explicit_off = dataclasses.replace(
+        result, question_state="OFF", questions=None, question_read=None
+    )
+    assert build_view(explicit_off, Session(), fake_clock) == view
+    # Questions on but nothing read yet: the gap notice stays, the pending line is shown.
+    pending = questions_collector(question_pair([]), fake_clock).latest()
+    waiting = build_view(pending, Session(), fake_clock)
+    assert waiting.gap_notice == GAP_NOTICE and waiting.questions.state == "PENDING"
+    assert waiting.questions.replaces_gap is False
+    assert "question read pending" in waiting.questions.summary
+    assert "last read" not in waiting.header2 and "not read yet" in waiting.header2
+
+
+def test_t10_m_on_every_worker_row_leaves_the_question_count_unchanged(fake_clock):
+    collector = questions_collector(question_pair(make_question_rows(3)), fake_clock)
+    result = collector.run_once()
+    session = Session()
+    before = build_view(result, session, fake_clock).questions
+    view = build_view(result, session, fake_clock)
+    for _ in range(3):  # select each worker row in turn and mark
+        session, _ = apply_key(session, Key("down"), view, fake_clock)
+        view = build_view(result, session, fake_clock)
+        session, _ = apply_key(session, Key("text", "m"), view, fake_clock)
+        view = build_view(result, session, fake_clock)
+    after = view.questions
+    assert session.marked is True
+    assert (after.counts_line, after.open_total, after.lines) == (
+        before.counts_line,
+        before.open_total,
+        before.lines,
+    )
+
+
+def test_t12_and_t11_retained_and_left_questions_render_with_their_marks(fake_clock):
+    two = question_pair(make_question_rows(2))
+    one_newer = question_pair(
+        make_question_rows(2, start=1)
+    )  # question 0 left the window
+    collector = questions_collector(
+        [two, one_newer, error_pair("consumer_fenced")], fake_clock
+    )
+    collector.run_once()
+    shifted = collector.run_once()
+    panel = panel_of(shifted, fake_clock).questions
+    assert panel.counts_line.startswith("observed open: 3 |")
+    assert [q.in_window for q in panel.lines] == [False, True, True]
+    assert panel.lines[0].text.endswith("no longer in source window")
+    failed = panel_of(collector.run_once(), fake_clock).questions
+    assert failed.state == "FAILED" and failed.code == "consumer-fenced"
+    assert failed.state_lines[0].startswith("FAILED (consumer fenced)")
+    assert QUESTIONS_NOT_HELD in failed.state_lines
+    assert failed.lines == panel.lines  # a failed read keeps every retained question
+    assert failed.counts_line == panel.counts_line
+
+
+def test_the_source_loss_never_closes_or_lowers_the_count_and_stale_keeps_questions(
+    fake_clock,
+):
+    collector = questions_collector(question_pair(make_question_rows(2)), fake_clock)
+    result = collector.run_once()
+    fake_clock.advance(46.0)
+    stale = panel_of(result, fake_clock).questions
+    assert stale.state == "STALE" and stale.state_lines == ("STALE 46s",)
+    assert stale.counts_line.startswith("observed open: 2 |") and len(stale.lines) == 2
+    assert "closed" not in " ".join(q.text for q in stale.lines)
+
+
+def test_an_empty_good_read_never_says_no_questions(fake_clock):
+    result = questions_collector(question_pair([]), fake_clock).run_once()
+    panel = panel_of(result, fake_clock).questions
+    assert panel.empty_text == (
+        "no observed questions in this source window; not proof none exist"
+    )
+    everything = " ".join(
+        [panel.summary, panel.counts_line, panel.empty_text, *panel.state_lines]
+    ).lower()
+    assert "no questions" not in everything
+    assert panel.counts_line.startswith("observed open: 0 |")
+
+
+def test_a_failed_first_read_names_the_unheld_run_and_shows_unknown_not_zero(
+    fake_clock,
+):
+    for code in ("no_active_terminal", "consumer_fenced"):
+        result = questions_collector(error_pair(code), fake_clock).run_once()
+        panel = panel_of(result, fake_clock).questions
+        assert panel.state == "FAILED" and QUESTIONS_NOT_HELD in panel.state_lines
+        assert panel.counts_line.startswith("observed open: unknown")
+        assert panel.replaces_gap and panel.open_total is UNKNOWN
+
+
+def test_t46_retention_exceeded_reads_unknown_with_the_retained_count(fake_clock):
+    result = questions_collector(
+        question_pair(make_question_rows(1)), fake_clock
+    ).run_once()
+    state = None
+    for start in range(0, 1001, 100):
+        rows = make_question_rows(min(100, 1001 - start), start=start)
+        parsed = parse_questions(make_question_envelope(rows), "ns", 1, QRUN)
+        state = merge_questions(state, parsed.rows, start // 100 + 1, True, True, QRUN)
+    over = dataclasses.replace(result, questions=state)
+    panel = panel_of(over, fake_clock).questions
+    assert "unknown (retention exceeded)" in panel.counts_line
+    assert "retained 1000" in panel.counts_line
+    assert panel.open_total is UNKNOWN and (panel.retained, panel.evicted) == (1000, 1)
+
+
+def test_markup_and_injection_in_a_subject_are_literal_text_in_the_view(fake_clock):
+    rows = make_question_rows(1, subject="[bold]loud[/bold] \x1b[31mred\x1b[0m ‮")
+    result = questions_collector(question_pair(rows), fake_clock).run_once()
+    (line,) = panel_of(result, fake_clock).questions.lines
+    assert "[bold]loud[/bold]" in line.text
+    assert "\x1b" not in line.text and "‮" not in line.text
+
+
+def test_window_full_is_shown_at_exactly_100_rows_only(fake_clock):
+    full = questions_collector(
+        question_pair(make_question_rows(100)), fake_clock
+    ).run_once()
+    assert panel_of(full, fake_clock).questions.window_full_text == (
+        "window full: older questions may be missing"
+    )
+    short = questions_collector(
+        question_pair(make_question_rows(99)), fake_clock
+    ).run_once()
+    assert panel_of(short, fake_clock).questions.window_full_text is None
+
+
+def test_the_panel_never_carries_a_body_handle_or_payload(fake_clock):
+    result = questions_collector(
+        question_pair(make_question_rows(2)), fake_clock
+    ).run_once()
+    panel = panel_of(result, fake_clock).questions
+    flat = repr(panel)
+    for forbidden in ("synthetic body", "term_synthetic", "run:run_", "payload"):
+        assert forbidden not in flat, forbidden
+
+
+@pytest.mark.parametrize("n", [0, 1])
+def test_questions_pending_summary_is_one_line(fake_clock, n):
+    pending = questions_collector(question_pair([]), fake_clock).latest()
+    summary = panel_of(pending, fake_clock).questions.summary
+    assert "\n" not in summary and summary.endswith(QRUN)


Delta diff from the previous reviewed tree (empty on the first review): 
diff --git a/tests/observe/release1_surface.py b/tests/observe/release1_surface.py
new file mode 100644
index 000000000..d2d089355
--- /dev/null
+++ b/tests/observe/release1_surface.py
@@ -0,0 +1,62 @@
+"""The questions-off surface of the observer, as a plain dict (T47 byte-identity with release 1).
+
+``golden_release1_surface.json`` was generated by running ``surface()`` against the release 1
+source, ``git archive 9e2608b03 src/superclaude`` (the commit before release 2), with
+``PYTHONPATH=<that tree>:.`` and ``uv run python``. A test runs ``surface()`` against the
+current source and compares it with that file, so "questions off is byte-identical to
+release 1" is checked against release 1's own bytes, not against the current code.
+
+This module uses only names that exist in release 1.
+"""
+
+from __future__ import annotations
+
+import io
+
+from rich.console import Console
+
+from superclaude.cli.observe.collector import Collector, FixtureSource
+from superclaude.cli.observe.export import record_text, snapshot_json
+from superclaude.cli.observe.render import render, screen_lines
+from superclaude.cli.observe.terminal import make_console, resolve_policy
+from superclaude.cli.observe.view import Session, build_view
+from tests.observe.conftest import FakeClock
+
+VARIANTS = ("base", "empty", "source-loss", "injection", "missing-fields")
+WIDTHS = (160, 116, 80)
+HEIGHTS = (40, 12)
+
+
+def _policy(width: int, height: int):
+    return resolve_policy({}, "utf-8", {"ascii": False}, width, height)
+
+
+def _printed(view, policy) -> str:
+    buffer = io.StringIO()
+    console: Console = make_console(policy, file=buffer, record=True)
+    console.print(render(view, policy))
+    return buffer.getvalue()
+
+
+def surface() -> dict:
+    out: dict = {}
+    for variant in VARIANTS:
+        clock = FakeClock()
+        collector = Collector(FixtureSource(variant), clock)
+        result = collector.run_once()
+        result = collector.run_once()
+        view = build_view(result, Session(), clock)
+        entry: dict = {
+            "header1": view.header1,
+            "header2": view.header2,
+            "gap_notice": view.gap_notice,
+            "record_text": record_text(view),
+            "snapshot_json": snapshot_json(view),
+        }
+        for width in WIDTHS:
+            for height in HEIGHTS:
+                policy = _policy(width, height)
+                entry[f"lines_{width}x{height}"] = screen_lines(view, policy)
+            entry[f"printed_{width}"] = _printed(view, _policy(width, 40))
+        out[variant] = entry
+    return out
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index 45e1cd23d..50116a8bc 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -606,3 +606,22 @@ def test_rendering_the_panel_twice_is_byte_identical(fake_clock):
     view = build_view(result, Session(), fake_clock)
     policy = policy_for(116)
     assert printed(view, policy) == printed(view, policy)
+
+
+# -- T47: questions off is byte-identical to release 1 (against release 1's own recorded bytes) ------------------------
+
+
+def test_t47_questions_off_is_byte_identical_to_the_recorded_release_1_surface():
+    from tests.observe.release1_surface import surface
+
+    golden = json.loads(
+        (Path(__file__).parent / "golden_release1_surface.json").read_text(
+            encoding="utf-8"
+        )
+    )
+    current = surface()
+    assert current.keys() == golden.keys()
+    for variant, expected in golden.items():
+        assert current[variant].keys() == expected.keys(), variant
+        for key, text in expected.items():
+            assert current[variant][key] == text, f"{variant}:{key}"


Earlier blocking findings of this start (empty on the first review): 
F1.1 ac=T10.AC1 at=tests/observe/test_render.py:492 anchor="T47 with questions off is byte-identical to release 1 output" chk=y,n,n,n family=t47-byte-identity fix=Compare the questions-off screen_lines output against a frozen release-1 reference. For example, render the same fixture view with the start-sha render logic or a stored golden, and assert the lists are equal. At `tests/observe/test_view.py:947` the check `build_view(explicit_off) == view` compares the new code with itself. `test_render.py:492` only asserts that `GAP_NOTICE` is present and that no line contains "COORDINATOR". covers="T47 with questions off is byte-identical to release 1 output": The T47 tests do not compare against release 1 bytes. The code appears equivalent, so this is a missing proof, not a visible output change.

Saved-probe re-check hit locations (may be empty): 
probe hits (location only):
tests/observe/test_render.py:611:# -- T47: questions off is 
tests/observe/test_render.py:618:        (Path(__file__).par


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
