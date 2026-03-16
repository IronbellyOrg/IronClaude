# Evidence: D-0018 — Phase Result File Generation

## Task
T03.03 — Implement Phase Result File Generation

## Output Path
`config.result_file(phase)` → `results/phase-<N>-result.md`

## Implementation
After all tasks complete per phase:
1. Build `AggregatedPhaseReport` from task results
2. Call `report.to_markdown()` to generate content
3. Call `_inject_source_field(markdown)` to insert `source: preflight` into YAML frontmatter
4. Write to `config.result_file(phase)` via `Path.write_text()`
5. Parent directory created via `mkdir(parents=True, exist_ok=True)`

## Result File Structure (PASS example)

```markdown
---
phase: 1
status: PASS
tasks_total: 1
tasks_passed: 1
tasks_failed: 0
source: preflight
---

# Phase 1 — Aggregated Task Report

| Task ID | Title | Status | Turns | Duration |
|---------|-------|--------|-------|----------|
| T01.01 | ... | pass | 0 | 0.0s |

**Total turns consumed:** 0
**Total duration:** 0.0s

EXIT_RECOMMENDATION: CONTINUE
```

## YAML Frontmatter Fields
- `phase`: phase number
- `status`: PASS / FAIL / PARTIAL
- `tasks_total`, `tasks_passed`, `tasks_failed`: counts
- `source: preflight` (injected by `_inject_source_field()`)

## EXIT_RECOMMENDATION Logic
- `AggregatedPhaseReport.status == "PASS"` → `EXIT_RECOMMENDATION: CONTINUE`
- Any other status → `EXIT_RECOMMENDATION: HALT`

## Verification

Test command: `uv run pytest tests/sprint/test_preflight.py -v -k "result_file or result_parseable or compatibility"` — 5 passed

- `test_result_parseable`: PASS result file parsed by `_determine_phase_status()` → PhaseStatus.PASS
- `test_result_file_halt_parseable`: HALT result file → PhaseStatus.HALT
- `test_result_file_contains_source_preflight`: `source: preflight` present in result file
