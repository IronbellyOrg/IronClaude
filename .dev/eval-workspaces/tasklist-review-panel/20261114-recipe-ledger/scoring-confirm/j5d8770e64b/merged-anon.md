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
| L2 | open | no | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | overlap | MAJOR | - | R2, R3 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: The live-check script and its whole troubleshoot directory are absent from the checkout and no task creates them, so the Task 4 live-check acceptance criterion cannot pass.
- anchor: "`python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py <worktree root> <a private mktemp -d scratch dir>`"
- anchor2: "Scope is exactly the four files named in the source"

#### L1.t1b-1 (F3)

- claim: The exact-pid stop rule and the pkill -f cleanup instruction conflict; the plan never says which governs, though the unique tmp path limits the harm.
- anchor: "Every throwaway shim or test process started while working is stopped by its exact pid"
- anchor2: "`pkill -f` the per-test copy path"

#### L1.t1b-1 (F5)

- claim: Only port 4013 answers a health probe in this environment; 4114 refuses the connection, so there is no 4114 pid to record before and after.
- anchor: "The live shims on ports 4013 and 4114 report the same pids before and after"

#### L1.t1b-1 (F7)

- claim: Task 1 never says to capture and join the thread result or read url from the seen file, though its acceptance criteria assert on the streamed reply.
- anchor: "start `_ask_raw(url, \"claude-gw-tier2\", stream=True)` in a thread"

#### L1.t3-1 (F1)

- claim: Task 4 live-check acceptance cannot pass because orca_close_repro.py and its directory do not exist in the checkout.
- anchor: "`python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py <worktree root> <a private mktemp -d scratch dir>`"

#### L1.t3-1 (F2)

- claim: The uv-run-only constraint contradicts the bare python3 live-check command; an implementer must guess which wins.
- anchor: "Use `uv run` for Python."
- anchor2: "`python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py <worktree root> <a private mktemp -d scratch dir>`"

#### L1.t3-1 (F4)

- claim: Task 1 never states joining the streaming thread, so the post-kill assertions rely on an inferred join step.
- anchor: "in a thread; after 1 s send SIGTERM"

## Other findings

- L2 (MAJOR, open, single): No task runs make sync-dev before verify-sync and .claude/skills is absent in this checkout, so the required verify-sync pass has no stated path.
- L3 (MAJOR, open, single): A shim that already leads its process group silently stays in the launcher session after the swallowed OSError, with no warning or stated scope limit.
- L4 (MAJOR, open, overlap): The test body runs before fixture teardown, so the in-test assert variant cannot observe the shim after teardown; only the external pgrep variant works.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
