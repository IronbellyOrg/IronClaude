2997c7f4abe7ad2cea3b1bb2100aae36841b5a67
A1 r1-1 F1.1 note ac=scope at=tests/skills/test_issue_orca_worktree.py:1446 chk=n,n,n,n: L2 edge cases (directory or dangling symlink at hooks/pre-push, relative core.hooksPath, missing worktree, git failure) are correct in code but not pinned by tests.
A1 r1-1 F1.2 note ac=scope at=src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:954 chk=n,n,n,n: the absent line is also printed when git fails; its parenthetical is slightly stronger than what was verified.
A1 r1-1 F1.3 note ac=scope at=src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:948 chk=n,n,n,n: a HOME path with a double quote or dollar sign would break the printed rm line.
