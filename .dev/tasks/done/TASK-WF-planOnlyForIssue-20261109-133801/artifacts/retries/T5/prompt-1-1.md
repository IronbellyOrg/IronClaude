e1b4a3a15d33066fb845bbf2666f1794120b3235
Review one task for spec compliance.

Task brief: Read Task 5 and its six ACs at lines 159-186 of /home/coder/workspaces/worktrees/IronClaude/issue-462/.dev/tasks/to-do/TASK-WF-planOnlyForIssue-20261109-133801/TASK-WF-planOnlyForIssue-20261109-133801.md. Assign T5.AC1-AC6 in bullet order. Read the complete task diff and current three delivery files, plus artifacts/task5-delivery.md and its named machine logs. Inspect current resolver/launcher/shim sections where needed to check README claims, and source/help sections covered by the inventory to check that it is not a blanket word ban. Confirm plugin changes preserve unrelated differences. FINAL/archive follow Task 5 and remain executor-owned, not an absent Task 5 implementation. Return complete text for parent-owned artifacts/retries/T5/review-1-raw.md using only Read/Grep/Glob, never Write/Bash/SendMessage/spawn. Begin adversarially and give a Self-audit if no findings survive. Each Read stays under 100 lines and each search under 40 lines. Actual backend and tools will be audited. Do not trust a claim of tests passing without reading the logs.
Global constraints: Read plan Constraints at lines 17-31. Implementation of the existing plan is authorized. The user's 2026-11-09 explicit override accepts Task 3's bounded test fix without adviser/revert/re-review or its ordinary ruling-eligibility gate; its earlier missing verdict remains unchanged. Do not reopen it. No model experiments, historical replay, home installs, global settings changes, Coder-source changes, new worktrees, commits, pushes, PRs, merges or external posts. No second worker_done. Never read .dev/issues or .dev/troubleshoot. .dev/tasks evidence is staged; .claude mirrors, .dev/issues and root artifacts are not staged. Historical cause is unknown; static selection evidence is not live dispatch or served-backend proof. Task 5 does not build or repair the incomplete plugin protocol distribution. No files may be changed by the reviewer.
Start sha: e1b4a3a15d33066fb845bbf2666f1794120b3235
Diff against the start snapshot: Read /home/coder/workspaces/worktrees/IronClaude/issue-462/.dev/tasks/to-do/TASK-WF-planOnlyForIssue-20261109-133801/artifacts/task5-review.diff in full and the current delivery files. Reviewed tree: 919053b5bb46fc673610990bcc12733d0da5a2d1.
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
