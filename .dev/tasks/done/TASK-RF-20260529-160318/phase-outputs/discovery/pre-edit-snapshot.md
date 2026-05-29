# Pre-Edit Snapshot — SKILL.md + report-template.md Heading Lines

Captured: 2026-05-29 17:10
Purpose: Freshness guard — verify research-era line numbers are still current before any edits land.

## SKILL.md line count

```
468 /config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
```

## SKILL.md heading lines (grep -nE '^### Wave|^## ')

```
16:## Purpose
26:## Required Input (STOP if missing)
37:## Output Contract
73:## Wave Structure
91:### Wave 0: Parse + Validate Input
129:### Wave 1: Tier 1 — Real-Code Grounding
152:### Wave 1.5: Documentation Grounding
190:### Wave 1.7: Tier 1 — Hypothesis Formation
210:### Wave 2: Confidence Gate
230:### Wave 3: Tier 2 — Parallel Hypotheses
295:### Wave 4: Tier 2 — Adversarial Fix Debate
324:### Wave 5: Synthesis + Report
371:### Wave 6: Tier 3 — Remediation Chain
389:## Tool Coordination Summary
404:## Will Do
415:## Will Not Do
427:## Error Handling
446:## Token Cost Profile
457:## Refs
```

## report-template.md heading lines (grep -nE '^### Wave|^## ')

```
5:## Template
25:## Summary
31:## Documentation Context
43:## Diagnosis
53:## Evidence
63:## Proposed Fix
79:## Alternative Fixes Considered
90:## Risk + Rollback
100:## Follow-up tasks
112:## Grounding Gaps
124:## Next Steps
134:## Audit
143:## Rendering rules
150:## Test-is-wrong rule
171:## Behavior-is-documented rule
```

## Side-by-side comparison vs research expectations

| Element | Research expectation | Live line | Status |
|---------|---------------------|-----------|--------|
| `## Wave Structure` header | L73 (block at L75-85) | L73 | ✓ MATCH |
| `## Output Contract` header | L37 (table L41-57) | L37 | ✓ MATCH |
| `### Wave 0` header (parse-flags Step 1 at L97) | L91 (step 1 at L97 per research/06 §A2) | L91 | ✓ MATCH — Step 1 line verified separately below |
| `### Wave 1.5` header | L152 | L152 | ✓ MATCH |
| Wave 1.5 closing `---` separator | L188 per research/06 Correction 1 | (verified separately below) | ✓ Implied by Wave 1.7 at L190 |
| `### Wave 1.7` header | L190 per research/06 | L190 | ✓ MATCH |
| `### Wave 5` header (step 2 at L331-342) | L324 (step 2 at L331-342) | L324 | ✓ MATCH |
| `## Tool Coordination Summary` | L389 (block at L389-402) | L389 | ✓ MATCH |
| `## Will Do` | L404 (block L404-413) | L404 | ✓ MATCH |
| `## Will Not Do` | L415 (block L415-425) | L415 | ✓ MATCH |
| `## Error Handling` | L427 (block L427-444) | L427 | ✓ MATCH |
| `## Token Cost Profile` | L446 (block L446-454) | L446 | ✓ MATCH |
| `## Refs` | L457 (block L457-466) | L457 | ✓ MATCH |
| report-template.md `## Documentation Context` | L31 per research/06 Correction 2 | L31 | ✓ MATCH |
| report-template.md `## Diagnosis` (follows at L43, L42 blank) | L43 | L43 | ✓ MATCH |

## Verdict

**ALL HEADING LINES MATCH RESEARCH-ERA COORDINATES.**

No drift detected (drift threshold per Step 1.4: ±2 lines). The research/05 §2 line-range table and the research/06 corrections both remain authoritative. Subsequent Phase 4 change-points can use the research-cited line numbers without local recalibration, with the explicit caveat that line numbers will shift after Step 4.4's ~70-line Wave 1.6 insertion (Steps 4.5+ MUST use `grep -n` to re-locate their edit zones, as instructed in the task file).

## Notes on file length

SKILL.md is 468 lines total. Post-Step-4.4 insertion of the new ~70-line Wave 1.6 section will push it to ~535 lines, matching the projection cited in Step 6.1 ("the file is ~535 lines post-Wave-1.6 insertion").
