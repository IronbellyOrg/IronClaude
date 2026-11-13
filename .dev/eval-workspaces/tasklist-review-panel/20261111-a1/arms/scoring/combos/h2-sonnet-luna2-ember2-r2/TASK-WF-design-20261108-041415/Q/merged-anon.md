review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R5: report <redacted>, block ok false
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3, R4, R5 |
| L2 | open | no | single | MINOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | no | overlap | MAJOR | - | R2, R3 |
| L5 | open | no | single | MINOR | - | R2 |
| L6 | open | no | single | MAJOR | - | R3 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: No task updates tests/skills/test_worker_contract.py, whose exact-line table pins the create.md, SKILL.md and issue-worker-t3.md lines the plan rewrites, so the full suite goes red and Task 12 never runs that file.
- anchor: "`make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"
- anchor2: "First, the gh call rule paragraph near line 9"

#### L1.R1 (F2)

- claim: If the pushback comment fails after the issue exists, the run STOPs before the final output, so the not-set lines are never printed and the three new return keys are null; the plan does not say what prints on that STOP.
- anchor: "`E-CREATE-FAILED` and `E-POST-FAILED` keep their current meaning."
- anchor2: "pushback comment; final output with every `not applied` and `not set` line)"

#### L1.R1 (F3)

- claim: Task 8 names no regex for the orgs/ scanner, so a plain orgs/\S+ pattern flags the prose Task 2 requires and truncates the spaced orgs/<owner of R>/issue-fields spelling.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals"
- anchor2: "and that no other `orgs/` path is allowed"

#### L1.R1 (F4)

- claim: None of the six listed new tests asserts text that only Task 3 adds to SKILL.md, so the revert criterion is not met for Task 3 by the tests as listed.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L1.R1 (F5)

- claim: The plan gives no rule for matching a single-select value in the read-back, whose response nests the option in single_select_option; comparing value to the option name could print a false not-applied-after-create line on every create.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R1 (F7)

- claim: The two-writes sentence omits the mode label and the pushback comment that the Goal and Tasks 1 to 3 keep; consistent only if read as the two new classification writes.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R1 (F9)

- claim: Task 12 writes files outside the four paths the Constraints allow; consistent only if plan-package output is exempt.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.R4 (F1)

- claim: The plan both forbids changes under `.claude/` and requires a sync that copies source files there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R4 (F2)

- claim: The plan requires writing the manual-check document and check log under `./artifacts/`, outside its permitted edit paths.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R5 (F1)

- claim: The plan forbids editing `.claude/` while requiring a sync command that copies source edits into `.claude/`.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.R2 (F1)

- claim: The plan never states the path of the Complexity POST body file, so the implementer must guess where it is written.
- anchor: "the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>`"

#### L1.R2 (F3)

- claim: The exactly-two-writes count appears to exclude the mode label that the goal and Task 1 require.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R2 (F5)

- claim: Kept maintainer label lines may retain the old <owner/repo> placeholder instead of the required <R> form.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

#### L1.R3 (F1)

- claim: Task 12 output path sits outside the four allowed edit roots and the package relative reading is unstated.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.R3 (F2)

- claim: Case insensitive matching is stated but the exact string to POST when cases differ is not stated.
- anchor: "matched to the field's option names without case sensitivity"

#### L1.R3 (F5)

- claim: A hard line number is cited without the re-read hedge the candidate uses elsewhere and has drifted.
- anchor: "in the style of `test_fork_safety_scan_fails_on_a_ref_without_repo` (line 642)"

## Other findings

- L2 (MINOR, open, single): Read literally this fails on the unchanged claim-mode line `gh api user -q .login` in the design doc; the skill's own rule allows the user path.
- L3 (MINOR, open, single): The test reads only SKILL.md, so keeping it unchanged does not check that the command file and the skill agree, and no other test covers Task 6's agreement criterion.
- L4 (MAJOR, open, overlap): The plan names the three keys but never defines the contents or format of classification_missing.
- L5 (MINOR, open, single): The quoted --mode row names only Feature or Bug and omits the Test case from the issue type rule.
- L6 (MAJOR, open, single): The candidate requires every reason from specification 2.4 without listing or attaching that section.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
