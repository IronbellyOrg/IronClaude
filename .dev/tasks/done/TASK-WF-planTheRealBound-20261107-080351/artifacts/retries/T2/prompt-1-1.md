c2fe3180cd764c802a7a0678026de7622e1b351a
Review one task for spec compliance.

Task brief: ## Task 2: Observe a governed and an ordinary session in the same worktree, a nested subagent and Monitor

Depends on: Task 1

Use the runner of Task 1 to start two real Claude --print sessions in the same disposable fixture repository, one whose session id has a private governed level record in the throwaway HOME's launch-level store (created as live_probe.py does for its governed variant) with the Bash adapter registered through --settings, and one ordinary session with no record. In each, the prompt asks for exactly one Bash command that runs the helper's identify action of src/superclaude/hooks/scripts/launch-job-identity.sh and prints the result together with the count of parent hops from the command's shell up to the Claude process (recorded as the depth in the ledger). Then run a governed session whose prompt asks a subagent to run the same Bash command, and a governed session that tries the Monitor tool. live_probe offers Claude only the Bash tool, so the subagent run also offers the tool that starts a subagent and the Monitor run also offers the Monitor tool, named from the preflight's tool list; a case is recorded unavailable for a missing tool only when the preflight shows the tool is not offered in print mode or after a run that actually offered it. Record the selector result of every command and the raw event types only, not the text.

Acceptance criteria:
- ./artifacts/same-worktree.json records, for the governed and the ordinary session run against the same worktree, the session id each reported and the selector status (governed with the governed session's own id, and ordinary), with the ordinary result produced while the governed session's record still existed; when the preflight reports a refused nested launch or missing authentication the file instead records both sessions unavailable with the redacted refusal result and its ledger line, and no run is spent.
- ./artifacts/subagent-and-monitor.json records, for the nested subagent case and the Monitor case, either the observed selector status and session id, or the result unavailable with the missing interface named (for example the tool not offered in print mode, or a refused nested launch); neither is reported as passed without an observed selector line.
- Every run of this task has an exit status line in ./artifacts/run-status.jsonl, and a log ./artifacts/phase2-cleanup.log shows no leftover Claude, supervisor or fixture process after the task.
Global constraints: ## Constraints

- The authoritative design is docs/designs/sc-issue-launch-level-hook.md, section 19 (19.1 for the required cases and 19.7 for the merged job-identity contract). The gap list is the six findings F2.1 to F2.6 in review-2.md of the blocked package, at artifacts/retries/T1/ inside package TASK-WF-implementDocsDes-20261106-210206 (a package in the to-do folder of .dev/tasks/). The identity helper under test is src/superclaude/hooks/scripts/launch-job-identity.sh; the earlier real-CLI observation helper is tests/hooks/fixtures/launch_level/live_probe.py. Read all of them; edit none of them.
- Do not modify, move or re-run package TASK-WF-implementDocsDes-20261106-210206, and do not modify the done package TASK-WF-authorizedNarrow-20261106-214325. Their files are read-only inputs.
- This plan observes and reports only. It adds no production hook, no registration, no installer change, no change under src/, plugins/ or tests/, and it never configures a real repository's hooks. Git experiments run only in disposable local repositories and disposable local bare repositories created under a temporary directory. No push to a real origin or any protected branch of a real remote. No interaction with the SuperClaude upstream repository.
- Real Claude runs use a throwaway HOME and CLAUDE_CONFIG_DIR, an explicit --settings file and --setting-sources "", exactly like tests/hooks/fixtures/launch_level/live_probe.py. Never edit the user's real Claude settings. Each real Claude run is capped with --max-budget-usd 0.25 and a bounded timeout, except the one interactive /clear run in Task 3, which the owner authorized on 2026-11-08 (review decision M2-02) as a separately bounded run because the installed CLI restricts --max-budget-usd to --print, and the whole plan makes at most twelve real Claude runs, counting every start of Claude including a refused launch and allowing no retries. Run budget: the preflight one, Task 2 four, Task 3 four and Task 4 three (its shapes share governed sessions as separate commands, grouped so that no shape runs after a call that stays blocked in the same session), twelve in all. Keep CLAUDECODE and existing auth variables intact: a nested-session refusal or missing authentication is recorded as unavailable and is never worked around.
- A case counts as observed only when a real Claude, Orca or Git process produced it in this plan's runs. Cases built from controlled processes or edited fixture state are labelled controlled and are never reported as real harness behavior. A case that cannot be driven is recorded as unavailable with the exact missing interface named. Never fabricate payload logs, and never write an unsupported or unobserved case as passed.
- Redact credentials, environment values, command text and process arguments from every artifact: keep identities, field names, hashes, selector results, exit codes and counts only.
- Use UV for Python (uv run --no-project python -I ...). Evidence belongs under ./artifacts/ in this package. No commit, push or issue comment is authorized. Stage .dev/tasks, including package evidence, throughout execution. Do not change this plan once implementation starts.
Start sha: c2fe3180cd764c802a7a0678026de7622e1b351a
Diff against the start snapshot: Tracked files: `git diff c2fe3180cd764c802a7a0678026de7622e1b351a` shows no change to any tracked source file (the ledger progress.md and the Task 1 notes are not product). The touched files of this task are new or appended, so read each one in full from disk:
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/observe/real_case.py
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/observe/task2.py
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/same-worktree.json
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/subagent-and-monitor.json
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/run-status.jsonl
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/phase2-cleanup.log
run-status.jsonl and phase2-cleanup.log also hold earlier Task 1 lines; this task's lines are the t2-* cases and the group=t2 line. artifacts/observe/observe.py is the Task 1 runner this task imports (unchanged in this task), and artifacts/preflight.json is its earlier output. Reading ./artifacts/ files other than the retries folder is allowed. src/superclaude/hooks/scripts/launch-job-identity.sh is an unchanged read-only input.
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
