review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R1 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (f1)

- claim: The Task 10 criterion cannot pass on the live design document, which contains gh api user at line 157 and states the path rule without the user exception at line 330.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

### L2

#### L2.R1 (f2)

- claim: Task 12 writes to an artifacts path outside the edit scope the Constraints allow, without pinning where that path lives.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L2.R1 (f3)

- claim: The kept maintainer lines still read --repo <owner/repo>, which the Constraints rewrite as <owner> and <R>, and no check catches it.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block."
- anchor2: "No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`."

#### L2.R3 (f1)

- claim: The plan requires an artifact outside its permitted edit scope, so an implementer cannot satisfy both instructions as written.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.R2 (f1)

- claim: The plan does not define how to report <redacted> classification when its read-back command fails, leaving the promised final output and return-contract values unspecified for that failure.
- anchor: "read-back with `gh issue view <N> --repo <R> --json issueType --jq .issueType.name`; the POST with `gh api -X POST"

## Other findings

- L3 (MINOR, open, single): The new orgs test accepts two spellings while Tasks 2, 3 and 5 each require exactly one.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report <redacted> byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
