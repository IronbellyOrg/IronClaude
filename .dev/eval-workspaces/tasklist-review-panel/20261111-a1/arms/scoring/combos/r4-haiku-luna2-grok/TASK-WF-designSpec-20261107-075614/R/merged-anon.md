review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R4: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R1, R4 |
| L2 | open | no | overlap | MAJOR | - | R1, R4 |
| L3 | open | no | overlap | MAJOR | - | R1, R4 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MAJOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | no | single | MAJOR | - | R4 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, overlap): An implementer who follows Task 9's Wave 0 bullet and Task 8's Resume section builds a Wave 0 hook that runs Resume rows at ordinals 0 to 2, and X is wrong because Constraint 25 limits those ordinals to one report line; the release path at those ordinals is not stated.
- L2 (MAJOR, open, overlap): An implementer who follows Task 11 builds a trace that asserts no call at ordinals 0 to 2, and X is wrong if the resume read at those ordinals is needed, which the candidate does not state.
- L3 (MAJOR, open, overlap): An implementer who follows Task 3 may build fold_draft_guard as a dataclass, and X is wrong because Task 5's acceptance reads it by subscript; the return type is not stated.
- L4 (MAJOR, open, single): If the base already fails a test under tests/pr_submit, Task 11 cannot pass while Task 13 accepts that failure, and the candidate does not state the base result.
- L5 (MAJOR, open, single): An implementer who compares only the start text builds a pin that passes after the rest of the S5a or Wave 6 sentence changes, and X is wrong because the criterion says byte-identical.
- L6 (MINOR, open, single): The grep for 43 matches any substring containing 43, so the criterion depends on judgment rather than a mechanical result.
- L7 (MAJOR, open, single): Pinning --repo on the gh repo view fallback satisfies both checks while defeating the unscoped discovery call those resolution tests exist to lock.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
