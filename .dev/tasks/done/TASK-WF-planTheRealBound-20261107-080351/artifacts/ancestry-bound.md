# Actor-selector process-tree depth and exhaustion behavior (Task 7)

Evidence label: the depths are from real Claude runs (Tasks 2, 3 and 4); the deep-chain case is controlled (processes started by the runner under a governed job through the helper's own prepare and run actions). No real run was spent on this task.

## How the selector decides (helper lines, read now)

- `identify` starts at `src/superclaude/hooks/scripts/launch-job-identity.sh:215`. It reads the target process's kernel session id (`src/superclaude/hooks/scripts/launch-job-identity.sh:219`) and then the job record named after that session (`src/superclaude/hooks/scripts/launch-job-identity.sh:223`).
- The file itself states the method: `src/superclaude/hooks/scripts/launch-job-identity.sh:253` reads "No bounded ancestry walk or truncated scan is interpreted as ordinary". The only scan is `members` (`src/superclaude/hooks/scripts/launch-job-identity.sh:251`), which lists processes whose kernel session equals the supervisor's session; it is used by the supervisor to wait for its own descendants, not by `identify` to climb parents.
- The supervisor makes its own session with `os.setsid()` (`src/superclaude/hooks/scripts/launch-job-identity.sh:292`), so membership, not parent distance, is what binds a process to a job.
- The record is accepted only while the supervisor's pid, start ticks and boot identity still match (`src/superclaude/hooks/scripts/launch-job-identity.sh:234`); stale or unreadable state returns `unknown` (`src/superclaude/hooks/scripts/launch-job-identity.sh:244`); a deleted level record returns `ordinary` with reason `released` (`src/superclaude/hooks/scripts/launch-job-identity.sh:241`).

## Measured real process-tree depth (from run-status.jsonl and the Task 4 artifact)

Hops are parent links from the command's shell up to the Claude process, measured by the command itself. Ledger lines are in ./artifacts/run-status.jsonl (the run id column); the Task 4 numbers are in ./artifacts/background-jobs.json (their run ids are in the same ledger).

| Case | Hops to the Claude process | Claude process reached | Run id |
|---|---|---|---|
| t2-governed | 5 | yes | d26d5ce5dffe |
| t2-ordinary | 2 | yes | cbc9c8711f03 |
| t2-subagent | 5 | yes | 1f6cc0d01ea4 |
| t2-monitor | 2 | yes | ee11e0a48d51 |
| t3-first | 5 | yes | 23bb376ba27f |
| t3-resume | 5 | yes | 0c6d6a35dc9e |
| t3-fork | 2 | yes | a2d1d6b085c5 |
| t4 foreground_reparent (first call) | 5 | yes | 8d2becc8a4c2 |
| t4 killed_supervisor (first call) | 5 | yes | 65a6f40544c1 |
| t4 killed_supervisor (second Bash call) | 5 | yes | 65a6f40544c1 |
| t4 run_in_background (first call) | 5 | yes | 8d2becc8a4c2 |
| t4 run_in_background (second Bash call) | 5 | yes | 8d2becc8a4c2 |
| t4 setsid_daemon (first call) | 5 | yes | c321f2bba905 |
| t4 setsid_daemon (second Bash call) | 5 | yes | c321f2bba905 |

Summary: Bash calls rewritten by the adapter (governed sessions) measured [5] hops; commands not wrapped by the adapter (the ordinary session and the Monitor command) measured [2] hops. The largest real depth observed in this plan is 5 hops.

## Historical controller-ancestry probe

The historical probe in the blocked package walked parent links with a traversal cap of 64 hops (`.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-probe.sh:11`, "Diagnostic bound only; not a proven production ancestry limit"). The merged selector does not use that probe.

## Exhaustion behavior: not applicable

The bound question is recorded as **not applicable**. The selector checks kernel session membership and does not walk the parent chain (`src/superclaude/hooks/scripts/launch-job-identity.sh:253`), so there is no walk to exhaust and no hop bound to choose. Unreadable or stale registered state selects `unknown` (`src/superclaude/hooks/scripts/launch-job-identity.sh:244`), and the design states that `unknown` is not a trusted-human verdict (docs/designs/sc-issue-launch-level-hook.md section 19.7); this artifact does not describe an exhausted or unreadable walk as a trusted human.

Controlled deep-chain case (label: controlled): a governed job ran a nested shell chain and called `identify` at the bottom.

| Chain | Nesting requested | Hops from the bottom shell to the supervisor | Selector status | Session id |
|---|---|---|---|---|
| shallow control | 0 | 1 | governed | f4c47067-bbfe-4b94-9796-460bf9972871 |
| very deep | 200 | 201 | governed | f4c47067-bbfe-4b94-9796-460bf9972871 |

Result: the selector status of the very deep chain is unchanged from the shallow chain (same status and session id), at a depth well beyond the historical 64-hop cap.

## Statement on the historical cap

The historical 64-hop cap is **not adopted** as a production bound. It is not measured here as a requirement: the selector has no ancestry bound, and the largest real depth measured in this plan is 5 hops. If a future design reintroduces a parent walk, that bound would need its own measurement and an explicit exhaustion rule.

Cleanup: the controlled chain's group teardown left 0 processes and removed its directories (./artifacts/phase2-cleanup.log).
