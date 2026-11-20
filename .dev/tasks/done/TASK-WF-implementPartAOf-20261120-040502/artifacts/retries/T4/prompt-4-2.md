1fb5852106c928db57a2b98165ce7b3eb59dae4a
Review one task for spec compliance.

Task brief: Task 4: Sync the dev copies and open the pull request

Depends on: Task 2, Task 3

Run `make sync-dev` and `make verify-sync` (must exit 0), stage `src/`, `tests/` and `.dev/tasks` (this package and its `./artifacts/`) and never a `.claude/` path, commit on the work branch, rebase on `origin/master`, and open the pull request with `/sc:pr-submit --monitor 3` (head the work branch, base `master`, repo `IronbellyOrg/IronClaude`). The body names issue 691 Part A, states that Part B waits for pull request 685, and states that no agent-printing rule was added. Write the sync and test outputs to `./artifacts/t4-sync.log` (the artifacts folder of this package, not the project-root `artifacts/`).

Acceptance criteria:
- T4.AC1: `./artifacts/t4-sync.log` shows `make verify-sync` exiting 0 and the four test files named in Tasks 2 and 3 (`tests/skills/test_issue_orca_worktree.py`, `tests/skills/test_issue_l2_install.py`, `tests/skills/test_issue_protocol.py`, `tests/commands/test_issue_command.py`) passing, and `git status` shows no `.claude/` path staged and `.dev/tasks` staged.
- T4.AC2: The returned pull request URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`.
Global constraints: Edit distributable files only under `src/superclaude/` and tests under `tests/`; then run `make sync-dev` and `make verify-sync`. The `.claude/` copies are never staged, and no installed primitive may name a `src/superclaude/` path. The file is best-effort: a failed write never changes the JSON the `launch` subcommand prints, and the existing launch JSON keys keep their names and values. Part B (session-gov.sh, observation runbook, superclaude install, live OB-H2 rerun) and a verbatim-print rule for the claiming agent are out of scope.
Start sha: 1fb5852106c928db57a2b98165ce7b3eb59dae4a
Diff against the start snapshot: The change is in the worktree at /home/coder/workspaces/worktrees/IronClaude/issue-691-launch-result. Produce it with `git diff 1fb5852106c928db57a2b98165ce7b3eb59dae4a -- src tests` (changed files: no src or tests change in this task; evidence is .dev/tasks/TASK-WF-implementPartAOf-20261120-040502/artifacts/t4-sync.log (rewritten after the first review), git show --name-only HEAD, git status --short (staged paths), and the pull request https://github.com/IronbellyOrg/IronClaude/pull/693 (gh pr view 693 --repo IronbellyOrg/IronClaude --json url,headRefOid); no untracked product files). Codegraph context: index_state: fresh, checked_at: 2026-11-20T04:06:49Z, worktree_root and projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-691-launch-result. Call codegraph only when index_state: fresh, never to widen scope.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): F1.1 ac=T4.AC1 at=.dev/tasks/to-do/TASK-WF-implementPartAOf-20261120-040502/artifacts/t4-sync.log:15 anchor="the four test files named in Tasks 2 and 3 ... passing" chk=y,n,n,n family=t4-log-evidence fix=name each file with its result: the log named only one of the four test files
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
