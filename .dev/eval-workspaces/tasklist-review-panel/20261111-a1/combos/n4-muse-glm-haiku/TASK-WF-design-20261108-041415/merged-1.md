review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-muse-glm-haiku/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-muse-glm-haiku/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-muse-glm-haiku/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2b-1, t3-1, t4-1 |
| L2 | open | no | overlap | MAJOR | - | t2b-1, t4-1 |
| L3 | open | no | overlap | MAJOR | - | t2b-1, t4-1 |
| L4 | open | no | single | MINOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 10 forbids the gh api user path that Task 2 allows and the claim lookup uses, so the design document cannot satisfy both texts.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

#### L1.t2b-1 (F2)

- claim: Writing the required Task 12 artifacts breaks the edit-only constraint, and obeying the constraint fails the Task 12 acceptance criteria.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t2b-1 (M3)

- claim: The exactly-two-writes sentence can be read to exclude the mode label or the pushback comment that Task 2 requires.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t3-1 (F1)

- claim: Cited line numbers are stale against the live files, but the plan itself mandates re-reading before each edit, so no wrong edit follows.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.t3-1 (F2)

- claim: The artifacts path is two-readable (package-local vs project-root artifacts/); repo convention and 'in this package' resolve it, so at worst a file lands in the wrong directory.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a create flow that posts a pushback comment on the new issue, and that is wrong because line 23 says the skill writes exactly two things to a created issue besides the issue itself.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every"

#### L1.t4-1 (M4)

- claim: No new test covers create.md Wave 1, so reverting only that part of Task 2 leaves all tests green (Medium).
- anchor: "`create.md` names `issue-types` and `issue-fields` in Wave 1"

#### L1.t4-1 (M5)

- claim: The output folder is ambiguous and outside the constraint 19 edit list (Medium).
- anchor: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.t4-1 (N1)

- claim: The rule forbids editing .claude/ while requiring make sync-dev, which writes there; the intended reading is not stated.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"

## Other findings

- L2 (MAJOR, open, overlap): The Complexity read-back comparison rule is unspecified, so a successful field write can be reported as not applied after create.
- L3 (MAJOR, open, overlap): The third return-contract block fixes its keys but not the source or contents of their values.
- L4 (MINOR, open, single): --type names both the area flag and gh's issue-type flag, which a reader could confuse.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
