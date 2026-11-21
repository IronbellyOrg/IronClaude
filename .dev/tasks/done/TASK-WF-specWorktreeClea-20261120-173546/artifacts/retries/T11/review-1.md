279eeef4a0fe7a43f5fea61dff96307e813d8ebc tree=384da619597cf721a566238591d17231dfa441df
T11.AC1 met scripts/worktree_cleanup.py:2379, 2391, 2407, 2417, 2425, 2446, 2460, 2464, 2497, 2509, 2511, 2520
T11.AC2 met scripts/worktree_cleanup.py:2382, 2384, 2443, 2446, 503, 512, 516, 530
T11.AC3 met scripts/worktree_cleanup.py:369, 381, 506, 484, 477, 2446
T11.AC4 met scripts/worktree_cleanup.py:2365, 2367, 2368, 2379, 2391, 2446, tests/worktree_cleanup/test_removal.py:233
T11.AC5 unmet (F1.2) scripts/worktree_cleanup.py:2525
F1.1 sev=minor trigger=none ac=scope at=scripts/worktree_cleanup.py:2334 anchor=scripts/worktree_cleanup.py:1200 chk=n,n,n,n family=shadowed-helper fix=rename the new helper and use it at its three call sites first=A1 origin=new: a second module level _first_line replaces the earlier one for every caller.
F1.2 sev=blocking trigger=B2 ac=T11.AC5 at=scripts/worktree_cleanup.py:2525 anchor=scripts/worktree_cleanup.py:2508 chk=n,y,n,n family=orca-readback-substring fix=read the Orca list output as JSON and compare paths and ids for equality instead of a substring test covers="When Orca still lists the worktree at the read back" first=A1 origin=new: a removed worktree whose path or id is a prefix of a surviving sibling is reported as still listed in Orca.
