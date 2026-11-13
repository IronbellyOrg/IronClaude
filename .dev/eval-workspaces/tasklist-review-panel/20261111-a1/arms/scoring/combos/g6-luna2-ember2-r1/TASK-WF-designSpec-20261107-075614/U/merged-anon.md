review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R3: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R2, R3 |
| L2 | open | yes | overlap | MAJOR | - | R1, R4 |
| L3 | open | no | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | no | single | MAJOR | - | R2 |
| L6 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L2

#### L2.R4 (F1)

- claim: The plan both restricts edits to `src/superclaude/` and requires edits or new files under tests, docs, and the task package, so it cannot be followed as written.
- anchor: "Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files."
- anchor2: "Create `./artifacts/pre-build-gate.md` in this package from ./source.md sections 6, 8 and 10."

#### L2.R4 (F2)

- claim: The plan does not require verifying a clean base commit before recording baseline results, so pre-existing checkout changes could be recorded as the base-commit state.
- anchor: "First record the base-commit state: run `make lint`, `uv run ruff format --check src/ tests/` and the full suite `uv run pytest -q tests` before any code edit"

#### L2.R1 (F2)

- claim: Task-level classification instructions cover only gh hits, missing the git write-verb pattern of the stated constraint
- anchor: "add one `WRITE_VERB_CLASSIFICATION` entry in `tests/skills/test_worker_contract.py` for every line of the script that matches `gh pr` or `gh api`"
- anchor2: "Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry"

## Other findings

- L1 (MAJOR, open, overlap): A release retry can mark the PR ready despite an unreadable timeline, contrary to the stated hold-on-unreadable policy.
- L3 (MAJOR, open, overlap): Wave 0 bullet wording test and the required L3 off-line conflict unless the plan settles which the test checks
- L4 (MINOR, open, single): Neither length is named, so the test target must be guessed
- L5 (MAJOR, open, single): Resume row 4 has no stated return value, so the implementer must invent the re-entry signal.
- L6 (MINOR, open, single): A bare grep for 43 fails on any unrelated number, not just the enum-member claim.

## Reviser brief

Blocking finding ids: L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
