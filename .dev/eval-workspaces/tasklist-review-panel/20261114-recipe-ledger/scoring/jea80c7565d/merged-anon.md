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
| L1 | open | yes | single | MAJOR | - | R3 |
| L2 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t3-1 (F1)

- claim: The source-only edit constraint contradicts required edits to tests and user-guide files outside `src/superclaude/`.
- anchor: "Edit canonical files under `src/superclaude/` only"
- anchor2: "Edit `docs/user-guide/commands.md`"

## Other findings

- L2 (MAJOR, open, single): The source requires `make sync-dev` followed by `make verify-sync` after edits under `src/superclaude/`; the plan narrows its per-task sync rule to skills and commands and does not require per-task verification.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
