review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- R3: report <path>, block ok true
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R3 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | overlap | MAJOR | - | R3, R1, R2 |
| L4 | open | no | overlap | MAJOR | - | R3, R1 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): Design record keeps glm-5.3 as a fixed haiku fact after tiers.md is corrected, so docs disagree; historical-record intent makes this Medium.
- L2 (MAJOR, open, single): Bundled bullets allow two test splits, so exactly-seven needs a guess about function count; Medium, not a stated-text contradiction.
- L3 (MAJOR, open, overlap): Residual allow-list is undefined in membership and could hide a real bypass; no current hit needs it.
- L4 (MAJOR, open, overlap): Scratch copy does not state REPO_ROOT fix, so depending on artifacts depth SKILL_DIR may misresolve; implementer must guess the adjustment, Medium.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
