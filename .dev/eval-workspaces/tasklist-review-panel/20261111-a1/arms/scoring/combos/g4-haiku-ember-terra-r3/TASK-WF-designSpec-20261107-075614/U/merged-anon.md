review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R3 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L5 | open | no | single | MAJOR | - | R3 |
| L6 | open | no | single | MINOR | - | R3 |
| L7 | open | no | single | MINOR | - | R3 |
| L8 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: The reference's Engage section puts CI-fix engagement at the end of Wave 3, while the Wave 8 bullet engages it in Wave 8, so a CI-fix push can go out on a ready PR.
- anchor: "Engage at the end of Wave 3 (L3, only when at least one verified finding of Medium severity or higher is routed to a fix, once per cycle id; review-fix cycles and CI-fix cycles;"
- anchor2: "the Wave 8 bullet states that a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll."

#### L1.R3 (F7)

- claim: The script never emits the phrase already in target state; it returns changed false, so the phrase cannot be tested.
- anchor: "`already in target state` counts as confirmed"

### L4

#### L4.R3 (F4)

- claim: The Wave 0 bullet must state an L3-only off line, but the acceptance test fails on any named L3 condition, and the two texts give different trigger words.
- anchor: "that applies at every ordinal and in both modes and carries no L3 or `draft` condition"
- anchor2: "when it names an L3 or `draft` condition, or when"

#### L4.R2 (F1)

- claim: Wave 0 bullet must also carry an L3 off clause and a draft call prohibition, so no L3 or draft wording is ambiguous as a test guard.
- anchor: "one new bullet under Wave 0, written as a flat line before the Wave 1 bullet, that applies at every ordinal and in both modes and carries no L3 or `draft` condition"

#### L4.R1 (F1)

- claim: The required Wave 0 bullet must contain an L3 condition, but its acceptance test must reject a bullet that names one.
- anchor: "at L3 with `--merge-guard off` the line"
- anchor2: "when it names an L3 or `draft` condition"

## Other findings

- L2 (MAJOR, open, single): The plan never says observed transitions are counted from the baseline, so a PR with earlier human toggles reads as foreign at release.
- L3 (MAJOR, open, single): The acceptance wording makes mode OFF at ordinal 3 with no record report released, while section 4.1 reports off for any mode OFF.
- L5 (MAJOR, open, single): No task says what reads the parsed merge_guard value at run time, so an off setting may never reach the protocol.
- L6 (MINOR, open, single): The Goal says engage as soon as routing happens, while the constraint says engage at the end of Wave 3.
- L7 (MINOR, open, single): This checkout already holds the build and a 45-member test under another name, so the stated base state and the rename instruction do not match it.
- L8 (MINOR, open, single): Scenario imports lack a named helper or fixture symbol, so implementer must choose the symbol name.

## Reviser brief

Blocking finding ids: L1, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
