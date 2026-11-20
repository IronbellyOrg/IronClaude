FINAL: issues

Package P = /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618
S = /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts
R = /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-results.md
RB = /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-runbook.md
RT = P/artifacts/retries

How I checked: read the plan, whole ledger, every delivery file in /tmp/final-state-1.json, the T10/T11 logs, ob-logs and retries. Ran selftest.sh on a copy of the scripts, runbook, fixtures and plan under /tmp/fr (git-initialised): SELFTEST_OK, 386 OK, 0 FAIL (a first run in a copy without .git failed only in session-a2 because main_checkout needs git; not a defect). Live read-only checks: gh pr view 654 = CLOSED (base master); issues 642-645 and 593-596 = CLOSED; the title search returns all eight; orca worktree list has no issue-642..645; /tmp/ob is gone; src/ and tests/ unchanged (git status shows only .dev/). Independent byte checks of the 17 p*.txt prompts (RB 228-472) and 9 g*.txt prompts (RB 536-697) against the runbook text blocks: all equal. Secret regex of evidence.sh over P/artifacts/ob-logs: no hit (only "task-" words). Saved prompts were compared with the qa.md template by a regex built from the template (slots free, all other words and lines fixed, whitespace-tolerant).

== Per-task acceptance criteria

T1 (all met)
- AC1 bash -n clean on lib.sh and selftest.sh (all 20 scripts pass bash -n); selftest.sh prints SELFTEST_OK, exit 0 (my run; P/artifacts/t1-selftest.txt:12-13).
- AC2 S/lib-selftest.sh:21-31 (--repo pinned), :40-44 (api repos/SuperClaude-Org/x refused, stub not reached); S/lib.sh:42-85.
- AC3 S/lib-selftest.sh:58-64 (value with spaces, awk read, no eval; S/lib.sh:29-40).

T2 (all met)
- AC1 S/setup-selftest.sh:40-42 (layout), :47-50 (rerun refused, --resume passes); S/setup.sh:17-20.
- AC2 S/setup-selftest.sh:66-75 (fake HOME/.claude listing and digests equal before and after).
- AC3 S/setup-selftest.sh:57-59 (probe, tree, settings equal RB lines 62-86, 97-110, 121-136; still true after the T9 edit because those lines sit above the edited region).

T3 (all met)
- AC1 S/driver-selftest.sh:26-65 (stop, blocked, idle, timeout, NEEDS_INPUT, nothing sent).
- AC2 S/driver-selftest.sh:73-78 and S/driver.sh:21-26,53.
- AC3 S/driver-selftest.sh:39-44.
- AC4 S/driver-selftest.sh:80-126 (late notice answered, pending, none, non-notice, stale); S/driver-helpers.sh:51-57.
- AC5 S/driver-selftest.sh:128-134; S/driver.sh:101-112.
- AC6 P/artifacts/t3-orca-help.txt:1,27,42,77,107 (send, wait, read, create, list).
- Note: S/driver.sh gained esc, fire and raw subcommands during T10; they do not weaken any AC.

T4 (all met, except the saved-prompt defect F1)
- AC1 S/session-a-selftest.sh:33-52 (17 blocks, 0 differing); my independent extraction agrees.
- AC2 S/session-a-selftest.sh:62-96 (order, counts, PENDING at NEEDS_INPUT).
- AC3 S/session-a-selftest.sh:54-60; grep shows only prompts/p10-llnobind.txt holds sc-launch:v1:, and no prompt file starts with it.

T5 (AC1, AC2 met; AC3 UNMET at the end state, see F2)
- AC1 S/setup-github-selftest.sh:92-102 (4 creates, --repo, --body-file, rerun adds none).
- AC2 S/setup-github-selftest.sh:130-138 (settings equal the line-197 generator), :154-169 (EXISTS refusal); S/setup-github.sh:126-139.
- AC3 "worktree paths are read from the claim screen ... a self-test case with a scripted screen records WT_T1": not true now. S/setup-github.sh:111-122 reads the path from the JSON of `orca_worktree.py worktree`, and S/setup-github-selftest.sh:120-127 uses a stub `uv`, not a scripted screen.

