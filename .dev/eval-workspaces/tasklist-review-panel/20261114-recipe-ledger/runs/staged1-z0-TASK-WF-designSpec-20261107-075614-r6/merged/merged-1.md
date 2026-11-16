review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/evalsb-recipe/cand/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-designSpec-20261107-075614-r6/normalised/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-designSpec-20261107-075614-r6/normalised/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-designSpec-20261107-075614-r6/normalised/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | t2b-1 |
| L2 | open | no | single | MAJOR | - | t2b-1 |
| L3 | open | no | single | MAJOR | - | t3-1 |
| L4 | open | no | single | MAJOR | - | t3-1 |
| L5 | open | yes | single | MAJOR | - | t4-1 |
| L6 | open | no | single | MAJOR | - | t4-1 |

## Blocking findings

### L5

#### L5.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a plan that forbids required test and documentation edits, so the acceptance criteria cannot pass.
- anchor: "Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files."
- anchor2: "Edit `docs/user-guide/commands.md`: add `[--merge-guard {draft,off}]` to the `/sc:pr-submit` usage line"

## Other findings

- L1 (MAJOR, open, single): Wave 0 bullet must state the L3 off line yet its test fails it for naming an L3 condition; wording is ambiguous between gating and mentioning L3.
- L2 (MAJOR, open, single): Ref task omits source section 4.2, so event fields (idempotency_key format, first-only timeline_baseline/original_is_draft) never reach the protocol text.
- L3 (MAJOR, open, single): The source requires `fix_cycle_id` to reject every `n < 1`, but this criterion checks only zero, leaving negative cycle numbers unspecified.
- L4 (MAJOR, open, single): The source also calls for sync and sync verification after edits under `src/superclaude/`, while this plan requires per-task sync only for skills and commands.
- L6 (MAJOR, open, single): The plan does not require scenario coverage for crashes before and after every guard request and settle, as the driving document requires.

## Reviser brief

Blocking finding ids: L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
