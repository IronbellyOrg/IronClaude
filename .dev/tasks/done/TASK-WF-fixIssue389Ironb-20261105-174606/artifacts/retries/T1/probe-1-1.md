ce35c6d0c850b99092a711707782d011227b3fd5
family: t1-negative-witness-tier-line
defect form: the saved negative log lists fewer [ccsession] lines than the AC names (tier line missing because the test fixture is not in tier mode)
command: grep -n -F -e '[ccsession]' -- /home/coder/workspaces/worktrees/IronClaude/ic-issue-389/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t1-negative.log tests/unit/test_ccsession_tag.py
before:
.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t1-negative.log:10:E   AssertionError: assert '[ccsession] ...laude Code)\n' == '2.1.318 (Claude Code)\n'
.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t1-negative.log:12:E     + [ccsession] Shim already running on 127.0.0.1:4555 (reusing)
.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t1-negative.log:13:E     + [ccsession] Starting untagged session
tests/unit/test_ccsession_tag.py:660:            "[ccsession] WARNING: could not pre-load gateway models; Claude Code will retry "
tests/unit/test_ccsession_tag.py:1508:    assert "[ccsession] Starting untagged session" in result.stderr
coupled sites: tests/unit/test_ccsession_tag.py test_version_through_orca_keeps_stdout_clean assertion on 'Starting untagged session'; the AC text of Task 1
after:
10:E   AssertionError: assert '[ccsession] tier2 (Tier 2: stand-in-t2model01, stand-in-t2model02, stand-in-t2model03, stand-in-t2model04, stand-in-t2model05, stand-in-t2model06): model claude-gw-tier2
12:E     + [ccsession] tier2 (Tier 2: stand-in-t2model01, stand-in-t2model02, stand-in-t2model03, stand-in-t2model04, stand-in-t2model05, stand-in-t2model06): model claude-gw-tier2[1m], context 500000
13:E     + [ccsession] Shim already running on 127.0.0.1:4555 (reusing)
14:E     + [ccsession] Starting untagged session
17:FAILED tests/unit/test_ccsession_tag.py::test_version_through_orca_keeps_stdout_clean - AssertionError: assert '[ccsession] tier2 (Tier 2: stand-in-t2model01, stand-in-t2model02, stand-in-t2model03
19:  + [ccsession] tier2 (Tier 2: stand-in-t2model01, stand-in-t2model02, stand-in-t2model03, stand-in-t2model04, stand-in-t2model05, stand-in-t2model06): model claude-gw-tier2[1m], context 500000, au
20:  + [ccsession] Shim already running on 127.0.0.1:4555 (reusing)
21:  + [ccsession] Starting untagged session
