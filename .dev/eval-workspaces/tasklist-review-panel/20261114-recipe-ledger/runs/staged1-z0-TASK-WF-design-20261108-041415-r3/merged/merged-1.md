review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/evalsb-recipe/cand/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r3/normalised/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r3/normalised/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r3/normalised/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2b-1, t3-1, t4-1 |
| L2 | open | no | single | MAJOR | - | t2b-1 |
| L3 | open | no | single | MAJOR | - | t2b-1 |
| L4 | open | no | single | MAJOR | - | t2b-1 |
| L5 | open | no | single | MINOR | - | t2b-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 10 acceptance is unpassable because gh api user paths must stay allowed yet the criterion forbids every path except repos/<R>/ and one orgs read.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`,"

#### L1.t2b-1 (F2)

- claim: Task 12 requires a file under ./artifacts/ which the Constraints forbid, so both texts cannot be satisfied together.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t3-1 (F1)

- claim: The plan requires a mode-label write and a pushback-comment write while also limiting issue writes to exactly two, contradicting its required type and Complexity writes.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "mode label only; `--type` when listed; `gh issue create` and the rename; type read-back; field POST and read-back; pushback comment; final output"

#### L1.t4-1 (F1)

- claim: The plan both prohibits edits under `.claude/` and requires `make sync-dev`, whose target copies source files into `.claude/`, so its instructions cannot all be followed.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

## Other findings

- L2 (MAJOR, open, single): Candidate never states classification_missing holds each not-set line without the prefix, so any content passes the key-only tests.
- L3 (MAJOR, open, single): Candidate omits the required .dev/issues/<N>/complexity-field.json path and its post-rename location, allowing a lost-path file choice.
- L4 (MAJOR, open, single): Candidate drops the source requirement to also record the --type area in the pushback comment.
- L5 (MINOR, open, single): Task 8 test accepts bare orgs/<owner>/issue-fields, weakening the Q4 pin that owner is derived from R.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
