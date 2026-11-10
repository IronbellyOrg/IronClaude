start=c531b24edaa45cfd3cba6f8204d20a3434eb5cb5
Review one task for spec compliance.

Task brief: Task 4: Add the ordered owner checklist and the cron install step to docs/designs/issue-watcher-setup.md

Depends on: Task 3

The runbook already describes each owner step (section 7 shadow run, 8.1 review, 8.2 lock test, 8.3 restart test, 8.4 staleness alert, 8.5 live-test record, 8.6 set enabled, 14.1 live test), but they are spread over two places, with the live test in section 14 although it must come first, and the cron entry (FU-2) has only a one-line mention at the end of 8.6. Make two edits:
- Add a subsection "8.7 Install the cron entry (FU-2)" after 8.6. It says: only after 8.6; the schedule is `0 */5 * * * *` (six fields, seconds first: every 5 minutes, at second 0); the scheduled command is `superclaude issue-watch once` (with `--config <path>` when the configuration file is not at the default path); run `superclaude issue-watch check-config` first and confirm the `state_dir` it prints is on storage that survives a workspace restart, setting `state_dir` in the configuration file when `$HOME` is not persistent; after the first scheduled cycles, `superclaude issue-watch status` exits 0. Keep the existing sentence that the scheduler is the owner's choice; do not name a scheduler product the runbook does not already name. Move the one-line cron mention from 8.6 into 8.7 rather than repeating it.
- Add a section "16. Rollout checklist" at the end of the file: a bulleted list (plain `-` bullets, no checkboxes, no numbers) in this order, each bullet one sentence that links to the section that holds the detail: pre-flight (section 1); configuration with `enabled: false` (section 2); approvers file, labels, `init-state` (sections 3 to 5); the live test with the capture sheet and the committed record (section 14.1, 14.1.1, 8.5); the captured replies replace the fixtures and `uv run pytest tests/issue_watch/` passes; the 24-hour shadow run (section 7) and its review (8.1); the lock test (8.2); the restart test (8.3); the staleness alert (8.4); set `enabled` to `true` (8.6); install the cron entry (8.7). The list opens with one sentence saying every item is run by the owner and nothing in the implementation runs any of it.

Acceptance criteria:
T4.AC1: `docs/designs/issue-watcher-setup.md` has a "8.7 Install the cron entry (FU-2)" subsection containing `0 */5 * * * *`, `superclaude issue-watch once`, `check-config`, `state_dir` and `status`, and section 8.6 no longer carries its own cron sentence (`grep -c '0 \*/5 \* \* \* \*'` counts one in 8.7 plus the unchanged FU-2 row of 15.3).
T4.AC2: A "16. Rollout checklist" section exists with the eleven bullets in the order above, each linking to its section; it has no `- [ ]` and no numbered lines.
T4.AC3: `grep -n '"enabled": false' docs/designs/issue-watcher-setup.md` still finds the section 2 example, and the checklist puts "set `enabled` to `true`" after the live test, shadow run, lock and restart bullets and before the cron bullet.
T4.AC4: The FU-1 and FU-2 rows of section 15.3 are unchanged.
T4.AC5: The checks above and their output are saved to `./artifacts/t4-checklist-check.log`.
Global constraints: 
- Agent tasks change only `docs/designs/issue-watcher.md`, `docs/designs/issue-watcher-setup.md` (Tasks 1 to 4) and, in Task 5, the 19 files under `tests/issue_watch/fixtures/_assumed_shape/` and `tests/issue_watch/test_github.py`. No file under `src/` or `.claude/` changes.
- `enabled` stays `false`: the example configuration in section 2 of `docs/designs/issue-watcher-setup.md` (`"enabled": false`) and the default `raw.get("enabled", False)` in `src/superclaude/cli/issue_watch/cycle.py` are not touched by any task.
- No agent runs `gh`, `orca` or `superclaude issue-watch` against real GitHub or Orca, writes to GitHub, launches an Orca agent, takes the lock on a real state directory, edits a crontab or scheduler, commits or pushes. Those are owner-run items (listed below); the plan only writes them down.
- No agent writes `docs/designs/issue-watcher-live-test.md`. The design (section 1, "Deployment gate") and the runbook (section 14.1) say the owner writes and commits it.
- Task 2 adds one row to the exit-code table in section 4.3 of `docs/designs/issue-watcher.md`, which shifts the design line numbers that the fixture `source` fields cite by one. That is accepted: Task 5 rewrites the `source` field of every captured fixture. New text cites sections and table rows by name, never by line number.
- Out of scope: follow-ups FU-3 to FU-12, the owner questions Q1 to Q4 in section 16 of the design, the low regression fix recorded in the build's worker final report, renaming the `_assumed_shape` fixture directory, and any change to the parsers in `src/superclaude/cli/issue_watch/github.py` or `launch.py` (a captured shape that breaks a parser is recorded for a follow-up plan, never patched here).


