# Gaps and Questions — PRD Pipeline Integration Research

**Compiled from:** analyst-completeness-report.md, qa-research-gate-report.md, qa-research-gate-fix-cycle-1.md
**Date:** 2026-03-27

## Resolved (Fix Cycle 1)

| # | Issue | Severity | Resolution |
|---|-------|----------|------------|
| 1 | File 04 proposed `detect_input_type()` extension for PRD mode | CRITICAL | Corrected — PRD is supplementary only, no mode changes |
| 2 | File 04 status header said "In Progress" | MINOR | Fixed — now "Complete" |
| 3 | File 04 referenced nonexistent PRD template path | IMPORTANT | Fixed — now points to `src/superclaude/skills/prd/SKILL.md` |
| 4 | File 04 proposed `--supplementary-file` generalization | IMPORTANT | Resolved — using `--prd-file` per design decision |

## Open Questions (for synthesis to address or defer)

| # | Question | Source | Severity | Impact |
|---|----------|--------|----------|--------|
| 1 | ~~`tdd_file` on `RoadmapConfig` is dead code — should PRD integration fix this?~~ **RESOLVED:** Yes — wire both `tdd_file` AND `prd_file` through roadmap CLI and executor in one pass. Same files, same pattern, consistent treatment. | File 01 | Important | RESOLVED — included in implementation plan Phase 1, steps 1.1.2-1.1.7 |
| 2 | 7 of 9 prompt builders need refactoring from single-return to base-pattern | File 02 | Important | Increases implementation scope beyond just adding PRD blocks |
| 3 | PRD supplementary task generation is weaker than TDD | File 04 | Minor | PRD content informs task descriptions but doesn't generate 1:1 tasks |
| 4 | spec-panel is inference-only — no Python CLI backing | File 04 | Minor | PRD additions to spec-panel only update protocol doc |
| 5 | Deferred TDD generate prompt comment at prompts.py:309-316 | File 02 | Minor | Could be addressed alongside PRD integration |
| 6 | `gates.py` received minimal investigation -- only a one-line mention ("no new gates needed") with no cited gate constants | File 01 / Analyst report | Minor | Likely correct but unverified; confirm EXTRACT_GATE etc. during implementation |
| 7 | PRD template file (`src/superclaude/examples/prd_template.md`) was never directly read by any research agent; section inventory sourced from `prd/SKILL.md` instead | Files 02/04/05 / Analyst report | Important | Cross-validate section numbering against actual template before drafting prompt blocks |
| 8 | File 01 describes "9-step pipeline" but actual executor has 11 step entries (including anti-instinct and certify) | Files 01/05 / QA phase-2 review | Minor | Cosmetic -- both counts are correct at different scopes; clarify in synthesis |
