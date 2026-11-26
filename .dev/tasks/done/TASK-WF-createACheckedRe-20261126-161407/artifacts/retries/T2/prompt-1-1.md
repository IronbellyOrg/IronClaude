b69f41dfefdb1da4e4828bc306209c3de57c8e1a
Review one task for spec compliance.

Task brief: Task 2 text and acceptance criteria at /home/coder/workspaces/worktrees/IronClaude/issue-540-resume-marker/.dev/tasks/to-do/TASK-WF-createACheckedRe-20261126-161407/TASK-WF-createACheckedRe-20261126-161407.md:40-55. AC ids in bullet order: T2.AC1 at51, T2.AC2 at52, T2.AC3 at53, T2.AC4 at54, T2.AC5 at55.
Global constraints: The same plan's full ## Constraints section, lines17-25.
Start sha: b69f41dfefdb1da4e4828bc306209c3de57c8e1a
Diff against the start snapshot: Full actual diff including full new task-owned files is supplied as /home/coder/workspaces/worktrees/IronClaude/issue-540-resume-marker/.dev/tasks/to-do/TASK-WF-createACheckedRe-20261126-161407/artifacts/t2-diff.patch.
Codegraph context: index_state: fresh; checked_at: 2026-11-26T17:40:24Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-540-resume-marker; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-540-resume-marker. call codegraph only when index_state: fresh, never to widen scope. Dependents: src/superclaude/cli/swarm/__init__.py:150 registers run_cmd; commands.py public run entry reaches _run_resume_branch; signatures unchanged. Import-dependent graph rows capped10/99 after higher-limit retry, graph:truncated, not exhaustive callers. Current source Read confirms registry call150 and resume call1717; modified-source rows are leads.
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
