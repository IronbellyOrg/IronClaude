review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n5-muse-glm-luna/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n5-muse-glm-luna/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n5-muse-glm-luna/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | t2b-1 |
| L2 | open | no | single | MAJOR | - | t2b-1 |
| L3 | open | no | overlap | MAJOR | - | t2b-1, t3-1 |
| L4 | open | no | single | MAJOR | - | t2b-1 |
| L5 | open | no | single | MAJOR | - | t2b-1 |
| L6 | open | no | overlap | MINOR | - | t2b-1, t3-1 |
| L7 | open | no | single | MAJOR | - | t3-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: The script cannot both have every gh line repo-scoped as stated and pass the _RESOLUTION_SCRIPTS tests, which require an unscoped gh repo view fallback line.
- anchor: "every `gh` call carries `--repo \"$REPO\"` or a `repos/${REPO}/...` path"
- anchor2: "Add the script to `_RESOLUTION_SCRIPTS` in `tests/pr_submit/test_static_grep.py`"

## Other findings

- L2 (MAJOR, open, single): Resume row 4 re-enters release_decision but neither resume_decision nor the folded guard supplies target_sha or applied_edits for the head proof.
- L3 (MAJOR, open, overlap): The Wave 0 acceptance test as worded can reject the bullet for the L3 off-notice clause the same task requires it to contain.
- L4 (MAJOR, open, single): If ./artifacts resolves at the repository root, the Task 1 and Task 13 records fall outside every path Task 13 allows in git status.
- L5 (MAJOR, open, single): An engage-failure halt creates no guard record, so the stated exit mapping reports released for a run halted as draft_guard_unavailable.
- L6 (MINOR, open, overlap): The decision and fold tables are delegated to a source file that is not in the candidate package, so the plan cannot be executed from the package as given.
- L7 (MAJOR, open, single): Programmatic callers of `run_skill` cannot express `--merge-guard off`; only argv parsing exposes the flag, a stated decision whose consequence deserves an owner's explicit sign-off.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
