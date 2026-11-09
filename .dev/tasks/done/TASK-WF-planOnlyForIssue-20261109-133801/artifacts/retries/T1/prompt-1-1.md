68f058e2aeb47a04fbd759c68653a368e529ed22
Review one task for spec compliance.

Task brief: Read the full Task 1 text (lines 35-60) in .dev/tasks/to-do/TASK-WF-planOnlyForIssue-20261109-133801/TASK-WF-planOnlyForIssue-20261109-133801.md. Its six Acceptance criteria bullets are T1.AC1 through T1.AC6 in source order. Review only that task, not the dependent tasks. The task's declared evidence output is artifacts/task1-default-boundary.md and its referenced test logs. All paths are relative to /home/coder/workspaces/worktrees/IronClaude/issue-462. Return your complete review data; the parent persists it because this restricted profile has no Write tool.
Global constraints: Read the plan's complete Constraints section (lines 17-31), plus the explicit Task 1 instructions. The user subsequently authorized implementation with "Override and proceed with implementation" and "Continue the implementation". The no-model-execution wording is explicitly limited to the planning run, not a prohibition on this required implementation review. No historical cause is established. Use only this profile's read-only tools; no delegation, runtime probes, modifications or external publication. Model routing was checked separately by the parent and is not a product-compliance finding.
Start sha: 68f058e2aeb47a04fbd759c68653a368e529ed22
Diff against the start snapshot: Read the complete saved Q3 diff at .dev/tasks/to-do/TASK-WF-planOnlyForIssue-20261109-133801/artifacts/task1-review.diff, then independently inspect the live delivery files as needed. This is the full diff against the task's start snapshot for its six touched paths, not an implementer summary.
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
