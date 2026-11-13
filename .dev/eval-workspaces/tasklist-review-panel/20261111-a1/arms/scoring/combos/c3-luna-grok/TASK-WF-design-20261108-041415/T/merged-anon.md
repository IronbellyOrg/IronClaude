review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R2 |
| L2 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: A create flow that writes only the issue type and one Complexity POST drops the mode label and the pushback comment that the goal and Task 2 require.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "mode label only; `--type` when listed; `gh issue create` and the rename; type read-back; field POST and read-back; pushback comment"

## Other findings

- L2 (MAJOR, open, single): The plan orders a field read-back but never says how to read it, so matching the POST's value string to the GET value reports a successful Complexity write as not applied.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
