92e3a5822c4cab0cbab81b9ff398a9b35a095064
Review one task for spec compliance.

Task brief: 
## Task 11: Add the question group to the snapshot export

Depends on: Task 10

Edit `src/superclaude/cli/observe/export.py`, `src/superclaude/cli/observe/snapshot.schema.json` and add tests to `tests/observe/test_snapshot_schema.py` and `tests/observe/test_export.py`.

- Add an optional `questions` object to the snapshot when questions are on: `runId`, `state`, `code`, `observedOpen` (number or the string `UNKNOWN`), `windowFull`, `retained`, `evicted`, `closureEvidence` fixed to `unavailable`, and per question only `id`, `createdAt`, `ageSeconds`, `inWindow`. No subject, body, handle or payload is exported. The record text export (`e`, `--once`) carries the same lines as the screen.
- Keep `schemaVersion` 1 if the schema accepts the optional group; otherwise record the change in the schema file and the test (the existing test rejects an unknown major).

Acceptance criteria:
- `uv run pytest tests/observe/test_snapshot_schema.py tests/observe/test_export.py -v` passes: a snapshot with questions on validates; one with questions off is byte-identical to release 1; a test asserts the exported JSON holds no `subject`, `body`, `from_handle` or `payload` key anywhere; missing values are the string `UNKNOWN`.
- The record export contains no ESC byte and the full question ids.

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

Start sha: 92e3a5822c4cab0cbab81b9ff398a9b35a095064
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/export.py b/src/superclaude/cli/observe/export.py
index 057547296..5f16fab89 100644
--- a/src/superclaude/cli/observe/export.py
+++ b/src/superclaude/cli/observe/export.py
@@ -94,9 +94,31 @@ def record_text(view: View) -> str:
     ]
     lines.extend(view.ledger_empty)
     lines.extend(_row_line(row) for row in view.all_rows)
+    lines.extend(_question_lines(view))
     return "\n".join(sanitize(line, "line") for line in lines) + "\n"
 
 
+def _question_lines(view: View) -> list[str]:
+    """The R2 panel as record lines: every question with its full id, no windowing."""
+    panel = view.questions
+    if panel is None:
+        return []
+    lines = [panel.title, panel.run_line]
+    if not panel.replaces_gap:
+        lines.append(panel.summary)  # nothing read yet: the gap notice above stays
+    lines.append(panel.disclosure)
+    lines.extend(panel.state_lines)
+    lines.append(panel.counts_line)
+    lines.extend(f"{q.qid} | {q.text}" for q in panel.lines)
+    lines.extend(
+        text
+        for text in (panel.empty_text, panel.window_full_text, *panel.notes)
+        if text
+    )
+    lines.append(panel.retention_line)
+    return lines
+
+
 # -- JSON snapshot -----------------------------------------------------------------------------------
 
 
@@ -134,6 +156,31 @@ def _row_dict(view_row: RowView) -> dict:
     return out
 
 
+def _questions_dict(panel: Any) -> dict:
+    """The optional ``questions`` group: ids, times and counts only (never subject or body)."""
+    out: dict = {
+        "runId": panel.run_id,
+        "state": panel.state,
+        "observedOpen": _unknown(panel.open_total),
+        "windowFull": panel.window_full,
+        "retained": panel.retained,
+        "evicted": panel.evicted,
+        "closureEvidence": "unavailable",
+        "items": [
+            {
+                "id": q.qid,
+                "createdAt": _text(q.created_at),
+                "ageSeconds": _unknown(q.age_seconds),
+                "inWindow": q.in_window,
+            }
+            for q in panel.lines
+        ],
+    }
+    if panel.code is not None:
+        out["code"] = panel.code
+    return out
+
+
 def snapshot_dict(view: View) -> dict:
     meta = view.meta
     source: dict = {
@@ -158,6 +205,8 @@ def snapshot_dict(view: View) -> dict:
         "counts": _unknown(meta.counts),
         "rows": [_row_dict(row) for row in view.all_rows],
     }
