review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 15b1a9a41b1390e7fc76eb9c142cbd4c4bd4ac2d1875bf20dacb0541758ab3ce
reviewers:
- R3: report <path>, block ok true
- R2: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R3, R2 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: The live-check script and its whole troubleshoot directory are absent from the checkout, so the Task 4 acceptance requiring after.txt output can never pass and the four-file scope forbids creating it.
- anchor: "`python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py <worktree root> <a private mktemp -d scratch dir>`"
- anchor2: "Scope is exactly the four files named in the source:"

#### L1.t1b-1 (F2)

- claim: The cited remediation-source.md and REPORT.md do not exist in this checkout, so the restrictions the candidate attributes to them cannot be verified by the implementer.
- anchor: "Diagnosis and requirements: `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md` and `REPORT.md` in the same directory (issue #341)."

#### L1.t1b-1 (F3)

- claim: No .claude/skills tree exists in this checkout and the candidate never names the make sync-dev step, so verify-sync has no stated path to pass within the four-file scope.
- anchor: "`make lint` and `make verify-sync` pass, with commands and results in ./artifacts/t5-checks.log."
- anchor2: "Scope is exactly the four files named in the source:"

#### L1.t1b-1 (F5)

- claim: Port 4114 currently refuses connections while 4013 answers, so the fixed two-port pid comparison cannot be recorded as written.
- anchor: "The live shims on ports 4013 and 4114 report the same pids before and after (`curl -s http://127.0.0.1:<port>/__ccsession_shim`), recorded in ./artifacts/t4-tests.log."
- anchor2: "Never signal, restart or reconfigure the running shims on ports 4013 and 4114 (or whatever serves them)"

#### L1.t1b-1 (F6)

- claim: Task 1 cleanup uses pkill -f although the candidate's own constraint says throwaway processes are stopped by exact pid; Task 4 also uses python3 despite the uv run constraint and Task 2 omits the fixture start() call.
- anchor: "Clean up in `finally`: kill the shim by its pid, `pkill -f` the per-test copy path, close the gateway, and kill any remaining root process."
- anchor2: "Every throwaway shim or test process started while working is stopped by its exact pid; no temp files left behind."

#### L1.t3-1 (F2)

- claim: live-check uses bare python3 -I while constraints require uv run for Python
- anchor: "Use `uv run` for Python."
- anchor2: "`python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py <worktree root> <a private mktemp -d scratch dir>`"

#### L1.t3-1 (F3)

- claim: troubleshoot directory absent in this checkout so live-check script cannot be run here
- anchor: "Diagnosis and requirements: `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md`"

## Other findings

- L2 (MAJOR, open, single): When the shim already leads a process group the setsid call silently does nothing and the shim stays in the launcher's session, so the goal is unmet for hand-started shims and Task 2's Popen fixture cannot catch it.
- L3 (MINOR, open, single): pgrep on tmp path cannot match sleep 60, so a leaked sleep passes this check

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
