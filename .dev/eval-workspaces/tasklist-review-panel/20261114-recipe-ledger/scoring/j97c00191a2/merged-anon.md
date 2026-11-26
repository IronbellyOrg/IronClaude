review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | CRITICAL | - | R1, R2, R3 |
| L2 | open | no | single | MINOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |

## Blocking findings

none.

## Other findings

- L1 (CRITICAL, open, overlap): An implementer who follows the edit-scope rule as written builds no artifacts files, and Task 12 cannot pass.
- L2 (MINOR, open, single): Follow-up candidate: orgs path notation differs from orgs/<owner of R>/issue-fields used in Tasks 2, 3 and 5.
- L3 (MAJOR, open, single): Follow-up candidate: source requires body file under .dev/issues/<N>/ after rename, but candidate never names that path.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
