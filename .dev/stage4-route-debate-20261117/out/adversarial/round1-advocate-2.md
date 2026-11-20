# Round 1 advocate statement: variant 2 (Route B, copy and surgical edits)

## Position summary
The owner's rulings touch Task 1 and the Constraints block plus one added carrier task; Tasks 2 to 4 need only citation fixes. A full regeneration spends tens of minutes to rewrite what is not broken and risks the cuts-debate keeps. Route B is better if its contract is hand-written and the review is run, both of which are cheap.

## Steelman of variant 1
Route A's strongest form: the plan has no `return-contract.yaml` (verified: folder holds only `TASK-WF-blockerStage4-20261116-030206.md`, `source.md`, `artifacts/`), so any plan needs a valid contract before `/sc:implement` will run it. The ledger rule (README.md:3) says one package per stage, generated with `/sc:workflow`. Stage 1 precedent (README.md:18): a hand-built package without a contract was replaced by a regenerated one, and the review then found a blocking finding. A generator-made package passes detection by construction and gets the review for free.

## Strengths claimed
1. Rulings are narrow. The plan has four tasks (plan lines 39, 67, 81, 101). The gate lives in Constraints line 20 and Task 1 lines 41 and 52-54. The word "reflect" appears 0 times in the plan (grep count 0), so the carrier is an addition, not a rewrite. Tasks 2 to 4 are untouched except line citations.
2. Rewriting everything puts hard-won text at risk: the "doubt-adjacent lines kept on purpose" decision (plan line 28) and the exact grep checks (lines 55-60) are the product of the cuts debate (line 19). A generator re-derives them from a request; the request holds only a summary.
3. Hand-built packages can pass detection. managed-workspace.md:9-12 lists four checks: slug regex plus folder and file name equal, contract 1.1 with the same slug and status success or partial, realpath under `.dev/tasks/to-do/<slug>/`, and `source.md` present. A copy under a new slug in `to-do/` meets all four. The realpath check fails only for a plan outside the checkout (line 11), not for a copy inside it.
4. Review cost is the same either way. `/sc:reflect --mode pre` can be run on the copy directly; Route A's "built in" run is just that command called by the generator.
5. Diff clarity: the owner can read three or four edits against a plan they know.

## Weaknesses identified in variant 1
1. It spends a full generation to change about one task and a half. X-002 stands: the premise "generator rewrites all four tasks" (A:19) is a cost, not a benefit.
2. A:19 concedes cuts-debate detail "can be lost unless the request carries it". The request is identical to `source.md` (verified with `cmp`: SAME) and is 89 lines against a 110-line plan whose long lines carry the checks. That is lossy by size.
3. A:15 "fixes stale line numbers by construction" is overstated. The plan already says line numbers are only hints and each place is re-read by its text (plan line 32), so stale line numbers are a low-severity defect either way.
4. A:12 cites stage 3 having no review; that is a process failure, not a property of copying.

## Concessions
- Route B must hand-write the contract and run the review, and stage 3 shows the cost: a skipped review and a stale id. Without discipline, B is worse.
- `source.md` must be edited too, or plan and source disagree (B:19). Route A gets this free.
- Ledger rule README.md:3 favors A. I could not verify whether `/sc:implement` or `/sc:workflow` checks that a plan was generated rather than hand-made: UNVERIFIED, detection lists no such check.

## Shared assumptions
- A-001 QUALIFY: both routes share the loss if stage 4 is held, but B loses less (small edits), which favors B.
- A-002 QUALIFY: the gate text depends on the owner's decision (waive, hold, rollback). Ask first; B can edit that one clause in minutes, A must re-generate.
- A-003 ACCEPT: the advisory review is useful but it is only as good as the person who reads it; I count it as equal on both routes.

## Contradictions
- X-001: the claim in A:16 is partly true (re-grounding does reach new text) but a regenerated plan can invent new stale facts, as stage 1 showed one blocking self-contradiction (README.md:18). Edits plus a targeted grep for stage ids and package names are enough.
- X-002: verified. The rulings reach Task 1 (gate), Constraints (line 20), and a new carrier task; Task 3's cadence line near 260 and Task 4's counts need re-reading only. Hand-built detection is passable (strength 3). The cost of B is a contract file, a `source.md` edit and a review run, all small.

## Confidence
62
