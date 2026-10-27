# Merge Log: Resume Fix Design Spec

**Base**: Variant A (`brainstorm-resume-fix-A.md`) -- score 0.918
**Incorporated**: Variant B (`brainstorm-resume-fix-B.md`), Variant C (`brainstorm-resume-fix-C.md`)
**Output**: `merged-resume-fix.md`
**Date**: 2026-03-18
**Changes applied**: 18 of 18

---

## Applied Changes

### Change #1: Add `--depth` coverage section after Bug 1
- **Source**: Variant B, Section 4 ("Does `--depth` Have the Same Bug?")
- **Risk**: LOW (additive)
- **Integration point**: New subsection under Bug 1, after Edge Cases table
- **Before**: Bug 1 covered only `--agents`
- **After**: Added `--depth` Coverage subsection explaining same detection pattern applies
- **Validation**: Section fits naturally after edge cases; no heading conflicts

### Change #2: Add CLI option audit table
- **Source**: Variant B, Section 4 ("Other Options to Audit" table)
- **Risk**: LOW (additive)
- **Integration point**: New top-level section before Test Plan
- **Before**: No audit of all CLI options
- **After**: Added "CLI Option Audit" section with risk ratings for all 6 options
- **Validation**: Table data consistent with Bug 1 fix; only --agents and --depth need None-default

### Change #3: Add fix interaction matrix
- **Source**: Variant B, Section 5 ("Interaction Between Fixes" table)
- **Risk**: LOW (additive)
- **Integration point**: New subsection under Implementation Order
- **Before**: Implementation order listed but no analysis of partial application
- **After**: Added interaction matrix showing what happens with each fix applied alone; identified Bug 1 + Bug 4 as minimum viable fix
- **Validation**: Matrix conclusions consistent with fix descriptions

### Change #4: Add differential depth/agents treatment rationale
- **Source**: Variant C, Section 4 ("The `--depth` Problem", subsections 4.1-4.2)
- **Risk**: LOW (additive)
- **Integration point**: New subsection under Bug 1, after --depth coverage
- **Before**: No explanation of why depth and agents are treated differently on resume
- **After**: Added "Differential Treatment" subsection explaining agents=always-restore vs depth=auto-restore-with-warning
- **Validation**: Rationale consistent with Variant C's analysis of depth affecting single step

### Change #5: Replace `get_parameter_source` approach with None-default + source detection
- **Source**: Variant B, Section 3 (Fix 1b: None-default approach)
- **Risk**: MEDIUM (replaces core detection mechanism in Bug 1)
- **Integration point**: Bug 1 Fix section -- all 3 code changes rewritten
- **Before**: Base Variant A used `get_parameter_source()` alone with string defaults
- **After**: Combined approach: Change Click defaults to `None`, use `get_parameter_source()` as belt-and-suspenders, pass `agents_explicit`/`depth_explicit` booleans to executor. `_restore_from_state()` handles both agents and depth
- **Validation**: Code blocks compile logically; key invariant preserved ("_build_steps never called until config resolved"); backward compatible via default `True` for explicit flags

### Change #6: Add `--on-conflict` flag design
- **Source**: Variant B Section 2 (defensive check suggestion) + Variant C Section 3.1 (guard approach)
- **Risk**: LOW (additive new feature)
- **Integration point**: New top-level section between Bug 4 and Implementation Order
- **Before**: No mechanism for non-interactive conflict resolution
- **After**: Added `--on-conflict ask|override|fail` flag with implementation code
- **Validation**: Default `ask` preserves current behavior; `fail` mode useful for CI

### Change #7: Add state-driven path resolution to Bug 3
- **Source**: Variant C, Section 3.2 ("State-Driven Path Resolution")
- **Risk**: MEDIUM (modifies _apply_resume control flow)
- **Integration point**: Integrated into `_step_needs_rerun()` helper and `_apply_resume()` body
- **Before**: `_apply_resume` always used config-derived paths for gate checks
- **After**: `_apply_resume` builds `state_paths` dict from state file; `_step_needs_rerun` uses state-recorded path when available, falling back to config-derived path
- **Validation**: Test 8 (state-driven path resolution) validates this behavior; defense-in-depth complements Bug 1 fix

