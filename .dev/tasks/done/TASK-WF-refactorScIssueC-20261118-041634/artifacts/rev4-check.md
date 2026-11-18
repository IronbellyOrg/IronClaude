# Third fresh check of the plan (2026-11-18), and revision 4

Checker: a third fresh read-only reviewer agent (reflect-reviewer class, alias opus, new instance). It was told to judge the plan cold and to search the whole tests/ tree, scripts/, the Makefile, src/superclaude/cli and .github for readers of every file the tasks change, because the earlier misses were all existing tests pinning text in changed files. It ran no tests.

Verdict on revision 3: PASS. No blocking defect: no existing test under tests/ would fail because of a planned edit without the plan naming it. It read every test that touches the changed files, including the worker-contract write-verb audit, the HOW-WE-WORK readers, the onboarding deck test and the user-guide readers; it re-read every line the tasks cite; it found no scope creep on `--submit` and no edit to the watcher or its tests; the package files agree.

Medium findings, each confirmed by the orchestrator against the real file before it was applied in revision 4:
1. An already-launched level is not always in `worktree.json`: the helper falls back to a mirror file in the worktree's git directory (`orca_worktree.py` `read_mirror`, used when the record has no `launch` entry, i.e. a re-claim from inside the worktree). Task 4 now names the mirror file as the second source.
2. In `docs/designs/sc-issue-claim-pipeline-flag.md` lines 21, 43, 66, 78 and 274 are table rows (line 87 is prose). A note placed as a new line under a row would split the table. Task 8 now says to append each note inside the row's last cell, as decision P4 at line 45 does, and its acceptance checks that the tables still render.
3. `tests/skills/test_issue_protocol.py::test_no_source_tree_path_in_skill_files` forbids `src/superclaude/` in every file under `sc-issue-protocol/`, not only in the command file. The Constraints now say so, and add the checker's caution that `tests/skills/test_worker_contract.py` audits `git add`, `git commit`, `git push`, `git merge`, `gh pr` and `gh api` in new lines of command and skill files.

Notes applied: Task 4 says "line 142 of `refs/claim.md`"; Task 7 names "the row at line 1557"; Task 4 now has `Depends on: Task 3`. Notes not applied: wording nits on the "Superseded by #384" phrase and the unchanged `>= 2` count.

Revision 3 is kept in artifacts/plan-rev3-before-checker-c.md and the change set in artifacts/plan-rev3-to-rev4.diff. Revision 4 has not itself been re-checked; its edits are the three medium fixes, the caution and the three notes above.
