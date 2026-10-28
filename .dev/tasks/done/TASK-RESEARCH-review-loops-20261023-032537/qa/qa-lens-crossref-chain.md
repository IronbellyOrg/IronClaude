## Crossref-Chain-Integrity QA Report
**Report reviewed:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md (1,263 lines, read in full: lines 1-1263)
**Lens:** Crossref-Chain-Integrity (QA phase report-lens-crossref-chain; Task Step 6.8)
**Date:** 2026-10-24
**Reviewer:** rf-qa-qualitative, report-only (fix authorization false); no file edited
**Output path for parent persistence:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-lens-crossref-chain.md
**Governing template:** `/config/.claude/skills/tech-research/SKILL.md:1042-1151` (Lens-Specific QA Agent Prompt Template; Crossref-Chain-Integrity Checklist at :1102-1106). Task Step 6.8 rules (task file :405-407) override the template's "at least N errors" quota: no quota is applied.
**Inherited Structural Verdict:** none supplied in the spawn prompt, so I reviewed standalone.
**Gate context:** The report header (:10) says the Phase 5 synthesis gate advanced by user authorization without cycle-2 verification. I treated every synthesis-derived claim as unverified and checked it against primary package sources.

### Checks Performed
| # | Check | Result | Evidence |
|---|---|---|---|
| a | Every Section 4 gap leads to a Section 8 step or a Section 9 question | FAIL | Traced all 12 gap rows (:311-322) against Section 8 (:779-911), Section 9 (:918-939) and the Section 10.10 map (:1240-1253). Rows exist for every gap, but the persisted-summary condition of gap 8 is lost, and two mappings in 10.10 point at questions that do not address their gap (Findings 2 and 4). |
| b | Every Section 6 hypothesis traces to Section 2 or real external evidence | PASS, with a citation defect | Options A-E (:478-609) each cite cases represented in Section 2.2-2.5 (:143-231). Section 5 is a reasoned N/A, so there is no external evidence to trace. Option C's Support row has unresolvable or missing citations (Finding 5). |
| c | Every ranked recommendation in Section 7 traces to debate arguments and the comparison | PASS, with citation-precision defects | Re-read `ADV/debate-transcript.md:40-219,240-489`. Every rank-position citation in 7.1 resolves to the stated advocate statement: :258, 297, 337, 378, 419 (V1); :343, 380, 421 (V3); :264, 302, 343, 379, 385, 425 (V2); :384, 426 (V5); :381, 384 (V4). The 7.2 orders match :477-484, and the tallies match :486 and `invariant-probe.md:43`. Two citations overclaim (Findings 6 and 7). |
| d | Every actionable finding traces to a gap or a proposed check | PASS | 7.5 "Not a card cause" (Task 10 overreach, record 2028) leads to gap 6 (:316) and the Section 8 Phase 3 consent row (:867). Checkpoint-guard and live-source findings in 2.5 (:226-228) lead to gaps 9 and 10 and Phase 3 rows. 7.6 orders 1-4 map one-to-one onto Section 8 Phase 2 rows (:846-851). |
| e | Each citation points to text that actually supports the claim, not just an ID | FAIL | Two current-protocol line anchors now resolve to text that does not support the claim (Findings 1 and 3). |
| f | No dropped controls or conditions | FAIL | The gap 8 target condition is dropped between Section 4 and Section 8 (Finding 2). The successful controls (Session 10 Task 4, Session 17 Task 8, Session 17 FINAL, Sessions 13/14) keep their deck limits in Options A, B, D and E and in Section 8 Phase 3: checked against `evidence-deck.md:650-655`. |
| g | No made-up file links | PASS | Bare artifact names resolve through the case registers: `coverage-matrix.yaml` and `merged-verdict.yaml` via `research/01-session-ac2cd1fd.md:38-41`; `t12-review-2.md` via `research/02-session-a9b88895.md:55,214`; nested agent IDs via `research/06-session-0690ee9f.md:86,167,195,212,244-256`. |

