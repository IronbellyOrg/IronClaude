2c0fc20bd207a5f4ef80faac8ec4150f1b38998a
Review one task for spec compliance.

Task brief: 
## Task 15: Build the T51 quiet-scope non-consumption test

Depends on: Task 6, Task 9

Create `tests/observe/test_question_quiet_scope.py` (T51, `acceptance-tests.md` as rewritten by Task 5; INV-022). It uses a stateful fake Orca backend over the probe shapes (REPORT section 2.2 steps 1 to 9, evidence files 03 to 12): the fake keeps a mailbox of question rows and a `delivered_at`/ack state, answers only the question template, and fails the test if any argv could consume (`check` without `--all`, `--ack`, `--wait`).

- Step one establishes readable identity: the test asserts every returned row has a `msg_` id, a Run id and a created time before any comparison.
- Then repeated reads on a quiet scope (no sender writes between reads): before-and-after readings through the observer return identical question ids, identical order and an unchanged fake mailbox state (no delivery or ack field changed).
- The test docstring and a final assertion message state that a pass covers only the visible effects tested, as the owner as Run owner on a probe Run, and does not show non-consumption by a non-owner reader (Q-1).

Acceptance criteria:
- `uv run pytest tests/observe/test_question_quiet_scope.py -v` passes; a deliberately consuming fake (mailbox changes on read) makes a companion test fail, proving the test can detect consumption.
- The test file contains no `--peek`, `--ack` or `run-use` argv apart from the assertions that forbid them.

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

