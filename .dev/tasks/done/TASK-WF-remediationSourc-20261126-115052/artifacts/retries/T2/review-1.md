7f9f65b5e32ef5e1d5a066a5c728ff8748128d5c tree=f2fc3d7d0a5fb1fa8a8792678ac8d4e4be0ba5aa
T2.AC1 met ./artifacts/t2-after.txt:3
T2.AC2 met ./artifacts/t2-after.txt:5-14
T2.AC3 unmet [F1.1] ./artifacts/t2-after.txt:28
T2.AC4 met ./artifacts/t2-after.txt:3
T2.AC5 met ./artifacts/t2-after.txt:3
T2.AC6 met ./artifacts/t2-outcome.md:7,9,11
T2.AC7 met ./artifacts/t2-after.txt:23-24
T2.AC8 met ./artifacts/t2-outcome.md:3,15
F1.1 sev=blocking trigger=B1 ac=T2.AC3 at=./artifacts/t2-after.txt:28 anchor="holds the after readings and the `worktrees preserved:` line" chk=y,n,n,n family=evidence-after-worktree-ids fix=add the after ids of this repository's worktrees to t2-after.txt first=A1 origin=new: t2-after.txt records only a count (32 listed) where the after readings must repeat the worktree-id reading.
F1.2 sev=minor trigger=none ac=T2.AC3 at=./artifacts/t2-after.txt:17 anchor="no part of the response beyond the three named fields is saved" chk=n,n,n,n family=evidence-response-extra-field fix=shorten the line first=A1 origin=new: ok: true is copied from the response outside the three named fields.
F1.3 sev=minor trigger=none ac=T2.AC2 at=./artifacts/t2-after.txt:14 anchor="lists every command that was run" chk=n,n,n,n family=evidence-command-list fix=quote the exact variable tests and date calls first=A1 origin=new: the variable checks and date -u calls are described, not quoted.
