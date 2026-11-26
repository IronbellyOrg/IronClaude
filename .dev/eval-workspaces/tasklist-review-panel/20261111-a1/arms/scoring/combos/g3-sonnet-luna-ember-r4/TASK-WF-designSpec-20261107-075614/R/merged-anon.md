review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok false

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | overlap | MINOR | - | R1, R2 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L2

#### L2.R1 (F2)

- claim: The plan never says whether the folded guard is a dict or a dataclass; Task 5 needs subscript access while Tasks 3 and 4 use attribute access.
- anchor: "returns `state[\"draft_guard\"][\"phase\"] == \"held\"` with `owned_draft` true"
- anchor2: "`classify_toggles(guard, read)` (the exact rule of ./source.md section 4.1"

#### L2.R1 (F5)

- claim: Zero-edit release is checked before publication, so a resumed run with an unpublished earlier fix can make the PR ready while that fix is local only.
- anchor: "while the guard record already holds an earlier fixing cycle returns `RELEASE` with cause `no_edits`"

#### L2.R3 (F1)

- claim: Resume cannot pass the expected target SHA to the release check, so it cannot prove the published fix is on the PR head before marking the PR ready.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"
- anchor2: "each re-enter release_decision with push_completed=True"

#### L2.R2 (F1)

- claim: Task 4 lists 7 resume parameters but never states where the row-4 release_decision re-entry gets target_sha, applied_edits or cycle_id, so the head proof on the landed/published branch has no stated source.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"
- anchor2: "phase `HELD` with `dangling_branch == \"landed\"` and phase `HELD` with `dangling_branch is None` and `published=True` each re-enter `release_decision` with `push_completed=True`"

## Other findings

- L1 (MAJOR, open, single): The engage-failure halt message that names --merge-guard off and prints the clear command is dropped from Task 8, so a G1 plan-support failure halts with no escape hatch.
- L3 (MINOR, open, overlap): The required bullet text mentions L3 and draft while the test is said to fail on any L3 or draft condition; the test must target load gating phrases only.
- L4 (MAJOR, open, single): The ci-<n> id has no stated mint site after Wave 3, so the guard and the push triad can use different ids and the PR stays draft after a good CI push.
- L5 (MINOR, open, single): No task owns the conversion of the --read JSON into GuardRead (object-or-null to bool, field renames).
- L6 (MINOR, open, single): A real cycle also writes push_decision and push_initiated, so the order check must be a subsequence check, not full-list equality.
- L7 (MAJOR, open, single): Task 13 does not say 'in this package' and its git-status allowlist omits artifacts/, so a repository-root reading of ./artifacts/final-checks.md violates its own acceptance criterion.

## Reviser brief

Blocking finding ids: L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
