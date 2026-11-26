review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 2da8dc1d6e06cf9a184d60842a7a79012d17e24d428a6f885f95a80a56569c06
reviewers:
- R2: report <path>, block ok true
- R1: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | R2 |
| L2 | open | no | single | MAJOR | C-7 | R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MAJOR | C-1 | R2 |
| L5 | open | no | single | MAJOR | WC-10 | R2 |
| L6 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Design file absent from worktree, so exact-wording copy and v1-carriage acceptance cannot be performed as written.
- anchor: "Use the exact wording of section 10.2 of the design (read it in pieces of at most 80 lines)."

## Other findings

- L2 (MAJOR, open, single): C-7 sentence omits worker's own observation as a permitted positive proof.
- L3 (MAJOR, open, single): Sweep omits projection.liveness, stage, attention and transcript-timestamp facts source states to respect.
- L4 (MAJOR, open, single): Deadline W is named but never given a value, leaving C-1 probe authorisation undefined.
- L5 (MAJOR, open, single): Second WC-10 key overwrites existing WC-10 pin, breaking a pin required to keep passing.
- L6 (MINOR, open, single): Invented fence constraint with no source or test basis; which fences is unspecified.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