+    if view.questions is not None:
+        snapshot["questions"] = _questions_dict(view.questions)
     if meta.collection_state is not None:
         snapshot["collection"] = {
             "state": meta.collection_state,
diff --git a/src/superclaude/cli/observe/snapshot.schema.json b/src/superclaude/cli/observe/snapshot.schema.json
index ccf9b501b..5dd6bf3b0 100644
--- a/src/superclaude/cli/observe/snapshot.schema.json
+++ b/src/superclaude/cli/observe/snapshot.schema.json
@@ -62,6 +62,36 @@
         "duplicatesIgnored": {"type": "integer", "minimum": 0}
       }
     },
+    "questions": {
+      "description": "Optional (R2, only when the coordinator-questions source is on): the retained questions of the one named Run. No subject, body, handle or payload is ever exported.",
+      "type": "object",
+      "additionalProperties": false,
+      "required": ["runId", "state", "observedOpen", "windowFull", "retained", "evicted", "closureEvidence", "items"],
+      "properties": {
+        "runId": {"$ref": "#/definitions/text"},
+        "state": {"enum": ["PENDING", "OK", "STALE", "FAILED"]},
+        "code": {"type": "string"},
+        "observedOpen": {"anyOf": [{"type": "integer", "minimum": 0}, {"const": "UNKNOWN"}]},
+        "windowFull": {"type": "boolean"},
+        "retained": {"type": "integer", "minimum": 0},
+        "evicted": {"type": "integer", "minimum": 0},
+        "closureEvidence": {"const": "unavailable"},
+        "items": {
+          "type": "array",
+          "items": {
+            "type": "object",
+            "additionalProperties": false,
+            "required": ["id", "createdAt", "ageSeconds", "inWindow"],
+            "properties": {
+              "id": {"$ref": "#/definitions/text"},
+              "createdAt": {"$ref": "#/definitions/text"},
+              "ageSeconds": {"anyOf": [{"type": "number", "minimum": 0}, {"const": "UNKNOWN"}]},
+              "inWindow": {"type": "boolean"}
+            }
+          }
+        }
+      }
+    },
     "rows": {"type": "array", "items": {"$ref": "#/definitions/row"}}
   },
   "definitions": {
diff --git a/tests/observe/test_export.py b/tests/observe/test_export.py
index 15e922aae..c6fb930cc 100644
--- a/tests/observe/test_export.py
+++ b/tests/observe/test_export.py
@@ -241,3 +241,67 @@ def test_export_does_not_import_render_parse_or_adapter_or_use_a_console():
         r"observe\.(render|parse|adapter|collector)\b|Console\b|from rich|import rich",
         text,
     )