Start sha: c531b24edaa45cfd3cba6f8204d20a3434eb5cb5
Diff against the start snapshot: diff --git a/docs/designs/issue-watcher-setup.md b/docs/designs/issue-watcher-setup.md
index 7ddeffccf..d49f9f04b 100644
--- a/docs/designs/issue-watcher-setup.md
+++ b/docs/designs/issue-watcher-setup.md
@@ -279,7 +279,11 @@ Only now change `"enabled": false` to `"enabled": true` in the configuration fil
 
 Run `superclaude issue-watch check-config` again. The first real cycle starts a session for any issue that passes every check, so before you change the file, list which issues carry both labels, and keep the kill switch of section 9 at hand. Once a real cycle has ended with exit 0 and the reason `cycle_complete`, `superclaude issue-watch status` exits 0.
 
-The cron entry is follow-up FU-2 and this work does not enable it. Its schedule is `"0 */5 * * * *"`: six fields, seconds first, which is every 5 minutes. FU-2 also covers a persisted `state_dir` if `$HOME` is not persistent.
+### 8.7 Install the cron entry (FU-2)
+
+Only after section 8.6, install the cron entry for `superclaude issue-watch once`, adding `--config <path>` when the configuration file is not at the default path. Its schedule is `0 */5 * * * *`: six fields, seconds first, every 5 minutes at second 0; use the scheduler chosen in section 7 with that six-field interpretation. This work does not install or enable the entry.
+
+Before installing it, run `superclaude issue-watch check-config` and confirm that the `state_dir` it prints is on storage that survives a workspace restart, as tested in section 8.3. If `$HOME` is not persistent, set `state_dir` in the configuration file to an absolute path on persistent storage and repeat that check before scheduling anything. After the first scheduled cycles, run `superclaude issue-watch status` and confirm it exits 0.
 
 ## 9. The kill switch
 
@@ -679,3 +683,19 @@ None of these is built by this work.
 ### 15.4 Coder#477
 
 > Option A makes IronbellyOrg/Coder#477 unnecessary unless B or C is revisited. Options B and C, and Coder#477, return only on a revisit condition: the workspace cannot run a reliable cron, or one poller per login becomes unworkable.
+
+## 16. Rollout checklist
+
+Every item below is run by the owner; nothing in the implementation runs any of it.
+
+- Complete the [pre-flight checks (section 1)](#1-pre-flight).
+- Create the [configuration (section 2)](#2-the-configuration-file) with `enabled: false`.
+- Prepare the [approvers file (section 3)](#3-the-approvers-file), [labels (section 4)](#4-label-setup) and [`init-state` (section 5)](#5-create-the-state-and-re-approve-earlier-issues).
+- Perform the [live test (section 14.1)](#141-the-live-test-follow-up-fu-1) using the [capture sheet (section 14.1.1)](#1411-capture-sheet), then commit the [live-test record (section 8.5)](#85-the-live-test-record).
+- Replace the fixtures with the [captured replies (section 14.1.1)](#1411-capture-sheet) and confirm `uv run pytest tests/issue_watch/` passes, as required by the [live-test gate (section 14.1)](#141-the-live-test-follow-up-fu-1).
+- Complete the [24-hour shadow run (section 7)](#7-shadow-rollout) and [review it (section 8.1)](#81-review-the-shadow-run).
+- Pass the [two-process lock test (section 8.2)](#82-two-process-lock-test).
+- Pass the [state-directory restart test (section 8.3)](#83-the-state-directory-survives-a-restart).
+- Verify the [staleness alert (section 8.4)](#84-the-staleness-alert).
+- Only then [set `enabled` to `true` (section 8.6)](#86-set-enabled).
+- Install the [cron entry (section 8.7)](#87-install-the-cron-entry-fu-2).

Full new evidence file: .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/artifacts/t4-checklist-check.log (read current contents).
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
