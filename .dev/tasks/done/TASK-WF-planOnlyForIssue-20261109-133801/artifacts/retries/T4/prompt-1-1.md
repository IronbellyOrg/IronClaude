3171a298fb0dea246fb35a35f2f92e01998c68e4
Review one task for spec compliance.

Task brief: Read Task 4 and its five ACs at lines 127-155 of /home/coder/workspaces/worktrees/IronClaude/issue-462/.dev/tasks/to-do/TASK-WF-planOnlyForIssue-20261109-133801/TASK-WF-planOnlyForIssue-20261109-133801.md. Assign T4.AC1-AC5 in bullet order. Read the full diff, changed current sections of each named delivery file, current focused tests, and the complete artifacts/task4-dispatch-coverage.md and task4-tests-initial.log under that package. Inspect the connected dispatch paths and help for contradictions, not just the diff wording. Review this task only; Task 5 plugin/help completion is future scope. Runtime tools are only Read, Grep, Glob. Return complete review text for parent-owned artifacts/retries/T4/review-1-raw.md; never Write, Bash, SendMessage or spawn. Begin adversarially; if zero findings survive include a brief Self-audit. Keep each Read under 100 lines and search output below 40 lines. Actual backend/tool use will be audited. No executable parser or live dispatch was built or tested.
Global constraints: Read plan Constraints at lines 17-31. The user authorized implementation of this existing plan. On 2026-11-09 they explicitly overrode Task 3's pending retry/re-review: preserve its user-accepted missing verdict without reopening it. This does not waive Task 4 verification. No paid behavioral experiments, historical replay, installations, global configuration changes, commits, pushes, PRs, merges or external posts. Historical cause remains unproved; no second worker_done. Never read .dev/issues or .dev/troubleshoot; never read retries. Do not judge future Task 5 or change any file. Requested aliases/markers are not served-backend evidence. Preserve run pipeline and suite behavior.
Start sha: 3171a298fb0dea246fb35a35f2f92e01998c68e4
Diff against the start snapshot: Read /home/coder/workspaces/worktrees/IronClaude/issue-462/.dev/tasks/to-do/TASK-WF-planOnlyForIssue-20261109-133801/artifacts/task4-review.diff in full and the current delivery files. Reviewed tree: c355ea5c7a497ac06217ea91f7b4ad94bae149e5.
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
