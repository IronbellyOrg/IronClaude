---
artifact: refactor-plan
pipeline: sc:adversarial
date: 2026-03-20
base_variant: V3
---

# Refactoring Plan

Base: V3 (v3.2 Wiring Verification Gate)
Donors: V1 (v3.05 Deterministic Fidelity Gates), V2 (v3.1 Anti-Instincts Gate)

---

## 1. Incorporations from Non-Base Variants

### INC-01: Cost Constant Calibration Framework (from V1)

**Source**: V1 Section 3, NR-3. Unique contribution U-001 (debate score: 9/10).

**Target location in V3**: New subsection under Section 4.5 (Sprint Integration), after the SprintConfig field replacement discussion.

**Rationale**: The debate transcript notes (U-001 assessment): "No other proposal provides specific numeric values for budget calibration. Without these constants, TurnLedger integration is abstract." V3 references `WIRING_ANALYSIS_TURNS=1` but does not provide the broader calibration framework that V1 establishes. Adding V1's cost constant pattern (module-level integers, not config fields, with MIN/STD/MAX derived budgets) gives V3 the same calibration rigor.

**Integration approach**: Adapt V1's NR-3 acceptance criteria to wiring-gate-specific constants. V1's constants are convergence-specific (CHECKER_COST=10, REMEDIATION_COST=8, etc.), so the values change but the pattern (module-level integers with derived budget ranges) transfers directly.

**Risk level**: Low. Additive content that does not conflict with any existing V3 section.

---

### INC-02: Dual-Guard Invariant Pattern (from V1)

**Source**: V1 Section 4, CONFLICT-1 resolution. Unique contribution U-002 (debate score: 8/10).

**Target location in V3**: Section 7 (Risk Assessment), as a new invariant note following the existing R1-R6 risks.

**Rationale**: Debate transcript (U-002 assessment): "The insight that loop cap and turn budget are independent guards with different failure modes (structural vs. economic) is architecturally important. This pattern should be adopted in V3's wiring gate as well." V3's wiring gate has an analogous dual guard: `wiring_gate_enabled` (structural) and `ledger.can_run_wiring_gate()` (economic). Making this explicit prevents confusion about which guard terminates execution.

**Integration approach**: Add a paragraph documenting the dual-guard invariant for the wiring gate: the enabled flag and the ledger budget guard are independent. Neither subsumes the other. The flag prevents construction; the budget guard prevents execution when funds are insufficient. Both must pass for analysis to proceed.

**Risk level**: Low. Documentation-only addition.

---

### INC-03: Pipeline Separation Analysis (from V2)

**Source**: V2 Section 7 ("Items in TLD That Do NOT Affect AIG"). Unique contribution U-003 (debate score: 9/10).

**Target location in V3**: New Section 7.5 (or appended to Section 7), titled "TurnLedger Sections That Do Not Affect Wiring Gate".

**Rationale**: Debate transcript (U-003 assessment): "V2's Section 7 is the only boundary analysis that explicitly maps which TLD sections are sprint-only. This prevents over-integration." V3 does not have an equivalent boundary map. Adding one prevents implementers from over-integrating TLD sections that are irrelevant to the wiring gate.

**Integration approach**: Adapt V2's table format listing TLD sections and their non-impact rationale. Replace AIG-specific entries with wiring-gate-specific entries. The TLD sections that are sprint-only (Sections 2.1-2.3 debit/credit call sites for other gates, Section 4 DeferredRemediationLog, Section 5 GateKPIReport base) apply equally to the wiring gate context but the reasoning differs.

**Risk level**: Low. Additive boundary documentation.

---

### INC-04: Enforcement Tier Dual-Mode Semantics (from V2)

**Source**: V2 Section 5, RESOLUTION for CONFLICT-01. Debate winner on C-002 (70% confidence).

**Target location in V3**: Section 6.3 (Gate Contract), following the Conflict C2 resolution on enforcement_mode frontmatter.

**Rationale**: Debate transcript (C-002): "V2's proposal that `enforcement_tier` is an intrinsic gate property while `gate_rollout_mode` is a runtime override is the cleanest separation of concerns. This applies across all gates, not just anti-instinct." V3 addresses the enforcement_mode frontmatter label but does not articulate the intrinsic-vs-runtime distinction. Adding V2's framing strengthens V3's architectural clarity.

