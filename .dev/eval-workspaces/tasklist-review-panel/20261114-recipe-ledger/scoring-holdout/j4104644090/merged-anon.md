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
| L1 | open | no | single | MAJOR | WC-3 | R2 |
| L2 | open | no | single | MAJOR | WC-10 | R2 |
| L3 | open | no | single | MINOR | - | R2 |
| L4 | open | no | single | MINOR | - | R2 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): A WC-3 ask-timeout pin with ident WC-3 has no line holding WC-3 and its phrase, so test_contract_states_rule fails.
- L2 (MAJOR, open, single): If WC-10 is rewrapped across lines, the WC-10 ident and never as death no longer share a line and the pin fails.
- L3 (MINOR, open, single): The fence number rule has no enforcing test, so an implementer must guess how to render numbered ladder and table lines.
- L4 (MINOR, open, single): A smaller suite can replace the full tests run, leaving the pass claim unverified for the full suite.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
