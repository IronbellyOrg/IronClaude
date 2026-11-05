0f943f95513cccc1cfecdec3ab83ab61091ddc50
Review one task for spec compliance.

Task brief: ## Task 8: Add per-reviewer wait outcomes and the merge truth table

Depends on: Task 6

Add to src/superclaude/pr_submit/reviewers.py per design section 6: `augment_wait_outcome(state, next_state)` (pending / done / absent / incomplete from the existing gate state and `poll_outcome` result), `codex_wait_outcome(state, *, active, elapsed, timeout, silence_timeout, other_settled)` and `merge_wait(augment, codex)` returning `{"outcome", "used", "absent", "incomplete"}` with outcome in polling / clean / findings / declined / no_response / timeout, exactly per the design's merge table rows.

Acceptance criteria:
- Every row of the design section 6 merge table has a matching assertion (Augment only, Codex only, both done, neither present, pending on either side, incomplete combinations, Augment declined).
- An inactive Codex is `absent` as soon as Augment is settled, and before that only at the silence deadline.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 0f943f95513cccc1cfecdec3ab83ab61091ddc50
Diff against the start snapshot: --- a/src/superclaude/pr_submit/reviewers.py
+++ b/src/superclaude/pr_submit/reviewers.py
@@ -19,6 +19,7 @@
 from .classifier import (
     _COMPLETENESS,
     STATE_CLEAN,
+    STATE_DECLINED,
     STATE_FINDINGS,
     STATE_POLLING,
     _augment_entries,
@@ -311,3 +312,94 @@
             }
         )
     return rows
