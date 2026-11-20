# Route A: edit the request, then regenerate the plan with /sc:workflow

Question: how do we revise the stage 4 plan (issue 552) so it reflects the owner's rulings of 2026-11-17 (gate no longer true; reflect reviewer carrier missing; stale citations)?

## The route
1. Edit `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/stage4-request.md` (89 lines, holds Revisions 2 to 4, identical to the package's `source.md`) with the revisions.
2. Run `/sc:workflow @<that file> --depth standard --handoff none`. It writes a NEW package (never overwrites), a `workflow-plan/1.2` plan, `source.md`, and `return-contract.yaml` (1.1), then runs the built-in advisory `/sc:reflect --mode pre` on the result.
3. Read the printed plan and review result. Archive the old package only with owner approval.

## Rewards
- The package is valid by construction. The current package has NO `return-contract.yaml` (verified: the folder holds only the plan, `source.md` and `artifacts/`), and `/sc:implement` refuses a managed plan without a contract (`E-MANAGED-INVALID`). The generator writes it.
- The pre-execution review is built in. The ledger says this review is "owed" for stage 4. Stage 1's regenerated plan had its review find one blocking self-contradiction before any run; stage 3's hand-trimmed plan never had a review and carried a stale stage 1 package id.
- Plan and source stay in step: `source.md` is a byte copy of the request, so the review compares the plan against the text it came from.
- It follows the ledger rule (README.md): one managed package per stage, generated with /sc:workflow.
- Tasks are re-grounded against the post-stage-3 tree (codegraph and Read), which fixes the stale line numbers by construction.

## Risks
- The generator rewrites all four tasks from the request. Detail the cuts debate and four revision rounds put into the old plan can be lost or reworded unless the request carries it. Mitigation: the request already holds the revision history and is current.
- Cost: a full generation plus a Tier 2 review, tens of minutes, and the output must be read in full.
- A fresh plan is itself unreviewed by humans; the review is advisory.

## ROI claim
Highest assurance per hour for a plan that will change the live review rule in about 15 more files. The extra generation time is small next to a failed run or a second rollback.
