FINAL: pass

Package P = /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618
S = /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts
R = /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-results.md
RB = /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-runbook.md
RT = P/artifacts/retries   (second archive attempt; fresh reviewer, FINAL-review-1.md used only as context)

== How I checked
- State: `archive_workspace.py --print-state` (read-only) returns 45ecf4b860b00c00af3fea913ea8b253602f02f9808280f2e929daeaf549a53b, equal to /tmp/final-state-1.json; the helper accepted the whole ledger. The delivery files are therefore byte-identical to those of the first FINAL.
- Ran S/selftest.sh on a git-initialised copy of the scripts, runbook, fixtures, plan and orca_worktree.py under /tmp/fr2/repo: rc 0, `SELFTEST_OK`, 386 OK, 0 FAIL. `bash -n` passes on all 20 scripts.
- Re-read every cited delivery span below. Extracted every runbook `text` block myself (RB 228-472 and 536-697) and compared with S/prompts: p01-p17 and g01-g09, 26 of 26 equal. Marker `[sc-launch:v1:` is only in S/prompts/p10-llnobind.txt; no prompt file starts with it.
- Live read-only checks: PR 654 CLOSED (base master, IronbellyOrg/IronClaude); issues 642-645 and 593-596 CLOSED; title search "ob-442 disposable in:title" returns exactly those eight; `orca worktree list` has no issue-642..645; /tmp/ob absent; `git status --short src tests` empty. Secret regex of evidence.sh over P/artifacts/ob-logs: only the words `task-id`/`task-notification` (sk- inside "task-"), no secret.

== (1) Saved prompts (qa.md "FINAL derived test", "Defective saved prompt")
- Built a regex from the qa.md template (seven slots free; every other non-blank line, word and space fixed; only blank lines and trailing whitespace tolerant) and ran it over every saved prompt in RT/T*/prompt-*.md: 20 of 20 match, none differs by a changed, added, removed or reordered non-blank line. Each of the eight re-review prompts (T1 prompt-1-3, T2 2-3, T3 3-4, T4 4-3, T5 2-2 and 3-3, T6 1-3, T9 3-2) matches, and so do the untouched ones (T1 1-1, T2 2-1, T3 3-1, T5 1-1, T6 1-1, T7 1-1, T8 1-1, T9 1-1, T10 1-1..1-3, T11 1-1). Negative control: the same regex rejects 10 of the 11 superseded prompts (T4-prompt-4-1 matches the template but carries the wrong start sha, which is why it was moved).
- Line 1 of every saved prompt equals the task's start sha of the ledger, and the "Start sha:" slot equals line 1 (T4: ce29bcda4f5cb5efdd9b720f7e78c81cd1f36e63, progress.md:13; T10 prompts carry the second start line, progress.md:34). Each template marker line (Review one task..., Do not trust..., First mark..., Anchor rule, You are not given..., Do not write sev=) appears once per prompt (no slot spill). The delta, earlier-findings and re-check slots of the eight re-review prompts are empty.
- Superseded prompts: 11 files in P/artifacts/superseded-prompts/ with original mtimes (moved unchanged), a README.md naming each file, old path, the FINAL line (progress.md:41) and the replacing prompt. Folders (P, artifacts, superseded-prompts, retries) are real directories, no symlink under artifacts. Each re-review uses the next unused j of its k (T1 1-3, T2 2-3, T3 3-4, T4 4-3, T5 2-2 and 3-3, T6 1-3, T9 3-2) and each of those tasks has a complete line after the FINAL line: T1 progress.md:43, T2 :48, T3 :51, T4 :44, T5 :54, T6 :57, T9 :45. Rule met.

== Per-task acceptance criteria (end state)
T1 (all met)
- AC1 bash -n clean; selftest prints SELFTEST_OK, rc 0 (my run; P/artifacts/t1-selftest.txt:12-13).
- AC2 S/lib-selftest.sh:21-23 (--repo pinned) and :40-44 (api repos/SuperClaude-Org/x refused, stub log absent); S/lib.sh:42-85.
- AC3 S/lib-selftest.sh:58-64 (value with spaces round-trips; awk read, no eval); S/lib.sh:29-40.
- Recovery review RT/T1/review-recovery-1-3.md: no blocking finding.

