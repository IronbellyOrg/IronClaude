9d2b2d48cef4aa08ea82db6a74196a5011d081a8
Review one task for spec compliance.

Task brief: 
## Task 7: Parse question rows in parse.py

Depends on: Task 6

Edit `src/superclaude/cli/observe/parse.py` and add tests to `tests/observe/test_parse.py`. First open REPORT's evidence files 03, 14 and 24 and use their real key names; invent no key.

- Add a frozen `Question` dataclass: `qid` (the `message.id`), `run_id`, `namespace`, `from_handle`, `subject`, `priority`, `thread_id`, `created_at` (text) and `created_epoch` (parsed with `parse_timestamp`, else unknown), every field `UNKNOWN` when absent. `body`, `payload` and `to_handle` are not kept.
- Add `parse_questions(page, namespace, cycle)` returning rows plus counts: required `result.messages` a JSON list (else `ShapeError`, same rule as `parse_page`); a row that is not an object is counted and skipped; a row whose `type` is not `question`, or whose `run_id` differs from the requested Run, is dropped and counted as `contradictory rows ignored`; a row with no `id` has no identity, is flagged `identity unknown`, is not retained; duplicate ids in one read are counted. All strings pass `sanitize`.
- Identity is Run plus `message.id`; never a `dispatchId`.

Acceptance criteria:
- `uv run pytest tests/observe/test_parse.py -v` passes with new tests built from the probe shapes: a 2-row envelope parses to 2 `Question` rows; `result.messages` missing, `null` or not a list raises `ShapeError`; a status-type row and a wrong-Run row are dropped and counted; absent `subject` reads `UNKNOWN`; `[bold]` in a subject stays literal text; no parsed object has a `body` attribute.
- A deep-nesting or injection subject (CSI, OSC 8, U+202E) leaves no ESC, C1 or Cf character in the parsed value.

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

Start sha: 9d2b2d48cef4aa08ea82db6a74196a5011d081a8
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/parse.py b/src/superclaude/cli/observe/parse.py
index 1947ff42c..6c6cc586a 100644
--- a/src/superclaude/cli/observe/parse.py
+++ b/src/superclaude/cli/observe/parse.py
@@ -410,6 +410,128 @@ def parse_page(
     )
 
 
