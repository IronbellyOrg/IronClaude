d172849bf407ec62836f7c8de0f9a0829bd27faf
Review one task for spec compliance.

Task brief: ## Task 9: Fix the vacuous render assertion and remove two duplicated test blocks (T8, T5, T7)

Edit `tests/observe/test_render.py` (T8): replace the assertion at :95-100 that ends in `or True` with `assert len(overflow) == 1`; keep all 27 cases of the test. If the corrected assertion fails, report that as a finding and do not loosen it. Edit `tests/observe/test_question_quiet_scope.py` (T5): delete only `test_t51_the_backend_refuses_every_consuming_argv_it_could_be_given` (:192-203, the test of the fake mailbox itself); keep :137-145, :148-171, :174-179 and :182-189 and the fake's own argv assertions. Edit `tests/observe/test_golden_contract.py` (T7): in the two golden leak scans delete only the duplicated `for what, pattern in SENSITIVE.items(): assert not pattern.search(...)` pairs (:214-215 and :518-519); keep the `isascii` checks (:213, :517), the 32-character rule (:216), the run, terminal and message id rule (:520) and :521-527; remove the `SENSITIVE` import there only if it becomes unused. The surviving guard for the removed scans is `tests/observe/test_fixtures.py:185-191`, which runs the same patterns over every packaged fixture.

