review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/evalsb-recipe/cand/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r2/normalised/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r2/normalised/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r2/normalised/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | t2b-1 |
| L2 | open | no | overlap | MAJOR | - | t2b-1, t3-1, t4-1 |
| L3 | open | no | single | MINOR | - | t2b-1 |
| L4 | open | yes | overlap | MAJOR | - | t2b-1, t4-1 |
| L5 | open | no | single | MINOR | - | t2b-1 |
| L6 | open | no | single | MAJOR | - | t3-1 |

## Blocking findings

### L4

#### L4.t2b-1 (F5)

- claim: Generic <file> omits the source's .dev/issues/<N>/complexity-field.json path after the rename, so an implementer can point the POST at the pre-rename draft path that no longer exists.
- anchor: "the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>`"

#### L4.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a command description promising Feature for feature mode with area tests, and that is wrong because Q7 requires Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature"

## Other findings

- L1 (MAJOR, open, single): Line 329 is the /sc:graph row; the /sc:issue phrase is at live line 333, so a literal edit hits the wrong row and fails Task 11 acceptance criterion 2.
- L2 (MAJOR, open, overlap): The edit-only list excludes ./artifacts while Task 12 requires writing the manual check there, so the two statements disagree on where Task 12 output goes.
- L3 (MINOR, open, single): Named test line numbers are stale (st10 at 545, Will test at 580, fork-safety at 695); only the test names keep the directives findable.
- L5 (MINOR, open, single): The new orgs/ test accepts two spellings while Tasks 2, 3 and 5 prescribe exactly orgs/<owner of R>/issue-fields, so a wrong-spelling file passes the new test.
- L6 (MAJOR, open, single): The candidate specifies the third block's keys but not their values; the source requires read-back values or null for the first two and each not-set line without its prefix for classification_missing.

## Reviser brief

Blocking finding ids: L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
