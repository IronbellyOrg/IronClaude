101a45fe391d993a3315e0b72e249eb5a0277124
A1 r1-1 F1.1 minor tests/vcs/test_worktree_protection.py:386 ac=scope n,n,n,n the orphan-hook test orders its "too early" read before a rewrite using a fixed 2-second delay, so a slow machine could fail it (fix: poll for the orphan marker file instead of sleeping).
