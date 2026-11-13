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
| L1 | open | no | overlap | MAJOR | - | R2, R3 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | overlap | MAJOR | - | R1, R2, R3 |
| L4 | open | no | overlap | MINOR | - | R2, R3 |
| L5 | open | no | single | MAJOR | - | R3 |
| L6 | open | no | single | MAJOR | - | R3 |
| L7 | open | no | overlap | MINOR | - | R1, R3 |
| L8 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L2

#### L2.R2 (F2)

- claim: Task 9 requires the Wave 0 bullet to carry no L3 condition while also requiring it to state an L3-gated off notice, so an implementer who tests for any L3 mention makes the required bullet fail its own test.
- anchor: "that applies at every ordinal and in both modes and carries no L3 or `draft` condition"
- anchor2: "and that at L3 with `--merge-guard off` the line \"Remediation is unprotected: --merge-guard off.\" is printed once and no draft call is made"

#### L2.R3 (F1)

- claim: The Wave 0 bullet must name the L3 off condition, but its acceptance test fails any bullet that names an L3 or draft condition, so the required text cannot pass.
- anchor: "and carries no L3 or `draft` condition;"
- anchor2: "and that at L3 with `--merge-guard off` the line"

#### L2.R3 (F9)

- claim: The output row carries the L2 line but does not say when it prints.
- anchor: "that also carries the literal L2 line"

#### L2.R1 (F2)

- claim: The Wave 0 bullet must name L3 for the off line, yet the criterion says the test fails when the bullet names an L3 condition, so the broader reading rejects the mandated sentence.
- anchor: "at L3 with `--merge-guard off` the line"
- anchor2: "when it names an L3 or `draft` condition"

## Other findings

- L1 (MAJOR, open, overlap): Task 11 (and Task 5) consume the Task 2 event enum through RunLog.append but declare no dependency on Task 2, so a dependency-ordered executor can run them before the new event types exist.
- L3 (MAJOR, open, overlap): The Resume protocol never states where the re-entered release decision gets target_sha and this cycle's applied_edits, so an implementer can release through the no_edits row without comparing the PR head to the held cycle's pushed SHA.
- L4 (MINOR, open, overlap): The guard_status acceptance enumeration never names the direct HELD to held or RELEASED to released cases despite claiming every phase is covered.
- L5 (MAJOR, open, single): The plan's base has no guard code, but HEAD already has the module, the 45-member enum and the flag, so the create step would overwrite a tracked module and the 43-R4 edit finds nothing to change.
- L6 (MAJOR, open, single): The note has no required action, so an armed auto-merge is silently disarmed by the draft conversion and not restored or reported.
- L7 (MINOR, open, overlap): git status never lists gitignored mirrors, so the acceptance wording promises a listing it cannot show.
- L8 (MAJOR, open, single): A section titled "Merge guard" does not match grep for "merge-guard", so the criterion that grep shows the section heading fails unless the heading also carries the hyphenated flag.

## Reviser brief

Blocking finding ids: L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