**Integration approach**: Add a note to V3's C2 resolution stating that `enforcement_mode` in the frontmatter reflects the effective runtime mode (TRAILING -> "shadow", BLOCKING -> "full"), while the gate definition's enforcement tier is an intrinsic property. Reference V2's dual-mode proposal for architectural consistency across all gate definitions.

**Risk level**: Low. Clarifying note, no structural change.

---

### INC-05: Remediation Retry Model Distinction (from V2)

**Source**: V2 Section 5, RESOLUTION for CONFLICT-02. Debate winner on C-006 (72% confidence) and X-001 (65% confidence).

**Target location in V3**: Section 4.5b (NEW-2: Remediation Path), as a clarifying paragraph.

**Rationale**: Debate transcript (C-006): "V2's distinction between gate-check retry and upstream-subprocess retry is an architectural insight that prevents misimplementation across all specs." V3 describes `attempt_remediation()` but does not clarify what remediation retries. For the wiring gate, remediation retries the task subprocess (re-generates the code), then re-evaluates the gate -- not retry the deterministic gate check itself.

**Integration approach**: Add a paragraph to V3's remediation path section (NEW-2) explicitly stating: "Remediation via `attempt_remediation()` re-runs the upstream task subprocess that produced the failing artifact, then re-evaluates the wiring gate on the new artifact. It does not retry the gate check on the same artifact, as wiring analysis is deterministic given identical input."

**Risk level**: Low. Clarifying content.

---

### INC-06: GateCriteria Canonical Location (from V2)

**Source**: V2 Section 5, RESOLUTION for CONFLICT-04. Debate winner on C-003 (65% confidence) and X-002 (80% confidence).

**Target location in V3**: Section 11 (Dependency Map), as an added dependency note.

**Rationale**: Debate transcript (X-002): "V2 provides the most explicit analysis (CONFLICT-04) and resolution (confirm `GateCriteria` in `pipeline/gates.py`). V3 implicitly agrees." V3's dependency map shows new edges but does not confirm the canonical type location. Making this explicit prevents future confusion.

**Integration approach**: Add a note to V3's Section 11 confirming: "`GateCriteria`, `SemanticCheck`, and `gate_passed()` are canonically defined in `pipeline/gates.py`. Gate instances (e.g., `WIRING_GATE`) are defined in `roadmap/gates.py` and import their types from `pipeline/gates.py`."

**Risk level**: Low. Architectural clarification.

---

### INC-07: Line-Level Evidence Citations (from V1)

**Source**: V1 Section 4, per-conflict Evidence subsections. Debate winner on S-002 (60% confidence).

**Target location in V3**: Section 4 (Risks and Conflicts), applied to each conflict C1-C5.

**Rationale**: Debate transcript (S-002): "V1's Evidence + Severity + Resolution structure per conflict is the most thorough. V1's line-level citations provide better traceability." V3's conflicts have severity labels but lack line-level evidence citations. Adding specific line/section references to the source spec and design.md improves traceability.

**Integration approach**: For each of V3's conflicts C1-C5, add an "Evidence" line citing the specific section and line reference in both the original spec and design.md. Follow V1's pattern: "Evidence in spec: [section, line]. Evidence in design: [section, line]."

**Risk level**: Low. Additive detail.

---

### INC-08: DeferredRemediationLog Awareness (from V2)

**Source**: V2 Section 3.3 (New Section 8.5). Unique contribution U-005 (debate score: 5/10).

**Target location in V3**: Section 4.5b (NEW-2: Remediation Path), as a brief note.

**Rationale**: Although scored lower (5/10), the DeferredRemediationLog concept is relevant to V3's remediation path. When a wiring gate fails in BLOCKING mode and remediation is exhausted, the failure should be recorded in a persistent journal for resume recovery. V3 mentions `attempt_remediation()` but does not describe what happens to unresolved failures.

**Integration approach**: Add a note stating that unresolved wiring gate failures (after exhausted remediation attempts) are recorded in `DeferredRemediationLog` for cross-phase persistence, resume recovery via `--resume`, and KPI feed. Keep it brief -- this is a pointer to TLD Section 4, not a full specification.

**Risk level**: Low. Reference note only.

---

## 2. Base Weaknesses Addressed by Non-Base Variants

