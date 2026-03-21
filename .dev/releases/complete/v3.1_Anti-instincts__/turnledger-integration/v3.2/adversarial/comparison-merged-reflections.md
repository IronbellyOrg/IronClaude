# Adversarial Comparison: v3.2 Merged Reflections

**Date**: 2026-03-20
**Document A**: `adversarial/reflect-merged.md` (session A merge)
**Document B**: `adversarial/reflection/merged-reflection.md` (session B merge)
**Ground truth**: `tasklist.md` (28 tasks, 7 waves) + `adversarial/merged-output.md` (3-plan adversarial merge)

---

## Per-Dimension Scoring

### S1: Gap Detection Completeness (x2.5)

**Doc A**: 6/10

Doc A identifies only one real gap (CF-2: Section 6.1 `emit_report()` signature mismatch) and rates everything else as fully covered with zero gaps. Cross-checking against the tasklist and merged plan reveals several real issues Doc A missed:

- **V05 editing anti-pattern**: V05 (a verify task) is tasked with updating `estimated_scope` frontmatter -- a spec edit, not a verification. Doc A does not flag this process anti-pattern at all.
- **Section 4.3 buried in T06**: T06's section header says "Section 6.3 Gate Contract" but its description also modifies Section 4.3's report format example. This dual-section edit is noted in CF-8 but only as "acceptable," not as a risk that executors might miss the 4.3 edit. The gap is that the task header does not surface Section 4.3.
- **Intra-wave ordering documentation**: Doc A notes intra-wave dependencies in CF-4 as "correct" but does not flag that the wave structure is misleading to executors who assume full parallelism within waves. No recommendation to document ordering constraints.
- **Acceptance criteria vagueness**: Doc A states all tasks are HIGH fidelity (CF-3) without flagging any vague acceptance criteria (V01 "no contradictions" is subjective; T09 "all 6 items" not enumerated; T07 diagram format unspecified).

Doc A does catch the Appendix A stale reference (DF-1) and T02 cross-section relocation (DF-2), both valid low-severity findings. It also correctly identifies the CLI argument parser concern (DF-3) from Agent B. However, the overall false-negative rate is high -- it misses 3 Medium-severity gaps.

**Doc B**: 8/10

Doc B identifies 8 gaps (3 Medium, 5 Low), covering substantially more ground:

- G1 (Section 4.3 buried in T06) -- real, Medium. Verified: T06 header says "Section 6.3" but description edits Section 4.3.
- G2 (V05 editing anti-pattern) -- real, Medium. Verified: V05 description line 297 includes "Update spec frontmatter: `estimated_scope`" -- this is an edit, not a verify.
- G3 (Section 6.1 `emit_report()`) -- real, Medium. Same as Doc A's CF-2.
- G4-G8 (migration authoring, BC-5, rationale, constant location, IE-4 risk signal) -- all valid Low findings.

Doc B also identifies 6 vague acceptance criteria (AC-1 through AC-6) and 3 dependency issues (DEP-1 through DEP-3). Cross-checking against the tasklist confirms all are real. The only weakness is that Doc B does not flag Doc A's Appendix A stale reference or T02 relocation concern, but these are genuinely Low severity.

### S2: Actionability of Findings (x2.0)

**Doc A**: 7/10

Doc A's action items are concrete and well-structured. Action Item 1 (V03 check for `emit_report()`) specifies exactly what to add and where. Action Items 3 and 4 give precise text to add to task descriptions. Action Item 5 (adjust parallelism estimate) gives the corrected value. However, several action items are vague about implementation: "Add a note to T16's description" and "Add a note to T02's description" specify the content but not the precise location within the task. More critically, Doc A only produces 5 action items total, missing the higher-impact V05 and T06 header fixes entirely.

**Doc B**: 9/10

