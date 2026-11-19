4bf8f84e56b01a644fcb81014084a87af9447026
Review one task for spec compliance.

Task brief: Task 6 of plan .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md (read it, lines 137-171). Deliverable: .dev/issues/442/scripts/session-gov.sh with subcommands b, c, d and e for runbook section 2.2.1 to 2.2.4 (.dev/issues/442/observation-runbook.md lines 536-697), prompt files copied byte for byte into .dev/issues/442/scripts/prompts/ (g01 to g09), and the self-test .dev/issues/442/scripts/session-gov-selftest.sh registered in selftest.sh. AC ids: T6.AC1 = "With the stub `orca` and `gh` and scripted screens, the self-test shows session `e` refusing the push prompt when the push URL is not `/tmp/ob/bare-push.git`, and refusing a pull request URL outside `IronbellyOrg/IronClaude`."; T6.AC2 = "The self-test shows the release step refusing an `rm` path that is not this run's `GSID` or its `.ok` file, and treating an already-absent target as released."; T6.AC3 = "The self-test shows `b` and `c` refusing to start when item 5 is not PASS, and `d` refusing when item 1 is not PASS."; T6.AC4 = "Every prompt file matches its runbook `text` block byte for byte (a self-test diff over lines 536-697)."

Global constraints: plan lines 17-27 (read them). Key: the owner authorization covers governed claims on the four disposable issues only, and only when a later authorized run executes the scripts; nothing in this task may run live; every gh call via gh_fork (--repo pinned, api path repos/IronbellyOrg/IronClaude/...); nothing targets SuperClaude-Org; no Orca --issue/--pr link flags; uv only; every external call timeout-bounded; set -u -o pipefail umask 077; scratch under /tmp/ob (OB overridable); no src/ or tests/ changes; settings, hook, git config and launch-store changes only from the driving agent's own shell (LL-TAMPER); no prompt starting [sc-launch:v1:.

Start sha: 4bf8f84e56b01a644fcb81014084a87af9447026

Diff against the start snapshot: new files, read in full: .dev/issues/442/scripts/session-gov.sh, .dev/issues/442/scripts/session-gov-selftest.sh, the nine prompt files .dev/issues/442/scripts/prompts/g01-b-implement.txt, g02-commit.txt, g03-approved.txt, g04-gov-bg.txt, g05-gov-det.txt, g06-gov-clear.txt, g07-c-implement.txt, g08-e-push.txt, g09-e-merge.txt; changed: .dev/issues/442/scripts/selftest.sh (one registration line for the new self-test). Helpers it uses and that you may read for grounding: .dev/issues/442/scripts/lib.sh, driver.sh, driver-helpers.sh. The saved run log is .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t6-selftest.txt (read it). Runbook grounding: .dev/issues/442/observation-runbook.md lines 536-697 and 718-726; the claim result shape is in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py (launch_result, session_report, find_handle, record_launch).

Delta diff from the previous reviewed tree (rebuilt from the fix pass edits; paths under .dev/issues/442/scripts/):

session-gov.sh
- launch_real signature comment now reads: launch_real <T1..T4> <flags> <session name> [first-stop wait secs; absent or 0 = do not wait]
- last line of launch_real changed:
-   wait_first_stop "$label" "${OB_INITIAL_WAIT_S:-900}" || pending "reason=no-first-stop label=$label"
+   # b and c wait for the plan boundary; d and e own longer waits of their own
+   [ "${4:-0}" = 0 ] || wait_first_stop "$label" "$4" || pending "reason=no-first-stop label=$label"
- run_b: launch_real T1 "--pipeline worktree" gB  ->  launch_real T1 "--pipeline worktree" gB "${OB_INITIAL_WAIT_S:-900}"
- run_c: launch_real T2 "--pipeline worktree" gC  ->  launch_real T2 "--pipeline worktree" gC "${OB_INITIAL_WAIT_S:-900}"
- run_d and run_e calls unchanged (no fourth argument, so no first-stop wait)
- fire_o10: local list gains wtbr; after the "no head branch" check:
+   wtbr=$(tgit -C "$WT4" rev-parse --abbrev-ref HEAD 2>/dev/null)
+   if [ "$br" != "$wtbr" ]; then
+     rec e-o10 FAIL "pull request $num head branch $br is not the T4 worktree branch ${wtbr:-unknown}; no write made"
+     state_set O10 skipped; return 0
+   fi

session-gov-selftest.sh
- stub orca: the Stop-appending loop honours STUB_STOP_ONLY=<label> (only that log gets a Stop)
- stub gh: pr view prints ${STUB_PR_BRANCH:-ob-442-t4-branch}
- mkenv: the T4 test worktree is checked out on branch ob-442-t4-branch
- new case group 9b: e5, head branch some-other-branch gives "FAIL e-o10 pull request 77 head branch some-other-branch is not the T4 worktree branch ob-442-t4-branch", no PUT, run ends SESSION_E_DONE
- new case group 9c: d3 (d reaches its own 90-minute wait, no no-first-stop), e6 (e reaches PENDING cycle-not-ended, no no-first-stop), c4 (c still stops with PENDING reason=no-first-stop label=h2-T2); all with STUB_STOP_ONLY=claim

Earlier blocking findings of this start (empty on the first review):
F6.1 sev=blocking trigger=B4 ac=scope at=.dev/issues/442/scripts/session-gov.sh:154 anchor="It waits up to 90 minutes for the agent's final `git status --short`, then sends the commit prompt." chk=amiss:n,false:n,harm:n,constraint:y family=first-stop-gate fix="launch_real takes the first-stop wait as an optional fourth argument; b and c pass it, d and e do not" first=A1 origin=new: launch_real ended every session with PENDING no-first-stop after 900 s, which cut d's 90-minute wait and e's cycle wait short
F6.2 sev=blocking trigger=B3 ac=scope at=.dev/issues/442/scripts/session-gov.sh:334 anchor=.dev/issues/442/scripts/session-gov.sh:334 chk=amiss:n,false:n,harm:y,constraint:n family=o10-target fix="compare the pull request head branch with the T4 worktree branch before the PUT; otherwise record FAIL and write nothing" first=A1 origin=new: the contents-API PUT targeted the first pull request URL found anywhere in the h2-T4 log

Saved-probe re-check hit locations (may be empty): the saved probes were re-run over session-gov.sh and session-gov-selftest.sh; current hits (file:line, session-gov.sh lines unprefixed after line 11): session-gov.sh:96 wait_first_stop definition; :134 launch_real definition; :155 the optional wait; :234 and :270 (b, c pass OB_INITIAL_WAIT_S); :300 and :355 (d, e pass nothing); session-gov-selftest.sh:129, 294, 300, 306 (OB_INITIAL_WAIT_S uses); session-gov.sh:314 find_pr_url; :328 fire_o10; :330 gh_fork pr view; :338 gh_fork api read; :341 gh_fork api PUT (the only write); :359 and :365 callers.

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
