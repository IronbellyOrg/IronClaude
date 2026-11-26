review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/evalsb-recipe/cand/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r1/normalised/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r1/normalised/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r1/normalised/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | 2.1, 2.3 | t2b-1 |
| L2 | open | no | single | MAJOR | 2.2 | t2b-1 |
| L3 | open | no | single | MAJOR | 2.1, 2.4, 2.5 | t2b-1 |
| L4 | open | no | single | MAJOR | 2.1, 2.5 | t2b-1 |
| L5 | open | no | single | MAJOR | 3.4 | t2b-1 |
| L6 | open | no | single | MINOR | 3.1 | t2b-1 |
| L7 | open | yes | overlap | MAJOR | - | t3-1, t4-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: The constraint counts only issue type and field POST as writes, so following it literally drops the mode label that the Goal and Tasks 1-3 require.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

### L7

#### L7.t3-1 (F1)

- claim: Task 12 requires creating an artifact outside the paths permitted by Constraints, so both requirements cannot be satisfied together.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L7.t4-1 (F1)

- claim: Task 12 requires writing artifact files outside the stated edit scope, so following both instructions is impossible.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L7.t4-1 (F2)

- claim: The plan does not explicitly require checking that an outside-organization caller gets a non-fatal `not set` line, as the driving document specifies.
- anchor: "It states, in plain bullets, the single manual check the owner runs after merge"

## Other findings

- L2 (MAJOR, open, single): Task 3 pins only the third block's keys and never states the source 2.2 values (read-back names or null; classification_missing without the not-set prefix), so a wrong-valued block passes.
- L3 (MAJOR, open, single): No task states the write-failed first-line-of-error rule or the explicit option-not-found case, and the <reason> placeholder acceptance passes with a literal placeholder.
- L4 (MAJOR, open, single): No task names the body file .dev/issues/<N>/complexity-field.json written after the draft rename, leaving the POST input path to implementer choice.
- L5 (MAJOR, open, single): Task 12 omits the source 3.4 org-visibility and API-version risks and mislabels Q7 as a fourth reversible owner default.
- L6 (MINOR, open, single): Named line numbers are stale (HOW-WE-WORK row is at 333, return-contract test at 545, fork-safety test at 695); the re-read rule mitigates this.

## Reviser brief

Blocking finding ids: L1, L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
