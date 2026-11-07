# Round 1 - Advocate for Variant 2 (reviewer-2, qa persona)

Evidence below was Read this turn: plan, source.md Part 2/3/4/5, `src/superclaude/commands/analyze.md:92-101`, `src/superclaude/commands/brainstorm.md:152-157`, `src/superclaude/core/WORKER-CONTRACT.md:12-16,30-32`, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:280-286`, `.gitignore`, `src/superclaude/skills/sc-implement-protocol/SKILL.md:9`.

## Position summary

V2 is the only card that audits the plan against the brief's own fidelity rules (source.md:34: "the task acceptance criteria of the new plan must contain a check equivalent to its verifier"; Part 4 "copy exactly"), and it correctly finds two silent departures (F-16 line, F-13 sentence). V2 is the thinnest card, though: it missed the listed-contract conflict (C-001) that V3 found, and its P1 on F-16 is overstated on substance.

## Steelman

### Variant 1 (analyzer)
Strongest version: V1 is the only card that tested the plan's checks rather than reading them. It found that Task 4's `git show HEAD:` check, written with a short path, can pass without testing anything (plan:95 says "the same command for `refs/handoff-routing.md`"), and that no exit codes are recorded (plan:152). It checked the index and showed Task 7 bullet 3 is not vacuous today because the earlier package is already staged. And it saw that the plan's F-16 wording ("a branch the live-check worktree is built from") matches spec:282, which says the edits are committed to "the feature branch or a scratch branch with the user's authorization", with no merge step. That is right: I read spec:282 and it names no merge.
Critique: (a) A-2 (the listed-contract conflict) is filed P2 INFERRED although `analyze.md:98` ("written on every outcome") and `analyze.md:97` (refused directory: "printed in chat only") are directly on disk, and plan:133 states "no known false FAIL"; that is Grounded. (b) V1 calls the F-16 departure a "documentation nit" and never asks the brief's own question (source.md:34): where is the AC check equivalent to the F-16 verifier? The plan has none, and it also does not record why it departs, although it records another departure at plan:131. (c) A-1 says Task 5's check is weak because "grep -c exits 1"; the AC says "prints 0", so the exit code is irrelevant there. That half is overstated. (d) The Task 4 half of A-1 is real: a reader can fairly take "the same command" to mean the same full path, so the weakness is narrower than V1 presents.

### Variant 3 (refactorer)
Strongest version: R3-1 is the best finding on any card. Task 1 tells the worker "The nested contract is listed in `artifacts`, also when the call failed" (plan:38). Task 6 requires "every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`" without the `skipped`/refused carve-outs, which attach only to the later "required" clause (plan:128). The plan itself admits `/sc:analyze` can stop before writing (plan:128, the timeout parenthesis). A worker that follows Task 1 literally lists a contract that was never written, and the check then fails a correct run. That falsifies the plan's own claim at plan:133. R3-3 is also correct and unique: brainstorm.md:154 says that with `--report-dir` the worker contract is a separate file that only lists brainstorm's own contract, while `domain` and `enrichment_used` are fields of the own contract (brainstorm.md:65,102,156,191).
Critique: (a) R3-2 is a P1 resting on a premise V3 itself says was "not verified" (that the earlier package is untracked). The index shows it staged, so the P1 is false today. (b) V3 demands that the plan reword the skill sentence, but Part 4 (source.md:213-233) says "copy exactly, do not paraphrase". The defect is in the brief, and a rewording by the plan would be an unrecorded departure of the kind V3 ignores on F-16 and F-13. V3 is inconsistent about whether brief fidelity matters. (c) R3-4, R3-5 and R3-6 (companion sentence, "this tier's quality_tier", "Skill/Agent/Task all inferred") target sentences that Part 4 mandates verbatim (source.md:221, 230, 239). They are brief defects, not plan defects, and a plan review should say so. (d) V3 is silent on C-002/C-003, the two places where the plan really does not match the brief text.

## Strengths claimed

