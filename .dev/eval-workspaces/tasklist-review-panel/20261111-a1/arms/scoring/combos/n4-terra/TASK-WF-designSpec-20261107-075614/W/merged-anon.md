review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R2, R4 |
| L2 | open | no | single | MAJOR | - | R2 |
| L3 | open | no | overlap | MINOR | - | R2, R4 |
| L4 | open | no | overlap | MAJOR | - | R2, R3, R4 |
| L5 | open | no | single | MINOR | - | R3 |
| L6 | open | no | single | MAJOR | - | R4 |
| L7 | open | no | single | MAJOR | - | R4 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: A literal L3-substring test mandated by the acceptance criterion would fail the very bullet the same task requires, though the narrower gate-wording reading in the same task avoids it.
- anchor: "when it names an L3 or `draft` condition, or when the literal `off` line is missing"
- anchor2: "and that at L3 with `--merge-guard off` the line"

#### L1.R4 (F1)

- claim: The Wave 0 bullet must name L3 and a draft call, but its acceptance fails any bullet naming an L3 or draft condition, so the real file cannot pass.
- anchor: "carries no L3 or `draft` condition"
- anchor2: "and that at L3 with `--merge-guard off` the line"

## Other findings

- L2 (MAJOR, open, single): A test built only from the recorded start text cannot detect a changed sentence tail, so the byte-identical acceptance claim can pass on altered text.
- L3 (MINOR, open, overlap): Task 13 requires .dev/tasks to be staged at acceptance but no step in its command list stages it.
- L4 (MAJOR, open, overlap): The Tasks 8 and 12 classification steps omit the git-write-verb case the governing constraint requires, so such a line would be written unclassified.
- L5 (MINOR, open, single): The artifact location is fixed only by the phrase "in this package"; reading ./artifacts/ as repo-root would create an unstaged path that Task 13's git-status acceptance criterion then rejects.
- L6 (MAJOR, open, single): The plan assumes a pre-feature base, but the module, events, script and guard bullets are already tracked at HEAD, so Create overwrites and Add duplicates.
- L7 (MAJOR, open, single): The plan does not say whether a failing timeline read sets ok false or exit 1, and the engage halt depends on it.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
