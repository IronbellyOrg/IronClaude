```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.84
citations_total: 48
citations_revalidated: 48
citations_dropped: 0
citations_inferred: 3
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report: B-CTX observation plan, UC-1 pre-execution re-run

- Plan under review: `.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/TASK-WF-planTheRealBound-20261107-080351.md` (the working tree includes the edits for findings M-05 to M-17, not yet committed)
- Spec: `.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/source.md`
- Date: 2026-11-08
- Tier reached 2: the Tier 1 card was calibrated at 0.86 and would have stopped on confidence alone, but the sparse-spec guard (inferred 10 > parsed 0) forbids a Tier 1 stop. Two reviewers (haiku class analyzer, opus class qa) reviewed in parallel, were calibrated by a separate sonnet-class calibrator (0.83 and 0.84), and an adversarial merge (depth quick, Round 1 only) produced `adversarial/merged-verdict.yaml`.
- Status is `partial` because the debate did not converge (strict 40.0%, threshold 80%; depth quick has no rebuttal round) and because two protocol steps were not run (listed under Degraded components).

## Verdict

**PASS-WITH-FIXES (advisory).** The earlier run judged the plan FAIL-ADVISORY: it could not produce a meaningful binary B-CTX result. That is no longer true. Fourteen of the seventeen earlier findings (including all four HIGH ones) are resolved in the text; three (M-07, M-12, M-15) are only partly resolved. An executor can now produce an honest and informative result. What remains is nine MEDIUM execution-readiness defects (M2-01 to M2-09) that should be fixed before the plan is run, four LOW items and one INFO item. The plan has no ledger yet (the package holds only source.md, the plan and return-contract.yaml), so it can still be edited (plan:25 freezes it only once implementation starts).

## What changed since the earlier review (M-01 to M-17)

| Earlier finding | Now | Where |
|---|---|---|
| M-01, M-02, M-03, M-04, M-05, M-06, M-08, M-09, M-10, M-11, M-13, M-14, M-16, M-17 | resolved | Tier 1 card re-read of the plan; both reviewers found nothing contradicting |
| M-07 (run budget) | partly resolved | the budget arithmetic now holds (plan:22) but the ledger cannot be audited against it: M2-06 |
| M-12 (missing cases in Task 8) | partly resolved | the cases are named (plan:114) but no task acquires wrapper, tree or auto-mode evidence: M2-04 |
| M-15 (session id across resume, fork, /clear) | partly resolved | the id is recorded (plan:55) but the topology and expected statuses are unspecified: M2-03 |

M-02 and M-16 are resolved individually but conflict with each other (survivor protection versus the timeout sweep): M2-01.

## Findings (HIGH/MEDIUM/LOW scale)

| id | severity | plan_line | finding | recommendation |
|---|---|---|---|---|
| M2-01 | MEDIUM | plan:31, :35, :55-60 | the plan says per-case cleanup "never signals a surviving job or its supervisor" yet timeout and teardown sweep /proc by working directory and stop each match; a timeout during the resume or fork run would kill the old child and mislabel later cases; a setsid daemon that changes directory escapes the sweep | exempt registered survivors from timeout sweeps, label a runner-caused stop differently, add a self-check that times out a dependent run while the survivor lives, stop every recorded pid at teardown after a start-ticks check |
| M2-02 | MEDIUM | plan:22, :55 | every real run is capped with --max-budget-usd 0.25 but Task 3 needs an interactive pty session, and the archived CLI help says the option "only works with --print" (.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/claude-help.txt:131-132) | owner decision before execution: record the pty /clear case unavailable, or authorize a separately bounded interactive run without --disable-slash-commands (live_probe.py:253) |
| M2-03 | MEDIUM | plan:55, :59 | the reused-process /clear case is not set up: the first Claude process is killed and a different pty process is started, the starting identity and the expected status of each call are unstated, and the fork's expected status (ordinary, helper:435-437) is unstated | state the controller identity, the ordered calls (governed, /clear, ordinary) and the fork status; name how the event's session id is captured |
| M2-04 | MEDIUM | plan:44, :90, :114, :117 | no task acquires launch-wrapper, Git and hook process-tree or auto-mode evidence, yet Task 8 requires those rows "observed or unavailable"; Task 6 uses controlled actors and spends no real Claude run (plan:90) | add redacted tree snapshots, one bounded observation each or a "not run (budget)" label, and one real governed Git push inside an existing run |
| M2-05 | MEDIUM | plan:23, :31, :55, :117 | report rows allow only observed, controlled or unavailable-with-an-interface, but the plan itself produces "blocked", "child identity changed" and "job did not survive the first Claude process ending" | add a row category "not observed (reason)" counted as an evidence gap |
| M2-06 | MEDIUM | plan:22, :31, :66, :119 | the plan does not force a thirteenth Claude start (four Task 4 shapes share three sessions), but the ledger field list at plan:31 names no run id and plan:119 counts ledger entries with real_claude true, so the cap cannot be audited; this corrects the Tier 1 claim | add claude_run_id and claude_started to the ledger |
| M2-07 | MEDIUM (value risk) | plan:22, :31 | [INFERRED] if the executor runs inside Claude Code a nested launch may be refused and the real-Claude half becomes an empty FAIL | add a precondition: run from a terminal that is not a Claude session; unset nothing |
| M2-08 | MEDIUM | plan:31, :49, :55, :66 | Tasks 3 and 4 both use "the run group of Task 1", so a Task 4 sweep can kill Task 3's survivor | one run group per task |
| M2-09 | MEDIUM (opportunity) | plan:79, :120 | release can be observed for real by deleting the governed session record after Task 3 (design:526, :557; helper:238-241) at no extra Claude run; it removes one of the independent causes of the fixed FAIL | add the step to Task 3, with identify run inside a later real Claude Bash call so it counts as observed |
| M2-10 | LOW | plan:55 | the old child is "a bounded sleep" with no duration | state a minimum lifetime such as 900 s |
| M2-11 | LOW | plan:66, :69 | the reparent shape samples before the intermediate parent exits and proves no reparenting (helper:292-295 installs a subreaper) | require the parent to exit and the PPID to change before sampling |
| M2-12 | LOW | plan:22, :66 | the shape-to-session grouping is only in Constraints; the supervisor-kill method is unstated | add a shape-to-run table and the method to Task 4 |
| M2-13 | LOW | plan:31, :44, :55, :95, :101, :121 | small items, each with its line: confirm the first Claude process exited (plan:55; launcher-shim pid [INFERRED]); the preflight uses the default tool set (plan:31); identify the Claude pid for the hop count (plan:44); ignore *.sample hooks (plan:95); the deep chain states a depth above 64 (plan:101); compare content hashes instead of unstaged git status (plan:121) | apply each |
| M2-14 | INFO | plan:118-120 | PASS is unreachable by construction, so the binary line carries no information by itself | optionally report the contract result and the evidence result separately |

## Coverage of the spec (Step 1B.0)

Pass 1 found no requirement IDs (source.md is one inline paragraph); Pass 2 inferred ten requirements, each quote-pinned to `source.md:1`. The deterministic containment rule matched 9 of 10; INF-006 was a lexical miss (the plan says "exit-status ledger") and is covered. coverage_pct (parsed) is null; coverage_pct_union is 1.0; INF-003 stays Partial (M2-03, M2-11) and INF-005 is covered as controlled evidence only (M2-09).

## Inferred requirements (Pass 2)

| id | quote | citation | match result |
|---|---|---|---|
| INF-001 | Plan the real bounded observation run that the blocked package .dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206 (its Task 1, the B-CTX feasibility gate) never completed. | source.md:1 | Constraints (0.72, containment); covered with defects M2-01, M2-02 |
| INF-002 | Use docs/designs/sc-issue-launch-level-hook.md section 19 | source.md:1 | Constraints (0.75); covered with a gap M2-04 |
| INF-003 | unobserved real cases (ordinary Claude session in the same worktree, /clear, resume into a new process, detached or reparented job, same-worktree human terminal, Monitor and nested subagent) | source.md:1 | Task 8 (0.90); Partial M2-03, M2-11 |
| INF-004 | boot identity not compared in the selector | source.md:1 | Task 8 (1.00); covered, helper:234 compares boot identity |
| INF-005 | no release with a live child | source.md:1 | Task 5 (1.00); covered as controlled evidence only, M2-09 |
| INF-006 | no exit-status file | source.md:1 | none (0.50, lexical miss); confirmed covered by Task 1 (plan:29, :31) |
| INF-007 | the unmeasured ancestry bound | source.md:1 | Task 7 (0.67); covered, helper:219-223 and :253 |
| INF-008 | Plan only observation evidence and the report with a binary result | source.md:1 | Task 8 (0.83); covered with a defect M2-05 |
| INF-009 | no production hook, no real protected-branch push, no change to global Claude settings, no commit or push | source.md:1 | Constraints (0.80); covered, plan:21-25 |
| INF-010 | Do not modify the blocked package -210206. | source.md:1 | Constraints (0.75); covered, plan:20, :121 |

## Evidence

- `helper:338` (src/superclaude/hooks/scripts/launch-job-identity.sh:338) `if status is not None and not live:` is the only normal return of the supervise loop, so a governed call waits for ordinary descendants.
- `helper:234` (src/superclaude/hooks/scripts/launch-job-identity.sh:234) `... or boot() != value['boot']:` compares start ticks and boot identity.
- `helper:253` (src/superclaude/hooks/scripts/launch-job-identity.sh:253) `# No bounded ancestry walk or truncated scan is interpreted as ordinary.`
- `helper:292` (src/superclaude/hooks/scripts/launch-job-identity.sh:292) `os.setsid()` in `supervise`: the supervisor is its own session leader.
- `helper:435` (src/superclaude/hooks/scripts/launch-job-identity.sh:435-437) a session id with no record is not rewritten, so the work is handled as ordinary.
- `design:504` (docs/designs/sc-issue-launch-level-hook.md:504) names the required cases including "Bash/Monitor-to-Git and hook process trees" and the reused-process distinction.
- `design:555` (docs/designs/sc-issue-launch-level-hook.md:555) command completion waits for ordinary live descendants "deliberately".
- `live_probe:253` (tests/hooks/fixtures/launch_level/live_probe.py:253) passes `--disable-slash-commands`.
- `help:131` (.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/claude-help.txt:131-132) the budget option "only works with --print".
- `plan:22` (the plan, line 22) twelve real Claude runs, budget "the preflight one, Task 2 four, Task 3 four and Task 4 three".
- `plan:31` (the plan, line 31) the ledger is "one JSON line per run" and per-case cleanup "never signals a surviving job or its supervisor".
- `plan:55` (the plan, line 55) the pty-driven interactive /clear step and the survivor rules.
- `plan:66` (the plan, line 66) the reparent shape samples "inside the same governed command before it exits".
- `plan:117` (the plan, line 117) rows are "observed or unavailable"; "no unavailable row lacks a named interface" is at plan:117.
- `plan:119` (the plan, line 119) the report counts real Claude runs (real_claude true), at most twelve.

