review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R3: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R2, R3 |
| L2 | open | yes | overlap | CRITICAL | - | R1, R2, R3, R4 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: For a feature in the tests area, Task 6 directs the command to describe Feature as the issue type while Q7 requires Test.
- anchor: "the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "mode `feature` with area `tests` gives Test"

#### L1.R2 (F5)

- claim: The kept maintainer gh label create lines carry --repo <owner/repo> while the constraint says every gh label line carries --repo <R>; the fork-safety scan only checks --repo presence.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block."

### L2

#### L2.R3 (F2)

- claim: Task 12 requires writing the owner check under artifacts, outside the allowed edit locations.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.R3 (F4)

- claim: The manual-check instruction says to file one issue but then directs the owner to repeat the check with a second issue.
- anchor: "the single manual check the owner runs after merge because no step of this plan wrote to GitHub: file one test issue"

#### L2.R4 (F1)

- claim: The plan requires applying a mode label but also says the issue type and Complexity field are the only writes besides the issue, contradicting its required create behavior.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L2.R4 (F2)

- claim: Task 12 requires writing the owner-check artifact outside the paths permitted by Constraint 19.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.R1 (F1)

- claim: Task 12 writes outside the allowed edit directories and never says which artifacts directory is meant.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.R1 (F2)

- claim: The default list has three items in the Constraints and four in Task 12, and the fourth is a stated rule.
- anchor: "Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`"
- anchor2: "and the four defaults the owner may reverse (the `orgs/` read exception, keeping the `--type` flag, keeping the mode labels, area `tests` giving Test)"

#### L2.R1 (F3)

- claim: The Goal wording promises the third block holds every unset classification, but the block holds only the not set lines.
- anchor: "and lists every classification it could not set in its final output and in a third return-contract block."

#### L2.R2 (F1)

- claim: The edit-only constraint forbids the ./artifacts/ write that Task 12 requires, so the implementer cannot satisfy both as written.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "write `./artifacts/owner-manual-check.md` in this package."

#### L2.R2 (F2)

- claim: Cited line numbers and test locations are stale against the live checkout but harmless because the plan instructs re-reading before each edit.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L2.R2 (F3)

- claim: The allowed orgs path is spelled two ways across tasks and the new test accepts both, so cross-file spelling consistency is unpinned.
- anchor: "create.md states the single `orgs/<owner>/issue-fields` exception"
- anchor2: "orgs/<owner of R>/issue-fields"

## Other findings

- L3 (MAJOR, open, single): The plan does not define field-write behavior when the Complexity field is not a single-select field, despite recording other field data types.
- L4 (MAJOR, open, single): The plan references an orgs path scanner helper that it never defines, so the self-check test cannot be added verbatim.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
