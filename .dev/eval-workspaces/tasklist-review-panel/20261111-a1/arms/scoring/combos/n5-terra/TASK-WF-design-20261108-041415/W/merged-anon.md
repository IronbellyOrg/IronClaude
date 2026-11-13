review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R2, R3 |
| L2 | open | no | overlap | MAJOR | - | R2, R3 |
| L3 | open | no | single | MAJOR | - | R3 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: Task 10 acceptance forbids the gh api user path that Task 2 allows and unchanged claim text requires, so the acceptance criterion cannot pass as written.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception, the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields`"

#### L1.R3 (F1)

- claim: Task 10's criterion omits the `user` path its own edit list preserves, so it fails as written against the doc the task produces and a letter-reading implementer would delete the correct `gh api user -q .login` sentence.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

## Other findings

- L2 (MAJOR, open, overlap): Task 12 writes under ./artifacts/ which the edit-only constraint does not list, so compliance depends on reading write as different from edit.
- L3 (MAJOR, open, single): The plan cites ./source.md as the only holder of the exact output-line reason enumeration, and that file is absent from the package, so an implementer working from the package must guess the canonical reason list.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
