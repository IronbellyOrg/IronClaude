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
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | no | single | MINOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Constraint 23 forbids any write to the created issue beyond the type and the Complexity value, while Task 2 keeps the pushback comment on that issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output"

#### L1.R1 (F2)

- claim: The step list posts the Complexity value with no check that the field and matching option exist, so a missing field produces a POST with no field id instead of a not-set line.
- anchor: "the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>`"

#### L1.R1 (F3)

- claim: The type read-back has no condition, so with no --type passed it can add a false not-applied line.
- anchor: "type read-back; field POST and read-back"

#### L1.R1 (F4)

- claim: The area is not stated as the user flag or the worker-chosen value, so an implementer may pick either and get Test or Feature differently.
- anchor: "mode `feature` with area `tests` gives Test; every other feature gives Feature"

#### L1.R1 (F5)

- claim: No regex is given and the path spelling differs between tasks, so a plain non-space capture fails on correct text and the scanner is undefined.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals"
- anchor2: "names exactly one `orgs/` path, `orgs/<owner of R>/issue-fields`"

#### L1.R1 (F6)

- claim: Task 2 does not require the exact line formats in create.md, so following it can leave test 4 red.
- anchor: "final output with every `not applied` and `not set` line"
- anchor2: "Fourth, `create.md` and `labels.md` carry the three exact line formats"

#### L1.R1 (F7)

- claim: The kept mode-label lines carry --repo <owner/repo> rather than <R>, and the acceptance check covers only gh issue lines.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block"

#### L1.R1 (F8)

- claim: No writer is assigned for the new Issue type row in flags.md, and the worker files that write it are frozen.
- anchor: "`flags.md` gets a derived `Issue type` row by the Q7 rule"

#### L1.R1 (F9)

- claim: The artifact paths fall outside the four allowed edit roots, and the location is ambiguous between repo root and package folder.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.R1 (F12)

- claim: Constraint 26 lists three defaults and Task 12 lists four.
- anchor: "the four defaults the owner may reverse"
- anchor2: "Decisions taken as defaults (the owner may reverse them later)"

#### L1.R3 (F1)

- claim: The permitted edit paths exclude the required owner manual-check file, so the plan cannot satisfy both its scope constraint and Task 12.
- anchor: "- Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make syn"
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F2)

- claim: The plan requires a pushback comment on the created issue but also says exactly two things are written to it besides the issue itself.
- anchor: "The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Co"
- anchor2: "pushback comment"

#### L1.R3 (F3)

- claim: The `--mode` wording says feature mode picks Feature even for area `tests`, contradicting the rule that this combination gets Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "mode `feature` with area `tests` gives Test"

#### L1.R2 (F1)

- claim: The prescribed `--mode` row limits issue types to Feature or Bug, contradicting the rule that feature mode with area `tests` selects Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the issue type rule (mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature; Task is never chosen)"

#### L1.R2 (F2)

- claim: The plan both forbids edits outside the listed directories and requires an owner-check artifact under `./artifacts/`, so both requirements cannot be met.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F4)

- claim: The plan calls this a single manual check but directs the owner to run two issue-creation cases.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package. It states, in plain bullets, the single manual check the owner runs after merge"

## Other findings

- L2 (MINOR, open, single): Only one inventory test exists at line 209; lines 233 and 277 are unrelated, and the other cited lines have drifted.
- L3 (MINOR, open, single): The phrase is at line 333 in the live file, not 329.
- L4 (MAJOR, open, single): The task does not specify the required values and meanings for the three return-contract fields, leaving their implementation and verification underspecified.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report <redacted> byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
