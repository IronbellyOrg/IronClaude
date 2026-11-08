# B-CTX report: observed actor-isolation lifecycle cases

Package TASK-WF-planTheRealBound-20261107-080351. Measured against the identity integration of PR #414 (`src/superclaude/hooks/scripts/launch-job-identity.sh`) and section 19 of `docs/designs/sc-issue-launch-level-hook.md`. Nothing is enforced and no production file changed.

Evidence classes: **observed** = a real Claude process produced it in this plan's runs (selector output captured by the runner by run id, never the model's own report); **controlled** = built from runner-started processes or an edited fixture record, never real harness behavior; **unavailable** = not driven, with the missing interface named.

## Real Claude runs (counted from ./artifacts/run-status.jsonl)

Real Claude runs counted (`real_claude` true, refused launches included): **12** of at most 12. Refused launches: 0. Re-runs: none.

| Case | Run id | Exit | Result | Ledger line |
|---|---|---|---|---|
| preflight | 2759fb66d2d2 | 1 | blocked | ./artifacts/run-status.jsonl:8 |
| t2-governed | d26d5ce5dffe | 0 | observed | ./artifacts/run-status.jsonl:16 |
| t2-ordinary | cbc9c8711f03 | 0 | observed | ./artifacts/run-status.jsonl:17 |
| t2-subagent | 1f6cc0d01ea4 | 0 | observed | ./artifacts/run-status.jsonl:18 |
| t2-monitor | ee11e0a48d51 | 0 | observed | ./artifacts/run-status.jsonl:19 |
| t3-first | 23bb376ba27f | signal:SIGKILL | observed | ./artifacts/run-status.jsonl:20 |
| t3-resume | 0c6d6a35dc9e | 0 | observed | ./artifacts/run-status.jsonl:21 |
| t3-fork | a2d1d6b085c5 | 0 | observed | ./artifacts/run-status.jsonl:22 |
| t3-clear-interactive | 26ebfaffd570 | 143 | unavailable | ./artifacts/run-status.jsonl:23 |
| t4-setsid | c321f2bba905 | 0 | observed | ./artifacts/run-status.jsonl:24 |
| t4-killed-supervisor | 65a6f40544c1 | 0 | observed | ./artifacts/run-status.jsonl:25 |
| t4-background-reparent | 8d2becc8a4c2 | 0 | observed | ./artifacts/run-status.jsonl:26 |

The first run (the preflight) exited 1 after Claude started and listed its tools; its failure category was not captured by the first version of the runner, so `./artifacts/preflight.json` reads `unavailable` for `nested_launch_refused` and `authentication_available` (it records the exit, not a refusal). All 11 later real runs started and none showed a nested-launch refusal or an authentication failure (nine exited 0, one was ended by the planned SIGKILL of Task 3, and the interactive `/clear` run was ended by the runner after it produced nothing, exit 143), so those two preflight fields describe an undetermined first run, not the state of this host.

## Required cases (section 19.1)

