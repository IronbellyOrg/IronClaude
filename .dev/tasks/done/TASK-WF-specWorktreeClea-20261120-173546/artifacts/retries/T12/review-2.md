44f5941e9fc784d4934bd6650ea57ab811cc7d1a tree=ab42ba5ae5be5da7e551cdeb120639e8da00dd32
F1.1 resolved
F1.2 resolved
F1.3 resolved
F1.4 resolved
T12.AC1 met scripts/worktree_cleanup.py:2960, scripts/worktree_cleanup.py:2956, tests/worktree_cleanup/test_verbs.py:159, tests/worktree_cleanup/test_verbs.py:187
T12.AC2 met scripts/worktree_cleanup.py:2819, scripts/worktree_cleanup.py:2867, scripts/worktree_cleanup.py:2911, tests/worktree_cleanup/test_verbs.py:300, tests/worktree_cleanup/test_verbs.py:281
T12.AC3 unmet (F1.5) scripts/worktree_cleanup.py:2458, scripts/worktree_cleanup.py:2466, scripts/worktree_cleanup.py:2968, scripts/worktree_cleanup.py:3061, scripts/worktree_cleanup.py:2908
T12.AC4 met scripts/worktree_cleanup.py:2951, scripts/worktree_cleanup.py:2977, scripts/worktree_cleanup.py:2980, scripts/worktree_cleanup.py:1833, scripts/worktree_cleanup.py:2942, tests/worktree_cleanup/test_verbs.py:187
F1.5 sev=blocking trigger=B1 ac=T12.AC3 at=scripts/worktree_cleanup.py:2458 anchor="69 lookup or removal failure" chk=y,n,n,n family=exit-code-recheck fix=when the re-check after the terminals are closed cannot read a fact (git status gives None, the process scan fails, or the relation to the pull request is unknown), have remove_worktree return a failed status so prune counts it in failed and retire exits 69 first=A1 origin=late: remove_worktree returns kept for an unreadable re-check, so prune --apply exits 0 with failed 0 and retire exits 64.
F1.5 resolved (attempt 3, review-3.md)
