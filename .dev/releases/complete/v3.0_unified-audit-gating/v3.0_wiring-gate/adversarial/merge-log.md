---
title: "Merge Log — Adversarial Debate Resolution"
timestamp: 2026-03-18T00:00:00Z
step: 5
protocol: adversarial-debate
base_variant: B (spec2.md)
output: adversarial/merged-spec.md
changes_applied: 22
---

# Merge Log

## Summary

Merged specification produced from Variant B (spec2.md) as base, incorporating targeted additions from Variant A (spec.md) and Variant C (spec3.md) per the refactoring plan and debate transcript consensus.

**Base**: Variant B (spec2.md) -- scored 0.954 in hybrid selection
**Incorporations**: 9 from refactoring plan + 7 invariant resolutions + 4 debate consensus items
**Rejections**: 6 (documented in refactoring plan Section 3)

---

## Changes Applied

### From Variant A (spec.md)

| ID | Change | Target Section | Status | Notes |
|----|--------|---------------|--------|-------|
| S-001 | Insertion point rationale ("Why `_build_steps()` is the correct insertion point") | Section 5.7.1 (new subsection) | APPLIED | Added anti-instinct precedent argument and no-dynamic-registry argument |
| S-002 | 7 required report body sections | Section 5.4.1 (new subsection) | APPLIED | Summary, Unwired Callables, Orphans, Registries, Suppressions, Remediation, Evidence |
| S-003 | Resume behavior discussion | Section 5.7.2 (new subsection) | APPLIED | Documents deterministic resume compatibility |
| S-008 | Rejected LLM option with rationale | Section 14 D2a (new subsection) | APPLIED | Documents "too weak for wiring assurance" rejection |
| S-009 | Suppression expiry concept | Appendix C backlog entry | APPLIED | Deferred to v2.1 per debate U-004 (70% confidence for deferral) |

### From Variant C (spec3.md)

| ID | Change | Target Section | Status | Notes |
|----|--------|---------------|--------|-------|
| S-004 | Coordination notes section | Section 15 (new section) | APPLIED | Merge conflict risk with Anti-Instincts and Unified Audit Gating |
| S-005 | FPR calibration formula | Section 7 Phase 2 | APPLIED | `measured_FPR + 2 sigma` replaces simple percentage threshold |
| S-006 | WiringConfig dataclass details | Section 4.2.1 (new subsection) | APPLIED | Concrete fields: registry_patterns, provider_dir_names, whitelist_path, exclude_patterns |
| S-007 | Deviation count reconciliation | Appendix C backlog entry | APPLIED | Deferred to separate release per debate X-011 (90% confidence) |

### From Invariant Resolutions

| INV | Change | Target Section | Status | Notes |
|-----|--------|---------------|--------|-------|
| INV-001 | `_extract_frontmatter_values()` helper specification | Section 5.5 (new section) | APPLIED | ~15 LOC private helper, layering-safe duplication of regex |
| INV-003 | `_get_all_step_ids()` synchronization requirement | Section 5.7 Step 5 | APPLIED | Explicit note about desync being intentional, new step in both functions |
| INV-006 | `grace_period` interaction note for shadow mode | Section 7 Phase 1 | APPLIED | Documents TRAILING vs BLOCKING behavior under grace_period=0 |
| INV-008 | Single-source computation requirement | Section 5.1 (note after data models) | APPLIED | Category and severity counts derive from same finding lists |
| INV-012 | `retry_limit=0` semantics documented | Section 5.7 Step 4 | APPLIED | `max_attempts = retry_limit + 1` per executor.py:158 |
| INV-014 | Flat frontmatter confirmed | Section 5.4 | ALREADY IN BASE | B already uses flat fields, no nested severity_summary |

### From Debate Consensus

| Point | Change | Target Section | Status | Notes |
|-------|--------|---------------|--------|-------|
| X-006 / W-001 | Rename `WiringReport.passed` to `.clean`, add `blocking_for_mode()` | Section 5.1 | APPLIED | Resolves semantic gap between analysis truth and enforcement policy |
| W-002 | ToolOrchestrator cut criteria | Section 5.3.1 (new subsection) | APPLIED | Explicit deferral criteria if T06 threatens critical path |
| A-008 | `files_skipped` field | Section 5.1, 5.4, 8.2 | APPLIED | Added to WiringReport, frontmatter, and gate contract |
| -- | `info` severity in WiringFinding | Section 5.1 | ALREADY IN BASE | B already includes "info" in severity Literal |

---

## Changes NOT Made (Rejections)

| ID | Rejected Change | Reason | Confidence |
|----|----------------|--------|------------|
| R-001 | Gate constant in `roadmap/gates.py` (Variant A) | Co-locating gate with analysis engine in `audit/wiring_gate.py` is superior (debate X-001, 85%) | 85% |
| R-002 | `WIRING_VERIFICATION_GATE` naming (Variant A) | `WIRING_GATE` matches shorter naming convention of existing gates | 80% |
| R-003 | Nested `severity_summary` YAML block (Variant A) | Collides with flat key extraction in `_check_frontmatter()` (INV-014, conclusive) | 95% |
| R-004 | Per-category-zero semantic checks (Variant C) | Breaks shadow mode when `grace_period=0` forces BLOCKING (INV-006, 95%) | 95% |
| R-005 | Deviation reconciliation bundled in this release (Variant C) | Scope creep risk, merge conflict with concurrent gates.py changes (X-011, 90%) | 90% |
| R-006 | `retry_limit=1` (Variant C) | Deterministic step produces identical results on retry (INV-012, 95%) | 95% |

---

## Structural Changes to Base

| Type | Count | Description |
|------|-------|-------------|
| New subsections added | 6 | 4.2.1, 5.3.1, 5.4.1, 5.5, 5.7.1, 5.7.2 |
| New sections added | 1 | Section 15 (Coordination Notes) |
| Appendix entries added | 2 | Deviation Reconciliation backlog, Suppression Expiry backlog |
| Decision entries expanded | 1 | D2a rejected alternative detail |
| Data model changes | 3 | `.passed` -> `.clean`, added `blocking_for_mode()`, added `files_skipped` |
| Sections removed | 0 | -- |
| Section reordering | 0 | -- |

**Estimated text delta**: +200-240 lines added to base. No sections removed. No structural reorganization.

---

## Verification Checklist

- [x] All 9 S-NNN incorporations from refactoring plan applied
- [x] All 4 W-NNN weakness fixes from refactoring plan applied
- [x] All 7 INV-NNN invariant resolutions reflected
- [x] All 6 R-NNN rejections confirmed NOT present
- [x] Provenance annotations added as HTML comments throughout
- [x] Heading hierarchy preserved (H1 -> H2 -> H3 -> H4)
- [x] Section numbering consistent and sequential
- [x] All internal cross-references valid
- [x] `WiringReport.passed` renamed to `.clean` per W-001
- [x] `files_skipped` field added per A-008 consensus
- [x] `info` severity present in WiringFinding (already in base)
- [x] Flat frontmatter throughout (no nested YAML blocks)
- [x] `retry_limit=0` with documented semantics
- [x] `_get_all_step_ids()` synchronization requirement explicit
- [x] `grace_period` interaction documented in rollout plan
- [x] Coordination notes section present
- [x] FPR calibration formula in Phase 2
- [x] WiringConfig dataclass specified
- [x] Required report body sections enumerated
- [x] Insertion point rationale documented
- [x] Resume behavior documented
- [x] Rejected LLM option documented in decisions
- [x] ToolOrchestrator cut criteria specified
- [x] Backlog items for deferred features in Appendix C