T2 (AC1-AC3 met; two owner-accepted defects remain)
- AC1 S/setup-selftest.sh:40-42 (layout), :47-50 (rerun refused, --resume rc 0); S/setup.sh:17-20.
- AC2 S/setup-selftest.sh:32-33 and :66-75 (fake HOME/.claude listing and md5 identical before and after).
- AC3 S/setup-selftest.sh:57-59 (probe, tree, settings diffed with RB 62-86, 97-110, 121-136; still valid, those lines sit above the T9 edit).
- Accepted by the Ruling at progress.md:47 (owner, 2026-11-19): S/setup.sh:41-42 (`|| true` then `rc=$?` always 0 for `gh --version`) and S/setup.sh:157-158 (comment says the push continues if the hook exec target is missing; false). Both are still present, unchanged; recovery review RT/T2/review-recovery-2-3.md F1.1 and F1.2. F1.3 is all-no.

T3 (AC1, AC3-AC6 met; AC2 unmet in its self-test only, accepted)
- AC1 S/driver-selftest.sh:26-29 stop, :33-37 blocked, :47-50 idle, :54-56 timeout, :59-65 NEEDS_INPUT (nothing sent); S/driver-helpers.sh:17-49.
- AC2 code refuses before any orca call (S/driver.sh:53, :21-26), but S/driver-selftest.sh:74-78 checks only the exit code and sent.txt (terminal send calls only), so "without calling orca" is not shown. UNMET in the self-test; accepted by the Ruling at progress.md:50.
- AC3 S/driver-selftest.sh:39-44 (old `Blocked: first` on screen: timeout, not blocked).
- AC4 S/driver-selftest.sh:80-126 (notice answered; pending when the notice never arrives, is a non-notice prompt, or is stale); S/driver-helpers.sh:51-57.
- AC5 S/driver-selftest.sh:131-134; S/driver.sh:101-112.
- AC6 P/artifacts/t3-orca-help.txt:1 (send), and read, wait, create, list sections.
- Accepted by the same Ruling, all still as recorded: empty event count when no probe log exists (S/driver.sh:59, S/driver-helpers.sh:22,38); `screen <name>` takes no file argument (S/driver.sh:92-95) and names files `<name>-HHMMSS-<n>.json` (S/driver.sh:17), unlike the task text.

T4 (all met)
- AC1 S/session-a-selftest.sh:36 and :52 (17 blocks, 0 differing); my own extraction agrees.
- AC2 S/session-a-selftest.sh:79 (order-full) and :103 (PENDING at a scripted NEEDS_INPUT); the three item-5 prompts use wait-notice.
- AC3 S/session-a-selftest.sh:59-60; grep: marker only in S/prompts/p10-llnobind.txt.
- RT/T4/review-recovery-4-3.md: six findings, all four answers `no`; recorded in RT/T4/notes.md:2-7 (progress.md:44 token notes@:1-7).

T5 (AC1, AC2 met; AC3 unmet, accepted; one deviation accepted)
- AC1 S/setup-github-selftest.sh:93 (four creates, --repo, --body-file), :116 (rerun adds none); S/setup-github.sh:16-17, :32.
- AC2 S/setup-github-selftest.sh:137 (generated settings equal the RB:197 generator), :167 (EXISTS refusal); S/setup-github.sh:128-137.
- AC3 "read from the claim screen ... scripted screen records WT_T1": UNMET. S/setup-github.sh:111-122 reads `.path` from `orca_worktree.py worktree` JSON; S/setup-github-selftest.sh:125 records WT_T1 through a stub `uv`; no scripted-screen case. Accepted by the Ruling at progress.md:42 (owner, 2026-11-19); current outcome matches that Ruling's wording.
- Accepted by the Ruling at progress.md:53: claim session command is `env -u CLICKUP_API_TOKEN claude --settings $OB/settings-claim.json` (S/setup-github.sh:72), not the literal command in the task text.

T6 (all four AC met; one deviation accepted)
- AC1 S/session-gov-selftest.sh:324 (upstream PR URL: FAIL misrouted-pr, rc 5) and :333 (push URL lie: REFUSED push prompt, rc 6); S/session-gov.sh:443-446, :459-462.
- AC2 S/session-gov-selftest.sh:176 (foreign GSID pair refused); S/session-gov.sh:206-210 (paths must equal this GSID or GSID.ok; `rm -f`, absent target released).
- AC3 S/session-gov-selftest.sh:140 (b, c need item 5; d, e need 5 and 1); S/session-gov.sh:35-42.
- AC4 S/session-gov-selftest.sh:376 and my own cmp over RB 536-697: g01-g09 equal.
- Accepted by the Ruling at progress.md:56: when the claim output has no terminal key the handle is found with `orca terminal list` (worktree path and sc-launch title, exactly one match) before the stop for the operator (S/session-gov.sh:173-183).