1. **Brief-fidelity audit with line evidence (R2-1).** Brief F-16 (source.md:199) requires the Constraints line "The edits reach the next live plan only after the owner commits and merges them; this plan does not commit." The plan carries a different sentence (plan:25). The verifier is "Constraints contains the quoted line" (source.md:201), and the plan has no equivalent AC. V1 confirms the departure; V3 never mentions it.
2. **Unrecorded-departure discipline.** The plan records one departure explicitly (plan:131, "Necessary deviation from the brief, recorded here"). Its silence on F-16 and F-13 is therefore inconsistent with its own practice, which is exactly what V2 reports.
3. **F-13 widening is forced, not careless (R2-2).** F-2 adds `status-after.txt`, so the brief's sentence "it writes only the logs under `./artifacts/`" cannot stay literal; plan:152 adds "and the status snapshot". V2 classifies it as a necessary deviation that needs recording and also notes it is still untrue because `make sync-dev` rewrites `.claude/` (plan:21 says so). V1 reaches the second point, not the first.
4. **Honest classification of R2-5.** V2 checked that the plan does satisfy Part 2/Part 4 spans and reports only a matrix-completeness defect. It does not inflate this. Source.md:34 (the "equivalent check" rule) is the preamble span the matrix never sampled, and it is the rule that gives R2-1 its force.
5. **Cheap, correct anchors.** R2-4 (step 4 line begins "4. Check the contract", spec:286) is confirmed by my Read of spec:286.

## Weaknesses identified

1. **V2 missed C-001 entirely.** This is the highest-severity item in the diff analysis. A QA card that reads plan:38 and plan:128 should have caught it; the evidence (analyze.md:97-98, plan:133) was one file away.
2. **R2-1 is P1 but should be P2.** Spec:282 requires only commit to a feature/scratch branch with the user's authorization; the brief's "commits and merges" is stronger than the spec. The plan's wording is arguably more accurate, and it still covers a P2 author on another branch, because it says a branch the worktree is built from. The real defect is unrecorded departure plus missing AC check, not a lost scenario.
3. **R2-3 is tagged Grounded but is speculation.** "Anything /sc:implement's final review or a mid-run reflect pass writes under .dev/" names no concrete file. The only support is that `.gitignore` has no rule for `.dev/reflect/` (I grepped it: no match), so such a write would appear as `??`. That is a plausible risk, not an observed one, and V1's check that executor outputs stay in the package is more specific.
4. **Short card.** Five findings, no INFERRED tags. Calibration across the three cards is better on V1 and V3, which separate checked from inferred.
5. **R2-2 says "necessary deviation" in the same breath as "departure unrecorded"; the card does not say what the plan should have written.** A fix line would have made it actionable.

## Concessions

- C-001/X-001: V3 is right. The defect exists, and plan:133's "no known false FAIL" is untrue because the plan concedes a timeout can leave no contract. I would keep it at P1 only in the narrow sense that it contradicts a stated plan claim.
- C-004/X-002: V1 is right that the P1 premise (earlier package untracked) is false today.
- C-005, C-006: V1's catches are real and V2 saw neither.
- C-007: V3 is right (brainstorm.md:154).
- F-16: V1 is right on substance (spec:282).
- V2's own P1 rating should be P2.

## Shared assumptions

- **A-001: QUALIFY.** `analyze.md:98` says the contract "is written on every outcome" and `analyze.md:97` says an unusable directory is refused with "printed in chat only"; WC-4 (WORKER-CONTRACT.md:31-32) defines `artifacts` as "every other file written". That supports the refusal edge. It does not cover a timeout kill before write, which is the plan's own carve-out (plan:128) and is not a handled "outcome" of the command. So the assumption holds for refusal and fails for the timeout path.
- **A-002: QUALIFY.** `/sc:implement` does "spec-compliance QA against that task's AC" (sc-implement-protocol SKILL.md:9). Task ACs are judged as written, so an unpassable AC blocks. But the F-16 Constraints line is in no task AC, so it will not block implement; it is a brief-fidelity matter for the pre-execution review. C-002 is therefore a recording/coverage defect, not an execution blocker.
- **A-003: QUALIFY.** Task 1 snapshots state before any edit and Task 7 compares to it, so changes before Task 1 cancel. Only changes after the snapshot matter (new untracked paths such as `.dev/reflect/` output, which is not gitignored). Today's index facts are from the diff analysis, not re-run by me.
- **A-004: ACCEPT.** Exact-substring pins are what the brief mandates (source.md:232-233) and are simple to verify. The weakness V1 found is in the `git show` verification of the pins, not in the pins.
- **A-005: QUALIFY.** The brief does not state a rule that the plan must record every departure. But it does state a rule that each F-n must have an equivalent AC check (source.md:34), and the plan's own practice at plan:131 is to record departures. Silence is a gap against those two, not against a free-standing reviewer convention.

