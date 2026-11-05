# QA Report: Report Validation, Internal-Consistency Lens

Persist to: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-lens-internal-consistency.md`. I could not write it myself because report-file writes are prohibited for this agent. This text is the complete report.

## Internal-Consistency QA Report
**Report reviewed:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md` (1,263 lines, last changed 2026-10-24T03:56:00Z)
**Lens:** Internal consistency
**Date:** 2026-10-24
**Phase:** report-validation (`report-lens-internal-consistency`), Task Step 6.3
**Fix authorization:** false. Report only; no file was edited.
**Fix cycle:** N/A
**Governing template:** `/config/.claude/skills/tech-research/SKILL.md:1042-1151`, Lens-Specific QA Agent Prompt Template, Internal-Consistency Checklist at lines 1070-1074.
**Quota note:** The template's "assume at least N errors" line was used as the adversarial stance only. Step 6.3 forbids invented quota findings, so none were added to reach a number.

## Overall Verdict: FAIL

The report is largely consistent: cause names, rankings, tallies, case counts and inventory arithmetic all agree. It still has 4 real defects, all MINOR, and any defect fails this lens.

### Findings
| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|-------------|
| 1 | MINOR | Sections 6, 7 and 10.9 (lines 459, 460, 495, 661, 675, 677, 683, 684, 688, 703, 1201, 1202, 1210, 1211) | Some citations do not resolve under the report's own path rules. Lines 12 and 448 say package-relative paths resolve under the package root and that `ADV/` means `reviews/adversarial/adversarial/`. These lines instead cite bare filenames: `return-contract.md`, `merged-root-cause-analysis.md`, `refactor-plan.md` and `synthesis-gate-decision.md`. None of them is at the package root. `return-contract.md` and `merged-root-cause-analysis.md` are also not under `ADV/`; they are in `reviews/adversarial/`. A reader who carries the `ADV/` prefix forward from the same cell (for example line 460, `ADV/base-selection.md...; merged-root-cause-analysis.md:21`) lands on a file that does not exist. `synthesis-gate-decision.md` is in `phase-outputs/plans/`. I confirmed with `find` that each basename is unique, so a search recovers them, but the report's own convention does not. | Prefix each cited filename: `reviews/adversarial/return-contract.md`, `reviews/adversarial/merged-root-cause-analysis.md`, `ADV/refactor-plan.md` and `phase-outputs/plans/synthesis-gate-decision.md`. |
| 2 | MINOR | Section 2.1 (line 118) vs Section 2.2 (line 147) and Option E (line 596) | The order of the manual-page results is contradicted. Line 118 says "Two `cannot-verify` results after evidence-only resubmission". Line 147 says the first review could not verify rendering before the static-only retry, and only the second result came after it. Line 596 gives the same order (records 430, then 433-434/443, then 450). The source deck puts "after evidence-only resubmission" in the subset label, not on the count (`research/evidence-deck.md:54`). | Change line 118 to: "Two `cannot-verify` results, the second after an evidence-only resubmission, with unchanged text and missing rendering proof." |
| 3 | MINOR | Section 8 Phase 1 (line 801) vs Phase 2 feasibility row (line 850) | Line 801 says "One later row cites a file outside this table", meaning the order-4 row. The Phase 2 row "Check feasibility and correction authority before resubmission" also cites "the three current rendering targets above". Those three Coder files are not in the Verified existing input targets table (lines 803-815); they are in the separate table at lines 830-834. So two rows cite files outside the input table, and the claim "Names in the comparison tables resolve to these exact absolute paths" does not hold for that row. | Change line 801 to say two rows reference files outside this table: the feasibility row names the three verified rendering targets in the table below, and the order-4 row names the debate transcript. |
| 4 | MINOR | Section 2.3 (lines 173, 176-178), Option E (line 603), Section 7.5 (lines 713 and 716) | The report calls these "current checkout" citations, but the checkout changed before assembly. Section 2.3 says it read "directly from the current checkout", and line 716 says the installed managed-workspace pin text "is at line 43", unlike checkout line 42. The checkout switched to branch `fix/retry-citation-line-count` at 2026-10-24T03:42:30Z (`git reflog`), 9 minutes before the 03:51:27Z assembly enumeration. Commit c6009cd3 added one line at checkout `managed-workspace.md:36`. At assembly, checkout line 42 was blank and the pin text was at line 43, the same as the installed copy. So the stated layer difference was false when the report was assembled. Every checkout `managed-workspace.md` anchor after line 36 is off by one: `:42`, `:44-60`, `:60-68`, `:78-85`. Separately, checkout `sc-workflow-protocol/SKILL.md` gained 2 lines at line 28 in the same checkout, so `:48-72` is off by two. `qa.md` and `quality-gates.md` are unchanged. The text was correct when the synthesis components were written; it went stale when it was put into the assembled report under a "current" label. | Either date-stamp these anchors as read from the pre-03:42Z checkout (master `2165ae25`), or re-read the current checkout and update the anchors. Delete or correct the line-716 claim that the two layers differ in pin-line position. |

