---
title: "Refactoring Plan — Variant B as Base"
timestamp: 2026-03-18T00:00:00Z
step: 4
protocol: adversarial-debate
base_variant: B (spec2.md)
strengths_to_incorporate: 9
weaknesses_to_fix: 4
changes_rejected: 6
---

# Step 4: Refactoring Plan

## 1. Strengths to Incorporate from Non-Base Variants

### S-001: Insertion Point Rationale (from Variant A, Section 4.2 + 5.3)

- **Source**: Variant A, Sections 4.2 ("Existing precedent for non-LLM post-merge steps") and 5.3 ("Why `_build_steps()` is the correct insertion point")
- **Target location**: Add as a subsection within B's Section 5.6 (Roadmap Pipeline Integration), after "Step 4: Add to `_build_steps()`"
- **Rationale**: A provides two architectural arguments that B lacks: (1) the anti-instinct audit step precedent for deterministic non-LLM steps, and (2) the explicit argument that no dynamic gate registry exists, making `_build_steps()` the only viable insertion point. These strengthen the design justification for reviewers unfamiliar with the codebase.
- **Risk**: LOW. Additive text only, no structural change.

### S-002: Report Body Section Requirements (from Variant A, Section 7.3)

- **Source**: Variant A, Section 7.3 ("Required body sections")
- **Target location**: Add after B's Section 5.4 (Report Format), as a new subsection "5.4.1 Required Body Sections"
- **Rationale**: B specifies frontmatter in detail but does not prescribe the Markdown body structure. A defines 7 required sections: Summary, Unwired Optional Callable Injections, Orphan Modules/Symbols, Unregistered Dispatch Entries, Suppressions and Dynamic Retention, Recommended Remediation, Evidence and Limitations. This ensures human-readable reports have consistent structure across runs.
- **Risk**: LOW. Additive constraint on the report emitter.

### S-003: Resume Behavior Discussion (from Variant A, Section 9.3)

- **Source**: Variant A, Section 9.3 ("Resume behavior")
- **Target location**: Add as new subsection "5.6.1 Resume Behavior" within B's Section 5.6
- **Rationale**: B does not discuss how the wiring step interacts with roadmap resume. A correctly notes that resume works naturally if the report is deterministic, the gate result is reproducible, and `_get_all_step_ids()` includes the new step. This is important operational knowledge that prevents resume bugs.
- **Risk**: LOW. Documentation only, confirms existing behavior.

### S-004: Coordination Notes (from Variant C, Section 18)

- **Source**: Variant C, Section 18 ("Coordination Notes")
- **Target location**: Add as new Section 15 in B (before or after Appendices)
- **Rationale**: C identifies concrete merge conflict risks when modifying `roadmap/gates.py` -- specifically with Anti-Instincts (`ANTI_INSTINCT_GATE` in v3.05) and Unified Audit Gating (D-03/D-04 `SPEC_FIDELITY_GATE` extensions). This operational awareness prevents avoidable integration failures.
- **Risk**: LOW. Additive section.

### S-005: FPR Calibration Formula (from Variant C, Section 9)

- **Source**: Variant C, Section 9, Phase 2 ("FPR calibration")
- **Target location**: Replace B's Section 7 Phase 2 criteria with the more rigorous formula
- **Rationale**: C specifies "Set thresholds at `measured_FPR + 2 sigma` above re-export noise floor. Phase 2 MUST NOT activate if unwired-callable FPR cannot be separated from noise." This is more rigorous than B's simple "FPR < 15%" threshold. The statistical approach prevents premature soft-mode activation when FPR variance is high.
- **Risk**: LOW. Strengthens rollout criteria without changing mechanism.

### S-006: WiringConfig Dataclass (from Variant C, Section 6)

