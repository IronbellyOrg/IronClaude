review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n5-terra/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n5-terra/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n5-terra/t4-1.md, block ok true
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n5-terra/t2-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2b-1, t3-1 |
| L2 | open | no | overlap | MAJOR | - | t2b-1, t3-1 |
| L3 | open | no | single | MAJOR | - | t3-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 10 acceptance forbids the gh api user path that Task 2 allows and unchanged claim text requires, so the acceptance criterion cannot pass as written.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception, the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields`"

#### L1.t3-1 (F1)

- claim: Task 10's criterion omits the `user` path its own edit list preserves, so it fails as written against the doc the task produces and a letter-reading implementer would delete the correct `gh api user -q .login` sentence.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

## Other findings

- L2 (MAJOR, open, overlap): Task 12 writes under ./artifacts/ which the edit-only constraint does not list, so compliance depends on reading write as different from edit.
- L3 (MAJOR, open, single): The plan cites ./source.md as the only holder of the exact output-line reason enumeration, and that file is absent from the package, so an implementer working from the package must guess the canonical reason list.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