T7 (all met)
- AC1 S/evidence-selftest.sh:63 (12 blocks; missing log reads pending). AC2 :80 and :84 (bare `Approved!` gives item 5 FAIL; wrong or missing parent gives item 1 FAIL). AC3 :103 (F1-F8 equal RB 505-520). AC4 :184 and :193 (ghp_ and Bearer stop the copy; value not in the report). AC5 :171 (rerun gives the same file).

T8 (all met)
- AC1 S/cleanup-selftest.sh:101 (apply order), plan-* cases (plan calls nothing). AC2 :127 (foreign entry skipped), :141, :148 (step 7 refused). AC3 :165 (key unset only for worktreeConfigPre=unset), :171 (SKIP for absent PR and issues). AC4 :178 (gated run, 8 steps). AC5 :103 (gh pinned).

T9 (all met)
- AC1 `grep -n 'not representative' RB` and `grep -n 'must be.*typed by a person' RB` print nothing (rc 1); `grep -c 'orca terminal send' RB` = 1 (RB:765); RB:764-769 carry the new wording; section 6 at RB:837-860 names every script file (my check and runbook-selftest); handoff paragraph at /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/handoff-runbook.md:63.
- AC2 selftest.sh prints SELFTEST_OK (my run, includes S/runbook-selftest.sh).

T10 (AC1 and AC4 met; AC3 met except the accepted issue-count deviation; AC2 see note N1)
- AC1 R has 12 item blocks (R:19,44,68,96,151,204,237,262,317,348,477,544); every PASS (items 1, 3, 4, 5, 9, OB-CTX) carries an evidence command and log lines or a screen. I re-read P/artifacts/ob-logs/logs/h1.jsonl lines 6 and 11: PreToolUse Bash rows with agent_id afec0ca3385c21677 and a85b8013a874ad75a and session_id equal to the session-A SessionStart (R:24-37).
- AC2 ob-logs exists and passes the scan (my grep: no secret); P/artifacts/t10-run-log.md:12-14 and :43 hold the dialog answers with reasons; exit codes in :2-72 and :74-86.
- AC3 R:10 holds https://github.com/IronbellyOrg/IronClaude/pull/654 (live: CLOSED, base master). "lists exactly four issues" is NOT met: the search lists eight (593-596 accidental first set, 642-645 this run), recorded at R:14 and run-log:83-85; accepted by the Ruling at progress.md:39. Claim screens (2827 `claim-*.json`) mention only issues 642-645.
- AC4 R:17 states the OB-H2 FAIL and the section 3 consequence at the top.
- Accepted wording (same Ruling): R:527 and R:540 say the tab shows one guard line in a tool box and not the guard's Blocked:/Why:/You can: lines; verified against P/artifacts/ob-logs/screens/gB-190650-5.json:4-5 (the line wraps onto "worktree."). Matches the Ruling.

T11 (all met)
- AC1 P/artifacts/t11-cleanup.txt:3,13,14,19,27,32,37,39 (steps 1-8), plan at t11-cleanup-plan.txt:36; PR lines at :20-21 show a real close, so no SKIP is due. AC2 :33-37 both diffs "(none)"; /tmp/ob absent. AC3 live PR 654 and 642-645 CLOSED. AC4 live worktree list shows none of issue-642..645. AC5 package staged except progress.md ("AM") and artifacts/retries/ledger-repair-2.md ("??"); see N3.

