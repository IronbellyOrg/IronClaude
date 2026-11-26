review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/evalsb-recipe/cand/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r7/normalised/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r7/normalised/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r7/normalised/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | t2b-1 |
| L2 | open | yes | overlap | MAJOR | - | t2b-1, t3-1, t4-1 |
| L3 | open | no | overlap | MAJOR | - | t2b-1, t3-1 |
| L4 | open | no | single | MINOR | - | t2b-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 10 AC forbids the legitimate user path so the design doc must misstate or delete the claim gh api user lookup to pass.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

### L2

#### L2.t2b-1 (F2)

- claim: Artifacts path contradicts the edit-only list and is ambiguous between repo-root and package directories.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.t3-1 (F1)

- claim: An implementer who follows the stated text as written builds a plan that both forbids edits under `./artifacts/` and requires writing `./artifacts/owner-manual-check.md` and `./artifacts/t12-checks.log`, and that is wrong because both requirements cannot be met.
- anchor: "- Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make syn"
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.t4-1 (F1)

- claim: The exact-two-writes constraint conflicts with the required mode label and the conditional pushback comment, so following it omits required issue updates.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L2.t4-1 (F2)

- claim: The plan forbids edits outside its listed directories but requires creating an artifact under `./artifacts/`, so the scope constraint and required deliverable cannot both be satisfied.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L3 (MAJOR, open, overlap): POST body file path after the rename is unspecified, risking a write from the renamed draft directory.
- L4 (MINOR, open, single): Stale test line numbers differ from live file but the re-read rule mitigates them.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