### WEAK-01: No Budget Calibration Framework

**Weakness in V3**: V3 uses `WIRING_ANALYSIS_TURNS=1` as a single constant but does not provide MIN/STD/MAX budget ranges or a calibration methodology.

**Addressed by**: V1's NR-3 (INC-01 above).

**Fix approach**: Adapt V1's cost constant pattern. Define wiring-specific constants (WIRING_ANALYSIS_TURNS, WIRING_REMEDIATION_TURNS, MIN_WIRING_BUDGET, STD_WIRING_BUDGET, MAX_WIRING_BUDGET) as module-level integers with documented derivation.

---

### WEAK-02: No Pipeline Boundary Map

**Weakness in V3**: V3 does not identify which TLD sections are irrelevant to the wiring gate, risking over-integration.

**Addressed by**: V2's Section 7 (INC-03 above).

**Fix approach**: Add a boundary table modeled on V2's format.

---

### WEAK-03: Remediation Target Ambiguity

**Weakness in V3**: V3 describes `attempt_remediation()` but does not clarify whether it retries the gate check or the upstream subprocess.

**Addressed by**: V2's CONFLICT-02 resolution (INC-05 above).

**Fix approach**: Add clarifying paragraph to remediation section.

---

### WEAK-04: No Dual-Guard Documentation

**Weakness in V3**: V3 has two independent guards (enabled flag + budget guard) but does not document their independence as an invariant.

**Addressed by**: V1's CONFLICT-1 resolution (INC-02 above).

**Fix approach**: Add invariant documentation to risk section.

---

## 3. Changes NOT Being Made

### REJ-01: V2's Table-Driven Format for Diff Summary

**Source**: V2's 3-column comparison (Current/Impact/Verdict) format.

**Rationale for rejection**: V3's hybrid format (Status tables + inline prose) was selected as the base. While V2's format won S-001 at 65% confidence, reformatting V3's entire diff summary to V2's table structure would require restructuring the entire document. The marginal improvement in scannability does not justify the restructuring cost, especially since V3's hybrid approach was noted in the debate as inheriting advantages of both formats.

---

### REJ-02: V1's Narrative-Only "What stays / What changes / What's new" Format

**Source**: V1's Section 1 narrative structure.

**Rationale for rejection**: V1's narrative format lost to V2's table format (S-001) and V3's hybrid is a functional compromise. Converting V3 to V1's format would lose the table scannability.

---

### REJ-03: V2's Graduated Rollout as a Separate New Section (Section 13.1)

**Source**: V2's proposed Section 13.1 (Sprint Pipeline Rollout). Unique contribution U-004 (debate score: 6/10).

**Rationale for rejection**: V3 already handles rollout via the three-field SprintConfig form (Section 8) with config-only phase transitions. V2's Section 13.1 is specific to anti-instinct gate rollout in the roadmap pipeline, which is V2's domain. The wiring gate rollout is already well-covered in V3. Adding a separate rollout section would duplicate content.

---

### REJ-04: V2's DeferredRemediationLog as a Full New Section (Section 8.5)

**Source**: V2's proposed Section 8.5. U-005 (debate score: 5/10).

**Rationale for rejection**: A full section specification of DeferredRemediationLog would exceed V3's scope (wiring gate integration). A brief note pointing to TLD Section 4 is sufficient (see INC-08). The remediation log is TLD infrastructure, not wiring-gate-specific content.

---

### REJ-05: V1's Per-Convergence TurnLedger Construction Model

**Source**: V1's NR-1 (TurnLedger constructed per-convergence-invocation).

**Rationale for rejection**: Debate transcript (C-001): "V3's per-task threading is more composable. Multiple gates can share a single ledger without per-feature construction logic." V3's model (ledger threaded through executor, shared across tasks) won on composability. V1's per-invocation model is correct for convergence but does not generalize.

---

### REJ-06: V1's Conservative Reimbursement Option (separate convergence_credit_rate)

**Source**: V1 Section 4, CONFLICT-4, option 2.

**Rationale for rejection**: V3 already proposes accepting the 1-turn cost at default settings with documentation. Introducing a separate credit rate field adds configuration complexity without solving the fundamental `int(1*0.8)=0` problem for single-turn operations. The debate awarded V3 the win on C-004 (70% confidence) for identifying the bug concretely.
