c637be7c75d269eca8fc89091dce6d9f0005050c
Review one task for spec compliance.

Task brief: Task 1 of /home/coder/workspaces/worktrees/IronClaude/hook-launch-level-394/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/TASK-WF-implementDocsDes-20261106-210206.md. Read its Task 1 body and five acceptance bullets as T1.AC1 through T1.AC5. The current design's section 19.1 defines the blocking actor-context prerequisite. Read actual task outputs in the diff slot, not an implementer summary.
Global constraints: Read the plan's complete Constraints section; preserve unrestricted same-worktree human pushes; Task 1 is a blocking prerequisite and unsupported lifecycle is not a PASS; no invented launcher/harness integration, production activation, global settings changes, real protected-branch push, commit or external post. Preserve pre-existing unrelated files. Task 1 must retain log-only evidence and stop before Task 2 if it cannot meet isolation.
Start sha: c637be7c75d269eca8fc89091dce6d9f0005050c
Diff against the start snapshot: Three newly created task-output files under /home/coder/workspaces/worktrees/IronClaude/hook-launch-level-394/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/: actor-context-probe.sh, actor-context-observed.json, actor-context-report.md. None existed in the start snapshot. Read their entire current contents as the new-file diff. Production source files are unchanged by this task. The pre-existing dirty design is not a task-output change.
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
