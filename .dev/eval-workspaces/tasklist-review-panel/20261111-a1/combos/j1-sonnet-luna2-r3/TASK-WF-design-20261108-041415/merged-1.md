review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/j1-sonnet-luna2-r3/t1b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/j1-sonnet-luna2-r3/t4-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/j1-sonnet-luna2-r3/t3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t1b-1, t3-1, t4-1 |
| L2 | open | no | single | MAJOR | 2.2 | t1b-1 |
| L3 | open | no | single | MINOR | 2.1 | t1b-1 |
| L4 | open | no | overlap | MAJOR | - | t3-1, t4-1 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: The design doc keeps `gh api user -q .login` in the unchanged claim flow, so the criterion that every gh api path is repos/<R>/... or the orgs read cannot pass without rewriting claim text.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.t1b-1 (F2)

- claim: None of the seven listed new tests asserts SKILL.md-only text, so reverting Task 3 leaves every new test green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "the skill folder and the agents contain `-X POST` together with `issue-field-values` and no `-X PUT`"

#### L1.t1b-1 (F5)

- claim: A naive orgs/ regex flags the prose sentence that Task 2 requires, so the scanner needs a bare-token exception the plan does not mention.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files"
- anchor2: "that no other `orgs/` path is allowed"

#### L1.t1b-1 (F6)

- claim: The constraint counts two writes, but Wave 5 also writes the mode label and the pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t1b-1 (F7)

- claim: Constraints list three defaults while Task 12 asks the owner note to record four.
- anchor: "the four defaults the owner may reverse"
- anchor2: "Decisions taken as defaults (the owner may reverse them later)"

#### L1.t4-1 (F1)

- claim: The required owner-check and test-log artifacts fall outside the plan's explicitly permitted edit locations.
- anchor: "- Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t4-1 (F2)

- claim: The plan requires a sync that writes `.claude/` dev copies while forbidding edits to those same paths.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint`"

#### L1.t3-1 (F1)

- claim: Task 12 requires creating an artifact outside the plan's explicitly allowed edit paths, making its acceptance criteria incompatible with the scope constraint.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, single): The plan never says to match the read-back by field id and single_select_option.name, so comparing the raw value yields a false 'not applied after create'.
- L3 (MINOR, open, single): Who writes the Issue type row is unstated, and the unchanged T1/T2 workers fill flags.md from the template, so the row may be blank.
- L4 (MAJOR, open, overlap): The rewrite instructions do not state how to compare a single-select field's returned option ID and name, leaving an implementation path that falsely reports a successfully set field as missing.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
