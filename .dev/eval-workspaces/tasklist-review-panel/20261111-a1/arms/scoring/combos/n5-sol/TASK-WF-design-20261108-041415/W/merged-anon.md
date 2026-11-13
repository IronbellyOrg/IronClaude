review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok false
- R4: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R2, R3 |
| L2 | open | no | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The exactly-two-writes constraint contradicts the required mode label application and pushback comment in Wave 5, so one stated text must be violated.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "mode label only; `--type` when listed; `gh issue create` and the rename; type read-back; field POST and read-back; pushback comment"

#### L1.R2 (F2)

- claim: Task 10's acceptance criterion cannot pass while the documented gh api user claim lookup remains, which Task 2 and the unchanged claim rule require.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception, the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields`"

#### L1.R2 (F3)

- claim: Task 12 requires writing ./artifacts/ files that sit outside every edit root the Constraints allow.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F6)

- claim: Task 2's option-name wording and Task 4's fixed Simple/Medium/Complex values allow posting a casing the org field does not have.
- anchor: "the Complexity row holds the option name."
- anchor2: "change the Complexity row values to `<Simple | Medium | Complex>`"

#### L1.R3 (F2)

- claim: `./artifacts/` is ambiguous between the task package's artifacts directory (staged with `.dev/tasks/`) and the checkout-root `artifacts/` folder (never staged); `in this package` points at the right root but the tasks run from the repo root.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F3)

- claim: Named line anchors are stale by 1 to 40 lines against the live tree (e.g. HOW-WE-WORK 329 vs live 330, return-contract test 492-520 vs live 545-577); the plan's own re-read constraint covers the drift, so numbers must not be trusted as-is.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.R3 (F4)

- claim: The Goal reads as if all three classifications appear in the third return-contract block, but a missing mode label is reported in the first block (`labels_missing`); the third block collects only the `not set` lines.
- anchor: "lists every classification it could not set in its final output and in a third return-contract block"

## Other findings

- L2 (MAJOR, open, single): Acceptance depends on source sections 2.4, 3.2 and 3.4 that are not included in the candidate package, so the required reason lists cannot be enumerated from the plan alone.
- L3 (MAJOR, open, single): The content of classification_missing is never defined, so implementations that pass the key-only tests can emit different return-contract values.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
