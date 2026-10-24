pick: advice-4-b.md; runner-up: advice-4-a.md; reason: 7 vs 5 review findings cited
## Task 8: Deliver fixture-based generation results and implementation evidence

Acceptance criteria:
T8.AC1: - Cover S01-S29 and their unavailable-plugin/seeded-cache variants in the evaluation matrix. Record actual generated outputs and per-case pass/fail/blocked status separately from static checks. Do not substitute expected answers for observed output; missing execution prerequisites are explicit blockers, never passes.
T8.AC2: - The generated handoffs preserve current inputs, options, deliverable/authority boundaries and contract-gap degradation. Correct confirmed in-scope routing failures; do not execute product commands or repair deferred specialist engines.
T8.AC3: - Deliver an evidence-backed implementation summary mapping all twelve requirements and the 47 commands to delivered files/tests/results, with the remaining named contract limitations and any unexecuted evaluation cases explicit. Use a registered research/report template for the summary.
T8.AC4: - Appropriate lint/typecheck/tests and current parity/sync outputs are recorded honestly. No optional check substitutes for per-task specification compliance.
T8.AC5: - Keep task artifacts staged and product/source changes uncommitted. Whole-plan independent review, final state recheck and safe archive remain the executor's completion duties, not claims made by this task.

Steps:
1. Before editing, the parent must add src/superclaude/skills/sc-recommend/SKILL.md and plugins/superclaude/skills/sc-recommend/SKILL.md to the registered revert set. Today the revert restores only the two guide files.
2. Replace the response cell of the SKILL.md:159 row with this meaning: "Drop an irrelevant candidate without noise. A requested or selected target stays visible as `not installed: <name>`, never runnable. That covers a matched row's step, an explicitly named command, or the command the guide's Other commands entry selects for this request. Offer a justified native alternative only where the guide permits." In :149, change "a matched step remains visible" to "a matched or selected requested step remains visible". Make no other edits. The cold-worker prompt (prompts.py:163-166) already matches this rule, so leave it unchanged.
3. Copy SKILL.md byte-for-byte to the plugin copy. Run make sync-dev, but never stage .claude paths.
4. Regenerate the unavailable variants of S23, S24, S25, S26 and S27 with expectations withheld. Grade each with a fresh grader against its fixture row and SPEC:319/:759. S23 passes only if `not installed: sc:git` appears and any native status offer is labeled as justified. Then recheck all 7 earlier fixture-defect grades: any whose expectation agrees with the spec becomes pass or fail, never fixture-defect.
5. Reconcile results.json:
   - Set per-unit in_scope_routing_failure to true for S11-primary and S11-seededcache, or remove them from the confirmed-failures list, so the two agree (review-3.md:55).
   - Make the top-level status equal the final status, or rename it round1_status, so S04-repeat1 no longer shows fail next to final pass (review-3.md:55).
   - Mark S04-primary as generated under the superseded A2 wording (review-3.md:56).
   - Recompute the totals.
   - List the SKILL.md:159 correction under the confirmed in-scope corrections.
6. Rebuild the summary from template:137-178:
   - Assignment table line: "none: no loader exists for this task, so no Required class was injected."
   - Capability block (47 rows): Required class is DEMONSTRATED as the template fixes it (:90). Observed class is at most TESTED with Provenance `fixture`. Discharged is NO, derived from :108 with the comparison stated.
   - Criterion block (12 rows): Required class cannot be injected (no assignment table), so no row can discharge; mark each NO with that reason.
   - Both block verdicts and the overall verdict: QUARANTINE.
   - Put the delivered files, tests and results in the Observed fact cells. State that QUARANTINE reflects evidence that comes only from fixtures, not a test failure. Remove every DISCHARGED claim.
   - Correct the git row. Keep the limitations and the zero-unexecuted statement.
7. Rerun after the last edit: the affected pytest suites including tests/skills/test_sc_recommend_routing_contract.py and the parity tests, ruff check, format check, make verify-sync, cmp of both guide copies and of both SKILL.md copies. State the typecheck skip honestly. Write a fresh t8-final-checks.log.
8. Stage .dev/tasks and confirm no .claude path is staged. Confirm HEAD is still 77288289 and nothing is committed. Write t8-a4.diff covering the four product files.

differs-by: Earlier attempts left SKILL.md alone and graded the conflict with :159 as a fixture defect. This attempt fixes the source rule itself, and the summary reports the verdict the template computes (QUARANTINE) instead of an author-chosen DISCHARGED.
