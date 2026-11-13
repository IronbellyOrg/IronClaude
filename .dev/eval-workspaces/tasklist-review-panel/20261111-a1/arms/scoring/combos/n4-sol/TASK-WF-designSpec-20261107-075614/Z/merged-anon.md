review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R2, R3, R4 |
| L2 | open | no | overlap | MAJOR | - | R2, R4 |
| L3 | open | no | overlap | MAJOR | - | R2, R4 |
| L4 | open | no | overlap | MAJOR | - | R2, R4 |
| L5 | open | no | single | MAJOR | - | R3 |
| L6 | open | no | overlap | MINOR | - | R3, R4 |
| L7 | open | no | single | MINOR | FR-6 | R3 |
| L8 | open | yes | overlap | MAJOR | - | R3, R4 |
| L9 | open | yes | single | MAJOR | - | R4 |
| L10 | open | no | single | MAJOR | - | R4 |

## Blocking findings

### L8

#### L8.R3 (F5)

- claim: A failed pre-push read is labelled pr_not_open like a genuinely non-OPEN PR instead of draft_guard_unavailable; inherited from the design and fail-closed either way, so only the operator-facing reason can mislead.
- anchor: "the script `--read` must show `OPEN` at the pre-push head guard step before `push_decision`, otherwise halt `pr_not_open`"

#### L8.R4 (F2)

- claim: The Engage trigger excludes CI-fix cycles because a failing CI check has no severity, while the Wave 8 bullet says they always engage, so a CI fix push can land on a ready PR.
- anchor: "only when at least one verified finding of Medium severity or higher is routed to a fix, once per cycle id; review-fix cycles and CI-fix cycles"
- anchor2: "a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll"

### L9

#### L9.R4 (F1)

- claim: A zero-edit cycle releases the PR to ready even when an earlier fixing cycle's push never completed, which the owner decision says must keep the PR draft.
- anchor: "`release_decision` called with `applied_edits=0` for a new cycle while the guard record already holds an earlier fixing cycle returns `RELEASE` with cause `no_edits`"
- anchor2: "unreadable timeline or unpublished exit keeps the PR draft"

## Other findings

- L1 (MAJOR, open, overlap): The Wave 0 acceptance wording can be read as rejecting any L3 mention although the required bullet must contain the at-L3 off sentence, so a literal test could fail the required text.
- L2 (MAJOR, open, overlap): Resume row 4 must re-enter release_decision but the stated resume inputs include neither target_sha nor this cycle's applied_edits, leaving the head-equality release proof unspecified.
- L3 (MAJOR, open, overlap): No stated rule rebinds a held guard to a later cycle, so publication can be judged by the earlier cycle's cycle_id after a second cycle engages while held.
- L4 (MAJOR, open, overlap): Comparing only the recorded start text cannot prove the S5a and Wave 6 pre-push sentences stayed byte-identical, so the Task 10 check is weaker than claimed.
- L5 (MAJOR, open, single): The plan drops the design's requirement that the engage-failure halt message names `--merge-guard off` and prints the clear command; Tasks 8 and 11 specify only the halt reason and its before-any-edit timing.
- L6 (MINOR, open, overlap): The parenthetical misstates why: double collection comes from importing a test_* name into the importing module, not from importing a helper from a test module; the instruction itself is safe.
- L7 (MINOR, open, single): The assertion is weaker than the design's 'never mutate' for an already-draft PR, which should produce no draft-state call at all; the scenario body states the intent, so only the literal AC is looser.
- L10 (MAJOR, open, single): No text says how the parsed merge_guard value reaches the mode argument of the decision functions, so the flag may be parsed and never used.

## Reviser brief

Blocking finding ids: L8, L9.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
