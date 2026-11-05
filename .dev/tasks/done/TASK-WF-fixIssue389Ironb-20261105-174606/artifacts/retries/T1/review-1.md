ce35c6d0c850b99092a711707782d011227b3fd5
tree=d90ee7a139cba17770a1a58c3fa641057c338b13
AC marks (reviewer, verbatim):
- T1.AC1: met. tests/unit/test_ccsession_tag.py:1487-1510 (direct subprocess.run with capture_output, separate stdout/stderr reads, import at line 31)
- T1.AC2: unmet (F1.1). tests/unit/test_ccsession_tag.py:1507 fails on the stdout assertion; artifacts/t1-negative.log:8-14 shows two [ccsession] lines, the AC requires three
F1.1 sev=blocking trigger=B1 ac=T1.AC2 at=.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t1-negative.log:11-13 anchor="the failure output shows three `[ccsession]` lines (tier line, `Shim already running on 127.0.0.1:4555 (reusing)`, `Starting untagged session`) ahead of Claude's line" chk=y,n,n,n family=t1-negative-witness-tier-line fix=make the fixture enter tier mode (explicit AIDEV_AI_DEFAULTS_PATH with a tier block) so the unfixed tree prints the tier line, re-record the log first=A1 origin=new: The saved log shows only two [ccsession] lines (log lines 12-13), so the tier line is missing.