+
+
+# --- per-reviewer wait outcomes and the merge (design section 6 + section 18 A2) ---
+
+WAIT_PENDING = "pending"
+WAIT_DONE = "done"
+WAIT_ABSENT = "absent"
+WAIT_INCOMPLETE = "incomplete"
+_DONE_STATES = (STATE_CLEAN, STATE_FINDINGS, STATE_DECLINED)
+
+
+def _state_name(value: Any) -> str:
+    return str(getattr(value, "value", value))
+
+
+def augment_wait_outcome(state: str, next_state: Any, *, absent: bool = False) -> str:
+    """Augment's wait outcome from the existing gate state and ``poll_outcome`` result.
+
+    ``absent`` (already recorded absent, or no Augment identity) is ``absent`` at
+    once and is never ``pending`` (A2).
+    """
+    if absent:
+        return WAIT_ABSENT
+    if state in _DONE_STATES:
+        return WAIT_DONE
+    nxt = _state_name(next_state)
+    if nxt == "TERMINAL_AUGMENT_NO_RESPONSE":
+        return WAIT_ABSENT
+    if nxt == "TERMINAL_TIMEOUT":
+        return WAIT_INCOMPLETE
+    return WAIT_PENDING
+
+
+def codex_wait_outcome(
+    state: str,
+    *,
+    active: bool,
+    elapsed: int,
+    timeout: int,
+    silence_timeout: int,
+    other_settled: bool,
+    absent: bool = False,
+) -> str:
+    """Codex's wait outcome.
+
+    ``absent`` (already recorded absent, or no Codex identity) is ``absent`` at once
+    (A2). A Codex with no activity is absent as soon as Augment is settled or at the
+    silence deadline; an active Codex with no completion is ``incomplete`` at
+    ``--timeout``.
+    """
+    if absent:
+        return WAIT_ABSENT
+    if state in (STATE_CLEAN, STATE_FINDINGS):
+        return WAIT_DONE
+    if active:
+        return WAIT_INCOMPLETE if elapsed >= timeout else WAIT_PENDING
+    if other_settled or elapsed >= min(silence_timeout, timeout):
+        return WAIT_ABSENT
+    return WAIT_PENDING
+
+
+def merge_wait(augment: tuple[str, str], codex: tuple[str, str]) -> dict:
+    """Merge per-reviewer ``(wait_outcome, gate_state)`` pairs into one round outcome.
+
+    ``outcome`` is ``polling`` / ``clean`` / ``findings`` / ``declined`` /
+    ``no_response`` / ``timeout``; ``used`` names the reviewers whose results the
+    outcome uses, ``absent`` / ``incomplete`` the others (design section 6 table).
+    """
+    pairs = {"augment": augment, "codex": codex}
+    absent = [name for name, (out, _) in pairs.items() if out == WAIT_ABSENT]
+    incomplete = [name for name, (out, _) in pairs.items() if out == WAIT_INCOMPLETE]
+    done = [(name, st) for name, (out, st) in pairs.items() if out == WAIT_DONE]
+    result = {
+        "outcome": STATE_POLLING,
+        "used": [],
+        "absent": absent,
+        "incomplete": incomplete,
+    }
+    if any(out == WAIT_PENDING for out, _ in pairs.values()):
+        return result
+    result["used"] = [name for name, _ in done]
+    if augment == (WAIT_DONE, STATE_DECLINED):
+        result["outcome"] = STATE_DECLINED
+    elif done:
+        findings = any(st == STATE_FINDINGS for _, st in done)
+        result["outcome"] = STATE_FINDINGS if findings else STATE_CLEAN
+    elif len(absent) == len(pairs):
+        result["outcome"] = "no_response"
+    else:
+        result["outcome"] = "timeout"
+    return result
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t8-check.py b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t8-check.py
new file mode 100644
index 00000000..01dc93ec
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t8-check.py
@@ -0,0 +1,61 @@
+"""T8 check: every row of the design section 6 tables, plus amendment A2."""
+import sys
+
+from superclaude.pr_submit.models import MonitorState as M
+from superclaude.pr_submit.reviewers import augment_wait_outcome, codex_wait_outcome, merge_wait
+
+ok = []
+
+
+def check(name, got, want):
+    ok.append(got == want)
+    print(f"{'PASS' if got == want else 'FAIL'} {name}: got={got!r} want={want!r}")
+
+
+# augment wait outcome (left column of the wait table)
+check("augment polling + S2_CLASSIFY -> pending", augment_wait_outcome("polling", M.S2_CLASSIFY), "pending")
+check("augment polling + S5C_SILENCE_REREQUEST -> pending", augment_wait_outcome("polling", M.S5C_SILENCE_REREQUEST), "pending")
+for st in ("clean", "findings", "declined"):
+    check(f"augment {st} -> done", augment_wait_outcome(st, M.S2_CLASSIFY), "done")
+check("augment TERMINAL_AUGMENT_NO_RESPONSE -> absent", augment_wait_outcome("polling", M.TERMINAL_AUGMENT_NO_RESPONSE), "absent")
+check("augment already absent (A2) -> absent", augment_wait_outcome("polling", M.S2_CLASSIFY, absent=True), "absent")
+check("augment TERMINAL_TIMEOUT -> incomplete", augment_wait_outcome("polling", M.TERMINAL_TIMEOUT), "incomplete")
+
+# codex wait outcome (right column)
+kw = dict(elapsed=60, timeout=600, silence_timeout=300)
+check("codex clean -> done", codex_wait_outcome("clean", active=True, other_settled=False, **kw), "done")
+check("codex findings -> done", codex_wait_outcome("findings", active=True, other_settled=False, **kw), "done")
+check("codex active, not timed out -> pending", codex_wait_outcome("polling", active=True, other_settled=False, **kw), "pending")
+check("codex active at timeout -> incomplete", codex_wait_outcome("polling", active=True, other_settled=False, elapsed=600, timeout=600, silence_timeout=300), "incomplete")
+check("codex inactive, before deadline, Augment pending -> pending", codex_wait_outcome("polling", active=False, other_settled=False, **kw), "pending")
+check("codex inactive, Augment settled -> absent at once", codex_wait_outcome("polling", active=False, other_settled=True, **kw), "absent")
+check("codex inactive at silence deadline -> absent", codex_wait_outcome("polling", active=False, other_settled=False, elapsed=300, timeout=600, silence_timeout=300), "absent")
+check("codex already absent (A2) -> absent even if active", codex_wait_outcome("polling", active=True, other_settled=False, absent=True, **kw), "absent")
+
+
+def out(a, c):
+    return merge_wait(a, c)["outcome"]
+
+
+P, D, AB, IN = "pending", "done", "absent", "incomplete"
+check("pending | any -> polling", out((P, "polling"), (D, "clean")), "polling")
+check("any | pending -> polling", out((D, "clean"), (P, "polling")), "polling")
+check("declined | settled -> declined", out((D, "declined"), (D, "findings")), "declined")
+check("declined | absent -> declined", out((D, "declined"), (AB, "polling")), "declined")
+check("done | done (findings) -> findings", out((D, "clean"), (D, "findings")), "findings")
+check("done | done (both clean) -> clean", out((D, "clean"), (D, "clean")), "clean")
+check("done | absent -> Augment's state (Augment only)", out((D, "findings"), (AB, "polling")), "findings")
+r = merge_wait((D, "clean"), (IN, "polling"))
+check("done | incomplete -> Augment's state, Codex reported incomplete", (r["outcome"], r["used"], r["incomplete"]), ("clean", ["augment"], ["codex"]))
+r = merge_wait((AB, "polling"), (D, "findings"))
+check("absent | done -> Codex's state (Codex only)", (r["outcome"], r["used"], r["absent"]), ("findings", ["codex"], ["augment"]))
+check("incomplete | done -> Codex's state", out((IN, "polling"), (D, "clean")), "clean")
+check("absent | absent (neither) -> no_response", out((AB, "polling"), (AB, "polling")), "no_response")
+check("incomplete | absent -> timeout", out((IN, "polling"), (AB, "polling")), "timeout")
+check("incomplete | incomplete -> timeout", out((IN, "polling"), (IN, "polling")), "timeout")
+check("absent | incomplete -> timeout", out((AB, "polling"), (IN, "polling")), "timeout")
+# A2: Augment's silence outcome with Codex present continues with Codex instead of ending the run
+a = augment_wait_outcome("polling", M.TERMINAL_AUGMENT_NO_RESPONSE)
+c = codex_wait_outcome("findings", active=True, other_settled=True, **kw)
+check("A2: Augment silent + Codex done -> continues with Codex findings", out((a, "polling"), (c, "findings")), "findings")
+sys.exit(0 if all(ok) else 1)
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t8-check.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t8-check.log
new file mode 100644
index 00000000..648f4b98
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t8-check.log
@@ -0,0 +1,32 @@
+PASS augment polling + S2_CLASSIFY -> pending: got='pending' want='pending'
+PASS augment polling + S5C_SILENCE_REREQUEST -> pending: got='pending' want='pending'
+PASS augment clean -> done: got='done' want='done'
+PASS augment findings -> done: got='done' want='done'
+PASS augment declined -> done: got='done' want='done'
+PASS augment TERMINAL_AUGMENT_NO_RESPONSE -> absent: got='absent' want='absent'
+PASS augment already absent (A2) -> absent: got='absent' want='absent'
+PASS augment TERMINAL_TIMEOUT -> incomplete: got='incomplete' want='incomplete'
+PASS codex clean -> done: got='done' want='done'
+PASS codex findings -> done: got='done' want='done'
+PASS codex active, not timed out -> pending: got='pending' want='pending'
+PASS codex active at timeout -> incomplete: got='incomplete' want='incomplete'
+PASS codex inactive, before deadline, Augment pending -> pending: got='pending' want='pending'
+PASS codex inactive, Augment settled -> absent at once: got='absent' want='absent'
+PASS codex inactive at silence deadline -> absent: got='absent' want='absent'
+PASS codex already absent (A2) -> absent even if active: got='absent' want='absent'
+PASS pending | any -> polling: got='polling' want='polling'
+PASS any | pending -> polling: got='polling' want='polling'
+PASS declined | settled -> declined: got='declined' want='declined'
+PASS declined | absent -> declined: got='declined' want='declined'
+PASS done | done (findings) -> findings: got='findings' want='findings'
+PASS done | done (both clean) -> clean: got='clean' want='clean'
+PASS done | absent -> Augment's state (Augment only): got='findings' want='findings'
+PASS done | incomplete -> Augment's state, Codex reported incomplete: got=('clean', ['augment'], ['codex']) want=('clean', ['augment'], ['codex'])
+PASS absent | done -> Codex's state (Codex only): got=('findings', ['codex'], ['augment']) want=('findings', ['codex'], ['augment'])
+PASS incomplete | done -> Codex's state: got='clean' want='clean'
+PASS absent | absent (neither) -> no_response: got='no_response' want='no_response'
+PASS incomplete | absent -> timeout: got='timeout' want='timeout'
+PASS incomplete | incomplete -> timeout: got='timeout' want='timeout'
+PASS absent | incomplete -> timeout: got='timeout' want='timeout'
+PASS A2: Augment silent + Codex done -> continues with Codex findings: got='findings' want='findings'
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t8-test.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t8-test.log
new file mode 100644
index 00000000..f85ece51
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t8-test.log
@@ -0,0 +1,54 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 4.3.5
+benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex
+configfile: pyproject.toml
+plugins: superclaude-4.3.5, benchmark-5.3.0, anyio-4.15.1, cov-7.1.0
+collected 647 items
+
+tests/pr_submit/test_auggie_fallback.py ............                     [  1%]
+tests/pr_submit/test_augment_review_remediation.py .......               [  2%]
+tests/pr_submit/test_autonomy_gates.py .......                           [  4%]
+tests/pr_submit/test_ci_classify.py ....................                 [  7%]
+tests/pr_submit/test_contract_setup_diagnosis.py ..............          [  9%]
+tests/pr_submit/test_contract_setup_evidence.py .....................    [ 12%]
+tests/pr_submit/test_contract_setup_pr_submit_integration.py ......      [ 13%]
+tests/pr_submit/test_contract_setup_questions.py .........               [ 14%]
+tests/pr_submit/test_contract_setup_validation.py .............          [ 16%]
+tests/pr_submit/test_contract_setup_writer.py ................           [ 19%]
+tests/pr_submit/test_cosmos_poll.py .................................... [ 24%]
+...............................................................          [ 34%]
+tests/pr_submit/test_cosmos_protocol.py ...............                  [ 36%]
+tests/pr_submit/test_cosmos_review.py .................................. [ 42%]
+........................................................................ [ 53%]
+                                                                         [ 53%]
+tests/pr_submit/test_crash_recovery.py ................                  [ 55%]
+tests/pr_submit/test_detection_contract.py ............................. [ 60%]
+.....                                                                    [ 61%]
+tests/pr_submit/test_edge_cases.py ...................                   [ 63%]
+tests/pr_submit/test_finding_verify.py ...                               [ 64%]
+tests/pr_submit/test_gate_helper_coverage.py ...........                 [ 66%]
+tests/pr_submit/test_gate_helper_differentials.py ...................... [ 69%]
+                                                                         [ 69%]
+tests/pr_submit/test_idempotency.py ......                               [ 70%]
+tests/pr_submit/test_loop_guard.py .............                         [ 72%]
+tests/pr_submit/test_monitor_arm.py ...                                  [ 72%]
+tests/pr_submit/test_pre_pr_checks.py .................................. [ 78%]
+.....                                                                    [ 78%]
+tests/pr_submit/test_rate_limit.py ....                                  [ 79%]
+tests/pr_submit/test_reply_resolve.py ..........                         [ 81%]
+tests/pr_submit/test_review_retrigger.py .......                         [ 82%]
+tests/pr_submit/test_run_log.py ............                             [ 84%]
+tests/pr_submit/test_setup_questions_resolution.py ....                  [ 84%]
+tests/pr_submit/test_severity_router.py ............................     [ 89%]
+tests/pr_submit/test_silence.py .................                        [ 91%]
+tests/pr_submit/test_skill_parse.py ..............                       [ 93%]
+tests/pr_submit/test_static_grep.py ...................                  [ 96%]
+tests/pr_submit/test_timeout.py .....                                    [ 97%]
+tests/pr_submit/test_troubleshoot_seed.py ....                           [ 98%]
+tests/pr_submit/test_validated_not_verified.py ...                       [ 98%]
+tests/pr_submit/test_validation_gate.py .........                        [100%]
+
+============================= 647 passed in 14.40s =============================
+rc=0
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