T6 (all met, except the saved-prompt defect F1)
- AC1 S/session-gov.sh:431-465 (push URL re-check inline), :443-446 (misrouted PR, exit 5); selftest cases e-misrouted-*, e-pushurl-* (all OK in my run).
- AC2 S/session-gov.sh:193-211 (rm paths must equal this GSID or GSID.ok; rm -f makes an absent target released).
- AC3 S/session-gov.sh:42 (b,c need item 5; d,e need items 5 and 1).
- AC4 prompt files equal RB text blocks in 536-697 (my independent cmp: 9 of 9).

T7 (all met)
- AC1 S/evidence-selftest.sh:59-68 (12 blocks, pending without logs).
- AC2 S/evidence-selftest.sh:78-87 (bare Approved! gives FAIL for item 5; wrong or missing parent session gives FAIL for item 1).
- AC3 S/evidence-selftest.sh:99-104 (F1-F8 equal RB 505-520).
- AC4 S/evidence-selftest.sh:179-195 (ghp_ and Bearer stop the copy; the value is not in the report).
- AC5 S/evidence-selftest.sh:168-172 (rerun gives the same file).

T8 (all met)
- AC1 S/cleanup-selftest.sh:85-99; AC2 :125-148; AC3 :152-171; AC4 :174-182; AC5 :99-101. S/cleanup.sh:195-198 runs steps 1-8 in order, step 4 before step 5.

T9 (all met)
- AC1 `grep -n 'not representative' RB` and `grep -n 'must be.*typed by a person' RB` print nothing (rc 1); `grep -c 'orca terminal send' RB` = 1 (RB:765); section 6 at RB:837-860 names every file in S (my loop: none missing); handoff paragraph at /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/handoff-runbook.md:63.
- AC2 selftest.sh prints SELFTEST_OK (my run), including S/runbook-selftest.sh.

