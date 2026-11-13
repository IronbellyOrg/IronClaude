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
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3 |
| L2 | open | no | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The Task 10 criterion forbids the existing `gh api user` line, which the skill's own path rule allows, so the criterion cannot pass without deleting a correct claim-mode line.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.R1 (F3)

- claim: None of the six listed new tests asserts on SKILL.md text, so reverting Task 3 leaves every new test green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."

#### L1.R1 (F4)

- claim: A simple regex would flag the bare prose `orgs/` that Tasks 2 and 3 require, and the plan does not say to ignore it.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files"
- anchor2: "that no other `orgs/` path is allowed"

#### L1.R1 (F5)

- claim: The constraint says two writes, but Wave 5 also posts the pushback comment and sets the mode label.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F6)

- claim: Task 12 writes files outside the folders the constraint allows, and the artifacts path is ambiguous.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F1)

- claim: The plan both prohibits edits under `.claude/` and requires a sync target that copies files into `.claude/`.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`, never by editing `.claude/`."

#### L1.R2 (F1)

- claim: The scope forbids the package artifacts that Task 12 and its acceptance criteria require.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, overlap): No rule says how to compare the read-back value with the option name, so a naive comparison can print a false 'not applied after create' line.
- L3 (MINOR, open, single): The note that labels_applied and labels_missing now describe the mode label only is not carried into SKILL.md.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
