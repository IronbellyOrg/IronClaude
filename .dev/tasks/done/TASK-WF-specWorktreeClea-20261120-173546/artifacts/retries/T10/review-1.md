feef03e3aed612bd5efb11ae0a546ecf0836bff5 tree=83b68bfadad0ce89dc381570e5ba155f2ecc2d1c
T10.AC1 met tests/worktree_cleanup/test_archive.py:109, :192, :328, :357, :404, :430, :618, :665
T10.AC2 unmet (F1.1) tests/worktree_cleanup/test_archive.py:109, :192, :281, :301, :328, :357, :391, :404, :618, :430, :665
T10.AC3 met tests/worktree_cleanup/test_archive.py:685
F1.1 sev=blocking trigger=B4 ac=T10.AC2 at=tests/worktree_cleanup/test_archive.py:678 anchor="assert the assembled value is absent from captured output and from every file of the evidence clone" chk=n,n,n,y family=secret-clone-scope fix=read every file of the clone with no folder filter in both secret tests, and make the clone exist in the first test first=A1 origin=new: the existing-clone test skips the .git folder and the first secret test checks no clone file because the clone never exists.
F1.2 sev=blocking trigger=B4 ac=scope at=tests/worktree_cleanup/test_archive.py:602 anchor="Build any token-shaped test string at run time from two pieces" chk=n,n,n,y family=committed-token-literal fix=split the literal in two pieces covers="Build any token-shaped test string at run time from two pieces" first=A1 origin=new: a whole token-shaped literal is committed in one piece.
F1.1 resolved
F1.2 resolved
