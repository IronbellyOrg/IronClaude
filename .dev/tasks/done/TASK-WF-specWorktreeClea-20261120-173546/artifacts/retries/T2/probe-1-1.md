6cc89734a79f8ee9834b04288bf19c6c08ae4997
family: runner-refusal-tests
defect form: a banned shape named in the acceptance criteria has no assertion that the runner refuses it
command: grep -n -E "(-f|--force)" tests/worktree_cleanup/test_runner.py
before: lines 53 to 56 and 98 to 99 and 157 and 169 of tests/worktree_cleanup/test_runner.py hold -f or --force cases; the case for the Orca worktree removal has only --force at line 56 and no -f case
coupled sites: the BANNED list at tests/worktree_cleanup/test_runner.py:52-64 (each banned shape of the criterion: --force or -f on the Orca removal and on the git worktree removal, git branch -D, rm, git worktree prune, git clean, git push with a delete flag or a :ref refspec, git push outside the evidence clone, git clean with an unregistered path)
after: (second run of the command) the Orca worktree removal now has the --force case at line 56 and the -f cases at lines 57 and 58, a second --force case at line 59; all banned shapes of the criterion have an assertion
