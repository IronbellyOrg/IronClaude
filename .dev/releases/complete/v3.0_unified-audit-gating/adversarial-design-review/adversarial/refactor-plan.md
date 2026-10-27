# Refactoring Plan: Merge into Variant A Base

## Overview
- **Base variant**: A (brainstorm-resume-fix-A.md)
- **Incorporated variants**: B (7 items), C (6 items), Round 3 consensus (5 items)
- **Total planned changes**: 18
- **Overall risk**: Medium (structural additions, no destructive changes to base)
- **Review status**: Auto-approved

---

## Planned Changes

### Change #1: Add `--depth` Coverage (from B, §4)
- **Source**: Variant B, §4 ("Does `--depth` Have the Same Bug?")
- **Target**: After Bug 1 section in base (new §between Bug 1 and Bug 2)
- **Integration approach**: Insert new subsection covering `--depth` default detection using same `get_parameter_source` mechanism
- **Rationale**: A conceded this gap in Round 1; `--depth` has identical bug class (debate C-005, 85% confidence for C's position)
- **Risk**: Low (additive)

### Change #2: Add CLI Option Audit Table (from B, §4)
- **Source**: Variant B, §4 option audit table
- **Target**: New section after `--depth` coverage
- **Integration approach**: Insert B's table reviewing `--output`, `--model`, `--max-turns`, `--retrospective` with risk ratings
- **Rationale**: Unique contribution U-001 (HIGH value); closes the bug class systemically (debate scoring 72% for B)
- **Risk**: Low (additive)

### Change #3: Add Fix Interaction Matrix (from B, §5)
- **Source**: Variant B, §5 ("Interaction Between Fixes")
- **Target**: New section before Implementation Order
- **Integration approach**: Insert B's interaction matrix showing what happens when each fix applied alone
- **Rationale**: Unique contribution U-002 (HIGH value); essential for safe incremental rollout
- **Risk**: Low (additive)

### Change #4: Add Differential `--depth` vs `--agents` Treatment Rationale (from C, §4)
- **Source**: Variant C, §4 ("The `--depth` Problem")
- **Target**: Within the new `--depth` section (Change #1)
- **Integration approach**: Add C's analysis of why depth can be auto-restored (single-step impact) while agents require explicit handling (structural impact)
- **Rationale**: C won this point decisively (X-004, 85% confidence); B conceded in Round 2
- **Risk**: Low (additive)

### Change #5: Replace `get_parameter_source` with `ResumableConfig` (Round 3 consensus)
- **Source**: Round 3 consensus (B's proposal, C's serialization requirement)
- **Target**: Bug 1 Fix section, replacing `ctx.get_parameter_source` approach
- **Integration approach**: Replace the detection mechanism with `ResumableConfig` dataclass that stores values + `source: str` tag. Update code samples.
- **Rationale**: Addresses INV-001 (HIGH); programmatic invocation safety. All three advocates converged.
- **Risk**: Medium (modifies base's core mechanism)

### Change #6: Add `--on-conflict` Flag Design (Round 3 consensus)
- **Source**: Round 3 consensus (C's proposal, A+C majority)
- **Target**: New subsection in Bug 1 Fix
- **Integration approach**: Add `--on-conflict ask|override|fail` flag with non-interactive default `fail`
- **Rationale**: Addresses INV-004 (HIGH); CI/automation safety. 2-1 majority.
- **Risk**: Low (additive flag design)

### Change #7: Enhance `_apply_resume` with State-Driven Path Resolution (from C, §3.2)
- **Source**: Variant C, §3.2 ("State-Driven Path Resolution")
- **Target**: Bug 3 Fix section, as enhancement to `_apply_resume` rewrite
- **Integration approach**: Add `state_paths` dict lookup as defense-in-depth within the dependency-aware rewrite
- **Rationale**: Unique contribution U-005 (HIGH value); decouples resume from config for gate checks
- **Risk**: Medium (modifies core `_apply_resume` logic)

### Change #8: Extract `_step_needs_rerun()` Helper (from B, §3)
- **Source**: Variant B, §3.1 (`_step_needs_rerun()` function)
- **Target**: Bug 3 Fix section, refactoring A's inline logic into named helper
- **Integration approach**: Extract the per-step rerun decision into a named, testable function
- **Rationale**: Better modularity; debate agreed A and B have same algorithm, B's factoring is better (C-006)
- **Risk**: Low (refactor, no behavior change)

### Change #9: Add Parallel Group Semantics (Round 3 consensus)
- **Source**: Round 3 consensus (A's init, B's group_progress, C's schema versioning)
- **Target**: Bug 3 Fix section, within `_apply_resume` rewrite
- **Integration approach**: Add `-1` high-water mark init, atomic group completion, `group_progress` dict
- **Rationale**: Addresses INV-006 (HIGH); parallel group partial completion
- **Risk**: Medium (new data structures in resume logic)

### Change #10: Add No-Progress Guard to `_save_state` (from C, §3.4)
- **Source**: Variant C, §3.4 ("Conditional State Writes")
- **Target**: Bug 4 Fix section, enhancing defense-in-depth
- **Integration approach**: Add "no steps passed → no write" guard before A's existing defense logic
- **Rationale**: C won this point (X-003, 75% confidence); prevents state corruption from failed runs
- **Risk**: Low (additive guard)

### Change #11: Add Cascade Logging (from C, §3.3)
- **Source**: Variant C, §3.3 (cascade logging)
- **Target**: Bug 3 Fix section, within `_apply_resume` rewrite
- **Integration approach**: Add `_log.info` calls for each downstream step included in re-run
- **Rationale**: Observability improvement; complements dependency-aware tracking
- **Risk**: Low (logging only)

### Change #12: Add Schema Version / Migration Analysis (from B, §7)
- **Source**: Variant B, §7 ("Migration / Backward Compatibility")
- **Target**: Backward Compatibility section (expand existing)
- **Integration approach**: Add B's 3 subsections (existing state files, CLI interface, schema version)
- **Rationale**: Unique contribution U-003 (MEDIUM value); production readiness
- **Risk**: Low (documentation)

### Change #13: Expand Test Plan (from B, §6)
- **Source**: Variant B, §6 ("Test Plan")
- **Target**: Test Plan section (expand from 6 to ~17 tests)
- **Integration approach**: Add B's integration tests (4) and edge cases (5) to A's existing 6 unit tests
- **Rationale**: A conceded 6 tests insufficient; B has broadest coverage
- **Risk**: Low (test additions)

### Change #14: Add 5-Layer Defense Summary (from C, §5)
- **Source**: Variant C, §5 ("Defense in Depth: Layered Guard Summary")
- **Target**: New section before Risk Assessment
- **Integration approach**: Insert C's 5-layer diagram, updated to reflect merged architecture
- **Rationale**: Unique contribution U-006 (MEDIUM value); aids reviewers in understanding defense posture
- **Risk**: Low (documentation)

### Change #15: Add Depth/Agent Coupling WARNING (Round 3 consensus)
- **Source**: Round 3 consensus (A's proposal, B+C agreement)
- **Target**: Within `--depth` coverage section (Change #1)
- **Integration approach**: Add config validation that warns on orphaned agent assignments under quick depth
- **Rationale**: Addresses INV-010 (HIGH); prevents inconsistent configurations
- **Risk**: Low (validation warning)

### Change #16: Add Dirty-Output Propagation Order Note (from invariant probe)
- **Source**: INV-007 finding
- **Target**: Bug 3 Fix section
- **Integration approach**: Add note that `_apply_resume` must iterate steps in topological order for dirty propagation to be correct (existing pipeline order guarantees this)
- **Rationale**: Documents assumption explicitly; prevents future regression
- **Risk**: Low (documentation)

### Change #17: Add State File Atomicity Note (from invariant probe)
- **Source**: INV-003 finding
- **Target**: Bug 4 Fix section or Risk Assessment
- **Integration approach**: Note that state file should use write-then-rename for atomicity
- **Rationale**: MEDIUM invariant; prevents corruption on crash
- **Risk**: Low (documentation + minor code change)

### Change #18: Add Estimated Diff Size (from B)
- **Source**: Variant B, final line
- **Target**: End of Files Changed section
- **Integration approach**: Add estimated diff size annotation
- **Rationale**: Aids review planning
- **Risk**: Low (documentation)

---

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale for Rejection |
|------------|-------------------|------------------------|
| C-001 (Click defaults to None) | B: Change Click defaults to `None` | Round 3 converged on `ResumableConfig` with source tag instead; `None` defaults have broader blast radius (A's criticism accepted by debate) |
| X-001 (Hard abort on mismatch) | C: `sys.exit(1)` on agent mismatch | Round 2 refined to warn-and-confirm → Round 3 refined to `--on-conflict` flag; hard abort rejected for UX reasons |
| X-002 (Keep found_failure cascade) | C: Retain cascade with logging only | Dependency-aware tracking (A+B) won 80% confidence; cascade is semantically identical but less modular |
| C-003 (Cascade is correct) | C: Argued cascade is architecturally correct | While semantically equivalent, the `dirty_outputs`/`_step_needs_rerun` approach is more explicit and testable |
| S-001 (Bug-centric organization) | B: Phase-centric organization | Keeping A's bug-centric structure as it's the base; content additions follow A's pattern |

---

## Risk Summary

| Risk Level | Count | Changes |
|------------|-------|---------|
| Low | 13 | #1, #2, #3, #4, #6, #8, #10, #11, #12, #13, #14, #16, #17, #18 |
| Medium | 3 | #5, #7, #9 |
| High | 0 | -- |

The three medium-risk changes (#5 ResumableConfig, #7 state-driven paths, #9 parallel group semantics) modify core logic. They should be reviewed together as they interact within `_apply_resume`.

---

## Review Status
- **Status**: Auto-approved
- **Timestamp**: 2026-03-18T00:00:00Z
