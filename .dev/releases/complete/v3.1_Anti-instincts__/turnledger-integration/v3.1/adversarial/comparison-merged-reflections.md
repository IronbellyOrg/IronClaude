# Adversarial Comparison: v3.1 Merged Reflections

> **Date**: 2026-03-20
> **Document A**: `adversarial/reflect-merged.md` (Session 1)
> **Document B**: `adversarial/reflection/merged-reflection.md` (Session 2)
> **Ground truth**: `tasklist.md` (22 tasks, 6 waves), `adversarial/merged-output.md`

---

## Per-Dimension Scoring

### S1: Gap Detection Completeness (x2.5)

**Doc A**: 5/10 -- Doc A reports "Complete Coverage -- No Gaps" as a consensus finding, stating both agents verified every merged-plan edit has a corresponding task. This is correct for edit-to-task mapping but misses a critical class of gap: design commitments in the merged plan that are not edits but still need to materialize as spec text. Specifically, backward compatibility notes 4, 5, 8, and 9 (staging, execution order, SprintGatePolicy activation, TurnLedger migration) are documented in the merged plan's "Migration / Backward Compatibility Notes" section but no tasklist task creates spec text for them. Task 021 verifies they are "explicitly stated or implied," but for notes 4, 5, 8, and 9, they are neither -- they exist only in the merged plan, not in any task's edit scope. Doc A also missed interaction effects 3 and 7 having no dedicated edit tasks. Doc A did catch valid divergences (D-1 through D-8), but the "zero gaps" headline is a false negative on the most consequential finding.

**Doc B**: 8/10 -- Doc B's Agent B identified three genuine coverage gaps (GAP-1: backward compatibility notes 4/5/8/9, GAP-2: interaction effect 3, GAP-3: interaction effect 7) and the merge correctly awarded the win to Agent B over Agent A's "zero gaps" position. Doc B also produced a complete interaction effects coverage table (10 rows) showing exactly which effects are covered and which are gaps. Doc B further identified three vague acceptance criteria (Tasks 022, 018, 007) that Doc A did not flag as issues. The interaction effects table cross-checked against the merged plan is accurate. Minor deduction: Doc B did not independently verify whether the line number discrepancies it reports (Task 003: "1077-1083" vs "1079-1083") are real -- the tasklist says "1077-1083" and the merged plan says "spec lines 1077-1083," so this may be a false positive if the spec has shifted since authoring.

### S2: Actionability of Findings (x2.0)

**Doc A**: 7/10 -- Doc A's 6 action items are reasonably concrete. Items 1 and 2 specify which tasks to modify and what dependency declarations to add. Item 3 specifies adding a context-loading note. Items 4-6 are advisory with clear directives. However, the action items are limited to dependency hardening and cosmetic fixes because Doc A's gap detection missed the substantive issues. The most impactful action (ensuring backward compatibility notes become spec text) is absent entirely.

**Doc B**: 9/10 -- Doc B's action items are highly specific. The top priority item identifies the exact gap (backward compatibility notes 4, 5, 8, 9), names the specific task to expand (Task 017) or proposes creating Task 017.5, and identifies the target section (Section 14). The dependency issues name exact task pairs (008->002, 010->002, 010->008). The acceptance criteria fixes provide replacement text (e.g., "No verbatim repetition across sections. Same concept uses same term throughout" for Task 022). The interaction effects table provides a complete coverage map with per-row resolutions. Each finding has a clear what/where/how.

### S3: Evidence Rigor (x2.0)

**Doc A**: 7/10 -- Doc A consistently cites both agents with direct quotes (e.g., Agent A: "Every edit specified in the merged plan has a corresponding task in the tasklist. All 10 sections targeted..."). Each divergent finding (D-1 through D-8) attributes to its source agent and provides the counter-position. Task IDs are cited throughout (003, 008, 009, 010, 016, 017). The contradiction resolution (C-1) provides a reasoned analysis. However, Doc A does not cite line numbers from the tasklist or merged plan to anchor its claims, and the "Assessment" paragraphs for divergent findings sometimes rely on architectural reasoning ("the executor is designed to load context files") without citing the specific executor documentation.

