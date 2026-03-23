# Agent D4 Validation Report: reachability_framework Domain

**Agent**: D4
**Domain**: reachability_framework
**Spec**: v3.3-requirements-spec.md
**Roadmap**: v3.3-TurnLedger-Validation/roadmap.md
**Date**: 2026-03-23

---

## REQ-039: FR-4.1 — Spec-driven wiring manifest

- Spec source: FR-4.1 (section "FR-4: Reachability Eval Framework")
- Spec text: "Each release spec declares a `wiring_manifest` section. The example below shows the 9 core entries for illustration. See **Wiring Manifest (v3.3)** section below for the authoritative 13-entry manifest including all v3.1, v3.2, and v3.05 constructs." The manifest schema requires both `entry_points` and `required_reachable` sections.
- Status: PARTIAL
- Match quality: SEMANTIC
- Evidence:
  - Roadmap location: Phase 1B, tasks 1B.1 and 1B.4
  - Roadmap text: "1B.1 | FR-4.1 | Wiring manifest YAML schema — `entry_points` section listing callable entry points, `required_reachable` section listing target symbols with spec references" and "1B.4 | FR-4.1 | Initial wiring manifest YAML for executor.py entry points — `tests/v3.3/wiring_manifest.yaml`"
- Finding:
  - Severity: MEDIUM
  - Gap description: Task 1B.1 correctly names both schema sections (`entry_points` and `required_reachable`), and 1B.4 commits to a standalone `.yaml` file (Open Question 4 confirms this). However, the roadmap task 1B.4 says "Initial wiring manifest YAML for executor.py entry points" — the qualifier "for executor.py entry points" may signal an incomplete initial manifest covering only the sprint executor, not all 3 entry points (both `execute_sprint` and `_run_convergence_spec_fidelity` from the spec). The spec's authoritative manifest has 2 entry points and 13 `required_reachable` entries, but the roadmap does not enumerate the expected count or explicitly call out that the convergence entry point (`_run_convergence_spec_fidelity`) must be included.
  - Impact: If the initial manifest omits `_run_convergence_spec_fidelity` and its 3 dependent targets (`execute_fidelity_with_convergence`, `reimburse_for_progress`, `handle_regression`), the NFR-5 completeness check in task 4.4 will pass against an incomplete baseline, silently missing 3 of 13 required entries.
  - Recommended correction: Amend task 1B.4 to state: "Initial wiring manifest YAML — `tests/v3.3/wiring_manifest.yaml` — must include BOTH entry points (`execute_sprint`, `_run_convergence_spec_fidelity`) and all 13 `required_reachable` entries as specified in the Wiring Manifest (v3.3) section of the spec."
- Confidence: HIGH

---

## REQ-040: FR-4.2 — AST call-chain analyzer

- Spec source: FR-4.2 (section "FR-4: Reachability Eval Framework")
- Spec text: "**Algorithm**: 1. `ast.parse()` the entry point module 2. Walk the AST, building a call graph (function → set of called functions) 3. Resolve imports to follow cross-module calls 4. BFS/DFS from entry point function to determine reachable set 5. Report any target NOT in reachable set as a GAP"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 1B, task 1B.2
  - Roadmap text: "1B.2 | FR-4.2 | AST call-chain analyzer module — `src/superclaude/cli/audit/reachability.py`: `ast.parse()` → call graph construction → BFS/DFS reachability; cross-module import resolution; lazy import handling"
- Confidence: HIGH

---

## REQ-041: FR-4.2 limitations — documented limitations

- Spec source: FR-4.2 (section "Limitations to document")
- Spec text: "- Dynamic dispatch (`getattr`, `**kwargs` delegation) produces false negatives - Conditional imports (`if TYPE_CHECKING`) are excluded from reachability - Lazy imports inside functions ARE included (these are real runtime paths)"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 1B, task 1B.3
  - Roadmap text: "1B.3 | FR-4.2 | Documented limitations in module docstring: dynamic dispatch (`getattr`, `**kwargs`) → false negatives; `TYPE_CHECKING` conditionals excluded; lazy imports inside functions included (NFR-6)"
- Confidence: HIGH

---

## REQ-042: FR-4.3 — Reachability gate integration

- Spec source: FR-4.3 (section "FR-4: Reachability Eval Framework")
- Spec text: "The analyzer runs as a pipeline gate that: - Reads the wiring manifest from the release spec - Runs AST analysis for each entry - Produces a structured report: PASS: All required targets reachable / FAIL: List of unreachable targets with spec references - Integrates with existing `GateCriteria` infrastructure"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 3A, task 3A.4
  - Roadmap text: "3A.4 | FR-4.3 | `src/superclaude/cli/audit/reachability.py` | Add `GateCriteria`-compatible interface: reads manifest, runs AST analysis, produces structured PASS/FAIL report"
- Confidence: HIGH

---

## REQ-043: FR-4.4 — Regression test

- Spec source: FR-4.4 (section "FR-4: Reachability Eval Framework")
- Spec text: "**Test**: Intentionally remove a call to `run_post_phase_wiring_hook()` from `execute_sprint()`. Run the reachability gate. Assert it detects the gap and references the correct spec (v3.2-T02)."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 3B, task 3B.2
  - Roadmap text: "3B.2 | FR-4.4, SC-7, SC-9 | Regression test: remove `run_post_phase_wiring_hook()` call → gate detects gap referencing v3.2-T02"
- Confidence: HIGH

---