Acceptance criteria:
- `tests/observe/test_render.py` has no `or True`; the test passes with all 27 parametrized cases.
- `test_t51_the_backend_refuses_every_consuming_argv_it_could_be_given` no longer exists; the other tests in `tests/observe/test_question_quiet_scope.py` pass; `tests/observe/test_adapter.py:158-192` still holds the forbidden-prefix tests.
- `tests/observe/test_golden_contract.py` still contains the 32-character rule and the id rule and passes; `tests/observe/test_fixtures.py:185-191` passes.
- The task states one deleted test function (T5) and the gate passes with the passed count reduced by exactly 1.
Global constraints: 
- Shorthand. PKG is `src/superclaude/cli/observe/`. TESTS is `tests/observe/`. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`. The debate's final list and its row text are copied into `./source.md`; each task below restates what it needs.
- Scope is these eleven rows only. No commit, no push, no pull request. Every other row of the debate (KEEP, owner decisions, low confidence) is out of scope.
- Never touch: the sanitizer (`PKG/sanitize.py` and its use), the argv allow-list and forbidden verbs in `PKG/adapter.py`, process-group kill and output caps, terminal restore on exit and signals, the rule that message bodies, payload and `to_handle` are never kept, snapshot redaction, the disclosure label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`, `QUESTION_GATE_TEXT` in `PKG/commands.py` (pinned by `TESTS/test_commands.py`), any DIRECTION-SELECTED line, and any file git does not track (for example `.dev/issues/409/handoff-mvp-brainstorm.md`).
- Line numbers in the tasks were read live on 2026-11-16 at HEAD f104ca51a and are leads only: re-grep every target right before editing, because other sessions share the worktree.
- Gate for every task: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q` passes and `uv run ruff check src/superclaude/cli/observe tests/observe` is clean. The baseline is 694 passed; the passed count falls only by the test functions a task deliberately deletes, and the task states the number it expects and the number it got. UV only; never bare python or pip. A failing gate is reported as a finding and never loosened to pass.
- Edits touch only `src/`, `tests/`, `.dev/issues/409/` and this package's `./artifacts/`; nothing under `.claude/`.
- Whole-package checks, applied by the final review and not tasks of their own: Task 1 first saves `git status --short` to `./artifacts/baseline-status.txt`; at the end `git status --short` differs from that baseline only by the files these tasks name, `.dev/issues/409/` and this package; the full gate passes with the passed count equal to 694 minus the test cases the tasks removed (9 in Task 1 and 1 in Task 9, so 684, unless Task 6 had to remove an aggregate-only test); and `grep -rn "run-use" src/superclaude/cli/observe/` shows `run-use` only in the forbidden set in `PKG/adapter.py` and in the help text that says the observer never runs it.
- Names, not line numbers, wherever a check or a document points at code, because earlier tasks shift line numbers (for example `_question_refusal` in `PKG/commands.py`). A Grep check below means uses of the named symbol, not test function names that merely contain the word (`tests/observe/test_questions.py:50` and `tests/observe/test_view.py:174` keep such names).
- Labels. T5, T7, T8 and T9 in task titles are the debate's row names; the spec test ids in Task 12 are written "spec test T7", "T17", "T45" and "T50".
- Facts the debate found false in the earlier proposal, not to be repeated: the R1 test ranges were too wide, R3 must not drop the five parsed row fields, T9 keeps the `test_render.py` copy and deletes the `test_terminal.py` copy, T7 keeps the 32-character rule and the id rule, T8 keeps all 27 cases, D1 touches owner decisions 6 and 8 only.
Start sha: d172849bf407ec62836f7c8de0f9a0829bd27faf
Diff against the start snapshot: diff --git a/tests/observe/test_golden_contract.py b/tests/observe/test_golden_contract.py
index eb6fc4011..71fd02479 100644
--- a/tests/observe/test_golden_contract.py
+++ b/tests/observe/test_golden_contract.py
@@ -20,3 +20,2 @@ from tests.observe import record_golden
 from tests.observe.conftest import FakeDiscover, FakeRunner
-from tests.observe.test_fixtures import SENSITIVE
 
@@ -213,4 +212,2 @@ def test_golden_files_hold_no_path_handle_token_credential_url_or_escape_byte(na
     assert "\x1b" not in text and text.isascii()
-    for what, pattern in SENSITIVE.items():
-        assert not pattern.search(text), f"{name}: {what}"
     assert not re.search(r"[A-Za-z0-9_+=-]{32,}", text.replace("redacted", ""))
@@ -517,4 +514,2 @@ def test_question_golden_files_hold_no_path_handle_token_credential_url_or_escap
     assert "\x1b" not in text and text.isascii()
-    for what, pattern in SENSITIVE.items():
-        assert not pattern.search(text), f"{name}: {what}"
     assert not re.search(r"run_[0-9a-f]{12}|term_|msg_[0-9a-f]*[a-f][0-9a-f]*\b", text)
diff --git a/tests/observe/test_question_quiet_scope.py b/tests/observe/test_question_quiet_scope.py
index 60d1cbacc..881f6fde6 100644
--- a/tests/observe/test_question_quiet_scope.py
+++ b/tests/observe/test_question_quiet_scope.py
@@ -189,15 +189 @@ def test_t51_the_check_is_sensitive_to_a_new_question_so_quiet_means_no_sender_w
     assert after != before and set(before) < set(after)
-
-
-def test_t51_the_backend_refuses_every_consuming_argv_it_could_be_given():
-    backend = FakeOrcaMailbox(probe_rows(1))
-    bad = [
-        ["/o", "orchestration", "check", "--json"],
-        ["/o", "orchestration", "check", "--all", "--ack", "d1"],
-        ["/o", "orchestration", "check", "--all", "--wait"],
-        ["/o", "orchestration", "check", "--peek", "--types", "question"],
-    ]
-    for argv in bad:
-        with pytest.raises(AssertionError):
-            backend(argv, 1.0)
-    assert backend.reads == 0 and backend.delivery is None
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index 8f4f6319d..e3101a520 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -94,8 +94,3 @@ def test_matrix_lines_fit_counts_are_k_of_n_and_overflow_names_the_total(
     overflow = [l for l in lines if re.match(r"^\d+/\d+ shown", l)]
-    assert (
-        len(overflow) == 1
-        and overflow[0].startswith(f"{len(view.window(30).rows) if False else ''}")
-        is True
-        or True
-    )
+    assert len(overflow) == 1
     x, y = map(int, re.match(r"^(\d+)/(\d+) shown", overflow[0]).groups())
Evidence this task produced (machine output of the gate, file /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/artifacts/t9-gate.log):
== grep (each pattern expected to match nothing)
none: or True
none: test_t51_the_backend_refuses_every_consuming_argv
== pytest
.                                                                        [100%]

============================= 684 passed in 23.01s =============================
== ruff
All checks passed!
== matrix cases kept (expect 27)

=============== 27/104 tests collected (77 deselected) in 0.15s ================
== SENSITIVE uses
tests/observe/test_fixtures.py:180:SENSITIVE = {
tests/observe/test_fixtures.py:198:    for what, pattern in SENSITIVE.items():
== kept rules in test_golden_contract.py
212:    assert "\x1b" not in text and text.isascii()
213:    assert not re.search(r"[A-Za-z0-9_+=-]{32,}", text.replace("redacted", ""))
514:    assert "\x1b" not in text and text.isascii()
515:    assert not re.search(r"run_[0-9a-f]{12}|term_|msg_[0-9a-f]*[a-f][0-9a-f]*\b", text)
== T5 test list in quiet-scope file
137:def test_t51_repeated_reads_on_a_quiet_scope_leave_ids_order_and_mailbox_unchanged():
148:def test_t51_the_observer_never_sends_a_consuming_or_narrowing_argv():
174:def test_t51_a_consuming_fake_makes_the_same_check_fail_so_the_test_can_detect_it():
182:def test_t51_the_check_is_sensitive_to_a_new_question_so_quiet_means_no_sender_write():
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

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
