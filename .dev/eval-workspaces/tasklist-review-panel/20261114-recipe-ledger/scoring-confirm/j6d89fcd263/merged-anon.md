review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 1f84077e475af7358384ebaf383d03500bc6d6e46b9a85e8a977a67a18341e0a
reviewers:
- R2: report <path>, block ok true
- R1: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R2 |
| L2 | open | no | overlap | MAJOR | - | R2, R1 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MINOR | - | R2 |
| L5 | open | no | overlap | MINOR | - | R2, R1 |
| L6 | open | no | single | MAJOR | - | R1 |
| L7 | open | no | single | MAJOR | - | R1 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): Task 10 scopes merge_wait tests to the four presence combinations, so no task explicitly assigns assertions for the pending, incomplete and declined merge-table rows.
- L2 (MAJOR, open, overlap): The dry-check acceptance depends on live PR 336 state and gh credentials, so correct code can fail it if the PR threads change; no frozen fixture backs this check.
- L3 (MAJOR, open, single): Task 12 depends only on Task 9 but its snapshot gate and Wave 6 text use classify_codex from Task 7 and merge_wait from Task 8, which the declared dependency graph does not order before it.
- L4 (MINOR, open, single): The grouping key is unspecified when both line and original_line are None, so location-less findings on one path would be grouped together by default.
- L5 (MINOR, open, overlap): No task updates the member-count message in run_log.py, already stale at 37, so it remains wrong after the enum grows to 41.
- L6 (MAJOR, open, single): Design file absent from checkout and never quoted, so gate rules, merge table and fixture shapes cannot be built or checked from the candidate alone.
- L7 (MAJOR, open, single): Contract writer/candidate paths untouched, so Codex fields do not round-trip through a locked contract.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
