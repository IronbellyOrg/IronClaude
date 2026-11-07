# Reviewer 3 card (refactorer, opus class) - 8 deviations (Regression 1, Drift 4, Necessary 2, Authorized 1)

| # | Class | Location | Finding | Evidence | Sev |
|---|---|---|---|---|---|
| 1 | Regression | plan:58 (Task 1 install line) | `cmp` of "every file under src/superclaude/commands/" includes README.md and __init__.py, which are not installed; exits non-zero, install line FAIL, all live tasks `not run` (plan:21, :36) | src/superclaude/cli/install_commands.py:11, :40; plan:21, :36, :61 | HIGH |
| 2 | Drift | plan:541 (Task 23) | `find ... -name return-contract.yaml` over a checkout of the branch is never empty because tracked files exist; the plan saves no pre-run find to subtract; false FAIL | source.md:78; plan:541, :544 | MEDIUM |
| 3 | Drift | plan:58, :61, :65 | clean-tracked-tree check conflicts with the planned plan-file edit (plan:52), the modified APPROVED.md, and the plan's own no-commit rule (plan:24) | plan:24, :52, :58, :61, :65 | MEDIUM |
| 4 | Necessary | plan:14, :19, :33 | tip pin replaced by branch-tip.txt plus ancestor check | source.md:30 | LOW |
| 5 | Drift | plan:14, :52, :552 | stated reason for dropping the grant file does not explain it; the swap forces a plan edit that collides with #3; not listed in post-fix-rechecks.md | source.md:79 | LOW |
| 6 | Drift | plan:584 | stale "grant file" wording in Task 25 acceptance | plan:51, :552, :584 | LOW |
| 7 | Necessary | plan:554 | child worktree created first, synced, no --setup; `--parent-worktree active` not re-checked on Orca 1.4.245 | source.md:79; p0-live-orca-help.txt:36,69 | LOW |
| 8 | Authorized | plan:473, :495 | not-invoked check for guard cases 1 and 2 | spec AC-1.7 | LOW |

Advisory: (1) `pgrep -af -- '--watch'` likely matches the Bash tool's own shell, so lc18's before/after comparison may fail falsely (plan:227, :451, :465). (2) No rule normalises the worker's `--report-path` against `<R>/return-contract.yaml` (plan:41, :43, :73).

Notes: possible further problem, install_skills.py:88-98 does not install sc-* skills served by a same-named command, so the skills cmp could fail if the branch diff touches one (not checked). lc15 omits `--output <file>` and lc13 uses --report-dir; both follow source.md.
