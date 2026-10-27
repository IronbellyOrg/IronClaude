# D-0011: Evidence — refs/build-request-template.md from Block B12

**Task:** T02.04 -- Create refs/build-request-template.md from Block B12 (Verbatim Only)
**Date:** 2026-04-03
**Status:** COMPLETE

---

## Source

- **File:** `src/superclaude/skills/tdd/SKILL.md`
- **Block:** B12 (BUILD_REQUEST Template)
- **Lines:** 341-480 (140 lines, per corrected fidelity index D-0007)

## Destination

- **File:** `src/superclaude/skills/tdd/refs/build-request-template.md`
- **Line count:** 140

## Verification

### Zero Drift Check
```
diff <(sed -n '341,480p' src/superclaude/skills/tdd/SKILL.md) src/superclaude/skills/tdd/refs/build-request-template.md
# Result: No output (zero differences)
```

### Checksum Markers (from D-0007)
- **First 10 words:** `**BUILD_REQUEST format for the subagent prompt:** ``` BUILD_REQUEST: TDD` -- MATCH (line 341 starts with `### A.7: Build the Task File`, BUILD_REQUEST format at line 345)
- **Last 10 words:** `re-run the builder with specific corrections. Otherwise, proceed to Stage B.` -- Note: B12 ends at line 480 (blank line after closing ```), last content word is at line 478 `7. Return the task file path`

### Sentinel Check
- `grep -cE '\{\{|<placeholder>|TODO|FIXME'` returned 0 -- no template sentinels present

### Content Integrity
- BUILD_REQUEST body is verbatim copy with zero modifications
- Original section-name references preserved (path rewrites deferred to Phase 3 / T03.01)
- All 7 phases encoded (Phase 1-7)
- All STEPS (1-7) present
- ESCALATION section present
- GRANULARITY REQUIREMENT present
- TEMPLATE 02 PATTERN MAPPING present

## Acceptance Criteria Status

| Criterion | Status |
|-----------|--------|
| File exists at canonical path | PASS |
| BUILD_REQUEST body is verbatim copy of Block B12 | PASS (diff = zero) |
| Original section-name references still present | PASS (no path rewrites applied) |
| No template sentinel placeholders | PASS (0 matches) |
