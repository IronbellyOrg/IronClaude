389b3504e14fc30faaa1be079ba1a6ab608cce29
Review one task for spec compliance.

Task brief: ## Task 6: Observe same-worktree human pushes against governed pushes in a disposable bare repository

Depends on: Task 1

In a temporary directory create a bare repository and a clone with a linked worktree, install a log-only pre-push hook in that fixture clone only (it appends the selector status of the pushing process, via the identify action of src/superclaude/hooks/scripts/launch-job-identity.sh, and the destination field of each pushed ref to a log, then exits 0 so it vetoes nothing), and push to branches named main and master of the disposable bare repository only. Pin the throwaway HOME (the helper's store() reads HOME) and an isolated git configuration for both actors. The governed pusher is a job started through the helper's own run action under a governed session record in the throwaway HOME, so it is labelled controlled; no real Claude run is spent on this task. The plain shell is started by the runner, not by a person at a terminal, so it is labelled controlled as a human-style shell, and the case of a person in an Orca terminal is recorded unavailable with that missing interface. The existing real-Git test (tests/hooks/test_launch_job_identity.py:1291-1354, with the human push at :1306-1331 and the refused governed push at :1347-1348) is the controlled baseline; this task adds a log-only hook and the concurrent run. Run the human-style push to main and the governed push to master concurrently in the same worktree, so a same-ref race cannot hide whether the human push landed. Record the selector status the hook saw for each and the resulting refs of the bare repository.

Acceptance criteria:
- ./artifacts/human-vs-governed-push.json shows, for each push, the actor started from (plain shell or governed job), the selector status the hook logged, the pushed destination ref, and the bare repository's refs before and after; the plain-shell pushes are logged ordinary and the governed-job pushes are logged governed with the governed session id, and every entry is labelled controlled with its reason; the Orca-terminal human case is recorded unavailable with the missing interface named.
- A concurrent run shows the human push and the governed push in the same worktree at the same time with different logged statuses, and the human push reaches the bare repository.
- No remote other than the temporary bare repository is configured or contacted, shown by the fixture's git remote listing in the artifact, and the fixture's pre-push hook is the only hook installed and exists only in the temporary directory.
Global constraints: ## Constraints

- The authoritative design is docs/designs/sc-issue-launch-level-hook.md, section 19 (19.1 for the required cases and 19.7 for the merged job-identity contract). The gap list is the six findings F2.1 to F2.6 in review-2.md of the blocked package, at artifacts/retries/T1/ inside package TASK-WF-implementDocsDes-20261106-210206 (a package in the to-do folder of .dev/tasks/). The identity helper under test is src/superclaude/hooks/scripts/launch-job-identity.sh; the earlier real-CLI observation helper is tests/hooks/fixtures/launch_level/live_probe.py. Read all of them; edit none of them.
- Do not modify, move or re-run package TASK-WF-implementDocsDes-20261106-210206, and do not modify the done package TASK-WF-authorizedNarrow-20261106-214325. Their files are read-only inputs.
- This plan observes and reports only. It adds no production hook, no registration, no installer change, no change under src/, plugins/ or tests/, and it never configures a real repository's hooks. Git experiments run only in disposable local repositories and disposable local bare repositories created under a temporary directory. No push to a real origin or any protected branch of a real remote. No interaction with the SuperClaude upstream repository.
- Real Claude runs use a throwaway HOME and CLAUDE_CONFIG_DIR, an explicit --settings file and --setting-sources "", exactly like tests/hooks/fixtures/launch_level/live_probe.py. Never edit the user's real Claude settings. Each real Claude run is capped with --max-budget-usd 0.25 and a bounded timeout, except the one interactive /clear run in Task 3, which the owner authorized on 2026-11-08 (review decision M2-02) as a separately bounded run because the installed CLI restricts --max-budget-usd to --print, and the whole plan makes at most twelve real Claude runs, counting every start of Claude including a refused launch and allowing no retries. Run budget: the preflight one, Task 2 four, Task 3 four and Task 4 three (its shapes share governed sessions as separate commands, grouped so that no shape runs after a call that stays blocked in the same session), twelve in all. Keep CLAUDECODE and existing auth variables intact: a nested-session refusal or missing authentication is recorded as unavailable and is never worked around.
- A case counts as observed only when a real Claude, Orca or Git process produced it in this plan's runs. Cases built from controlled processes or edited fixture state are labelled controlled and are never reported as real harness behavior. A case that cannot be driven is recorded as unavailable with the exact missing interface named. Never fabricate payload logs, and never write an unsupported or unobserved case as passed.
- Redact credentials, environment values, command text and process arguments from every artifact: keep identities, field names, hashes, selector results, exit codes and counts only.
- Use UV for Python (uv run --no-project python -I ...). Evidence belongs under ./artifacts/ in this package. No commit, push or issue comment is authorized. Stage .dev/tasks, including package evidence, throughout execution. Do not change this plan once implementation starts.
Start sha: 389b3504e14fc30faaa1be079ba1a6ab608cce29
Diff against the start snapshot: Tracked files: `git diff 389b3504e14fc30faaa1be079ba1a6ab608cce29` shows no change to any tracked source file (the ledger progress.md and earlier notes are not product). The touched files of this task are new or appended, so read each one in full from disk:
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/observe/task6.py
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/human-vs-governed-push.json
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/run-status.jsonl
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/phase2-cleanup.log
run-status.jsonl and phase2-cleanup.log also hold earlier lines; this task's lines are the t6-* case and the group=t6 lines. artifacts/observe/observe.py is the Task 1 runner this task imports (unchanged in this task). Reading ./artifacts/ files other than the retries folder is allowed. src/superclaude/hooks/scripts/launch-job-identity.sh and tests/hooks/test_launch_job_identity.py are unchanged read-only inputs.
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
