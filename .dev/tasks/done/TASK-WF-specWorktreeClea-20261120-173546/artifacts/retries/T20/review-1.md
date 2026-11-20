44f5941e9fc784d4934bd6650ea57ab811cc7d1a tree=0c0c560ed41b94213c802aac2adea165bf613070
T20.AC1 met dry-run-report.md:40, dry-run/commands.txt:1-4
T20.AC2 met dry-run-report.md:60
T20.AC3 met dry-run/compare.txt:1
T20.AC4 met for worktrees, Orca objects and tracked files (see F1.1, F1.2)
T20.AC5 met (see F1.3)
F1.1 sev=blocking trigger=B1 ac=scope at=artifacts/dry-run-report.md:36 anchor="Only reads were made" chk=n,y,n,n family=safety-evidence-wording fix=say that the landed check runs a git fetch inside the real repos first=A1 origin=new: the report said only reads were made, but the landed check writes FETCH_HEAD and fetched objects in the real repos.
F1.2 sev=minor ac=scope at=artifacts/dry-run-report.md:87 family=safety-evidence-wording: the report said a lock folder was written under /tmp/worktree-cleanup-dry-run, but a dry run takes no lock.
F1.3 sev=blocking trigger=B1 ac=T20.AC5 at=artifacts/dry-run-report.md:93 anchor="the regression gate of source section 9 run on the finished change" chk=y,n,n,n family=gate-evidence fix=save the outputs of the reruns and cite them first=A1 origin=new: the reruns after the last edits (1924, 946, 487) had no saved evidence.
F1.4 sev=minor ac=scope at=artifacts/dry-run-report.md:68 family=count-comparison: the in Orca figure of 36 is compared with itself.
F1.5 sev=minor ac=scope at=artifacts/dry-run-report.md:79-80 family=report-precision: the fifth open-issue row is not named, and the ignored .env statement covers only rows that reach rule 5.
