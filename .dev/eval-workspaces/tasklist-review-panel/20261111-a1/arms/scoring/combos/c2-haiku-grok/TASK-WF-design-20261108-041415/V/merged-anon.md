review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2 |
| L2 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Line 23 allows exactly two writes to the created issue, but Task 2 Wave 5 keeps a pushback comment posted to that issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every"

#### L1.R1 (M1)

- claim: The GitHub reference for this path documents only PUT, which replaces all stored values, so the POST may fail on every run (Medium, one fetch).
- anchor: "the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>`"
- anchor2: "The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs"

#### L1.R1 (M2)

- claim: The base commit is absent, the target wording and tests already exist, and the phrase Task 11 says to change is not in HOW-WE-WORK.md (Medium).
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"
- anchor2: "Edit `src/superclaude/core/HOW-WE-WORK.md` at line 329"

#### L1.R1 (M3)

- claim: The plan gives no rule for comparing the read-back value with Simple, Medium or Complex, so a successful write can be reported as not applied (Medium).
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R1 (M4)

- claim: The relative artifacts path can resolve to the project-root folder, which is outside the allowed trees and never staged (Medium).
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/`"

#### L1.R1 (M5)

- claim: Constraint 26 lists three defaults and Task 12 asks for four.
- anchor: "Decisions taken as defaults (the owner may reverse them later)"
- anchor2: "the four defaults the owner may reverse"

#### L1.R2 (F1)

- claim: The owner-check file Task 12 requires cannot be created inside the only directories the plan allows to be edited.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F2)

- claim: Following the exactly-two-writes rule drops the mode label and the pushback comment, both of which the plan requires on the created issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`), no longer asks for `type:` or `complexity:` labels"

#### L1.R2 (F3)

- claim: The required --mode cell says the issue type is Feature or Bug, while a feature in tests must be Test.
- anchor: "Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "mode `feature` with area `tests` gives Test"

#### L1.R2 (F4)

- claim: The plan never says the read-back value is an option id, so a name comparison marks a successful Complexity write as not set.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R2 (F5)

- claim: The task body and its acceptance criterion require two different spellings of the one allowed orgs path.
- anchor: "`create.md` states the single `orgs/<owner>/issue-fields` exception"
- anchor2: "the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields`"

#### L1.R2 (F6)

- claim: The live maintainer lines the plan says to keep use --repo <owner/repo>, not --repo <R>.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block."
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

## Other findings

- L2 (MINOR, open, single): The reasons the acceptance check names are in source.md, which is not in the candidate's folder, so the check cannot be run from the candidate alone.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
