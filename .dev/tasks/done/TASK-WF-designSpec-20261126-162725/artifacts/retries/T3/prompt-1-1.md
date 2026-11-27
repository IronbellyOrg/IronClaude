cc69d8f129da749dc7a61ba1672ecb956b08d304
Review one task for spec compliance.

Task brief: ## Task 3: Build the pure scoring functions

Depends on: Task 2

Create `.dev/research/jev-vs-keyword-table-611/harness/scorer.py` (first part) and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py`. Functions, all pure and stdlib only:
- `right(label, answer) -> bool`; answer `None` means unset.
- `sign_test_passes(b, c) -> bool` using `math.comb` and the integer test `20 * tail < 2 ** n` with `n = b + c` and `tail = sum(comb(n, k) for k in range(b, n + 1))`, reading the factor 20 from the rule's `alpha_inverse`.
- `jev_answer(noul_p, choice, rule) -> (answer, reason)`. Here `noul_p` is the Noul value for `any_type_fits` (a high value means a type fits) and `choice` is the validated answer of `problem_type`. If `noul_p` is below the low edge by the low operator (`lt` means strictly below `noul_low`, `le` means at or below), the answer is `None` with reason `none-fit`. Else if `noul_p` is above the high edge by the high operator (`gt` strictly above `noul_high`, `ge` at or above), the answer is `choice`. Otherwise the answer is `None` with reason `not-settled`. It refuses when an operator is `UNSET` or not valid for its edge.
- `median(values)` (even count: mean of the two middle values; empty list: `None`), `percentile_nearest_rank(values, 0.9)` (index `ceil(0.9 * n) - 1` of the sorted list; empty list: `None`) and `latency_stats(attempts, rule)` returning the median over the population `median_population` says, the slowest over all attempts with a timeout counted at `attempt_timeout_s`, and the 90th percentile; each is `None` when no attempt qualifies.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py -v` passes.
- A test asserts `sign_test_passes` is True for 5-0, 7-1 and 9-2 and False for 4-0, 6-1, 8-2 and (0, 0), and asserts the smallest passing b for each c from 0 to 6 is 5, 7, 9, 10, 12, 13 and 15, and agrees with a reference loop for every b and c up to 30 (requirement T-12 and T-15).
- Tests give `jev_answer` these expected values for the four operator pairs (`lt` or `le` with `gt` or `ge`): a value just below 0.3 gives `none-fit`; exactly 0.3 gives `none-fit` under `le` and `not-settled` under `lt`; a value between the edges gives `not-settled`; exactly 0.7 gives the choice under `ge` and `not-settled` under `gt`; a value just above 0.7 gives the choice. A test shows the refusal for an `UNSET` operator and for `gt` on the low edge (T-05).
- Tests cover `right` for a typed label, an `ambiguous` label and a `none-fit` label with an unset answer (T-07), odd and even median counts, the nearest-rank 90th percentile, a timeout counted at 10 seconds in the slowest and left out of the median under `answered_only` (T-08), and `None` results for empty input.
- `scorer.py` contains no floating-point comparison at the 0.05 line.