| # | Case | Result | Evidence artifact | Runner-captured record | Separation shown | Missing interface |
|---|---|---|---|---|---|---|
| 1 | Main Claude (governed session, Bash adapter) | observed | ./artifacts/same-worktree.json:3 | run d26d5ce5dffe, selector line sha256 6c2f1d6931df | yes: governed with its own session id (af861632-9753-4020-b06c-99b4a00c9a3f) | - |
| 2 | Subagent and nested tool calls (the nested subagent's Bash call) | observed | ./artifacts/subagent-and-monitor.json:89 | run 1f6cc0d01ea4, selector line sha256 1425b014e373 | yes: governed with the parent session's id; the hook event carried an agent id | - |
| 3a | Background Bash descendant (run_in_background) | observed | ./artifacts/background-jobs.json:235 | run 8d2becc8a4c2, selector line sha256 ddd8aac1b8d7 | yes: descendant governed with the session's own id, inside the command and from a second Bash call | - |
| 3b | Monitor descendant | observed (documented escape) | ./artifacts/subagent-and-monitor.json:2 | run ee11e0a48d51, selector line sha256 0d525830bea5 | no: ordinary (Monitor has no adapter); attribution to the Monitor tool is an inference from the 2-hop depth | - |
| 4a | Same-worktree human terminal: human-style shell started by the runner | controlled | ./artifacts/human-vs-governed-push.json:38 | controlled push records (no real run) | ordinary logged for both plain-shell pushes | - |
| 4b | Same-worktree human terminal: a person in an Orca terminal | unavailable | ./artifacts/human-vs-governed-push.json:34 | none | not observed | a person's interactive terminal inside an Orca-managed worktree: the runner has no authorized interface to start an Orca terminal as a person would, and starting one would create terminals in the user's real Orca |
| 5 | Ordinary Claude session in the same worktree | observed | ./artifacts/same-worktree.json:131 | run cbc9c8711f03, selector line sha256 0d525830bea5 | yes: ordinary, produced while the governed session's record existed (True) | - |
| 6a | Reparented job (foreground command whose descendant is reparented) | observed | ./artifacts/background-jobs.json:156 | run 8d2becc8a4c2, selector line sha256 ddd8aac1b8d7 | yes: governed inside the same command; the call waited 28.2 s for the descendant | - |
| 6b | Detached job: deliberate setsid daemonized child | observed (documented escape) | ./artifacts/background-jobs.json:282 | run c321f2bba905, selector line sha256 0d525830bea5 | no: the child reported ordinary (documented limit, section 19.7) | - |
| 6c | Detached job: supervisor killed while a child lives | observed (documented escape) | ./artifacts/background-jobs.json:192 | run 65a6f40544c1, selector line sha256 44a446afb90e | no: governed before the kill, unknown after it (documented limit, section 19.7) | - |
| 7a | Process exit and PID reuse (recorded start ticks no longer match) | controlled | ./artifacts/selector-invariants.json:81 | controlled edit of a job record (no real run) | not governed after the edit (unknown) | - |
| 7b | Boot identity change | controlled | ./artifacts/selector-invariants.json:2 | controlled edit of a job record (no real run) | not governed after the edit (unknown) | - |
| 8 | Resume into a new process | observed | ./artifacts/resume-fork-clear.json:209 | run 0c6d6a35dc9e, selector lines a0266d940410,a0266d940410 | yes: the resumed session kept the origin id a590b456-1cb9-4c51-91ec-1bbc34f499c4 and its command reported governed; the old child stayed governed | - |
| 9a | Fork | observed | ./artifacts/resume-fork-clear.json:161 | run a2d1d6b085c5, selector lines a0266d940410,0d525830bea5 | yes: the forked session (new id 64b3f68b-b483-42dc-90cf-1a64b2984088) reported ordinary while the old child stayed governed | - |
| 9b | /clear | unavailable | ./artifacts/resume-fork-clear.json:2 | run 26ebfaffd570 (no selector line) | not observed | Keyboard input to the interactive Claude Code terminal UI through a pty: the runner sent the two prompts ("/clear", then one governed-command prompt) after the screen settled, but nothing shows that either reached a session. There is no transcript for the pty session's starting id, no PreToolUse hook event, and no selector line, after 129.9 seconds and 6288 bytes of terminal output. The cause was not captured (the screen contents were not retained), so no cause is claimed. One attempt, no retry, as the plan bounds it. |
| 10 | Release with a live old background child | controlled | ./artifacts/selector-invariants.json:37 | controlled processes (no real run) | only the released session's child changed (governed to ordinary, reason released); the other stayed governed | - |
| 11 | The launch wrapper | unavailable | ./artifacts/observe/observe.py:456 | none (not run) | not observed | the production launch path that starts a governed agent session (the claim-code launcher, section 19.8 of the design): this plan may not run it because it configures real worktrees and hooks, and the Task 2 to 4 sessions were started by the runner's own argv, not by that wrapper |
| 12 | The Git and hook process trees | unavailable | ./artifacts/human-vs-governed-push.json:38 | none (no real run invoked Git) | not observed in a real session | a real Claude Bash call that runs git push so that the pre-push hook's process tree under a real Claude process is read; Task 6 gives controlled evidence only (a plain shell and a governed job started by the runner), and no task of this plan runs Git from a real Claude session (the 12-run budget is fully assigned to Tasks 1 to 4) |
| 13 | The auto-mode variants | unavailable | ./artifacts/observe/observe.py:463 | none (no run used auto mode) | not observed | a real Claude run in auto permission mode under the Bash adapter: every real run here used the dontAsk permission mode, and the design lists live auto-mode rewrites as unobserved (section 19.7) |
| 14a | Decisive distinction, new-process form: old governed background child alive while a new ordinary session starts (fork) | observed | ./artifacts/resume-fork-clear.json:83 | run a2d1d6b085c5 (fork) | yes: the old child reported governed with origin a590b456-1cb9-4c51-91ec-1bbc34f499c4 and the new forked session reported ordinary | - |
| 14b | Decisive distinction, reused-process form: an ordinary new session started by /clear in the same Claude process | unavailable | ./artifacts/resume-fork-clear.json:52 | none | not observed | unavailable: the single-process /clear form (a new ordinary session started in a reused Claude process) was not observed; the resume and fork runs start new processes and cannot test it |

Notes on the rows: row 3b rests on a 2-hop selector line and the absence of an adapter rewrite for that command; the stream summary of that run kept event types but not tool names, so naming Monitor as the source is an inference. Row 9b: the interactive run sent both prompts but nothing shows either reached a session, and the cause was not captured. Task 4's third session saw five Bash calls for four requested commands (`./artifacts/background-jobs.json`, `extra_bash_call_note`). The log-only pre-push hook of Task 6 sleeps one second to widen the overlap window of its concurrent pushes.

## Gap findings F2.1 to F2.6 of the blocked review

The findings are in `.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/retries/T1/review-2.md` (read only).

- **F2.1 (lifecycle cases listed without observed evidence or a named interface): closed by the case table of this report.** Evidence class: observed for rows 1, 2, 3a, 3b, 5, 6a to 6c, 8, 9a and 14a; unavailable with the interface named for rows 4b, 9b, 11, 12, 13 and 14b; controlled for rows 4a, 7a, 7b and 10. Resume, fork, Monitor and the nested subagent are closed by observed results of the same cases, not by controlled ones; `/clear` is closed only in the sense that its missing interface is now named.
- **F2.2 (decisive distinction unproven): open (why).** The new-process form is observed (row 14a, ./artifacts/resume-fork-clear.json:83: old child governed with origin a590b456-1cb9-4c51-91ec-1bbc34f499c4, forked session ordinary). The form the finding asks for, a reused Claude process starting an ordinary session while the old governed child lives, needs `/clear` in one process and stays unavailable (row 14b).
- **F2.3 (ancestry bound not derived from observed trees): superseded or not applicable (src/superclaude/hooks/scripts/launch-job-identity.sh:253).** The merged selector checks kernel session membership and does not walk the parent chain; the real depths and the controlled deep chain are in `./artifacts/ancestry-bound.md`.
- **F2.4 (authority invariants not exercised): closed by `./artifacts/selector-invariants.json` and `./artifacts/human-vs-governed-push.json`; evidence class controlled.** Boot identity and start ticks are compared at src/superclaude/hooks/scripts/launch-job-identity.sh:234 (controlled check ./artifacts/selector-invariants.json:2); release with a live child changed only the released session's child (./artifacts/selector-invariants.json:37); a same-worktree human-style push and a governed push against a disposable bare repository were logged ordinary and governed (./artifacts/human-vs-governed-push.json:2). The real-session observation of release and of Git pushes stays an evidence gap (rows 10 and 12).
- **F2.5 (no file recording each probe run's command and exit status): closed by `./artifacts/run-status.jsonl`; evidence class observed for the 12 real runs and controlled for the other lines.** Each line records the case id, a redacted label, start and end, the exit code or signal and the result.
- **F2.6 (exhaustion described as never a trusted human, but the old walk discarded its stop reason): superseded or not applicable (the finding describes only the historical controller-ancestry probe, `.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-probe.sh:39`).** The merged selector has no walk; unreadable or stale registered state returns `unknown` (src/superclaude/hooks/scripts/launch-job-identity.sh:244), which the design says is not a trusted-human verdict (section 19.7).

## Why the result is FAIL

Task 5 can label release, PID reuse and boot identity only controlled, and `/clear`, the launch wrapper, the Git and hook process trees and the auto-mode variants were not observed, so not every required case is observed. **A FAIL result is the expected outcome of this plan.** Observed documented escapes (a setsid child, a killed supervisor, a Monitor command without an adapter) show no separation and never count toward a pass.

B-CTX: FAIL

### Contract gaps (observed cases whose status broke the separation)

1. **Monitor command (row 3b).** Missing binding: no adapter exists for the Monitor tool, so its command ran outside the supervisor and reported ordinary. Smallest integration: register the same PreToolUse adapter for the Monitor tool so its command is wrapped in a supervisor, or deny the Monitor tool in governed sessions. Whether Monitor input can be rewritten was not observed.
2. **Deliberate setsid child (row 6b).** Missing child-lifetime contract: a process that calls `setsid` leaves the supervisor's kernel session and reported ordinary. Smallest integration: containment that setsid cannot leave (for example a control group or a pidfd-tracked tree), as the helper's own comment says (src/superclaude/hooks/scripts/launch-job-identity.sh:7-9).
3. **Killed supervisor (row 6c).** Missing child-lifetime contract: after the supervisor was killed, its live child went from governed to unknown. Smallest integration: state what the pre-push decision does with `unknown` for a registered job whose supervisor is dead (the design says only that unknown is not a trusted-human verdict), or keep the supervisor out of the agent's reach.

### Evidence gaps (controlled or unavailable cases and the real-observation interface that would make each observed)

- Row 4a (human-style shell, controlled) and 4b (a person in an Orca terminal): a real person's terminal in an Orca-managed worktree pushing while a governed session works.
- Rows 7a and 7b (PID reuse and boot identity, controlled): a real recycled process id for a registered job and a real reboot of the host with a stale record; neither can be forced from a Claude session, so the nearest real observation is a recorded job read after a host restart.
- Row 10 (release, controlled): delete a governed session's level record from outside while a real Claude session's background child lives, then identify the child from a later Bash call.
- Row 9b and row 14b (`/clear`, unavailable): keyboard input to Claude Code's interactive terminal UI through a pty that provably reaches a session (this run's single attempt did not).
- Row 11 (launch wrapper, unavailable): a governed session started by the production claim-code launcher.
- Row 12 (Git and hook process trees, unavailable): a real Claude Bash call that runs `git push` to a disposable bare repository with the log-only hook installed.
- Row 13 (auto-mode variants, unavailable): a real Claude run in auto permission mode under the Bash adapter.

The contract-gap list is not empty: three observed cases broke the separation, all of them documented limits of the merged design (section 19.7). This result does not waive the blocked package's gate: package TASK-WF-implementDocsDes-20261106-210206 stays blocked and was not modified, moved or re-run.

## Cleanup record

- Processes and temporary directories: 11 group teardowns in `./artifacts/phase2-cleanup.log`, every one reporting `leftover_processes=0 directory_removed=True`: **True**. Leftover `/tmp/observe-*` directories: none. Processes whose working directory is under `/tmp/observe-*`: 0. Registry files left in `./artifacts/groups/`: none.
- Real Claude settings checksum: unchanged before and after every one of the 12 real runs (each `real_claude` entry of `./artifacts/run-status.jsonl` has equal before-run and after-run values): **True**; and equal to the value in `./artifacts/baseline.json`: **True**.
- Git state of `src/`, `plugins/`, `tests/` and the blocked package against `./artifacts/baseline.json` (status and diff checksums, plus the package tree checksums of the blocked and done packages): equal = **True**, differing keys: none.
- Staging: `git add .dev/tasks` was run when this report was generated. Files of this package staged: 5; untracked files in the package: 0; files staged under `src/`, `plugins/` or `tests/`: 0. Nothing was committed.
