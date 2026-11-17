# QA Report: report-only-scope (instance b)

**Topic:** one unified central Review Panel (shared core plus thin modules) from E1, E2 and E3 (run 2, report only)
**Phase:** report-validation (Gate 3, structural lens 5 of 5, instance b)
**Range reviewed:** lines 2115 to 5057 of `RESEARCH-REPORT-review-panel-unification-run2.md` (Sections 6 to 10, Appendix A pointer, Appendix B). Other half: Grep only.
**Grading:** grading-override.md applies (BLOCKING only for decision-affecting defect, missing required deliverable/section, or safety risk).
**Status:** In Progress

---

## Items Reviewed (lens checklist a to d, range 2115 to 5057)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a1 | Conflict log 6.12 present with debate result or deciding evidence per conflict (range) | PASS | Read 3107-3168, 3403-3544. Classification rule at 3143-3146: DECIDED-BY-EVIDENCE rows carry decision plus evidence, UNDECIDABLE rows are `ROUTED: C-nn`. 6.12.10 (3508-3517) sums 16+22+36+31+41+15+28 = 189, 10+21+14+25+21+15+28 = 134, 6+1+22+6+20 = 55 (recomputed, matches). Line 3539: all 15 slots adjudicated, all 55 routed rows have an outcome (6.12.9.1 at 3482). |
| a2 | Target architecture 7.1 present | PASS | Read 3650-3758: diagram, modules table, 9 core elements, invariants I-1 to I-9, defect-ownership table. |
| a3 | Future-use exposure check 7.2 present with verdicts | PASS | Read 3760-3823: 7.2.1 PR review (verdict NO block), 7.2.2 rf-qa (NO), 7.2.3 later reviewers (NO), 7.2.4 verdict table with conditions. |
| a4 | Value inventory 8.1: one destination per item, reason per DROP | PASS (with note) | Read 4209-4364. Rows are carried in Appendix A (`synthesis/synth-08-value-inventory.md`), not inline; the carrying change is declared at 4215 and 5033. Bash read-only check of that file: 5950 rows (`grep -c '^| \(VL-\|DR-\)'`); DROP section lines 4062-6034 holds 1969 rows, 0 of them lack `DROP[`; non-DROP section 45-4061 has 0 `DROP[` rows. Table 8.1.0 recomputed by hand: every column and row sum matches (CORE 948, reflect 278, tasklist 340, spec 69, pr-review 45, rfqa 53, EVAL 1365, HARNESS 467, KNOWLEDGE 416, DROP 1969 = 5950; ledger row totals 886, 868, 1685, 955, 796, 589, 171). |
| a5 | Overlap matrix 2.9 | OUT OF RANGE | Section 2.9 sits at lines 828-1109 (instance a). Not reviewed here. |
| b | No roadmap, branch plan, PR plan, risk register, schedule, effort estimate, owner assignment in range | PASS | Grep over the whole report for roadmap, branch plan, PR plan, risk register, schedule, timeline, milestone, sprint, weeks, hours, person-day, assignee, effort estimate: every hit in range is a "no roadmap" disclaimer, a name of an existing command or file, or a column name. All Effort cells in 6.1 to 6.11 (2165-2961) are XS to XL qualitative with an evidence basis (allowed). Risk cells are Low/Medium/High per option; 2131 states "Not a risk register". Section 8.2 read in full (4369-4540): (a) constraints C1-C29, (b) gates G1-G27, (c) dependency facts D1-D26, (d) acceptance evidence AE-1 to AE-15, (e) files touched; no phase, work order, estimate or owner. |
| c | Section 8.2 names byte-identical reflect contract 1.8.0 and the git ref constraint | PASS | C1 (4389): `contract_version: "1.8.0"`, 110 stable and 27 telemetry names; C2 (4390): `### 9.1` block byte-identical to HEAD; C4 (4392): `feat/review-panel` and `feat/review-panel/<name>` cannot both exist, with both git error texts (exit 128). Repeated as invariant I-1 (3731) and I-6 (3736). |
| d | No implementation, merge, worktree, branch creation, commit or push claimed as done or instructed | PASS (with note) | Grep for committed, pushed, merged into, created branch or worktree, git push, git commit, implemented: no hit in range claims work done by this task. "committed" hits in range are repository facts or future evaluation rules (3646, 4164-4165, 4416, 4496). Q-35 (4730) asks the owner whether run-2 output may be committed and pushed and says "Wait for the owner's word"; it instructs nothing. Section 10 and Appendix B (4806-5057) contain no plan content; 5057 repeats the report-only statement. |

## Issues Found

| # | Severity | Section | Finding | Evidence | Proposed Fix |
|---|----------|---------|---------|----------|--------------|
| 1 | MINOR (minor under grading override) | 7 axes 5-8 (3615-3618) and A-8 row (3634) | "Built now", "Ships now", "Core now" and "done now" phrasing stages the recommended design as a first change versus deferred parts. "the decided document and script fixes D1 (CV-1 ...) are done now" can be read as completed work, which this report-only task did not do. No decision, destination, conflict outcome or number depends on the wording: the same cells state the outcome (what is in the design, what is gated or deferred) and "now" has no date or order. | 3618: "D1 ... are done now, with the SKILL.md edit allow-list widened in the same change"; 3634: "the D1 document and script fixes are done now"; 3615: "Ships now:"; 3616: "Core now:"; 3617: "Built now". | Reword "done now" to "in scope of the recommended design"; "built now / ships now" to "in the recommended design". |
| 2 | MINOR (minor under grading override) | 8.2(a) C21 (4409), C28 (4416) | Two constraint rows read as short step sequences although 8.2 says "It orders no work": C21 lists "Coder slot first; `ccsession-models.json` `T4Model04`; ...; golden regenerated once; `make sync-dev`, `make verify-sync`"; C28 says the rule, script and values file "are committed after C-02 lands and before the first run commit". Both are adjudicated conditions tagged [ADJUDICATED CONDITION]; AE-3 (4496) carries the same pre-registration order as acceptance evidence, which 8.2 allows. Nothing is scheduled, estimated or assigned. | 4371 scope statement; 4409; 4416; 4496. | Optional: add "order stated by the debate, not a work order" to C21 and C28. |
| 3 | MINOR (minor under grading override) | 9.8 Q-35 (4730) | Suggested Resolution names a next-step command chain (`/sc:adversarial --compare --merge` on the two reports, then `/sc:workflow ... --depth standard --handoff none`). It is a pointer to the next workflow step in an Open Questions table, not a roadmap of the work, and it commits nothing. | 4730. | Optional: drop the second clause or label it a process pointer. |

No BLOCKING finding in this dimension and range.

## Summary

- Lens checks in range: 7 (a1 to a4, b, c, d); a5 (overlap matrix 2.9) belongs to instance a.
- Checks passed: 7 / 7. Failed: 0.
- Findings: 3, all MINOR (minor under grading override). Blocking: 0 (CRITICAL 0, IMPORTANT 0).
- Fixes applied: 0 (fix_authorization false; only this report was written).
- Confidence: Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (a5 excluded as out of range).
- Tool engagement: Read: 19 | Grep: 8 | Glob: 1 | Bash: 1 (read-only `wc`, `sed`, `grep -c` on Appendix A). No web research, no Tavily or fallback calls.
- Limit: Section 6 option bodies (2135-3106) were checked by grep for Effort and Risk cells, plan words and done-claims, not read line by line; 6.12 tables A to G (3171-3402) and 7.3 (3935-4208) were checked by grep for the scope terms only.

## Overall Verdict: PASS

Status: Complete
