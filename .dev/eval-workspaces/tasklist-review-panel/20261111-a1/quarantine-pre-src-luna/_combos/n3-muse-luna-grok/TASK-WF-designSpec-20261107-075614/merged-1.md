review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n3-muse-luna-grok/t2b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n3-muse-luna-grok/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n3-muse-luna-grok/t4-2.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t2b-1, t4-2 |
| L2 | open | no | overlap | MAJOR | - | t2b-1, t4-2 |
| L3 | open | no | overlap | MAJOR | - | t2b-1, t4-2 |
| L4 | open | no | single | MINOR | - | t2b-1 |
| L5 | open | no | single | MINOR | - | t2b-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: resume_decision is given no target_sha or applied_edits source, so its row 4 re-entry into release_decision cannot perform the head-equals-target_sha proof the Release section requires for the landed and normally-published resume cases.
- anchor: "and `resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"
- anchor2: "phase `HELD` with `dangling_branch == \"landed\"` and phase `HELD` with `dangling_branch is None` and `published=True` each re-enter `release_decision` with `push_completed=True`"

#### L1.t4-2 (F1)

- claim: Failed settles add permanent slack and a not-changed confirm adds no toggle, so leftover slack hides a later user round-trip and the guard drafts the PR again.
- anchor: "`settled(draft, failed)` gives `RELEASE_PENDING`, increments `failed_mutations` and leaves `owned_draft` unchanged"
- anchor2: "`foreign` when observed transitions exceed `run_toggles + unsettled + failed_mutations`"

#### L1.t4-2 (F4)

- claim: A later cycle that reuses a held draft never moves cycle_id, so resume judges publication on the earlier cycle's push.
- anchor: "`held_cycle_published(events, guard)` (true when a `push_completed` event, normal or recovered, carries the guard's `cycle_id`)"
- anchor2: "phase `HELD` -> `NOOP(already_held)`"

## Other findings

- L2 (MAJOR, open, overlap): The required Wave 0 bullet names an L3 condition for the off line while its acceptance test is worded to fail when the bullet names an L3 or draft condition, so a whole-bullet test implementation rejects the bullet the task requires.
- L3 (MAJOR, open, overlap): The resolution tests require a gh repo view fallback line that carries neither --repo nor a repos/ path, so a literal every-gh-line scan of the script fails on a line the script must contain.
- L4 (MINOR, open, single): Comparing against start-of-sentence constants cannot assert a whole sentence byte-identical, so an edit to the middle or end of either pinned sentence would pass the specified test.
- L5 (MINOR, open, single): The grep for 43 still returns the pre-existing 42nd-43rd per-event numbering comment on a correct edit, so the check depends on reader judgement rather than on the grep result.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