## Diff-point positions

| Point | Superior position | One-line evidence |
|---|---|---|
| S-001 | none | Counts reflect depth, not correctness; V3's two P1s are one real (R3-1) and one on a false premise (R3-2). |
| S-002 | split | V1 and V3 separate checked from inferred; V2 tags R2-3 Grounded though speculative. |
| C-001 | V3 | plan:38 vs plan:128, analyze.md:97-98, plan:133 "no known false FAIL"; the sentence itself is brief-mandated (source.md:229, 217). |
| C-002 | split | V2: departure unrecorded, no AC equivalent (source.md:34, 199, 201; plan:25); V1: plan wording matches spec:282. P2, not P1. |
| C-003 | split | V2 shows the widening is forced by F-2 (plan:152); V1 shows the wanted literal sentence is absent and sync-dev still writes `.claude/`. |
| C-004 | V1 | Earlier package is staged; V3's untracked premise is false today; V2's exposure is real but unquantified. |
| C-005 | V1 | plan:95 gives only a short path for the routing ref; empty `git show` output makes `grep -c` print 0. |
| C-006 | V1 | plan:152 saves outputs to files with no exit-code capture; the AC asks to "show" exit 0. |
| C-007 | V3 | brainstorm.md:154 says with `--report-dir` the worker contract is separate and lists the own contract; `domain` and `enrichment_used` are own-contract fields. |
| C-008 | V3 | Companion sentence is general and the installed twin gets no edit; I did not re-verify WORKER-CONTRACT.md:24, and the wording is brief-mandated (source.md:221). |
| C-009 | V3 | plan:54 says "this tier's quality_tier" for a scan that can be recorded skipped; wording is brief-mandated (source.md:230). |
| C-010 | V3 | The spec names Skill and Agent already per V3's cites (spec:60,62); the residual-risk text is brief-mandated (source.md:239). Low. |
| C-011 | V3 | Plan shows Tasks 2, 3, 6 with no Depends-on line while Task 1 says "before any edit" (plan:33). |
| C-012 | V2 | The matrix skips the Part 3 preamble (source.md:34, the equivalent-check rule); the plan itself complies. |
| C-013 | split | V1 and V2 both right: spec:286 begins "4. Check the contract". |
| C-014 | none | All three confirm pins, slices and Part 4 copying; no disagreement. |
| X-001 | V3 | The conflict exists and falsifies plan:133; P1 is defensible only as contradiction of the plan's own claim. |
| X-002 | V1 | The earlier package is staged today; V3's P1 depends on an unverified premise. |
| X-003 | split | V1 right on substance (spec:282); V2 right that it is unrecorded and lacks an AC check; neither is P1. |
| X-004 | V2 | Forced by F-2 (necessary deviation), unrecorded, and still untrue because of sync-dev (plan:21). |
| X-005 | split | V1: executor outputs stay in the package; V2: `.dev/reflect/` is not gitignored, so other writes are possible. Nobody measured it. |
| A-001 | QUALIFY | Holds for refusal (analyze.md:97-98), not for the timeout kill the plan itself names (plan:128). |
| A-002 | QUALIFY | Implement judges per-task AC (SKILL.md:9); the F-16 line is in no task AC. |
| A-003 | QUALIFY | Task 1's snapshot neutralizes earlier state; only post-snapshot changes matter. |
| A-004 | ACCEPT | Exact-substring pins are what the brief mandates (source.md:232-233). |
| A-005 | QUALIFY | Not a brief rule, but source.md:34 and the plan's own practice at plan:131 make silence a gap. |
