start=4bf8f84e56b01a644fcb81014084a87af9447026 tree=unrecorded (the reviewed tree of attempt 1 review 1 was not pinned before the fix pass; the delta below is rebuilt from the edit calls)
AC T6.AC1 met .dev/issues/442/scripts/session-gov.sh:354-356,373 (self-test cases e-misrouted-*, e-pushurl-*)
AC T6.AC2 met .dev/issues/442/scripts/session-gov.sh:160-170 (self-test cases release-foreign-*, release-settings-*, c-released)
AC T6.AC3 met .dev/issues/442/scripts/session-gov.sh:35-42 (self-test cases gate-*)
AC T6.AC4 met .dev/issues/442/scripts/session-gov-selftest.sh:274-282 (prompts-bytes 9 of 9)
F6.1 sev=blocking trigger=B4 ac=scope at=.dev/issues/442/scripts/session-gov.sh:154 anchor="It waits up to 90 minutes for the agent's final `git status --short`, then sends the commit prompt." chk=amiss:n,false:n,harm:n,constraint:y family=first-stop-gate fix="launch_real takes the first-stop wait as an optional fourth argument; b and c pass it, d and e do not" first=A1 origin=new: launch_real ended every session with PENDING no-first-stop after 900 s, which cut d's 90-minute wait and e's cycle wait short; the plan text sits at TASK-WF-scriptThe442Obse-20261108-061618.md:152 (Read back, quoted words present)
F6.2 sev=blocking trigger=B3 ac=scope at=.dev/issues/442/scripts/session-gov.sh:334 anchor=.dev/issues/442/scripts/session-gov.sh:334 chk=amiss:n,false:n,harm:y,constraint:n family=o10-target fix="compare the pull request head branch with the T4 worktree branch before the PUT; otherwise record FAIL and write nothing" first=A1 origin=new: the contents-API PUT (line 334, Read back, it is the write) targeted the first pull request URL found anywhere in the h2-T4 log, so an unrelated fork pull request the agent read could receive a commit
F6.3 sev=minor trigger=none ac=scope at=.dev/issues/442/scripts/session-gov.sh:222 anchor=none chk=amiss:n,false:n,harm:n,constraint:n family=backup-check fix="remove the backup first or test the exit status of cp" first=A1 origin=new: a stale t1-local.json can satisfy the -s test when the source is missing
F6.4 sev=minor trigger=none ac=scope at=.dev/issues/442/scripts/session-gov.sh:147 anchor=none chk=amiss:n,false:n,harm:n,constraint:n family=main-unset fix="set MAIN once at entry" first=A1 origin=new: MAIN is unset for c and d, so the diagnostic worktree.json read in the no-terminal fallback uses the current directory
F6.5 sev=minor trigger=none ac=scope at=.dev/issues/442/scripts/session-gov-selftest.sh:23 anchor=none chk=amiss:n,false:n,harm:n,constraint:n family=selftest-stubs fix="add a claude stub to the test bin" first=A1 origin=new: session e runs the real claude --version during the self-test (read only, temp HOME)

--- re-review r1-2 tree=c4075ca05ae0686af6e13c06263fed58a36503e7 ---
F6.1 resolved
F6.2 resolved
No new findings; T6.AC1 to AC4 met.