+
+
+# -- R2: the record export carries the same question lines as the screen ---------------------------------------------------
+
+from superclaude.cli.observe.view import QUESTIONS_DISCLOSURE  # noqa: E402
+from tests.observe.conftest import (  # noqa: E402
+    QRUN,
+    make_question_envelope,
+    make_question_rows,
+    routed_runner_responses,
+)
+
+
+def question_view(rows, clock, session=None):
+    from superclaude.cli.observe.view import Session, build_view
+
+    worker = (0, json.dumps(make_envelope(make_rows(3, 1), total=3)))
+    message = (0, json.dumps(make_question_envelope(rows)))
+    runner = FakeRunner([], [routed_runner_responses(worker, message)])
+    collector = Collector(
+        LiveSource(runner, FakeDiscover([])), clock, run_id=QRUN, questions=True
+    )
+    return build_view(collector.run_once(), session or Session(), clock)
+
+
+def test_the_record_lists_every_question_with_its_full_id_and_no_escape(fake_clock):
+    long_id = "msg_" + "a" * 60
+    rows = make_question_rows(3, subject="[bold]loud[/bold] \x1b[31mred\x1b[0m")
+    rows[0]["id"] = long_id
+    text = record_text(question_view(rows, fake_clock))
+    assert "\x1b" not in text and long_id in text
+    lines = text.splitlines()
+    assert "COORDINATOR QUESTIONS" in lines and f"one Run only: {QRUN}" in lines
+    assert QUESTIONS_DISCLOSURE in lines
+    assert sum(" | " in ln and "reason unknown" in ln for ln in lines) == 3
+    assert "observed open: 3 | closed by evidence: unavailable (no source)" in lines
+    assert any(ln.startswith("retention reset at ") for ln in lines)
+    assert "[bold]loud[/bold]" in text  # literal text, as on the screen
+    assert not any(ord(ch) in range(0x80, 0xA0) for ch in text)
+
+
+def test_the_record_with_questions_off_has_no_question_lines(fake_clock):
+    text = record_text(fixture_view("base", fake_clock))
+    assert "COORDINATOR" not in text and "reason unknown" not in text
+    assert (
+        "Human questions: source UNVERIFIED" in text
+    )  # the release 1 gap notice stays
+
+
+def test_the_record_keeps_the_question_lines_in_a_failed_state(fake_clock):
+    from superclaude.cli.observe.view import Session, build_view
+
+    worker = (0, json.dumps(make_envelope(make_rows(2, 1), total=2)))
+    good = (0, json.dumps(make_question_envelope(make_question_rows(2))))
+    fenced = (1, json.dumps({"ok": False, "error": {"code": "consumer_fenced"}}))
+    runner = FakeRunner([], [routed_runner_responses(worker, [good, fenced])])
+    collector = Collector(
+        LiveSource(runner, FakeDiscover([])), fake_clock, run_id=QRUN, questions=True
+    )
+    collector.run_once()
+    text = record_text(build_view(collector.run_once(), Session(), fake_clock))
+    assert "FAILED (consumer fenced)" in text
+    assert "this terminal does not hold the named Run" in text
+    assert text.count("reason unknown") == 2
diff --git a/tests/observe/test_snapshot_schema.py b/tests/observe/test_snapshot_schema.py
index ae4d8be24..e560879fe 100644
--- a/tests/observe/test_snapshot_schema.py
+++ b/tests/observe/test_snapshot_schema.py
@@ -408,3 +408,151 @@ def test_not_reobserved_rows_carry_the_flag_and_output_is_indented_and_sorted(
     assert flagged == ["w-003"]
     assert text == json.dumps(data, indent=2, sort_keys=True)
     assert re.match(r'^\{\n  "collection"', text)
+
+
+# -- R2: the optional questions group (ids, times and counts only) --------------------------------------------------------
+
+from superclaude.cli.observe.export import snapshot_dict  # noqa: E402
+from tests.observe.conftest import (  # noqa: E402
+    QRUN,
+    make_question_envelope,
+    make_question_error,
+    make_question_rows,
+    routed_runner_responses,
+)
+
+WITHHELD_QUESTION_KEYS = {"subject", "body", "from_handle", "to_handle", "payload"}
+
+
+def question_cycle(message, clock, cycles=1, **kw):
+    worker = (0, json.dumps(make_envelope(make_rows(3, 1), total=3)))
+    runner = FakeRunner([], [routed_runner_responses(worker, message)])
+    collector = Collector(
+        LiveSource(runner, FakeDiscover([])), clock, run_id=QRUN, questions=True, **kw
+    )
+    result = None
+    for _ in range(cycles):
+        result = collector.run_once()
+    return collector, result
+
+
+def ok_pair(rows):
+    return 0, json.dumps(make_question_envelope(rows))
+
+
+def questions_snapshot(message, clock, cycles=1):
+    _, result = question_cycle(message, clock, cycles)
+    return json.loads(snapshot_json(build_view(result, Session(), clock)))
+
+
+def test_a_snapshot_with_questions_on_validates_and_keeps_schema_version_1(fake_clock):
+    snapshot = questions_snapshot(ok_pair(make_question_rows(3)), fake_clock)
+    assert not list(VALIDATOR.iter_errors(snapshot))
+    assert snapshot["schemaVersion"] == 1
+    group = snapshot["questions"]
+    assert group["runId"] == QRUN and group["state"] == "OK"
+    assert group["observedOpen"] == 3 and group["closureEvidence"] == "unavailable"
+    assert (group["windowFull"], group["retained"], group["evicted"]) == (False, 3, 0)
+    assert "code" not in group
+    assert [i["id"] for i in group["items"]] == [
+        "msg_000000000000",
+        "msg_000000000001",
+        "msg_000000000002",
+    ]
+    for item in group["items"]:
+        assert set(item) == {"id", "createdAt", "ageSeconds", "inWindow"}
+        assert item["inWindow"] is True and isinstance(item["ageSeconds"], float)
+
+
+def test_the_questions_group_carries_the_failure_code_and_window_flags(fake_clock):
+    fenced = (1, json.dumps(make_question_error("consumer_fenced")))
+    snapshot = questions_snapshot(
+        [ok_pair(make_question_rows(100)), fenced], fake_clock, cycles=2
+    )
+    assert not list(VALIDATOR.iter_errors(snapshot))
+    group = snapshot["questions"]
+    assert (group["state"], group["code"]) == ("FAILED", "consumer-fenced")
+    assert group["windowFull"] is True and group["retained"] == 100
+    first = questions_snapshot(fenced, fake_clock)
+    assert first["questions"]["observedOpen"] == "UNKNOWN"  # nothing read, never 0
+    assert not list(VALIDATOR.iter_errors(first))
+
+
+def test_a_snapshot_with_questions_off_has_no_questions_key_and_is_unchanged(
+    fake_clock,
+):
+    snapshot = live_snapshot(make_rows(3, 1), fake_clock)
+    assert "questions" not in snapshot and not list(VALIDATOR.iter_errors(snapshot))
+    for variant in VARIANTS:
+        for shot in every_snapshot(variant, fake_clock):
+            assert "questions" not in shot
+
+
+def test_exported_question_json_holds_no_subject_body_handle_or_payload_key(fake_clock):
+    rows = make_question_rows(3, subject="visible only on screen")
+    snapshot = questions_snapshot(ok_pair(rows), fake_clock)
+    keys = {key for _, key in _only_keys(snapshot["questions"])}
+    assert keys.isdisjoint(WITHHELD_QUESTION_KEYS), keys
+    text = json.dumps(snapshot)
+    for forbidden in (
+        "visible only on screen",
+        "synthetic body",
+        "term_synthetic",
+        "run:run_",
+    ):
+        assert forbidden not in text, forbidden
+
+
+def test_an_unparsable_created_time_exports_the_string_unknown(fake_clock):
+    rows = make_question_rows(1)
+    rows[0]["created_at"] = None
+    snapshot = questions_snapshot(ok_pair(rows), fake_clock)
+    (item,) = snapshot["questions"]["items"]
+    assert (item["createdAt"], item["ageSeconds"]) == ("UNKNOWN", "UNKNOWN")
+    assert not list(VALIDATOR.iter_errors(snapshot))
+
+
+def test_the_schema_rejects_a_misshaped_questions_group(fake_clock):
+    good = questions_snapshot(ok_pair(make_question_rows(1)), fake_clock)
+    for mutate in (
+        lambda g: g.update(closureEvidence="available"),
+        lambda g: g.update(observedOpen="-1"),
+        lambda g: g.update(state="DONE"),
+        lambda g: g.update(subject="leak"),
+        lambda g: g["items"][0].update(subject="leak"),
+        lambda g: g["items"][0].pop("id"),
+    ):
+        bad = copy.deepcopy(good)
+        mutate(bad["questions"])
+        assert list(VALIDATOR.iter_errors(bad))
+
+
+def test_retention_exceeded_exports_unknown_with_the_retained_count(fake_clock):
+    import dataclasses
+
+    from superclaude.cli.observe.parse import parse_questions
+    from superclaude.cli.observe.questions import merge_questions
+
+    _, result = question_cycle(ok_pair(make_question_rows(1)), fake_clock)
+    state = None
+    for start in range(0, 1001, 100):
+        rows = make_question_rows(min(100, 1001 - start), start=start)
+        parsed = parse_questions(make_question_envelope(rows), "ns", 1, QRUN)
+        state = merge_questions(state, parsed.rows, 1 + start // 100, True, True, QRUN)
+    over = dataclasses.replace(result, questions=state)
+    snapshot = json.loads(snapshot_json(build_view(over, Session(), fake_clock)))
+    group = snapshot["questions"]
+    assert (group["observedOpen"], group["retained"], group["evicted"]) == (
+        "UNKNOWN",
+        1000,
+        1,
+    )
+    assert not list(VALIDATOR.iter_errors(snapshot))
+
+
+def test_snapshot_dict_and_json_agree_on_the_questions_group(fake_clock):
+    _, result = question_cycle(ok_pair(make_question_rows(2)), fake_clock)
+    view = build_view(result, Session(), fake_clock)
+    assert (
+        json.loads(snapshot_json(view))["questions"] == snapshot_dict(view)["questions"]
+    )


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