**Doc B**: 8/10 -- Doc B provides structured evidence tables with IDs (G-1 through G-3, DEP-1 through DEP-3, AC-1 through AC-3, WO-1 through WO-4). Each disagreement resolution (D-1 through D-5) names the winning agent and provides reasoning. The interaction effects table maps each effect to specific edit tasks and sections. The backward compatibility notes gap (G-1) is grounded in a verifiable claim: "Task 021 cannot verify what was never written." The line number discrepancy finding (D-4) cites specific numbers. However, Doc B does not quote directly from the source agent reflections as consistently as Doc A does -- it summarizes positions rather than quoting them.

### S4: Contradiction Resolution Quality (x1.5)

**Doc A**: 7/10 -- Doc A identifies one explicit contradiction (C-1: "exact content" directive as strength vs weakness) and resolves it with a reasoned argument favoring Agent B's position. The resolution is well-argued: content drift risk from inlining exceeds the risk of executor failure to load files. Doc A also resolves implicit disagreements in D-4 (Task 017 dependencies) and D-5 (Task 010 dependencies) with balanced reasoning. However, Doc A resolves D-1 by downgrading severity from MEDIUM to LOW without fully engaging with Agent A's concern -- the argument that "the executor is designed to load context files" is an assertion about executor behavior, not evidence from executor documentation.

**Doc B**: 8/10 -- Doc B identifies five explicit disagreements (D-1 through D-5) and resolves each with a clear winner declaration and reasoning. D-1 (coverage gaps) is the most consequential: Doc B correctly awards the win to Agent B who found real gaps that Agent A missed. D-3 (vague acceptance criteria) is well-resolved with practical fixes. D-5 (Wave 4 parallelization) awards the win to Agent A for audit trail preservation, which is a sound judgment. The resolutions are consistent and well-reasoned. Minor deduction: D-4 (line number discrepancies) awards the win to Agent B, but the discrepancies may be false positives -- this should have been verified against the actual spec file rather than accepted at face value.

### S5: Risk Calibration (x1.0)

**Doc A**: 6/10 -- Doc A rates everything as "advisory" or "recommended" severity, with nothing above LOW after its own reassessments. The "PASS WITH NOTES" verdict with "no correctness issues" understates the risk of the backward compatibility notes gap. If Task 021 checks for notes that no task creates, that is a verification gap that will produce a false-pass or a confusing failure during execution. Doc A's severity calibration is systematically too low because its gap detection missed the most important finding. The dependency hardening items are correctly rated as low-severity (wave ordering provides the guarantee), and the cosmetic items (source attribution, wave count labeling) are correctly rated as advisory.

**Doc B**: 8/10 -- Doc B correctly identifies the backward compatibility notes gap as the only MEDIUM-severity item and rates everything else LOW. This calibration is accurate: the gap is real but not blocking (the backward compatibility notes are design commitments, not implementation-blocking spec text), and the other issues are genuinely low severity. The "execution-ready with one MEDIUM action" verdict is proportionate. The interaction effects gaps (3 and 7) are correctly rated LOW since they are documentation concerns, not functional gaps. Minor deduction: Doc B could have considered whether the acceptance criteria vagueness (AC-1 through AC-3) might be MEDIUM rather than LOW for verification tasks, since subjective criteria in verification tasks undermine the verification itself.

### S6: Structural Clarity (x1.0)

**Doc A**: 8/10 -- Doc A is well-organized with clear sections: Consensus Findings (9 items), Divergent Findings (D-1 through D-8), Resolved Contradictions (C-1), Final Verdict, and Action Items (6 numbered items with severity labels). The verdict is easy to find. Action items are numbered and each has What/Why/Severity structure. The document flows logically from agreement to disagreement to resolution. Deduction: the 9 consensus findings are somewhat verbose and could have been condensed, and the divergent findings section is long (8 items) without a summary table for quick scanning.

**Doc B**: 9/10 -- Doc B has excellent structure: Agreement Summary (9 bullet points), Disagreements & Resolutions (D-1 through D-5 with clear winner declarations), Merged Findings (4 structured tables: Gaps, Dependencies, Acceptance Criteria, Wave Optimization), Interaction Effects Coverage (10-row table), and Final Verdict with prioritized action list. The tables are immediately scannable. The interaction effects coverage table is a standout feature -- it provides a complete at-a-glance view of coverage status. The verdict section leads with confidence level, total counts, and a priority-ordered action list. Every finding has an ID for cross-referencing.

