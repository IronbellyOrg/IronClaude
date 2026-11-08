0e3f563466981fcebe2faa51b2b5f06203b5470d
Review one task for spec compliance.

Task brief: Task 1: Measure the serial idle baseline (D1). Run, on the current HEAD with no other load: `LL_SPEED_RESULTS=<package>/artifacts/d1-serial-idle.md uv run pytest tests/hooks/test_launch_level_guard.py -k test_speed_large_commands -p no:xdist -rP`. The test itself samples each of the 4 cases 100 times (well above the 30-run floor); the report file records per-case median/p95/max, and `-rP` also prints the rows as the fallback source. If the LL_SPEED_RESULTS file is not written or is empty, fall back to parsing the `-rP` row output into the artifact by hand. Acceptance criteria: `artifacts/d1-serial-idle.md` exists and holds, for each of the 4 cases (`heredoc-git-words-64KB`, `backslash-lines-64KB`, `git-status-lines-64KB`, `1MB-big`), the runs count, median and max in seconds (or ms as printed), plus the command used. The slowest 64 KB max and the slowest overall max are stated in a one-line summary at the top of the artifact. AC ids: T1.AC1, T1.AC2.
Global constraints: Guard scripts src/superclaude/hooks/scripts/launch-level-guard.sh and launch-job-identity.sh must not change. Test and CI-config changes only; if no limit <= 2.5 s both clears the noise and fails the 10x wrapper, record the outcome and stop (serial CI step is proposed, not implemented). The 1 s documented figure stays a reported design target. UV only for Python. Stage .dev/tasks; never stage .claude/ (except .claude/settings.json) or .dev/issues/. No push, no PR, no merge. The numeric limit comes from the measurements recorded under artifacts/.
Start sha: 0e3f563466981fcebe2faa51b2b5f06203b5470d
Diff against the start snapshot: no tracked-file changes. One new untracked task-owned file: .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d1-serial-idle.md (full contents at that path; Read it). Its line 1 is an executor-added one-line summary; the rest is the test module's own LL_SPEED_RESULTS report (command, host, method, per-case table with Runs/Median/p95/Target/Result). A second new untracked file is this package's ledger/progress files (progress.md, PLAN pin, T1 start line), not part of the task's product output.
Delta diff from the previous reviewed tree: one added line at .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d1-serial-idle.md:2: "# COMMAND USED (executor-added): LL_SPEED_RESULTS=.dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d1-serial-idle.md uv run pytest tests/hooks/test_launch_level_guard.py -k test_speed_large_commands -p no:xdist -rP"
Earlier blocking findings of this start: F1.1 ac=T1.AC1 at=.dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d1-serial-idle.md:7 anchor=amiss:the AC words "plus the command used" false:tests/hooks/test_launch_level_guard.py:1097 chk=amiss:y,false:y,harm:n,constraint:n family=cmd-provenance fix=Add one executor-added provenance line beside line 1; leave the generator line 7 as-is covers="plus the command used"
Saved-probe re-check hit locations (may be empty): (empty)

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
