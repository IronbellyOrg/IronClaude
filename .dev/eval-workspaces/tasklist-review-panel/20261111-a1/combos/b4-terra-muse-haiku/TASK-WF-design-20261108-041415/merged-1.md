review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/b4-terra-muse-haiku/t2-1.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/b4-terra-muse-haiku/t2b-1.md, block ok false
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/b4-terra-muse-haiku/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2-1, t2b-1, t4-1 |
| L2 | open | no | single | MAJOR | - | t4-1 |
| L3 | open | no | single | MINOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t2-1 (F1)

- claim: The required sync writes generated files under .claude even though the constraints forbid editing them.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.t2-1 (F2)

- claim: The required package artifacts are outside every permitted edit path.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t2-1 (F3)

- claim: The rewrite does not require the existing response-shape rule needed to compare a field option name reliably.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t2b-1 (F1)

- claim: Task 10 acceptance cannot pass on a correct design document because it forbids the allowed gh api user path that unchanged claim mode uses.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.t2b-1 (F2)

- claim: The exactly-two-writes cap can be read as forbidding the required mode label application and pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.t2b-1 (F3)

- claim: Keeping the maintainer label lines verbatim keeps --repo <owner/repo>, which the stated --repo <R> rule forbids.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block."

#### L1.t2b-1 (F4)

- claim: No read-back comparison rule is stated, so comparing the numeric option id with Simple, Medium or Complex reports every successful Complexity write as not set.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t2b-1 (F5)

- claim: The base directory for ./artifacts/ is unstated, so the manual check can land in the repo-root artifacts folder instead of the task package.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t4-1 (F1)

- claim: Constraint 23 allows only the type and the field as writes to the created issue, but Task 2 requires the pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.t4-1 (F2)

- claim: The read-back has no matching rule, so a correct single-select write can be reported as not applied.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t4-1 (F4)

- claim: The plan describes edits to a state the checkout already has, and its quoted test line numbers are stale.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"

#### L1.t4-1 (F5)

- claim: The artifact location is undefined and may fall outside the four editable trees.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.t4-1 (F6)

- claim: The maintainer label lines use `<owner/repo>` where the constraint asks for `<R>`.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

## Other findings

- L2 (MAJOR, open, single): The six listed tests do not turn red when Task 3's SKILL.md text is reverted.
- L3 (MINOR, open, single): The plan does not say that the org field read needs the read:org scope.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