## Grounding gaps

- All Claude Code runtime behaviour is [INFERRED] and was not observed: survival of the supervisor and child after a SIGKILL of Claude, whether /clear changes the session id, nested-launch refusal from the executor's terminal, driving a pty session in a fresh HOME, tool timeouts, and launcher-shim pids.
- The archived CLI help file may differ from the installed CLI (not re-run).
- Reviewers read only; nothing was executed. A dry run of the runner is the plan's own preflight.
- `actor-context-probe.sh:11` (LIMIT = 64) was only grepped by two reviewers and not re-read by a calibrator.

## Degraded components

- `position-bias-pass: not-run` (the reverse-order second qualitative evaluation was skipped).
- `invariant-probe: skipped` (depth quick skips Round 2.5), and no rebuttal round (Round 2) ran; convergence is strict 40.0% (6 of 15 points), 46.7% by substance.
- `t2_vendor_diversity: single` (the three model aliases are gateway tier names of one proxy); `t2_model_class_diversity: full`; calibrator class (sonnet) equals the executor class (the plan was authored in this session): the executor-reviewer partition holds, the executor-calibrator partition does not.

## Recommendations

1. Edit the plan for M2-01 to M2-08 before running it (all are wording changes; none adds a Claude run). Decide M2-02 first: it needs an owner choice between recording the pty /clear case unavailable and authorizing a separately bounded interactive run.
2. Take M2-09 (observe release for real) if the owner wants one more cause of the fixed FAIL removed at no cost.
3. Re-run this review at `--depth standard` after the edits if a converged debate is wanted.
