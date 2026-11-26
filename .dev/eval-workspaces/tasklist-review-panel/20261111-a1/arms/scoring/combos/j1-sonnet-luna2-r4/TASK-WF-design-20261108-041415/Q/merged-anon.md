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
| L2 | open | no | single | MAJOR | 2.1 | R1 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | no | single | MINOR | 3.1 | R1 |
| L5 | open | no | single | MAJOR | - | R3 |
| L6 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The design doc keeps the claim lookup `gh api user -q .login`, so a check that every gh api path is repos/<R>/... except one orgs read cannot pass without editing claim text the constraints freeze.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged"

#### L1.R1 (F3)

- claim: The constraint says two writes besides the issue, but Task 2 also applies a mode label and posts a pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F4)

- claim: Task 12 writes files outside the four trees the constraint allows editing.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R1 (F5)

- claim: Task 12 expects four reversible defaults while the constraints and source list three.
- anchor: "the four defaults the owner may reverse"
- anchor2: "Decisions taken as defaults (the owner may reverse them later)"

#### L1.R3 (F1)

- claim: Task 12 requires an artifact outside the allowed edit paths, so an implementer cannot satisfy both stated requirements.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: Task 12 requires artifact files outside the only permitted edit paths, so its acceptance criteria cannot pass while obeying the constraint.
- anchor: "Constraints\n\n- Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F2)

- claim: The required sync edits generated files under `.claude/`, contradicting the explicit prohibition on editing that directory.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

## Other findings

- L2 (MAJOR, open, single): The plan never says how to match the single-select value in the read-back (option name versus numeric value), so a naive comparison reports a false 'not applied after create'.
- L3 (MINOR, open, single): Task 3 changes only the skill's Will Not list, so Task 6's Will-list agreement criterion has nothing to compare against.
- L4 (MINOR, open, single): The line range differs from source.md (99 to 103); harmless because the plan says to re-read live lines.
- L5 (MAJOR, open, single): The plan omits the response-field comparison needed to verify a single-select field value, so an implementer may compare the numeric value instead of the option name and falsely report the field as unset.
- L6 (MAJOR, open, single): The plan does not specify how to verify the selected option from the field read-back, which can lead an implementation to compare the option name against a returned option ID.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
