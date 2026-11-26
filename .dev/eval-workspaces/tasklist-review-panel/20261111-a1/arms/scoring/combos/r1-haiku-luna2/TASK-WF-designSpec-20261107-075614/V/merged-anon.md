review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R2 |
| L2 | open | yes | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MAJOR | - | R2 |
| L6 | open | no | single | MINOR | - | R2 |
| L7 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The Wave 0 bullet must print its off-line at L3 yet its acceptance test fails on any L3 mention, so the bullet cannot pass its own test.
- anchor: "carries no L3 or `draft` condition"
- anchor2: "at L3 with `--merge-guard off` the line"

### L2

#### L2.R2 (F2)

- claim: The release gate must run before default-on or merge, yet Task 6 sets default draft and no task waits on the gate.
- anchor: "before the feature is merged or turned on by default"
- anchor2: "DEFAULT_MERGE_GUARD = \"draft\""

## Other findings

- L3 (MAJOR, open, single): The goal says draft as soon as routing while the engage rule says end of Wave 3, so the timing is unclear.
- L4 (MAJOR, open, single): The CI-fix engage trigger has no severity, so an implementer must guess whether a CI-fix cycle engages.
- L5 (MAJOR, open, single): HEAD already has the guard module, the enum member and the SKILL and command text, so following Create or add literally overwrites or duplicates code and a duplicate enum member fails at import.
- L6 (MINOR, open, single): No task states the serialized string for each Phase value, so the held assertion depends on an unstated mapping.
- L7 (MAJOR, open, single): It is unstated whether a failed timeline read sets ok false with exit 1 or leaves ok true with exit 0.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
