review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R3: report <redacted> block ok true
- R2: report <redacted> block ok true
- R1: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R2, R3 |
| L2 | open | no | overlap | MAJOR | - | R1, R2 |
| L3 | open | yes | single | MAJOR | - | R1 |
| L4 | open | no | single | MAJOR | 3.2 | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L3

#### L3.R1 (F1)

- claim: Task 10 acceptance forbids gh api user while Task 2 and the live design doc allow and use it, so the criterion cannot pass without breaking the claim lookup.
- anchor: "- Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

## Other findings

- L1 (MAJOR, open, overlap): Task 3 does not specify the third block's value semantics, so an implementer could add the required keys without returning read-back values or listing every unset classification.
- L2 (MAJOR, open, overlap): The plan does not identify the package directory or show that its artifacts subdirectory is within the allowed edit scope, leaving implementers unable to establish whether the required output violates the scope constraint.
- L4 (MAJOR, open, single): Self-check test runs on synthetic text only and never fails when real behavior breaks, contrary to source 3.2 fail-if-breaks rule.
- L5 (MINOR, open, single): Stated live line is 329 but the phrase is on line 333 in both copies; phrase search rescues it.
- L6 (MINOR, open, single): Design-doc line 272 footer wording also becomes false after section 11 changes but is not listed.
- L7 (MAJOR, open, single): Named Will/Will Not test reads only SKILL.md and cannot fail on command-file disagreement, so agree has no finite check.

## Reviser brief

Blocking finding ids: L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