- **Source**: Variant C, Section 6 (Data Models, `WiringConfig` class)
- **Target location**: Merge into B's `audit/wiring_config.py` design (Section 4.2 module map)
- **Rationale**: C provides the concrete `WiringConfig` dataclass with `registry_patterns`, `provider_dir_names`, `whitelist_path`, and `exclude_patterns`. B references `wiring_config.py` in the module map and mentions `WiringConfig` in the public API but does not show the concrete fields. C's model is ready for implementation.
- **Risk**: LOW. B already allocates the file; this fills in the content.

### S-007: Deviation Count Reconciliation (from Variant C, Section 10) -- DEFERRED

- **Source**: Variant C, Section 10 ("Companion: Deviation Count Reconciliation")
- **Target location**: Add to B's out-of-scope / backlog section with cross-reference
- **Rationale**: The debate transcript (X-011) reached 90% confidence that this should be a separate release to prevent scope creep and merge conflicts. However, the feature itself is valuable and should be tracked. Add a backlog entry in the merged spec's out-of-scope section referencing C's design.
- **Risk**: NONE. Deferred, documentation only.

### S-008: Rejected Option Documentation (from Variant A, Section 9.1)

- **Source**: Variant A, Section 9.1 ("Rejected option")
- **Target location**: Add to B's Section 14 (Decisions), expand D2 entry
- **Rationale**: A explicitly documents the rejected LLM-synthesis approach with rationale ("too weak for wiring assurance and too dependent on narrative interpretation"). B's D2 states the decision but not the rejected alternative. Recording rejected options prevents future re-debates.
- **Risk**: LOW. Additive to decision table.

### S-009: Suppression Expiry Concept (from Variant A, Section 10.2) -- DEFERRED

- **Source**: Variant A, Section 10.2 ("Suppression policy", optional expiry/revalidation note)
- **Target location**: Add to B's out-of-scope with v1.1 backlog reference
- **Rationale**: The debate transcript (U-004) scored this at 70% confidence for deferral. Whitelist entries with expiry dates force periodic re-evaluation and prevent stale suppressions. Useful but adds schema complexity. Track for v1.1.
- **Risk**: NONE. Deferred.

---

## 2. Base Weaknesses to Fix

### W-001: report.passed vs gate-passed semantic gap

- **Issue**: B's `WiringReport.passed` property returns `True` when `total_findings == 0`, but gate pass depends on rollout mode (shadow always passes, soft passes if no critical, full passes if no critical+major). This semantic gap could confuse implementers who check `report.passed` expecting it to reflect enforcement policy.
- **Better variant**: Debate transcript X-006 identifies the issue. No variant fully resolves it.
- **Fix approach**: Add explicit docstring to `WiringReport.passed`: "Returns True when analysis found zero issues. This represents analysis truth, not enforcement policy. Gate enforcement depends on rollout_mode -- see _zero_blocking_findings_for_mode()." Add a method `WiringReport.blocking_for_mode(mode: str) -> int` that returns the blocking finding count for a given mode, making the computation available at the data model level.
- **Risk**: LOW. Additive clarification, no behavioral change.

### W-002: ToolOrchestrator cut-risk not formalized