+# -- question rows (R2; keys seen on probe Runs only, UNVERIFIED for other Runs) -----------
+
+QUESTION_TYPE = "question"
+
+
+@dataclass(frozen=True)
+class Question:
+    """One coordinator question row. Identity is the Run plus ``message.id``, never a
+    ``dispatchId``. ``body``, ``payload`` and ``to_handle`` are not kept; every other
+    value is a sanitized source value or ``UNKNOWN``."""
+
+    qid: Any = UNKNOWN
+    run_id: Any = UNKNOWN
+    namespace: str = ""
+    from_handle: Any = UNKNOWN
+    subject: Any = UNKNOWN
+    priority: Any = UNKNOWN
+    thread_id: Any = UNKNOWN
+    created_at: Any = UNKNOWN
+    created_epoch: Any = UNKNOWN  # epoch seconds, or UNKNOWN when unparsable
+    flags: tuple[str, ...] = ()
+
+    @property
+    def identity_unknown(self) -> bool:
+        return IDENTITY_UNKNOWN in self.flags
+
+
+@dataclass(frozen=True)
+class ParsedQuestions:
+    rows: tuple[Question, ...]
+    cycle: int
+    namespace: str
+    run_id: Any = UNKNOWN  # the Run this read was for (requested, else result.runId)
+    raw_count: int = 0  # entries in result.messages, whatever they were
+    malformed_rows: int = 0  # entries that were not objects
+    contradictory_rows: int = 0  # wrong type or wrong Run: dropped and counted
+    identity_unknown_rows: int = 0  # kept in ``rows`` with a flag, never retained
+    duplicates: int = 0  # repeated ids within this one read
+
+
+_QUESTION_FIELDS: tuple[tuple[str, str], ...] = (
+    ("qid", "id"),
+    ("run_id", "run_id"),
+    ("from_handle", "from_handle"),
+    ("subject", "subject"),
+    ("priority", "priority"),
+    ("thread_id", "thread_id"),
+    ("created_at", "created_at"),
+)
+
+
+def parse_questions(
+    obj: Any, namespace: str, cycle: int, run_id: str | None = None
+) -> ParsedQuestions:
+    """Parse one decoded message-read envelope; raise ``ShapeError`` on a broken one.
+
+    ``result.messages`` must be a JSON list. A row that is not an object is counted and
+    skipped; a row whose ``type`` is not ``question`` or whose ``run_id`` differs from the
+    Run read is dropped and counted as contradictory; a row with no usable ``id`` has no
+    identity. ``run_id`` is the requested Run; without it ``result.runId`` stands in.
+    """
+    result = obj.get("result") if isinstance(obj, dict) else None
+    if not isinstance(result, dict):
+        raise ShapeError("result is not an object")
+    messages = result.get("messages")
+    if not isinstance(messages, list):
+        raise ShapeError("result.messages is not a list")
+    reported = result.get("runId")
+    run = run_id if run_id else reported
+    run = sanitize(run, "line") if isinstance(run, str) and run.strip() else UNKNOWN
+
+    rows: list[Question] = []
+    seen: set[str] = set()
+    malformed = contradictory = anonymous = duplicates = 0
+    for raw in messages:
+        if not isinstance(raw, dict):
+            malformed += 1
+            continue
+        values: dict[str, Any] = {}
+        for attr, key in _QUESTION_FIELDS:
+            found = raw.get(key)
+            values[attr] = UNKNOWN if found is None else _value(found, attr)
+        if raw.get("type") != QUESTION_TYPE or (
+            run is not UNKNOWN
+            and values["run_id"] is not UNKNOWN
+            and values["run_id"] != run
+        ):
+            contradictory += 1
+            continue
+        qid = values["qid"]
+        flags: tuple[str, ...] = ()
+        if not isinstance(qid, str) or not qid.strip():
+            values["qid"] = UNKNOWN
+            flags = (IDENTITY_UNKNOWN,)
+            anonymous += 1
+        elif qid in seen:
+            duplicates += 1
+            continue
+        else:
+            seen.add(qid)
+        epoch = parse_timestamp(raw.get("created_at"))
+        rows.append(
+            Question(
+                namespace=namespace,
+                created_epoch=UNKNOWN if epoch is None else epoch,
+                flags=flags,
+                **values,
+            )
+        )
+    return ParsedQuestions(
+        rows=tuple(rows),
+        cycle=cycle,
+        namespace=namespace,
+        run_id=run,
+        raw_count=len(messages),
+        malformed_rows=malformed,
+        contradictory_rows=contradictory,
+        identity_unknown_rows=anonymous,
+        duplicates=duplicates,
+    )
+
+
 # -- merging --------------------------------------------------------------------------
 
 
diff --git a/tests/observe/test_parse.py b/tests/observe/test_parse.py
index 7f470fe7f..907229955 100644
--- a/tests/observe/test_parse.py
+++ b/tests/observe/test_parse.py
@@ -11,9 +11,11 @@ from superclaude.cli.observe.parse import (
     IDENTITY_UNKNOWN,
     ORDER_UNKNOWN,
     UNKNOWN,
+    Question,
     ShapeError,
     merge,
     parse_page,
+    parse_questions,
     parse_timestamp,
 )
 
@@ -442,3 +444,195 @@ def test_envelope_fields_are_sanitized_and_counted():
 )
 def test_parse_timestamp(value, expected):
     assert parse_timestamp(value) == expected
