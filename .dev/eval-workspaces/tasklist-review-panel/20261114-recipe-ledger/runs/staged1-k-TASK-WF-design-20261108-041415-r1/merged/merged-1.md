review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/evalsb-recipe/cand/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-k-TASK-WF-design-20261108-041415-r1/normalised/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-k-TASK-WF-design-20261108-041415-r1/normalised/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-k-TASK-WF-design-20261108-041415-r1/normalised/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | 2.3, 3.1 | t2b-1 |
| L2 | open | no | single | MAJOR | 2.1, 2.5 | t2b-1 |
| L3 | open | no | single | MAJOR | - | t2b-1 |
| L4 | open | yes | overlap | CRITICAL | - | t3-1, t4-1 |
| L5 | open | no | single | MAJOR | - | t3-1 |
| L6 | open | no | single | MAJOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: An implementer following Task 10 must rewrite the allowed gh api user call (line 157) to repos/<R>/... or fail the check, breaking the claim login lookup.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

### L4

#### L4.t3-1 (F1)

- claim: The plan both forbids edits under `.claude/` and requires `make sync-dev`, which writes the development copies there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L4.t3-1 (F2)

- claim: Task 12 requires writing the manual-check artifact outside the only directories the plan permits editing.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L4.t4-1 (F1)

- claim: Task 12 requires writing two files under `./artifacts/`, which the scope constraint forbids, so the stated plan cannot satisfy its own acceptance criteria.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, single): The plan never names the body file path .dev/issues/<N>/complexity-field.json from spec 2.1, so any path passes the plan but the draft layout loses a known location.
- L3 (MAJOR, open, single): The plan drops Q4 words never typed from user input, so nothing forbids deriving the org from typed input as Q4 forbids.
- L5 (MAJOR, open, single): The source requires rerunning the level-table copy into CLAUDE.md, but Task 11 can leave that copy untouched.
- L6 (MAJOR, open, single): The plan omits the source's permission-visibility case: a caller outside the organization may not see the Complexity field and should receive a non-fatal `not set` result.

## Reviser brief

Blocking finding ids: L1, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
