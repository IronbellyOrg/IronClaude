review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/e1-grok-ember-luna/t4-2.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/e1-grok-ember-luna/t2b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/e1-grok-ember-luna/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t2b-1, t4-1, t4-2 |
| L2 | open | no | single | MAJOR | - | t2b-1 |
| L3 | open | no | single | MINOR | - | t2b-1 |
| L4 | open | no | single | MAJOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t4-2 (F1)

- claim: A read-back that treats the returned value as the option name reports Complexity as not set after a successful POST, because the name is single_select_option.name and value is a separate scalar.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"
- anchor2: "\"value\":\"<option name>\""

#### L1.t4-2 (F2)

- claim: The closed two-write list drops the mode label and the pushback comment that Wave 5 requires, so the issue is filed without the label the goal requires.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "mode label only; `--type` when listed; `gh issue create` and the rename; type read-back; field POST and read-back; pushback comment"

#### L1.t4-2 (F3)

- claim: The owner check says the Test mapping may be reversed, but the constraints and source 3.4 allow reversing only the org read, the area flag, and the mode labels.
- anchor: "the four defaults the owner may reverse (the `orgs/` read exception, keeping the `--type` flag, keeping the mode labels, area `tests` giving Test)"
- anchor2: "the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay."

#### L1.t4-2 (F4)

- claim: A literal check for the short orgs path fails the long path the same task tells the implementer to write, unless both spellings are copied.
- anchor: "states the single `orgs/<owner>/issue-fields` exception"
- anchor2: "read-only GET of `orgs/<owner of R>/issue-fields`"

#### L1.t2b-1 (F1)

- claim: Task 12 requires artifact writes outside the four listed edit trees.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t2b-1 (F2)

- claim: Kept maintainer lines carry --repo <owner/repo>, not --repo <R>.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block."

#### L1.t2b-1 (F4)

- claim: Task 1 list omits the option-name versus option-id read-back comparison.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t4-1 (F1)

- claim: Task 12 requires artifact writes outside the only permitted edit locations, so following both instructions is impossible.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, single): Literal copying of the instructed row text contains the forbidden label wording.
- L3 (MINOR, open, single): Vague history-retention rule may leave wording that trips the design-doc criterion.
- L4 (MAJOR, open, single): The plan does not specify matching the field ID and comparing the single-select option name, so an implementation could misreport a successfully set Complexity value.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