Acceptance criterion ids (in source order):
T3.AC1: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py -v` passes.
T3.AC2: A test asserts `sign_test_passes` is True for 5-0, 7-1 and 9-2 and False for 4-0, 6-1, 8-2 and (0, 0), and asserts the smallest passing b for each c from 0 to 6 is 5, 7, 9, 10, 12, 13 and 15, and agrees with a reference loop for every b and c up to 30 (requirement T-12 and T-15).
T3.AC3: Tests give `jev_answer` these expected values for the four operator pairs (`lt` or `le` with `gt` or `ge`): a value just below 0.3 gives `none-fit`; exactly 0.3 gives `none-fit` under `le` and `not-settled` under `lt`; a value between the edges gives `not-settled`; exactly 0.7 gives the choice under `ge` and `not-settled` under `gt`; a value just above 0.7 gives the choice. A test shows the refusal for an `UNSET` operator and for `gt` on the low edge (T-05).
T3.AC4: Tests cover `right` for a typed label, an `ambiguous` label and a `none-fit` label with an unset answer (T-07), odd and even median counts, the nearest-rank 90th percentile, a timeout counted at 10 seconds in the slowest and left out of the median under `answered_only` (T-08), and `None` results for empty input.
T3.AC5: `scorer.py` contains no floating-point comparison at the 0.05 line.
Global constraints: ## Constraints

- Scope is build and test only. No task sends a prompt to TypeSafe, reads `TYPESAFE_API_KEY` or `JEV_API_KEY` from the real environment, or opens a network connection. Tests use `MockTransport` and a socket guard, set a fake key with `monkeypatch.setenv`, and use a temporary experiment root for every file the gates, events, runner and scorer write. The live run is a coordinator action under rule J2 of `.dev/research/346-review-loop-experiments/p15/plans/SHARED-CONTRACT.md` (lines 145 to 165).
- Left for a person or the coordinator, not in this plan: choosing and labelling about 30 public prompts (a named human labeller is required), applying the keyword table to them (a session or person who sees prompts only, after Gate 1), the live run with `keyscan.py`, scoring and the report, and the updates on issues 611, 609 and 612. Tasks 7 and 8 produce the procedures, templates and instructions those steps need. The pull request that delivers this plan says `Refs #611` and lists parts B to E of section 8 of the design as left (Task 8 puts that sentence in the README).
- Nothing under `src/`, `tests/`, `.claude/` or the existing `.dev/research/346-review-loop-experiments/p15/jev/jevlib/` folder is changed. `jevlib` is imported read-only, and only from its submodules (`client`, `budget`, `journal`, `transport`, `questions`, `manifest`, `config`), because `jevlib/__init__.py` exports only `MODEL`, `API_URL` and `KEY_ENV`.
- Spend cap is 1 dollar in total; public prompts only; the key is never printed, logged, written to a file, put on a command line or put in a pull request. The runner copies `TYPESAFE_API_KEY` into `JEV_API_KEY` inside its own process only, because `jevlib.config.KEY_ENV` is `JEV_API_KEY`.
- Agreed decision rule (AGREED 2026-11-26 by the IronFlow session and the build agent, relayed by the lead; Clay's own words as quoted by the IronFlow session, not typed by Clay: "you and the agent debate whats correct way to handle this and do it").
- Margin: an exact one-sided sign test on the prompts where only one arm is right. b is the count right only for Jev; c is the count right only for the table. Jev passes when 20 times the sum of comb(b+c, k) for k from b to b+c is below 2 to the power b+c, in integer arithmetic. Checked cases: 5-0 passes, 4-0 fails, 7-1 passes, 6-1 fails, 8-2 fails (56/1024 is 0.0547), 9-2 passes, and b+c of 0 is not clearly.
- Right: a typed label is right when the answer is that type; an `ambiguous` or `none-fit` label is right when the answer is unset. Same for both arms. An unset answer on a typed label is not right.
- Latency: measured on the client from sending the request to receiving the full response, per attempt. The median over each prompt's final answered attempt must be 2 seconds or less. The slowest over all attempts, with a timeout counted at its timeout value, must be 5 seconds or less. Per-call timeout is 10 seconds. The 90th percentile by nearest rank is reported.
- Failures: one rerun per failed prompt, never a rerun of the whole run. Both attempts are logged and counted against the cap. A prompt that fails twice is an `error`, is not right for Jev, and is never scored as a "no".
- Verdict: `JEV_BEATS_TABLE` only when the run is valid, the margin test passes and both latency limits hold. `NOT_CLEARLY` for a valid run that does not. `RUN_INVALID` with a reason otherwise. `RUN_INVALID` makes no build or close decision on issue 612.
- Still open, so written as `UNSET` in the rule file: the operators at exactly 0.3 and 0.7 for the Noul band, and the count of unresolved failures that makes a run invalid. Gate 1 accepts `UNSET` and does not freeze the rule file's hash. The scorer, the `freeze-rule` command and Gate 2 refuse any `UNSET` value, and `freeze-rule` is the step that freezes the rule file's hash after the owner has filled the fields.
- The real client behaves differently from a mock-backed dry run: `JevClient` with `live=False` builds, screens and budgets the request, then returns `refused` with error `dry_run` before any transport call. So the runner has two subcommands: `run` needs `--live`, both gates and the key; `rehearse` never posts and needs no gate and no key. Tests that need the transport path use `live=True`, an injected `MockTransport` and a fake `JEV_API_KEY`.
- Test run command, recorded by `gate.py record-tests`: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v`. The repository's `testpaths` is `tests`, so tests under `.dev/` are only collected when this path is given.
- Each of the four command-line modules (`gate.py`, `events.py`, `runner.py` and `scorer.py`) inserts the existing `jevlib` folder and the experiment folder into `sys.path` itself, as `.dev/research/346-review-loop-experiments/p15/jev/probe.py` does (read-only reference), because only `conftest.py` does so for tests (finding M-12).
Start sha: cc69d8f129da749dc7a61ba1672ecb956b08d304
Diff against the start snapshot: diff --git a/.dev/research/jev-vs-keyword-table-611/harness/scorer.py b/.dev/research/jev-vs-keyword-table-611/harness/scorer.py
new file mode 100644
index 000000000..d03fd9b60
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/scorer.py
@@ -0,0 +1,94 @@
+"""Scorer, part 1: the pure functions of the decision rule.
+
+Stdlib only.  Nothing here reads a file or the environment; every policy value comes in through the ``rule`` argument that
+``loader.load_rule`` returns.  The pipeline, the verdict and the report are added further down in this module.
+"""
+import math
+
+TYPED = ("bug", "build", "performance", "deployment", "security", "test")
+UNSET_LABELS = ("ambiguous", "none-fit")
+
+
+def right(label, answer):
+    """A typed label is right when the answer is that type; an ``ambiguous`` or ``none-fit`` label is right when the answer is
+    unset (``None``).  The same rule serves both arms.  An unset answer on a typed label is not right."""
+    if label in UNSET_LABELS:
+        return answer is None
+    if label in TYPED:
+        return answer == label
+    raise ValueError(f"unknown label {label!r}")
+
+
+def sign_test_passes(b, c, alpha_inverse=20):
+    """Exact one-sided sign test in integer arithmetic.  b = prompts only Jev gets right, c = prompts only the table gets right.
+    Jev clearly beats the table when ``alpha_inverse * tail < 2 ** n``, where n = b + c and tail = the count of outcomes with at
+    least b successes out of n fair coin tosses.  With b + c = 0 there is nothing to test: not clearly."""
+    n = b + c
+    if n == 0:
+        return False
+    tail = sum(math.comb(n, k) for k in range(b, n + 1))
+    return alpha_inverse * tail < 2 ** n
+
+
+def jev_answer(noul_p, choice, rule):
+    """Map Jev's two answers to one answer or an unset answer.
+
+    ``noul_p`` is the Noul value of ``any_type_fits`` (high means a type fits); ``choice`` is the validated answer of
+    ``problem_type``.  Below the low edge (``lt``: strictly below ``noul_low``; ``le``: at or below) the answer is unset with
+    reason ``none-fit``.  Above the high edge (``gt``: strictly above ``noul_high``; ``ge``: at or above) the answer is the
+    choice.  In between it is unset with reason ``not-settled``.  Returns ``(answer, reason)``; the reason is ``None`` when the
+    answer is the choice.  Refuses an operator that is ``UNSET`` or not valid for its edge."""
+    low_op, high_op = rule["noul_low_operator"], rule["noul_high_operator"]
+    if low_op not in ("lt", "le"):
+        raise ValueError(f"noul_low_operator must be lt or le, not {low_op!r}")
+    if high_op not in ("gt", "ge"):
+        raise ValueError(f"noul_high_operator must be gt or ge, not {high_op!r}")
+    low, high = rule["noul_low"], rule["noul_high"]
+    if (noul_p < low) if low_op == "lt" else (noul_p <= low):
+        return None, "none-fit"
+    if (noul_p > high) if high_op == "gt" else (noul_p >= high):
+        return choice, None
+    return None, "not-settled"
+
+
+def median(values):
+    """The median; an even count gives the mean of the two middle values; an empty list gives ``None``."""
+    v = sorted(values)
+    if not v:
+        return None
+    mid = len(v) // 2
+    return v[mid] if len(v) % 2 else (v[mid - 1] + v[mid]) / 2
+
+
+def percentile_nearest_rank(values, q):
+    """Nearest-rank percentile: ``sorted[ceil(q * n) - 1]``; an empty list gives ``None``."""
+    v = sorted(values)
+    if not v:
+        return None
+    return v[min(max(math.ceil(round(q * len(v), 9)) - 1, 0), len(v) - 1)]
+
+
+def latency_stats(attempts, rule):
+    """Latency statistics over the attempts of a run.
+
+    Each attempt is a dict with ``prompt_id``, ``latency_s``, ``timed_out`` and ``answered`` (the response was a valid answer).
+    The slowest is taken over all attempts, a timeout counted at ``attempt_timeout_s``.  The median and the 90th percentile are
+    taken over one value per prompt, by ``median_population``: ``answered_only`` uses each prompt's last answered attempt;
+    ``include_timeouts_at_cap`` uses each prompt's last attempt that answered or timed out, a timeout at ``attempt_timeout_s``.
+    Every statistic is ``None`` when no value qualifies."""
+    cap = rule["attempt_timeout_s"]
+
+    def value(a):
+        return cap if a["timed_out"] else a["latency_s"]
+
+    mode = rule["median_population"]
+    if mode not in ("answered_only", "include_timeouts_at_cap"):
+        raise ValueError(f"unknown median_population {mode!r}")
+    last = {}
+    for a in attempts:
+        if a["answered"] or (mode == "include_timeouts_at_cap" and a["timed_out"]):
+            last[a["prompt_id"]] = value(a)
+    pop = list(last.values())
+    slowest = [value(a) for a in attempts]
+    return {"median": median(pop), "slowest": max(slowest) if slowest else None,
+            "p90": percentile_nearest_rank(pop, 0.9), "n": len(pop)}
diff --git a/.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py
new file mode 100644
index 000000000..5fca1d077
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py
@@ -0,0 +1,137 @@
+from fractions import Fraction
+
+import pytest
+from harness import scorer
+from harness.scorer import (
+    jev_answer,
+    latency_stats,
+    median,
+    percentile_nearest_rank,
+    right,
+    sign_test_passes,
+)
+
+# ---- right (T-07)
+
+def test_right_for_a_typed_label():
+    assert right("bug", "bug") is True
+    assert right("bug", "test") is False
+    assert right("bug", None) is False                 # an unset answer on a typed label is not right
+
+
+@pytest.mark.parametrize("label", ["ambiguous", "none-fit"])
+def test_right_for_an_unset_label_needs_an_unset_answer(label):
+    assert right(label, None) is True
+    assert right(label, "bug") is False
+
+
+def test_right_refuses_an_unknown_label():
+    with pytest.raises(ValueError):
+        right("urgent", None)
+
+
+# ---- sign test (T-12, T-15)
+
+@pytest.mark.parametrize("b,c", [(5, 0), (7, 1), (9, 2)])
+def test_sign_test_passes_for_the_agreed_cases(b, c):
+    assert sign_test_passes(b, c) is True
+
+
+@pytest.mark.parametrize("b,c", [(4, 0), (6, 1), (8, 2), (0, 0), (0, 7), (3, 9)])
+def test_sign_test_fails_for_the_agreed_cases(b, c):
+    assert sign_test_passes(b, c) is False
+
+
+def test_smallest_passing_b_for_each_c_from_0_to_6():
+    smallest = [next(b for b in range(0, 40) if sign_test_passes(b, c)) for c in range(7)]
+    assert smallest == [5, 7, 9, 10, 12, 13, 15]
+
+
+def test_sign_test_agrees_with_an_exact_fraction_reference_up_to_30():
+    from math import comb
+    for b in range(31):
+        for c in range(31):
+            n = b + c
+            expected = n > 0 and Fraction(sum(comb(n, k) for k in range(b, n + 1)), 2 ** n) < Fraction(1, 20)
+            assert sign_test_passes(b, c) is expected, (b, c)
+
+
+def test_sign_test_reads_the_factor_from_the_rule():
+    assert sign_test_passes(4, 0, alpha_inverse=10) is True      # 1/16 is below 1/10 but not below 1/20
+    assert sign_test_passes(4, 0, alpha_inverse=20) is False
+
+
+# ---- jev_answer (T-05)
+
+def _rule(low_op, high_op):
+    return {"noul_low": 0.3, "noul_high": 0.7, "noul_low_operator": low_op, "noul_high_operator": high_op}
+
+
+@pytest.mark.parametrize("low_op", ["lt", "le"])
+@pytest.mark.parametrize("high_op", ["gt", "ge"])
+def test_jev_answer_at_and_around_both_edges(low_op, high_op):
+    rule = _rule(low_op, high_op)
+    assert jev_answer(0.2999999, "bug", rule) == (None, "none-fit")
+    assert jev_answer(0.3, "bug", rule) == ((None, "none-fit") if low_op == "le" else (None, "not-settled"))
+    assert jev_answer(0.3000001, "bug", rule) == (None, "not-settled")
+    assert jev_answer(0.5, "bug", rule) == (None, "not-settled")
+    assert jev_answer(0.6999999, "bug", rule) == (None, "not-settled")
+    assert jev_answer(0.7, "bug", rule) == (("bug", None) if high_op == "ge" else (None, "not-settled"))
+    assert jev_answer(0.7000001, "bug", rule) == ("bug", None)
+
+
+@pytest.mark.parametrize("low_op,high_op", [("UNSET", "ge"), ("le", "UNSET"), ("gt", "ge"), ("le", "lt")])
+def test_jev_answer_refuses_an_unset_or_misplaced_operator(low_op, high_op):
+    with pytest.raises(ValueError):
+        jev_answer(0.5, "bug", _rule(low_op, high_op))
+
+
+# ---- median, percentile, latency (T-08)
+
+def test_median_of_odd_and_even_counts_and_empty():
+    assert median([3, 1, 2]) == 2
+    assert median([4, 1, 3, 2]) == 2.5
+    assert median([]) is None
+
+
+def test_nearest_rank_percentile():
+    assert percentile_nearest_rank(list(range(1, 11)), 0.9) == 9          # ceil(9) - 1 = index 8
+    assert percentile_nearest_rank(list(range(1, 31)), 0.9) == 27
+    assert percentile_nearest_rank(list(range(1, 12)), 0.9) == 10         # ceil(9.9) - 1 = index 9
+    assert percentile_nearest_rank([5], 0.9) == 5
+    assert percentile_nearest_rank([], 0.9) is None
+
+
+def _a(pid, latency, timed_out=False, answered=True):
+    return {"prompt_id": pid, "latency_s": latency, "timed_out": timed_out, "answered": answered}
+
+
+RULE = {"attempt_timeout_s": 10.0, "median_population": "answered_only"}
+
+
+def test_timeout_counts_at_the_cap_in_the_slowest_and_is_left_out_of_the_median():
+    attempts = [_a("p1", 10.4, timed_out=True, answered=False), _a("p1", 1.0), _a("p2", 3.0)]
+    s = latency_stats(attempts, RULE)
+    assert s["slowest"] == 10.0 and s["median"] == 2.0 and s["p90"] == 3.0 and s["n"] == 2
+
+
+def test_a_prompt_that_never_answered_is_not_in_the_answered_only_population():
+    s = latency_stats([_a("p1", 0.5), _a("p2", 2.0, answered=False)], RULE)
+    assert s["n"] == 1 and s["median"] == 0.5 and s["slowest"] == 2.0
+
+
+def test_the_include_timeouts_population_counts_a_timeout_at_the_cap():
+    rule = dict(RULE, median_population="include_timeouts_at_cap")
+    s = latency_stats([_a("p1", 1.0), _a("p2", 10.2, timed_out=True, answered=False)], rule)
+    assert s["n"] == 2 and s["median"] == 5.5 and s["slowest"] == 10.0
+
+
+def test_latency_stats_on_no_attempts_are_none_and_an_unknown_population_is_refused():
+    assert latency_stats([], RULE) == {"median": None, "slowest": None, "p90": None, "n": 0}
+    with pytest.raises(ValueError):
+        latency_stats([_a("p1", 1.0)], dict(RULE, median_population="all"))
+
+
+def test_scorer_has_no_floating_point_comparison_at_the_agreed_line():
+    text = open(scorer.__file__, encoding="utf-8").read()
+    assert "0.05" not in text and "0.95" not in text


Codegraph context
index_state: fresh
checked_at: 2026-11-26T16:38:23Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-611
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-611
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: the files of this task are new or only used by later tasks; no dependent outside the touched files.
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
