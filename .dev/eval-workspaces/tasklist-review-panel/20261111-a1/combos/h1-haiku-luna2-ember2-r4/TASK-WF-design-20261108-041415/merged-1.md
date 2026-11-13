review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h1-haiku-luna2-ember2-r4/t2-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h1-haiku-luna2-ember2-r4/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h1-haiku-luna2-ember2-r4/t4-2.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h1-haiku-luna2-ember2-r4/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h1-haiku-luna2-ember2-r4/t3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t2-1, t2b-1, t3-1, t4-1, t4-2 |
| L2 | open | no | overlap | MAJOR | - | t2-1, t2b-1, t3-1 |
| L3 | open | no | overlap | MINOR | - | t2-1, t2b-1 |
| L4 | open | no | single | MINOR | - | t4-2 |
| L5 | open | yes | overlap | MAJOR | - | t2b-1, t3-1 |
| L6 | open | no | single | MAJOR | - | t2b-1 |
| L7 | open | no | single | MAJOR | - | t3-1 |
| L8 | open | no | single | MINOR | - | t3-1 |

## Blocking findings

### L1

#### L1.t2-1 (F1)

- claim: The never-edit-.claude rule and the required make sync-dev step contradict each other, so either verify-sync cannot pass or the no-edit rule is broken.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.t2-1 (F2)

- claim: The exactly-two-writes rule contradicts Task 2, which keeps the pushback comment as a third write to the issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.t2-1 (F3)

- claim: The edit-only path list forbids the ./artifacts files that Task 12 requires, so its acceptance cannot pass.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.t2-1 (F6)

- claim: Task 12 lists four defaults while the constraints list three, and the fourth is a rule rather than a default.
- anchor: "the four defaults the owner may reverse (the `orgs/` read exception"
- anchor2: "Decisions taken as defaults (the owner may reverse them later)"

#### L1.t2-1 (F7)

- claim: The kept gh label create lines in labels.md use the placeholder <owner/repo>, not <R> as the constraint requires.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

#### L1.t4-1 (F1)

- claim: Create mode is required to apply a mode label and may post a pushback comment, contradicting the limit of exactly two writes to the created issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type"
- anchor2: "pushback comment"

#### L1.t4-1 (F2)

- claim: Task 12 requires artifact files outside the plan's allowed edit locations, so its required deliverables cannot comply with the stated scope.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t4-2 (F1)

- claim: The stated two-write limit conflicts with the required mode label and pushback comment in create mode.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "postback comment"

#### L1.t4-2 (F2)

- claim: The plan requires a sync that writes under `.claude/` while also prohibiting edits there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint`"

#### L1.t4-2 (F3)

- claim: The required owner manual-check artifact is outside the plan's allowed edit paths.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t2b-1 (F1)

- claim: Task 12 requires a new file under ./artifacts/, outside the four directories the Constraints allow edits under, so no single implementation satisfies both texts.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t3-1 (F1)

- claim: Task 12 writes to ./artifacts/, which the edit-only constraint does not list.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t3-1 (F3)

- claim: Goal scope for classification_missing is broader than source 2.2, which covers only not-set lines.
- anchor: "lists every classification it could not set in its final output and in a third return-contract block"

### L5

#### L5.t2b-1 (F2)

- claim: Line 157 of docs/designs/sc-issue-command.md holds `gh api user -q .login`, is never named in Task 10's places to change, and violates the every-gh-api-path acceptance criterion as written.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "the Wave 1 lookup text (add the issue types and the Complexity field lookups and the single `orgs/` read)"

#### L5.t2b-1 (m1)

- claim: Line numbers are stale versus the live design doc; the plan's re-read disclaimer covers it.
- anchor: "at the places listed by grep for \"label\" (around lines 18, 76, 77, 197, 207, 224, 225, 283 to 293, 354, 366, 370, 449, 479 and 492)"

#### L5.t3-1 (F5)

- claim: History instruction and acceptance criterion leave the judgement of false wording unoperationalised.
- anchor: "Leave history and decision-log entries as they are except for wording that is now false."
- anchor2: "`docs/designs/sc-issue-command.md` no longer says that `type: <type>` or `complexity: <...>` labels are applied"

## Other findings

- L2 (MAJOR, open, overlap): The orgs scanner regex is not stated, and a naive pattern cuts the path at the space inside the placeholder, so the test fails on correct files.
- L3 (MINOR, open, overlap): Several cited test line numbers are stale against the live test file, which the constraints already say to re-read.
- L4 (MINOR, open, single): The plan does not specify that `classification_missing` must contain every classification failure.
- L6 (MAJOR, open, single): No stated behavior covers a Complexity field whose data type is not single_select, though the template allows text, number and date.
- L7 (MAJOR, open, single): Candidate never states the single-select read-back shape, so a numeric value may be compared directly to the option name.
- L8 (MINOR, open, single): The -k expression does not select the plugin-parity test, leaving the mirror check to cmp alone.

## Reviser brief

Blocking finding ids: L1, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
