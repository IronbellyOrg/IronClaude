# Route B: copy the original plan, make surgical edits, submit the edited duplicate as a new plan

Question: how do we revise the stage 4 plan (issue 552) so it reflects the owner's rulings of 2026-11-17 (gate no longer true; reflect reviewer carrier missing; stale citations)?

## The route
1. Copy `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/` to a new package id of the form `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>`.
2. Reason through each needed change and apply it with the Edit tool: rewrite the Task 1 entry gate, add one task for the reflect reviewer carrier, fix stale citations.
3. Set `slug:` in the plan to the new id, write a matching `return-contract.yaml`, keep `source.md`, and submit it as the new plan. Run the review separately (`/sc:reflect --mode pre`).

## Rewards
- Keeps what four revision rounds and the cuts debate already put into the plan: the 4-task shape, the decided keeps ("doubt-adjacent lines kept on purpose"), the exact grep acceptance checks. Nothing regresses by regeneration.
- Small, reviewable diff: the owner can read exactly what changed, line by line, against a plan they already know.
- Cheaper and faster: three edits instead of a full generation, and no risk of a generator reintroducing cut work.
- The plan was edited in place before (revisions 2 to 4); this is the established practice for this program.

## Risks
- A hand-copied package is not a generator product. Managed detection needs the slug to equal the folder name and file name, a contract with `contract_version: "1.1"` and the same slug, and the realpath under `.dev/tasks/to-do/<slug>/` (managed-workspace.md, Detection). A copy that misses any of these fails with `E-MANAGED-INVALID`.
- The built-in review does not run. The review must be run by hand and its result written into the contract by hand. This session had to hand-write stage 3's contract and ran it with the review marked "skipped".
- `source.md` must stay a byte copy of what the plan came from. Editing the plan without editing the request leaves source and plan disagreeing, which defeats the review's check.
- Stale text survives: edits fix only what we think to look for, and the plan has already shown stale ids (stage 3 named an archived package).

## ROI claim
Best cost and diff clarity, if the three edits are the only ones needed and the hand-written contract and review are done carefully.
