828be9d8645525e9144a71c10c51d8b2f3be4400
[Orchestrator preamble sent before the template, outside it: "You are a read-only spec-compliance reviewer. Do not edit, create or delete any file; read-only shell commands (git grep, git worktree list, cat, wc) are allowed for live checks. Return your review as text." Orchestrator postscript sent after the template: "Use F1.1, F1.2, ... as finding ids." The template text below is unmodified.]
Review one task for spec compliance.

Task brief: Task T1 of the plan /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md, lines 33-51 (Read them verbatim; "./artifacts/" means /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/artifacts/). AC ids: T1.AC1 = plan line 49, T1.AC2 = plan line 50, T1.AC3 = plan line 51.
Global constraints: the same plan, section "## Constraints", lines 17-29 (Read them verbatim).
Start sha: 828be9d8645525e9144a71c10c51d8b2f3be4400
Diff against the start snapshot: /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/artifacts/q2/T1-r1-1.diff (four new untracked files; the diff holds their full contents; the files themselves are at the same paths under ./artifacts/). Repository root for live checks: /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths
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
