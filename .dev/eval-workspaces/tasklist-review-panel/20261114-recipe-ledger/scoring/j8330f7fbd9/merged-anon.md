review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <path> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | 2.3, 3.1 | R1 |
| L2 | open | no | single | MAJOR | 2.1, 2.5 | R1 |
| L3 | open | no | single | MAJOR | 3.1 | R1 |
| L4 | open | no | single | MINOR | 3.1 | R1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 10 acceptance forbids gh api user, but the design doc contains gh api user and source 2.3 allows user, so the check cannot pass.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

## Other findings

- L2 (MAJOR, open, single): Plan leaves POST input as generic <file>, dropping required post-rename path .dev/issues/<N>/complexity-field.json.
- L3 (MAJOR, open, single): Command task drops source requirement that area also appears in pushback comment, keeping only flags.md.
- L4 (MINOR, open, single): HOW-WE-WORK line 329 is stale, live line is 333, so implementer must re-read despite exact line citation.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
