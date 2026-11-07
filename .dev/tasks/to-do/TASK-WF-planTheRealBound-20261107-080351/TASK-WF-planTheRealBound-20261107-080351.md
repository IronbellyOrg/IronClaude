---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-planTheRealBound-20261107-080351
version: "1"
priority: Medium
created_date: "2026-11-07"
---

# Observe the real actor-isolation lifecycle cases and report a binary B-CTX result

Source: ./source.md
Goal: Produce observed evidence, or an explicit unsupported result that names the missing interface, for every actor and lifecycle case that the blocked B-CTX gate (Task 1 of package TASK-WF-implementDocsDes-20261106-210206) left unobserved, measured against the identity integration that PR #414 merged, and end with one report carrying a binary B-CTX result. Nothing is enforced and no production file changes.

## Constraints

- The authoritative design is docs/designs/sc-issue-launch-level-hook.md, section 19 (19.1 for the required cases and 19.7 for the merged job-identity contract). The gap list is the six findings F2.1 to F2.6 in review-2.md of the blocked package, at artifacts/retries/T1/ inside package TASK-WF-implementDocsDes-20261106-210206 (a package in the to-do folder of .dev/tasks/). The identity helper under test is src/superclaude/hooks/scripts/launch-job-identity.sh; the earlier real-CLI observation helper is tests/hooks/fixtures/launch_level/live_probe.py. Read all of them; edit none of them.
- Do not modify, move or re-run package TASK-WF-implementDocsDes-20261106-210206, and do not modify the done package TASK-WF-authorizedNarrow-20261106-214325. Their files are read-only inputs.
- This plan observes and reports only. It adds no production hook, no registration, no installer change, no change under src/, plugins/ or tests/, and it never configures a real repository's hooks. Git experiments run only in disposable local repositories and disposable local bare repositories created under a temporary directory. No push to a real origin or any protected branch of a real remote. No interaction with the SuperClaude upstream repository.
- Real Claude runs use a throwaway HOME and CLAUDE_CONFIG_DIR, an explicit --settings file and --setting-sources "", exactly like tests/hooks/fixtures/launch_level/live_probe.py. Never edit the user's real Claude settings. Each real Claude run is capped with --max-budget-usd 0.25 and a bounded timeout, and the whole plan makes at most twelve real Claude runs. Keep CLAUDECODE and existing auth variables intact: a nested-session refusal or missing authentication is recorded as unavailable and is never worked around.
- A case counts as observed only when a real Claude, Orca or Git process produced it in this plan's runs. Cases built from controlled processes or edited fixture state are labelled controlled and are never reported as real harness behavior. A case that cannot be driven is recorded as unavailable with the exact missing interface named. Never fabricate payload logs, and never write an unsupported or unobserved case as passed.
- Redact credentials, environment values, command text and process arguments from every artifact: keep identities, field names, hashes, selector results, exit codes and counts only.
- Use UV for Python (uv run --no-project python -I ...). Evidence belongs under ./artifacts/ in this package. No commit, push or issue comment is authorized. Stage .dev/tasks, including package evidence, throughout execution. Do not change this plan once implementation starts.

## Phase 1: Safe observation harness

## Task 1: Build the observation runner with a preflight and an exit-status ledger

Write ./artifacts/observe/observe.py, a stdlib Python runner started with uv run --no-project python -I, that all later tasks use. It creates its disposable HOME, disposable fixture repository and temporary directory, runs one named case at a time with a timeout, and appends one JSON line per run to ./artifacts/run-status.jsonl with the case id, a redacted command label, start and end time, exit code or signal, and a result of observed, controlled, unavailable or blocked. Model its isolated HOME, settings file and redaction on tests/hooks/fixtures/launch_level/live_probe.py and read the exit and cleanup handling of its probe function. Add a preflight command that writes ./artifacts/preflight.json recording the Claude version, whether a nested Claude launch is refused, whether authentication is available in the throwaway HOME, whether UV, Bash, git and /proc are present, and the host boot identity.

Acceptance criteria:
- ./artifacts/observe/observe.py exists, runs a preflight with uv run --no-project python -I, and writes ./artifacts/preflight.json whose every field is an observed value or the word unavailable; the preflight exit status is recorded in ./artifacts/run-status.jsonl.
- A runner self-check in ./artifacts/observe-selfcheck.log shows that a secret-looking environment value and a command argument placed in a test run never appear in run-status.jsonl or preflight.json, that a timeout kills the whole process group and is recorded as blocked, and that the disposable HOME and temporary directory are removed afterwards.
- The runner touches nothing outside its temporary directory and ./artifacts/: git status for src/, plugins/ and tests/ is empty after the self-check, and the user's real Claude settings file has the same checksum before and after.

## Phase 2: Real harness lifecycle observations

