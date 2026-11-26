review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R2 |
| L2 | open | no | single | MAJOR | - | R2 |
| L3 | open | no | single | MINOR | - | R2 |
| L4 | open | yes | overlap | CRITICAL | - | R3, R1 |
| L5 | open | yes | single | MAJOR | - | R1 |

## Blocking findings

### L4

#### L4.t3-1 (F1)

- claim: The explicitly allowed bash -c example can execute bare python3, bypassing the stated UV-only block.
- anchor: "bash -c \"python3 x.py\" (quoted text)"
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L4.t3-1 (F2)

- claim: The candidate does not carry forward the source requirement to read the issue in full before implementation.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

#### L4.t3-1 (F3)

- claim: The live fresh-session check is specified in Task 7, not Task 6.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"

#### L4.t4-1 (F2)

- claim: The plan does not carry forward the driving document's instruction to read issue #357 in full before implementation.
- anchor: "Requirements come from issue #357"

### L5

#### L5.t4-1 (F1)

- claim: The plan allows this command even though Bash executes the quoted string as a child command, so the hook permits a bare python3 invocation.
- anchor: "bash -c \"python3 x.py\" (quoted text)"

## Other findings

- L1 (MAJOR, open, single): Straightforward basename comparison needs python and pip literals in code, so the grep check hits code lines, not only comments and the block message.
- L2 (MAJOR, open, single): Sudo, nice and time options, and timeout options that take an argument, are not skipped, so sudo -E python3 and timeout -k 5s 30 python3 run bare python unblocked.
- L3 (MINOR, open, single): The listed allowed cases have && and | chains but no unquoted ; chain, so that chained-form acceptance needs one extra allowed case beyond the table.

## Reviser brief

Blocking finding ids: L4, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
