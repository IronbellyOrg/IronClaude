review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 2da8dc1d6e06cf9a184d60842a7a79012d17e24d428a6f885f95a80a56569c06
reviewers:
- R1: report <path>, block ok true
- R3: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | CRITICAL | C-1, C-17 | R1 |
| L2 | open | no | overlap | MAJOR | - | R1, R2 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

none.

## Other findings

- L1 (CRITICAL, open, single): Design file .dev/brainstorms/.../merged-requirements.md is absent, so exact C-1 to C-17 wording cannot be produced or checked.
- L2 (MAJOR, open, overlap): Task 6 drops source facts: projection.liveness verdict fields, transcript millisecond timestamps, leave-a-wait-only-on-positive-proof, and background heartbeat loop note.
- L3 (MINOR, open, single): Invented fence restriction is not stated in source and can force omission of exact design wording inside fences.
- L4 (MINOR, open, single): Copies check omits docs/developer-guide and docs/designs references found by whole-tree search, so evidence is narrower than the no-other-copy claim.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
