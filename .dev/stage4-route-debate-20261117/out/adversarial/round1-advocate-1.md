# Round 1 - Advocate 1 (Route A: edit request, regenerate with /sc:workflow)

## Position summary
Route A is better. The three changes are made once, as edits to the request (a small, readable diff). The generator then produces a valid package and runs the review, both of which Route B must fake by hand.

## Steelman of variant 2
Strongest version: the plan has had four revision rounds and a cuts debate. Copying it keeps the 4-task shape and the exact grep checks, and the owner reviews a three-edit diff against a plan they know. Hand-writing a contract is a known, small job (managed-workspace.md:9-11 lists the three checks), and stage 3 already did it. It is also cheaper, and a generator can reword or drop decided keeps. B is right that regeneration carries real regression risk.

## Strengths claimed
1. The current package has no contract. Verified: the folder holds only `TASK-WF-blockerStage4-20261116-030206.md`, `source.md` and `artifacts/codegraph-grounding.md`. Without `return-contract.yaml` at `contract_version: "1.1"`, `/sc:implement` stops with `E-MANAGED-INVALID` (managed-workspace.md:7-10). The generator writes it (SKILL.md:105).
2. The pre-execution review is a built-in final step, before any handoff (sc-workflow-protocol SKILL.md:89). Under B it is a separate manual run, and the stage 3 precedent shows it gets skipped: README.md:20 says "reviewer pass owed".
3. Ledger rule, owner decision 2026-11-16: "one managed plan package per stage, each generated with /sc:workflow" (README.md:3, README.md:9). B's package is not generator output.
4. `source.md` equals the request byte for byte (verified with `cmp`: SAME, 89 lines each). Route A edits the one file, so source and plan cannot disagree. Route B must edit two files in step (managed-workspace.md:44 hashes both plan and source).
5. A's diff is also small: the owner reads the request edit, not 110 regenerated lines. The request already carries Revisions 2 to 4 and the decided keeps (README.md:32-33), so detail survives if the request states it.

## Weaknesses identified in variant 2
1. Its own ROI is conditional: "if the three edits are the only ones needed" (B:23). Adding a reflect-carrier task changes the task count and numbering, so it is not a "surgical" edit.
2. It needs a hand-written contract plus a hand-run review, two steps where errors are silent. The manual path produces a "skipped" review mark (B:18).
3. A copied folder must get a new slug that matches folder name and file name (managed-workspace.md:9). Any miss fails the whole run.
4. Stale citations: B fixes only what the author looks for. The stage 3 package named an archived package id (README.md:20 records it).

## Concessions
- A can reword or drop cut-debate detail (A:19). The mitigation depends on the request being complete; I checked it is the same text as `source.md`, but not that it states every decided keep. UNVERIFIED.
- A costs tens of minutes and a full read of the new plan.
- The advisory review is advisory only (SKILL.md:93).

## Shared assumptions
- A-001 QUALIFY: gate both routes on the owner's go for stage 4 first. Generating a plan is cheap, but README.md:9 says to generate only after the owner's go.
- A-002 QUALIFY: the gate wording depends on the owner's decision (waive, hold, rollback). Under A, put the decision in the request; under B, in an Edit. A is safer because the request carries it as a stated ruling.
- A-003 ACCEPT: the review is meaningful because it found a blocking self-contradiction on stage 1 (README.md:18). A person must read it.

## Contradictions
- X-001: Route A re-grounds against the code (SKILL.md:87 pre-check lists non-existent files and unresolved symbols). That is a check, not a guarantee. I withdraw "by construction" and say "checked by the pre-check".
- X-002: the premises differ, and B's premise breaks as soon as it adds a task. A's cost is the same four tasks, but the generator decides the split. Fact that changes cost: the contract is missing, so B owes a new file either way.

## Confidence
72
