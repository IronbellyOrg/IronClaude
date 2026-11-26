57895d5aca1f7bf6bd78cfb5a2dd36d1107e3f4f
Review one task for spec compliance.

Task brief: Task 10 of the plan /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-181052/TASK-WF-remediationSourc-20261126-181052.md (read lines 120-128 of that plan for the full Task 10 text and AC; the spec is the sibling source.md, sections "Schedule and install notes doc", "Pre-install check" and "Hook"; the Task 8 decision in ./artifacts/hook-decision.md of the package folder ends "Decision: deliver", so the drop paragraph is not needed). Summary: create docs/user-guide/run-ledger.md holding: what the ledger is and where it lives (${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger.json); the schedule recommendation for Coder#545 (system crontab, every 30 minutes at offset minutes such as 17,47, wrapped in flock -n on a lock file, command superclaude sweep ledger, with an explicit PATH that includes the directory of the Orca CLI shim, output appended to a log under ${XDG_STATE_HOME:-~/.local/state}/superclaude/), with the reasons from the source (survives session and Orca restarts, no model, logged non-zero exit; a session-only cron dies with the session; whether an Orca automation can run a non-model command is UNVERIFIED); the hook registration entry {"matcher":"Bash","hooks":[{"type":"command","command":"~/.claude/hooks/run-ledger-record.sh"}]} under hooks.PostToolUse; the plain statement that in Coder the crontab is rewritten on every boot so a hand-edited crontab is lost and that the schedule and the hook registration are registered by Coder#545, not by this work; the pre-install check `env -i HOME=$HOME PATH=<the cron PATH> superclaude sweep ledger --dry-run` must exit 0 and the `command -v superclaude` check; the session-cron fallback; the stale warning (90 minutes) the sweep prints when the schedule dies; and that after an Orca database reset run-list returns no Runs while an old ledger exists, so every build exits implausible: until the old ledger file is removed by hand. The doc must not tell the reader to run crontab -e.
Acceptance criteria:
T10.AC1: docs/user-guide/run-ledger.md exists, names the command superclaude sweep ledger, the exact hook registration entry (or the drop paragraph), the pre-install check and the Coder#545 ownership statement, and contains no crontab -e instruction and no src/superclaude/ path.
T10.AC2: Every superclaude command and flag the doc names exists in `uv run superclaude sweep ledger --help` or `uv run superclaude sweep run --help`; other tools the doc names (flock, env, command) are outside this check.
Global constraints: UV only. Not allowed: installing a crontab, scheduling anything, editing ~/.claude/settings.json, adding the hook to hooks.json, committing, pushing, PRs, GitHub writes. Behaviour facts the doc states must match the code in src/superclaude/cli/sweep/ledger.py and src/superclaude/cli/sweep/commands.py (check the claims about exit codes, guards, the 24 hour rule, the 90 minute stale header, --add and the hook against the code).
Start sha: 57895d5aca1f7bf6bd78cfb5a2dd36d1107e3f4f
Diff against the start snapshot: new file, whole contents: /home/coder/workspaces/worktrees/IronClaude/run-ledger/docs/user-guide/run-ledger.md. Run state of the code graph: index_state: fresh, checked_at: 2026-11-26T18:23:53Z, worktree_root: /home/coder/workspaces/worktrees/IronClaude/run-ledger, projectPath: /home/coder/workspaces/worktrees/IronClaude/run-ledger. call codegraph only when index_state: fresh, never to widen scope.
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
