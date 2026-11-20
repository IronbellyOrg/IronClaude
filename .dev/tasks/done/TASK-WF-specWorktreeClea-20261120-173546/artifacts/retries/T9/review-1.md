bcbec7b3496ae617b63e13242967471cef806251 tree=50b6e65d7d56d40d0e2916c768add67b323c5363
T9.AC1 met scripts/worktree_cleanup.py:2255-2286,2293-2309; tests/worktree_cleanup/test_archive.py:109
T9.AC2 unmet (F1.2) scripts/worktree_cleanup.py:2123-2139,2111-2119,2287-2288; test_archive.py:192,281,301
T9.AC3 met scripts/worktree_cleanup.py:1925-1958,2007-2018,2214-2286; test_archive.py:328,357
T9.AC4 met scripts/worktree_cleanup.py:1883-1902,2200-2202; test_archive.py:430
F1.1 sev=blocking trigger=B4 ac=scope at=scripts/worktree_cleanup.py:2245 anchor="A repeat run verifies an existing folder again and checks every file now in the worktree is covered" chk=n,n,n,y family=repeat-run-existing-folder-unverified fix=in the branch that writes a new -r2 or -r3 folder, verify every folder in existing as well and fail if any differs from origin/main covers="A repeat run verifies an existing folder again" first=A1 origin=new: an existing folder that was never committed counts as covered, so its paths are returned as saved although their only copy was never pushed or checked.
F1.2 sev=blocking trigger=B1 ac=T9.AC2 at=scripts/worktree_cleanup.py:1887 anchor="a failed copy each return a failure reason beginning" chk=y,n,n,n family=read-failure-not-failed-closed fix=catch OSError and ValueError around the secret scan, the digest step and the saved-paths and manifest writes and return a saved copy failed reason first=A1 origin=new: an unreadable file raises instead of returning a saved copy failed result.
F1.3 sev=blocking trigger=B4 ac=scope at=scripts/worktree_cleanup.py:1839 anchor="scans the files to be saved for token-shaped content" chk=n,n,n,y family=secret-pattern-over-broad fix=add a left boundary to the sk-, AKIA and gh token patterns first=A1 origin=new: the sk- pattern has no left boundary, so ordinary hyphenated words match and harmless files stop the save.
F1.1 resolved
F1.2 resolved
F1.3 resolved