Doc B's 7 prioritized action items are highly specific:
- Action 1: "Add explicit edit task for Section 6.1 `emit_report()` signature" -- specifies both merged plan and tasklist need updating.
- Action 2: "Promote `estimated_scope` from V05 to an edit task" -- specifies Wave 5 or T12 scope.
- Action 3: "Document intra-wave ordering constraints" -- lists the exact 3 dependency pairs.
- Action 4: "Elevate T06 section header to include Section 4.3" -- precise directive.
- Action 5: "Tighten 6 vague acceptance criteria" -- references AC-1 through AC-6 with specific fixes.
- Actions 6-7: Wave optimizations and BC-5 content creation.

Doc B also provides a proposed optimized wave structure (7-wave to 7-wave restructure) that an executor could adopt directly. The only deduction is that the wave restructure is somewhat aggressive (collapsing V01 into Wave 2 changes the verification model) without fully analyzing risk.

### S3: Evidence Rigor (x2.0)

**Doc A**: 7/10

Doc A cites specific evidence for most findings: "spec line 638" for `emit_report()`, "spec line 963" for Appendix A, "lines 572-576 in Section 4.5" for T02. Each consensus finding cites both agents' positions. However, the divergent findings section lacks task ID specificity in places -- DF-3 references "IE-7" from the merged plan but does not cite the specific merged plan line or section. The resolved contradictions section is thin ("No direct contradictions were found") despite the merged plan containing 4 explicit contradictions that the source agents should have evaluated differently.

**Doc B**: 8/10

Doc B uses structured tables with Source columns (Agent A / Agent B / Both) for every finding, making provenance traceable. Gap IDs (G1-G8), dependency IDs (DEP-1 through DEP-3), and acceptance criteria IDs (AC-1 through AC-6) are all cross-referenced. The IE coverage table maps each interaction effect to specific tasks. However, Doc B does not cite spec line numbers as frequently as Doc A -- it references task IDs and section numbers but fewer raw line references. The disagreement resolutions (D1-D7) cite both agents' positions with clear winner declarations.

### S4: Contradiction Resolution Quality (x1.5)

**Doc A**: 5/10

Doc A's "Resolved Contradictions" section states: "No direct contradictions were found between the two agents." This is problematic. While the two reflection agents may not have directly contradicted each other, the merged plan they were reflecting on contained 4 explicit contradictions (Section 6.3 frontmatter handling, models.py LOC, tasklist structure, Section 3.3 changes). A merged reflection should evaluate whether the tasklist correctly resolved those upstream contradictions. Doc A does address DF-5 (where to add `emit_report()` clarification) as a divergent recommendation and picks Agent B's approach with reasoning, which is good. But the overall treatment of disagreements is shallow.

**Doc B**: 8/10

Doc B identifies 7 disagreements (D1-D7) between the source agents and resolves each with explicit winner declarations and reasoning:
- D1: Agent A wins on Section 6.1 gap (with evidence).
- D3: Agent B wins on IE-5 coverage (distinguishing mechanical vs. risk-signal coverage).
- D4: Agent B wins on intra-wave ordering (the strongest resolution -- correctly identifies that wave grouping is misleading).
- D5: Agent A wins on T10 wave placement.
- D6: Reconciles different gap counts as different granularity levels.
- D7: Merges complementary acceptance criteria findings.

Each resolution cites specific evidence. The only weakness is D2 (BC-5), where the resolution is somewhat hand-wavy ("Agent A is more specific; Agent B's framing is broader but correct").

### S5: Risk Calibration (x1.0)

**Doc A**: 7/10

Doc A's risk calibration is mostly appropriate:
- CF-2 (`emit_report()` gap) rated MEDIUM and marked Blocking in action items -- proportionate.
- CF-5 (T11 highest risk) -- correct given T11's 8 discrete changes and cross-section dependencies.
- DF-1 (Appendix A) rated LOW -- correct, Appendix A is forensic.
- DF-3 (CLI argument parser) rated ADVISORY -- correct, Beta confirms no CLI flags exist.

