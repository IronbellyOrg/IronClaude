review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <path> sha256 2da8dc1d6e06cf9a184d60842a7a79012d17e24d428a6f885f95a80a56569c06
reviewers:
- R2: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MINOR | C-1, WC-10 | R2 |
| L2 | open | no | single | MAJOR | WC-11 | R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MINOR | - | R2 |
| L5 | open | no | single | MINOR | - | R2 |
| L6 | open | no | single | MAJOR | C-7 | R1 |

## Blocking findings

none.

## Other findings

- L1 (MINOR, open, single): Example pin phrase never as death will not be found if the contract carries C-1 wording absence is never death.
- L2 (MAJOR, open, single): Sweep text omits projection.liveness verdicts and millisecond transcript stamps required as coordinator facts.
- L3 (MAJOR, open, single): Exact-wording rule conflicts with summarise instruction for the new subsection, so the implementer must guess.
- L4 (MINOR, open, single): Artifacts path is ambiguous between project root and package folder, risking unstaged logs or a wrong staging set.
- L5 (MINOR, open, single): Plan omits the source fact that a background loop is allowed, which explains why timer heartbeats are not progress proof.
- L6 (MAJOR, open, single): The C-7 checklist omits the worker's own observation as a positive basis for leaving a wait, so that required case is not pinned into the coordinator procedure.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