Start sha: 2c0fc20bd207a5f4ef80faac8ec4150f1b38998a
Diff against the start snapshot: 
diff --git a/tests/observe/test_question_quiet_scope.py b/tests/observe/test_question_quiet_scope.py
new file mode 100644
index 000000000..9abfa67bb
--- /dev/null
+++ b/tests/observe/test_question_quiet_scope.py
@@ -0,0 +1,203 @@
+"""T51: the quiet-scope non-consumption test for the message read (INV-022).
+
+A stateful fake Orca backend keeps a mailbox of ``question`` rows, a ``delivered_at`` marker per
+row and an acknowledgement set. It answers only the one R2 template. It fails the test if an
+argv could consume (plain ``check`` without ``--all``, or an acknowledgement or wait option) or
+could narrow the read in a way the observer must not use (``--peek`` hides acknowledged rows).
+The shapes follow REPORT 2.2, steps 1 to 9 (``research/evidence`` files 03 to 12 of the gate
+research): rows with ``id`` (``msg_``), ``run_id``, ``created_at`` and ``delivered_at``.
+
+A pass covers ONLY the visible effects tested here, which are the effects the gate research saw
+as the owner of a probe Run: repeated reads through the observer return the same ids in the
+same order and leave the fake mailbox state unchanged. It does NOT show non-consumption by a
+reader that is not the Run's owner (Q-1, UNVERIFIED); that needs a plain terminal and is
+plan Task 16.
+"""
+
+from __future__ import annotations
+
+import copy
+import itertools
+import json
+
+import pytest
+
+from superclaude.cli.observe.adapter import LiveSource
+from superclaude.cli.observe.collector import Collector
+from tests.observe.conftest import (
+    QRUN,
+    QUESTION_BASE,
+    FakeClock,
+    FakeDiscover,
+    FakeRunner,
+    make_envelope,
+    make_question_rows,
+    make_rows,
+)
+
+PASS_SCOPE = (
+    "a pass covers only the visible effects tested, as the owner of a probe Run; "
+    "it does not show non-consumption by a non-owner reader (Q-1)"
+)
+CONSUMING_TOKENS = ("--ack", "--wait", "--peek")  # none may ever reach the backend
+
+
+class FakeOrcaMailbox:
+    """The Run mailbox of one probe Run, answering only the R2 message template."""
+
+    consuming = False  # a consuming fake changes the mailbox on every read
+
+    def __init__(self, rows):
+        self.rows = [dict(r) for r in rows]  # newest first, as check --all returns them
+        self.delivery = None  # a pending delivery id, set only by a consuming read
+        self.acknowledged = []
+        self._envelope_ids = itertools.count(1)
+        self.reads = 0
+
+    def fingerprint(self):
+        """Every piece of state a read could change: rows, markers, delivery and acks."""
+        return json.dumps(
+            {
+                "rows": self.rows,
+                "delivery": self.delivery,
+                "acknowledged": self.acknowledged,
+            },
+            sort_keys=True,
+        )
+
+    def __call__(self, argv, timeout):
+        tail = list(argv[1:])
+        for token in CONSUMING_TOKENS:
+            assert token not in tail, f"{token} reached the backend: {tail}"
+        if tail[:5] != QUESTION_BASE:
+            assert tail[:3] == ["orchestration", "worker-list", "--json"], tail
+            assert "check" not in tail  # plain check would consume a delivery
+            return 0, json.dumps(make_envelope(make_rows(2, 1), total=2))
+        assert tail[5:] == ["--run", QRUN, "--json"], tail
+        self.reads += 1
+        if self.consuming:  # the behaviour the test must be able to detect
+            self.delivery = f"delivery_{self.reads}"
+            for row in self.rows:
+                row["delivered_at"] = "2026-11-11T20:01:30Z"
+        envelope = {
+            "id": f"env-{next(self._envelope_ids)}",  # differs per call, like the real one
+            "ok": True,
+            "result": {
+                "acknowledged": None,
+                "count": len(self.rows),
+                "messages": copy.deepcopy(self.rows),
+                "runId": QRUN,
+            },
+            "_meta": {"runtimeId": "redacted"},
+        }
+        return 0, json.dumps(envelope)
+
+    def send(self, rows):
+        """A sender writes new questions (the scope stops being quiet)."""
+        self.rows = [*rows, *self.rows]
+
+
+def observer_over(backend, clock):
+    runner = FakeRunner([], [backend])
+    return Collector(
+        LiveSource(runner, FakeDiscover([])), clock, run_id=QRUN, questions=True
+    )
+
+
+def observe_quiet_scope(backend, cycles=5):
+    """Step one establishes identity; then repeated reads on a quiet scope are compared."""
+    clock = FakeClock()
+    collector = observer_over(backend, clock)
+    first = collector.run_once()
+    # Step one: readable identity fields exist before any comparison is made.
+    assert first.question_state == "OK" and first.questions.retained > 0
+    for row in backend.rows:
+        assert row["id"].startswith("msg_") and row["run_id"] == QRUN
+        assert isinstance(row["created_at"], str) and row["created_at"]
+    for record in first.questions.records:
+        assert record.question.qid.startswith("msg_") and record.key[0] == QRUN
+        assert isinstance(record.question.created_epoch, float)  # a created time
+    baseline = [r.question.qid for r in first.questions.records]
+    before = backend.fingerprint()
+    seen = []
+    for _ in range(cycles):
+        clock.advance(15.0)
+        result = collector.run_once()
+        assert result.question_state == "OK"
+        seen.append([r.question.qid for r in result.questions.records])
+        assert backend.fingerprint() == before, "the read changed the mailbox state"
+    assert all(ids == baseline for ids in seen), "ids or order changed on a quiet scope"
+    return baseline
+
+
+def probe_rows(n=6):
+    return make_question_rows(n)  # synthetic rows with the recorded key names
+
+
+def test_t51_repeated_reads_on_a_quiet_scope_leave_ids_order_and_mailbox_unchanged():
+    backend = FakeOrcaMailbox(probe_rows(6))
+    ids = observe_quiet_scope(backend, cycles=5)
+    assert len(ids) == 6 and ids == sorted(ids)  # oldest created first, stable
+    assert (
+        backend.reads == 6 and backend.delivery is None and backend.acknowledged == []
+    )
+    assert all(row["delivered_at"] is None for row in backend.rows)
+    assert PASS_SCOPE.startswith("a pass covers only the visible effects tested")
+
+
+def test_t51_the_observer_never_sends_a_consuming_or_narrowing_argv():
+    backend = FakeOrcaMailbox(probe_rows(3))
+    log = []
+
+    def spy(argv, timeout):
+        log.append(list(argv))
+        return backend(argv, timeout)
+
+    clock = FakeClock()
+    collector = Collector(
+        LiveSource(FakeRunner([], [spy]), FakeDiscover([])),
+        clock,
+        run_id=QRUN,
+        questions=True,
+    )
+    for _ in range(3):
+        collector.run_once()
+        clock.advance(15.0)
+    messages = [a for a in log if "check" in a]
+    assert len(messages) == 3 and all(a[1:6] == QUESTION_BASE for a in messages)
+    for argv in log:
+        for token in CONSUMING_TOKENS:
+            assert token not in argv
+    assert all(a.count("check") == 1 and "--all" in a for a in messages)
+
+
+def test_t51_a_consuming_fake_makes_the_same_check_fail_so_the_test_can_detect_it():
+    backend = FakeOrcaMailbox(probe_rows(4))
+    backend.consuming = True
+    with pytest.raises(AssertionError, match="changed the mailbox state"):
+        observe_quiet_scope(backend, cycles=3)
+    assert backend.delivery is not None  # the fake really did consume
+
+
+def test_t51_the_check_is_sensitive_to_a_new_question_so_quiet_means_no_sender_write():
+    backend = FakeOrcaMailbox(probe_rows(3))
+    clock = FakeClock()
+    collector = observer_over(backend, clock)
+    before = [r.question.qid for r in collector.run_once().questions.records]
+    backend.send(make_question_rows(1, start=10))  # a sender writes: not a quiet scope
+    after = [r.question.qid for r in collector.run_once().questions.records]
+    assert after != before and set(before) < set(after)
+
+
+def test_t51_the_backend_refuses_every_consuming_argv_it_could_be_given():
+    backend = FakeOrcaMailbox(probe_rows(1))
+    bad = [
+        ["/o", "orchestration", "check", "--json"],
+        ["/o", "orchestration", "check", "--all", "--ack", "d1"],
+        ["/o", "orchestration", "check", "--all", "--wait"],
+        ["/o", "orchestration", "check", "--peek", "--types", "question"],
+    ]
+    for argv in bad:
+        with pytest.raises(AssertionError):
+            backend(argv, 1.0)
+    assert backend.reads == 0 and backend.delivery is None


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
