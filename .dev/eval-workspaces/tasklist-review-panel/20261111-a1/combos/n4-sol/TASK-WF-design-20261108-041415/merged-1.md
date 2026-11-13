review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-sol/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-sol/t3-1.md, block ok false
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-sol/t4-1.md, block ok true
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-sol/t2-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2b-1, t3-1, t4-1 |
| L2 | open | no | overlap | MAJOR | - | t2b-1, t4-1 |
| L3 | open | no | single | MAJOR | - | t2b-1 |
| L4 | open | no | single | MINOR | - | t3-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 10 acceptance forbids the gh api user path that Task 2 allows and unchanged claim text in the design doc uses, so the criterion cannot pass without an out-of-scope edit.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

#### L1.t2b-1 (F2)

- claim: Task 12 requires writing under ./artifacts/, which the edit-only constraint forbids, so the constraint and Task 12 acceptance cannot both be satisfied.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t2b-1 (F5)

- claim: The plan does not say whether the kept maintainer label lines keep their existing repo placeholder or switch to <R> as the global constraint requires.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block."

#### L1.t2b-1 (F6)

- claim: The described new tests assert folder-wide presence, so reverting Task 3 alone need not turn any new test red.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."

#### L1.t2b-1 (F7)

- claim: No task states the read-back value shape or comparison rule, and scout records option names only, so a direct name comparison falsely reports the field as not set.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"
- anchor2: "field id, data type, option names, or `not found` / `lookup failed: <reason>`"

#### L1.t3-1 (F3)

- claim: The sentence under-counts the mode label the same plan applies via `--label` on the same create call; the operational reading (two write actions) is consistent, the enumerative reading is not.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)"

#### L1.t3-1 (F4)

- claim: The plan's test scope omits tests/skills/test_worker_contract.py, which mirrors the exact gh api lines Tasks 2, 3 and 5 rewrite; that suite broke during execution (2 failures) and was fixed outside the plan.
- anchor: "`uv run pytest tests/skills/test_issue_protocol.py -v` passes and the new tests are collected"
- anchor2: "`make verify-sync` and `make lint` exit 0 and the whole `tests/skills/test_issue_protocol.py` file passes"

#### L1.t3-1 (F5)

- claim: Nothing records label-list truncation at the `--limit 200` read, so a repo with more than 200 labels can produce a false `not applied: label missing in repo` line and an unlabeled issue.
- anchor: "labels intersected with the repo labels in `scout.md`"

#### L1.t4-1 (F1)

- claim: The Wave 5 pushback comment is a third write to the created issue, which Constraint 23 forbids.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t4-1 (F2)

- claim: The listed Task 8 tests never assert Task 3 text, so reverting Task 3 cannot turn a new test red.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L1.t4-1 (F3)

- claim: Passing Task 10's acceptance needs a claim-text edit (line 157 gh api user) that Constraint 22 forbids, and Task 10's edit list omits it.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged, including its two-block part of the return contract"

#### L1.t4-1 (F4)

- claim: The artifacts folder is ambiguous, and the project-root reading is outside the editable paths and never staged.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "the outputs are saved to `./artifacts/t12-checks.log`"

#### L1.t4-1 (F6)

- claim: No minimum gh version is stated for the --type flag, so an older gh stops every create.
- anchor: "`--type` when listed; `gh issue create` and the rename"

#### L1.t4-1 (F7)

- claim: The 'before' text and several line numbers do not match the live checkout, so the base commit needs confirming.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

## Other findings

- L2 (MAJOR, open, overlap): The exact reason strings live only in a source.md that is not supplied with the candidate, so the implementer must guess them.
- L3 (MAJOR, open, single): The rewritten --mode row omits the Test issue type that a feature in area tests receives under the same plan.
- L4 (MINOR, open, single): Several cited line numbers are off against the live files (HOW-WE-WORK row at 330, return-contract test around 545-580, Will/Will Not test at 586, fork-safety model test at 701); the plan's own re-read constraint covers the drift and content anchors are correct.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
