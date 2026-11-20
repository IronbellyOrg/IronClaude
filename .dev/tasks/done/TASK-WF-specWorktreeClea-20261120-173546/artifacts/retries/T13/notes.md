43b2163eaeb4ba44939bdd2e758aa5c4fbb327c3
A1 r1-1 F1.5 note tests/worktree_cleanup/test_safety.py:361 ac=scope n,n,n,n the safety refusal tests import only BANNED, UNLISTED and PUSH_REFUSED; the other refusal shapes (gh without --repo, a foreign owner, an unauthorized terminal close, a bad tar or landed-check argument) are covered in test_runner.py (Task 2)
