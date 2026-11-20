<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (Route B, copy and surgical edits) -->
<!-- Merge date: 2026-11-17 -->

# Merged route: revise the stage 4 plan by copy and surgical edit, with five safeguards

Question: how do we revise the stage 4 plan (issue 552) so it reflects the owner's rulings of 2026-11-17 (the entry gate is no longer true; the reflect reviewer is a missing carrier; citations are stale)?

## Precondition (new)
<!-- Source: Variant 1 and Variant 2 (both QUALIFY A-001, A-002) -- merged per Change #1 -->
The owner decides the Task 1 gate first: waive, hold, or roll back. The gate wording depends on that answer, and README.md:9 says to generate a stage package only after the owner's go. No edit starts before that decision, and no stage 4 go is written by this work.

## The route
<!-- Source: Base (original, modified) -- steps 2 and 3 made concrete per Changes #2 and #3 -->
1. Copy `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/` to a new package id of the form `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>` (subject: lower camelCase, at most 16 characters, no hyphens; a `-2` to `-9` suffix is also allowed by the slug pattern).
2. Apply the changes with the Edit tool: rewrite the Task 1 entry gate and Constraints line, add one task for the reflect-reviewer carrier, fix stale citations (grep the copy for old package ids and archived package names). Make the same edits to the request file `stage-requests/stage4-request.md` and then copy it byte for byte to the new `source.md` (verify with `cmp`). The plan and its source must not disagree.
3. Make the package pass managed detection (managed-workspace.md:9-12): set `slug:` in the plan to the new id (folder, file name and slug all equal), write `return-contract.yaml` with `contract_version: "1.1"`, the same slug and `status: success` or `partial`, keep `source.md` as a regular file, and keep the package inside this checkout under `.dev/tasks/to-do/<slug>/`.
4. Run `/sc:reflect --mode pre` on the copy, read its report, and write its result into the contract. Skipping it is a recorded gap, not a pass (stage 3 shipped with the review marked owed).

## Rewards
<!-- Source: Base (original) -->
- Keeps what four revision rounds and the cuts debate produced: the 4-task shape, the decided keeps and the exact grep acceptance checks (won C-003, 70%).
- Small diff the owner can read line by line against a plan they know (won C-005, 70%).
- The rulings are narrow, verified on disk: the plan has 110 lines and 0 mentions of "reflect", so the carrier is an addition, not a rewrite.
- In-place editing of this plan is established practice (revisions 2 to 4).

## Risks
<!-- Source: Base (original, modified); Variant 1 -- merged per Changes #2 to #4 -->
- A hand-built package is not generator output. A miss on any of the four detection checks stops `/sc:implement` with `E-MANAGED-INVALID`. The package today has no `return-contract.yaml` at all.
- The review does not run on its own; it must be run and read by a person (A-003 accepted by both).
- Edits fix only what is looked for. Mitigation: the targeted grep in step 2.
- This route departs from the ledger rule "one managed package per stage, generated with /sc:workflow" (README.md:3). Record it as an owner-approved exception in the ledger row before running it.
<!-- Source: Variant 1 (Route A), Rewards 1 to 4 -- merged per Change #4 -->

## Switch to Route A (regenerate) when
<!-- Source: Variant 1 and Variant 2; X-002 unresolved -- merged per Change #5 -->
- the new carrier task forces changes to more than one existing task, or
- the pre-execution review finds more than one blocking defect, or
- the owner prefers the ledger rule over keeping the trimmed text.
Route A: edit `stage4-request.md`, then `/sc:workflow @<that file> --depth standard --handoff none`. It writes a valid package and runs the review itself, at the cost of rewriting all four tasks and tens of minutes.

## ROI claim
Route B has the better return for a narrow change: fewer files rewritten, a diff the owner can read, and the cuts-debate text kept. Its cost is a hand-written contract and a review someone must run and read. If the changes turn out wider than expected, Route A is the fallback.

## Not settled by the debate (UNVERIFIED)
- C-002: whether a hand-run review is skipped in practice (A) or equal to the built-in one (B). Stage 3 skipped it; that is one data point.
- X-002: whether the rulings change one task and a half (B) or enough to justify a rewrite (A). The 0-hit "reflect" count supports B only for the carrier addition.
- Whether `/sc:workflow` accepts an edited plan copy as its source, which would be a third route. Not checked.
- Quick depth: no rebuttal round and no invariant probe ran. Both advocates were general-purpose agents on the same model.
