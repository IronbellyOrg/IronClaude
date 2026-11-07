d7997c8df7f1c257d366942ecabcbc9cd41c0aac tree=b0f1f01cdfc909a96da6aec8c3987da49df58919
T5.AC1 unmet tests/skills/test_issue_orca_worktree.py:159 F1.1
F1.1 sev=blocking trigger=B1 ac=T5.AC1 at=tests/skills/test_issue_orca_worktree.py:159 anchor="`uv run pytest tests/skills/test_issue_orca_worktree.py -k prompt` passes with PR-1 to PR-4" chk=y,n,n,n family=ac-selector fix=rename test_pr1..test_pr4 and test_pr_unusable_template_is_reported_not_raised to carry "prompt" in the name first=start origin=new: the `-k prompt` command run as written selects only test_arg1_prompt_bad_arguments_exit_2, so PR-1 to PR-4 never run under it.
F1.1 resolved (re-review r1-2)