### Findings
| # | Severity | Section | Finding | Proposed Fix |
|---|---|---|---|---|
| 1 | IMPORTANT | 2.3 (:176-178); 6 Option E current-rule row (:603); 7.5 V5 row (:713) and lead note (:716) | The report cites the checkout copy `/config/workspace/IronClaude/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:42` for the plan/source pin and says the installed copy has it at line 43, as if the two copies differ. Commit `c6009cd3` (2026-10-23T18:03:42Z, "1 insertion") came after the rule map (`research/scope-rules.md:45` still cites :42). It moved the text down one line. Today, in HEAD and in the working tree, checkout line 42 is blank and the pin text ("The first `T<id>: start` line is the immutability boundary") is at line 43 in both copies (`grep -n "immutability boundary"` returns :43 for both paths; `git show c6009cd3^` returns :42). So the cited checkout line holds no supporting text, and the stated difference between the two copies no longer exists. The other managed-workspace ranges in 2.3 (:44-60, :60-68, :78-85) use the old numbering and are off by one. | Re-anchor every checkout `managed-workspace.md` citation to the current lines (pin :43; re-read and shift :44-60, :60-68, :78-85). Delete the "installed-layer line 43" contrast in :603, :713 and :716, or replace it with a dated note: "rule map read :42 before commit c6009cd3; both copies now :43". |
| 2 | IMPORTANT | 4 gap 8 (:318) → 8 Phase 3 (:865) and 10.10 (:1249) | Gap 8 has two parts: missing ledger events, and persisted summaries that shorten reviews (Orca's 13/3 narrative and the condensed targeted verdict). Its target state requires: "Where a persisted summary or verdict condenses a review, read the original returned review before counting or classifying its findings." Section 2.6 (:239) explicitly sends the condensed verdict to this gap. The mapped Section 8 row, "Keep results and denominators separate" (:865), covers only ledger omissions ("A ledger can omit real review events"). Nothing in Section 8 (:779-911) mentions condensed or persisted summaries or the returned-review condition (grep for condens / 13 fixed / 13/3 / persisted summar / returned review: no match). No Section 9 question covers it either. 10.10 nevertheless marks the gap linked, with "None" for questions. | Add the condition to the Details of the :865 row, bound to `research/01-session-ac2cd1fd.md:81,90-103,253` and `research/evidence-deck.md:613,858-859`, or add a Section 9 question. Then update the 10.10 row at :1249. |
| 3 | MINOR | 2.3 "Bounded automatic task attempts" row (:175) | `src/superclaude/skills/sc-implement-protocol/refs/retry.md:142-146` is presented as "read directly from the current checkout". In the current working tree those lines read "If A5 fails ... ### Model ladder", because of uncommitted edits on the checked-out branch (`git diff`: +20/-1 lines, hunk at :78). The supporting text ("Cost and caps ... Each resume after a halt adds an operator review") is at :142-146 only in HEAD `bbbfcc4b` and in the installed copy `/config/.claude/skills/sc-implement-protocol/refs/retry.md`. | Name the version that was read (HEAD `bbbfcc4b` or the installed copy) and the observation time. Do not edit `retry.md`: those edits are the user's own uncommitted work. |
| 4 | MINOR | 10.10 gap-to-question table (:1242, :1248) | Two links are question IDs that do not address the gap. Gap 1 (behavioral requirements exceed the checks credited as coverage) maps to Q15 (:934), which asks whether durable evidence pointers support their criteria. That belongs to gap 4, which is also mapped to it. Gap 7 (reviewer overclaims, duplicates and faulty proposed repairs) maps to Q2 (:921), which asks why reviewers missed defects that already existed: the opposite failure. | Set those question cells to "None", or name a question that really bears on each gap. |
| 5 | MINOR | 6 Option C Support (:545) | "Orca source contradictions (source `:142,285,382,402`)" names no file. "source" is not a path, and this clause cites no case report, so the reader cannot locate the lines. The real anchor is `research/01-session-ac2cd1fd.md:296-297` (Source:142/285/382/402). "CI boundary-file dispute, later conceded as optional hardening" has no citation at all, although its source card cites it (`synthesis/hypothesis-03.md:60`). | Add `research/01-session-ac2cd1fd.md`, section 6 (:296-297) to the Orca clause, and `research/04-session-43582de1.md`, section 6.3 (or `research/evidence-deck.md:511,621`) to the CI clause. |
| 6 | MINOR | 7.2 source line (:661) | The sentence says the five per-advocate final orders in the table above are "repeated at `return-contract.md:24`". That line repeats only the displayed order and the two pair tallies, not the five advocate orders. `merged-root-cause-analysis.md:37-43` does repeat them. | Replace with "displayed order and pair tallies also at `return-contract.md:24`", or drop the reference. |
| 7 | MINOR | 6 Option E Debate record (:602) | The quoted phrase "more direct for its two retained blockers, but narrower overall" is credited to three advocates (`:265; :304; :344`). The words appear only at :265. :304 says "more decisive ... but narrower". :344 says "this is a narrower judgment ... V5 overrides it decisively", which supports the position in substance but not the quoted words. | Credit the exact quote to :265 only, and cite :304 and :344 as agreeing in substance, without quotation marks. |

### Summary
- Total findings: 7
- Critical: 0
- Important: 2
- Minor: 5
- Verdict: FAIL

### Confidence Gate
- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 22 | Grep: 0 (searches ran through Bash) | Glob: 0 | Bash: 15. Read + Bash = 37, which exceeds the 7 checklist items.
- UNCHECKED items: none. UNVERIFIABLE items: none.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None. No Inherited Structural Verdict was supplied. The 10.10 "Pass" claims (:1255-1263) were tested, not relied on, and three of them failed (Findings 2 and 4 for the gap-to-step map, and indirectly Finding 1 for "current-rule citations name the exact layer").

**(b) Independent semantic checks:**
- **Gap-to-step chain:** read all 12 Section 4 rows, every Section 8 row and all 20 Section 9 questions, then grepped Section 8 for the persisted-summary condition (no match). Basis for Finding 2.
- **Debate-citation chain:** read `ADV/debate-transcript.md:40-219` (Round 1) and `:240-489` (Round 2, convergence and ordering), plus `return-contract.md` (full), `merged-root-cause-analysis.md` (full), `refactor-plan.md:1-40`, `invariant-probe.md:1-76`, `diff-analysis.md:1-75`, `base-selection.md:1-8,148-172`, `plan-review-evidence.md:14-18`, `qa/adversarial-post-merge-validation.md:116-122` and `reviews/adversarial/run-evidence.md:12-18`. Every Section 6 and 7 debate anchor matched except Findings 6 and 7.
- **Current-rule citations:** used `sed`, `grep` and `git show` on the checkout working tree, HEAD, the parent of `c6009cd3` and the installed copies of `qa.md`, `managed-workspace.md`, `quality-gates.md` and `retry.md`, plus `git log` of those sources since 2026-10-22. `qa.md:82` and `quality-gates.md:24-41` support their claims in both copies. `managed-workspace.md:42` and working-tree `retry.md:142-146` do not (Findings 1 and 3).
- **Evidence-deck bindings:** read `research/evidence-deck.md:10-169,270-429,486-670,672-901` and checked gap-row and Options citations (:244, 280, 312, 350, 378-391, 389, 505, 547, 551, 564-569, 585-598, 608-668, 683, 709, 724-731, 823, 858-862). All support their claims.
- **Case-report anchors:** read `research/01-session-ac2cd1fd.md:55-110,286-341`, `research/06-session-0690ee9f.md:150-269`, the section headings of cases 02-05 and `research/03-session-6f744b87.md:156-180`. They confirm record numbers 485-486, 498/503/506, 946 and 2028, the nested agent IDs (abd76ef…, a6d8fbaf…, acf0a51e…, af349dd5…, a4bfff37…) and the section numbers the report cites. They also expose Finding 5.
- **Gap register:** read `gaps-and-questions.md` in full. Confirms the :11, :29-35, :53-59 and :56 bindings.
- **Zero-issue check:** not applicable, because the verdict is FAIL with tool-backed findings. Items marked PASS (b, c, d, g) were each tested with the citations listed above, not assumed.

**Web research:** none performed; no external lookup was needed, so Tavily and the fallbacks were not invoked.

## QA Complete

---

| Status | Result |
|---|---|
| DONE | Reviewed all 1,263 report lines against the debate artifacts, the evidence deck, the case reports, the gap register and the protocol sources (both copies and git history). Verdict FAIL: 7 findings, 2 IMPORTANT and 5 MINOR. |
| NEXT | Save this report at /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-lens-crossref-chain.md, then carry Findings 1-7 into the Step 6.17 consolidation. |