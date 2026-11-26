20a5b4889a1482fde59eefb34342aebd4e734312
Review one task for spec compliance.

Task brief: Task 4 of the plan /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md (the section '## Task 4:' with its body and its 'Acceptance criteria:' bullets). AC ids in bullet order: T4.AC1 = the first bullet, T4.AC2 = the second, T4.AC3 = the third, T4.AC4 = the fourth. One context fact for judging T4.AC2: the plan's Task 4 says that when a dry print-mode run shows no AskUserQuestion event the decision section is a stop report, and the user's standing rule recorded in /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/issues/834/issue-summary.md (the section 'Rule from Clay for all E2 stories') says not to stop to ask unless something is ambiguous or two sources conflict, and to record obvious answers in the Decided block.
Global constraints: The '## Constraints' section of the same plan file (/home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md), all of it; read it.
Start sha: 20a5b4889a1482fde59eefb34342aebd4e734312
Diff against the start snapshot: New untracked file .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness-feasibility.md (its diff against the start snapshot, which does not contain the path, is the full file content, saved at /tmp/impl-review/T4-diff-1.txt). Read it, and read the live file at /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness-feasibility.md. The raw evidence it quotes is in the scratch directory /tmp/createQuestionEv-scratch (dry-A.jsonl, dry-B.jsonl, dry-C.jsonl, dry-D.jsonl, dry-G.jsonl, dry-F.question-screen.txt, gh-stub-dry.log, claude-help.txt and home/.claude/projects/*/*.jsonl, the transcript of dry run F); check claims against it. The src files whose hashes it lists are under /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/src/superclaude/. The seeded home is /tmp/createQuestionEv-scratch/home. No source or test file changed in this task; the product of this task is the one file named above.
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