---

## Score Summary

| Dimension | Weight | Doc A | Doc B | Doc A Weighted | Doc B Weighted |
|-----------|--------|-------|-------|----------------|----------------|
| S1 Gap Detection | x2.5 | 5 | 8 | 12.5 | 20.0 |
| S2 Actionability | x2.0 | 7 | 9 | 14.0 | 18.0 |
| S3 Evidence Rigor | x2.0 | 7 | 8 | 14.0 | 16.0 |
| S4 Contradiction | x1.5 | 7 | 8 | 10.5 | 12.0 |
| S5 Risk Calibration | x1.0 | 6 | 8 | 6.0 | 8.0 |
| S6 Structural Clarity | x1.0 | 8 | 9 | 8.0 | 9.0 |
| **TOTAL** | | | | **65.0** | **83.0** |

---

## Strengths & Weaknesses

### Document A Strengths
- Direct quotes from both source agents throughout, making attribution transparent and verifiable
- Thorough analysis of the "exact content" directive contradiction (C-1) with a well-reasoned architectural argument
- Identified valid findings that Doc B missed: source attribution comments (D-2), line number fragility (D-8), and the Task 016/017 Wave 1 optimization (D-3)
- Clean What/Why/Severity structure in action items

### Document A Weaknesses
- Critical false negative: accepted the "zero gaps" conclusion without verifying backward compatibility notes 4, 5, 8, 9 have creating tasks (not just verification tasks)
- Did not produce a coverage map for interaction effects, missing the gap in effects 3 and 7
- Systematically under-calibrated severity -- everything is advisory or recommended, nothing is MEDIUM or higher
- The 9 consensus findings are verbose; several could be merged (e.g., findings 4 and 5 about dependency graph correctness and Wave 2 parallelism)

### Document B Strengths
- Correctly identified the most important gap in the entire tasklist (backward compatibility notes without creating tasks)
- Produced a complete 10-row interaction effects coverage table that serves as an auditable artifact
- Structured tables (Gaps, Dependencies, Acceptance Criteria, Wave Optimization) enable quick scanning
- Appropriately calibrated severity: one MEDIUM item, remainder LOW, zero blocking
- Identified acceptance criteria vagueness in verification tasks -- a category of issue Doc A entirely missed

### Document B Weaknesses
- Did not verify the line number discrepancy claims (D-4) against the actual spec file -- accepted Agent B's assertion without ground-truth checking
- Did not identify source attribution comments or line number fragility, which are valid (though minor) process improvements
- Summaries of agent positions sometimes lack the direct quotation that Doc A provides, making it harder to verify the merge accurately represented both agents
- The Wave 3 header clarification (WO-4: "parallel, after 011" is misleading for 013->014->015) is valid but was not highlighted as prominently as its impact warrants -- this could cause an executor to run Tasks 014 and 015 prematurely

---

## Winner & Justification

**Document B wins with 83.0 vs 65.0.**

The decisive factor is gap detection (S1). Doc B identified the single most consequential issue in the entire reflection: backward compatibility notes 4, 5, 8, and 9 exist as design commitments in the merged plan but no tasklist task creates corresponding spec text. Task 021 verifies these notes are "explicitly stated or implied," but without a creating task, the verification will either false-pass (accepting implied coverage that does not exist) or fail with no remediation path. This is exactly the kind of finding a reflection report exists to catch, and Doc A missed it entirely.

Doc B's structural advantages (coverage tables, ID-tagged findings, prioritized action list) compound the gap detection advantage by making the findings immediately actionable for an executor. An executor reading Doc B can scan the tables, see "one MEDIUM action before execution," and know exactly what to fix. An executor reading Doc A sees "PASS WITH NOTES, no correctness issues" and proceeds without addressing the backward compatibility notes gap -- a gap that will surface as confusion during Wave 4 verification.

Doc A is not without merit: its direct quotation practice and its identification of source attribution comments, line number fragility, and the Wave 1 optimization are valuable. An ideal merged reflection would combine Doc B's gap detection and structural rigor with Doc A's quotation discipline and minor-finding thoroughness.
