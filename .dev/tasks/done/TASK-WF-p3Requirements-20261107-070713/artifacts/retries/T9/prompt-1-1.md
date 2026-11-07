6a41381d7f180b28081e65efd61167483d80f0a6
Review one task for spec compliance.

Task brief: ## Task 9: Update the command summary and the user guides

Depends on: Task 5, Task 8

Run serially: Tasks 6 to 9 edit the same test files.

Satisfies: R-011, R-007, R-008, R-012 (part d).

Edit `src/superclaude/commands/pr-submit.md` (the paragraph at line 72 ending "Late text conflicts halt..."), `docs/user-guide/commands.md` (the paragraph at line 501) and `docs/user-guide/flags.md` (the paragraph at line 214). Add one sentence to each: a conflict that first appears while the CI wait is running gets one more Tier 1 sync only when no conflict cycle started earlier in the run; it needs `--conflict-max-tier` of at least 1 at every monitor level (with the default cap of 0 it ends with `tier_above_cap`); with a cap of at least 1 monitor 1 only proposes and monitor 2 only leaves a validated uncommitted merge, both only after a `clean` or `report_only` review, and only monitor 3 pushes; a late text (Tier 2) conflict halts. Keep the phrases that tests pin (listed in R-011 of `./source.md`).

Acceptance criteria (ids):
T9.AC1: `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py -q` passes.
T9.AC2: A new test in `tests/pr_submit/test_conflict_sync_protocol.py` asserts, per file and on its prose-normalised text, that each of the three files contains the full new sentence as written in that file (a full-sentence substring, not bare words, because "tier_above_cap" and "only after" may occur elsewhere in the same file) and, as a second check, the phrase "conflict cycle started earlier"; removing the new sentence from any one file fails only that file's case.
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
Start sha: 6a41381d7f180b28081e65efd61167483d80f0a6
Diff against the start snapshot: 
diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index ccd97311..6567eb13 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -498,7 +498,7 @@ PM Agent:
 | `1` (opt-in) | Also regenerate a conflicted root `uv.lock` before CI. For eligible Tier 1 cases after a clean or report-only review, monitor 1 proposes and monitor 2 leaves a validated, uncommitted merge in progress; monitor 3 may push one validated merge of the recorded base tip. |
 | `2` (opt-in) | Also resolve text/tree conflicts by stated intent, only before the first review at monitor 3. Requires at least two remaining review rounds, at most eight text-conflict files, a resolution record, a read-only grounding check and full tests. Re-triggers configured reviewers; an attributed re-review spends a round. |
 
-Tier 3 conflicts need human resolution: for example protected/migration paths, binary files, symlinks, mode changes, unsupported lock/generated files or unclear intent. They are reported at monitor 1 or 2 and halt at monitor 3. There is at most one conflict cycle per run; late text conflicts halt rather than triggering continuous repair. A Tier 1 sync push uses no review round and sends no reviewer re-trigger, reply or thread resolution; it does not clear a non-clean review outcome. After a merge push, CI follows the new head: expected-but-missing checks keep polling and may time out as `ci_not_started`; unresolved conflicts skip CI as `pr_conflicting`.
+Tier 3 conflicts need human resolution: for example protected/migration paths, binary files, symlinks, mode changes, unsupported lock/generated files or unclear intent. They are reported at monitor 1 or 2 and halt at monitor 3. There is at most one conflict cycle per run; late text conflicts halt rather than triggering continuous repair. A conflict that first appears while the CI wait is running gets one more Tier 1 sync only when no conflict cycle started earlier in the run; it needs `--conflict-max-tier` of at least 1 at every monitor level (with the default cap of 0 it ends with `tier_above_cap`), and with a cap of at least 1 monitor 1 only proposes and monitor 2 only leaves a validated uncommitted merge, both only after a `clean` or `report_only` review, and only monitor 3 pushes; a late text (Tier 2) conflict halts. A Tier 1 sync push uses no review round and sends no reviewer re-trigger, reply or thread resolution; it does not clear a non-clean review outcome. After a merge push, CI follows the new head: expected-but-missing checks keep polling and may time out as `ci_not_started`; unresolved conflicts skip CI as `pr_conflicting`.
 
 **Examples (run in Claude Code, not a shell):**
 
diff --git a/docs/user-guide/flags.md b/docs/user-guide/flags.md
index 5e6f5875..765495ba 100644
--- a/docs/user-guide/flags.md
+++ b/docs/user-guide/flags.md
@@ -211,7 +211,7 @@ Since 5.0.0 `FLAGS.md` and `MODES.md` are no longer shipped, and old copies left
 | `--conflict-max-tier` | Highest merge-conflict tier permitted, subject to the monitor ceiling | `0` (default: detect and report only), `1` (also root `uv.lock` regeneration, opt-in), `2` (also initial intent-based text/tree resolution at monitor `3`) |
 | `--head` / `--base` / `--title` / `--body` | PR details | Branch names, text |
 
