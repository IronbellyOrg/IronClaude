pick: refactor of advice-4-a.md; runner-up: none; reason: escalation 3
## Task 8: Deliver fixture-based generation results and implementation evidence

Acceptance criteria:
T8.AC1: - Cover S01-S29 and their unavailable-plugin/seeded-cache variants in the evaluation matrix. Record actual generated outputs and per-case pass/fail/blocked status separately from static checks. Do not substitute expected answers for observed output; missing execution prerequisites are explicit blockers, never passes.
T8.AC2: - The generated handoffs preserve current inputs, options, deliverable/authority boundaries and contract-gap degradation. Correct confirmed in-scope routing failures; do not execute product commands or repair deferred specialist engines.
T8.AC3: - Deliver an evidence-backed implementation summary mapping all twelve requirements and the 47 commands to delivered files/tests/results, with the remaining named contract limitations and any unexecuted evaluation cases explicit. Use a registered research/report template for the summary.
T8.AC4: - Appropriate lint/typecheck/tests and current parity/sync outputs are recorded honestly. No optional check substitutes for per-task specification compliance.
T8.AC5: - Keep task artifacts staged and product/source changes uncommitted. Whole-plan independent review, final state recheck and safe archive remain the executor's completion duties, not claims made by this task.

Steps:
1. Keep every A4 product edit byte-for-byte from attempt-4.diff: both HOW-WE-WORK.md clarifications and the SKILL.md missing-candidate rule, canonical and plugin copies (review-4.md:20 confirms they are correct and leave no stale unit).
2. From advice-4-a.md step 3: add one focused assertion to tests/skills/test_sc_recommend_routing_contract.py, in its existing style, pinning that the SKILL.md degradation row keeps `not installed: <name>` for a requested or guide-selected missing target while still dropping irrelevant candidates.
3. Keep all generation rounds as recorded; no regeneration is required because review-4.md:20 found no unit stale under the changed rule. Do not change any final_status.
4. In t8/results.json rename every unit's round-1 `reason` field to `round1_reason` so no superseded text sits beside final_status (review-4.md:54).
5. Replace the summary template: the claim-evidence matrix cannot be filled honestly here (review-4.md:29, review-4.md:53). Re-render t8-implementation-summary.md stub-first from the registered src/superclaude/templates/modularization-template-review/analyst-coverage-matrix_template.md: one row per required topic (the 12 requirements and the 47 commands), Covered? only YES/PARTIAL/NO, Source File(s) naming the files where each stated fact can be checked (delivered product file, mapping test file, t8/results.json, t8-final-checks.log), Coverage Detail with the evidence, Notes with limitations, zero-unexecuted statement in the Topic/summary, and the Overall Verdict computed by the template rule. Keep earlier summary versions as history.
6. Rerun the affected pytest suites (including the new assertion), ruff check, format check, make verify-sync, and cmp of both guide and both SKILL.md copies after the last edit; record t8-final-checks.log honestly with the typecheck skip. Stage .dev/tasks, stage no .claude paths, commit nothing, confirm HEAD is 7728828941242c9f096ecd8422599f7073175525, and write t8-a5.diff for the product files.

lessons from A4:
- review-4.md:29: the claim-evidence template's Required class enum, loader-computed Discharged and Artifact-verifiable Observed fact rules cannot be met without a loader, so claiming the template was applied as written was false.
- review-4.md:53: use a registered template whose columns can be filled from real evidence, with Source File(s) where each fact is checkable.
- review-4.md:54: superseded round-1 reason text remained next to the final status.

differs-by: The summary moves to the registered coverage-matrix template, whose columns can be filled truthfully from real evidence, and the SKILL.md degradation exception gains its own regression assertion; earlier attempts kept the claim-evidence template and left the new rule untested.
