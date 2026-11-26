review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R4: report <redacted>, block ok false
- R5: report <redacted>, block ok true
- R2: report <redacted>, block ok false
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3, R4, R5 |
| L2 | open | yes | overlap | MAJOR | - | R1, R3 |
| L3 | open | yes | single | MAJOR | - | R4 |
| L4 | open | no | single | MAJOR | - | R5 |
| L5 | open | no | overlap | MINOR | - | R2, R3 |
| L6 | open | no | single | MAJOR | - | R3 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Constraints say the skill writes exactly two things to a created issue, but Task 2 Wave 5 adds a pushback comment on that issue, so an implementer cannot satisfy both.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F3)

- claim: The before-state the tasks describe is absent from this checkout (commit 1aa2e5c3 is missing and the live files already carry the new wording), so an implementer cannot tell which edits remain.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"
- anchor2: "Remove the 11 `type: ...` labels, the 3 `complexity: ...` labels and their `gh label create` lines"

#### L1.R1 (F4)

- claim: The output path is ambiguous between the project-root artifacts folder (never staged) and the package artifacts folder, and both sit outside the edit list.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.R1 (F5)

- claim: Read literally, the no-brace rule covers scripts/orca_worktree.py:376 (an f-string with a repo variable) while the same constraint keeps scripts unchanged, so the implementer must guess the intent.
- anchor: "No file may contain a brace placeholder for owner and repo"
- anchor2: "`scripts/*.py` and the four issue-body templates stay unchanged"

#### L1.R1 (F6)

- claim: The read-back gives no comparison rule, so an implementer who compares the returned single-select value with the option name reports a successful write as not applied.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R4 (F1)

- claim: The plan forbids editing `.claude/` while requiring `make sync-dev`, which copies changed source files into `.claude/`.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R4 (F2)

- claim: Task 12 requires a file outside the plan's permitted edit scope.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R4 (F3)

- claim: Task 2 requires a pushback comment on the issue, contradicting the constraint that exactly two things besides the issue are written.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment"

#### L1.R5 (F1)

- claim: Task 12 requires writing the manual-check file outside the candidate's explicitly permitted edit directories.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.R2 (F2)

- claim: The manual-check artifact path is outside the four roots the Constraints allow editing under.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.R2 (F3)

- claim: The candidate never states the single-select read-back shape (option name vs numeric id), so the implementer cannot know what the read-back proves.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R2 (F4)

- claim: Task 2 spells the allowed read shorter than the mandated `orgs/<owner of R>/issue-fields` form used everywhere else.
- anchor: "states the single `orgs/<owner>/issue-fields` exception and that no other `orgs/` path is allowed"

#### L1.R3 (F3)

- claim: ./artifacts/ is ambiguous between package artifacts and project-root artifacts and is not in the edit allow-list
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

### L2

#### L2.R1 (F2)

- claim: The seven tests Task 8 lists assert nothing about flags-decision.md, create-review-comment.md, the SKILL.md error rows or the create.md Wave 1 issue-types text, so reverting those edits keeps the suite green and the stated mutation check fails.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "Write one test per rule, each failing when the behaviour breaks."

#### L2.R1 (F7)

- claim: The task asks for a self-check that feeds the orgs/ scanner but never names the scanner function, so the test has no defined target.
- anchor: "Add one self-check test in the style of `test_fork_safety_scan_fails_on_a_ref_without_repo`"

#### L2.R3 (F1)

- claim: The orgs scanner the self-check test must feed has no defined regex, name or location, so the test may pass while missing a bad path or fail on prose mentioning orgs/
- anchor: "the skill folder and the agents contain `-X POST` together with `issue-field-values` and no `-X PUT`."

### L3

#### L3.R4 (F4)

- claim: The required `--mode` wording assigns Feature to feature mode, while the required `--type` wording assigns Test to a feature in the `tests` area.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the `--type` row (line 42) to say the area of the change, which selects issue type Test for a feature in `tests`"

## Other findings

- L4 (MAJOR, open, single): The plan does not specify matching the returned field row by field id and comparing the single-select option name, so a successful write could be reported as not applied.
- L5 (MINOR, open, overlap): The cited line 329 is 330 in the live file, so the cited number is stale.
- L6 (MAJOR, open, single): Task 3 names only keys and one sentence, leaving read-back vs wanted value semantics to inference from the source

## Reviser brief

Blocking finding ids: L1, L2, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
