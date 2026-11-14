# Proposal A: no; write SW-02's plan in the coordinator home and keep PR #539 to code and tests

## Answer

No: SW-02's plan package is written in the coordinator home named under Q26, referenced from the #539 work by its absolute path, and PR #539's commits stage named code and test paths only.

## What happens next if the owner picks it

1. A session in the coordinator home runs `/sc:workflow` for SW-02 (the skill always writes into the checkout it runs in), producing `.dev/tasks/to-do/<id>/` there, staged on the coordinator's branch.
2. The #539 author runs `/sc:implement <absolute path to that plan>` from the #539 checkout; code and test changes land in #539, while the plan's progress ledger is written in the coordinator home.
3. The #539 author commits named paths only; nothing under `.dev/tasks/` enters #539 from SW-02.
4. The ledger records the plan path.

## What it unlocks

- PR #539 keeps its reviewed surface as tight as rule A-004 intends: the only new files are the fix and its tests.
- The plan sits beside the program's other records, under the always-staged rule, on the program's branch.

## What it costs or risks

- Two checkouts are coupled for one item: the #539 author writes the progress ledger into another folder, which the coordinator also uses. Where `/sc:implement` archives a package that lives in a different checkout from the code is UNVERIFIED.
- If Q26 is left at its default, there is no coordinator home, so this answer has nowhere to put the plan and SW-02 stalls until Q26 is answered.
- The plan for a change in #539 is not in #539's history, so a reader of the merged code cannot find it from the PR.

## What stays unresolved

- The archive location question above.
- Whether the plan is ever committed (only when the owner asks, on the coordinator's branch).
