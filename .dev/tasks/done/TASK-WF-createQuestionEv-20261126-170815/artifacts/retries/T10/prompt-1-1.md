f4d8f099df8827436b74d5463c596929bf998d51
Review one task for spec compliance.

Task brief: Task 10 of the plan /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md (the section '## Task 10:' with its body and its 'Acceptance criteria:' bullets). AC ids in bullet order: T10.AC1 = the first bullet, T10.AC2 = the second, T10.AC3 = the third. Deliverable: /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/gates.md, with the raw gate output in /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/gates/ (full-suite output there has its PASSED lines removed; the original is /tmp/createQuestionEv-scratch/gates/full.txt). The gates were run from the repository root /home/coder/workspaces/worktrees/IronClaude/issue-834-rest after the branch was fast-forwarded to origin/integration. Check the recorded commands, exit codes and counts against the raw output, the failing-test analysis (you may rerun nothing that writes; you have no shell: read the raw files and the test source tests/cli/eval/test_claude_process_adapter.py), and that the claims about git status ('nothing changed under src/, nothing staged') are consistent with the files you can read. The standing rule of the user is in /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/issues/834/issue-summary.md.
Global constraints: The '## Constraints' section of the same plan file (/home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md), all of it; read it.
Start sha: f4d8f099df8827436b74d5463c596929bf998d51
Diff against the start snapshot: This task changed no repository file except its own outputs: artifacts/gates.md and artifacts/gates/*. It ran `make sync-dev`, which writes only the gitignored .claude/ folder.
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