However, Doc A under-alarms on the V05 editing anti-pattern (not flagged at all) and the T06 buried section (flagged as "acceptable" rather than as a risk). The "PASS WITH NOTES" verdict is appropriate but the "Blocking" classification of Action Item 1 while everything else is Advisory/Recommended creates a slightly skewed risk profile -- the intra-wave ordering issue arguably has more blast radius than the `emit_report()` signature.

**Doc B**: 8/10

Doc B's severity assignments are well-calibrated:
- 3 Medium gaps (G1 T06 header, G2 V05 anti-pattern, G3 `emit_report()`) -- all proportionate. These are items that could cause executor confusion or spec inconsistency but would be caught by verification tasks.
- 5 Low gaps -- all correctly classified as items with minimal blast radius.
- "0 Blocking issues" verdict -- appropriate. None of the gaps would cause a failed sprint.
- DEP-1 through DEP-3 all marked as transitively satisfied with no functional risk -- correct.

The only slight over-alarm is the proposed wave restructure, which is more aggressive than the findings warrant (collapsing V01 changes the verification checkpoint model without discussing the tradeoff).

### S6: Structural Clarity (x1.0)

**Doc A**: 8/10

Doc A has clear structure: Consensus Findings (CF-1 through CF-9), Divergent Findings (DF-1 through DF-5), Resolved Contradictions, Final Verdict, Action Items. The verdict is easy to find ("PASS WITH NOTES" with bold). Action items are numbered with severity labels. Each finding has a clear assessment paragraph.

Weaknesses: The consensus section is verbose -- 9 consensus findings when many could be condensed (CF-3 "all HIGH fidelity" and CF-6 "risk rankings aligned" are the same type of observation). The DF-5 finding (where to add clarification) is a meta-disagreement about recommendations, not a finding about the tasklist, which muddies the structure slightly.

**Doc B**: 9/10

Doc B uses structured tables throughout (Confirmed Gaps, Dependency Issues, Acceptance Criteria Issues, Wave Optimization, IE Coverage), making it scannable. The Agreement Summary is a compact numbered list (11 items). Disagreements are clearly labeled D1-D7 with bold "Resolution" and winner declarations. The final verdict section has a clear priority-ordered action list with severity labels and a "Bottom line" summary.

The proposed optimized wave structure is a strong addition -- it gives the executor a concrete alternative rather than just identifying problems. The IE coverage table with COVERED/PARTIALLY COVERED status is immediately actionable.

Minor weakness: The document lacks a single bold "PASS" or "FAIL" verdict line at the top -- the verdict is at the bottom under "Final Verdict" with "Overall confidence: HIGH" rather than a clear pass/fail.

---

## Score Summary

| Dimension | Weight | Doc A | Doc B | Doc A Weighted | Doc B Weighted |
|-----------|--------|-------|-------|----------------|----------------|
| S1 Gap Detection | x2.5 | 6 | 8 | 15.0 | 20.0 |
| S2 Actionability | x2.0 | 7 | 9 | 14.0 | 18.0 |
| S3 Evidence Rigor | x2.0 | 7 | 8 | 14.0 | 16.0 |
| S4 Contradiction | x1.5 | 5 | 8 | 7.5 | 12.0 |
| S5 Risk Calibration | x1.0 | 7 | 8 | 7.0 | 8.0 |
| S6 Structural Clarity | x1.0 | 8 | 9 | 8.0 | 9.0 |
| **TOTAL** | | | | **65.5** | **83.0** |

---

## Strengths & Weaknesses

### Document A Strengths
- Catches the Appendix A stale reference (DF-1) that Doc B misses entirely -- a genuine, albeit low-severity, real finding with concrete evidence (spec line 963).
- Catches T02's cross-section relocation nature (DF-2) -- useful executor context that Doc B does not surface.
- The consensus-first structure clearly communicates where both agents agreed, which builds confidence in the shared findings.
- Line-number citations are specific and verifiable (spec lines 638, 963, 572-576, 546-569).
- Action Item 1 (V03 check) is the single most important fix and is described with precision.

