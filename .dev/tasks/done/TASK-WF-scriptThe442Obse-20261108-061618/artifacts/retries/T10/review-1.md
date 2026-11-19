start=dda1a4f25199cdc5db67ac3eabc337219ed51589 tree=f217b0b97308557e5c319e0f71c3e0c80ff4f013
Task 10 review 1 (start sha dda1a4f25199cdc5db67ac3eabc337219ed51589)

Paths used below:
R = /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-results.md
L = /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t10-run-log.md
OB = /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/ob-logs

## Earlier blocking findings
None were given (first review). No status lines.

## Per-AC marks

T10.AC1 unmet @R:15-751 (12 blocks present: R:15,40,64,92,147,200,233,258,313,344,473,540; each Result is PASS, FAIL or pending). Unmet because of F1.3 and F1.4.
T10.AC2 unmet @L:1-72. $PKG_ART/ob-logs exists (OB) and my own secret grep over OB found no match; the copy is made only after the scan (evidence.sh:404-412). Unmet because of F1.1.
T10.AC3 unmet @R:9-10. The PR URL is https://github.com/IronbellyOrg/IronClaude/pull/654 (R:10; gh pr view 654 shows same repository, base master, state CLOSED). The claim-session screens in OB show only issue numbers 642-645 (and the parent 442). But `gh issue list --search "ob-442 disposable" --state all` lists eight issues (593-596 and 642-645), and the default open list shows none. Unmet because of F1.2.
T10.AC4 met @R:13 ("FAIL in OB-H2: no governed claim on a real issue (runbook section 3). Report it instead." is at the top). OB-H3 is pending (R:477) and OB-CTX is PASS (R:544), so no other FAIL needs stating.

Header fields checked: claude 2.1.327, orca 1.4.245-aidev02.9cfecdd30b2a, git 2.47.3, and both sha256 values in R:5-8 equal what the live commands print now. /tmp/ob/preconditions.txt is gone, so I compared against live commands.

## Findings

F1.1 ac=T10.AC2 at=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t10-run-log.md:45-70 anchor="lists every script run with its exit code" chk=y,n,n,n family=runlog-exit-codes fix=add an exit-code line for each run that has none. In the final run these are: evidence.sh all at L:45/46/47, after B (L:59), after C (L:63), after D (L:66) and after E (L:70); setup-github.sh first run (L:48, stopped, no code); session-gov.sh b first pass (L:53, stopped, no code); the plan-only cleanup run behind t11-cleanup-plan.txt (L:70). The earlier run has the same gaps at L:17, L:19, L:26 and L:31. Use the real code or write "killed by me, no code" for a run that was stopped covers="every script run with its exit code": only some runs carry exit=N; the evidence.sh runs after sessions B, C, D and E and several stopped runs have none.

F1.2 ac=T10.AC3 at=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-results.md:9 anchor="`gh_fork issue list --search \"ob-442 disposable\"` lists exactly four issues" chk=y,n,n,n family=disposable-issue-count fix=run the list command, paste its output in the results file and the run log, and state why it shows eight issues (593-596 from the accidental 2026-11-17 run, adopted as T1-T4 and claimed and commented at L:5,33-35, closed 2026-11-17T18:42Z; 642-645 from the rerun, closed 2026-11-18T19:39Z). The AC as written cannot hold with both sets on GitHub, so either record this deviation openly or have the orchestrator reword the AC; as it stands no row records a count check and R:9 lists only 642-645 covers="lists exactly four issues": the live search with --state all returns 8 issues, the open-only default returns 0, and no check is recorded.

F1.3 ac=T10.AC1 at=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/ob-logs/logs/h1.jsonl:6 anchor=OB/logs/h1.jsonl:6 and :11 hold the two item-1 evidence rows (PreToolUse Bash with agent_id afec0ca3385c21677 and a85b8013a874ad75a); results line 33 cites "lines 2,3,4", which are the prompt, the Agent PreToolUse and the Agent PostToolUse with no agent_id chk=n,y,n,n family=evidence-citation fix=change the item 1 log line to 6 and 11, and add one line near the header saying the /tmp/ob/logs/... paths in the file are kept at OB/logs/... covers="no PASS lacks an evidence command and a log line or screen file": the cited lines do not hold the evidence shown (R:33).

F1.4 ac=T10.AC1 at=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-results.md:741 anchor="no PASS lacks an evidence command and a log line or screen file" chk=y,n,n,n family=evidence-file-missing fix=OB has no gov-log.txt (evidence.sh:412 copies only logs, screens and state.env, and /tmp/ob is gone), so the OB-CTX PASS parts "sleep 241 and sleep 242 told apart", "released case" and the OB-H3 .ok-file parts cannot be checked against the log file R:741 cites (/tmp/ob/gov-log.txt). Recover the gov-log text from the pasted rows into a file under OB, or re-record those parts with evidence that still exists; /tmp/ob/preconditions.txt is also gone covers="a log line or screen file": the log file cited for OB-CTX PASS does not exist in the delivered ob-logs.

F1.5 ac=scope at=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-results.md:469 anchor="For each `needs reading` mark, record the reading and the screen file it is based on in the results file." chk=n,n,n,y family=needs-reading-unrecorded fix=read the saved screens in OB/screens (sA-*, gB-*, gC-*, gE-*) and record the three readings with evidence.sh --reading u20, ac7 and retry-f7-f8 (each with its screen file), or write that no screen shows the block message; mind that evidence.sh all replaces the file on a rerun covers="record the reading and the screen file": R:469 (U20), R:535 (retry-f7-f8) and R:536 (AC-7) are still "needs reading" with no reading and no screen file, and OB-H3's "What you saw in the tab" (R:523) is empty.

F1.6 ac=scope at=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t10-run-log.md:30 anchor="session-a2.sh NOT run" chk=n,n,n,n family=a2-skipped fix=none needed for blocking; the task order lists session-a2.sh, but the run log gives the reason (real HOME trust entry outside the plan's named side effects) and OB-H1 item 7 is recorded pending (R:237) covers="session-a2.sh in the task order": skipped on purpose, recorded, item 7 pending, not a gate (runbook 3.3 needs items 1 and 5).

## Parent keys (orchestrator, after anchor Read-back)
F1.1 sev=blocking trigger=B1 first=A1 origin=new (AC words byte-present)
F1.2 sev=blocking trigger=B1 first=A1 origin=new (AC words byte-present; AC cannot hold with both issue sets on GitHub: needs a user-accepted gap or a rewording)
F1.3 sev=blocking trigger=B2 first=A1 origin=new (results line cites log lines 2,3,4; the evidence rows are 6 and 11 of the copied log)
F1.4 sev=blocking trigger=B1 first=A1 origin=new (gov-log.txt and preconditions.txt are not in the ob-logs copy)
F1.5 sev=blocking trigger=B4 first=A1 origin=new (task instruction text byte-present: "For each `needs reading` mark, record the reading and the screen file")
F1.6 sev=note (no blocking answer)
Verdict (computed): missing (T10.AC1, T10.AC2, T10.AC3 unmet; T10.AC4 met)
