# Adversarial Comparison: v3.05 Merged Reflections

**Date**: 2026-03-20
**Evaluator**: Adversarial Comparison Agent
**Document A**: `adversarial/reflect-merged.md` (12 consensus findings, 9 divergent findings, 3 resolved contradictions)
**Document B**: `adversarial/reflection/merged-reflection.md` (9 agreement items, 6 disagreements, merged findings table)

---

## Per-Dimension Scoring

### S1: Gap Detection Completeness (x2.5)

**Doc A**: 7/10

Doc A identifies 12 consensus findings and 9 divergent findings. Key gaps detected: W5-04 orphan status (CF-2), verification tasks as structural (CF-3), Appendix C traceability gap (CF-4), NFR-2 measurement language (CF-5), W4-03 misnomer (CF-6), W3-03 criterion count discrepancy (DF-1), missing dependencies W3-04->W1-04 (DF-2) and W5-01->W3-06 (DF-3), Wave 5 parallelism inaccuracy (DF-4), W2-02 ambiguity (DF-5), FR-7 subsection ordering (DF-6), W3-03/FR-7.1 contradiction risk (DF-8).

However, Doc A **misses** several real issues that Doc B catches:
- The 5 missing interaction effects (IE-4, IE-5, IE-6, IE-8, IE-9) from Cross-Cutting Notes -- this is a significant coverage gap verified against the merged plan's 9 IEs vs. the tasklist's 4. Doc A never audits IE coverage.
- The W3-03 missing dependency on W3-01/W3-02 (Doc B's DEP-1) -- a real dependency issue where W3-03's acceptance criteria reference `reimburse_for_progress()` and cost constants that W3-01/W3-02 define. Doc A flags only W3-04->W1-04 and W5-01->W3-06 (both advisory), missing the more impactful intra-wave dependency.
- The 3 vague acceptance criteria (W2-01 injection rationale, W5-01 "all debit/credit points", W3-04 cross-refs). Doc A's source Agent A rated all criteria as "specific and verifiable," which is overly generous per ground-truth check: W2-01's AC says "description paragraph present explaining injection rationale" but the merged plan specifies 3 distinct points (caller owns budget, prior consumption, step 9 reservation). Doc A inherited Agent A's blind spot.

**Doc B**: 8/10

Doc B identifies the 5 missing IEs (verified: the tasklist's Cross-Cutting Notes list IE-1, IE-2, IE-3, IE-7 but omit IE-4, IE-5, IE-6, IE-8, IE-9 from the merged plan). This is a concrete, verifiable gap that Doc A entirely misses. Doc B also catches: W3-03->W3-01/W3-02 dependency (DEP-1), 3 vague acceptance criteria, W4-03 section reference inaccuracy, NFR-2 and Appendix C gaps.

However, Doc B **misses** some findings Doc A catches:
- W5-01->W3-06 dependency (Doc A's DF-3) -- the diagram should reflect "subsumes" semantics.
- W3-03 criterion count discrepancy (15 vs. 15+1) -- Doc A's DF-1.
- W3-03/FR-7.1 potential contradiction on criterion #7 scope -- Doc A's DF-8.
- FR-7 subsection ordering concern -- Doc A's DF-6.

Net: Doc B catches the higher-impact gaps (IE coverage, intra-wave dependency, vague ACs) while Doc A catches more numerous but lower-impact findings. Doc B's gap detection is more consequential for execution safety.

---

### S2: Actionability of Findings (x2.0)

**Doc A**: 8/10

Doc A's action items section (9 items) is highly actionable. Each item specifies: what to fix, why (with cross-reference to finding ID), and severity label. Examples:
- "Fix Wave 5 parallelism claim: Amend the Wave 5 header to note that W5-04 must follow W5-03"
- "Add explicit W1-04 dependency to W3-04"
- "Rename W4-03 title: Change 'Section 4.2 (Module Disposition)' to 'YAML Frontmatter -- Module disposition annotations for convergence.py'"

One weakness: some action items are hedged with "Consider" (items 7, 8, 9), reducing directness.

**Doc B**: 9/10

Doc B's action items are exceptionally concrete. The "Recommended Actions Before Execution" section is ordered by priority with specific remediation text:
- "Add missing dependency W3-03 -> W3-01, W3-02" (DEP-1, MEDIUM)
- "Add IE-5 (reimbursement_rate multiple consumers) to Cross-Cutting Notes" (with explanation of why it's highest-priority among missing IEs -- cross-version coordination concern)
- "Tighten 3 acceptance criteria" with exact replacement text: "(a) caller owns budget, (b) prior consumption in steps 1-7, (c) step 9 reservation"
- AC-3 specifies "Change to 'all 7 debit/credit points enumerated in description'"

The specificity of replacement text (not just "fix this" but "change to X") makes Doc B more directly executable.

---

### S3: Evidence Rigor (x2.0)

**Doc A**: 8/10

Doc A consistently cites agent source ("Agent A flagged...", "Agent B noted...") with direct quotes for most findings. Examples:
- CF-8: 'Agent A: "If the replacement text is incorrect or incomplete, both budget systems could run simultaneously (double-charging)."'
- DF-4: 'Agent B flagged that "the Wave 5 header says 'Can execute in parallel' but W5-04 depends on W5-03."'
- CF-6: Both agents quoted with their exact phrasing.

Weakness: Doc A does not cite specific line numbers from the tasklist or merged plan. The merged plan's Edit Summary table and the tasklist's task definitions are referenced by task ID (W3-03, W5-04) but not by line number or section quote.

**Doc B**: 7/10

Doc B uses structured tables with agent positions side-by-side, which provides clear attribution. However, direct quotes from source agents are less frequent. Most findings reference task IDs and concepts rather than quoting source text. The disagreement resolution tables (D1-D6) show both positions but often summarize rather than quote.

Strength: Doc B cites specific merged plan structures (e.g., "the merged plan's completeness assessment flags these, but the 'Sections Unchanged' table lists them as intentionally untouched" -- identifying an internal contradiction in the merged plan itself). This is a stronger form of evidence than agent attribution.

Weakness: The IE coverage audit (agreement item 7) states "Both agents independently identified the same 5 missing IEs (IE-4, IE-5, IE-6, IE-8, IE-9)" but does not quote the agents' exact findings or cross-reference specific lines in the tasklist's Cross-Cutting Notes section.

---

### S4: Contradiction Resolution Quality (x1.5)

**Doc A**: 8/10

Doc A explicitly identifies 3 resolved contradictions (RC-1, RC-2, RC-3) with clear structure:
- RC-1 (W3-03 splitting): Correctly sides with Agent A (no split), noting Agent B called it a "soft recommendation" and the blast radius is low. Reasoning is sound -- the task has clear enumerated acceptance criteria.
- RC-2 (W2-02 ambiguity): Acknowledges both positions have merit, lands on "mildly ambiguous but not blocking" with the acceptance criterion as sufficient gate. Balanced.
- RC-3 (W5-01 risk ranking): Distinguishes between composition difficulty and blast radius axes, correctly prioritizing blast radius for a tasklist review.

Doc A also correctly identifies DF-7 as a FALSE POSITIVE (Agent B's W3-03 splitting recommendation), which is a valuable discrimination.

**Doc B**: 7/10

Doc B identifies 6 disagreements (D1-D6) with resolution tables. Resolutions are generally well-reasoned:
- D1 (W3-03 dependency): Correctly sides with Agent B on MEDIUM severity. Good reasoning about dangling references.
- D4 (Vague ACs): Correctly sides with Agent B, identifying 3 specific underspecified criteria.
- D5 (Section references): Correctly sides with Agent B on W4-03.
- D6 (Wave collapse): Correctly sides with Agent B (keep 6 waves).

Weakness: D2 and D3 are resolved as agreements rather than true contradictions, slightly inflating the contradiction count. The resolutions are less nuanced than Doc A's -- they tend to declare "Agent X wins" without acknowledging the losing agent's valid points as thoroughly.

---

### S5: Risk Calibration (x1.0)

**Doc A**: 7/10

Doc A correctly identifies W2-03 as highest risk (CF-8) and W3-03 as second highest (CF-9), both verified against the tasklist's dependency graph: W2-03 is depended on by W3-01 and W3-05, and its failure (incorrect mutual exclusion language) has the highest blast radius (double-charging). W3-03's 15+1 criteria volume creates numbering error risk.

Doc A rates all findings as "advisory" or "recommended" with none blocking, which aligns with ground truth -- the tasklist has 100% edit coverage and correct wave ordering.

Weakness: Doc A does not quantify cascading failure impact. DF-9 (Agent B's Wave 2 critical path analysis) is noted as "Valid and useful framing" but not incorporated into the risk model. Doc A treats Wave 2 risk atomically (per-task) rather than systemically.

**Doc B**: 8/10

Doc B provides better systemic risk calibration. The IE-5 finding (reimbursement_rate multiple consumers) is correctly rated MEDIUM and prioritized above other missing IEs because it creates a cross-version coordination concern. The dependency issue DEP-1 (W3-03->W3-01/W3-02) is rated MEDIUM based on executor confusion risk, which is proportional -- wave ordering mitigates but doesn't eliminate.

Doc B correctly rates all wave optimization opportunities as NOT RECOMMENDED, avoiding over-optimization of a correctness-critical process.

Doc B's "0 blocking issues" verdict is correct. The distinction between "ready for execution as-is" vs. "improvements, not prerequisites" is well-calibrated.

---

### S6: Structural Clarity (x1.0)

**Doc A**: 9/10

Doc A follows a clear three-part structure: Consensus Findings (CF-1 through CF-12), Divergent Findings (DF-1 through DF-9), Resolved Contradictions (RC-1 through RC-3), Final Verdict, Action Items. Each finding has a consistent format: what each agent said, assessment, verdict with severity label.

The Action Items section is numbered 1-9 with severity labels (recommended/advisory) and "Why" citations. An executor can scan the verdict ("PASS WITH NOTES") and jump directly to the 9 action items.

Minor weakness: The document is long (221 lines). The 12 consensus findings include some that are purely confirmatory (CF-1 "full edit coverage", CF-11 "dependency graph correct") and could be collapsed into a summary table.

**Doc B**: 8/10

Doc B uses a good structure: Agreement Summary (9 items), Disagreements & Resolutions (6 items with tables), Merged Findings (4 categorized tables), Final Verdict (summary table + ordered actions).

The tables (Confirmed Gaps, Confirmed Dependency Issues, Acceptance Criteria Issues, Wave Optimization, IE Coverage) are scannable and well-organized. The Final Verdict table with metrics (total gaps, total issues, blocking issues) is immediately useful.

Weakness: The document lacks severity labels in the agreement section -- the 9 agreement items are listed flatly without indicating which are most important. The disagreement resolution tables use a consistent format but require reading prose to understand the resolution. The "Execution Readiness" paragraph at the end effectively communicates the bottom line.

---

## Score Summary

| Dimension | Weight | Doc A | Doc B | Doc A Weighted | Doc B Weighted |
|-----------|--------|-------|-------|----------------|----------------|
| S1 Gap Detection | x2.5 | 7 | 8 | 17.5 | 20.0 |
| S2 Actionability | x2.0 | 8 | 9 | 16.0 | 18.0 |
| S3 Evidence Rigor | x2.0 | 8 | 7 | 16.0 | 14.0 |
| S4 Contradiction | x1.5 | 8 | 7 | 12.0 | 10.5 |
| S5 Risk Calibration | x1.0 | 7 | 8 | 7.0 | 8.0 |
| S6 Structural Clarity | x1.0 | 9 | 8 | 9.0 | 8.0 |
| **TOTAL** | | | | **77.5** | **78.5** |

---

## Strengths & Weaknesses

### Document A Strengths
- Superior evidence rigor: nearly every finding includes direct agent quotes, making claims verifiable
- Best contradiction resolution: RC-1 (W3-03 split rejection) and DF-7 (false positive identification) demonstrate strong discriminative judgment
- Comprehensive divergent findings catalogue: 9 divergent findings vs. Doc B's 6 disagreements, providing a more complete picture of where the agents differed
- Clear severity labeling on all action items (recommended vs. advisory)

### Document A Weaknesses
- Completely misses the 5 missing interaction effects (IE-4, IE-5, IE-6, IE-8, IE-9) from Cross-Cutting Notes -- this is the single largest coverage gap in either document, verified against ground truth
- Misses the W3-03->W3-01/W3-02 intra-wave dependency, which is more impactful than the advisory dependencies it does catch
- Inherits Agent A's blind spot on acceptance criteria quality, rating all ACs as specific when 3 are demonstrably underspecified
- No systemic risk analysis (Wave 2 as critical path bottleneck)

### Document B Strengths
- Catches the highest-impact gap: 5 missing IEs from Cross-Cutting Notes, verified against the merged plan's 9 IEs vs. tasklist's 4
- Most actionable findings: provides exact replacement text for acceptance criteria fixes (e.g., enumerate 3 injection rationale points, specify count of 7 debit/credit points)
- Better risk calibration: correctly prioritizes IE-5 as highest-priority missing IE due to cross-version coordination concern
- Identifies the merged plan's internal contradiction (completeness assessment vs. "Sections Unchanged" table) on NFR-2 and Appendix C

### Document B Weaknesses
- Misses several lower-impact findings that Doc A catches: W3-03 criterion count (15+1), W5-01->W3-06 dependency, W3-03/FR-7.1 criterion #7 scope ambiguity, FR-7 subsection ordering
- Less rigorous evidence: fewer direct quotes from source agents, more summarization
- Contradiction resolutions are less nuanced -- tends toward binary "Agent X wins" rather than acknowledging valid points from both sides
- Agreement section lacks severity differentiation -- 9 items listed without priority ordering

---

## Winner & Justification

**Document B wins by a narrow margin (78.5 vs. 77.5).**

The deciding factor is gap detection impact. Doc B identifies the three highest-consequence issues that Doc A misses entirely:

1. **5 missing IEs from Cross-Cutting Notes** (verified: IE-4, IE-5, IE-6, IE-8, IE-9 are absent from the tasklist's Cross-Cutting Notes section but present in the merged plan). This is an executor-facing gap -- without these notes, an executor may not monitor critical interaction effects like reimbursement_rate's multiple consumers (IE-5) or the ConvergenceBudget rejection rationale (IE-9).

2. **W3-03->W3-01/W3-02 dependency** (DEP-1). This is a functional dependency within Wave 3 where W3-03's acceptance criteria explicitly reference concepts defined by W3-01 and W3-02. Doc A catches only cross-wave advisory dependencies.

3. **3 underspecified acceptance criteria** with concrete fixes. Doc A's inherited "all ACs are specific" assessment is demonstrably wrong for W2-01 (merged plan specifies 3 points; AC says "paragraph present").

Doc A compensates with superior evidence rigor, better contradiction resolution (especially the false-positive identification on W3-03 splitting), and more comprehensive divergent findings. In a scenario where evidence traceability is paramount (e.g., audit), Doc A would be preferred. But for the immediate purpose -- producing a tasklist ready for `/sc:task-unified` execution -- Doc B's findings would lead to a better-prepared tasklist because it catches the gaps that would actually cause executor confusion or missed coordination.

The optimal outcome would merge Doc B's gap detection and actionability with Doc A's evidence rigor and contradiction resolution quality.
