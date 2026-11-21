24dad8c54df4a129e3277ae3e177f8b0c35783c8
family: fail-open-orca-references
defect form: a source of rule 4 whose read failed is skipped without recording a failure, so none_found can be true
command: grep -n -E "references\.ok|references is not None|\.unavailable" scripts/worktree_cleanup.py
before:
800:    ], f"{read.unavailable}; scanning the current checkout's repo only"
1483:    if references is not None and references.ok:
coupled sites: the collect_issues docstring (any failed lookup is recorded); the failed-lookup test in tests/worktree_cleanup/test_facts.py (add an unavailable reference read); repos_or_current at line 800 already records its reason and is not affected; the worktree argument of collect_issues is None when the tool does not list the worktree, which is allowed and is not a failure
after:
800:    ], f"{read.unavailable}; scanning the current checkout's repo only"
1484:    if references is not None and not references.ok:
1486:        unread.append(f"issue lookup failed: {references.unavailable}")
1487:    if references is not None and references.ok:
