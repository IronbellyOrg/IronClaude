review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r2-sonnet-src/t4-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r2-sonnet-src/t3-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r2-sonnet-src/t4-2.md, block ok true
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r2-sonnet-src/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t1b-1, t3-1, t4-1, t4-2 |
| L2 | open | yes | overlap | MAJOR | - | t1b-1, t3-1, t4-1 |
| L3 | open | no | single | MINOR | - | t3-1 |
| L4 | open | no | single | MINOR | - | t1b-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: Constraint 23 allows exactly two writes to the created issue, but the Goal and Task 1 require a mode label write and Task 2 requires a pushback comment write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.t4-1 (F2)

- claim: Kept maintainer gh label lines read --repo <owner/repo>, which Constraint 21 forbids, and Task 1 acceptance checks only gh issue lines.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block"
- anchor2: "carries `--repo <R>`"

#### L1.t4-1 (F3)

- claim: The named commit is absent from this clone and the live tree already has the edits the tasks describe, so the stated before-state is wrong for this checkout.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"

#### L1.t4-1 (F4)

- claim: E-POST-FAILED is the current STOP code for the pushback comment, so a failed field POST could be routed to a STOP the text says must not happen.
- anchor: "`E-CREATE-FAILED` and `E-POST-FAILED` keep their current meaning."
- anchor2: "says a failed type or field never stops the run after the issue exists"

#### L1.t4-1 (F6)

- claim: Task 12 writes two files outside the four allowed trees, and the location is ambiguous between project-root artifacts (never staged) and the package folder.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t4-1 (F7)

- claim: The owner check omits source 3.4's API-version risk, where a 404 on an older default API version turns every field write into a not set line.
- anchor: "It also records the three UNVERIFIED points from the source section 3.4"

#### L1.t4-1 (F8)

- claim: Bare pipes inside a table cell split the GitHub table row, so the template would render wrong.
- anchor: "add an `Issue type` row (`<Feature | Bug | Test>`, reason: derived from mode and area"

#### L1.t3-1 (F1)

- claim: Constraint 23 allows exactly two writes to a created issue, but the Wave 5 sequence adds a pushback comment, which is a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.t3-1 (F3)

- claim: The kept gh label lines use the placeholder `<owner/repo>` instead of `<R>`, and the plan does not say to change them.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

#### L1.t3-1 (F5)

- claim: The plan does not say whether a 404 for a user-owned repo is recorded as not found or as lookup failed, which changes the final output line.
- anchor: "a failed read is recorded as `lookup failed: <reason>` and the worker continues"
- anchor2: "field id, data type, option names, or `not found` / `lookup failed: <reason>`"

#### L1.t3-1 (F6)

- claim: Constraint 26 lists three defaults, but Task 12 asks for four and adds one that the constraint does not list.
- anchor: "and the four defaults the owner may reverse (the `orgs/` read exception"
- anchor2: "Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`"

#### L1.t3-1 (F7)

- claim: The artifact path can be read as project-root artifacts, which is outside the four trees Constraint 19 allows.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.t3-1 (F8)

- claim: The plan gives no rule for an edit whose target text is already present in the working copy, and several cited line numbers have drifted.
- anchor: "must be re-read in the live file before each edit"

#### L1.t3-1 (F10)

- claim: The owner check omits the org-visibility and API-version risks that source section 3.4 also names.
- anchor: "It also records the three UNVERIFIED points from the source section 3.4"

#### L1.t4-2 (F1)

- claim: The design-doc check forbids gh api user, which claim mode and Task 2 still require, so the check cannot pass unless that lookup is deleted from the doc.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

#### L1.t4-2 (F2)

- claim: Checking the read-back value for the option name always reports not set, because GitHub returns the option id in value and the name in single_select_option.name.
- anchor: "body `{\"issue_field_values\":[{\"field_id\":<id>,\"value\":\"<option name>\"}]}`; read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t4-2 (F3)

- claim: The command mode row says the issue type is Feature or Bug, while a feature whose area is tests is Test.
- anchor: "Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "mode `feature` with area `tests` gives Test"

#### L1.t1b-1 (F1)

- claim: Tasks 2, 3 and 5 rewrite lines that test_worker_contract.py pins by exact text, and no task updates or runs that file, so the suite goes red unnoticed.
- anchor: "then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"
- anchor2: "the \"Read-only GitHub access\" bullet (line 27) keeps"

#### L1.t1b-1 (F2)

- claim: The design doc keeps the claim-section call `gh api user -q .login`, so the literal check fails on a line the plan says to leave unchanged.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

#### L1.t1b-1 (F3)

- claim: The Constraint allows only the type and the field as writes to the new issue, yet Wave 5 still posts the pushback comment and applies the mode label.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t1b-1 (F5)

- claim: The plan never says which row or key proves the Complexity value is present, so the read-back can report false 'not applied after create' or a false success.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t1b-1 (F7)

- claim: Task 12 writes files in the package artifacts folder, which the edit-path Constraint does not list.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

### L2

#### L2.t4-1 (F5)

- claim: None of the seven listed new tests asserts SKILL.md text, so reverting Task 3 leaves every new test green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "Third, the skill folder and the agents contain `-X POST` together with `issue-field-values`"

#### L2.t3-1 (F2)

- claim: No new test asserts the SKILL.md text that Task 3 adds, so reverting Task 3 leaves every new test green and the Task 8 acceptance cannot pass.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "Sixth, `labels.md` states Feature, Bug, Test and Simple, Medium, Complex."

#### L2.t3-1 (F4)

- claim: The required value contains spaces, and a whitespace-stopping regex would capture orgs/<owner and fail the equality check.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals `orgs/<owner of R>/issue-fields`"

#### L2.t1b-1 (F4)

- claim: None of the listed new tests asserts SKILL.md text, so a Task 3 revert stays green unless the orgs-location test is written as set equality.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

## Other findings

- L3 (MINOR, open, single): The old phrase still appears in files outside the plan's list, and no acceptance check sweeps the whole repo for it.
- L4 (MINOR, open, single): Spec 2.2 says labels_applied and labels_missing now cover the mode label only, but Task 3 does not tell the implementer to update that sentence.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