Plan Constraints: no breach found. gh only through gh_fork (no bare `gh pr|issue|api|repo` in S/*.sh outside self-test text); no `--issue`/`--pr` in S/*.sh or orca_worktree.py; no `gh pr merge`; no src/ or tests/ change; no bare python; marker only at LL-NOBIND; claim session starts with `env -u CLICKUP_API_TOKEN claude` (plus --settings, accepted); all executable scripts have `set -u -o pipefail` and `umask 077` (lib.sh and driver-helpers.sh are sourced); only `printenv CLAUDE_CONFIG_DIR` is printed, no env dump. The literal "every external call bounded by timeout" is not met for local helpers (cp, grep, ls, sleep), a note since the first task reviews.

== (2) Rulings: current outcome vs recorded acceptance
T5.AC3 (progress.md:42), T2 (:47), T3 (:50), T5 claim command (:53), T6 (:56), T10 (:39): in each case the file lines the Ruling names still hold the accepted behaviour, and the unmet AC is cited above, not marked met. Every confirmed-blocking finding of the eight recovery re-reviews (RT/T2/review-recovery-2-3.md F1.1 F1.2; RT/T3/review-recovery-3-4.md AC2, F2.1, F3.1, F3.2; RT/T5/review-recovery-2-2.md F1.1 F1.2 and review-recovery-3-3.md F1.1; RT/T6/review-recovery-1-3.md F1.1) is named in a Ruling. T1, T4, T9 recovery reviews: no blocker. No new or changed unaccepted gap found. The delivery files did not change since the first FINAL.

== (3) Ledger repairs
- ledger-repair-2.md: /tmp/progress-before-rulings.md (45 lines) is an exact prefix of the current progress.md, so nothing before the rewrite was altered. Only the four Ruling-first appends were redone as blocked, Ruling, complete; the blocked lines carry the recovery verdicts (T2, T3, T5 missing, T6 extra) and are followed at once by the Ruling and an unchanged complete line. Hides nothing.
- retries/T10/ledger-repair.md: /tmp/progress-before-fix.md lines 1-35 and the Ruling (line 39) are identical to now. Verdicts unchanged (T10 blocked and complete stay `missing`; T11 `compliant`). Changed: end-state evidence pointers on lines 36-40, AC4 added to the evidence, extras=/files= added. Slightly understated in the note: old line 40 already had extras=none and files=; old line 38 also lost its prose ("one open blocking finding F2.3 ... wording since corrected ... not re-reviewed"), which now lives only in RT/T10/review-3.md and the T10 Ruling. Nothing that fails was hidden.

== Findings
Blocking: none.

Notes (every answer `no`; not issues):
N1 T10.AC2 "every script run with its exit code": P/artifacts/t10-run-log.md:81 says several 2026-11-17 runs (evidence.sh at 15:17 and later reruns) have no recoverable exit code. All runs of the delivered 2026-11-18 rerun carry a code (run-log:41-72, 74-80, 86). RT/T10/review-3.md judged AC2 met with this disclosure. This gap is NOT named in the T10 Ruling and I do not call AC2 fully met; it is not new or changed since the first FINAL and the log states it honestly, so I do not turn it into a blocker. The owner can add it to the Ruling if wanted.
N2 Protocol deviation, harmless at the end state: for T2, T3, T5, T6 the recovery wrote a `blocked` line before the Ruling and complete (to satisfy the archive helper), where qa.md "Defective saved prompt" says a re-review blocker appends no `blocked` line. Each is followed at once by Ruling and complete; the helper accepts the ledger.
N3 progress.md is "AM" and RT/ledger-repair-2.md is untracked; run `git add .dev/tasks` after the last ledger write (staging only).
N4 Paperwork: the Ruling at progress.md:53 cites review-recovery-3-3.md F1.2 for the claim command; in that file it is F1.3 (all no), and F1.2 is a weak self-test; the constraint finding is review-recovery-2-2.md F1.2. Also notes files RT/T6, T7, T8 notes.md have a finding on line 1 instead of the start sha, RT/T11/notes.md is a raw review dump, and the review-recovery-*.md files carry no start-sha header; by the qa.md first-line rule those count as absent. All their findings have all-no answers, so no unmet AC or constraint depends on them.
N5 T5.AC3's acceptance (progress.md:42) precedes the later T5 blocked line (:52) in file order; the Ruling at :53 names only the claim command, but the owner's "Accept the Task 2, 3, 5 and 6 gaps" covers all T5 gaps and the same finding F1.1 was re-raised in review-recovery-3-3.md. No action needed.
N6 S/session-gov.sh:202-204 releases this run's own two session files (named from GSID) when the claim text prints no `rm` line; it logs `release-text FAIL ... UNVERIFIED`. Paths are still restricted to GSID and GSID.ok, so AC2 holds.
N7 session-a2.sh was not run in Task 10 (run-log:30, :40); OB-H1 item 7 stays pending, not required by any AC. Other disclosed deviations match R: item 2 and 6 pending, item 8 FAIL, OB-H2 FAIL (verbatim-detail check only), OB-H3 pending.

Return: FINAL pass.
