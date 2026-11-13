review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r3-luna2-grok-src/t4-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r3-luna2-grok-src/t3-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r3-luna2-grok-src/t4-2.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t3-1, t4-1, t4-2 |
| L2 | open | yes | overlap | MAJOR | - | t3-1, t4-1, t4-2 |
| L3 | open | no | single | MAJOR | - | t4-2 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: The required `--mode` wording says feature selects Feature even though feature mode with area `tests` selects Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the issue type rule (mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature; Task is never chosen)"

#### L1.t4-1 (F4)

- claim: The plan does not specify how to interpret field read-back values, so an implementation may compare an option name with the returned option ID and falsely report the field as unset.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t3-1 (F2)

- claim: The plan requires a field-value read-back but omits the response interpretation needed to compare a single-select option name rather than its numeric value.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t4-2 (F2)

- claim: The read-back never says that a single-select `value` is an option id, so checking that property against the option name reports not-set after a successful POST.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t4-2 (F3)

- claim: The --mode row says the issue type is Feature or Bug, which is wrong for a feature whose area is tests.
- anchor: "the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "mode `feature` with area `tests` gives Test"

### L2

#### L2.t4-1 (F2)

- claim: The stated two-write limit omits the mode label that the goal requires applying.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L2.t4-1 (F3)

- claim: Task 12 requires writing artifacts outside the plan's stated allowed edit locations.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.t3-1 (F1)

- claim: Task 12 requires artifacts outside the plan's allowed edit paths, so its required outputs conflict with the stated scope constraint.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/."

#### L2.t4-2 (F1)

- claim: A create path that writes only the issue type and the Complexity field drops the mode label and the pushback comment that Task 2 requires.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "mode label only; `--type` when listed; `gh issue create` and the rename; type read-back; field POST and read-back; pushback comment"

## Other findings

- L3 (MAJOR, open, single): Editing the pinned gh api lines without updating test_worker_contract.py fails that file, and Task 12 never runs it.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
