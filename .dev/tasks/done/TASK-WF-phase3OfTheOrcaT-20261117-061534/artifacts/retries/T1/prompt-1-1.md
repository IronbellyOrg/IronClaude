07ece05644468d3dd1ab66ec04a29ba5991b2365
Review one task for spec compliance.

Task brief: Task 1 of the plan /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/TASK-WF-phase3OfTheOrcaT-20261117-061534.md ("## Task 1: Write the phase 3 contract into the spec files", read that section). Its acceptance criteria, ids T1.AC1 to T1.AC4 in source order: T1.AC1 adapter-contract.md no longer says that `payload` is not kept, and states the size cap, the id pattern, the cut mark, the four unlinked reasons with their exact texts and the never-kept list; T1.AC2 rendering-rules.md contains the keys `n`, `p` and `Esc` in the global key list (line 21), the `DECISION DESK` block with its texts, the evicted-selection wording, the one-stacked-block clause, the "only the question text is clipped" sentence and the named marker, and no longer says question lines are "not selectable" without the link-switch qualification; T1.AC3 acceptance-tests.md has rows T57 to T66 after T56, each with a test file name that Tasks 2 to 6 create or extend; T1.AC4 `grep -n "not kept"` on adapter-contract.md shows only the narrowed rule.
Global constraints: the plan's "## Constraints" and "## Out of scope" content in the plan file above (read that section).
Start sha: 07ece05644468d3dd1ab66ec04a29ba5991b2365
Diff against the start snapshot: the full diff is in the file /tmp/impl-T1-diff.patch (read it; it covers the three files this task edited, under .dev/issues/409/bmad/spec-orca-observer/). Codegraph context: index_state: fresh; checked_at: 2026-11-17T07:27:40Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp. Call codegraph only when index_state: fresh, never to widen scope. Q2b ran on the Grep/Read floor: this task changes documents only, no code symbol, so there are no dependents.
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
