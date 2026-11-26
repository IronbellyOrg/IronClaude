review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | 2.3 | R2 |
| L2 | open | no | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | 2.1 | R2 |
| L4 | open | no | single | MAJOR | 2.2 | R2 |
| L5 | open | yes | overlap | MAJOR | - | R2, R1 |
| L6 | open | yes | overlap | CRITICAL | - | R2, R1 |
| L7 | open | no | single | MINOR | - | R2 |
| L8 | open | no | single | MAJOR | 2.3 | R3 |
| L9 | open | no | single | MAJOR | - | R3 |
| L10 | open | no | single | MAJOR | 3.4 | R3 |
| L11 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L5

#### L5.t2b-1 (F5)

- claim: Task 12 writes outside the four-tree edit scope the Constraints enumerate.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L5.t4-1 (F2)

- claim: Task 12 requires writing artifacts outside the plan's expressly permitted edit areas, so following both instructions is impossible.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L5.t4-1 (F5)

- claim: The plan omits the documented endpoint-version caveat and the expected safe handling when an older CLI API default causes a 404.
- anchor: "the three UNVERIFIED points from the source section 3.4 (POST body, `--type` flag, silent drop without push access)"

### L6

#### L6.t2b-1 (F6)

- claim: Exactly-two-writes sentence omits the mode label applied via --label at create time.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."

#### L6.t4-1 (F1)

- claim: The plan requires posting a pushback comment as well as the issue type and Complexity field, contradicting its limit of exactly two additional writes.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment"

#### L6.t4-1 (F4)

- claim: The plan omits the source restriction that the organization owner must never be supplied from user input.
- anchor: "`<owner>` is the part of `<R>` before the slash; no other `orgs/` path"

## Other findings

- L1 (MAJOR, open, single): Reverting Task 3 turns no described new test red, so the revert-acceptance cannot be shown to hold.
- L2 (MAJOR, open, single): Acceptance checks gh issue lines only, so kept gh label lines can pass while violating the --repo <R> constraint.
- L3 (MAJOR, open, single): POST body file path is never stated, so --input can point at the pre-rename path and fail on the happy path.
- L4 (MAJOR, open, single): Third block value semantics from 2.2 are never carried; wrong values pass every criterion.
- L7 (MINOR, open, single): Stale line pointers: test defs live at lines 545/580/695, not 492-527/642.
- L8 (MAJOR, open, single): The plan does not preserve the source restriction that the organization owner used for the lookup is never typed from user input.
- L9 (MAJOR, open, single): The plan omits the source requirement to record the area in the pushback comment as well as in flags.md.
- L10 (MAJOR, open, single): The plan does not specify that callers outside the organization receive a `not set` line for the inaccessible Complexity field.
- L11 (MAJOR, open, single): The plan omits the stated case where an outside organization caller cannot see the field and must receive a non-fatal `not set` result.

## Reviser brief

Blocking finding ids: L5, L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
