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
| L1 | open | no | overlap | MAJOR | - | R1, R2 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L3

#### L3.R1 (F3)

- claim: The constraint says two writes besides the issue, but Wave 5 also posts a pushback comment and applies the mode label.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output"

#### L3.R1 (F4)

- claim: Task 12 writes files in the package artifacts folder, outside the four paths the constraint allows editing.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "write `./artifacts/owner-manual-check.md` in this package"

#### L3.R1 (F5)

- claim: Constraints list three reversible defaults while Task 12 asks the owner note for four, with the fourth stated only in Task 12.
- anchor: "the four defaults the owner may reverse"
- anchor2: "Decisions taken as defaults (the owner may reverse them later)"

#### L3.R3 (F1)

- claim: The required sync writes generated files under `.claude/`, which the plan simultaneously forbids editing.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`, never by editing `.claude/`."

#### L3.R3 (F2)

- claim: The required artifact is outside the plan’s permitted edit paths, so the artifact acceptance criterion cannot pass without violating the constraint.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L3.R2 (F1)

- claim: Task 12 requires writing deliverables under ./artifacts/, which the edit-only constraint forbids.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L3.R2 (F2)

- claim: Task 10 acceptance forbids the legitimate gh api user path that Task 2 allows and the design file uses.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

## Other findings

- L1 (MAJOR, open, overlap): Reverting Task 3 turns no new Task 8 test red when the orgs test is read as a subset check and the POST test reads the folder as one pile, so the revert criterion fails for SKILL.md.
- L2 (MAJOR, open, single): No rule says how to match the single-select value in the read-back, and GitHub's docs do not say whether the scalar value is the option name or id, so comparing value to the option name can print a false not set line after a successful write.
- L4 (MAJOR, open, single): Conditional CLAUDE.md copy plus a grep fallback can pass while the level table stays stale.
- L5 (MINOR, open, single): Scout template line range differs from the source citation; re-read rule makes this harmless.

## Reviser brief

Blocking finding ids: L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
