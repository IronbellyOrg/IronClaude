a3c625c1be181aa20f6753059574ae403a56eb10
Review one task for spec compliance.

Task brief: ## Task 7: Measure the process-tree depth and the exhaustion behavior of the actor selector

Depends on: Task 2, Task 3, Task 4, Task 5

Read identify() and the related process-reading code of src/superclaude/hooks/scripts/launch-job-identity.sh and cite the lines that decide the selection method: identify reads the target's kernel session and the job record of that session (helper:219-223) and the file states that no bounded ancestry walk is interpreted (helper:253), so the selector checks kernel session membership and does not walk the parent chain. Measure the real process-tree depth from the Claude process to a Bash tool command from the depth field of the observed runs of Tasks 2 to 4, and the depth of the historical controller-ancestry probe (its 64-hop traversal cap is in the blocked package's actor-context-probe.sh under artifacts/). Record the bound question as not applicable with that evidence, and run one controlled case with a very deep nested shell chain to observe that the selector's status is unchanged. If no real run of Tasks 2 to 4 was made because the preflight reported a refused nested launch or missing authentication, record the real depths as unavailable with that reason.

Acceptance criteria:
- ./artifacts/ancestry-bound.md cites the helper lines that decide the selection method and records the measured real process-tree depths from the Task 2 to 4 runs as numbers taken from ./artifacts/run-status.jsonl-linked output.
- The exhaustion behavior is recorded as not applicable with the cited reason (kernel session membership, no parent walk) and the controlled deep-chain control result, whose status is unchanged from the shallow chain.
- The artifact states that the historical 64-hop cap is not adopted as a production bound unless measured here, and does not describe an exhausted or unreadable walk as a trusted human.
Global constraints: ## Constraints

- The authoritative design is docs/designs/sc-issue-launch-level-hook.md, section 19 (19.1 for the required cases and 19.7 for the merged job-identity contract). The gap list is the six findings F2.1 to F2.6 in review-2.md of the blocked package, at artifacts/retries/T1/ inside package TASK-WF-implementDocsDes-20261106-210206 (a package in the to-do folder of .dev/tasks/). The identity helper under test is src/superclaude/hooks/scripts/launch-job-identity.sh; the earlier real-CLI observation helper is tests/hooks/fixtures/launch_level/live_probe.py. Read all of them; edit none of them.
- Do not modify, move or re-run package TASK-WF-implementDocsDes-20261106-210206, and do not modify the done package TASK-WF-authorizedNarrow-20261106-214325. Their files are read-only inputs.
- This plan observes and reports only. It adds no production hook, no registration, no installer change, no change under src/, plugins/ or tests/, and it never configures a real repository's hooks. Git experiments run only in disposable local repositories and disposable local bare repositories created under a temporary directory. No push to a real origin or any protected branch of a real remote. No interaction with the SuperClaude upstream repository.
- Real Claude runs use a throwaway HOME and CLAUDE_CONFIG_DIR, an explicit --settings file and --setting-sources "", exactly like tests/hooks/fixtures/launch_level/live_probe.py. Never edit the user's real Claude settings. Each real Claude run is capped with --max-budget-usd 0.25 and a bounded timeout, except the one interactive /clear run in Task 3, which the owner authorized on 2026-11-08 (review decision M2-02) as a separately bounded run because the installed CLI restricts --max-budget-usd to --print, and the whole plan makes at most twelve real Claude runs, counting every start of Claude including a refused launch and allowing no retries. Run budget: the preflight one, Task 2 four, Task 3 four and Task 4 three (its shapes share governed sessions as separate commands, grouped so that no shape runs after a call that stays blocked in the same session), twelve in all. Keep CLAUDECODE and existing auth variables intact: a nested-session refusal or missing authentication is recorded as unavailable and is never worked around.
- A case counts as observed only when a real Claude, Orca or Git process produced it in this plan's runs. Cases built from controlled processes or edited fixture state are labelled controlled and are never reported as real harness behavior. A case that cannot be driven is recorded as unavailable with the exact missing interface named. Never fabricate payload logs, and never write an unsupported or unobserved case as passed.
- Redact credentials, environment values, command text and process arguments from every artifact: keep identities, field names, hashes, selector results, exit codes and counts only.
- Use UV for Python (uv run --no-project python -I ...). Evidence belongs under ./artifacts/ in this package. No commit, push or issue comment is authorized. Stage .dev/tasks, including package evidence, throughout execution. Do not change this plan once implementation starts.
Start sha: a3c625c1be181aa20f6753059574ae403a56eb10
Diff against the start snapshot: Tracked files: `git diff a3c625c1be181aa20f6753059574ae403a56eb10` shows no change to any tracked source file (the ledger progress.md and earlier notes are not product). The touched files of this task are new or appended, so read each one in full from disk:
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/observe/task7.py
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/ancestry-bound.md
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/run-status.jsonl
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/phase2-cleanup.log
run-status.jsonl and phase2-cleanup.log also hold earlier lines; this task's line is the t7-deep-chain case and the group=t7 line. The measured depths in ancestry-bound.md come from the ledger lines of Tasks 2 and 3 and from artifacts/background-jobs.json (Task 4); artifacts/observe/observe.py is the Task 1 runner this task imports (unchanged in this task). Reading ./artifacts/ files other than the retries folder is allowed. src/superclaude/hooks/scripts/launch-job-identity.sh and the blocked package's artifacts/actor-context-probe.sh are unchanged read-only inputs; their line numbers can be checked directly.
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
