65d8bd254e86b9e9332250bd0fdeb62269ccdf8a
A1 r1-1 F1.1 note src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:322 ac=scope n,n,n,n lookup also drops main-worktree rows; the task text does not say so (intended: the main checkout is never an issue worktree)
A1 r1-1 F1.2 note src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:303 ac=scope n,n,n,n the marker regex has a lookbehind so "xsc:issue ..." does not match; stricter than the task text
A1 r1-1 F1.3 note src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:91 ac=scope n,n,n,n run() has a cwd parameter no caller passes
