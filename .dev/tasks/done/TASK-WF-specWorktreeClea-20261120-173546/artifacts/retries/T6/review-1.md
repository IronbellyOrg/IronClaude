ecb11d4e9bd0ff8c6a0a18828c506d3204b88c82 tree=361ea9affe1a4007ecce8e5d2756bab6e3c61765
T6.AC1 met scripts/worktree_cleanup.py:1557-1571, 1738-1751
T6.AC2 unmet (F1.1, F1.2, F1.3) scripts/worktree_cleanup.py:1601-1617, 1037-1048
T6.AC3 met scripts/worktree_cleanup.py:1697-1715, 1540
T6.AC4 met scripts/worktree_cleanup.py:1542-1554, 1795-1808
F1.1 sev=blocking trigger=B1 ac=T6.AC2 at=scripts/worktree_cleanup.py:1605 anchor="a worktree that fails only that rule is kept with that rule's reason" chk=y,n,n,n family=missing-folder-reason fix=in _rule1 test not f.present before the origin test; add a test with origin None and present False covers="the reasons are the strings of source section 6" first=A1 origin=new: a missing folder is reported as "not our repo", not as "folder missing (reported only)".
F1.2 sev=blocking trigger=B4 ac=scope at=scripts/worktree_cleanup.py:1725 anchor="Every rule fails closed: a fact that could not be read keeps the worktree" chk=n,n,n,y family=fail-open-unread-fact fix=in _rule7 return a created time unknown reason when age is None; add a test first=A1 origin=new: created_ts None passes rule 7.
F1.3 sev=blocking trigger=B4 ac=scope at=scripts/worktree_cleanup.py:1713 anchor="Every rule fails closed: a fact that could not be read keeps the worktree" chk=n,n,n,y family=fail-open-unread-fact fix=in _rule6 keep the worktree when git_dir is None; add a test first=A1 origin=new: when git rev-parse --git-dir fails, operations stays empty and rule 6 passes without the git operation check.
F1.1 resolved
F1.2 resolved
F1.3 resolved
