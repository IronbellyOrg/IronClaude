review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 2da8dc1d6e06cf9a184d60842a7a79012d17e24d428a6f885f95a80a56569c06
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | WC-14, WC-15, WC-3, WC-5 | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | WC-11 | R1 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: WC-14 makes the next Command the next action while WC-15 requires a handoff write after each Command, so both cannot be the immediate next action.
- anchor: "when a `Command:` line finishes, the next action in the same turn is the next `Command:` line or the WC-5 steps after the last one"
- anchor2: "after each `Command:` line write `<report-dir>/handoff/<n>-<command>.md`"

#### L1.t2b-1 (F7)

- claim: WC-14 permits ending the turn while blocked in ask, but WC-3 requires resuming the same message ID on ask timeout.
- anchor: "while blocked in the preamble's `ask`"

## Other findings

- L2 (MAJOR, open, single): Candidate omits the source fact that a background heartbeat loop is allowed, which is why a timer heartbeat is not progress evidence.
- L3 (MAJOR, open, single): Sweep never names projection.liveness, stage.activity, attention.categories or transcript timestamps needed to fill the state table.
- L4 (MAJOR, open, single): Restart list omits the source positive proof of the worker's own observation, so that leave-the-wait path is lost.
- L5 (MINOR, open, single): ./artifacts is ambiguous between the staged package folder and the never-staged repo-root artifacts folder.
- L6 (MINOR, open, single): Fence numbered-line ban is unexplained and untied to any test, sitting beside required numbered state and ladder content.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
