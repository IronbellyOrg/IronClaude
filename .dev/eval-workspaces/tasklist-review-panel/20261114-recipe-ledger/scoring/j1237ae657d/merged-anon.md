review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <path>, block ok true
- R3: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | yes | overlap | CRITICAL | - | R1, R3, R2 |
| L4 | open | no | overlap | MAJOR | - | R1, R2 |
| L5 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L3

#### L3.t2b-1 (F4)

- claim: Package versus repo-root location is unstated, so an implementer can place the file where the git status check fails.
- anchor: "to `./artifacts/final-checks.md`"

#### L3.t3-1 (F1)

- claim: The src-only restriction contradicts required test and documentation edits outside src, so following it prevents the plan's acceptance criteria from passing.
- anchor: "Edit canonical files under `src/superclaude/` only"
- anchor2: "Update `tests/pr_submit/test_run_log.py`"

#### L3.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a change limited to src/superclaude, and that change is wrong because the plan also requires edits to tests and user guides, which the source-only constraint forbids.
- anchor: "Edit canonical files under `src/superclaude/` only"
- anchor2: "Edit `docs/user-guide/commands.md`: add"

## Other findings

- L1 (MAJOR, open, single): The required halt naming --merge-guard off is omitted, so an implementer omits that part of the message.
- L2 (MAJOR, open, single): Which request cycle_id the fold keeps across multiple cycles is unspecified, so held_cycle_published can check the wrong cycle.
- L4 (MAJOR, open, overlap): Which wave list the line goes in is unstated, leaving placement to the implementer.
- L5 (MAJOR, open, single): The scenario tests do not explicitly cover crashes before and after each guard request and settle, as required by the source test design.

## Reviser brief

Blocking finding ids: L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
