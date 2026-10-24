pick: advice-3.md; runner-up: none; reason: single adviser
## Task 8: Deliver fixture-based generation results and implementation evidence

Acceptance criteria:
T8.AC1: - Cover S01-S29 and their unavailable-plugin/seeded-cache variants in the evaluation matrix. Record actual generated outputs and per-case pass/fail/blocked status separately from static checks. Do not substitute expected answers for observed output; missing execution prerequisites are explicit blockers, never passes.
T8.AC2: - The generated handoffs preserve current inputs, options, deliverable/authority boundaries and contract-gap degradation. Correct confirmed in-scope routing failures; do not execute product commands or repair deferred specialist engines.
T8.AC3: - Deliver an evidence-backed implementation summary mapping all twelve requirements and the 47 commands to delivered files/tests/results, with the remaining named contract limitations and any unexecuted evaluation cases explicit. Use a registered research/report template for the summary.
T8.AC4: - Appropriate lint/typecheck/tests and current parity/sync outputs are recorded honestly. No optional check substitutes for per-task specification compliance.
T8.AC5: - Keep task artifacts staged and product/source changes uncommitted. Whole-plan independent review, final state recheck and safe archive remain the executor's completion duties, not claims made by this task.

Steps:
1. Start from the reverted Q0 guide. Apply the S11 sentence from attempt-2.diff:41 again, unchanged.
2. In section 3.7 of src/superclaude/core/HOW-WE-WORK.md, keep the existing text "a hidden-config-only target is not exhaustively audited" exactly as it is (attempt-2.diff:31), because the phrase assertions depend on it. Replace only the A2 ending with this meaning: still route to `/sc:cleanup-audit`, state that the target falls under the hidden-path exclusion floor so it cannot be covered exhaustively, and never claim exhaustive coverage. Do not use "instead". Do not offer a replacement or native route.
3. Copy the guide byte-for-byte to plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md. Change no other file. Do not edit the fixture, the tests or the cleanup-audit sources.
4. Regenerate S04-repeat1 against the updated guide with expectations withheld. Grade it with a fresh grader against fixture:118 and :128 plus SPEC:794. Set final_status from the grade: pass only if target_ok=true and the claim is rejected, otherwise fail. Keep the A2 output as superseded evidence.
5. Regenerating S04 primary, unavailable and seeded-cache is optional. The edit does not affect their request (review-2.md:54). If you skip them, say so in the summary.
6. Update results.json for S04-repeat1 and add the hidden-only coverage limitation to named_limitations. Update the S04 counts, the corrected-case list and the limitations section in t8-implementation-summary.md, keeping the template headings.
7. Rerun the checks from the AC4 row and write the log after the last edit. Then stage .dev/tasks, confirm no .claude paths are staged, and confirm HEAD is still 77288289.

differs-by: The fixture is treated as correct against spec S04. The guide wording is fixed so cleanup-audit stays the target for a hidden-only request and coverage is limited only by disclosure. A2 instead changed the target to native inspection, and the reviewer's other option was to relabel S04-repeat1 as a fixture defect. This advice rejects both.
