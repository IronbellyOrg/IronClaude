13d4ac5d1aca6c9692fc3c1ec643ec91dd7c2952
Review one task for spec compliance.

Task brief: Task 11 of the plan /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md (the section '## Task 11:' with its body and its 'Acceptance criteria:' bullets). AC ids in bullet order: T11.AC1 = the first bullet, T11.AC2 = the second, T11.AC3 = the third. Deliverable: /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/pr-notes.md. Verify it against /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/gates.md, issue-state.txt, evidence-matrix.md and secret-scan.txt, the story's Decided block in /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/issues/834/issue-summary.md (the pull request body must quote it), and the Generator-Constraint path filter in /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.github/workflows/contract3-generator-constraint-lint.yml. The body must say that every GitHub call in the runs went to the fake gh with the other write paths blocked and mention no live issue creation. You have no shell: judge the path statements from the files you can read (git status at session start lists the untracked paths: .dev/issues/834/, .dev/reflect/..., .dev/tasks/..., tests/skills/test_issue_create_question_scenarios.py).
Global constraints: The '## Constraints' section of the same plan file (/home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md), all of it; read it.
Start sha: 13d4ac5d1aca6c9692fc3c1ec643ec91dd7c2952
Diff against the start snapshot: This task changed no repository file except its own output artifacts/pr-notes.md. After the first review three sentences were reworded: pr-notes.md line 18 (the live calls are reads only, and include the fork-activity snapshots), pr-notes.md line 3 ('.dev/tasks is to be staged'), and evidence-matrix.md line 3 (every GitHub call inside a run's model session went to the fake gh; the only live calls were read-only).
Delta diff from the previous reviewed tree (empty on the first review): The three rewordings listed above are the whole change since the previously reviewed tree; read pr-notes.md:3,18 and evidence-matrix.md:3.
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B2 ac=T11.AC2 at=.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/pr-notes.md:18 anchor=.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/pr-notes.md:18 chk=n,y,n,n family=live-call-wording fix=reword the sentence that says the one live call is a read of issue 834: the live calls are reads only and also include the fork-activity snapshots of every run first=A1 origin=new: the sentence "The one live call of this work is a read of issue 834's state" is false against the fork_activity block of every summary.json.
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
