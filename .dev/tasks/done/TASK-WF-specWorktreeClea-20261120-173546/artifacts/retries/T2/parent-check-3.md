Parent check of the escalation 1 advice for T2 (k=2, n=3).
advice-3-a.md: passes. Every citation reads back (sc_cite_check OK on attempt-2.diff, review-2.md, extras-2.log); T2.AC1 to T2.AC4 rows present once each; differs-by present; outcome: ready.
advice-3-b.md: fails. Citation review-1.md:7 is not an evidence file of this escalation (review-2.md, attempt-2.diff, extras-2.log) and `git diff --quiet <start> <checkpoint>` on it exits 1 (the file exists only after the start), so it does not survive the revert as cited content. All other citations read back OK.
Pick: advice-3-a.md, the only passing answer; no runner-up (so a failure of attempt 4 halts with no-runner-up).
