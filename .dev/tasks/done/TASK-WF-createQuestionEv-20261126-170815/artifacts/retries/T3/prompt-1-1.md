51d43a5148bbbdbd44e6f055a0ef62060e95979f
Review one task for spec compliance.

Task brief: Task 3 of the plan /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md (the section '## Task 3:' with its body and its 'Acceptance criteria:' bullets). AC ids in bullet order: T3.AC1 = the first bullet, T3.AC2 = the second, T3.AC3 = the third, T3.AC4 = the fourth.
Global constraints: The '## Constraints' section of the same plan file (/home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md), all of it; read it.
Start sha: 51d43a5148bbbdbd44e6f055a0ef62060e95979f
Diff against the start snapshot: File tests/skills/test_issue_create_question_scenarios.py (untracked; it already existed in the start snapshot with Tasks 1 and 2 content). The diff of the live file against the start snapshot copy is saved at /tmp/impl-review/T3-diff-1.txt. Read it, and read the live file at /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/tests/skills/test_issue_create_question_scenarios.py. The files the tests read are /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/src/superclaude/skills/sc-issue-protocol/refs/create.md and /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md; the helpers are in /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/tests/skills/test_issue_protocol.py (unchanged). Test results: the new module 46 passed; tests/skills/test_issue_protocol.py plus the new module 249 passed; the 17 existing tests selected by -k 'contradiction or draft_notes or create_question or additions or evidence' in tests/skills/test_issue_protocol.py passed (17 passed, 186 deselected).
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
