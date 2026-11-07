fdb08e60c8c3f45bcd1681cd1c79c40da4247b65
A1 r1-2 F1.1 minor .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-051649/artifacts/t1-red.log:14 ac=T1.AC1 n,n,n,n recovery re-review: the saved red log was captured in another worktree from an earlier version of the test file (failure lines sit 2 lines above the delivered asserts); the reviewer re-ran the start tree and got the same 7 failed and 6 passed
A1 r1-2 F1.2 note tests/skills/test_model_alias_policy.py:49 ac=scope n,n,n,n the tier-text test reads only the TEXT_SUFFIXES suffixes; no file outside them contains a tier id today
A1 r1-2 F1.3 note tests/skills/test_model_alias_policy.py:148 ac=scope n,n,n,n a Python module that does not parse is skipped without a report
A1 r1-2 F1.4 note tests/skills/test_model_alias_policy.py:6 ac=scope n,n,n,n the docstring says the launcher sets the three variables in tier mode; false at the start tree, true against the live launcher after #391, so no change needed
