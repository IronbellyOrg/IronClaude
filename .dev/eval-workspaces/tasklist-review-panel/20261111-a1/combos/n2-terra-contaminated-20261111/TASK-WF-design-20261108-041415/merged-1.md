review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n2-terra/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n2-terra/t4-2.md, block ok true
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n2-terra/t2-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t4-1, t4-2 |
| L2 | open | no | overlap | MAJOR | - | t4-1, t4-2 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: Constraint 23 allows exactly two writes besides the issue, but Task 2 Wave 5 keeps a pushback comment, which is a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t4-1 (F3)

- claim: Most target wording already exists at HEAD 8c93e1d, and the 'labels from a fixed set' phrase Task 11 says to change is not in HOW-WE-WORK, so the stated before-state is wrong.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"
- anchor2: "at line 329 (the `/sc:issue` row that says"

#### L1.t4-1 (F4)

- claim: The artifacts location is ambiguous and may fall outside the four trees that constraint 19 allows.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.t4-1 (F5)

- claim: The owner placeholder is spelled two ways across files; the test accepts both, so this is a wording note only.
- anchor: "states the single `orgs/<owner>/issue-fields` exception"
- anchor2: "name the one `orgs/<owner of R>/issue-fields` exception"

#### L1.t4-2 (F1)

- claim: The design-doc check cannot pass while the unchanged claim lookup still calls gh api user, and deleting that call makes the design false.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

## Other findings

- L2 (MAJOR, open, overlap): The read-back comparison rule and the failed read-back case are not stated, so an implementer may report a successful write as not applied.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