### Document A Weaknesses
- Misses 3 Medium-severity gaps (V05 anti-pattern, T06 buried header, intra-wave ordering) that Doc B correctly identifies. This is the most significant weakness -- a merged reflection that declares "full coverage -- no true gaps" when real gaps exist fails its primary function.
- "No direct contradictions" assertion is incorrect at the reflection-merge level. The source agents clearly disagreed on gap count, intra-wave severity, IE-5 coverage, and T10 placement. These are contradictions that should have been resolved with winner declarations.
- Over-reliance on the "both agents agree" framing masks gaps where both agents missed the same issue (V05 anti-pattern appears to have been missed by both source agents too, but a strong merge should cross-check against the tasklist independently).
- Only 5 action items versus Doc B's 7 priority-ordered items with supporting tables.
- The parallelism estimate correction (Action Item 5) is the weakest item -- cosmetic and at the bottom, yet it occupies the same structural position as real fixes.

### Document B Strengths
- Catches all 3 Medium-severity gaps that Doc A misses (G1 T06 header, G2 V05 anti-pattern, G3 `emit_report()`).
- Structured tables (Gaps, Dependencies, Acceptance Criteria, Wave Optimization, IE Coverage) make findings scannable and countable -- an executor can immediately see "8 gaps, 3 dependency issues, 6 AC issues, 4 wave optimizations."
- Strong contradiction resolution: 7 disagreements explicitly resolved with winner declarations and evidence-backed reasoning (D1-D7).
- Proposed optimized wave structure gives the executor a concrete alternative, not just problems.
- Priority-ordered action items with clear severity labels and "Bottom line" summary.
- The IE coverage table with per-IE status (COVERED / PARTIALLY COVERED) directly supports T18 validation.

### Document B Weaknesses
- Misses Doc A's Appendix A stale reference and T02 relocation findings -- both valid, low-severity.
- The proposed wave restructure (collapsing V01 into Wave 2) is presented without sufficient risk analysis -- V01 as a standalone wave serves as a verification checkpoint, and removing that checkpoint changes the execution model.
- Does not cite raw spec line numbers as frequently as Doc A -- findings reference task IDs and sections but fewer grounding line references.
- The "Quick compare + merge" depth label undersells the actual depth of analysis performed.
- The "0 Blocking issues" classification may under-alarm slightly -- G3 (`emit_report()` signature) is arguably blocking since it represents a gap in the merged plan itself that could propagate to the final spec.

---

## Winner & Justification

**Document B wins (83.0 vs 65.5).**

The decisive factor is S1 (Gap Detection Completeness), where Doc B outperforms by a full 5 weighted points. Doc A's assertion of "full coverage -- no true gaps" is its critical failure: it misses the V05 editing anti-pattern (a verify task making spec edits), the T06 buried section header (executor could miss the Section 4.3 edit), and the lack of intra-wave ordering documentation (executors would assume full parallelism). All three are real Medium-severity issues verified against the tasklist.

Doc B also substantially outperforms on S4 (Contradiction Resolution), identifying and resolving 7 source-agent disagreements with winner declarations, while Doc A claims "no contradictions" despite clear divergences in the source material.

An executor working from Doc B would produce a better refactored spec because they would: (1) fix the V05 anti-pattern before execution, (2) surface Section 4.3 in T06's header, (3) document intra-wave ordering, (4) tighten 6 vague acceptance criteria, and (5) have a concrete optimized wave structure to consider. An executor working from Doc A would miss all of these and proceed with false confidence in the tasklist's completeness.

Doc A's unique contributions (Appendix A stale reference, T02 relocation context) are valid but Low severity -- they would not materially change the refactoring outcome. The ideal merged reflection would combine Doc B's gap detection and structural rigor with Doc A's line-number specificity and Appendix A finding.
