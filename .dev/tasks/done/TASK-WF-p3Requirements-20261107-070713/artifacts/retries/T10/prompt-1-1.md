1ca93e0d4094bb86ea615bf3aec65c952501c996
Review one task for spec compliance.

Task brief: ## Task 10: Add the changelog entry and sync the dev copies

Depends on: Task 2, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9

Satisfies: R-013, R-014, R-012 (part d).

Edit `CHANGELOG.md`: add a bullet "pr-submit late conflict re-sync (P3, #361)" under `#### Added (pr-submit conflicts)` of the `### sc:pr-submit: merge-conflict detection and resolution (#305)` block (line 131 onward). It states the `merge_state` poll field, the late second Wave 8a pass, its limits per R-007 and R-008, that a late Tier 2 conflict halts as `late_conflict` with a cap of 2 and as `tier_above_cap` below it, and that the real-run go/no-go gate is still open. Rewrite the sentence "Late re-sync during the CI wait is #361." (line 146 of the same block) in place so it no longer reads as future work. Add a new test with a clear name (for example in `tests/pr_submit/test_conflict_sync_protocol.py`) with three separate assertions: `CHANGELOG.md` contains "late conflict re-sync", does not contain "is #361", and contains the rewritten sentence in full (so deleting the old sentence without a replacement fails). Then run `make sync-dev`.

Acceptance criteria (ids):
T10.AC1: `rg -n "late conflict re-sync" CHANGELOG.md` finds the new bullet, `rg -n "is #361" CHANGELOG.md` finds nothing, and each of the three assertions of the new test fails when only its text is removed.
T10.AC2: `make sync-dev` succeeds and `make verify-sync` passes.
T10.AC3: `uv run pytest tests/pr_submit tests/skills/test_worker_contract.py tests/unit/test_cli_install.py -q` passes and `make lint` reports no findings.
T10.AC4: `git diff --name-only` lists only paths under `src/superclaude/`, `tests/`, `docs/user-guide/`, `CHANGELOG.md` and `.dev/tasks/`, and `git diff --cached --name-only` lists no `.claude/` path.
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
Start sha: 1ca93e0d4094bb86ea615bf3aec65c952501c996
Diff against the start snapshot: 
diff --git a/CHANGELOG.md b/CHANGELOG.md
index f2436c80..78662b25 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -136,6 +136,7 @@ All notable changes to IronClaude are documented in this file.
 - Tier 3 (submodule, symlink, mode change, protected or migration path, binary, lock or generated file without a rule, more than 8 text files, anything unclassifiable) halts at the end of Wave 0 at L3 with nothing touched, and is reported at L1 and L2.
 - New flag `--conflict-max-tier {0,1,2}` (default 0); 0 detects and reports only, so no conflict is resolved unless you pass 1 or 2.
 - New core module `superclaude.pr_submit.conflicts`, refs `conflict-mechanical.md` and `conflict-intent.md`, scripts `probe-merge.sh`, `finish-merge.sh` and `collect-conflict-evidence.sh`, and `poll-ci-checks.sh --evidence-sha`.
+- pr-submit late conflict re-sync (P3, #361): the CI poll line now carries a `merge_state` object, and when it reads conflicting the SKILL runs the Wave 8a conflict step once more during the CI wait. The one-cycle cap still holds: the late pass runs only when no conflict cycle started earlier in the run, needs `--conflict-max-tier` of at least 1 at every monitor level (with the default cap of 0 it ends with `tier_above_cap`), monitor 1 only proposes, monitor 2 only leaves a validated uncommitted merge, and only monitor 3 pushes. A late Tier 2 (text) conflict halts as `late_conflict` with a cap of 2 and ends as `tier_above_cap` below it. The go/no-go gate of the issue (one real run where the base moved during the CI wait, or a maintainer waiver) is still open; nothing was run against a real PR.
 
 #### Changed (pr-submit conflicts)
 
@@ -143,7 +144,7 @@ All notable changes to IronClaude are documented in this file.
 - Every push record carries a `kind` (`fix`, `merge`, `sync`, `ci`); `--resume` uses it, so a crashed CI or sync push resumes into the CI wait instead of the review re-trigger path. Old run-logs read as `fix`.
 - `push_count` counts fix, CI and Tier 2 merge pushes; Tier 1 sync pushes are in `sync_push_count`. The documented bound is `push_count <= max_rounds + 1`.
 - The run-log event enum has 43 members (`sync_started`, `sync_concluded`).
-- A PR that is still conflicting at Wave 8 with nothing pushed skips the CI wait (`pr_conflicting`) and ends `terminal_halted` instead of waiting for checks that GitHub will not run; a run that saw a conflict re-reads `mergeable` before claiming clean. Late re-sync during the CI wait is #361.
+- A PR that is still conflicting at Wave 8 with nothing pushed skips the CI wait (`pr_conflicting`) and ends `terminal_halted` instead of waiting for checks that GitHub will not run; a run that saw a conflict re-reads `mergeable` before claiming clean. A conflict that first appears during the CI wait now gets one late re-sync pass (see the P3 entry above).
 
 ## [5.0.0] - 2026-11-02
 
diff --git a/tests/pr_submit/test_conflict_sync_protocol.py b/tests/pr_submit/test_conflict_sync_protocol.py
index 59055802..cc6245b7 100644
--- a/tests/pr_submit/test_conflict_sync_protocol.py
+++ b/tests/pr_submit/test_conflict_sync_protocol.py
@@ -111,6 +111,16 @@ def test_late_tier1_sync_sentence_is_in_each_user_facing_text(path):
     assert "conflict cycle started earlier" in text
 
 
+def test_changelog_records_the_late_conflict_resync_and_no_longer_defers_it():
+    text = _prose(REPO_ROOT / "CHANGELOG.md")
+    assert "late conflict re-sync" in text
+    assert "is #361" not in text
+    assert (
+        "A conflict that first appears during the CI wait now gets one late re-sync "
+        "pass (see the P3 entry above)."
+    ) in text
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
