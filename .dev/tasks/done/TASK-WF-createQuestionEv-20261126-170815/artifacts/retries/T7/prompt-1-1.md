996c438bf27a59178b4a1ea17bb20bf93a3cc4a0
Review one task for spec compliance.

Task brief: Task 7 of the plan /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md (the section '## Task 7:' with its body and its 'Acceptance criteria:' bullets). AC ids in bullet order: T7.AC1 = the first bullet, T7.AC2 = the second, T7.AC3 = the third, T7.AC4 = the fourth. Context: raw run output lives under runs/<run name> of the scratch directory /tmp/createQuestionEv-scratch (named in Task 4); Task 9 scans it and copies scanned files to ./artifacts/runs/, so the four run folders of Task 7 are read from /tmp/createQuestionEv-scratch/runs/standard-additions-only, standard-contradiction, standard-multi-contradiction and standard-flag-preserved. 'The same file set as Task 6' means the file set of runs/quick-additions-only and runs/quick-contradiction (summary.json, record.md, gh.log, gh-posted/, dev-issues/<fake issue number>/issue-body.md and draft-notes.md, final-output.txt, read-files.txt, transcripts/, screens, driver.log; the contradiction runs add at-question-1-*.md and screen-question-1.txt). The runs are interactive tmux sessions (decision in ./artifacts/harness-feasibility.md); the event log is the transcripts under runs/<name>/transcripts/. Each record.md was built by the deterministic scripts /tmp/createQuestionEv-scratch/addition_report.py and contradiction_report.py from the raw files (the keyword rule for 'present in' is approximate and says so), then a '## Task 7 facts and findings' section was appended by the orchestrator. The runs were executed before the ledger start line of this task; the harness script they used is the one Task 6 finished, and --reanalyse (read-only: it writes no STOP or PENDING-REVIEW file) re-derived each summary.json from the saved raw data; the counts and every other field equal the originals. No repository file was changed by this task; its deliverables are the four run folders in the scratch directory. The user's standing rule is in /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/issues/834/issue-summary.md. The fork-activity items were read and cleared by the orchestrator: see /tmp/createQuestionEv-scratch/pending-cleared.log.
Global constraints: The '## Constraints' section of the same plan file (/home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/TASK-WF-createQuestionEv-20261126-170815.md), all of it; read it.
Start sha: 996c438bf27a59178b4a1ea17bb20bf93a3cc4a0
Diff against the start snapshot: This task changed no repository file (git diff of the repository against the start tree shows nothing for this task). Its output is the four run folders and their records in /tmp/createQuestionEv-scratch/runs/ and the shell logs in /tmp/createQuestionEv-scratch/logs/. The deep-depth folders (Task 8) and the quick folders (Task 6) are separate tasks; ignore them.
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
