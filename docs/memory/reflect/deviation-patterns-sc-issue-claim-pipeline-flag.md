# Reflect deviation patterns: sc-issue-claim-pipeline-flag

## pre-TASK-WF-scIssueClaimPipe-20261107063558 (UC-1, /sc:issue --pipeline plan review)
- Verdict FAIL (tier 2, convergence 1.00, calibrated 0.78): 6 blocking Drift findings, 6 MEDIUM, 8 minor; no Regression after Round 2 (the Regression labels on transient plan states were withdrawn by all three advocates).
- Recurring plan-defect class for edits to src/superclaude/{skills,commands,agents}: `tests/skills/test_worker_contract.py` audits every line that names `git add|commit|push|merge|stash|update-ref|worktree add` or `gh pr|api` and requires an exact-text classification entry; a plan that adds such text (a launch prompt, a script docstring, a Will Not line) must name that test file and the entries. Editing an already-classified line also needs its key updated.
- Recurring plan-defect class: a task that creates a file under skills/*/scripts or templates must add the SKILL.md files-table row in the same task; `tests/skills/test_issue_protocol.py::test_every_named_path_exists_and_every_file_is_named` is red otherwise.
- Recurring design-vs-plan class: a design instruction that needs data from a script (the "untracked" line needs a tracked-files field) is unimplementable unless the script's output schema carries it; fix the design first.
- Test-pin traps seen in this repo: `tests/commands/test_issue_command.py` forbids the literal `--repo` anywhere in commands/issue.md; a substring scan for banned flags collides with `--issue-url` and `--prompt` (match whole tokens, parse the argv with ast).
- Reflect mechanics: specs labelled P/D/FR/ST/OB give 0 Pass-1 ids, so coverage_degraded parsed-sparse forces tier 2 every time (same as pre-mergedOutput-20261024165806).
