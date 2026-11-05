# Hypothesis: when `timeout` is missing, `bounded()` runs the command in the foreground, so a hung git read is waited out in full and the 60-second budget is only checked after it returns (A2)

**Agent**: root-cause-analyst (lens; worker troubleshoot-analyst)
**Tier**: 2
**Timestamp**: written by the parent on receipt (see audit.log)
**Cause class**: missing fallback (the deadline is enforced only between commands)
**Claim class**: `environment_dependent`
**Evidence class**: `runtime_repro` (parent probe, probe-evidence.out:7-8)
**Verdict direction**: `AFFIRM` (agrees with Tier 1 A2, endorses the draft)
**Consistency with docs**: aligned (the fix makes the header promise at collect-conflict-evidence.sh:25-26 hold; design :841)
runs-in=src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh:74-88 @ local operator checkout (bash, git)
environment-property: `timeout` absent from PATH (2x2 below; rows in diagnosability-tasklist.md `## Discriminator rows` D-1 to D-4)
producer-citation-check: skipped — menu absent or empty (producers.md header-only)

## Claim
At HEAD the no-`timeout` branch runs `"$@"; rc=$?` in the foreground; `check_deadline` compares SECONDS only before and after, so a hung read is not stopped while running. The failure needs both: `timeout` absent and a read running past the budget.

| 2x2 | read hangs past budget | read does not hang |
|---|---|---|
| `timeout` absent | D-1 unfixed: elapsed=65s, exit=2 (probe-evidence.out:7-8); draft: elapsed=61s, exit=2 (probe-evidence.out post-fix section) and P-1 passed | D-2 draft: test_without_timeout_a_normal_run_still_succeeds passed |
| `timeout` present | D-3 stub exit 124 -> EVIDENCE_FAIL timeout (test_a_command_hitting_the_time_bound_is_timeout passed); token mapping only, no real hang | D-4 existing success tests E1-E3 passed |

## Evidence
| # | Kind | Source | Content |
|---|---|---|---|
| E1 | command_output | probe-evidence.out:7-8 | wrapper sleeps 65 s on show, no timeout: exit=2, elapsed=65s (stdout discarded) |
| E2 | source_citation | tier1-hypothesis.md (HEAD form); src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh:68-70 | HEAD else branch, then check_deadline |
| E3 | source_citation | collect-conflict-evidence.sh (draft bounded()) | background job, kill -0 poll, TERM, 1 s grace, KILL, wait, fail timeout |
| E4 | source_citation | collect-conflict-evidence.sh:49-53 | fail writes to fd 3/4, which only the job closes |
| E5 | test_assertion | tests/pr_submit/test_conflict_scripts.py (P-1 hang test; no-hang test; helper) | 90 s exec-sleep hang must end under 75 s with EVIDENCE_FAIL timeout; no-hang exits 0 under 30 s; no temp dir; one stdout line; all passed (audit.log) |
| E6 | behaviour-definition | behaviour-definition: row 1 (observed), row 3 (verified by P-1) | foreground wait; kill -0 / kill |

## Proposed Fix
Keep the draft `bounded()` with its tests: local to one function; at most ~1.2 s past the budget; no banned words. bash reaps finished background children, so `kill -0` then fails (checked by the no-hang test).

## Confidence
Self-reported 0.85 (calibrator re-grades).

## Risks
- With job control off, background jobs ignore SIGINT/SIGQUIT; an operator interrupt during the poll leaves the read running; cleanup() removes $TMP but does not kill $pid (possible follow-up).
- A wrapper without exec leaves its sleep child after TERM; fds 3/4 closed keep it off the caller's pipes.
- PID reuse window (very small).

## If I'm wrong, it's probably because...
The 61 s figure came from the probe's own 65 s sleep ending; P-1's 90 s hang settles it (passed under 75 s).

## Falsification standard
P-1 taking 75 s or more, or stdout other than EVIDENCE_FAIL timeout, refutes the fix; the no-hang test taking 30 s or more refutes the poll loop; on HEAD a 90 s hang stopped before 60 s refutes the claim.

## Alternatives considered
- Fail usage when timeout is missing: rejected (hard Tier 3 on hosts without timeout).
- Watchdog subshell: works, but a second job to reap and kill.
- perl alarm / gtimeout: rejected (another external program).
