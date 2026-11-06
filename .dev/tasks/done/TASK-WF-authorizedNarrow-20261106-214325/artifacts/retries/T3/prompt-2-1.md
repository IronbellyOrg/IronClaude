0a59e7cf7531f1547580a9daf0ca7222f099062f
Review one task for spec compliance.

Task brief: Read Task 3 and its three Acceptance criteria as T3.AC1-T3.AC3 from .dev/tasks/to-do/TASK-WF-authorizedNarrow-20261106-214325/TASK-WF-authorizedNarrow-20261106-214325.md in /home/coder/workspaces/worktrees/IronClaude/hook-launch-level-394. Review distribution, hook registration and regression fixtures, not later live observation tasks.
Global constraints: Read that plan's complete Constraints. Scope is per-job logical session identity with unrestricted humans, not full enforcement or a hostile-user sandbox. No root/global install, unrelated edits or real protected-branch pushes.
Start sha: 0a59e7cf7531f1547580a9daf0ca7222f099062f
Diff against the start snapshot: Read ./artifacts/task3-source.diff beside this plan. Changed files are src/superclaude/cli/install_hooks.py, src/superclaude/hooks/hooks.json, tests/cli/test_install_hooks.py, tests/hooks/test_freshness_subagent_start_policy.py, plugins/superclaude/hooks/hooks.json and the new plugins/superclaude/hooks/scripts/launch-job-identity.sh. The freshness test explicitly pins the whole Bash hook set and its exact set/comment were updated for this required new registration. Worktree root is /home/coder/workspaces/worktrees/IronClaude/hook-launch-level-394. The fix also changes src/superclaude/hooks/scripts/launch-job-identity.sh and tests/hooks/test_launch_job_identity.py to repair the newly registered entry point.
Delta diff from the previous reviewed tree (empty on the first review): Read ./artifacts/task3-fix-delta.diff beside this plan.
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T3.AC2 at=plugins/superclaude/hooks/scripts/launch-job-identity.sh:25 anchor="Without positively governed session state it is inert for ordinary sessions." chk=y,n,n,n family=ordinary-dependency-gate fix=Keep unbound ordinary calls silent even when other launch state exists and UV is missing; add that regression covers="Without positively governed session state it is inert for ordinary sessions." first=start origin=inherited: The registered entry point checks UV after only checking the launch directory, not the event's binding. An isolated unbound event with existing state and PATH=/nonexistent exits 2 instead of remaining inert. The quoted Task3 AC lifts the inherited cap.
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