## REQ-NFR5: Every FR-1 wiring point must have manifest entry; validate completeness

- Spec source: Success Criteria / Phase 4 validation plan
- Spec text (SC-9 and Phase 4): "4. Cross-validate: every SC-* success criterion has at least one passing test" and implicitly from FR-4.1: "Each release spec declares a `wiring_manifest` section" with the intent that every wiring point is accounted for. The explicit NFR-5 reference appears in the roadmap's Phase 4 task.
- Status: PARTIAL
- Match quality: SEMANTIC
- Evidence:
  - Roadmap location: Phase 4, task 4.4
  - Roadmap text: "4.4 | NFR-5 | Validate wiring manifest completeness: every known wiring point from FR-1 has a manifest entry"
- Finding:
  - Severity: LOW
  - Gap description: Task 4.4 correctly defines a completeness validation step. However, the check is scoped to "every known wiring point from FR-1" — this means it validates FR-1 wiring points only. The authoritative 13-entry manifest also includes v3.05 convergence constructs (FR-2.1 territory: `execute_fidelity_with_convergence`, `reimburse_for_progress`, `handle_regression`). If those convergence-path wiring points are not in the FR-1 list, the completeness check in task 4.4 would pass even if those 3 entries are absent from the manifest. The spec's NFR-5 intent is that ALL wiring points have manifest entries, not just FR-1 wiring points.
  - Impact: Silent gap in completeness validation for v3.05 convergence path entries. The reachability gate might never test for `handle_regression` reachability.
  - Recommended correction: Broaden task 4.4 to: "Validate wiring manifest completeness: confirm all 13 entries from the authoritative Wiring Manifest (v3.3) are present, including FR-1 wiring points AND convergence path constructs from FR-2.1."
- Confidence: HIGH

---

## REQ-NFR6: AST analyzer limitations documented in module docstring

- Spec source: FR-4.2 limitations section + roadmap task 1B.3 cross-references NFR-6
- Spec text: The spec requires limitations to be documented (FR-4.2 "Limitations to document" section). The roadmap codifies this as NFR-6.
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 1B, task 1B.3
  - Roadmap text: "1B.3 | FR-4.2 | Documented limitations in module docstring: dynamic dispatch (`getattr`, `**kwargs`) → false negatives; `TYPE_CHECKING` conditionals excluded; lazy imports inside functions included (NFR-6)"
- Confidence: HIGH

---

## REQ-SC7: SC-7 — eval framework catches known-bad state

- Spec source: Success Criteria table
- Spec text: "SC-7 | Eval framework catches known-bad state | Regression test: break wiring → detected | 3"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 3B, task 3B.2; Success Criteria Validation Matrix row SC-7
  - Roadmap text (3B.2): "Regression test: remove `run_post_phase_wiring_hook()` call → gate detects gap referencing v3.2-T02"
  - Roadmap text (SC matrix): "SC-7 | Eval catches known-bad state | FR-4.4 regression test | 3 | Yes"
- Confidence: HIGH

---

## REQ-SC9: SC-9 — reachability gate detects unreachable code

- Spec source: Success Criteria table
- Spec text: "SC-9 | Reachability gate catches unreachable code | Hybrid A+D detects intentionally broken wiring | 3"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 3B, task 3B.2; Success Criteria Validation Matrix row SC-9; Validation Checkpoint C
  - Roadmap text (SC matrix): "SC-9 | Reachability gate detects unreachable | FR-4.4 on intentionally broken wiring | 3 | Yes"
  - Roadmap text (Checkpoint C): "Reachability gate catches intentionally broken wiring."
- Confidence: HIGH

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Requirements evaluated | 9 |
| COVERED | 6 |
| PARTIAL | 2 |
| MISSING | 0 |
| CONFLICTING | 0 |
| IMPLICIT | 0 |

| Severity of Findings | Count |
|----------------------|-------|
| CRITICAL | 0 |
| HIGH | 0 |
| MEDIUM | 1 |
| LOW | 1 |

### Finding Summary

**MEDIUM — REQ-039 (FR-4.1 manifest completeness at authoring time)**: The roadmap task 1B.4 describes the initial manifest as covering "executor.py entry points" rather than explicitly mandating both entry points and all 13 authoritative entries from the spec's Wiring Manifest (v3.3) section. This creates a risk that the convergence path entry point (`_run_convergence_spec_fidelity`) and its 3 dependent targets are omitted from the initial manifest, passing the NFR-5 completeness check at Phase 4 against an incomplete baseline.

**LOW — REQ-NFR5 (completeness check scope)**: The Phase 4 task 4.4 completeness validation is scoped to "FR-1 wiring points" only. The authoritative manifest contains 13 entries, including 3 convergence-path entries (v3.05 constructs) that fall under FR-2 territory, not FR-1. If these are absent from the FR-1 list, the completeness check silently passes with an incomplete manifest.

### Overall Domain Assessment

The reachability_framework domain is **well-covered** by the roadmap. All 5 core algorithm steps from FR-4.2, all 3 documented limitations (NFR-6), the GateCriteria-compatible interface (FR-4.3), and the specific regression test criteria (FR-4.4 including the v3.2-T02 spec reference) are addressed with exact or near-exact fidelity. The two PARTIAL findings are scoping ambiguities in manifest population and completeness validation — neither is a structural gap in the implementation plan, but both could result in silently incomplete artifacts if not clarified. No CRITICAL or HIGH severity gaps were found.
