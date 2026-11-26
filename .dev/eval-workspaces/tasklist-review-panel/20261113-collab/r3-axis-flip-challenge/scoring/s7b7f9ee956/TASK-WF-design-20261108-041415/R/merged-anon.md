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
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | yes | overlap | MAJOR | - | R1, R3 |
| L5 | open | no | single | MAJOR | - | R3 |

## Blocking findings

### L1

#### L1.R1 (f1)

- claim: Task 10 acceptance forces the valid claim lookup `gh api user` in the design doc to be rewritten or deleted, breaking existing claim behavior that Task 2 and the source keep.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

#### L1.R1 (f2)

- claim: `./artifacts/` is not resolved to the package artifacts directory versus the never-staged project-root artifacts folder.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (f1)

- claim: The plan says exactly two things are written to a created issue, while its required flow also applies a mode label and may post a pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "Wave 5 (lines 61 to 69): replace the label step with the sequence of specification 2.1 (mode label only; `--type` when listed; `gh issue create` and the rename; type read-back; field POST and read-bac"

#### L1.R3 (f3)

- claim: Task 12 requires artifact files outside the plan's permitted edit locations, making its required deliverables incompatible with the scope constraint.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (f1)

- claim: The two-write limit conflicts with the required pushback comment when flag validation finds a disagreement.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value"
- anchor2: "pushback comment;"

#### L1.R2 (f4)

- claim: Task 12 requires a file outside the allowed edit locations, so its required artifact cannot be produced while obeying the constraint.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (f3)

- claim: The plan does not clearly distinguish prohibited direct edits under `.claude/` from the generated writes made by the required sync.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

### L4

#### L4.R1 (f5)

- claim: No task states writing .dev/issues/<N>/complexity-field.json with the Q2 body, or the option-not-found branch, so the POST instruction references a file nothing is told to create.
- anchor: "the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>`"

#### L4.R3 (f4)

- claim: The `--mode` wording says feature mode selects Feature, contradicting the stated rule that feature mode with area `tests` selects Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the issue type rule (mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature; Task is never chosen)"

## Other findings

- L2 (MAJOR, open, single): The HOW-WE-WORK /sc:issue row is at line 333 on disk, not line 329, so a number-only navigation edits the /sc:graph row.
- L3 (MAJOR, open, single): The return-contract test is at line 545 and the Will/Will Not test at line 580 on disk, not at the cited 492 to 520 and 527.
- L5 (MAJOR, open, single): The plan does not specify the values that `classification_missing` must contain, so an implementation could omit missing classifications from the third return-contract block.

## Reviser brief

Blocking finding ids: L1, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report <redacted> byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
