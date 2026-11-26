review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 2da8dc1d6e06cf9a184d60842a7a79012d17e24d428a6f885f95a80a56569c06
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | 10.2, C-1, C-17 | R2 |
| L2 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Design file named as the source of exact wording is absent from this worktree, so verbatim C-1 to C-17 text cannot be obtained and exact-wording criteria cannot pass.
- anchor: "Use the exact wording of section 10.2 of the design (read it in pieces of at most 80 lines)."

## Other findings

- L2 (MAJOR, open, single): Source states a leave-a-wait-only-on-positive-proof rule plus worker-list projection facts; no task carries that rule into contract text or pins.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
