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
| L1 | open | no | single | MAJOR | - | R3 |
| L2 | open | yes | overlap | MAJOR | - | R3, R2, R1 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MAJOR | - | R3 |
| L5 | open | no | single | MINOR | - | R3 |
| L6 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L2

#### L2.t2b-1 (F2)

- claim: Generic <file> omits required .dev/issues/<N>/complexity-field.json path and post-rename timing.
- anchor: "the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>`"

#### L2.t2b-1 (F3)

- claim: Constraints count (type+field) omits mode label that Tasks 1-2 require; implementer must guess.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "the table of the only two labels the skill applies"

#### L2.t3-1 (F1)

- claim: The plan both forbids editing generated `.claude/` files and requires `make sync-dev`, so its required sync cannot be performed while obeying the constraint.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L2.t3-1 (F2)

- claim: The allowed edit locations exclude `./artifacts/`, so the required owner manual-check file cannot be created while obeying the constraint.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.t4-1 (F1)

- claim: An implementer who follows the stated text as written runs `make sync-dev`, which writes source copies into `.claude/`, and that is wrong because the constraint forbids editing anything there except `.claude/settings.json`.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L2.t4-1 (F2)

- claim: An implementer who follows the stated text as written writes the required owner-check artifact under `./artifacts/`, and that is wrong because the constraint permits edits only under the four listed directory roots.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L1 (MAJOR, open, single): Task 3 names keys but never defines their values; classification_missing semantics must be guessed.
- L3 (MAJOR, open, single): Task 6 omits never writes a field other than Complexity yet acceptance demands agreement with skill.
- L4 (MAJOR, open, single): Scope ambiguous: read as each file, agent must carry POST contradicting T3 GET-only rule.
- L5 (MINOR, open, single): Cited test line numbers are stale (live line 580); lookup by name is required.
- L6 (MAJOR, open, single): The plan does not carry forward the source rule that the owner in the organization lookup must never be typed from user input.

## Reviser brief

Blocking finding ids: L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
