acaeaabba1320e72bf0bdfcc6adfec7dadf9999a
Review one task for spec compliance.

Task brief: Task 3: Write the spec errata note. Source plan: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md, section "Task 3" (read that section and the Constraints section; the plan text is the task brief). The spec file is /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md (the spec; "PF" is its program folder). Acceptance criteria, in source order: T3.AC1 The spec no longer says the scored table is empty, will not exist in time, or has 30 to 40 rows, or that the held-out half is 15 to 20 rows (`grep -n "15 to 20\|was empty\|30 to 40 rows\|30 or more scored"` over the spec returns no stale claim). T3.AC2 `./artifacts/spec-reconciliation.md` lists each edited line with its old and new text, and records the result of the re-run Grep over section 17 and Appendix A. T3.AC3 Section 7.2 of the spec carries the M, C and E sentence with a pointer to `08-test/results.md` and no pointer to a file of this package. T3.AC4 The RT1 row of section 13.2 reads "any real blocker found in a Medium list", the RK15 mitigation no longer contains `M10b`, and the section 12 stage 3 row names RT1 and does not name RT2 or M12. T3.AC5 The spec carries the one line "Version 1 scope: see cuts-debate/final-cuts.md in this folder" once, directly under the `Date:` line, and the file `cuts-debate/final-cuts.md` exists in PF. Also part of the task text: the spec is edited only where the program results made it stale (the nine edit bullets of Task 3), "No other line of the spec is edited and no definition, exit number or staging decision is drafted into it".
Global constraints: the plan's `## Constraints` section (in the plan file named above). Quote it when you answer quoted-constraint-breach.
Start sha: acaeaabba1320e72bf0bdfcc6adfec7dadf9999a
Diff against the start snapshot: run `git diff acaeaabba1320e72bf0bdfcc6adfec7dadf9999a -- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` from /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel (that tree-ish is the start snapshot; it is the whole tracked-file diff of this task). The task also wrote new untracked files below /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/artifacts/: spec-reconciliation.md and spec-before-errata.md (a copy of the spec as it was before the edits). Reference inputs you may read: PF/cuts-debate/final-cuts.md, PF/08-test/results.md, PF/05-scoring/consensus.md, PF/OPEN-QUESTIONS.md. Codegraph context: index_state: fresh; checked_at: 2026-11-16T21:25:21Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel. Call codegraph only when index_state: fresh, never to widen scope. Q2b: no code symbol was changed (Markdown only); no dependents list.
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
