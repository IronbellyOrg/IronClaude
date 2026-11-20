279eeef4a0fe7a43f5fea61dff96307e813d8ebc tree=c028a2e3394b80a0664a399f005447d72f455c7b
F1.2 resolved
T11.AC1 met scripts/worktree_cleanup.py:2376-2481, tests/worktree_cleanup/test_removal.py:172-198
T11.AC2 met scripts/worktree_cleanup.py:2384, scripts/worktree_cleanup.py:2443-2448, scripts/worktree_cleanup.py:503-520, tests/worktree_cleanup/test_removal.py:483-493
T11.AC3 met scripts/worktree_cleanup.py:477-498, scripts/worktree_cleanup.py:506, scripts/worktree_cleanup.py:2460-2464, tests/worktree_cleanup/test_removal.py:201-227
T11.AC4 met scripts/worktree_cleanup.py:2365-2369, scripts/worktree_cleanup.py:1651-1659, scripts/worktree_cleanup.py:1680-1685, tests/worktree_cleanup/test_removal.py:233-254
T11.AC5 unmet (F1.3) scripts/worktree_cleanup.py:2525-2526
F1.3 sev=blocking trigger=B1 ac=T11.AC5 at=scripts/worktree_cleanup.py:2525 anchor="When Orca still lists the worktree at the read back" chk=y,n,n,n family=orca-readback-unlisted-skip fix=when orca is None still read the Orca list reply with orca_lists and return the still-listed failure if it is True, or the could-not-be-read failure if it is None; make orca_lists ignore an empty or missing id; add a test where the removal goes through git worktree remove and the Orca list still shows the path covers="When Orca still lists the worktree at the read back, the result is \"removed in git but still listed in Orca\"" first=A1 origin=late: the read back runs the Orca list for a worktree with no Orca row and then returns without reading the reply.
F1.3 resolved
