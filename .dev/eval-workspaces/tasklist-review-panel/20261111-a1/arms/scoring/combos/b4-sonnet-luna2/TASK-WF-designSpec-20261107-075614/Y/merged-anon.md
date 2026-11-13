review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | no | single | MAJOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | yes | single | MAJOR | - | R2 |

## Blocking findings

### L7

#### L7.R2 (F1)

- claim: The script’s required repository-resolution fallback cannot satisfy Task 7’s static check that every gh line carry --repo or a repos/ path.
- anchor: "asserts every `gh` line carries `--repo` or a `repos/` path"

## Other findings

- L1 (MAJOR, open, single): Row 4 must call release_decision, which needs target_sha, applied_edits and cycle_id, but the stated resume_decision signature carries none of them and the row 4 result is never defined.
- L2 (MAJOR, open, single): The Wave 0 bullet must carry no L3 or draft condition yet must name L3 and a draft call, so a substring-style test of the stated ban rejects the required text.
- L3 (MAJOR, open, single): A start-text constant cannot prove byte identity, so an edit inside a pinned sentence still passes.
- L4 (MINOR, open, single): A grep for merge-guard does not match a heading named Merge guard unless the heading also carries the flag text.
- L5 (MAJOR, open, single): Task 8 never says the resume rows run again after a RECONCILE settles, so a held PR can stay draft after its push landed.
- L6 (MINOR, open, single): The rule that a draft_guard_unavailable halt reports unavailable is not carried, and guard_status returns released when no guard record exists.

## Reviser brief

Blocking finding ids: L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
