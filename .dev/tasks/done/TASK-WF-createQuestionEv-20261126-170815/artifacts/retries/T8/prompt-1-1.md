bfef77f4e19483623c6031d7329e4e04fdd1dfae
Review one task for spec compliance.

Task brief: Task 8 of the plan /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md (the section '## Task 8:' with its body and its 'Acceptance criteria:' bullets). AC ids in bullet order: T8.AC1 = the first bullet, T8.AC2 = the second, T8.AC3 = the third. Context: raw run output lives under runs/<run name> of the scratch directory /tmp/createQuestionEv-scratch (named in Task 4); Task 9 scans it and copies scanned files to ./artifacts/runs/. The three deep runs are /tmp/createQuestionEv-scratch/runs/deep-additions-only, deep-contradiction and deep-flag-preserved. 'The same file set as Task 6' means the file set of runs/quick-additions-only and runs/quick-contradiction (summary.json, record.md, gh.log, gh-posted/, dev-issues/<fake issue number>/issue-body.md and draft-notes.md, final-output.txt, read-files.txt, transcripts/, screens, driver.log; the contradiction run adds at-question-1-*.md and screen-question-1.txt). The runs are interactive tmux sessions (decision in ./artifacts/harness-feasibility.md); the event log is the transcripts under runs/<name>/transcripts/. Each record.md was built by the deterministic scripts /tmp/createQuestionEv-scratch/addition_report.py and contradiction_report.py (the keyword rule for 'present in' is approximate and says so), then a '## Task 8 facts and findings' section was appended by the orchestrator. The first attempt of deep-contradiction is kept apart as runs/deep-contradiction-attempt1-invalid: the harness driver ended it while the deep worker was still running (an infrastructure failure; its record says so); the plan's one infrastructure repeat was used and the repeat is runs/deep-contradiction. The chain logs are /tmp/createQuestionEv-scratch/logs/chain-deep.log (deep-additions-only and the invalid attempt) and chain-deep2.log (the repeat and deep-flag-preserved); each chain reads the pending fork-activity list before and after every run (/tmp/createQuestionEv-scratch/review_pending.py, cleared entries in /tmp/createQuestionEv-scratch/pending-cleared.log) and the harness checks the STOP file at the start of every run. The user's standing rule is in /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/issues/834/issue-summary.md.
Global constraints: The '## Constraints' section of the same plan file (/home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md), all of it; read it.
Start sha: bfef77f4e19483623c6031d7329e4e04fdd1dfae
Diff against the start snapshot: The only repository file this task changed is the harness script /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness/run_create.py (the driver's idle detection: a running background agent shown on the screen, or the footer 'for shortcuts · ↓ to manage', counts as busy; the quiet threshold is 90 seconds for deep and 25 otherwise). Its diff against the start copy is saved at /tmp/impl-review/T8-diff-1.txt; read it and the live file. Task 6 and Task 7 folders (quick and standard runs) are separate tasks; ignore them.
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
