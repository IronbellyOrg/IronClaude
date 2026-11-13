review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The resume_decision signature has no target_sha, applied_edits or cycle_id, so row 4 cannot compute release_decision's head proof and its return value is unspecified.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"
- anchor2: "each re-enter `release_decision` with `push_completed=True`"

#### L1.R1 (F2)

- claim: After one failed engage every later engage returns HOLD(ownership_unproven), and the plan never says what the SKILL does on an engage HOLD, so a resumed run may edit and push with the PR mergeable.
- anchor: "`settled(draft, failed)` gives `RELEASE_PENDING`, increments `failed_mutations` and leaves `owned_draft` unchanged"
- anchor2: "all 11 rows, first match wins, `notes` carries `auto_merge_armed`"

#### L1.R1 (F6)

- claim: Below ordinal 3 a pending request is only reported and never reconciled, although source section 3 says resume reconciles unsettled requests at any ordinal.
- anchor: "ordinal 2 with phase `ENGAGE_PENDING` and a non-empty `pending` returns `REPORT_HELD` (row 2 wins over row 3)"

#### L1.R2 (F1)

- claim: The specified resume inputs provide no recorded push target, so the required release path cannot verify that the live PR head equals that target.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"
- anchor2: "re-enter release_decision with push_completed=True"

## Other findings

- L2 (MAJOR, open, single): The Wave 0 bullet must carry no L3 condition yet must print the off line only at L3 with the flag off, so a literal reading prints the unprotected line at every ordinal.
- L3 (MAJOR, open, single): One mint place at the end of Wave 3 cannot also mint ci ids for Wave 8, and a CI failure has no Medium-or-higher finding for the stated engage trigger.
- L4 (MAJOR, open, single): Release uses one head read with no wait, so a lagging PR head after a good push holds the PR as draft and the re-trigger may run on a draft PR with no stated handling.
- L5 (MINOR, open, single): A literal every-gh-line scan fails on the required gh repo view origin fallback line that the existing resolution tests demand.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
