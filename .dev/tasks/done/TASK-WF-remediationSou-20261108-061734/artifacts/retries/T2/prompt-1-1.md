cfb87ea3ff0e946f01d091dcbbab6b294dbe7908
Review one task for spec compliance.

Task brief: Task 2: Measure the xdist-idle arm (D4). Run the same test with one xdist worker and no load: `LL_SPEED_RESULTS=<package>/artifacts/d4-xdist1-idle.md uv run pytest tests/hooks/test_launch_level_guard.py -k test_speed_large_commands -n 1`. On current HEAD the rows may print `NOT ASSERTED` verdicts; the timing values are still recorded. This arm isolates the `PYTEST_XDIST_WORKER` plumbing from CPU contention. Acceptance criteria: `artifacts/d4-xdist1-idle.md` exists with per-case runs/median/max and the command used. A one-line comparison against Task 1's artifact states whether the xdist medians/maxima are within noise of the serial arm (delta under about 10 percent) or clearly above. AC ids: T2.AC1, T2.AC2.
Global constraints: Guard scripts src/superclaude/hooks/scripts/launch-level-guard.sh and launch-job-identity.sh must not change. Test and CI-config changes only; if no limit <= 2.5 s both clears the noise and fails the 10x wrapper, record the outcome and stop (serial CI step is proposed, not implemented). The 1 s documented figure stays a reported design target. UV only for Python. Stage .dev/tasks; never stage .claude/ (except .claude/settings.json) or .dev/issues/. No push, no PR, no merge. The numeric limit comes from the measurements recorded under artifacts/.
Start sha: cfb87ea3ff0e946f01d091dcbbab6b294dbe7908
Diff against the start snapshot: no tracked-file changes (note: installing pytest-xdist with `uv pip install "pytest-xdist>=3.5,<4"` matches how CI itself provisions it, test.yml:26-29, and changes only the .venv, which is gitignored; no tracked file changed). One new untracked task-owned file: .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d4-xdist1-idle.md (full contents at that path; Read it). Line 1 is an executor-added one-line summary including the D4-vs-D1 comparison; line 2 is the executor-added COMMAND USED provenance line; the rest is the test module's LL_SPEED_RESULTS report (its own Run: line is generator boilerplate, left as-is). The package ledger/progress files also changed (T1 complete line, T2 start line); not product output.
Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d4-xdist1-idle.md:2 (COMMAND USED line, the coupled cmd-provenance fix from T1's probe-1-1)

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