### Summary
- Total findings: 4
- Critical: 0
- Important: 0
- Minor: 4
- Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Cause IDs, names and ordering match across tables and prose (template a) | PASS | Option A-E headings (lines 478, 506, 533, 560, 587) match card titles in `synthesis/hypothesis-01..05.md:1`. They also match 7.1 (lines 645-649), 7.4, 7.5 and the Options Comparison (lines 613-625). Rank row "2/2/3/3/3, 3/3/2/2/2, 4/4/4/5/5, 5/5/5/4/4" (line 619) matches the 7.2 orders (lines 655-659), `ADV/debate-transcript.md:477-484`, `return-contract.md:24` and `merged-root-cause-analysis.md:37-43`. Writing-point assignments C-004, C-003, C-002, C-007 and C-005 match `ADV/base-selection.md:150`. |
| 2 | Session, incident, review, finding and transition counts agree (template b) | PASS | All counts agree across Sections 2.2, 2.5, 3, 4, 6, 8, 10.1 and 10.2: monitor 7 verdicts, 6 noncompliant and 1 compliant, 5 repairs, 5 reviewers; Orca 16, 14 and 2, 20 items, 13/3 disclosed as superseded; CI 18, 8 and 16 (5 medium, 11 low); credential 8 observations; 3 strict, 1 blocker, 2 planning; 30 slots, 7 synthetic. Checked against case 05 (lines 85 and 493-494: 697, 804, 849, 906, 1021, 1143, 1240), `research/evidence-deck.md:49-58,74-105` and `research/web-01-gap-applicability.md:28-49` (18 rows = 15 deck questions + 3, matching lines 382 and 963). |
| 3 | Section 10 inventory arithmetic | PASS | 258 = 23+10+191+17+9+4+4; 273 and 277 recomputed; 10.6 groups sum to 133+58 = 191. Expanding every 10.6 brace row yields 204 paths, all present on disk. The 3 extra qa files are the ones in 10.9. Later on-disk files are Phase 6 lens outputs written after assembly. All 6 component SHA-256 values in 10.9 match `sha256sum`, and the mtimes match the 01:44Z/03:48Z claim. |
| 4 | Cross-references resolve (template c) | FAIL | Every absolute path and every package-relative path checked exists, and the section anchors exist (case and card headings listed). Failures: findings 1 and 3. |
| 5 | Current and historical descriptions do not contradict | FAIL | Superseding rows in 10.1-10.8 and the 10.9 status table are consistent with `phase-outputs/plans/synthesis-gate-decision.md:17-19,31,66,68`. Failure: finding 4. |
| 6 | Observed endpoint statuses agree | PASS | Endpoints agree across 2.1, 2.2, 4, 7.4, 8 and 9: Orca v4 unreviewed; CI completed not-ready/partial; monitor accepted with 4 defects and `misunderstood`, no eighth review (deck line 322); oracle PASS at 668; render accepted `cannot-verify`; credential pass/archive at 2036. |
| 7 | Recommendation agrees with comparative evidence | PASS | V5 above V4 is the minority side of a 3-2 split. Lines 648, 668-669 and 674-676 disclose this, citing `ADV/refactor-plan.md:32` and `ADV/plan-review-evidence.md:16`. "V1 had the lowest writing score" matches `base-selection.md:150`. Order 4 matches Q1 and the Section 8 row 851; `debate-transcript.md:270` is C-001. |
| 8 | No contradictions within the document (template d) | FAIL | Finding 2. Every other candidate checked held, including record numbers 884/893 (case 05:93,230), 485-486 and 498/503 (case 03:160-176), 2028 (case 06:222), 843/849 (case 01:76), and "six HIGH" (`invariant-probe.md:6-11,69-70`). |

- Checks passed: 4 / 8
- Checks failed: 4
- Issues fixed in-place: 0 (not authorized)

## Self-Audit
- Read the full report in 7 sequential reads covering lines 1-1263, plus Step 6.3 and the lens template.
- Ruled out with tool evidence:
  - The evidence-deck "901 lines" claim: the Read tool shows 901 lines because of the trailing newline.
  - `t10-markdownlint.log` existence: the path exists.
  - The two issue358 packages: 193837 is credential, 210638 is documentation, and the report uses them correctly.
  - The A-001 response vectors at transcript lines 243, 277, 316, 356, 397 and 438.
- Out of lens and not graded: historical artifact names without package paths, such as `t12-review-2.md:20-28`, belong to the evidence-quality lens.

## Confidence and Tool Engagement
- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 0 (searches ran inside Bash) | Glob: 0 | Bash: 21 (read-only grep, sed, find, sha256sum, stat and git log/diff/reflog). No web research.
- UNCHECKED items: none. UNVERIFIABLE items: none.

## Recommendations
Apply the 4 fixes above to the report in one serialized correction pass, then rerun this lens on the corrected report.

| Status | Result |
|---|---|
| DONE | Internal-consistency review of the full assembled report: FAIL with 4 MINOR findings, each tied to exact report lines and source checks. |
| NEXT | Main session saves this report at `qa/qa-lens-internal-consistency.md` with attribution and logs it under Phase 6 Findings. |
| NEXT | One fixer applies findings 1-4, then this lens is rerun. |

## QA Complete