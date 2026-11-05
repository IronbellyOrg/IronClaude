0826837c8fa642fcb1a313d99be7822aabb6d960
You are a read-only spec-compliance reviewer. Do not edit, create or delete any file; read-only commands (git grep, git diff, git diff --cached --name-only, cmp, cat, wc) are allowed for live checks. Do not run make or pytest; the saved logs are the evidence. Return your review as text.

Review one task for spec compliance.

Task brief: Task T7 of the plan /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md, lines 150-160 (Read them verbatim; "./artifacts/" means /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/artifacts/). AC ids: T7.AC1 = plan line 157, T7.AC2 = plan line 158, T7.AC3 = plan line 159, T7.AC4 = plan line 160; the body at plan line 154 is the task instruction.
Global constraints: the same plan, section "## Constraints", lines 17-29 (Read them verbatim).
Start sha: 0826837c8fa642fcb1a313d99be7822aabb6d960
Diff against the start snapshot: /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/artifacts/q2/T7-r1-1.diff (three plugins/superclaude files modified; ./artifacts/t7-cmp.txt, t7-verify-sync.txt, t7-staged-claude.txt are new). The pytest log ./artifacts/t7-pytest.txt (452 lines) is also new and is not inlined in the diff; read it directly. `make sync-dev` writes only the gitignored `.claude/` mirror. Repository root for live checks: /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths
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

Use F1.1, F1.2, ... as finding ids.
