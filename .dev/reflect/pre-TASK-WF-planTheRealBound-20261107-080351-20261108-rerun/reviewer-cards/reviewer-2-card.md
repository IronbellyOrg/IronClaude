# Reviewer 2 card (qa, opus class / alias claude-gw-tier1a), UC-1

(Returned by the reflect-reviewer agent; persisted by the parent on receipt at 2026-11-08T02:06Z. plan:N = line N of the plan; helper = src/superclaude/hooks/scripts/launch-job-identity.sh.)

**Verdict:** an executor can produce an honest binary result from this plan, not a meaningful one. FAIL is reachable on every path and PASS is unreachable. Several mechanical contradictions would force the executor either to mislabel cases or to break its own cleanup rules. Fix the Medium findings before running it.

Also read by the reviewer: helper 1-566, live_probe.py 1-353, design 489-566, review-2.md 1-12, test_launch_job_identity.py 1288-1357, actor-context-probe.sh line 11.

## Findings (own, from reading the plan first)

| id | severity | plan_line | evidence (quoted) | recommendation |
|---|---|---|---|---|
| Q-1 | Medium | 55 | "attempt a pty-driven interactive Claude session in the throwaway HOME, send /clear, then run one governed Bash command" | the plan never says which identity the pty session starts with; after /clear the expected status is ordinary, not governed; state the order: start or resume the pty session as the governed id, run one Bash call (expected governed), send /clear, run one Bash call (expected ordinary) while the old child is alive; state the expected status of each call |
| Q-2 | Medium | 114, 117, 31, 55, 23 | report rows may only be "observed, controlled or unavailable" and "no unavailable row lacks a named interface"; but the ledger also has "blocked" (:31), Task 3 has "unobserved with the reason 'child identity changed'" (:55) and "job did not survive" | some outcomes are not a missing interface (timeout, dead job, model did not follow the prompt, budget cut); add a row category "not observed (reason)" counted as an evidence gap |
| Q-3 | Medium | 114, 117 | "The launch wrapper, Git and hook process tree, auto-mode and decisive-distinction rows are each observed or unavailable" | no task produces evidence for the launch wrapper or for auto mode; add one bounded observation for each, or allow "not run (budget)" as an evidence gap |
| Q-4 | Medium | 120, 79 | "Because Task 5 can label release, PID reuse and boot identity only controlled" | release can be observed for real: it is deleting the session record (design:526, :557; helper:238-241); after Task 3's decisive measurements and before teardown, delete the governed record and run identify on the real surviving child; no extra Claude run; closes the "no release with a live child" part of F2.4 with observed evidence |
| Q-5 | Low-Medium | 90 | "no real Claude run is spent on this task" | design:504 asks for "Bash/Monitor-to-Git and hook process trees"; a Git push started by a real governed Claude Bash call is never observed; add one push to the disposable bare repository inside an existing governed run (for example Task 2's governed run) |
| Q-6 | Low-Medium | 31, 66, 71 | the sweep targets "processes whose working directory is under the fixture repository or the group's temporary directory", but Task 4 creates "a deliberate setsid daemonized child" and requires "every descendant stopped" | a daemon that changes directory to / escapes the cwd sweep; teardown should also stop every process id recorded in ready files and case artifacts after checking start ticks |
| Q-7 | Low | 55, 59 | decisive case "child governed with the old origin, new session ordinary" | a fork gets a new session id with no record so the adapter treats it as ordinary (helper:435-437); state the expected fork status so the report cannot count it toward the separation by default |
| Q-8 | Low | 44 | "the count of parent hops from the command's shell up to the Claude process" | no rule identifies "the Claude process"; have the runner write the pid of its Claude child into the group's temporary directory, have the command walk the parent chain to that pid with a cap, and record "not reached" on failure |

## Judgement on the Tier 1 defects

N-1 confirm (Medium: one line per shape would push the count to 13 and the guard against a thirteenth run could refuse a legitimate shape); N-2 confirm (Medium-Low); N-3 confirm (Medium: a case timeout during resume kills the old child, its cwd is the fixture); N-4 confirm, budget part [INFERRED] (reviewer did not read claude --help; live_probe.py:253 passes --disable-slash-commands and plan:31 exempts only --no-session-persistence); N-5 confirm (Low); N-6 confirm (Low, [INFERRED], live_probe.py:129 uses shutil.which); N-7 confirm (Low; supervisor is its own session leader, helper:292); N-8 partly refute then extend (Task 6 covers only Git/hook tree, as controlled; no task produces launch-wrapper evidence; see Q-3, Q-5); N-9 confirm (Low-Medium; live_probe.py:237-240 uses --tools Bash); N-10 confirm (Low; historical cap 64, actor-context-probe.sh:11); N-11 confirm (Low); N-12 confirm (Medium, value risk, [INFERRED]; live_probe.py:280 detects the nested-launch refusal); N-13 confirm (Info/Low); N-14 confirm and strengthen (PASS is blocked by several independent causes: Task 5 controlled only, human terminal unavailable (plan:90), Monitor and setsid escapes never count (plan:120; helper:428), wrapper and auto-mode rows have no task; Q-4 removes only the release cause).

## Coverage of INF-001..INF-010

10 of 10 covered. INF-001 plan:15, :22; INF-002 covered with a minor gap (the done package is named only as read-only, plan:20; its live-harness-events.jsonl is never used as an input); INF-003 Tasks 2, 3, 4, 6; INF-004 plan:79, :84, helper:234; INF-005 covered but controlled only although observed evidence is reachable (Q-4); **INF-006 covered: confirms Tier 1 and refutes the lexical miss** (plan:29 heading "exit-status ledger", plan:31 run-status.jsonl with "exit code or signal", plan:34, :49, :71, :119); INF-007 Task 7, plan:101-106, helper:219-223, :253; INF-008 Task 8, plan:120; INF-009 plan:21, :22, :25; INF-010 plan:20, :121.

## Run budget arithmetic

1 (preflight) + 4 (Task 2) + 4 (Task 3) + 3 (Task 4) = 12, matching plan:22. Holds only if the ledger counts started Claude processes, not cases (N-1). The interactive /clear run may sit outside the dollar cap (N-4). The skip path (a refused launch or missing authentication spends no further runs) is consistent at plan:31, :47, :66.

## FAIL reachable, PASS unreachable honestly?

Yes on both. The plan says so itself (plan:120) and blocks a false PASS: every row must be observed, escapes never count, "superseded" is barred for lifecycle findings (plan:118). The binary line is fixed before any run, so the information is in the two gap lists; Q-2 and Q-3 are needed to keep those lists honest.

## Grade and confidence

Best-practice grade 3/5. Confidence 0.8.

## Grounding gaps

claude --help not read (the --max-budget-usd limitation, the effect of --disable-slash-commands on /clear and whether /clear and fork create new session ids are [INFERRED]); nested-launch refusal from this host not observed; the done package TASK-WF-authorizedNarrow-20261106-214325 and the blocked package beyond review-2.md and actor-context-probe.sh line 11 not read; how Claude's Bash tool times out and which process groups it kills after the Claude process is killed are [INFERRED].