## Task 2: Observe a governed and an ordinary session in the same worktree, a nested subagent and Monitor

Depends on: Task 1

Use the runner of Task 1 to start two real Claude --print sessions in the same disposable fixture repository, one whose session id has a private governed level record in the throwaway HOME's launch-level store (created as live_probe.py does for its governed variant) with the Bash adapter registered through --settings, and one ordinary session with no record. In each, the prompt asks for exactly one Bash command that runs the helper's identify action of src/superclaude/hooks/scripts/launch-job-identity.sh and prints the result. Then run a governed session whose prompt asks a subagent to run the same Bash command, and a governed session that tries the Monitor tool. Record the selector result of every command and the raw event types only, not the text.

Acceptance criteria:
- ./artifacts/same-worktree.json records, for the governed and the ordinary session run against the same worktree, the session id each reported and the selector status (governed with the governed session's own id, and ordinary), with the ordinary result produced while the governed session's record still existed.
- ./artifacts/subagent-and-monitor.json records, for the nested subagent case and the Monitor case, either the observed selector status and session id, or the result unavailable with the missing interface named (for example the tool not offered in print mode, or a refused nested launch); neither is reported as passed without an observed selector line.
- Every run of this task has an exit status line in ./artifacts/run-status.jsonl, and a log ./artifacts/phase2-cleanup.log shows no leftover Claude, supervisor or fixture process after the task.

## Task 3: Observe resume, fork and clear against an old live governed child

Depends on: Task 2

Using the runner of Task 1, observe the three lifecycle events that the blocked gate called unproven. First start a governed real Claude session whose Bash command starts a background child and prints its selector status, keep that child alive, then resume the same session id in a new Claude process (claude --resume) and run the identify action in the resumed process, and run a fork (claude --fork-session) the same way. For /clear, attempt a pty-driven interactive Claude session in the throwaway HOME, send /clear, then run one governed Bash command; if an interactive session cannot be driven within the budget, record /clear as unavailable and name the missing interface. In every case record whether the old child and the new work report the same or different session identities, and whether a new ordinary session started in a reused process is selected as ordinary.

Acceptance criteria:
- ./artifacts/resume-fork-clear.json has one entry each for resume, fork and /clear. Each entry holds the old child's selector status and origin session id, the new process's selector status and session id, and a result of observed or unavailable; an unavailable entry names the missing interface.
- The decisive case is answered from observation or marked unavailable with its interface: an old governed background child stays alive while a new ordinary session starts, and the two report different identities (child governed with the old origin, new session ordinary), or the entry states exactly what could not be observed.
- No entry is written as observed without a selector line captured in ./artifacts/run-status.jsonl-linked output, and every started child is accounted for as stopped in ./artifacts/phase2-cleanup.log.

## Task 4: Observe background and detached jobs under the governed Bash adapter

Depends on: Task 2

Using the runner of Task 1 in a governed real Claude session, observe four job shapes through the adapter's rewritten Bash call: an ordinary run_in_background Bash command, a foreground command that starts a descendant and exits so the descendant is reparented, a deliberate setsid daemonized child, and a command whose supervisor is killed while a child lives. For each, run the identify action of src/superclaude/hooks/scripts/launch-job-identity.sh against the descendant's process id from a second, ordinary Bash tool call and record the status and origin session id. Record the documented escapes (setsid, supervisor kill) as observed escapes, not as failures of the harness.

Acceptance criteria:
- ./artifacts/background-jobs.json records, for each of the four shapes, the selector status and origin session id reported for the descendant, or unavailable with the missing interface named when the harness did not run the case.
- The setsid and killed-supervisor entries state the status actually observed (for example ordinary or unknown) and say that these are documented limits of the merged design (section 19.7 of docs/designs/sc-issue-launch-level-hook.md), with no claim that they are protected.
- Exit statuses of all runs are in ./artifacts/run-status.jsonl and ./artifacts/phase2-cleanup.log shows every descendant stopped.

## Phase 3: Controlled selector invariants and the ancestry bound

## Task 5: Observe release, PID reuse and boot-identity rejection with controlled processes

Depends on: Task 1

Using controlled local processes and an edited copy of the launch-level state in the throwaway HOME, exercise the selector of src/superclaude/hooks/scripts/launch-job-identity.sh through its identify action, and label every result controlled. Cover three cases: release while a governed child is alive (delete that session's level record and show the child becomes ordinary with reason released while a second governed session's child stays governed); a registered job whose recorded process start ticks no longer match the live process (as after PID reuse); and a registered job whose recorded boot identity differs from the host boot identity. Read identify() and the job registration code of the helper first and cite the lines that compare start ticks and boot identity.

Acceptance criteria:
- ./artifacts/selector-invariants.json holds one entry per case with the selector status and reason, marked controlled, and cites the helper lines (path:line) that compare start ticks and boot identity.
- The release entry shows two governed sessions with one live child each, and only the released session's child changes status; the other session's child is unchanged.
- The start-tick mismatch and boot-identity mismatch entries show a status that is not governed (unknown or ordinary as the helper defines) and never governed; if the helper does not compare boot identity, the entry says so and records the case as a confirmed gap.

## Task 6: Observe same-worktree human pushes against governed pushes in a disposable bare repository

Depends on: Task 5

In a temporary directory create a bare repository and a clone with a linked worktree, install a log-only pre-push hook in that fixture clone only (it appends the selector status of the pushing process, via the identify action of src/superclaude/hooks/scripts/launch-job-identity.sh, and the destination field of each pushed ref to a log, then exits 0 so it vetoes nothing), and push to branches named main and master of the disposable bare repository only. Run pushes from a plain human-style shell and from a governed job, concurrently, in the same worktree. Record the selector status the hook saw for each and the resulting refs of the bare repository.

Acceptance criteria:
- ./artifacts/human-vs-governed-push.json shows, for each push, the actor started from (plain shell or governed job), the selector status the hook logged, the pushed destination ref, and the bare repository's refs before and after; the plain-shell pushes are logged ordinary and the governed-job pushes are logged governed with the governed session id.
- A concurrent run shows the human push and the governed push in the same worktree at the same time with different logged statuses, and the human push reaches the bare repository.
- No remote other than the temporary bare repository is configured or contacted, shown by the fixture's git remote listing in the artifact, and the fixture's pre-push hook is the only hook installed and exists only in the temporary directory.

## Task 7: Measure the process-tree depth and the exhaustion behavior of the actor selector

Depends on: Task 5

Read identify() and the related process-reading code of src/superclaude/hooks/scripts/launch-job-identity.sh and state, with path:line citations, whether the selector walks the parent chain (a bounded ancestry) or checks kernel session membership. Measure the real process-tree depth from the Claude process to a Bash tool command in the observed runs of Tasks 2 to 4, and the depth of the historical controller-ancestry probe (its 64-hop traversal cap is in the blocked package's actor-context-probe.sh under artifacts/). If the selector walks the parent chain, run it with a controlled chain deeper than its bound and record the exhaustion result; if it uses kernel session membership, record the bound question as not applicable with the evidence, and run one controlled case with a very deep nested shell chain to observe that the selector's status is unchanged.

Acceptance criteria:
- ./artifacts/ancestry-bound.md cites the helper lines that decide the selection method and records the measured real process-tree depths from the Task 2 to 4 runs as numbers taken from ./artifacts/run-status.jsonl-linked output.
- The exhaustion behavior is either observed (controlled chain deeper than the bound, with the status returned, which must not be governed or ordinary by default) or recorded as not applicable with the cited reason and the deep-chain control result.
- The artifact states that the historical 64-hop cap is not adopted as a production bound unless measured here, and does not describe an exhausted or unreadable walk as a trusted human.

## Phase 4: Binary result and report

## Task 8: Write the B-CTX report with a binary result

Depends on: Task 3, Task 4, Task 6, Task 7

Write ./artifacts/b-ctx-report.md. It lists every case that section 19.1 of docs/designs/sc-issue-launch-level-hook.md requires (main Claude, subagent and nested tool calls, background Bash and Monitor descendants, same-worktree human terminal, ordinary Claude session, detached or reparented jobs, process exit and PID reuse, resume into a new process, /clear and fork, release with a live old background child) with the artifact that holds its evidence, the result observed, controlled or unavailable, and for unavailable the missing interface. Map each of the gap findings F2.1 to F2.6 of the blocked review to the case or artifact that closes it, or state that it stays open. End with one binary line B-CTX: PASS or B-CTX: FAIL and, for FAIL, the exact missing binding, reset or child-lifetime contract and the smallest integration that would supply it. Finish with a cleanup record.

Acceptance criteria:
- ./artifacts/b-ctx-report.md has one row for every case named above, each linking to an artifact of this package and carrying observed, controlled or unavailable; no row is empty and no unavailable row lacks a named interface.
- Every one of the findings F2.1 to F2.6 has a line stating closed by (artifact) or open (why), and a closed claim is backed by an observed or controlled result of the same case.
- The report ends with exactly one result line B-CTX: PASS or B-CTX: FAIL; PASS appears only if every required case is observed (not controlled and not unavailable), otherwise the result is FAIL with the missing contract and smallest integration named, and the report states that the result does not waive the blocked package's gate.
- The cleanup record shows no leftover process or temporary directory from the plan's runs, and the git status of src/, plugins/, tests/ and the blocked package is unchanged, with the package's own files staged under .dev/tasks.