T10 (AC1, AC3, AC4 met with the accepted deviations; AC2 partly unmet, see N1)
- AC1 R has 12 "## " blocks (R:19,44,68,96,151,204,237,262,317,348,477,544). Every PASS has a command and log or screen: item 1 R:24-37 (rows h1.jsonl lines 6 and 11, I re-read them: PreToolUse Bash with agent_id afec0ca3385c21677 and a85b8013a874ad75a); items 3, 4, 5, 9 R:73-89, 98-149, 153-200, 319-346; OB-CTX R:549-752 (gov-log-reconstructed.txt equals the rows in P/artifacts/ob-logs/session-output/*.out for b-id-*, b-ctx-released, b-implement-ok, b-approved-no-unlock, b-inode). Header hashes R:8 equal the live sha256sum now.
- Accepted item (a), wording: R:527 and R:540 now read "one guard line in a tool box ... the guard's Blocked:, Why: and You can: lines are not shown" and "the line wraps onto the next row, which reads worktree."; I checked P/artifacts/ob-logs/screens/gB-190650-5.json:7-8 (guard line wraps onto "worktree."). This matches the Ruling at P/progress.md:39. Unmet-but-accepted: F2.3 of P/artifacts/retries/T10/review-3.md was never re-reviewed after the rewording.
- AC2 secret scan part met (my grep, no hit). Dialog answers with reasons at P/artifacts/t10-run-log.md:12-14,43. Exit codes: see N1.
- AC3 R:10 PR URL https://github.com/IronbellyOrg/IronClaude/pull/654 (live: CLOSED, base master). Issue count: the title search lists eight (593-596, 642-645), not four. Accepted deviation (b) of the Ruling, recorded at R:14 and P/artifacts/t10-run-log.md:83-85; the "exactly four" clause is NOT met and I do not mark it met. No other issue was claimed or commented on (review-2 checked 2827 claim screens; I found nothing contrary).
- AC4 R:17 states the OB-H2 FAIL and the section 3 consequence. OB-H3 is pending, OB-CTX is PASS.

T11 (all met)
- AC1 P/artifacts/t11-cleanup.txt:3,13,14,19,27,32,37,39 (steps 1-8), PR steps show a closed PR (:20-21) so no SKIP is due; plan at P/artifacts/t11-cleanup-plan.txt:36 CLEANUP_PLAN_DONE; apply ends CLEANUP_DONE at :40.
- AC2 t11-cleanup.txt:33-37 (both diffs "(none)"); /tmp/ob absent now.
- AC3 live: PR 654 CLOSED; 642, 643, 644, 645 CLOSED.
- AC4 live `orca worktree list` shows none of issue-642..645; t11-cleanup.txt:15-19.
- AC5 package staged except progress.md ("AM") and artifacts/retries/T10/ledger-repair.md ("??"); see N3.

Plan Constraints: no breach found. gh calls all go through gh_fork (grep: no bare gh); no Orca --issue or --pr in the scripts or in orca_worktree.py; no gh pr merge; no src/ or tests/ change; no prompt starts with the marker and only p10-llnobind.txt holds it; the claim session starts with `env -u CLICKUP_API_TOKEN claude --settings ...` (S/setup-github.sh:72); headers set -u -o pipefail and umask 077 in all 18 executable scripts (lib.sh and driver-helpers.sh are sourced). The literal "every external call bounded by timeout" is not met for local helpers (rm, cp, grep, ls, pgrep, sleep); reviewers treated this as a note since T1 (P/artifacts/retries/T3/notes.md F3.5), and I do the same.

== Findings (blocking)

F1 [blocking, FINAL derived test, saved prompts] Ten saved prompts differ from the qa.md "Subagent prompt" template outside the slots by more than blank lines or trailing whitespace. There is no superseded-prompts/ folder and no later template-exact prompt for these reviews, so nothing marks them history. Differences (all paths under RT):
 - T1/prompt-1-2.md:12 label reads "Delta diff from the previous reviewed tree: the fix-pass diff ..." (template: "... (empty on the first review): ").
 - T2/prompt-2-2.md:3 an added non-template line "REVIEW RE-RUN (r2-2) after the A2 fix pass ... Earlier blocking findings of this start:" before "Review one task for spec compliance." (line 4); lines 27-28 repeat "Do not trust the implementer's report." (the second may be slot spill).
 - T3/prompt-3-2.md:3 same kind of added line ("REVIEW RE-RUN (r3-2) ..."); lines 23-24 repeat "Do not trust ...".
 - T3/prompt-3-3.md: the first template line "Review one task for spec compliance." is absent (line 2 blank, line 3 "Task brief: ..."); :11 "Delta diff from the previous reviewed tree: ..." and :13 "Earlier blocking findings of this start:" lost their "(empty on the first review)".
 - T4/prompt-4-2.md:3 added line "REVIEW RE-RUN (r4-2) ..."; lines 24-25 repeat "Do not trust ...".
 - T5/prompt-2-1.md:3 added line "REVIEW RE-RUN (r5-2) ..."; lines 23-24 repeat "Do not trust ...".
 - T5/prompt-3-1.md: first template line absent; :11 and :13 labels changed as in T3/prompt-3-3.md.
 - T5/prompt-3-2.md: first template line absent; :11 "Delta diff from the previous reviewed tree (the repair-round fix applied after the A3 review; ...):" replaces the template label.
 - T6/prompt-1-2.md:12 "Delta diff from the previous reviewed tree (rebuilt from the fix pass edits; ...):" replaces the template label.
 - T9/prompt-3-1.md:2 reads "Review one task for spec compliance (attempt 3, rebuilt from the start snapshot)." instead of the template line.
 Template-exact (full regex match): T1/1-1, T2/2-1, T3/3-1, T4/4-1, T5/1-1, T6/1-1, T7/1-1, T8/1-1, T9/1-1, T10/1-1..1-3, T11/1-1.
 Fix: run the "Defective saved prompt (recovery)" of qa.md for T1, T2, T3, T4, T5, T6, T9: re-review with a template-exact prompt saved as the next unused j of the same k, then move the defective prompts unchanged to P/artifacts/superseded-prompts/ with a README.md. A re-review blocker goes into the FINAL evidence and the summary.

F1b [blocking, same rule, line 1] RT/T4/prompt-4-1.md:1 and RT/T4/prompt-4-2.md:1 (and their "Start sha:" slot) hold ce29bcda4f5cb5efdd7b720f7e78c81cd1f36e63, but the ledger start line (P/progress.md:13) is ce29bcda4f5cb5efdd9b720f7e78c81cd1f36e63. `git cat-file -t` shows the ledger sha is a tree and the saved one does not exist. Line 1 of a saved prompt must be the task's start sha. Fix: same recovery for T4 with the correct sha.

F2 [blocking, a later change contradicts an AC, B1] T5.AC3 says the worktree paths are "read from the claim screen, not guessed" and that a self-test case "with a scripted screen records WT_T1". The T10 adaptation to the rebased claim (a `--pipeline none` claim creates no worktree) replaced that: S/setup-github.sh:111-122 now runs `orca_worktree.py worktree` and reads `.path` from its JSON; S/setup-github-selftest.sh:30-64 uses a stub `uv`, and no case scripts a claim screen. The path is not guessed, but the AC as written is unmet. The ledger still shows T5 "compliant" (P/progress.md:20). The only trace of the change is P/artifacts/t10-run-log.md:6 ("adaptation to the rebased claim flow done; ... review 1 FAIL ..., re-review PASS: /tmp/t10-adapt-review.md and /tmp/t10-adapt-rereview.md"); both files are gone from /tmp, and the owner Ruling at P/progress.md:39 covers only the wording and the issue-count deviation. Fix: ask the owner for a scoped Ruling that accepts reading the worktree path from the claim's own worktree script instead of the claim screen (the claim no longer prints it), or restore a screen-based read; then a post-ruling complete line for T5.

== Findings (not blocking, for the record)

N1 T10.AC2 "lists every script run with its exit code": P/artifacts/t10-run-log.md:81 states that several runs of 2026-11-17 have no recoverable exit code (evidence.sh at 15:17 and later reruns). All runs of the delivered rerun (2026-11-18) carry a code (lines 41-72, 74-80, 86). review-3 judged AC2 met with this disclosure. Not turned into a blocker (no new or changed gap; the first-day run was cleaned up), but it is not covered by the Ruling at progress.md:39, so I record AC2 as partly unmet for the first-day runs.

N2 Ledger repair (P/artifacts/retries/T10/ledger-repair.md). I compared /tmp/progress-before-fix.md with P/progress.md. Lines 1-35 and line 39 (the Ruling) are byte-identical. Verdicts are unchanged (T10 blocked and complete stay verdict=missing; T11 compliant), so nothing that fails is hidden. But the repair is more than adding extras= and files=: (a) line 36 evidence pointers were replaced by end-state pointers (results:33 -> :19, run-log:45-70 -> :74, results:9 -> :10) and AC4 evidence was added while ac= still lists only AC1-AC3; (b) line 38 lost its text "one open blocking finding F2.3 after the third and last allowed review; wording since corrected at results:527 and :540, not re-reviewed; review loop limit reached, escalated to the owner" (the reason survives in review-3.md, the Ruling and the run log, and the old text only in /tmp); (c) line 40 changed extras=none to extras=lint:skip,typecheck:skip,test:pass and widened files= from three entries to nineteen (selftest does pass, so test:pass is true); (d) line 37 evidence ranges were narrowed to single lines. The note says the lines "lacked the extras= and files=" fields; old line 40 already had both. Also the order is odd: T11 complete (line 37) sits between two T10 blocked lines, so T11 was recorded complete while T10 was blocked (the run log says the owner go covered Tasks 10 and 11). None of this unmeets an AC. Recommend the owner knows the blocked-line explanation was dropped.

N3 T11.AC5 / staging: git status --short .dev/tasks shows the package staged except P/progress.md (AM) and RT/T10/ledger-repair.md (??). Run `git add .dev/tasks` after the last ledger write (staging only).

N4 session-a2.sh was not run in Task 10 (P/artifacts/t10-run-log.md:30 and :40: it starts Claude with the real HOME and would write a trust entry into ~/.claude.json; not approved by the owner). OB-H1 item 7 is therefore pending (R:237-259). The plan's run order lists session-a2.sh but no AC needs item 7, so this is a recorded deviation, not an unmet AC.

N5 Disclosed live deviations that match the results file: OB-H1 item 2 pending (one Skill call), item 6 pending (no TaskCreate), item 8 FAIL, OB-H2 FAIL (verbatim-detail check of the two preflight refusals only; the refusals themselves matched), OB-H3 pending (push and merge prompts not exercised because the agent refused them itself), session B typed /sc:implement took .dev/issues/642/issue-summary.md as its argument (P/artifacts/t10-run-log.md:60; not stated in R). Preconditions.txt, baseline files and gov-log.txt were lost with /tmp/ob; R:11-12 says so and the gov-log is reconstructed (ob-logs/gov-log-reconstructed.txt).

Return: FINAL issues. Blocking: F1 (+F1b) and F2.
