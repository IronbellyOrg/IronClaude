c5f6df7b6bd3ad6397b7db9f850e36b78a45be30
Review one task for spec compliance.

Task brief: Read Task 2 (lines 64-91) of /home/coder/workspaces/worktrees/IronClaude/issue-462/.dev/tasks/to-do/TASK-WF-planOnlyForIssue-20261109-133801/TASK-WF-planOnlyForIssue-20261109-133801.md. Its four Acceptance criteria bullets in source order are T2.AC1 through T2.AC4. Read the complete supplied diff and all nine live delivery files it names. The task-owned output is artifacts/task2-agent-defaults.log, whose initial failure and rerun must both be retained and honestly represented. Static contracts are not live native model-selection evidence. Your runtime profile permits only Read, Grep and Glob. Return the complete review as text for parent-owned persistence; do not write files or use SendMessage, Agent, Bash or other tools. Start adversarially and include a brief self-audit of what you actively checked if no findings survive. Parent-owned output path: artifacts/retries/T2/review-1-raw.md. Actual backend routing will be audited from your execution transcript, not inferred from the requested alias.
Global constraints: Read the entire Constraints section (lines 17-31) of the same plan. The user subsequently authorized implementation of this existing plan and its required independent reviews; the planning-only limitation is not a ban on those authorized actions. No paid behavioral experiments, historical replay, global configuration changes, installations, commits, pushes, external posts, PRs or merge. Preserve historical uncertainty and do not send a second worker_done. Never read .dev/issues or .dev/troubleshoot for this review. Do not alter any file. Judge only Task 2, not the planned future Tasks 3-5.
Start sha: c5f6df7b6bd3ad6397b7db9f850e36b78a45be30
Diff against the start snapshot: Read /home/coder/workspaces/worktrees/IronClaude/issue-462/.dev/tasks/to-do/TASK-WF-planOnlyForIssue-20261109-133801/artifacts/task2-review.diff in full. The new task-owned log at /home/coder/workspaces/worktrees/IronClaude/issue-462/.dev/tasks/to-do/TASK-WF-planOnlyForIssue-20261109-133801/artifacts/task2-agent-defaults.log is also part of the delivery set; read it in full because T2.AC4 explicitly requires its observed results. Reviewed tree is 9b1370be543a915041333388f6a8a9537638e0ab. Worktree root is /home/coder/workspaces/worktrees/IronClaude/issue-462. Keep individual reads under 100 lines and search outputs under 40 lines.
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
