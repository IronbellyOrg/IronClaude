review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 15b1a9a41b1390e7fc76eb9c142cbd4c4bd4ac2d1875bf20dacb0541758ab3ce
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R2, R3 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 4 requires running a live-check script at .dev/troubleshoot/.../orca_close_repro.py, but that directory and file do not exist in this checkout and the plan never creates it.
- anchor: "Live check against the changed source: `python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py"

#### L1.t2b-1 (F2)

- claim: The constraint requires uv run for Python while Task 4 invokes the live check with bare python3 -I, so no faithful implementation can satisfy both.
- anchor: "Use `uv run` for Python."
- anchor2: "Live check against the changed source: `python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py"

#### L1.t2b-1 (F3)

- claim: Task 1 cleanup uses pkill -f on the per-test copy path instead of only the exact pid, which breaks the stated exact-pid cleanup rule, though the unique tmp path keeps the practical risk low.
- anchor: "Clean up in `finally`: kill the shim by its pid, `pkill -f` the per-test copy path,"
- anchor2: "Every throwaway shim or test process started while working is stopped by its exact pid;"

#### L1.t2b-1 (F4)

- claim: Task 1 never says to wait for or join the streaming thread after the kill, but the reply needs a 4 second pause-stream to finish, so an implementer may assert before the reply completes and get a flaky failure.
- anchor: "and start `_ask_raw(url, \"claude-gw-tier2\", stream=True)` in a thread; after 1 s send SIGTERM to every descendant of the root and the root, wait 0.5 s, SIGKILL survivors"

#### L1.t2b-1 (F5)

- claim: The plan writes ./artifacts/*.log and an after.txt outside the four named scope files and leaves them behind, which sits uneasily with the exact four-file scope and the no-left-behind wording.
- anchor: "no temp files left behind."
- anchor2: "record the command and its failing output in ./artifacts/t1-before.log"

#### L1.t2b-1 (F6)

- claim: Task 4 hardcodes ports 4013 and 4114 while the constraint allows whatever port serves the live shims, so on any machine where the shim serves another port the curl check is meaningless.
- anchor: "The live shims on ports 4013 and 4114 report the same pids before and after"

#### L1.t2b-1 (F7)

- claim: The remediation notes this plan depends on are cited for the kill sequence and doc rules, but none of them exists in this checkout, so those justifications cannot be verified here.
- anchor: "Diagnosis and requirements: `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md` and `REPORT.md`"
- anchor2: "troubleshoot `tier1-observation.md` O8"

#### L1.t3-1 (F1)

- claim: The plan limits scope to four files but requires evidence logs and a live-check output file beyond that scope.
- anchor: "Scope is exactly the four files named in the source:"
- anchor2: "the test fails (record the command and its failing output in ./artifacts/t1-before.log)."

#### L1.t3-1 (F2)

- claim: The live-check acceptance command invokes Python directly, contrary to the stated requirement to use UV for Python operations.
- anchor: "Use `uv run` for Python."
- anchor2: "`python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py <worktree root> <a private mktemp -d scratch dir>`"

## Other findings

none.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
