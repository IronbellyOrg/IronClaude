71d0a0683b0d8a3cab6509fdf9c8a2c094611d8a
Review one task for spec compliance.

Task brief: Task 10 of the plan /home/coder/workspaces/worktrees/IronClaude/issue-326/.dev/tasks/to-do/TASK-WF-design-20261126-184601/TASK-WF-design-20261126-184601.md: its text and its acceptance criteria are plan lines 134-143 (read exactly those lines; the AC are the bullets under 'Acceptance criteria:', numbered in source order as T10.AC1, T10.AC2). The design the plan is built from is /home/coder/workspaces/worktrees/IronClaude/issue-326/.dev/tasks/to-do/TASK-WF-design-20261126-184601/source.md and the full requirement wording is in /home/coder/workspaces/worktrees/IronClaude/issue-326/.dev/brainstorms/20261126-115614-git-pm-workflows-skills/merged-requirements.md (read a cited FR there only when an AC needs its exact wording).
Global constraints: the plan's `## Constraints` section, plan lines 17-32 of /home/coder/workspaces/worktrees/IronClaude/issue-326/.dev/tasks/to-do/TASK-WF-design-20261126-184601/TASK-WF-design-20261126-184601.md (read them).
Start sha: 71d0a0683b0d8a3cab6509fdf9c8a2c094611d8a
Diff against the start snapshot: the complete output of `git diff 71d0a0683b0d8a3cab6509fdf9c8a2c094611d8a <current tree> -- .` (new files in full), saved at /tmp/impl326/T10-r1-1.diff. Read that whole file; it is the diff. The ledger, the retries folder and artifacts/codegraph.md of the package are excluded from it. Real current files are in the checkout /home/coder/workspaces/worktrees/IronClaude/issue-326; you may read them and run read-only commands (grep, git diff, `PYTHONDONTWRITEBYTECODE=1 uv run pytest ...`) to verify a claim. Do not create, edit, move or delete any file, do not run git add, commit, stash, checkout or reset.
Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

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