### Change #8: Extract `_step_needs_rerun()` helper
- **Source**: Variant B, Section 3 (Fix 3: `_step_needs_rerun` function)
- **Risk**: MEDIUM (structural refactor of _apply_resume)
- **Integration point**: New standalone function called by `_apply_resume()`
- **Before**: Rerun logic inlined in `_apply_resume()` loop
- **After**: Extracted to `_step_needs_rerun()` returning `(bool, str)` tuple with reason; integrates state-driven paths (Change #7) and force_extract check
- **Validation**: Testable in isolation (Tests 7, 8, 16); reason string enables cascade logging (Change #11)

### Change #9: Add parallel group semantics to Bug 3
- **Source**: Variant C, Section 3.3 + Variant A's existing parallel group handling
- **Risk**: MEDIUM (modifies parallel group re-run logic)
- **Integration point**: Within `_apply_resume()` parallel group handling
- **Before**: Base Variant A already handled parallel groups but with found_failure cascade
- **After**: Groups checked per-step via `_step_needs_rerun`; if any step needs rerun, entire group reruns; all group outputs marked dirty (atomic group completion); group_index tracking for high-water-mark
- **Validation**: Consistent with existing pipeline semantics; Test 7 (dirty propagation) validates transitive group behavior

### Change #10: Add no-progress guard to Bug 4's `_save_state`
- **Source**: Variant C, Section 3.4 ("Conditional State Writes")
- **Risk**: LOW (additive guard)
- **Integration point**: Top of `_save_state()` function body
- **Before**: `_save_state` wrote unconditionally
- **After**: Two guards: (1) no-progress guard refuses write when zero steps PASS; (2) agent-mismatch guard refuses write when agents differ from state and no generate step ran
- **Validation**: Test 10 validates no-progress guard; Test 9 validates agent preservation

### Change #11: Add cascade logging to Bug 3
- **Source**: Variant C, Section 3.3 (cascade logging code)
- **Risk**: LOW (observability only)
- **Integration point**: Within `_apply_resume()` at rerun decision points
- **Before**: No logging of which steps rerun or why
- **After**: `_log.info()` calls at each rerun decision with step name and reason string from `_step_needs_rerun`
- **Validation**: Does not affect behavior; reason strings propagated from Change #8

### Change #12: Expand backward compatibility into migration analysis
- **Source**: Variant B, Section 7 ("Migration / Backward Compatibility") + Variant C Section 6 (Click's is_eager problem)
- **Risk**: LOW (documentation expansion)
- **Integration point**: Replaced Base Variant A's brief backward compatibility section
- **Before**: 4 bullet points about compatibility
- **After**: 3 subsections: State File Format Migration (with scenario table), CLI Interface Compatibility, Behavioral Changes (before/after table)
- **Validation**: All behavioral changes documented accurately match code changes

### Change #13: Expand test plan from 6 to ~17 tests
- **Source**: Variant B, Section 6 (unit + integration + edge case tests) + Variant C, Section 8 (guard tests)
- **Risk**: LOW (additive)
- **Integration point**: Test Plan section reorganized into subsections by bug area
- **Before**: 6 tests (Tests 1-6 from Base Variant A)
- **After**: 17 tests organized as: Unit Tests (Bug 1: Tests 1-4), Unit Tests (Bug 2: Test 5), Unit Tests (Bug 3: Tests 6-8), Unit Tests (Bug 4: Tests 9-10), Integration Tests (Tests 11-13), Edge Case Tests (Tests 14-17)
- **Validation**: All original 6 tests preserved; new tests cover depth restoration, dirty propagation, state-driven paths, no-progress guard, double resume stability, explicit override, corrupted state, changed spec, reason strings, atomic write safety

### Change #14: Add 5-layer defense summary section
- **Source**: Variant C, Section 5 ("Defense in Depth: Layered Guard Summary")
- **Risk**: LOW (additive summary)
- **Integration point**: New subsection at end of Problem Summary, before Bug 1
- **Before**: No overview of defense layers
- **After**: Summary table mapping 5 defense layers to the bugs they address
- **Validation**: Layer descriptions match corresponding fix sections

### Change #15: Add depth/agent coupling WARNING validation
- **Source**: Variant C, Section 4.2 (depth/agents coupling analysis)
- **Risk**: LOW (additive note)
- **Integration point**: Blockquote after Differential Treatment subsection in Bug 1
- **Before**: No warning about depth/agent combination validity
- **After**: WARNING blockquote noting that overriding --agents without --depth may produce different quality outputs
- **Validation**: Warning is advisory, not blocking; consistent with differential treatment rationale

### Change #16: Note dirty-output propagation requires topological order
- **Source**: Variant C, Section 3.3 ("Counter-argument and why the cascade exists")
- **Risk**: LOW (additive note)
- **Integration point**: Blockquote at end of Bug 3 section
- **Before**: "Why This Is Safe" section mentioned pipeline order but not the invariant
- **After**: Added explicit note that `steps` list MUST be topologically sorted; current pipeline already guarantees this
- **Validation**: Note is a correctness constraint; consistent with Base Variant A's "forward pass is sufficient" statement

### Change #17: Note state file should use write-then-rename atomicity
- **Source**: Variant C, Section 3.4 (reference to atomic write in _save_state)
- **Risk**: LOW (additive note + code change)
- **Integration point**: Added `os.replace()` atomic write to `_save_state()` code block + explanatory blockquote
- **Before**: Base Variant A's `_save_state` used implicit write_text
- **After**: Explicit `tmp_path.write_text() + os.replace()` pattern; note explains POSIX vs Windows atomicity
- **Validation**: Test 17 validates crash safety

### Change #18: Add estimated diff size
- **Source**: Variant B, Section 8 (estimated diff size line)
- **Risk**: LOW (additive metadata)
- **Integration point**: New subsection under Files Changed table
- **Before**: No size estimate
- **After**: Table with per-file line counts: ~225 added, ~50 modified, ~30 removed in production code; ~120 lines test code
- **Validation**: Estimates derived from code block sizes in merged document

---

## Structural Integrity Checks

| Check | Status |
|-------|--------|
| Heading hierarchy (no skipped levels) | PASS -- h1 > h2 > h3 throughout |
| Section ordering logic | PASS -- Problem > Bug 1-4 > Conflict Resolution > Implementation Order > Files > CLI Audit > Test Plan > Risk > Backward Compatibility |
| Internal cross-references | PASS -- all "Change #N" annotations reference valid sections; test numbers sequential 1-17 |
| Code block consistency | PASS -- function signatures match across Bug 1 (commands.py, executor.py, helper) |
| Provenance annotations | PASS -- all sections have `<!-- Source: ... -->` comments |

## Issues Encountered

None. All 18 changes were additive or replacement changes that integrated cleanly into Variant A's bug-centric structure.
