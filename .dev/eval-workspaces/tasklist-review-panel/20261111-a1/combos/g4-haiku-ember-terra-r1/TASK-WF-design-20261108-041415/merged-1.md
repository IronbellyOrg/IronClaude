review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/g4-haiku-ember-terra-r1/t4-1.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/g4-haiku-ember-terra-r1/t2b-1.md, block ok true
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/g4-haiku-ember-terra-r1/t2-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t2-1, t2b-1, t4-1 |
| L2 | open | yes | overlap | MAJOR | - | t2-1, t4-1 |
| L3 | open | no | single | MAJOR | - | t4-1 |
| L4 | open | no | single | MAJOR | - | t2b-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: The Constraints allow exactly two writes to a created issue, but Task 2 keeps a pushback comment, which is a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.t4-1 (F2)

- claim: None of the seven listed new tests asserts text that Task 3 adds, so reverting Task 3 leaves them all green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L1.t4-1 (F5)

- claim: Task 2 does not require the exact text not applied: label missing in repo: with a colon in create.md, so Task 8 test 4 fails after Task 2 as written.
- anchor: "Fourth, `create.md` and `labels.md` carry the three exact line formats"
- anchor2: "final output with every `not applied` and `not set` line"

#### L1.t4-1 (F6)

- claim: Read literally, every agent must contain a POST, which the worker rules forbid, while the source asks only that the skill write the field.
- anchor: "Third, the skill folder and the agents contain `-X POST` together with `issue-field-values` and no `-X PUT`."

#### L1.t4-1 (F7)

- claim: The output path is outside the allowed write set and does not say which artifacts folder, so it may land in the project-root artifacts folder, which is never staged.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.t4-1 (F8)

- claim: Most described edits are already on disk and the plan does not say what to do when an edit is already present, so the implementer must guess whether to edit or verify.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.t4-1 (M1)

- claim: The constraint names three default decisions and Task 12 names four, so the owner-check list and the constraint disagree.
- anchor: "Decisions taken as defaults (the owner may reverse them later)"
- anchor2: "and the four defaults the owner may reverse"

#### L1.t4-1 (M2)

- claim: The constraint forbids editing .claude/ but also requires make sync-dev, which writes there, and the text does not say the sync is the one allowed write.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"

#### L1.t2b-1 (F1)

- claim: Task 10 acceptance cannot pass while gh api user remains legal for claim mode.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.t2b-1 (F2)

- claim: Exactly-two-writes constraint contradicts the required pushback comment write to the same issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t2b-1 (M2)

- claim: The --repo <R> rule and the maintainer target-repo placeholder allow two different writings.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

#### L1.t2b-1 (N1)

- claim: The never-edit rule and the run-sync-dev instruction need one exception sentence.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.t2-1 (F1)

- claim: The required package artifact is outside every permitted edit location.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t2-1 (F2)

- claim: The required pushback comment adds an issue write beyond the two writes expressly permitted.
- anchor: "It writes exactly two things to a created issue besides the issue itself:"
- anchor2: "field POST and read-back; pushback comment; final output"

### L2

#### L2.t4-1 (F3)

- claim: The plan never says which property of the read-back to compare with the option name, so the wrong choice reports every Complexity value as not applied.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L2.t2-1 (F3)

- claim: The required mode description says feature mode picks Feature even when the same plan requires Test for a feature in the tests area.
- anchor: "Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "mode `feature` with area `tests` gives Test"

## Other findings

- L3 (MAJOR, open, single): No task adds a create bullet to the skill's Will list, so the agreement criterion cannot be met from the tasks as written.
- L4 (MAJOR, open, single): The plan never states the full reason list it requires from specification 2.4.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
