0f1c718b84ac3f485ce1236b99e8d74e39ccb9a2
Review one task for spec compliance.

Task brief: Task 8 of the plan /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-181052/TASK-WF-remediationSourc-20261126-181052.md (read lines 100-106 of that plan for the full Task 8 text and AC). Summary: run exactly one `orca orchestration run-create --objective "scratch Run for the run-ledger hook payload test, safe to ignore" --json`. Authority: the owner's brief orders the test in the words "first test what such a hook actually receives from run-create"; that sentence is copied into ./artifacts/hook-decision.md (relative to the package folder, i.e. /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-181052/artifacts/hook-decision.md) as the authority. Orca cannot delete the Run, say so there. Save its stdout as tests/run_ledger/fixtures/run_create_stdout.json. Read the official Claude Code hooks documentation for the PostToolUse payload of the Bash tool and write tests/run_ledger/fixtures/posttooluse_run_create.json with that payload shape (tool_name, tool_input.command, tool_response) wrapping the captured output. Run `orca orchestration run-current` before and after and note whether this terminal is now bound to the scratch Run. hook-decision.md states: the authority sentence, the captured output (or the reason it could not be captured), whether a run_[0-9a-f]{12} id is in it, the payload shape source, the number of scratch Runs created, and the decision, as the last line `Decision: deliver` or `Decision: drop` (drop only when a real capture shows no Run id in the output).
Acceptance criteria:
T8.AC1: ./artifacts/hook-decision.md exists, quotes the authority sentence, states the number of scratch Runs created (one, or zero with Status: UNVERIFIED) and ends with a line Decision: deliver or Decision: drop.
T8.AC2: tests/run_ledger/fixtures/run_create_stdout.json and tests/run_ledger/fixtures/posttooluse_run_create.json exist and parse as JSON; at most one Run was created and no Run was deleted.
Global constraints: UV only. Not allowed: orca orchestration reset, deleting a Run, Orca link flags (--issue, --pr), editing ~/.claude/settings.json, installing a crontab, scheduling, committing, pushing, PRs, GitHub writes. Real Orca calls of the plan are: read-only list calls, run-current, the one scratch run-create of this task, and the commands of Task 11; none is part of pytest.
Start sha: 0f1c718b84ac3f485ce1236b99e8d74e39ccb9a2
Diff against the start snapshot: all new files (read them whole): /home/coder/workspaces/worktrees/IronClaude/run-ledger/tests/run_ledger/fixtures/run_create_stdout.json, /home/coder/workspaces/worktrees/IronClaude/run-ledger/tests/run_ledger/fixtures/posttooluse_run_create.json and the hook-decision.md named above. You may verify read-only: `orca orchestration run-list --json` (it should list a Run with the objective "scratch Run for the run-ledger hook payload test, safe to ignore" exactly once; do not run run-create, run-current-changing or any other Orca write). Run state of the code graph: index_state: fresh, checked_at: 2026-11-26T18:23:53Z, worktree_root: /home/coder/workspaces/worktrees/IronClaude/run-ledger, projectPath: /home/coder/workspaces/worktrees/IronClaude/run-ledger. call codegraph only when index_state: fresh, never to widen scope.
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
