# Adviser ladder entry: opus

outcome: ready
| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T8.AC1 | Met (review-3.md:11), but the totals of 96 pass and 7 fixture-defect depend on grades that change below. | Keep all 103 units. Regenerate only the units affected by the rule change, keep the old outputs as superseded evidence, and recompute the totals from the final grades. |
| T8.AC2 | The finding stands; I could not falsify it. SKILL.md:159 says "Drop the candidate. Do not surface it" for every unmatched missing source. That contradicts SKILL.md:149, which drops only "irrelevant" ghosts, and the spec, which says missing plugin capabilities stay visibly unavailable (SPEC:319), the requested step stays visible (SPEC:759, :601). The fixture matches the spec (fixture:540), so calling it a fixture defect was wrong (review-3.md:20). The same rule applies to every Other-commands unavailable unit (fixture:526, :548, :570, :592, :614). S27 passed only because the generator ignored :159 (review-3.md:20). The review's 7 fixture-defect reasons cover S23, S26 and S27 (review-3.md:58). | This is an in-scope policy defect in an approved recommendation file (plan:151). Narrow only the :159 cell, and make :149 consistent with it. Leave the guide edits unchanged (attempt-3.diff:1-44). |
| T8.AC3 | The summary writes Required class itself and claims 47/47 and 12/12 DISCHARGED. The template says Required class is loader-injected and never author-written (template:89-90). Capability rows are always DEMONSTRATED (:90). Fixture provenance can never reach DEMONSTRATED (:97-98). Discharged is never author-written (:108-109). Any NO forces QUARANTINE (:124-125, :178). The git row repeats the S23 misclassification (review-3.md:29). | Keep the template, apply it as written and report QUARANTINE honestly. Keep all 12 requirements, all 47 commands and the named limitations. |
| T8.AC4 | Met, but the log only counts after the last edit (extras-3.log:52, :61, :64). The SKILL.md edit is a new edit. | Rerun every check after the SKILL.md edit and after mirroring it to the plugin copy. |
| T8.AC5 | Met (review-3.md:47, extras-3.log:69). | Same staging duties. The product diff now has four files. |

differs-by: Earlier attempts left SKILL.md alone and graded the conflict with :159 as a fixture defect. This attempt fixes the source rule itself, and the summary reports the verdict the template computes (QUARANTINE) instead of an author-chosen DISCHARGED.

steps:
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

| Status | Result |
|---|---|
| DONE | Confirmed both review findings from the spec, SKILL.md, the fixture and the template. Found four more Other-commands unavailable units that depend on the same drop rule. |
| NEXT | Register the SKILL.md revert set, then run attempt A4 with the steps above. |
