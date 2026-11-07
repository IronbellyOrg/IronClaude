7bb99a1ab07d3093cefe6119b64b21c08f00ff59
Review one task for spec compliance.

Task brief: ## Task 8: Add the late pass to `refs/state-machine.md` section 5.2d

Depends on: Task 5, Task 7

Run serially: Tasks 6 to 9 edit the same test files.

Satisfies: R-010 (`state-machine.md`), R-007, R-008, R-012 (part d).

Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md`, section 5.2d: add one sentence to the Tier 1 bullet saying the sync can also run once from the Wave 8 late trigger, still with no FSM edge, no round and no re-trigger, and stating the R-007 cap wording and the R-008 preconditions (cap of at least 1 at every monitor level, only monitor 3 pushes, monitors 1 and 2 act only after `clean` or `report_only`). Leave the wait-only sentence pinned by `test_wait_only_sentences_name_the_one_sync_exception` byte-identical and add no standalone `gh` or `git` word.

Acceptance criteria (ids):
T8.AC1: A new assertion in `tests/pr_submit/test_static_grep.py` runs on `_prose(path)` of the file (the helper takes the file `Path`) and pins the new sentence ("late trigger", "conflict cycle started earlier", "`--conflict-max-tier` of at least 1"); removing only that sentence fails it, and the section still states `SYNC_CAP = 1`, `sync_push_count` and that the sync never counts in `push_count`.
T8.AC2: `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_autonomy_gates.py tests/pr_submit/test_conflict_sync_protocol.py -q` passes, including `test_tn50_core_pure_no_gh_git_tokens`.
Global constraints: 
- Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`; the `.claude/` mirrors are generated and are never staged.
- Use `uv run ...` for every Python and pytest call; no bare `python` or `pip`.
- `src/superclaude/pr_submit/fsm.py`, `run_log.py`, `models.py` and `ci.py` are not edited, no new `EventType` is added and every existing push-safety rule stays as it is (R-003, R-004).
- `src/superclaude/pr_submit/conflicts.py` and `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` are in the core-pure file set of `tests/pr_submit/test_static_grep.py`: neither may contain the standalone words `gh` or `git` on any line, comments and docstrings included.
- Several tests pin exact lines of the files this plan edits: `tests/skills/test_worker_contract.py` (an inventory keyed by exact file line, with a stale-entry check), `tests/pr_submit/test_conflict_sync_protocol.py` (fragments E1 to E13, order pins) and `tests/pr_submit/test_static_grep.py`. Each task that changes a pinned line updates the pin in the same task. The router outcomes any prose describes are the table in R-005 of `./source.md`, which `_WAVE8A_ROWS` in `tests/pr_submit/test_conflicts_core.py` already pins, so no router row is added anywhere in this plan.
- Every new prose deliverable gets its own positive assertion scoped to that text (R-012 part d), so that removing only that text fails exactly that assertion.
- Non-goal: the go/no-go gate of the issue (one real run where the base moved, or a maintainer waiver) is a release sign-off item and stays open (R-014). Nothing in this plan runs against a real PR.
- Non-goal: `.dev/brainstorms/issue-305-pr-submit-conflict-resolution/merged-requirements.md` and `.dev/designs/issue-305-pr-submit-conflict-resolution/DESIGN.md` are historical records and are not edited.
- Owner authorization (2026-11-07, relayed by the coordinator): after the third advisory review left two word-level blocking findings (the "unconditional" end-of-wait re-read in R-010 and Task 7, and the over-general status bullet in R-005), the owner allowed word edits to `./source.md` and this plan, with the listed minor guardrails, and no fourth review. The corrections are in R-005, R-010, Task 7 and the guardrails of Tasks 1, 2, 6, 7, 9 and 10; the report is `.dev/reflect/pre-TASK-WF-p3Requirements-20261107-070713-20261107070932/REPORT.md`.
Start sha: 7bb99a1ab07d3093cefe6119b64b21c08f00ff59
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
index 97583485..cfa31641 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
@@ -165,7 +165,11 @@ a non-halted CI-clean path sends `clean` to `transition()`. L0 never enters this
   (both tiers together). After `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE` that terminal
   stays and the sync outcome is reported alongside it. At L2 the resolution is left validated and
   uncommitted; the caller sets `S4'_HALT_BEFORE_PUSH` only when Wave 8 was entered from `clean` or
-  `REPORT_ONLY`.
+  `REPORT_ONLY`. The same sync can also run once from the Wave 8 late trigger (`SKILL.md`), still
+  with no FSM edge, no round and no re-trigger: the cap counts a conflict cycle whether or not it
+  landed, so the late sync runs only when no conflict cycle started earlier and the run has
+  `--conflict-max-tier` of at least 1, at every monitor level; only monitor 3 pushes, and monitors
+  1 and 2 act only after `clean` or `report_only`.
 - **Tier 2 (push kind `merge`)** adds exactly one edge: `(S2_CLASSIFY, conflicting)` goes to
   `HALT_MAX_ROUNDS` when the round gate fires (the same gate as `findings`), else to `S3_FIXING`
   (L2+) or `PROPOSED` (L1) by G-edit. The cycle then follows the existing edges
diff --git a/tests/pr_submit/test_static_grep.py b/tests/pr_submit/test_static_grep.py
index 0094550b..515e076b 100644
--- a/tests/pr_submit/test_static_grep.py
+++ b/tests/pr_submit/test_static_grep.py
@@ -842,6 +842,24 @@ def test_ci_poll_has_the_late_conflict_trigger_section():
     ) in _prose(_CI_POLL_REF)
 
 
+# --- Issue #361 (P3): refs/state-machine.md section 5.2d names the late pass ----
+
+
+def test_state_machine_5_2d_names_the_late_trigger_sync():
+    machine = _prose(SKILL_DIR / "refs" / "state-machine.md")
+    assert (
+        "The same sync can also run once from the Wave 8 late trigger (`SKILL.md`), "
+        "still with no FSM edge, no round and no re-trigger: the cap counts a conflict "
+        "cycle whether or not it landed, so the late sync runs only when no conflict "
+        "cycle started earlier and the run has `--conflict-max-tier` of at least 1, at "
+        "every monitor level; only monitor 3 pushes, and monitors 1 and 2 act only "
+        "after `clean` or `report_only`."
+    ) in machine
+    # The section keeps its cap, counter and "never in push_count" statements.
+    assert "`SYNC_CAP = 1`" in machine
+    assert "`sync_push_count`, never in `push_count`" in machine
+
+
 def test_s5a_retrigger_widened_for_merge_cycles_only():
     """P2 / QA-3a: the Wave 6 S5a re-trigger is widened only for a Tier 2 merge cycle;
     the zero-edit fix-commit sentence and the state-machine parent-check sentence are

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
