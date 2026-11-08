# Reflection card: UC-1 pre-execution, plan TASK-WF-planTheRealBound-20261107-080351

(Returned by the root-cause-analyst agent, Tier 1; persisted by the parent on receipt at 2026-11-08T02:01Z. `plan:N` = line N of the plan; helper = src/superclaude/hooks/scripts/launch-job-identity.sh.)

| Field | Value |
|---|---|
| Agent | root-cause-analyst |
| Tier | 1 |
| Mode | pre (UC-1) |
| Verdict | PASS-WITH-FIXES (advisory). An executor can now produce a meaningful B-CTX result. All 17 earlier findings are addressed in the text (15 fully, 2 partly). The edits introduced 5 Medium new defects (N-1, N-2, N-3, N-4, N-12) and several Low defects; M-07 and M-15 stay open as PARTLY (Medium). [Corrected by the parent after calibration: the agent's original text said "3 Medium".] |

## Findings M-01 to M-17

| id | status | plan_line | evidence | severity if open |
|---|---|---|---|---|
| M-01 | RESOLVED | plan:120, :117, :118 | Plan:120 says B-CTX: FAIL is the expected result and that an observed documented escape never counts toward PASS; plan:118 bars a controlled result from closing a resume, /clear, Monitor or subagent finding | n/a |
| M-02 | RESOLVED | plan:31, :55, :58-:60 | surviving jobs live until explicit teardown; SIGKILL to the first Claude process id only; child and supervisor /proc state read before resume; dead child recorded as "job did not survive the first Claude process ending"; no substitute child | n/a (residual: N-5) |
| M-03 | RESOLVED | plan:31, :55, :58 | HOME "created once per group ... removed only by an explicit teardown"; store-and-record check before each run; live_probe.py:134 is per-call | n/a (group scope: N-2) |
| M-04 | RESOLVED | plan:66, :69 | reparent shape runs identify inside the same governed command and records the wait; observer renamed "a second Bash tool call" | n/a |
| M-05 | RESOLVED | plan:31, :44, :99, :104 | ledger depth field; Task 2 command prints parent hops; Task 7 depends on Tasks 2, 3, 4, 5; no cycle | n/a |
| M-06 | RESOLVED | plan:79, :84, :101, :105-:106, :118 | helper:234 compares boot identity; helper:219-223 kernel session and jobs/<sid>.json; helper:253 "No bounded ancestry walk"; helper:83 owner-only mode and :149 st_nlink != 1; plan:118 adds "superseded or not applicable"; actor-context-probe.sh:11 LIMIT = 64 | n/a |
| M-07 | PARTLY | plan:22, :31, :119 | allocation 1+4+4+3 = 12; runner refuses a thirteenth; but the ledger is one line per run with no run-id field and Task 4's four shapes share three sessions (see N-1) | Medium |
| M-08 | RESOLVED | plan:31, :22 | persistence required for resumed and forked runs; live_probe.py:252 sets --no-session-persistence; preflight checks a persisted transcript | n/a |
| M-09 | RESOLVED | plan:44, :31 | subagent and Monitor runs offer the needed tool; helper:427-428 returns for non-Bash tools | n/a (N-9) |
| M-10 | RESOLVED | plan:47, :90, :101 | explicit unavailable branches in Task 2 criterion 1, Task 6, Task 7 | n/a |
| M-11 | RESOLVED | plan:31, :58, :60, :117 | command writes its own selector line to a file; runner copies redacted line with run id and sha256; plan:117 forbids the model's own report | n/a (run id field missing: N-1) |
| M-12 | RESOLVED | plan:114, :117 | launch wrapper, Git and hook process trees, auto-mode variants, decisive distinction are Task 8 rows | n/a (N-8) |
| M-13 | RESOLVED | plan:88, :90, :93-:95 | governed pusher is the helper's run action, labelled controlled; Orca terminal unavailable; HOME and git config pinned; main and master concurrent; Task 5 dependency dropped; test baseline test_launch_job_identity.py:1291-1354 | n/a |
| M-14 | RESOLVED | plan:31, :121 | baseline.json checksums compared in Task 8; blocked and done packages clean now | n/a (N-11) |
| M-15 | PARTLY | plan:55, :58 | records "the session id carried by the hook event" and names the pty /clear session as the reused-process case, but names no capture interface (an ordinary selector result carries no session id, helper:241-242) and the pty run cannot meet the budget cap (N-4) | Medium |
| M-16 | RESOLVED | plan:31, :60 | /proc sweep by cwd, stop by pid while start ticks match, logged; helper:292 os.setsid() | n/a (conflicts with survivor rule: N-3) |
| M-17 | RESOLVED | plan:121, :31, :36 | settings checksum unchanged before and after every real run; no per-run checksum field in the ledger | Low |

## New defects

| id | severity | plan_line | evidence | recommendation |
|---|---|---|---|---|
| N-1 | Medium | plan:22, :31, :66, :119 | ledger is one line per run with the case id; Task 8 counts lines with real_claude true, at most twelve; Task 4 has four shapes in three Claude runs, so one line per shape with real_claude true gives 1+4+4+4 = 13; no run-id field although plan:117 references records by run id | add claude_run_id and a claude_started boolean (true only on the line that starts a Claude process); count distinct started runs; each shape line carries its claude_run_id |
| N-2 | Medium | plan:31, :49, :55, :66 | Tasks 3 and 4 both say "the run group of Task 1" and depend only on Task 2; a Task 4 timeout sweep (cwd under the fixture) can kill Task 3's survivor | one group per task; tear each down at its own task end |
| N-3 | Medium | plan:31 | "per-case cleanup never signals a surviving job" versus "Timeout and teardown also sweep /proc ... and stop each"; a timeout in the resume or fork run would kill the old child and mislabel fork and /clear as "job did not survive" | the timeout sweep must exempt processes registered as surviving; only explicit teardown stops them; label a runner-caused stop distinctly |
| N-4 | Medium | plan:22, :55 | "--max-budget-usd ... (only works with --print)" per claude --help, but the pty /clear run is interactive; live_probe.py:228-255 argv carries --disable-slash-commands which would likely disable /clear [INFERRED]; fresh HOME may show onboarding dialogs [INFERRED] | add an explicit exception for the interactive run (bounded timeout, single scripted turn, no --disable-slash-commands, stated cost bound); "cannot be driven within budget" is the unavailable branch |
| N-5 | Low-Medium | plan:55 | the old child is "a bounded sleep" with no duration; it must outlive the kill, resume, fork and pty runs | state a minimum lifetime (for example 900 s); teardown stops it early |
| N-6 | Low | plan:31, :55 | the kill targets the runner's child handle pid; if claude is a launcher shim the real process could survive [INFERRED]; no check that the first Claude process actually exited | add an AC checking via /proc that no Claude process of the first run remains after the kill |
| N-7 | Low | plan:22, :66 | the four-shapes-in-three-sessions grouping appears only in Constraints; Task 4 does not say how the supervisor-killed shape finds and kills its own supervisor inside one governed command (helper:292 makes the supervisor its own kernel session leader) | put the shape-to-run table and the kill method in Task 4 |
| N-8 | Low | plan:117, :90 | launch-wrapper, Git/hook-tree, auto-mode and decisive rows are limited to observed or unavailable, but Task 6 evidence for wrapper and Git/hook tree is controlled; auto mode has no run and the CLI has --permission-mode, so "unavailable" cannot name a genuinely missing interface (plan:23) | allow controlled for wrapper and Git/hook-tree rows; for auto mode add "not run (budget)" counted as an evidence gap |
| N-9 | Low | plan:31, :44 | preflight flags unspecified; with --tools Bash as in live_probe.py:237-240 the tool list would falsely show subagent and Monitor as not offered | the preflight uses the default tool set |
| N-10 | Low | plan:101, :105 | deep-chain control gives no depth | require depth greater than 64 and bound it for pid limits |
| N-11 | Low | plan:25, :31, :121 | Task 8 compares "git status and diff checksums" of the blocked package while .dev/tasks is staged throughout | use a content hash such as git diff HEAD -- <pkg> or a tree hash, not unstaged status |
| N-12 | Medium (value risk) | plan:22, :31 | the executor runs inside Claude Code so CLAUDECODE is set; a refused nested launch makes the whole real-Claude half unavailable and the report an empty FAIL [INFERRED] | add a Task 1 precondition: run /sc:implement from a terminal that is not a Claude session; unset nothing |
| N-13 | Low | plan:95 | "the only hook installed" needs a script that ignores *.sample files | state the rule |
| N-14 | Info | plan:120 | PASS is unreachable by construction; the binary line carries no information and the two gap lists do the real work | optional: report the contract result and the evidence result separately |

No dependency cycle: Task 1 to Task 2, then Tasks 3 and 4 to Task 7, then Task 8; Tasks 5 and 6 hang off Task 1.

## Coverage statement

INF-001 to INF-010 all covered (10 of 10). INF-006 "no exit-status file" is covered: the matrix miss was lexical (best Constraints, ratio 0.5); the plan's Task 1 heading (plan:29) and ledger (plan:31) provide the exit-status ledger and plan:34, :49, :71, :119 repeat it. The gap list F2.1 to F2.6 is mapped in Task 8 at plan:118: F2.1 and F2.2 need observed evidence, F2.3 and F2.6 can be superseded, F2.4's boot-identity point is superseded by helper:234, F2.5 is closed by the ledger.

## Grade

4 / 5 as an observation plan.

## Confidence (self-reported)

0.80.

## Grounding gaps

Claude Code runtime behaviour is [INFERRED] (resuming a SIGKILLed session, onboarding dialogs in a fresh HOME, --disable-slash-commands effect on /clear, background tasks in print mode, launcher-shim PIDs). Not read: the earlier REPORT.md narrative beyond the findings list, test ranges such as test_launch_job_identity.py:473-488, design lines outside 480-565; actor-context-probe.sh only grepped at line 11. `claude --help` was run to confirm --max-budget-usd is print-only.
