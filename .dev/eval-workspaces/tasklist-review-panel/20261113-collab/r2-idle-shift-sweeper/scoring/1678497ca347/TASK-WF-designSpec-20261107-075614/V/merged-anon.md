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
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | yes | overlap | MAJOR | - | R1, R2 |
| L4 | open | yes | single | CRITICAL | - | R3 |

## Blocking findings

### L3

#### L3.R1 (F4)

- claim: Task 9 asks the Wave 0 bullet to be unconditional yet carry the L3 off line, leaving the exact permitted wording unclear.
- anchor: "carries no L3 or `draft` condition; it states that on `--resume`, or when the run log already holds guard events"

#### L3.R2 (F1)

- claim: The Wave 0 acceptance test is required to reject an L3 condition that the task requires the bullet to describe.
- anchor: "when it names an L3 or `draft` condition"
- anchor2: "at L3 with `--merge-guard off` the line \"Remediation is unprotected: --merge-guard off.\" is printed once"

### L4

#### L4.R3 (F1)

- claim: Limiting edits to `src/superclaude/` contradicts required edits to tests and user guides, making the plan’s acceptance criteria impossible to satisfy as written.
- anchor: "Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files."
- anchor2: "Edit `docs/user-guide/commands.md`: add `[--merge-guard {draft,off}]` to the `/sc:pr-submit` usage line and a paragraph after the \"Merge conflicts\" paragraph"

## Other findings

- L1 (MAJOR, open, single): Task 7 leaves the importable form of the fake gh open while Task 11 depends on one specific form.
- L2 (MAJOR, open, single): Comparing against only the literal start text cannot prove the pinned sentences are byte-identical.

## Reviser brief

Blocking finding ids: L3, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report <redacted> byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