- **Issue**: The debate transcript identifies the ToolOrchestrator AST plugin (B's Section 5.3, T06) as the highest-risk addition. B acknowledges it in passing but does not formalize the cut criteria.
- **Better variant**: Debate transcript acceptance risk #2 identifies this.
- **Fix approach**: Add a "Cut Criteria" subsection to Section 5.3: "If T06 is not complete by the time T08 (roadmap integration) begins, defer T06 to v1.1. Core wiring gate functionality (T01-T05, T07-T10) does not depend on the ToolOrchestrator plugin. The cleanup-audit integration (Mode C) operates with reduced accuracy but still functions using line-based analysis."
- **Risk**: LOW. Makes existing implicit assumption explicit.

### W-003: grace_period interaction not documented as operational requirement

- **Issue**: INV-006 resolution establishes that shadow mode works through mode-aware semantic checks even if BLOCKING is forced, but the `grace_period > 0` operational preference is only discussed in the debate transcript, not in the spec itself.
- **Better variant**: Debate transcript INV-006 resolution.
- **Fix approach**: Add to B's Section 7 (Rollout Plan), Phase 1: "Operational note: Roadmap configurations should set `grace_period > 0` during shadow rollout to enable `GateMode.TRAILING` behavior. If `grace_period = 0` forces BLOCKING, shadow mode still passes because `_zero_blocking_findings_for_mode` reads `rollout_mode=shadow` from frontmatter and returns True unconditionally. However, TRAILING mode provides cleaner operational semantics (deferred evaluation via `TrailingGateRunner` rather than immediate pass-through)."
- **Risk**: LOW. Documentation of an accepted operational interaction.

### W-004: _extract_frontmatter_values() helper not specified

- **Issue**: INV-001/INV-005 establish the need for a private `_extract_frontmatter_values(content: str) -> dict[str, str]` helper in `audit/wiring_gate.py`. All semantic checks implicitly need it, but B does not specify it.
- **Better variant**: Debate transcript INV-001 resolution.
- **Fix approach**: Add a subsection "5.5.1 Frontmatter Value Extraction" to B's Section 5.5: "All semantic check functions share a private helper `_extract_frontmatter_values(content: str) -> dict[str, str]` that uses the `_FRONTMATTER_RE` regex pattern (duplicated from `pipeline/gates.py:77` as a private constant to preserve NFR-007 layering) to extract frontmatter key-value pairs. Each check calls this helper once and casts values as needed. Estimated: ~15 LOC."
- **Risk**: LOW. Implementation detail that resolves a shared dependency.

---

## 3. Changes NOT Being Made

### R-001: Variant A's gate constant placement in roadmap/gates.py

- **Considered**: Variant A places `WIRING_VERIFICATION_GATE` in `roadmap/gates.py` alongside other roadmap gates.
- **Rejected**: Debate transcript X-001 (85% confidence) determines that co-locating the gate with the analysis engine in `audit/wiring_gate.py` is superior. The gate's semantic checks reference audit-specific concepts (rollout mode, wiring categories). Placing the gate in `roadmap/gates.py` would create a dependency from `roadmap/gates.py` on `audit/wiring_gate.py` for the check functions, which is architecturally worse than having `roadmap/executor.py` import `WIRING_GATE` from `audit/`. The existing `SPEC_FIDELITY_GATE` lives in `roadmap/gates.py` because its checks are roadmap-specific; `WIRING_GATE` checks are audit-specific.

### R-002: Variant A's WIRING_VERIFICATION_GATE naming

- **Considered**: Variant A uses the longer name `WIRING_VERIFICATION_GATE`.
- **Rejected**: `WIRING_GATE` is consistent with the shorter naming convention used by other gates (`SPEC_FIDELITY_GATE`, `MERGE_GATE`). The longer form adds no disambiguating value since there is only one wiring gate.

### R-003: Variant A's nested severity_summary YAML block

- **Considered**: Variant A's frontmatter includes a nested `severity_summary:` block with `critical:`, `major:`, `info:` sub-keys.
- **Rejected**: INV-014 resolution (debate transcript) conclusively demonstrates that the existing `_check_frontmatter()` function uses flat key extraction by line-splitting on `:`. Nested blocks create false-positive field presence detection and complicate the `_extract_frontmatter_values()` helper. B's flat `critical_count`, `major_count`, `info_count` fields convey identical information without interaction risks.

### R-004: Variant C's per-category-zero semantic checks

- **Considered**: Variant C defines separate `_zero_unwired_callables`, `_zero_orphan_modules`, `_zero_unwired_registries` checks that require each category count to be zero.
- **Rejected**: INV-006 resolution (debate transcript, 95% confidence) proves this design breaks shadow mode when `grace_period=0` forces BLOCKING. Under those conditions, any findings would fail the per-category-zero checks, making shadow mode impossible. B's mode-aware `_zero_blocking_findings_for_mode` check, which reads `rollout_mode` and `blocking_findings` from frontmatter, is the only design that survives all executor configurations.

### R-005: Variant C's deviation count reconciliation bundling

- **Considered**: Variant C includes a companion `_deviation_counts_reconciled()` function added to `SPEC_FIDELITY_GATE`.
- **Rejected**: Debate transcript X-011 (90% confidence) determines this should be a separate release. Bundling creates scope creep and increases merge conflict risk with concurrent `roadmap/gates.py` modifications from Anti-Instincts and Unified Audit Gating. The feature is tracked as a deferred backlog item (see S-007).

### R-006: Variant C's retry_limit=1

- **Considered**: Variant C sets `retry_limit=1` on the Step definition.
- **Rejected**: INV-012 resolution (debate transcript, 95% confidence) confirms that `retry_limit=0` means "one attempt, no retries" per `pipeline/executor.py:158` (`max_attempts = retry_limit + 1`). Since wiring analysis is deterministic, retrying produces identical results and wastes time. The only retry-worthy scenario (transient filesystem errors) should be handled within the analysis function itself, not at the step level.

---

## 4. Summary of Changes to Base (Variant B)

| ID | Type | Location in B | Change | Source |
|----|------|---------------|--------|--------|
| S-001 | Add | Section 5.6 | Insertion point rationale subsection | A 4.2, 5.3 |
| S-002 | Add | After Section 5.4 | Required body sections (7 sections) | A 7.3 |
| S-003 | Add | Section 5.6 | Resume behavior subsection | A 9.3 |
| S-004 | Add | New Section 15 | Coordination notes | C 18 |
| S-005 | Replace | Section 7 Phase 2 | FPR calibration formula | C 9 |
| S-006 | Merge | Section 4.2 / wiring_config.py | Concrete WiringConfig fields | C 6 |
| S-007 | Add | Appendix C | Deviation reconciliation backlog reference | C 10 |
| S-008 | Expand | Section 14 D2 | Rejected LLM option with rationale | A 9.1 |
| S-009 | Add | Appendix C | Suppression expiry v1.1 backlog | A 10.2 |
| W-001 | Fix | Section 5.1 | report.passed docstring + blocking_for_mode() | Debate X-006 |
| W-002 | Add | Section 5.3 | ToolOrchestrator cut criteria | Debate risk #2 |
| W-003 | Add | Section 7 Phase 1 | grace_period operational note | INV-006 |
| W-004 | Add | Section 5.5 | _extract_frontmatter_values() helper spec | INV-001 |

**Estimated delta**: +180-220 lines of spec text added to Variant B. No sections removed. No structural reorganization needed.

---

## 5. Invariant Resolutions to Embed

The debate transcript resolved 7 invariant findings. Each must be reflected in the merged spec:

| INV | Resolution | Where in merged spec |
|-----|-----------|---------------------|
| INV-001 | `_extract_frontmatter_values()` private helper | W-004: new subsection 5.5.1 |
| INV-003 | Insert in both `_build_steps()` and `_get_all_step_ids()` | Already in B Section 5.6 Step 5 |
| INV-005 | Merged with INV-001 | Same as INV-001 |
| INV-006 | Mode-aware checks survive grace_period=0 | W-003: operational note in Section 7 |
| INV-008 | Single-source count computation | Already in B Section 5.1 (WiringReport.total_findings property) |
| INV-012 | retry_limit=0 means 1 attempt | Already in B Section 5.6 Step 4 |
| INV-014 | Flat frontmatter, no nested YAML | Already in B Section 5.4 (no nested blocks) |

All 7 invariant resolutions are either already present in Variant B or addressed by the weakness fixes above. No additional structural changes needed.
