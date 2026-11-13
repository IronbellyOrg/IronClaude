review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/g6-luna2-ember2-r3/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/g6-luna2-ember2-r3/t4-2.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/g6-luna2-ember2-r3/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/g6-luna2-ember2-r3/t3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | t4-1 |
| L2 | open | yes | overlap | MAJOR | - | t2b-1, t3-1, t4-1 |
| L3 | open | no | overlap | MAJOR | - | t2b-1, t3-1 |
| L4 | open | no | single | MINOR | - | t2b-1 |
| L5 | open | no | single | MINOR | - | t2b-1 |
| L6 | open | no | single | MAJOR | - | t2b-1 |
| L7 | open | no | single | MAJOR | - | t3-1 |
| L8 | open | no | single | MAJOR | - | t3-1 |
| L9 | open | no | single | MINOR | - | t3-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: The source-only constraint forbids the user-guide and test edits required by later tasks, so an implementer cannot satisfy the plan as written.
- anchor: "Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files."
- anchor2: "Edit `docs/user-guide/commands.md`: add `[--merge-guard {draft,off}]` to the `/sc:pr-submit` usage line"

### L2

#### L2.t4-1 (F2)

- claim: The Wave 0 bullet is required both to state the L3 off behavior and to pass an acceptance criterion that fails when it names an L3 condition.
- anchor: "and that at L3 with `--merge-guard off` the line"
- anchor2: "when it names an L3 or `draft` condition"

#### L2.t2b-1 (F2)

- claim: Wave 0 bullet rule conflicts with the required L3 off line unless L3/draft is read narrowly as L3 only and draft-gate wording.
- anchor: "that applies at every ordinal and in both modes and carries no L3 or `draft` condition"
- anchor2: "at L3 with `--merge-guard off` the line \"Remediation is unprotected: --merge-guard off.\" is printed once"

#### L2.t3-1 (F5)

- claim: The Wave 0 test wording must separate the ungated ref load from the at-L3 printed line, which the plan leaves implicit.
- anchor: "that applies at every ordinal and in both modes and carries no L3 or `draft` condition"

## Other findings

- L3 (MAJOR, open, overlap): Static-scan wording omits the gh repo view exception, so a literal substring test rejects the required resolution fallback.
- L4 (MINOR, open, single): merge_guard.py is already in CORE_PURE_FILES, so the step would create a duplicate entry.
- L5 (MINOR, open, single): Both lengths are unnamed, leaving the exact assertion vague.
- L6 (MAJOR, open, single): The ./artifacts location is ambiguous between repository root and package folder, which decides whether the git-status acceptance passes.
- L7 (MAJOR, open, single): Resume re-entry into release has no stated values for the edit count and target commit, so an implementer must guess them.
- L8 (MAJOR, open, single): The plan does not state whether the new reference joins the existing reference and file lists, so coverage of the new reference depends on an unstated choice.
- L9 (MINOR, open, single): Comparing against the literal start text proves only the start of each pinned sentence, not byte identity of the whole sentence.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
