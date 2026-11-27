6b2daa9bbba471d6352aa47a40a434240add9292
Review one task for spec compliance.

Task brief: Task 7 of the plan /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-181052/TASK-WF-remediationSourc-20261126-181052.md (read lines 88-96 of that plan for the full Task 7 text and AC). Summary: edit src/superclaude/commands/sweep.md (the --run <id> row of the Options table and the sentence "When no Run is bound and none is named, the command exits ...") so they say that, with no --run and no bound Run, the Run ids come from the Run ledger built by `superclaude sweep ledger`, and that a missing ledger exits with a hint. Edit src/superclaude/skills/sc-sweep-protocol/SKILL.md near line 19 the same way, keeping the pinned phrase "adds no flag, reads no environment variable and has no worker mode" (required by tests/commands/test_sweep_command.py:497) and keeping the skill limited to the one command `superclaude sweep run`. Use installed paths only; no src/superclaude/ path inside either text. Then run `make sync-dev`.
Acceptance criteria:
T7.AC1: `uv run pytest tests/commands/test_sweep_command.py -v` passes.
T7.AC2: `make verify-sync` reports no difference, and `git status` shows no staged or modified .claude/ file other than what make sync-dev writes (those are never staged).
Global constraints: UV only. Edit under src/superclaude/ then run make sync-dev; never stage .claude/ contents; no text in an installed command, skill or hook may tell an agent to read a src/superclaude/... path. Not allowed: committing, pushing, PRs, GitHub writes, editing ~/.claude/settings.json. Behaviour decisions are fixed by the source: the sweep skill still runs only superclaude sweep run, and adds no flag.
Start sha: 6b2daa9bbba471d6352aa47a40a434240add9292
Diff against the start snapshot: run `git diff 6b2daa9bbba471d6352aa47a40a434240add9292 -- src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol/SKILL.md` from /home/coder/workspaces/worktrees/IronClaude/run-ledger. Run `make verify-sync` and `git status --short` yourself. Run state of the code graph: index_state: fresh, checked_at: 2026-11-26T18:23:53Z, worktree_root: /home/coder/workspaces/worktrees/IronClaude/run-ledger, projectPath: /home/coder/workspaces/worktrees/IronClaude/run-ledger. call codegraph only when index_state: fresh, never to widen scope.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
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