+
+
+# -- R2: question rows (probe shapes: evidence files 03, 14 and 24 of the gate research) ----------
+
+QRUN = "run_14cfcbd8edf2"
+OTHER_RUN = "run_c1badaa6576b"
+
+
+def qrow(i=1, **extra):
+    row = {
+        "id": f"msg_{i:012x}",
+        "run_id": QRUN,
+        "delivery_contract": "current_delivery",
+        "from_handle": "term_synthetic",
+        "to_handle": f"run:{QRUN}",
+        "subject": f"probe question {i}",
+        "body": "SECRET BODY synthetic",
+        "type": "question",
+        "priority": "normal",
+        "thread_id": None,
+        "payload": {"secret": "synthetic"},
+        "created_at": f"2026-11-11T20:01:{10 + i:02d}Z",
+        "delivered_at": None,
+    }
+    row.update(extra)
+    return row
+
+
+def qenvelope(rows, run=QRUN):
+    return {
+        "id": "env",
+        "ok": True,
+        "result": {
+            "acknowledged": None,
+            "count": len(rows),
+            "messages": rows,
+            "runId": run,
+        },
+    }
+
+
+def test_a_two_row_envelope_parses_to_two_question_rows():
+    parsed = parse_questions(qenvelope([qrow(2), qrow(1)]), "orca-a", 3, QRUN)
+    assert len(parsed.rows) == 2 and parsed.raw_count == 2
+    first = parsed.rows[0]
+    assert isinstance(first, Question)
+    assert (first.qid, first.run_id, first.subject) == (
+        "msg_000000000002",
+        QRUN,
+        "probe question 2",
+    )
+    assert (first.priority, first.from_handle, first.namespace) == (
+        "normal",
+        "term_synthetic",
+        "orca-a",
+    )
+    assert first.thread_id is UNKNOWN  # a JSON null is a fact the source did not give
+    assert first.created_at == "2026-11-11T20:01:12Z"
+    assert isinstance(first.created_epoch, float)
+    assert (parsed.cycle, parsed.run_id) == (3, QRUN)
+    assert parsed.contradictory_rows == parsed.malformed_rows == parsed.duplicates == 0
+
+
+@pytest.mark.parametrize(
+    "broken",
+    [
+        {},
+        [],
+        None,
+        {"result": None},
+        {"result": []},
+        {"result": {"runId": QRUN}},
+        {"result": {"messages": None}},
+        {"result": {"messages": {}}},
+        {"result": {"messages": "x"}},
+        {"result": {"messages": 5}},
+        {"ok": False, "error": {"code": "consumer_fenced"}},
+    ],
+)
+def test_result_messages_must_be_a_json_list(broken):
+    with pytest.raises(ShapeError):
+        parse_questions(broken, "orca-a", 1, QRUN)
+
+
+def test_a_status_row_and_a_wrong_run_row_are_dropped_and_counted():
+    rows = [
+        qrow(1),
+        qrow(2, type="status"),
+        qrow(3, run_id=OTHER_RUN),
+        qrow(4, type=None),
+        qrow(5, type="Question"),
+    ]
+    parsed = parse_questions(qenvelope(rows), "orca-a", 1, QRUN)
+    assert [q.qid for q in parsed.rows] == ["msg_000000000001"]
+    assert parsed.contradictory_rows == 4 and parsed.raw_count == 5
+
+
+def test_without_a_requested_run_the_reported_run_is_the_check():
+    rows = [qrow(1), qrow(2, run_id=OTHER_RUN)]
+    parsed = parse_questions(qenvelope(rows), "orca-a", 1)
+    assert len(parsed.rows) == 1 and parsed.contradictory_rows == 1
+    assert parsed.run_id == QRUN
+
+
+def test_absent_fields_read_unknown_and_never_none_zero_or_false():
+    parsed = parse_questions(
+        qenvelope([{"id": "msg_x", "type": "question"}]), "orca-a", 1, QRUN
+    )
+    (row,) = parsed.rows
+    for name in ("run_id", "from_handle", "subject", "priority", "thread_id"):
+        assert getattr(row, name) is UNKNOWN, name
+    assert row.created_at is UNKNOWN and row.created_epoch is UNKNOWN
+
+
+def test_an_unparsable_created_time_has_no_epoch_but_keeps_its_text():
+    (row,) = parse_questions(
+        qenvelope([qrow(1, created_at="last tuesday")]), "orca-a", 1, QRUN
+    ).rows
+    assert row.created_at == "last tuesday" and row.created_epoch is UNKNOWN
+
+
+def test_markup_in_a_subject_stays_literal_text():
+    (row,) = parse_questions(
+        qenvelope([qrow(1, subject="[bold]loud[/bold] [link=x]y[/link]")]),
+        "orca-a",
+        1,
+        QRUN,
+    ).rows
+    assert row.subject == "[bold]loud[/bold] [link=x]y[/link]"
+
+
+def test_no_parsed_object_keeps_a_body_payload_or_recipient():
+    parsed = parse_questions(qenvelope([qrow(1)]), "orca-a", 1, QRUN)
+    (row,) = parsed.rows
+    for name in ("body", "payload", "to_handle", "dispatch_id", "delivered_at"):
+        assert not hasattr(row, name) and not hasattr(parsed, name), name
+    assert "SECRET" not in repr(parsed) and "run:" not in repr(parsed)
+
+
+INJECTIONS = [
+    "a\x1b[31mred\x1b[0mb",
+    "link \x1b]8;;http://evil.example\x07click\x1b]8;;\x07 end",
+    "bidi ‮evil‬ text",
+    "c1 \x9b31m and \x9d0;title\x9c done",
+    "unterminated \x1b]0;title and more",
+    "bell \x07 and \x00 nul",
+]
+
+
+@pytest.mark.parametrize("subject", INJECTIONS)
+def test_an_injection_subject_leaves_no_escape_c1_or_format_character(subject):
+    import unicodedata
+
+    (row,) = parse_questions(
+        qenvelope([qrow(1, subject=subject, from_handle=subject, priority=subject)]),
+        "orca-a",
+        1,
+        QRUN,
+    ).rows
+    for value in (row.subject, row.from_handle, row.priority):
+        assert isinstance(value, str)
+        for ch in value:
+            assert ch != "\x1b" and not 0x80 <= ord(ch) <= 0x9F, repr(value)
+            assert unicodedata.category(ch) not in ("Cf", "Cc"), repr(value)
+
+
+def test_a_row_without_an_id_has_no_identity_and_duplicate_ids_are_counted():
+    rows = [qrow(1), qrow(1), qrow(2, id=None), qrow(3, id="  "), qrow(4, id=7), "x", 5]
+    parsed = parse_questions(qenvelope(rows), "orca-a", 1, QRUN)
+    assert parsed.duplicates == 1 and parsed.malformed_rows == 2
+    assert parsed.identity_unknown_rows == 3
+    flagged = [q for q in parsed.rows if q.identity_unknown]
+    assert len(flagged) == 3 and all(q.qid is UNKNOWN for q in flagged)
+    assert [q.qid for q in parsed.rows if not q.identity_unknown] == [
+        "msg_000000000001"
+    ]
+
+
+def test_identity_comes_from_message_id_and_never_a_dispatch_id():
+    (row,) = parse_questions(
+        qenvelope([qrow(1, dispatchId="w-001", dispatch_id="w-002")]), "orca-a", 1, QRUN
+    ).rows
+    assert row.qid == "msg_000000000001"
+    assert "w-001" not in repr(row) and "w-002" not in repr(row)
+
+
+def test_a_non_ascii_deeply_nested_subject_becomes_text_not_an_error():
+    nested = {"a": {"b": {"c": [1, 2, {"d": "é"}]}}}
+    (row,) = parse_questions(
+        qenvelope([qrow(1, subject=nested)]), "orca-a", 1, QRUN
+    ).rows
+    assert isinstance(row.subject, str) and "é" in row.subject


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
