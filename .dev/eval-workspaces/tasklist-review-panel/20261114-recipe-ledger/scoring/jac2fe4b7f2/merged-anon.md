review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R3: report <path>, block ok true
- R2: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R3, R2, R1 |
| L2 | open | yes | single | CRITICAL | - | R3 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Edit-scope constraint forbids the ./artifacts write Task 12 requires; one acceptance outcome must fail.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t2b-1 (F4)

- claim: Task 12 lists four reversible defaults where the source names three (Q4/Q5/Q6); Q7 is fixed.
- anchor: "and the four defaults the owner may reverse (the `orgs/` read exception, keeping the `--type` flag, keeping the mode labels, area `tests` giving Test)."

#### L1.t3-1 (F1)

- claim: An implementer who follows the stated text as written runs `make sync-dev`, and that is wrong because the command writes generated files under `.claude/`, which the plan forbids editing.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.t3-1 (F4)

- claim: The manual-check artifact omits the source's notes on organization-member visibility and the API-version-related 404 case.
- anchor: "It also records the three UNVERIFIED points from the source section 3.4 (POST body, `--type` flag, silent drop without push access)"

#### L1.t4-1 (F1)

- claim: Task 12 requires writing the owner check and saving test output under ./artifacts/, outside the plan's permitted edit locations.
- anchor: "- Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t4-1 (F2)

- claim: The required mode label is a third issue modification, contradicting the statement that only two things are written besides creating the issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

### L2

#### L2.t2b-1 (F2)

- claim: Task 10 acceptance forbids the legitimate gh api user path that Task 2 and the spec allow, so it cannot pass as written.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

## Other findings

- L3 (MAJOR, open, single): Plan never names the .dev/issues/<N>/complexity-field.json path or the post-rename write step the spec requires.
- L4 (MAJOR, open, single): The acceptance criterion permits the shorter `orgs/<owner>/issue-fields` form, so its test need not enforce the exact `orgs/<owner of R>/issue-fields` exception.
- L5 (MAJOR, open, single): The plan requires recording the area in `flags.md` but omits the source requirement to record it in the pushback comment.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
