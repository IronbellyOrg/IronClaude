a86192a99fa91470898f36951578ecd67c5e6d75
Review one task for spec compliance.

Task brief: Task 9 of the plan /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md (the section '## Task 9:' with its body and its 'Acceptance criteria:' bullets). AC ids in bullet order: T9.AC1 = the first bullet, T9.AC2 = the second, T9.AC3 = the third, T9.AC4 = the fourth. Deliverables are in /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/: secret-scan.txt, issue-state.txt, evidence-matrix.md, and the scanned copies runs/ (the run folders), logs/ (the chain logs) and scratch-scripts/ (the record scripts and the pending-review log). The raw originals are under /tmp/createQuestionEv-scratch/ (runs/, logs/); the copies are the scanned files (one finding was redacted in the copy; the original is untouched). Count questions and posts only from the event log (runs/<run>/transcripts, summed in summary.json) and the fake gh log (runs/<run>/gh.log). Verify the matrix numbers against the cited raw files (summary.json:22-26 observed counts, the gh.log lines, the record tables), the quoted acceptance criteria against the plan section, the per-criterion citations against the real source lines (src/superclaude/skills/sc-issue-protocol/refs/create.md, templates/draft-notes.md, SKILL.md, refs/claim.md, templates/launch-prompt.md, src/superclaude/commands/issue.md, docs/designs/sc-issue-command.md, docs/user-guide/commands.md, tests/skills/test_issue_protocol.py, tests/skills/test_issue_create_question_scenarios.py), and the two AC4 diffs (git diff origin/integration...HEAD -- the three files, git diff HEAD -- the three files: both must print nothing). The verdict words allowed are 'delivered by 852', 'delivered by this work', 'partly evidenced', 'not met' (AC6: pending). The standing rule of the user is in /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/issues/834/issue-summary.md.
Global constraints: The '## Constraints' section of the same plan file (/home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md), all of it; read it.
Start sha: a86192a99fa91470898f36951578ecd67c5e6d75
Diff against the start snapshot: Repository files this task created or changed: artifacts/secret-scan.txt, artifacts/issue-state.txt, artifacts/evidence-matrix.md, artifacts/runs/**, artifacts/logs/**, artifacts/scratch-scripts/**; artifacts/harness/run_create.py (one line of the self-test: the fake key header is now built from two string pieces so no staged file holds the literal; the diff against the Task 8 reviewed copy is /tmp/impl-review/T9-diff-1.txt); artifacts/harness/self-test.txt (refreshed, same layout, 27 PASS); artifacts/retries/T6/artifacts-2/harness/run_create.py (the literal redacted in place by the scan tool). Nothing under src/ or tests/ changed in this task.
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
