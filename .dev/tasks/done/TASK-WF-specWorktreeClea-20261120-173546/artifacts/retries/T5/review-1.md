24dad8c54df4a129e3277ae3e177f8b0c35783c8 tree=fa49b68aca3af910f1f0e1962aab8880b7e574a8
T5.AC1 met scripts/worktree_cleanup.py:438-454, scripts/worktree_cleanup.py:1292-1298, scripts/worktree_cleanup.py:1349-1352, scripts/worktree_cleanup.py:1440, scripts/worktree_cleanup.py:1451, tests/worktree_cleanup/test_facts.py:697-702
T5.AC2 met scripts/worktree_cleanup.py:1306-1308, tests/worktree_cleanup/test_facts.py:778-788
T5.AC3 met scripts/worktree_cleanup.py:1469-1494, scripts/worktree_cleanup.py:1499-1527, tests/worktree_cleanup/test_facts.py:939-995
T5.AC4 met scripts/worktree_cleanup.py:1332-1365, tests/worktree_cleanup/test_facts.py:891-920
F1.1 sev=blocking trigger=B2 ac=scope at=scripts/worktree_cleanup.py:1483 anchor=scripts/worktree_cleanup.py:1466 chk=n,y,n,n family=fail-open-orca-references fix=when references is given and not references.ok, append a failure so none_found is False and the worktree is kept; add a test with an unavailable OrcaRead covers="any lookup failure is \"issue lookup failed\" which keeps the worktree" first=A1 origin=new: an Orca reference read that came back not ok is skipped silently, so rule 4 can pass with "none found" when one of its sources was never read.
F1.1 resolved
