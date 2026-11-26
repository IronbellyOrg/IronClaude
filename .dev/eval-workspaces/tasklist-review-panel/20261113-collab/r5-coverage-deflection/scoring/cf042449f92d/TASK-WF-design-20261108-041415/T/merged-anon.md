review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted> block ok true
- R3: report <redacted> block ok true
- R1: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2 |
| L2 | open | yes | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MINOR | - | R2 |
| L6 | open | no | single | MINOR | - | R2 |
| L7 | open | no | single | MINOR | - | R2 |
| L8 | open | yes | single | MAJOR | - | R3 |
| L9 | open | yes | single | MAJOR | - | R3 |
| L10 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: Constraint line 23 allows only the issue type and Complexity writes, but Task 2 keeps the Wave 5 pushback comment, which is a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every"

#### L1.R2 (F4)

- claim: The '<owner of R>' spelling differs from the '<owner>' the constraint names, and a whitespace-stopping regex in test 2 captures orgs/<owner, which matches neither accepted form.
- anchor: "gh api orgs/<owner of R>/issue-fields"
- anchor2: "orgs/<owner>/issue-fields"

#### L1.R2 (F6)

- claim: ./artifacts is ambiguous between the package folder (staged) and the project-root artifacts folder (never staged), and it sits outside the four trees Constraint 19 allows.
- anchor: "in this package. It states, in plain bullets"
- anchor2: "Edit only under `src/superclaude/`"

#### L1.R1 (F1)

- claim: The plan requires an artifact outside its permitted edit locations, so an implementer cannot comply with both instructions.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-"
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

### L2

#### L2.R2 (F2)

- claim: Reverting Task 3 (SKILL.md) turns no new test red, because the new tests never assert SKILL.md error rows, POST lines or orgs exception.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "each new test asserts on the text that task adds"

### L8

#### L8.R3 (F1)

- claim: Task 10 would require removing or misrepresenting the existing claim-mode `gh api user` lookup in the design document, contrary to the plan's requirement that claim text stay unchanged.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

### L9

#### L9.R3 (F2)

- claim: The prescribed `--mode` wording says feature mode selects Feature, contradicting the rule that feature mode with area `tests` selects Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""

## Other findings

- L3 (MAJOR, open, single): No test compares issue.md with SKILL.md, so the agreement criterion has no check.
- L4 (MAJOR, open, single): A 404 for a user-owned repo is a failed read, so Task 5 records lookup failed where source 2.5 expects field not found in org; the 404 rule is not stated.
- L5 (MINOR, open, single): Line 329 is the /sc:graph row; the /sc:issue row with the phrase is at line 333.
- L6 (MINOR, open, single): Line numbers are stale: the Will test is at 580 (named as 527), the st10 test at 545-574, and the fork-safety test at 695 (named as 642).
- L7 (MINOR, open, single): Source 2.2 says labels_applied and labels_missing now describe the mode label only, and Task 3 omits that wording.
- L10 (MAJOR, open, single): When the field exists but its options do not include the requested value, the plan does not clearly require reporting `not set: field Complexity <value>: option not found`.

## Reviser brief

Blocking finding ids: L1, L2, L8, L9.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
