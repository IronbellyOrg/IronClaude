adc880232c23f71b22a83dfb626af4bb6f9a78e8
tree=none
T7.AC1 met tests/issue_watch/test_launch.py:659; T7.AC2 met tests/issue_watch/test_cycle.py:495; T7.AC3 met tests/issue_watch/test_security_invariants.py:69; T7.AC4 unmet (F1.1) src/superclaude/cli/issue_watch/cli.py:161
F1.1 ac=T7.AC4 at=src/superclaude/cli/issue_watch/cli.py:161 anchor="it must keep printing a valid command for every allowed Status and Pipeline" chk=y,n,n,y family=status-retry fix=recover the prompt on the real path sev=blocking trigger=B4 first=start origin=new: status_report prints argv None unless the caller passes prompts; the CLI passes none