-The monitor ceiling and conflict cap are independent: monitor defaults to `3`, conflict cap to `0`. Raising the cap does not authorize Tier 3 resolution or bypass monitor limits; monitor `0` skips conflict handling entirely. Eligible Tier 1 cases at monitor `1` propose, at `2` leave a validated uncommitted merge, and at `3` may push. Tier 2 requires monitor `3`, cap `2`, at least two remaining rounds and at most eight text-conflict files, and runs only before the first review. Thus `--max-rounds 1` cannot fund Tier 2 resolution. Only one conflict cycle is allowed per run; late text conflicts halt.
+The monitor ceiling and conflict cap are independent: monitor defaults to `3`, conflict cap to `0`. Raising the cap does not authorize Tier 3 resolution or bypass monitor limits; monitor `0` skips conflict handling entirely. Eligible Tier 1 cases at monitor `1` propose, at `2` leave a validated uncommitted merge, and at `3` may push. Tier 2 requires monitor `3`, cap `2`, at least two remaining rounds and at most eight text-conflict files, and runs only before the first review. Thus `--max-rounds 1` cannot fund Tier 2 resolution. Only one conflict cycle is allowed per run; late text conflicts halt. A conflict that first appears while the CI wait is running gets one more Tier 1 sync only when no conflict cycle started earlier in the run; it needs `--conflict-max-tier` of at least 1 at every monitor level (with the default cap of 0 it ends with `tier_above_cap`), and with a cap of at least 1 monitor 1 only proposes and monitor 2 only leaves a validated uncommitted merge, both only after a `clean` or `report_only` review, and only monitor 3 pushes; a late text (Tier 2) conflict halts.
 
 Opt in only for PRs from collaborators trusted with your credentials: lock regeneration, validation and commit hooks execute project code. The lock trust gate is not a sandbox and does not cover Git/URL dependency sources; without a TOML parser (including Python 3.10) it fails closed. See [the command guide](commands.md#scpr-submit---pr-review-auto-remediation-monitor) for examples, review/CI behavior, safety and recovery.
 
diff --git a/src/superclaude/commands/pr-submit.md b/src/superclaude/commands/pr-submit.md
index 6427aa49..3e64c64b 100644
--- a/src/superclaude/commands/pr-submit.md
+++ b/src/superclaude/commands/pr-submit.md
@@ -69,7 +69,7 @@ Explicit only — two activation paths:
 | 2: text/tree conflicts with statable intent | Cap 2 and monitor 3 only, before the first review, with at least two remaining review rounds and at most eight text-conflict files. The skill records both sides' intent and any dropped behavior, requires a read-only grounding check and full tests, then may publish the merge and re-trigger configured reviewers. An attributed re-review spends a round. |
 | 3: unsafe or unclassifiable | Report at monitor 1 or 2; halt for human resolution at monitor 3. Examples include protected or migration paths, binaries, symlinks, submodules, mode changes and unsupported lock/generated files. Unclear or semantic intent escalates here rather than being invented. |
 
-There is at most one conflict cycle per run across both resolving tiers. Late text conflicts halt; this is not continuous automatic conflict repair. A Tier 1 sync push spends no review round and sends no reviewer re-trigger, reply or thread resolution. It is the single sync exception on otherwise wait-only paths; it does not turn reviewer silence or round exhaustion into a clean review. Normal fix-cycle re-trigger behavior described below is unchanged.
+There is at most one conflict cycle per run across both resolving tiers. Late text conflicts halt; this is not continuous automatic conflict repair. A conflict that first appears while the CI wait is running gets one more Tier 1 sync only when no conflict cycle started earlier in the run; it needs `--conflict-max-tier` of at least 1 at every monitor level (with the default cap of 0 it ends with `tier_above_cap`), and with a cap of at least 1 monitor 1 only proposes and monitor 2 only leaves a validated uncommitted merge, both only after a `clean` or `report_only` review, and only monitor 3 pushes; a late text (Tier 2) conflict halts. A Tier 1 sync push spends no review round and sends no reviewer re-trigger, reply or thread resolution. It is the single sync exception on otherwise wait-only paths; it does not turn reviewer silence or round exhaustion into a clean review. Normal fix-cycle re-trigger behavior described below is unchanged.
 
 After a merge push, CI is checked against the new head. Expected checks that have not appeared keep the wait open and can time out as `ci_not_started`; they are not read as success. Unresolved conflicts skip the CI wait with reason `pr_conflicting`. The run output includes `sync_tier`, `sync_outcome` and `sync_push_count` alongside the review result.
 
diff --git a/tests/pr_submit/test_conflict_sync_protocol.py b/tests/pr_submit/test_conflict_sync_protocol.py
index ea64d9f4..59055802 100644
--- a/tests/pr_submit/test_conflict_sync_protocol.py
+++ b/tests/pr_submit/test_conflict_sync_protocol.py
@@ -83,6 +83,34 @@ def test_command_summarizes_conflict_protocol_without_replacing_activation():
     assert "Skill sc:pr-submit-protocol" in text
 
 
+# --- Issue #361 (P3): the late Tier 1 sync sentence in the three user-facing texts ---
+
+LATE_SYNC_SENTENCE = (
+    "A conflict that first appears while the CI wait is running gets one more Tier 1 "
+    "sync only when no conflict cycle started earlier in the run; it needs "
+    "`--conflict-max-tier` of at least 1 at every monitor level (with the default cap "
+    "of 0 it ends with `tier_above_cap`), and with a cap of at least 1 monitor 1 only "
+    "proposes and monitor 2 only leaves a validated uncommitted merge, both only after "
+    "a `clean` or `report_only` review, and only monitor 3 pushes; a late text (Tier 2) "
+    "conflict halts."
+)
+
+
+@pytest.mark.parametrize(
+    "path",
+    [
+        COMMAND_MD,
+        REPO_ROOT / "docs" / "user-guide" / "commands.md",
+        REPO_ROOT / "docs" / "user-guide" / "flags.md",
+    ],
+    ids=lambda p: p.parent.name + "/" + p.name,
+)
+def test_late_tier1_sync_sentence_is_in_each_user_facing_text(path):
+    text = _prose(path)
+    assert LATE_SYNC_SENTENCE in text
+    assert "conflict cycle started earlier" in text
+
+
 # --- Pinned phrases and order pins (design sections 8.2 and 8.3) --------------
 
 MECHANICAL_PINS = (

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
